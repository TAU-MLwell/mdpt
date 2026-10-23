"""Prompt-improvement loop: extract -> score -> improve guidance -> repeat.

The optimizer model sees only the fixed output format, previous guidance texts,
aggregate scores and the scorer's bounded public feedback. It never receives
reference tables, article text or file paths, and it can change only the
`guidance` field; the fixed output format in `user` is copied unchanged.

Trusted runner, same limits as run_experiment.py: not an OS sandbox.
"""
import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from almog_work.table1_experiment.extractor import (
    DEFAULT_MAX_NEW_TOKENS, DEFAULT_PROMPT_PATH, _parse_table_json, validate_prompt_config,
)
from almog_work.table1_experiment.run_experiment import (
    DATA_DIR, DEFAULT_CONFIG_PATH, _check_path, _write_json, load_split, run_experiment,
)
from almog_work.table1_experiment.scorer_client import DEFAULT_SCORER_URL, validate_public_report

MAX_GUIDANCE_CHARS = 8000
OPTIMIZER_MAX_NEW_TOKENS = 8000
PROMPT_KEYS = ("version", "system", "user", "guidance")

OPTIMIZER_SYSTEM = (
    "You improve the GUIDANCE section of a prompt that extracts Table 1 from biomedical "
    "articles into structured cells. You see only aggregate scores and a few bounded mistake "
    "descriptions; you never see the reference tables or the articles. Write general, reusable "
    "guidance about how to read and structure Table 1 content. Do not mention specific papers, "
    "diseases or drugs, and do not copy labels or values from the mistake examples. "
    "Return one JSON object only: {\"guidance\": \"<plain text>\"}."
)


def _snapshot(prompt: dict) -> dict:
    return {key: prompt[key] for key in PROMPT_KEYS}


def _metrics(report: dict) -> dict:
    cells, keys = report["summary"]["cells"], report["summary"]["keys_only"]
    return {"cell_f1": cells["f1"], "cell_precision": cells["precision"],
            "cell_recall": cells["recall"], "key_f1": keys["f1"],
            "value_accuracy": keys["value_accuracy_on_matched_keys"]}


def _invalid_papers(run_dir) -> list:
    """Paper keys whose model output stayed unusable (scored as empty); keys only."""
    log = json.loads((Path(run_dir) / "run.json").read_text(encoding="utf-8"))
    return [p["key"] for p in log["papers"] if p.get("status") == "invalid_output"]


def _duplicate_counts(run_dir) -> dict:
    """{paper key: number of repeated cells dropped}; counts only."""
    log = json.loads((Path(run_dir) / "run.json").read_text(encoding="utf-8"))
    return {p["key"]: p["duplicates_dropped"] for p in log["papers"]
            if p.get("duplicates_dropped")}


def build_optimizer_messages(best: dict, history: list) -> list:
    """`best` is a prompt dict; history items are {prompt, report}. No gold is involved."""
    contract = best["user"].replace("__TABLE_TEXT__", "<table text>").replace(
        "__GUIDANCE__", "<GUIDANCE GOES HERE>")
    lines = [
        "Fixed prompt (cannot be changed; your guidance is inserted where marked):",
        contract, "",
        "Scoring: a predicted cell is correct only if row_group, row_label, column_label and "
        "value all match the reference. Higher cell F1 is better (1.0 is perfect).",
        "Mistake types: 'extra_cell' = a predicted cell absent from the reference (its predicted "
        "value is shown); 'missing_cell' = a reference cell the extraction lacks (only its position "
        "is shown, its value is hidden).", "",
        "Previous attempts (version, cell F1, per-paper F1):",
    ]
    for item in history:
        report = item["report"]
        per_paper = ", ".join(f"{p['paper']}={p['cell_f1']}" for p in report["per_paper"])
        lines.append(f"- {item['prompt']['version']}: F1={report['summary']['cells']['f1']} ({per_paper})")
        if item.get("invalid_papers"):
            lines.append("  output not valid JSON/schema after 3 tries, scored as empty: "
                         + ", ".join(item["invalid_papers"]))
        if item.get("duplicates"):
            lines.append("  repeated cells (same row/group/column twice; extras were dropped): "
                         + ", ".join(f"{k}={n}" for k, n in item["duplicates"].items()))
        lines.append(f"  guidance ({len(item['prompt']['guidance'])} characters): "
                     f"{json.dumps(item['prompt']['guidance'], ensure_ascii=False)}")
    lines += ["", f"Current best guidance ({best['version']}): "
              + json.dumps(best["guidance"], ensure_ascii=False), "",
              "Mistake examples from the scorer (all attempts so far):"]
    examples = [(item["prompt"]["version"], e) for item in history
                for e in item["report"]["error_examples"]]
    if not examples:
        lines.append("(none available; use only the scores)")
    for version, e in examples:
        lines.append(f"- [{version}] {json.dumps(e, ensure_ascii=False)}")
    lines += ["", f"Write improved guidance (plain text). HARD LIMIT: at most {MAX_GUIDANCE_CHARS} "
              f"characters (about {MAX_GUIDANCE_CHARS // 7} words); longer replies are rejected. "
              "Aim for about 3000 characters (roughly 450 words). Earlier guidance above is "
              "already long: do not extend it; merge rules, delete redundant or low-value rules "
              "and examples, and keep only the most important points. The guidance must be "
              "different from all previous guidance. Address systematic patterns in how rows, "
              "row groups and column labels are chosen. Return JSON only."]
    return [{"role": "system", "content": OPTIMIZER_SYSTEM},
            {"role": "user", "content": "\n".join(lines)}]


def _guidance_problem(parsed: dict, seen: set):
    """Return (guidance, None) if acceptable, else (None, short reason sent back to the model)."""
    guidance = parsed.get("guidance")
    if set(parsed) != {"guidance"} or not isinstance(guidance, str) or not guidance.strip():
        return None, 'Return exactly one JSON object with only a nonempty string field "guidance".'
    if len(guidance) > MAX_GUIDANCE_CHARS:
        return None, (f"The guidance had {len(guidance)} characters; the limit is "
                      f"{MAX_GUIDANCE_CHARS}. Rewrite it at about 3000 characters by merging and "
                      "deleting rules, not by trimming the end.")
    if "__GUIDANCE__" in guidance or "__TABLE_TEXT__" in guidance:
        return None, "The guidance must not contain placeholder tokens."
    if guidance.strip() in seen:
        return None, "The guidance repeats an earlier version. Write different guidance."
    return guidance.strip(), None


def propose_guidance(best: dict, history: list, *, chat_fn=None, max_attempts=3,
                     max_new_tokens=OPTIMIZER_MAX_NEW_TOKENS) -> str:
    if chat_fn is None:
        from almog_work.common.openai_client import run_gpt_chat
        chat_fn = run_gpt_chat
    base_messages = build_optimizer_messages(best, history)
    seen = {item["prompt"]["guidance"].strip() for item in history}
    messages = base_messages
    for _ in range(max_attempts):
        reply, parsed_ok = None, False
        try:
            reply = chat_fn(messages=messages, max_new_tokens=max_new_tokens)
            guidance, reason = _guidance_problem(_parse_table_json(reply), seen)
            parsed_ok = True
        except ValueError:
            guidance, reason = None, ("The reply was not one complete JSON object (it may have "
                                      f"been cut off for length). Write much shorter guidance, "
                                      f"under {MAX_GUIDANCE_CHARS} characters.")
        if guidance is not None:
            return guidance
        # Retry with the rejection reason only (no reference data is involved).
        messages = base_messages + (
            [{"role": "assistant", "content": reply}] if parsed_ok and reply else []
        ) + [{"role": "user", "content": f"Rejected: {reason} Return corrected JSON only."}]
    raise ValueError("Optimizer did not return valid new guidance")


def _write_results(loop_dir: Path, rows: list, paper_keys: list) -> None:
    fields = (["iteration", "version", "status", "cell_f1", "cell_precision", "cell_recall",
               "key_f1", "value_accuracy"] + [f"f1_{key}" for key in paper_keys]
              + ["feedback_remaining", "evaluations_remaining", "is_best", "run_dir", "guidance"])
    with (loop_dir / "results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _row(iteration, prompt, report, run_dir, paper_keys):
    row = {"iteration": iteration, "version": prompt["version"], "status": "completed",
           **_metrics(report), "feedback_remaining": report["feedback_remaining"],
           "evaluations_remaining": report["evaluations_remaining"],
           "run_dir": str(run_dir), "guidance": prompt["guidance"], "is_best": False}
    scores = {p["paper"]: p["cell_f1"] for p in report["per_paper"]}
    for key in paper_keys:
        row[f"f1_{key}"] = scores.get(key)
    return row


def run_loop(papers: dict, loop_dir: Path, *, prompt_path=DEFAULT_PROMPT_PATH,
             max_iterations=4, min_improvement=0.005, patience=2,
             extract_chat_fn=None, optimizer_chat_fn=None, score_fn=None,
             scorer_url=DEFAULT_SCORER_URL, token=None,
             max_new_tokens=DEFAULT_MAX_NEW_TOKENS, timeout=30,
             reuse_baseline=None, progress=None) -> dict:
    """Baseline (or reused baseline run) plus up to max_iterations improved prompts."""
    loop_dir, prompt_path = Path(loop_dir), Path(prompt_path)
    _check_path(loop_dir)
    _check_path(prompt_path)
    if loop_dir.exists():
        raise ValueError("Loop directory already exists; choose a new directory")
    if type(max_iterations) is not int or not 1 <= max_iterations <= 20:
        raise ValueError("max_iterations must be between 1 and 20")
    if patience is not None and (type(patience) is not int or patience < 1):
        raise ValueError("patience must be a positive integer or None (no early stop)")
    if isinstance(min_improvement, bool) or not isinstance(min_improvement, (int, float)) or min_improvement < 0:
        raise ValueError("min_improvement must be a nonnegative number")
    baseline = json.loads(prompt_path.read_text(encoding="utf-8"))
    validate_prompt_config(baseline)
    if "guidance" not in baseline or not isinstance(baseline.get("version"), str):
        raise ValueError("The loop needs a prompt with a version and an editable guidance field")
    baseline = _snapshot(baseline)
    paper_keys = list(papers)
    loop_dir.mkdir(parents=True)
    (loop_dir / "prompts").mkdir()
    state = {"loop_id": loop_dir.name, "started_at": datetime.now(timezone.utc).isoformat(),
             "status": "running", "max_iterations": max_iterations,
             "min_improvement": min_improvement, "patience": patience,
             "baseline_version": baseline["version"], "baseline_reused": reuse_baseline is not None}
    _write_json(loop_dir / "loop.json", state)
    run_kwargs = dict(chat_fn=extract_chat_fn, score_fn=score_fn, scorer_url=scorer_url,
                      token=token, max_new_tokens=max_new_tokens, timeout=timeout,
                      progress=progress)
    say = progress or (lambda message: None)
    history, rows = [], []
    stage = "baseline"
    try:
        _write_json(loop_dir / "prompts" / "v00.json", baseline)
        if reuse_baseline is not None:
            reuse_baseline = Path(reuse_baseline)
            _check_path(reuse_baseline)
            if json.loads((reuse_baseline / "prompt.json").read_text(encoding="utf-8")) != baseline:
                raise ValueError("Reused baseline run used a different prompt")
            if json.loads((reuse_baseline / "run.json").read_text(encoding="utf-8")).get("status") != "completed":
                raise ValueError("Reused baseline run did not complete")
            report = validate_public_report(
                json.loads((reuse_baseline / "scores.json").read_text(encoding="utf-8")))
            baseline_run = reuse_baseline
        else:
            baseline_run = loop_dir / "runs" / "v00"
            say(f"[baseline] extracting {len(papers)} papers and scoring")
            report = run_experiment(papers, baseline_run, prompt_path=loop_dir / "prompts" / "v00.json",
                                    **run_kwargs)
        history.append({"prompt": baseline, "report": report,
                        "invalid_papers": _invalid_papers(baseline_run),
                        "duplicates": _duplicate_counts(baseline_run)})
        rows.append(_row(0, baseline, report, baseline_run, paper_keys))
        say(f"[baseline] done: cell F1 {report['summary']['cells']['f1']:.3f} "
            f"(evaluations left {report['evaluations_remaining']}, "
            f"feedback left {report['feedback_remaining']})")
        best_index, no_gain, stop_reason = 0, 0, "max_iterations"
        rows[0]["is_best"] = True
        _write_results(loop_dir, rows, paper_keys)
        for iteration in range(1, max_iterations + 1):
            if report["evaluations_remaining"] <= 0:
                stop_reason = "evaluation_budget"
                break
            stage = f"iteration_{iteration}_propose"
            best = history[best_index]["prompt"]
            say(f"[iteration {iteration}/{max_iterations}] asking the optimizer for new guidance")
            guidance = propose_guidance(best, history, chat_fn=optimizer_chat_fn)
            prompt = {**baseline, "version": f"v{iteration:02d}", "guidance": guidance}
            validate_prompt_config(prompt)
            prompt_file = loop_dir / "prompts" / f"{prompt['version']}.json"
            _write_json(prompt_file, prompt)
            say(f"[iteration {iteration}/{max_iterations}] {prompt['version']} guidance written "
                f"({len(guidance)} chars); extracting and scoring")
            stage = f"iteration_{iteration}_run"
            run_dir = loop_dir / "runs" / prompt["version"]
            report = run_experiment(papers, run_dir, prompt_path=prompt_file, **run_kwargs)
            history.append({"prompt": prompt, "report": report,
                            "invalid_papers": _invalid_papers(run_dir),
                            "duplicates": _duplicate_counts(run_dir)})
            rows.append(_row(iteration, prompt, report, run_dir, paper_keys))
            previous_best = history[best_index]["report"]["summary"]["cells"]["f1"]
            current = report["summary"]["cells"]["f1"]
            if current > previous_best:
                best_index = len(history) - 1
            no_gain = 0 if current - previous_best >= min_improvement else no_gain + 1
            for row in rows:
                row["is_best"] = False
            rows[best_index]["is_best"] = True
            _write_results(loop_dir, rows, paper_keys)
            say(f"[iteration {iteration}/{max_iterations}] done: {prompt['version']} cell F1 "
                f"{current:.3f} (previous best {previous_best:.3f}); best so far "
                f"{history[best_index]['prompt']['version']}; evaluations left "
                f"{report['evaluations_remaining']}, feedback left {report['feedback_remaining']}")
            if patience is not None and no_gain >= patience:
                stop_reason = "no_improvement"
                break
        best_prompt = history[best_index]["prompt"]
        _write_json(loop_dir / "best_prompt.json", best_prompt)
        state.update(status="completed", completed_at=datetime.now(timezone.utc).isoformat(),
                     stop_reason=stop_reason, iterations_run=len(history) - 1,
                     best_version=best_prompt["version"],
                     best_prompt_sha256=hashlib.sha256(
                         json.dumps(best_prompt, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
                     baseline_cell_f1=history[0]["report"]["summary"]["cells"]["f1"],
                     best_cell_f1=history[best_index]["report"]["summary"]["cells"]["f1"])
        _write_json(loop_dir / "loop.json", state)
        return state
    except BaseException as error:
        # No exception text, model output or server body is persisted.
        state.update(status="failed", completed_at=datetime.now(timezone.utc).isoformat(),
                     failure={"stage": stage, "exception_type": type(error).__name__})
        _write_json(loop_dir / "loop.json", state)
        say(f"[failed] stage {stage}, {type(error).__name__}; see loop.json")
        raise


def main():
    parser = argparse.ArgumentParser(description="Table-1 prompt-improvement loop on the dev split.")
    parser.add_argument("--loop-dir", type=Path, help="New folder; existing folders are never overwritten")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--prompt-config", type=Path, default=DEFAULT_PROMPT_PATH)
    parser.add_argument("--reuse-baseline", type=Path,
                        help="Completed run folder that used exactly the baseline prompt (saves an evaluation)")
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    try:
        papers, scorer_url = load_split("dev", args.config)
        loop_config = json.loads(args.config.read_text(encoding="utf-8"))["loop"]
    except (OSError, ValueError, KeyError):
        parser.error("Invalid config")
    loop_dir = args.loop_dir or DATA_DIR / "table1_experiments" / (
        "loop_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8])
    try:
        print(f"Loop folder: {loop_dir}", flush=True)
        state = run_loop(papers, loop_dir, prompt_path=args.prompt_config,
                         max_iterations=loop_config["max_iterations"],
                         min_improvement=loop_config["min_improvement"],
                         patience=loop_config["patience"], scorer_url=scorer_url,
                         max_new_tokens=args.max_new_tokens, timeout=args.timeout,
                         reuse_baseline=args.reuse_baseline,
                         progress=lambda message: print(message, flush=True))
    except Exception:
        parser.exit(1, "Loop failed. See loop.json and the run logs in the loop folder. No retry was made.\n")
    print(f"Loop finished: {loop_dir}")
    print(f"Stop reason: {state['stop_reason']}; iterations run: {state['iterations_run']}")
    print(f"Cell F1: baseline {state['baseline_cell_f1']} -> best {state['best_cell_f1']} ({state['best_version']})")


if __name__ == "__main__":
    main()
