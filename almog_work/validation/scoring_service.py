#!/usr/bin/env python3
"""Trusted, loopback-only scoring gateway for the future agent runner.

POST /score accepts {"predictions": {"<benchmark filename prefix>": table_json}}.
Gold paths, sampling settings and reference values are never part of the API.
Omitted benchmark papers count as missing predictions, not as a smaller benchmark.

The operator runs this service with gold access; agents must run without gold
filesystem/repository access and must not be given a shell on the scorer host.
This API is NOT an OS sandbox. For deployment use separate users/containers,
mount gold only in the scorer, and expose this API via a trusted runner. The
local HTTP server is not intended as a public internet service.

Evaluation and feedback budgets are process-local; restarting resets them.
The operator must persist/enforce experiment-wide budgets in the future runner.
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

from score_table_extraction import (
    aggregate_scores, build_per_paper, compare_paper, list_gold_files, sample_errors,
)

MAX_REQUEST_BYTES = 4 * 1024 * 1024


class RequestRejected(ValueError):
    """Public-safe validation error with no submitted/reference content."""


class BudgetExceeded(RuntimeError):
    pass


class ScoringGateway:
    """Trusted-only object; do not hand this object or its paths to an agent."""

    def __init__(self, gold_dir: Path, *, max_examples=5, feedback_budget=25,
                 max_evaluations=20, seed=42, keys=None):
        if type(max_examples) is not int or not 0 <= max_examples <= 10:
            raise ValueError("max_examples must be between 0 and 10")
        if type(feedback_budget) is not int or not 0 <= feedback_budget <= 100:
            raise ValueError("feedback_budget must be between 0 and 100")
        if type(max_evaluations) is not int or not 1 <= max_evaluations <= 100:
            raise ValueError("max_evaluations must be between 1 and 100")
        files = list_gold_files(gold_dir)
        if not files:
            raise ValueError("No benchmark tables configured")
        self._references = {
            p.name.removesuffix("_table_1_gold.json"): p for p in files
        }
        if keys is not None:
            # Score only the named papers, e.g. a dev or holdout split.
            if (not isinstance(keys, (list, tuple)) or not keys
                    or len(set(keys)) != len(keys)
                    or any(key not in self._references for key in keys)):
                raise ValueError("keys must be unique names of existing benchmark papers")
            self._references = {key: self._references[key] for key in keys}
        files = list(self._references.values())
        # Validate all references before accepting requests. No gold content is
        # emitted even if operator-side data is malformed or duplicated.
        for path in files:
            compare_paper(path, None)
        self._max_examples = max_examples
        self._feedback_remaining = feedback_budget
        self._evaluations_remaining = max_evaluations
        self._seed = seed

    def evaluate(self, request: dict) -> dict:
        if self._evaluations_remaining <= 0:
            raise BudgetExceeded("Evaluation budget exhausted")
        if not isinstance(request, dict) or set(request) != {"predictions"}:
            raise RequestRejected("Provide only a predictions object")
        predictions = request["predictions"]
        if not isinstance(predictions, dict):
            raise RequestRejected("predictions must be an object")
        if any(paper not in self._references for paper in predictions):
            raise RequestRejected("Unknown benchmark paper")
        scores, errors = [], []
        # Never accept caller-supplied file paths. Predictions live temporarily
        # outside the gold directory and are deleted after each evaluation.
        with TemporaryDirectory(prefix="table_predictions_") as directory:
            for index, (paper, gold_path) in enumerate(self._references.items()):
                pred_path = None
                if paper in predictions:
                    table = predictions[paper]
                    if not isinstance(table, dict):
                        raise RequestRejected("Each prediction must be a table object")
                    # Only cells are used for scoring. Raw article text or other
                    # submitted metadata is neither stored nor returned.
                    pred_path = Path(directory) / f"prediction_{index}.json"
                    pred_path.write_text(json.dumps({"cells": table.get("cells")}),
                                         encoding="utf-8")
                try:
                    score, mistakes = compare_paper(gold_path, pred_path)
                except ValueError:
                    raise RequestRejected("Invalid table cells") from None
                scores.append(score)
                errors.extend(mistakes)
        limit = min(self._max_examples, self._feedback_remaining)
        examples = sample_errors(errors, limit, self._seed)
        # Allowlist projection: do not serialize ErrorExample.__dict__, since
        # that contains reference answers for the trusted scorer's internal use.
        public_examples = [
            {"paper": e.paper, "error_type": e.error_type,
             "row_group": e.row_group, "row_label": e.row_label,
             "column_label": e.column_label, "predicted_value": e.pred_value}
            for e in examples
        ]
        self._feedback_remaining -= len(public_examples)
        self._evaluations_remaining -= 1
        return {
            "summary": aggregate_scores(scores),
            "per_paper": build_per_paper(scores),
            "error_examples": public_examples,
            "feedback_remaining": self._feedback_remaining,
            "evaluations_remaining": self._evaluations_remaining,
        }


def make_server(gateway: ScoringGateway, token: str, port=8765) -> HTTPServer:
    if not isinstance(token, str) or len(token) < 32 or not token.isascii():
        raise ValueError("A private ASCII token of at least 32 characters is required")

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def log_message(self, format, *args):
            # Never log authorization headers, predictions, paths or gold.
            pass

        def reply(self, status, body):
            payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            self.reply(405, {"error": "Use POST /score"})

        def do_POST(self):
            supplied = self.headers.get("Authorization", "").encode("utf-8")
            if not hmac.compare_digest(supplied, f"Bearer {token}".encode("ascii")):
                self.reply(401, {"error": "Unauthorized"})
                return
            if self.path != "/score":
                self.reply(404, {"error": "Unknown endpoint"})
                return
            if self.headers.get("Transfer-Encoding"):
                self.reply(400, {"error": "Content-Length required"})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                size = 0
            if not 0 < size <= MAX_REQUEST_BYTES:
                self.reply(413, {"error": "Invalid request size"})
                return
            try:
                request = json.loads(self.rfile.read(size).decode("utf-8"))
                report = gateway.evaluate(request)
            except (ValueError, UnicodeError):
                self.reply(400, {"error": "Invalid scoring request"})
                return
            except BudgetExceeded:
                self.reply(429, {"error": "Evaluation budget exhausted"})
                return
            except Exception:
                # Never expose traceback, private paths, or internal data.
                self.reply(500, {"error": "Scoring unavailable"})
                return
            self.reply(200, report)

    # Deliberately no caller-configurable host / remote public binding.
    return HTTPServer(("127.0.0.1", port), Handler)


def load_scorer_token():
    """TABLE_SCORER_TOKEN from the environment, else from almog_work/.env (that key only)."""
    value = os.environ.get("TABLE_SCORER_TOKEN")
    if value is not None:
        return value
    try:
        for line in (Path(__file__).resolve().parents[1] / ".env").read_text(encoding="utf-8").splitlines():
            key, sep, raw = line.strip().partition("=")
            if sep and key.strip() == "TABLE_SCORER_TOKEN":
                return raw.strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


def main():
    parser = argparse.ArgumentParser(description="Trusted local table scoring service")
    parser.add_argument("--gold-dir", required=True, type=Path)
    parser.add_argument("--keys", help="Comma-separated paper keys to score (a split); default is all")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--max-examples", type=int, default=5)
    parser.add_argument("--feedback-budget", type=int, default=25)
    parser.add_argument("--max-evaluations", type=int, default=20)
    args = parser.parse_args()
    token = load_scorer_token()
    try:
        gateway = ScoringGateway(args.gold_dir, max_examples=args.max_examples,
                                 feedback_budget=args.feedback_budget,
                                 max_evaluations=args.max_evaluations,
                                 keys=args.keys.split(",") if args.keys else None)
        server = make_server(gateway, token, args.port)
    except Exception:
        parser.exit(1, "Could not start scorer. Check private token, benchmark and server settings.\n")
    print("Scorer ready on loopback. Agents must not have gold filesystem access.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()