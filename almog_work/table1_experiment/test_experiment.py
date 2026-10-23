"""Offline orchestration and temporary synthetic HTTP integration tests."""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

from almog_work.table1_experiment.extractor import (
    _parse_table_json, DEFAULT_PROMPT_PATH, extract_table_one, find_table_section,
    render_user_prompt, validate_prompt_config, validate_table_result,
)
from almog_work.table1_experiment.run_experiment import (
    DATA_DIR, DEFAULT_CONFIG_PATH, load_split, run_experiment,
)
from almog_work.table1_experiment.scorer_client import (
    ScoringError, score_predictions, validate_connection, validate_public_report,
)

TOKEN = "synthetic-private-token-for-testing-only"
SOURCE = "Table 1. Synthetic table\nVariable\nStudy A\nStudy B\nEvents\n0\nNote: stop"


def table(value="0"):
    return {"table_title": "Synthetic table", "columns": ["Variable", "Study A", "Study B"],
            "cells": [{"row_group": None, "row_label": "Events", "column_label": "Study A",
                       "value": value}]}


def public_report():
    return {
        "summary": {"papers_scored": 1,
                    "cells": {"tp_exact": 1, "fp_exact": 0, "fn_exact": 0,
                              "precision": 1.0, "recall": 1.0, "f1": 1.0},
                    "keys_only": {"tp": 1, "fp": 0, "fn": 0,
                                  "precision": 1.0, "recall": 1.0, "f1": 1.0,
                                  "value_accuracy_on_matched_keys": 1.0},
                    "missing_prediction_files": []},
        "per_paper": [{"paper": "synthetic", "gold_cells": 1, "pred_cells": 1,
                       "missing_prediction_file": False,
                       "cell_precision": 1.0, "cell_recall": 1.0, "cell_f1": 1.0,
                       "key_precision": 1.0, "key_recall": 1.0,
                       "value_accuracy_on_matched_keys": 1.0}],
        "error_examples": [], "feedback_remaining": 5, "evaluations_remaining": 2,
    }


class ExperimentFixture(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.paper = self.root / "synthetic.txt"
        self.paper.write_text(SOURCE, encoding="utf-8")
        self.prompt = self.root / "candidate.json"
        self.config = {"version": "synthetic-v1", "system": "ONLY_SOURCE_AND_PROMPT",
                       "user": "Extract Table 1:\n__TABLE_TEXT__", "ignored_metadata": "NOT_SNAPSHOTTED"}
        self.prompt.write_text(json.dumps(self.config), encoding="utf-8")
        self.output = self.root / "run_01"

    def execute(self, **kwargs):
        options = {"prompt_path": self.prompt, "chat_fn": lambda **kw: json.dumps(table()),
                   "score_fn": lambda predictions: public_report()}
        options.update(kwargs)
        return run_experiment({"synthetic": self.paper}, self.output, **options)


class RunnerTests(ExperimentFixture):
    def test_complete_run_snapshots_logs_and_sends_only_cells(self):
        messages, requests = [], []
        def chat(**kwargs):
            messages.extend(kwargs["messages"])
            return json.dumps(table())
        def score(predictions):
            requests.append(copy.deepcopy(predictions))
            # Later file changes must not affect the snapshot already used.
            self.prompt.write_text("changed", encoding="utf-8")
            return public_report()
        report = self.execute(chat_fn=chat, score_fn=score, model_label="synthetic-model", max_new_tokens=1234)
        self.assertEqual(report["summary"]["cells"]["f1"], 1)
        self.assertEqual(len(requests), 1)
        self.assertEqual(set(requests[0]["synthetic"]), {"cells"})
        saved = json.loads((self.output / "predictions" / "synthetic_table_1_pred.json").read_text())
        self.assertEqual(saved["cells"][0]["value"], "0")
        self.assertEqual(len(saved["cells"]), 1)  # No record for blank Study B.
        snapshot = json.loads((self.output / "prompt.json").read_text())
        self.assertEqual(snapshot, {k: self.config[k] for k in ("version", "system", "user")})
        log = json.loads((self.output / "run.json").read_text())
        self.assertEqual(log["status"], "completed")
        self.assertEqual(log["model"]["max_new_tokens"], 1234)
        self.assertEqual(log["model"]["deployment"], "synthetic-model")
        self.assertEqual(log["papers"][0]["source_sha256"], hashlib.sha256(self.paper.read_bytes()).hexdigest())
        self.assertEqual(log["prompt_sha256"], hashlib.sha256(
            json.dumps(snapshot, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest())
        self.assertEqual(log["scoring"]["evaluations_remaining"], 2)
        text = json.dumps(messages)
        for forbidden in ("NOT_SNAPSHOTTED", "feedback_remaining", "gold_cells", TOKEN):
            self.assertNotIn(forbidden, text)

    def test_existing_run_is_not_overwritten_or_retried(self):
        self.execute()
        before = (self.output / "run.json").read_bytes()
        with self.assertRaises(ValueError):
            self.execute(chat_fn=lambda **kw: self.fail("No model call"))
        self.assertEqual((self.output / "run.json").read_bytes(), before)

    def test_invalid_model_output_is_scored_as_empty_and_logged_without_content(self):
        requests = []
        def score(predictions):
            requests.append(copy.deepcopy(predictions))
            return public_report()
        self.execute(chat_fn=lambda **kw: '{"SECRET_MODEL_OUTPUT":', score_fn=score)
        text = (self.output / "run.json").read_text()
        self.assertNotIn("SECRET_MODEL_OUTPUT", text)
        log = json.loads(text)
        self.assertEqual(log["status"], "completed")
        self.assertEqual(log["papers"][0]["status"], "invalid_output")
        self.assertEqual(log["papers"][0]["extraction_attempts"], 3)
        self.assertEqual(requests, [{"synthetic": {"cells": []}}])
        self.assertEqual(list((self.output / "predictions").iterdir()), [])

    def test_non_model_value_errors_are_not_retried_or_scored(self):
        calls = []
        def chat(**kw):
            calls.append(1)
            raise ValueError("deployment configuration problem")
        with self.assertRaises(ValueError):
            self.execute(chat_fn=chat, score_fn=lambda p: self.fail("No scoring call"))
        self.assertEqual(calls, [1])
        self.assertEqual(json.loads((self.output / "run.json").read_text())["status"], "failed")

    def test_invalid_output_is_retried_then_logged_and_bounded(self):
        replies = iter(['{"broken":', json.dumps(table())])
        self.execute(chat_fn=lambda **kw: next(replies))
        log = json.loads((self.output / "run.json").read_text())
        self.assertEqual(log["papers"][0]["extraction_attempts"], 2)
        self.assertEqual(log["status"], "completed")
        calls = []
        def always_bad(**kw):
            calls.append(1)
            return "{"
        run_experiment({"synthetic": self.paper}, self.root / "run_02", prompt_path=self.prompt,
                       chat_fn=always_bad, score_fn=lambda p: public_report())
        self.assertEqual(len(calls), 3)

    def test_scoring_failure_keeps_predictions_and_never_retries(self):
        calls = []
        def fail(predictions):
            calls.append(predictions)
            raise ScoringError("PRIVATE_SERVER_BODY_AND_TOKEN")
        with self.assertRaises(ScoringError):
            self.execute(score_fn=fail)
        self.assertEqual(len(calls), 1)
        text = (self.output / "run.json").read_text()
        self.assertNotIn("PRIVATE_SERVER_BODY_AND_TOKEN", text)
        self.assertEqual(json.loads(text)["failure"]["stage"], "scoring")
        self.assertTrue((self.output / "predictions" / "synthetic_table_1_pred.json").exists())
        self.assertFalse((self.output / "scores.json").exists())

    def test_unexpected_reference_fields_are_rejected_before_persistence(self):
        report = public_report()
        report["error_examples"] = [{"gold_value": "PRIVATE_REFERENCE"}]
        with self.assertRaises(ScoringError):
            self.execute(score_fn=lambda predictions: report)
        self.assertFalse((self.output / "scores.json").exists())
        self.assertNotIn("PRIVATE_REFERENCE", (self.output / "run.json").read_text())

    def test_missing_caption_is_saved_and_scored_as_empty_cells(self):
        self.paper.write_text("No caption in this article.", encoding="utf-8")
        requests = []
        def score(predictions):
            requests.append(predictions)
            return public_report()
        self.execute(chat_fn=lambda **kw: self.fail("No model call"), score_fn=score)
        self.assertEqual(requests, [{"synthetic": {"cells": []}}])
        self.assertFalse(json.loads((self.output / "predictions" / "synthetic_table_1_pred.json").read_text())["found"])

    def test_invalid_inputs_are_rejected_before_creating_run(self):
        for key in ("../../escape", "", "bad/name", "bad\\name"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                run_experiment({key: self.paper}, self.output, prompt_path=self.prompt,
                               chat_fn=lambda **kw: self.fail("No model call"),
                               score_fn=lambda predictions: self.fail("No scoring call"))
        self.config.pop("version")
        self.prompt.write_text(json.dumps(self.config), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.execute()
        self.assertFalse(self.output.exists())

    def test_token_preflight_does_not_import_model_or_create_run(self):
        with self.assertRaises(ScoringError):
            self.execute(score_fn=None, token="short",
                         chat_fn=lambda **kw: self.fail("No model call"))
        self.assertFalse(self.output.exists())

    def test_gold_paths_rejected_before_access(self):
        private = self.root / "gold_tables" / "private.txt"
        with self.assertRaises(ValueError):
            run_experiment({"synthetic": private}, self.output, prompt_path=self.prompt,
                           chat_fn=lambda **kw: self.fail("No model call"),
                           score_fn=lambda predictions: self.fail("No scoring call"))
        self.assertFalse(self.output.exists())

    def test_partial_extraction_failure_keeps_prior_valid_prediction(self):
        other = self.root / "other.txt"
        other.write_text(SOURCE, encoding="utf-8")
        calls = []
        def chat(**kw):
            calls.append(kw)
            if len(calls) == 1:
                return json.dumps(table())
            raise ConnectionError("service unavailable")
        with self.assertRaises(ConnectionError):
            run_experiment({"synthetic": self.paper, "other": other}, self.output,
                           prompt_path=self.prompt, chat_fn=chat,
                           score_fn=lambda predictions: self.fail("No partial-benchmark submission"))
        self.assertTrue((self.output / "predictions" / "synthetic_table_1_pred.json").exists())
        self.assertFalse((self.output / "predictions" / "other_table_1_pred.json").exists())


class ClientTests(unittest.TestCase):
    def server(self, status=200, body=None, redirect=False):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_POST(self):
                requests.append((self.headers.get("Authorization"),
                                 json.loads(self.rfile.read(int(self.headers["Content-Length"])))))
                self.send_response(status)
                if redirect:
                    self.send_header("Location", "/unexpected")
                self.end_headers()
                self.wfile.write(json.dumps(body if body is not None else public_report()).encode("utf-8"))
        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def cleanup():
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        self.addCleanup(cleanup)
        return f"http://127.0.0.1:{server.server_port}/score", requests

    def test_authenticated_contract_and_proxy_bypass(self):
        url, requests = self.server()
        predictions = {"synthetic": {"cells": table()["cells"]}}
        with patch.dict(os.environ, {"http_proxy": "http://invalid-proxy:9999", "HTTP_PROXY": "http://invalid-proxy:9999"}):
            report = score_predictions(predictions, url=url, token=TOKEN)
        self.assertEqual(report["summary"]["cells"]["f1"], 1)
        self.assertEqual(requests, [(f"Bearer {TOKEN}", {"predictions": predictions})])

    def test_http_error_does_not_echo_server_body(self):
        url, requests = self.server(status=401, body={"error": "PRIVATE_SERVER_BODY"})
        with self.assertRaises(ScoringError) as error:
            score_predictions({}, url=url, token=TOKEN)
        self.assertNotIn("PRIVATE_SERVER_BODY", str(error.exception))
        self.assertNotIn(TOKEN, str(error.exception))
        self.assertEqual(len(requests), 1)

    def test_redirect_is_not_followed(self):
        url, requests = self.server(status=307, redirect=True)
        with self.assertRaises(ScoringError):
            score_predictions({}, url=url, token=TOKEN)
        self.assertEqual(len(requests), 1)

    def test_unsafe_urls_and_tokens_are_rejected(self):
        for url in ("http://external.example/score", "file:///private/score",
                    "http://user:secret@127.0.0.1/score", "http://127.0.0.1/score?gold=/private",
                    "http://127.0.0.1/wrong", "http://127.0.0.1:99999/score"):
            with self.subTest(url=url), self.assertRaises(ScoringError):
                validate_connection(url, TOKEN)
        for token in ("short", "x" * 32 + "\r\n", "é" * 32):
            with self.subTest(token=token), self.assertRaises(ScoringError):
                validate_connection("http://127.0.0.1/score", token)

    def test_unexpected_fields_and_nonfinite_metrics_are_rejected(self):
        report = public_report()
        report["summary"]["gold_value"] = "PRIVATE"
        with self.assertRaises(ScoringError):
            validate_public_report(report)
        report = public_report()
        report["summary"]["cells"]["f1"] = float("nan")
        with self.assertRaises(ScoringError):
            validate_public_report(report)

    def test_oversized_request_is_rejected_before_connection(self):
        with patch("almog_work.table1_experiment.scorer_client.build_opener") as opener:
            with self.assertRaises(ScoringError):
                score_predictions({"synthetic": {"cells": ["x" * (4 * 1024 * 1024)]}}, token=TOKEN)
            opener.assert_not_called()


class HttpIntegrationTests(ExperimentFixture):
    """Full runner-to-service integration with temporary synthetic references."""
    def start_gateway(self, *, two_papers=False, value="0", max_evaluations=2):
        validation = Path(__file__).resolve().parents[1] / "validation"
        sys.path.insert(0, str(validation))
        from scoring_service import ScoringGateway, make_server
        private = self.root / "private_references"
        private.mkdir()
        (private / "synthetic_table_1_gold.json").write_text(json.dumps({"cells": table(value)["cells"]}))
        if two_papers:
            (private / "other_table_1_gold.json").write_text(json.dumps({"cells": table()["cells"]}))
        gateway = ScoringGateway(private, max_evaluations=max_evaluations)
        server = make_server(gateway, TOKEN, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def cleanup():
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        self.addCleanup(cleanup)
        return f"http://127.0.0.1:{server.server_port}/score"

    def test_real_http_full_benchmark_and_omitted_paper(self):
        url = self.start_gateway(two_papers=True)
        report = self.execute(score_fn=None, scorer_url=url, token=TOKEN)
        self.assertEqual(report["summary"]["papers_scored"], 2)
        self.assertEqual(report["summary"]["cells"]["tp_exact"], 1)
        self.assertEqual(report["summary"]["cells"]["fn_exact"], 1)
        self.assertEqual(report["summary"]["missing_prediction_files"], ["other"])
        for path in (self.output / "run.json", self.output / "scores.json"):
            self.assertNotIn(TOKEN, path.read_text())
            self.assertNotIn(str(self.root / "private_references"), path.read_text())

    def test_reference_value_does_not_enter_feedback_logs_or_model(self):
        url = self.start_gateway(value="PRIVATE_EXPECTED_VALUE")
        calls = []
        def chat(**kwargs):
            calls.append(kwargs)
            return json.dumps(table())
        report = self.execute(score_fn=None, scorer_url=url, token=TOKEN, chat_fn=chat)
        self.assertEqual(report["summary"]["cells"]["f1"], 0)
        self.assertEqual(len(report["error_examples"]), 1)
        artifacts = "".join(p.read_text() for p in self.output.rglob("*.json"))
        self.assertNotIn("PRIVATE_EXPECTED_VALUE", artifacts)
        self.assertNotIn("PRIVATE_EXPECTED_VALUE", json.dumps(calls))
        self.assertNotIn(TOKEN, artifacts)

    def test_exhausted_service_budget_is_logged_without_retry(self):
        url = self.start_gateway(max_evaluations=1)
        self.execute(score_fn=None, scorer_url=url, token=TOKEN)
        self.output = self.root / "run_02"
        with self.assertRaises(ScoringError):
            self.execute(score_fn=None, scorer_url=url, token=TOKEN)
        log = json.loads((self.output / "run.json").read_text())
        self.assertEqual(log["status"], "failed")
        self.assertEqual(log["failure"]["stage"], "scoring")
        self.assertEqual(log["scoring"]["automatic_retries"], 0)
        self.assertFalse((self.output / "scores.json").exists())


class CliTests(unittest.TestCase):
    def test_cli_help_needs_no_model_or_credentials(self):
        result = subprocess.run([sys.executable, "-m", "almog_work.table1_experiment.run_experiment", "--help"],
                                capture_output=True, text=True, cwd=Path(__file__).resolve().parents[2])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Table-1", result.stdout)

    def test_cli_missing_token_fails_before_model_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper = root / "paper.txt"
            paper.write_text(SOURCE, encoding="utf-8")
            run = root / "run"
            env = dict(os.environ, TABLE_SCORER_TOKEN="")
            result = subprocess.run([
                sys.executable, "-m", "almog_work.table1_experiment.run_experiment",
                "--paper", f"synthetic={paper}", "--run-dir", str(run)],
                capture_output=True, text=True, cwd=Path(__file__).resolve().parents[2], env=env)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse(run.exists())

    def run_cli(self, *args):
        env = dict(os.environ, TABLE_SCORER_TOKEN="")
        return subprocess.run(
            [sys.executable, "-m", "almog_work.table1_experiment.run_experiment", *args],
            capture_output=True, text=True, cwd=Path(__file__).resolve().parents[2], env=env)

    def test_cli_holdout_requires_final_flag(self):
        result = self.run_cli("--split", "holdout")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--final", result.stderr)

    def test_cli_requires_exactly_one_paper_source(self):
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(self.run_cli("--split", "dev", "--paper", "a=b.txt").returncode, 2)


class ConfigTests(unittest.TestCase):
    def test_real_config_splits_are_disjoint_and_papers_exist(self):
        dev, dev_url = load_split("dev", DEFAULT_CONFIG_PATH)
        holdout, holdout_url = load_split("holdout", DEFAULT_CONFIG_PATH)
        self.assertEqual((len(dev), len(holdout)), (6, 4))
        self.assertFalse(set(dev) & set(holdout))
        self.assertNotEqual(dev_url, holdout_url)
        for path in list(dev.values()) + list(holdout.values()):
            self.assertTrue(path.is_file(), path.name)
        config = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(config["splits"]["holdout"]["max_evaluations"], 1)
        self.assertEqual(config["splits"]["holdout"]["max_examples"], 0)

    def test_overlapping_or_unknown_splits_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            entry = {"papers": ["a"], "scorer_url": "http://127.0.0.1:1/score"}
            path.write_text(json.dumps({"papers_dir": ".", "splits": {"dev": entry, "holdout": entry}}),
                            encoding="utf-8")
            with self.assertRaises(ValueError):
                load_split("dev", path)
            with self.assertRaises(ValueError):
                load_split("other", path)


EX_SOURCE = ("Intro (Table 1).\nTable 1. Synthetic baseline\nVariable\nStudy A\nAge\n42 ± 3\n"
             "Note: footnote\nNARRATIVE_SENTINEL\nTable 2. Other table\nTABLE_TWO_SENTINEL")


def ex_table():
    return {"table_title": "Synthetic baseline", "columns": ["Variable", "Study A"],
            "cells": [{"row_label": "Age", "row_group": "Demographics",
                       "column_label": "Study A", "value": "42 ± 3"}]}


class ExtractorTests(unittest.TestCase):
    def extract(self, response=None, source=EX_SOURCE):
        return extract_table_one(source, paper_id="synthetic",
                                 chat_fn=lambda **kwargs: json.dumps(response or ex_table()))

    def test_valid_prediction_has_gold_compatible_envelope(self):
        result = self.extract()
        validate_table_result(result)
        self.assertEqual(result["paper_id"], "synthetic")
        self.assertEqual(result["table_number"], 1)
        self.assertTrue(result["found"])
        self.assertEqual(result["cells"][0]["row_group"], "Demographics")

    def test_only_table_one_is_sent_to_model(self):
        calls = []
        def chat(**kwargs):
            calls.append(kwargs)
            return json.dumps(ex_table())
        extract_table_one(EX_SOURCE, chat_fn=chat)
        self.assertEqual(len(calls), 1)
        message = calls[0]["messages"][1]["content"]
        self.assertIn("42 ± 3", message)
        self.assertNotIn("NARRATIVE_SENTINEL", message)
        self.assertNotIn("TABLE_TWO_SENTINEL", message)

    def test_missing_table_does_not_call_model(self):
        def chat(**kwargs):
            self.fail("Model must not be called for a missing table")
        result = extract_table_one("We refer to Table 1 in the narrative.", chat_fn=chat)
        self.assertFalse(result["found"])
        validate_table_result(result)

    def test_lowercase_caption_and_colon(self):
        section = find_table_section("TABLE 1: baseline\nAge\n42\nTable 2. Next")
        self.assertIsNotNone(section)
        self.assertNotIn("Table 2", section[0])

    def test_figure_and_section_boundaries(self):
        for boundary in ["Fig. 1 Caption", "Figure 1 Caption", "Discussion", "Abbreviations: SD"]:
            with self.subTest(boundary=boundary):
                section = find_table_section(f"Table 1. Baseline\n42\n{boundary}\nSENTINEL")
                self.assertNotIn("SENTINEL", section[0])

    def test_oversized_source_is_not_silently_truncated(self):
        with self.assertRaises(ValueError):
            find_table_section("Table 1. Baseline\n" + "x" * 100, max_chars=25)

    def test_truncated_json_is_rejected(self):
        for raw in ('{"cells": [', '[]', '', None, 'before {"cells": []} after'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                _parse_table_json(raw)

    def test_complete_markdown_fence_is_accepted(self):
        self.assertEqual(_parse_table_json("```json\n" + json.dumps(ex_table()) + "\n```"), ex_table())

    def test_invalid_cells_and_column_references_are_rejected(self):
        for field, value in [("column_label", "undeclared"), ("value", 42),
                             ("row_label", ""), ("row_group", 123)]:
            bad = ex_table()
            bad["cells"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.extract(bad)

    def test_repeated_cells_keep_the_first_copy_and_are_counted(self):
        data = ex_table()
        first = copy.deepcopy(data["cells"][0])
        repeat = dict(first, value="DIFFERENT")
        data["cells"] = data["cells"] + [repeat, dict(first)]
        stats = {}
        result = extract_table_one(EX_SOURCE, paper_id="p", chat_fn=lambda **kw: json.dumps(data),
                                   stats=stats)
        self.assertEqual(result["cells"][0], first)
        self.assertEqual(len(result["cells"]), len(ex_table()["cells"]))
        self.assertEqual(stats["duplicates_dropped"], 2)

    def test_malformed_cells_are_still_rejected_not_deduplicated(self):
        bad = ex_table()
        bad["cells"] = bad["cells"] + [dict(bad["cells"][0], row_label=["x"])]
        with self.assertRaises(ValueError):
            self.extract(bad)

    def test_blank_value_cells_are_dropped_but_other_bad_values_are_rejected(self):
        for value in (None, "", " \t\n"):
            data = ex_table()
            data["cells"].append({**data["cells"][0], "column_label": data["columns"][-1],
                                  "row_label": "Blank row", "value": value})
            with self.subTest(value=value):
                self.assertEqual(len(self.extract(data)["cells"]), len(ex_table()["cells"]))
        for value in (5, 0, [], {}):
            bad = ex_table()
            bad["cells"][0]["value"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.extract(bad)

    def test_reported_zeros_and_missing_markers_are_preserved(self):
        for value in ("0", "0.0", "0 (0%)", "N/A", "—"):
            data = ex_table()
            data["cells"][0]["value"] = value
            with self.subTest(value=value):
                self.assertEqual(self.extract(data)["cells"][0]["value"], value)

    def test_unreported_column_cell_does_not_require_a_record(self):
        data = ex_table()
        data["columns"].append("Study B")
        result = self.extract(data)
        self.assertEqual(len(result["cells"]), 1)
        self.assertFalse(any(cell["column_label"] == "Study B" for cell in result["cells"]))

    def test_category_level_statistic_preserves_null_row_label(self):
        data = ex_table()
        data["cells"][0].update(row_label=None, row_group="Gender")
        self.assertIsNone(self.extract(data)["cells"][0]["row_label"])

    def test_nested_headers_are_preserved(self):
        data = ex_table()
        data["columns"] = ["GROUP A: Arm 1 (n = 10)", "GROUP B: Arm 2 (n = 12)"]
        data["cells"][0]["column_label"] = data["columns"][0]
        result = self.extract(data)
        self.assertEqual(result["columns"], data["columns"])
        self.assertEqual(result["cells"][0]["column_label"], data["columns"][0])

    def test_custom_prompt_is_used_and_validated(self):
        calls = []
        config = {"version": "candidate-v2", "system": "CUSTOM_SYSTEM",
                  "user": "CUSTOM_USER\n__TABLE_TEXT__"}
        def chat(**kwargs):
            calls.append(kwargs)
            return json.dumps(ex_table())
        extract_table_one(EX_SOURCE, prompt_config=config, chat_fn=chat, max_new_tokens=9000)
        self.assertEqual(calls[0]["messages"][0]["content"], "CUSTOM_SYSTEM")
        self.assertEqual(calls[0]["max_new_tokens"], 9000)
        with self.assertRaises(ValueError):
            extract_table_one(EX_SOURCE, prompt_config={"system": "test", "user": "no placeholder"}, chat_fn=chat)

    def test_saved_prediction_keeps_utf8_symbols_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper = root / "paper.txt"
            paper.write_text(EX_SOURCE, encoding="utf-8")
            run_experiment({"synthetic": paper}, root / "run", chat_fn=lambda **kw: json.dumps(ex_table()),
                           score_fn=lambda predictions: public_report())
            saved = (root / "run" / "predictions" / "synthetic_table_1_pred.json").read_bytes()
            self.assertIn("±".encode("utf-8"), saved)
            self.assertNotIn(bytes([92]) + b"u00b1", saved)

    def test_default_data_dir_is_not_the_gold_folder(self):
        self.assertNotIn("gold_tables", DATA_DIR.parts)

    def test_guidance_is_rendered_and_baseline_is_valid(self):
        baseline = json.loads(DEFAULT_PROMPT_PATH.read_text(encoding="utf-8"))
        validate_prompt_config(baseline)
        rendered = render_user_prompt(baseline, "TABLE_BODY")
        self.assertIn(baseline["guidance"], rendered)
        self.assertIn("TABLE_BODY", rendered)
        self.assertNotIn("__GUIDANCE__", rendered)
        self.assertNotIn("__TABLE_TEXT__", rendered)
        config = {"system": "s", "user": "G:\n__GUIDANCE__\nT:\n__TABLE_TEXT__", "guidance": "be careful"}
        validate_prompt_config(config)
        self.assertEqual(render_user_prompt(config, "x"), "G:\nbe careful\nT:\nx")

    def test_guidance_misuse_is_rejected(self):
        base = {"system": "s", "user": "G:\n__GUIDANCE__\n__TABLE_TEXT__", "guidance": "ok"}
        for changes in ({"guidance": "  "}, {"guidance": 5}, {"guidance": "__TABLE_TEXT__"},
                        {"guidance": "__GUIDANCE__"}, {"user": "__TABLE_TEXT__"}):
            with self.assertRaises(ValueError, msg=str(changes)):
                validate_prompt_config({**base, **changes})
        with self.assertRaises(ValueError):
            validate_prompt_config({"system": "s", "user": "__GUIDANCE__ __TABLE_TEXT__"})

    def test_run_snapshot_keeps_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper = root / "paper.txt"
            paper.write_text(EX_SOURCE, encoding="utf-8")
            run_experiment({"synthetic": paper}, root / "run", chat_fn=lambda **kw: json.dumps(ex_table()),
                           score_fn=lambda predictions: public_report())
            snapshot = json.loads((root / "run" / "prompt.json").read_text(encoding="utf-8"))
            self.assertEqual(set(snapshot), {"version", "system", "user", "guidance"})


if __name__ == "__main__":
    unittest.main()