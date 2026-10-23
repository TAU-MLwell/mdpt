"""One prompt, selected papers, one HTTP scoring call, reproducible run artifacts.

This is a TRUSTED runner, not an agent sandbox. In deployment, stage only papers,
prompts and experiment code for agents; do not expose gold, repository history,
remote repository retrieval, this runner's token or scorer-host shell access.

The server scores its full operator-configured benchmark. Missing papers count
as missing predictions. Budget counters are logged but remain server-process-local;
experiment-wide durable budgets and the prompt-improvement loop are future work.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from almog_work.table1_experiment.extractor import (
    DEFAULT_MAX_NEW_TOKENS, DEFAULT_PROMPT_PATH, MAX_TABLE_SECTION_CHARS,
    InvalidModelOutput, extract_table_one, validate_prompt_config,
)
from almog_work.table1_experiment.scorer_client import (
    DEFAULT_SCORER_URL, load_scorer_token, score_predictions, validate_connection,
    validate_public_report,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_split(split: str, config_path=DEFAULT_CONFIG_PATH) -> tuple:
    """Return (papers {key: txt path}, scorer_url) for a configured split.

    Splits must be disjoint so dev feedback can never describe holdout papers.
    """
    config_path = Path(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    splits = config.get("splits")
    if not isinstance(splits, dict) or split not in splits:
        raise ValueError("Unknown split")
    seen = set()
    for name, entry in splits.items():
        keys = entry.get("papers")
        if not isinstance(keys, list) or not keys or len(set(keys)) != len(keys):
            raise ValueError("Each split needs a nonempty list of unique papers")
        if seen & set(keys):
            raise ValueError("Splits must not share papers")
        seen |= set(keys)
    papers_dir = (config_path.parent / config["papers_dir"]).resolve()
    entry = splits[split]
    return ({key: papers_dir / f"{key}.txt" for key in entry["papers"]}, entry["scorer_url"])


def _check_path(path: Path) -> None:
    """Accidental-access guard only; not a filesystem or repository sandbox."""
    resolved = path.resolve()
    if ("gold_tables" in resolved.parts or path.name.endswith("_gold.json")
            or resolved.name.endswith("_gold.json")):
        raise ValueError("Experiment paths must not reference gold files or the gold directory")


def _now():
    return datetime.now(timezone.utc).isoformat()


def _write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                    encoding="utf-8")


def run_experiment(papers: dict, run_dir: Path, *, prompt_path=DEFAULT_PROMPT_PATH,
                   chat_fn=None, score_fn=None, scorer_url=DEFAULT_SCORER_URL,
                   token=None, max_new_tokens=DEFAULT_MAX_NEW_TOKENS,
                   timeout=30, model_label=None, max_extraction_attempts=3,
                   progress=None) -> dict:
    """Injected chat/scoring functions permit offline tests without credentials.

    Paper keys must match benchmark filename prefixes, not necessarily paper_id.
    Failed runs keep validated predictions and a sanitized failure log. They are
    never retried or overwritten automatically.
    """
    run_dir, prompt_path = Path(run_dir), Path(prompt_path)
    _check_path(run_dir)
    _check_path(prompt_path)
    if run_dir.exists():
        raise ValueError("Run directory already exists; choose a new run directory")
    if type(max_new_tokens) is not int or max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be a positive integer")
    if type(max_extraction_attempts) is not int or not 1 <= max_extraction_attempts <= 5:
        raise ValueError("max_extraction_attempts must be between 1 and 5")
    if not isinstance(papers, dict) or not papers:
        raise ValueError("Supply at least one paper keyed by benchmark filename prefix")
    sources = {}
    for key, path in papers.items():
        if not isinstance(key, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", key) is None:
            raise ValueError("Invalid paper key")
        path = Path(path)
        _check_path(path)
        if path.suffix.lower() != ".txt" or not path.is_file():
            raise ValueError("Each paper must be an existing text file")
        raw = path.read_bytes()
        sources[key] = (path.name, raw.decode("utf-8"), hashlib.sha256(raw).hexdigest())
    prompt = json.loads(prompt_path.read_text(encoding="utf-8"))
    validate_prompt_config(prompt)
    if not isinstance(prompt.get("version"), str) or not prompt["version"].strip():
        raise ValueError("Experiment prompts require a nonempty version")
    # Snapshot only extraction prompt fields, not arbitrary caller metadata.
    prompt = {key: prompt[key] for key in ("version", "system", "user", "guidance") if key in prompt}
    score_transport = "http" if score_fn is None else "injected"
    if score_fn is None:
        token = token if token is not None else load_scorer_token()
        validate_connection(scorer_url, token, timeout)
        def score_fn(predictions):
            return score_predictions(predictions, url=scorer_url, token=token, timeout=timeout)
    if chat_fn is None:
        from almog_work.common.openai_client import GPT_MODEL, run_gpt_chat
        chat_fn, model_label = run_gpt_chat, GPT_MODEL
        provider = "azure_openai"
    else:
        provider, model_label = "injected", model_label or "injected-chat"
    if not isinstance(model_label, str) or not model_label.strip():
        raise ValueError("model_label must be a nonempty string")
    run_dir.mkdir(parents=True, exist_ok=False)
    prediction_dir = run_dir / "predictions"
    prediction_dir.mkdir()
    _write_json(run_dir / "prompt.json", prompt)
    prompt_bytes = json.dumps(prompt, sort_keys=True, ensure_ascii=False).encode("utf-8")
    log = {
        "run_id": run_dir.name, "started_at": _now(), "status": "extracting",
        "prompt_version": prompt["version"], "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
        "model": {"provider": provider, "deployment": model_label,
                  "max_new_tokens": max_new_tokens},
        "table_number": 1, "max_table_section_chars": MAX_TABLE_SECTION_CHARS,
        "scoring": {"transport": score_transport,
                "timeout_seconds": timeout if score_transport == "http" else None,
                    "scope": "full scorer-configured benchmark", "request_attempted": False,
                    "automatic_retries": 0, "budget_scope": "scorer process"},
        "papers": [{"key": key, "source_file": name, "source_sha256": digest}
                   for key, (name, _, digest) in sources.items()],
    }
    _write_json(run_dir / "run.json", log)
    predictions = {}
    stage = "extraction"
    say = progress or (lambda message: None)
    try:
        for number, paper_log in enumerate(log["papers"], start=1):
            key = paper_log["key"]
            say(f"    extracting {key} ({number}/{len(log['papers'])})")
            # Only unusable model output (InvalidModelOutput) is retried; after the last
            # attempt the paper is scored as an empty prediction and logged. The scoring
            # call below is never retried. Attempts are logged.
            result = None
            for attempt in range(1, max_extraction_attempts + 1):
                paper_log["extraction_attempts"] = attempt
                try:
                    stats = {}
                    result = extract_table_one(sources[key][1], paper_id=key, chat_fn=chat_fn,
                                               prompt_config=prompt, max_new_tokens=max_new_tokens,
                                               stats=stats)
                    break
                except InvalidModelOutput:
                    _write_json(run_dir / "run.json", log)
                    if attempt < max_extraction_attempts:
                        say(f"    {key}: invalid model output, retrying (attempt {attempt + 1})")
            if result is None:
                paper_log.update(status="invalid_output", found=None, cells_extracted=0)
                predictions[key] = {"cells": []}
                say(f"    {key}: invalid output after {max_extraction_attempts} attempts; scored as empty")
                _write_json(run_dir / "run.json", log)
                continue
            filename = f"{key}_table_1_pred.json"
            _write_json(prediction_dir / filename, result)
            predictions[key] = {"cells": result["cells"]}
            paper_log.update(prediction=f"predictions/{filename}", found=result["found"],
                             cells_extracted=len(result["cells"]),
                             duplicates_dropped=stats.get("duplicates_dropped", 0))
            if stats.get("duplicates_dropped"):
                say(f"    {key}: dropped {stats['duplicates_dropped']} repeated cell(s)")
            _write_json(run_dir / "run.json", log)
        stage = "scoring"
        say("    all papers extracted; sending predictions to the scorer")
        log["status"] = "scoring"
        log["scoring"]["request_attempted"] = True
        _write_json(run_dir / "run.json", log)
        # Only validated cells are sent; raw source text is not sent to the scorer.
        report = validate_public_report(score_fn(predictions))
        _write_json(run_dir / "scores.json", report)
        log.update(status="completed", completed_at=_now(), score_file="scores.json")
        log["scoring"].update(feedback_remaining=report["feedback_remaining"],
                              evaluations_remaining=report["evaluations_remaining"])
        _write_json(run_dir / "run.json", log)
        return report
    except BaseException as error:
        # No exception text, model output, token or server body is persisted.
        log.update(status="failed", completed_at=_now(),
                   failure={"stage": stage, "exception_type": type(error).__name__})
        _write_json(run_dir / "run.json", log)
        raise


def main():
    parser = argparse.ArgumentParser(description="Separate Table-1 experiment: extract, save, score, log.")
    parser.add_argument("--paper", action="append", metavar="KEY=TEXT_PATH",
                        help="Repeat for each benchmark filename prefix; omitted benchmark papers score as missing")
    parser.add_argument("--split", choices=("dev", "holdout"),
                        help="Use papers and scorer URL of a split from config.json instead of --paper")
    parser.add_argument("--final", action="store_true",
                        help="Required for the holdout split; the holdout scorer allows one evaluation")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--run-dir", type=Path, help="New output folder; existing folders are never overwritten")
    parser.add_argument("--prompt-config", type=Path, default=DEFAULT_PROMPT_PATH)
    parser.add_argument("--scorer-url", default=DEFAULT_SCORER_URL)
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if bool(args.split) == bool(args.paper):
        parser.error("Use exactly one of --split or --paper")
    if args.split == "holdout" and not args.final:
        parser.error("The holdout split requires --final")
    papers = {}
    if args.split:
        try:
            papers, args.scorer_url = load_split(args.split, args.config)
        except (OSError, ValueError, KeyError):
            parser.error("Invalid config or split")
    for item in args.paper or []:
        key, separator, path = item.partition("=")
        if not separator or not path or key in papers:
            parser.error("Each --paper must specify a unique KEY=TEXT_PATH")
        papers[key] = Path(path)
    run_dir = args.run_dir or DATA_DIR / "table1_experiments" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8])
    try:
        report = run_experiment(papers, run_dir, prompt_path=args.prompt_config,
                                scorer_url=args.scorer_url, max_new_tokens=args.max_new_tokens,
                                timeout=args.timeout)
    except Exception:
        parser.exit(1, "Experiment failed. Check configuration/service and the sanitized run log if created. No retry was made.\n")
    print(f"Completed run: {run_dir}")
    print(f"Full-benchmark cell F1: {report['summary']['cells']['f1']}")
    print(f"Scorer evaluations remaining: {report['evaluations_remaining']}")


if __name__ == "__main__":
    main()