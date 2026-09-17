"""Flatten compare_models.py per-paper JSON outputs into one CSV for easy manual review.

One row per extracted statement (per paper, per backend), with its validation verdict
lined up next to it. Open the result in Excel/Google Sheets and sort/filter by paper,
backend, or verdict instead of reading nested JSON by hand.

Usage:
    .venv/bin/python export_comparison_csv.py --input-dir ../data/comparison \
        --output ../data/comparison/comparison_flat.csv
"""
import argparse
import csv
import json
from pathlib import Path


def flatten_paper(paper_id, data):
    """Yield one flat row per (backend, statement) pair for a single paper's result."""
    for backend in ("granite", "gpt"):
        backend_result = data.get(backend, {})
        if "error" in backend_result:
            yield {
                "paper_id": paper_id,
                "backend": backend,
                "elapsed_seconds": "",
                "statement_index": "",
                "statement_text": "",
                "statement_type": "",
                "verdict": "ERROR",
                "confidence": "",
                "evidence_span": backend_result["error"],
            }
            continue

        extracted = backend_result.get("extracted", [])
        validated = backend_result.get("validated", [])
        elapsed = backend_result.get("elapsed_seconds", "")

        # validated is expected to be extracted statements + a "verdict" field, in the
        # same order as extracted. Fall back gracefully if lengths differ.
        for i, statement in enumerate(extracted):
            verdict_item = validated[i] if i < len(validated) else {}
            yield {
                "paper_id": paper_id,
                "backend": backend,
                "elapsed_seconds": elapsed,
                "statement_index": i,
                "statement_text": statement.get("statement_text", ""),
                "statement_type": statement.get("statement_type", ""),
                "verdict": verdict_item.get("verdict", ""),
                "confidence": statement.get("confidence", ""),
                "evidence_span": statement.get("evidence_span", ""),
            }


def main():
    parser = argparse.ArgumentParser(description="Flatten comparison JSON outputs into a CSV.")
    parser.add_argument("--input-dir", default="../data/comparison", help="Directory with per-paper JSON files")
    parser.add_argument("--output", default="../data/comparison/comparison_flat.csv", help="CSV output path")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    rows = []
    for path in sorted(input_dir.glob("*.json")):
        if path.name == "summary.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        paper_id = data.get("pmid") or data.get("pmcid") or path.stem
        rows.extend(flatten_paper(paper_id, data))

    fieldnames = [
        "paper_id", "backend", "elapsed_seconds", "statement_index",
        "statement_text", "statement_type", "verdict", "confidence", "evidence_span",
    ]
    output_path = Path(args.output)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
