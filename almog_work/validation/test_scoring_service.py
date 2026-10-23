"""Gateway/privacy tests using temporary synthetic reference tables only."""
import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from scoring_service import BudgetExceeded, RequestRejected, ScoringGateway, make_server
from test_score_table_extraction import cell


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.gold_dir = Path(self.tmp.name) / "private_gold"
        self.gold_dir.mkdir()
        self.reference = {"cells": [cell("PRIVATE_GOLD_VALUE", row=str(i)) for i in range(12)],
                          "raw_table_text": "PRIVATE_ARTICLE_TEXT"}
        (self.gold_dir / "synthetic_table_1_gold.json").write_text(
            json.dumps(self.reference), encoding="utf-8")

    def gateway(self, **kwargs):
        return ScoringGateway(self.gold_dir, **kwargs)

    def test_bounded_report_does_not_disclose_reference_values_or_paths(self):
        report = self.gateway(max_examples=2).evaluate({"predictions": {"synthetic": {
            "cells": [cell("incorrect", row=str(i)) for i in range(12)]}}})
        text = json.dumps(report)
        self.assertEqual(len(report["error_examples"]), 2)
        for forbidden in ("PRIVATE_GOLD_VALUE", "PRIVATE_ARTICLE_TEXT", "gold_value",
                          str(self.gold_dir), "raw_table_text"):
            self.assertNotIn(forbidden, text)

    def test_caller_cannot_request_paths_or_change_policy(self):
        gateway = self.gateway()
        for field in ("gold_dir", "pred_dir", "output", "max_examples", "seed"):
            with self.subTest(field=field), self.assertRaises(RequestRejected):
                gateway.evaluate({"predictions": {}, field: "/private/path"})
        with self.assertRaises(RequestRejected):
            gateway.evaluate({"predictions": {"../../private": {"cells": []}}})

    def test_feedback_budget_applies_across_requests(self):
        gateway = self.gateway(max_examples=2, feedback_budget=3)
        request = {"predictions": {"synthetic": {"cells": []}}}
        reports = [gateway.evaluate(request) for _ in range(3)]
        self.assertEqual([len(r["error_examples"]) for r in reports], [2, 1, 0])
        self.assertEqual(reports[-1]["feedback_remaining"], 0)

    def test_evaluation_budget(self):
        gateway = self.gateway(max_evaluations=1)
        gateway.evaluate({"predictions": {}})
        with self.assertRaises(BudgetExceeded):
            gateway.evaluate({"predictions": {}})

    def test_omitted_papers_are_scored_as_missing(self):
        report = self.gateway().evaluate({"predictions": {}})
        self.assertEqual(report["summary"]["papers_scored"], 1)
        self.assertEqual(report["summary"]["cells"]["fn_exact"], 12)
        self.assertEqual(report["summary"]["missing_prediction_files"], ["synthetic"])

    def test_perfect_predictions_still_score_correctly(self):
        report = self.gateway().evaluate({"predictions": {"synthetic": self.reference}})
        self.assertEqual(report["summary"]["cells"]["f1"], 1)
        self.assertEqual(report["error_examples"], [])

    def test_invalid_prediction_is_rejected_without_echoing_content(self):
        for table in ("/secret/file", {}, {"cells": [None]}):
            with self.subTest(table=table), self.assertRaises(RequestRejected) as error:
                self.gateway().evaluate({"predictions": {"synthetic": table}})
            self.assertNotIn("PRIVATE_GOLD_VALUE", str(error.exception))

    def test_keys_limit_scoring_to_one_split(self):
        (self.gold_dir / "other_table_1_gold.json").write_text(
            json.dumps(self.reference), encoding="utf-8")
        report = self.gateway(keys=["synthetic"]).evaluate({"predictions": {}})
        self.assertEqual(report["summary"]["papers_scored"], 1)
        self.assertEqual(report["summary"]["missing_prediction_files"], ["synthetic"])
        with self.assertRaises(RequestRejected):
            self.gateway(keys=["synthetic"]).evaluate(
                {"predictions": {"other": self.reference}})
        for keys in ([], ["missing"], ["synthetic", "synthetic"], "synthetic"):
            with self.subTest(keys=keys), self.assertRaises(ValueError):
                self.gateway(keys=keys)

    def test_policy_bounds(self):
        for kwargs in ({"max_examples": 11}, {"feedback_budget": 101},
                       {"max_evaluations": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.gateway(**kwargs)

    def test_http_authentication_and_sanitized_failures(self):
        token = "synthetic-test-token-only-" * 2
        server = make_server(self.gateway(), token, port=0)
        self.assertEqual(server.server_address[0], "127.0.0.1")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            def post(body, auth=None):
                connection = http.client.HTTPConnection(*server.server_address, timeout=5)
                try:
                    headers = {"Content-Type": "application/json"}
                    if auth:
                        headers["Authorization"] = auth
                    connection.request("POST", "/score", body=body, headers=headers)
                    response = connection.getresponse()
                    return response.status, response.read().decode("utf-8")
                finally:
                    connection.close()
            status, _ = post('{"predictions": {}}')
            self.assertEqual(status, 401)
            status, text = post("malformed PRIVATE_INPUT", f"Bearer {token}")
            self.assertEqual(status, 400)
            self.assertNotIn("PRIVATE_INPUT", text)
            status, text = post('{"predictions": {}}', f"Bearer {token}")
            self.assertEqual(status, 200)
            self.assertNotIn("PRIVATE_GOLD_VALUE", text)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()