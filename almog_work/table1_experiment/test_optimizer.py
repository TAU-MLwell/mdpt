"""Loop tests with injected chat/scoring functions and synthetic data only."""
import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

from almog_work.table1_experiment.optimizer import (
    MAX_GUIDANCE_CHARS, build_optimizer_messages, propose_guidance, run_loop,
)
from almog_work.table1_experiment.run_experiment import run_experiment
from almog_work.table1_experiment.test_experiment import SOURCE, public_report, table

BASE = {"version": "base", "system": "SYSTEM_TEXT",
        "user": "FIXED_FORMAT\nGuidance:\n__GUIDANCE__\nTable:\n__TABLE_TEXT__",
        "guidance": "start guidance"}
EXAMPLE = {"paper": "synthetic", "error_type": "missing_cell", "row_group": None,
           "row_label": "ExampleRow", "column_label": "ExampleCol", "predicted_value": None}


def report_with(f1, examples=(), evaluations_remaining=10):
    report = copy.deepcopy(public_report())
    report["summary"]["cells"]["f1"] = f1
    report["per_paper"][0]["cell_f1"] = f1
    report["error_examples"] = list(examples)
    report["evaluations_remaining"] = evaluations_remaining
    return report


class LoopFixture(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.paper = self.root / "synthetic.txt"
        self.paper.write_text(SOURCE, encoding="utf-8")
        self.prompt = self.root / "base.json"
        self.prompt.write_text(json.dumps(BASE), encoding="utf-8")
        self.optimizer_messages = []
        self.score_calls = 0

    def scorer(self, f1_values, examples=(), evaluations_remaining=10):
        values = iter(f1_values)
        def score(predictions):
            self.score_calls += 1
            return report_with(next(values), examples, evaluations_remaining)
        return score

    def optimizer(self):
        counter = iter(range(1, 100))
        def chat(messages, max_new_tokens):
            self.optimizer_messages.append(messages)
            return json.dumps({"guidance": f"improved guidance {next(counter)}"})
        return chat

    def loop(self, f1_values, **kwargs):
        options = dict(prompt_path=self.prompt, extract_chat_fn=lambda **kw: json.dumps(table()),
                       optimizer_chat_fn=self.optimizer(), score_fn=self.scorer(f1_values))
        options.update(kwargs)
        return run_loop({"synthetic": self.paper}, self.root / "loop", **options)


class LoopTests(LoopFixture):
    def test_loop_improves_logs_and_keeps_fixed_format(self):
        state = self.loop([0.2, 0.4, 0.5], max_iterations=2)
        self.assertEqual(state["status"], "completed")
        self.assertEqual((state["baseline_cell_f1"], state["best_cell_f1"]), (0.2, 0.5))
        self.assertEqual(state["best_version"], "v02")
        self.assertEqual(state["stop_reason"], "max_iterations")
        best = json.loads((self.root / "loop" / "best_prompt.json").read_text())
        self.assertEqual(best["guidance"], "improved guidance 2")
        for version in ("v00", "v01", "v02"):
            prompt = json.loads((self.root / "loop" / "prompts" / f"{version}.json").read_text())
            self.assertEqual((prompt["user"], prompt["system"]), (BASE["user"], BASE["system"]))
        with (self.root / "loop" / "results.csv").open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([r["version"] for r in rows], ["base", "v01", "v02"])
        self.assertEqual([r["is_best"] for r in rows], ["False", "False", "True"])
        self.assertIn("f1_synthetic", rows[0])

    def test_progress_reports_phases_without_content(self):
        messages = []
        self.loop([0.2, 0.4], max_iterations=1, progress=messages.append)
        text = "\n".join(messages)
        for expected in ("[baseline] extracting", "[baseline] done", "[iteration 1/1] asking",
                         "guidance written", "[iteration 1/1] done", "extracting synthetic"):
            self.assertIn(expected, text)
        self.assertNotIn("improved guidance", text)
        self.assertNotIn(SOURCE, text)

    def test_repeated_cells_are_counted_in_the_log_and_reported_by_count_only(self):
        repeated = table()
        repeated["cells"] = repeated["cells"] + [dict(repeated["cells"][0], value="REPEAT_SECRET")]
        self.loop([0.2, 0.3], max_iterations=1, extract_chat_fn=lambda **kw: json.dumps(repeated))
        log = json.loads((self.root / "loop" / "runs" / "v00" / "run.json").read_text())
        self.assertEqual(log["papers"][0]["duplicates_dropped"], 1)
        text = json.dumps(self.optimizer_messages)
        self.assertIn("synthetic=1", text)
        self.assertNotIn("REPEAT_SECRET", text)

    def test_invalid_output_papers_are_reported_to_the_optimizer_by_key_only(self):
        self.loop([0.2, 0.3], max_iterations=1,
                  extract_chat_fn=lambda **kw: '{"SECRET_MODEL_OUTPUT":')
        text = json.dumps(self.optimizer_messages)
        self.assertIn("scored as empty: synthetic", text)
        self.assertNotIn("SECRET_MODEL_OUTPUT", text)

    def test_stops_after_patience_without_improvement(self):
        state = self.loop([0.4, 0.4, 0.39, 0.9], max_iterations=4, patience=2)
        self.assertEqual(state["stop_reason"], "no_improvement")
        self.assertEqual(state["iterations_run"], 2)
        self.assertEqual(state["best_version"], "base")

    def test_no_patience_runs_every_iteration_even_without_gain(self):
        state = self.loop([0.4, 0.4, 0.39, 0.38], max_iterations=3, patience=None)
        self.assertEqual(state["stop_reason"], "max_iterations")
        self.assertEqual(state["iterations_run"], 3)
        self.assertEqual(state["best_version"], "base")

    def test_small_gain_below_threshold_counts_as_no_improvement(self):
        state = self.loop([0.4, 0.401, 0.402], max_iterations=4, patience=2, min_improvement=0.005)
        self.assertEqual(state["stop_reason"], "no_improvement")
        self.assertEqual(state["best_version"], "v02")

    def test_stops_when_evaluation_budget_is_exhausted(self):
        state = self.loop([0.1, 0.2], max_iterations=4,
                          score_fn=self.scorer([0.1, 0.2], evaluations_remaining=0))
        self.assertEqual(state["stop_reason"], "evaluation_budget")
        self.assertEqual(self.score_calls, 1)

    def test_optimizer_never_sees_article_text_or_predictions(self):
        self.loop([0.2, 0.3], max_iterations=1, score_fn=self.scorer([0.2, 0.3], [EXAMPLE]))
        text = json.dumps(self.optimizer_messages)
        self.assertIn("ExampleRow", text)
        self.assertIn("FIXED_FORMAT", text)
        self.assertIn("start guidance", text)
        for forbidden in ("Variable", "Study A", "Events", "Synthetic table", "predictions/"):
            self.assertNotIn(forbidden, text)

    def test_reused_baseline_saves_an_evaluation(self):
        baseline_run = self.root / "earlier_run"
        run_experiment({"synthetic": self.paper}, baseline_run, prompt_path=self.prompt,
                       chat_fn=lambda **kw: json.dumps(table()),
                       score_fn=lambda predictions: report_with(0.3))
        state = self.loop([0.5], max_iterations=1, reuse_baseline=baseline_run)
        self.assertEqual(self.score_calls, 1)
        self.assertTrue(state["baseline_reused"])
        self.assertEqual(state["baseline_cell_f1"], 0.3)

    def test_reused_baseline_must_match_the_prompt(self):
        baseline_run = self.root / "earlier_run"
        other = dict(BASE, guidance="different guidance")
        other_path = self.root / "other.json"
        other_path.write_text(json.dumps(other), encoding="utf-8")
        run_experiment({"synthetic": self.paper}, baseline_run, prompt_path=other_path,
                       chat_fn=lambda **kw: json.dumps(table()),
                       score_fn=lambda predictions: report_with(0.3))
        with self.assertRaises(ValueError):
            self.loop([0.5], reuse_baseline=baseline_run)
        self.assertEqual(json.loads((self.root / "loop" / "loop.json").read_text())["status"], "failed")

    def test_failure_is_logged_without_content_and_not_retried(self):
        with self.assertRaises(ValueError):
            self.loop([0.2, 0.3], max_iterations=2,
                      optimizer_chat_fn=lambda messages, max_new_tokens: "SECRET_OPTIMIZER_OUTPUT")
        text = (self.root / "loop" / "loop.json").read_text()
        self.assertNotIn("SECRET_OPTIMIZER_OUTPUT", text)
        state = json.loads(text)
        self.assertEqual((state["status"], state["failure"]["stage"]),
                         ("failed", "iteration_1_propose"))
        self.assertTrue((self.root / "loop" / "results.csv").exists())

    def test_existing_directory_and_bad_settings_are_rejected(self):
        (self.root / "loop").mkdir()
        with self.assertRaises(ValueError):
            self.loop([0.1])
        for kwargs in ({"max_iterations": 0}, {"patience": 0}, {"min_improvement": -1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_loop({"synthetic": self.paper}, self.root / "fresh", prompt_path=self.prompt,
                         **kwargs)
        self.assertFalse((self.root / "fresh").exists())

    def test_prompt_without_guidance_is_rejected(self):
        plain = {"version": "x", "system": "s", "user": "u __TABLE_TEXT__"}
        self.prompt.write_text(json.dumps(plain), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.loop([0.1])


class ProposeGuidanceTests(unittest.TestCase):
    history = [{"prompt": BASE, "report": report_with(0.2, [EXAMPLE])}]

    def propose(self, reply):
        return propose_guidance(BASE, self.history, chat_fn=lambda messages, max_new_tokens: reply)

    def test_valid_guidance_is_returned_stripped_and_fenced_json_is_accepted(self):
        self.assertEqual(self.propose('{"guidance": "  new text  "}'), "new text")
        self.assertEqual(self.propose('```json\n{"guidance": "fenced"}\n```'), "fenced")

    def test_invalid_replies_are_rejected(self):
        bad = ['{"guidance": ""}', '{"guidance": 5}', '{"guidance": "x", "other": 1}',
               '{"guidance": "start guidance"}', '{"guidance": "has __TABLE_TEXT__"}',
               '{"guidance": "has __GUIDANCE__"}', "not json",
               json.dumps({"guidance": "x" * (MAX_GUIDANCE_CHARS + 1)})]
        for reply in bad:
            with self.subTest(reply=reply[:30]), self.assertRaises(ValueError):
                self.propose(reply)

    def test_retries_invalid_reply_up_to_three_times(self):
        replies = iter(["bad", "bad", '{"guidance": "third time"}'])
        result = propose_guidance(BASE, self.history,
                                  chat_fn=lambda messages, max_new_tokens: next(replies))
        self.assertEqual(result, "third time")

    def test_retry_tells_the_model_why_it_was_rejected(self):
        seen = []
        replies = iter([json.dumps({"guidance": "x" * (MAX_GUIDANCE_CHARS + 39)}),
                        '{"guidance": "short enough"}'])
        def chat(messages, max_new_tokens):
            seen.append(messages)
            return next(replies)
        self.assertEqual(propose_guidance(BASE, self.history, chat_fn=chat), "short enough")
        rejection = seen[1][-1]["content"]
        self.assertIn(str(MAX_GUIDANCE_CHARS + 39), rejection)
        self.assertIn("Rewrite it at about 3000", rejection)
        self.assertEqual(len(seen[0]), 2)

    def test_messages_contain_scores_and_feedback_only(self):
        text = json.dumps(build_optimizer_messages(BASE, self.history))
        self.assertIn("0.2", text)
        self.assertIn("ExampleRow", text)
        self.assertNotIn("__TABLE_TEXT__", text.replace("<table text>", ""))


if __name__ == "__main__":
    unittest.main()
