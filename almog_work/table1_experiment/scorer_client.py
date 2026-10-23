"""Restricted HTTP client; no scorer implementation or reference-table imports.

Token comes from the trusted runner's environment, never prompts or logs.
No redirects, automatic retries, caller-selected reference paths or subsets.
"""
import json
import math
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

DEFAULT_SCORER_URL = "http://127.0.0.1:8765/score"
MAX_BYTES = 4 * 1024 * 1024


class ScoringError(RuntimeError):
    """Public-safe error; never includes response bodies or authorization."""


def load_scorer_token(env_path=None):
    """TABLE_SCORER_TOKEN from the environment, else from almog_work/.env (that key only)."""
    value = os.environ.get("TABLE_SCORER_TOKEN")
    if value is not None:
        return value
    path = Path(env_path) if env_path else Path(__file__).resolve().parents[1] / ".env"
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            key, sep, raw = line.strip().partition("=")
            if sep and key.strip() == "TABLE_SCORER_TOKEN":
                return raw.strip().strip('"').strip("'")
    except OSError:
        pass
    return ""


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_connection(url, token, timeout=30):
    try:
        parts = urlsplit(url)
        port = parts.port
        valid = (
            parts.scheme in ("http", "https") and parts.hostname
            and parts.path == "/score" and not parts.query and not parts.fragment
            and parts.username is None and parts.password is None
            and (port is None or 1 <= port <= 65535)
            and (parts.scheme == "https" or parts.hostname in ("127.0.0.1", "localhost", "::1"))
        )
    except (ValueError, TypeError):
        valid = False
    if not valid:
        raise ScoringError("Scorer requires HTTPS or loopback HTTP at /score, without credentials in the URL")
    if not isinstance(token, str) or len(token) < 32 or not token.isascii() or any(
        ord(c) < 33 or ord(c) == 127 for c in token
    ):
        raise ScoringError("Configure a private scorer token of at least 32 printable ASCII characters")
    if type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 300:
        raise ScoringError("Scorer timeout must be between 0 and 300 seconds")


def validate_public_report(report):
    """Allowlist the current service contract before persisting any feedback."""
    def fields(value, names):
        if not isinstance(value, dict) or set(value) != set(names):
            raise ScoringError("Invalid public scoring report")

    def count(value):
        if type(value) is not int or value < 0:
            raise ScoringError("Invalid public scoring report")

    def metric(value):
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ScoringError("Invalid public scoring report")

    def text(value, nullable=False):
        if value is None and nullable:
            return
        if not isinstance(value, str):
            raise ScoringError("Invalid public scoring report")

    fields(report, ("summary", "per_paper", "error_examples", "feedback_remaining", "evaluations_remaining"))
    summary = report["summary"]
    fields(summary, ("papers_scored", "cells", "keys_only", "missing_prediction_files"))
    count(summary["papers_scored"])
    for name, counts, metrics in (
        ("cells", ("tp_exact", "fp_exact", "fn_exact"), ("precision", "recall", "f1")),
        ("keys_only", ("tp", "fp", "fn"), ("precision", "recall", "f1", "value_accuracy_on_matched_keys")),
    ):
        fields(summary[name], counts + metrics)
        for key in counts:
            count(summary[name][key])
        for key in metrics:
            metric(summary[name][key])
    if not isinstance(summary["missing_prediction_files"], list):
        raise ScoringError("Invalid public scoring report")
    for paper in summary["missing_prediction_files"]:
        text(paper)
    per_paper = report["per_paper"]
    if not isinstance(per_paper, list) or len(per_paper) != summary["papers_scored"]:
        raise ScoringError("Invalid public scoring report")
    paper_metrics = ("cell_precision", "cell_recall", "cell_f1", "key_precision",
                     "key_recall", "value_accuracy_on_matched_keys")
    for paper in per_paper:
        fields(paper, ("paper", "gold_cells", "pred_cells", "missing_prediction_file") + paper_metrics)
        text(paper["paper"])
        for key in ("gold_cells", "pred_cells"):
            count(paper[key])
        if type(paper["missing_prediction_file"]) is not bool:
            raise ScoringError("Invalid public scoring report")
        for key in paper_metrics:
            metric(paper[key])
    examples = report["error_examples"]
    if not isinstance(examples, list) or len(examples) > 10:
        raise ScoringError("Invalid public scoring report")
    for example in examples:
        fields(example, ("paper", "error_type", "row_group", "row_label", "column_label", "predicted_value"))
        text(example["paper"])
        text(example["error_type"])
        for key in ("row_group", "row_label", "column_label", "predicted_value"):
            text(example[key], nullable=True)
    count(report["feedback_remaining"])
    count(report["evaluations_remaining"])
    return report


def score_predictions(predictions: dict, *, url=DEFAULT_SCORER_URL, token, timeout=30) -> dict:
    validate_connection(url, token, timeout)
    if not isinstance(predictions, dict):
        raise ScoringError("Predictions must be an object")
    try:
        payload = json.dumps({"predictions": predictions}, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, TypeError):
        raise ScoringError("Invalid predictions") from None
    if len(payload) > MAX_BYTES:
        raise ScoringError("Scoring request exceeds the size limit")
    request = Request(url, data=payload, method="POST", headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
    })
    # Do not route the private token through environment-configured proxies.
    opener = build_opener(ProxyHandler({}), _NoRedirects())
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ScoringError("Scoring response exceeds the size limit")
        report = json.loads(raw.decode("utf-8"))
    except HTTPError as error:
        status = error.code
        error.close()
        raise ScoringError(f"Scoring request failed (HTTP {status}); no automatic retry") from None
    except (URLError, TimeoutError, OSError):
        raise ScoringError("Scoring connection failed; evaluation consumption may be unknown, no automatic retry") from None
    except (ValueError, UnicodeError):
        raise ScoringError("Invalid public scoring report") from None
    return validate_public_report(report)