"""Synthetic-only tests: never load the repository's reviewed gold tables."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from score_table_extraction import (
    aggregate_scores, compare_paper, load_cells, normalize_text, sample_errors,
)


def cell(value="42", row="Age", group="Demographics", column="Study A"):
    return dict(row_label=row, row_group=group, column_label=column, value=value)


class ScorerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.gold = Path(self.tmp.name) / "synthetic_table_1_gold.json"
        self.pred = Path(self.tmp.name) / "synthetic_table_1_pred.json"

    def write(self, path, cells):
        path.write_text(json.dumps({"cells": cells}), encoding="utf-8")

    def compare(self, gold, pred):
        self.write(self.gold, gold)
        self.write(self.pred, pred)
        return compare_paper(self.gold, self.pred)

    def test_perfect_match_and_order_independence(self):
        a, b = cell(), cell("7", row="Count")
        score, errors = self.compare([a, b], [b, a])
        self.assertEqual(aggregate_scores([score])["cells"]["f1"], 1)
        self.assertEqual(errors, [])

    def test_missing_and_extra(self):
        score, errors = self.compare([cell(), cell(row="Missing")],
                                     [cell(), cell(row="Extra")])
        self.assertEqual((score.tp_exact, score.fp_exact, score.fn_exact), (1, 1, 1))
        self.assertEqual({e.error_type for e in errors}, {"missing_cell", "extra_cell"})

    def test_wrong_value_counts_as_fp_and_fn(self):
        score, errors = self.compare([cell()], [cell("43")])
        self.assertEqual((score.tp_exact, score.fp_exact, score.fn_exact), (0, 1, 1))
        self.assertEqual(score.key_tp, 1)
        self.assertEqual(errors[0].error_type, "wrong_value")

    def test_wrong_group_or_population_is_not_a_match(self):
        for prediction in [cell(group=None), cell(column="Study B")]:
            with self.subTest(prediction=prediction):
                score, _ = self.compare([cell()], [prediction])
                self.assertEqual((score.tp_exact, score.key_tp), (0, 0))

    def test_duplicate_prediction_is_penalized(self):
        score, errors = self.compare([cell()], [cell(), cell()])
        self.assertEqual((score.tp_exact, score.fp_exact, score.fn_exact), (1, 1, 0))
        self.assertEqual((score.key_tp, score.key_fp), (1, 1))
        self.assertEqual(aggregate_scores([score])["cells"]["precision"], 0.5)
        self.assertIn("duplicate_cell", [e.error_type for e in errors])

    def test_conflicting_duplicate_order_does_not_change_score(self):
        scores = []
        for predictions in [[cell(), cell("43")], [cell("43"), cell()]]:
            score, _ = self.compare([cell()], predictions)
            scores.append(aggregate_scores([score]))
        self.assertEqual(scores[0], scores[1])
        self.assertEqual(scores[0]["keys_only"]["value_accuracy_on_matched_keys"], 1)

    def test_duplicate_gold_key_is_rejected(self):
        for gold in [[cell(), cell()], [cell(), cell("43")]]:
            with self.subTest(gold=gold), self.assertRaises(ValueError):
                self.compare(gold, [cell()])

    def test_missing_prediction_file(self):
        self.write(self.gold, [cell()])
        score, errors = compare_paper(self.gold, self.pred)
        self.assertTrue(score.missing_prediction_file)
        self.assertEqual(score.fn_exact, 1)
        self.assertIsNone(errors[0].gold_value)

    def test_empty_prediction(self):
        score, _ = self.compare([cell()], [])
        self.assertEqual((score.tp_exact, score.fn_exact), (0, 1))

    def test_empty_value_is_not_missing_cell(self):
        score, _ = self.compare([cell("")], [cell("")])
        self.assertEqual(score.tp_exact, 1)

    def test_normalization_preserves_numbers_and_operators(self):
        self.assertEqual(normalize_text("  4.0 [3.5–4.4]  "), "4.0 [3.5-4.4]")
        self.assertEqual(normalize_text("≥ 20"), ">=20")
        self.assertNotEqual(normalize_text("<0.001"), normalize_text("0.001"))
        self.assertNotEqual(normalize_text("42"), normalize_text("43"))

    def test_invalid_schema_is_rejected(self):
        for data in [{}, [], {"cells": [None]}, {"cells": [{"value": "42"}]},
                     {"cells": [cell(value=42)]}]:
            self.pred.write_text(json.dumps(data), encoding="utf-8")
            with self.subTest(data=data), self.assertRaises(ValueError):
                load_cells(self.pred)

    def test_sampling_limit_seed_and_zero(self):
        _, errors = self.compare([cell(row=str(i)) for i in range(20)], [])
        self.assertEqual(len(sample_errors(errors, 3, 42)), 3)
        self.assertEqual(sample_errors(errors, 3, 42), sample_errors(errors, 3, 42))
        self.assertEqual(sample_errors(errors, 0, 42), [])
        with self.assertRaises(ValueError):
            sample_errors(errors, -1, 42)

    def test_micro_aggregation(self):
        perfect, _ = self.compare([cell()], [cell()])
        missing, _ = self.compare([cell(), cell(row="Count")], [])
        summary = aggregate_scores([perfect, missing])["cells"]
        self.assertEqual(summary["precision"], 1)
        self.assertEqual(summary["recall"], 0.333333)

    def test_cli_reports_only_capped_examples_and_metrics(self):
        root = Path(self.tmp.name)
        gold_dir, pred_dir = root / "gold", root / "pred"
        gold_dir.mkdir()
        pred_dir.mkdir()
        reference = {"cells": [cell(row=str(i)) for i in range(20)],
                     "raw_table_text": "PRIVATE_SYNTHETIC_REFERENCE"}
        (gold_dir / self.gold.name).write_text(json.dumps(reference), encoding="utf-8")
        self.write(pred_dir / self.pred.name, [])
        output = root / "report.json"
        result = subprocess.run([
            sys.executable, str(Path(__file__).with_name("score_table_extraction.py")),
            "--gold-dir", str(gold_dir), "--pred-dir", str(pred_dir),
            "--max-error-examples", "2", "--output", str(output),
        ], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report, json.loads(output.read_text(encoding="utf-8")))
        self.assertEqual(report["summary"]["cells"]["fn_exact"], 20)
        self.assertEqual(len(report["error_examples"]), 2)
        self.assertNotIn("PRIVATE_SYNTHETIC_REFERENCE", result.stdout)
        self.assertNotIn("raw_table_text", result.stdout)
        self.assertNotIn('"cells": [', result.stdout)


if __name__ == "__main__":
    unittest.main()