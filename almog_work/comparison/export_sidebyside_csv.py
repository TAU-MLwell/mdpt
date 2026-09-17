"""Export comparison results side-by-side: GPT vs Granite statements on one row per paper.

One row per paper, showing GPT and Granite extraction/validation results side by side.
Useful for manual evaluation of which model found what.

Usage:
    .venv/bin/python export_sidebyside_csv.py --input-dir ../data/comparison \
        --output ../data/comparison/comparison_sidebyside.csv
"""
import argparse
import csv
import json
from pathlib import Path


def flatten_sidebyside(paper_id, data):
    """Yield one row per statement index, with GPT and Granite columns side-by-side."""
    granite_result = data.get("granite", {})
    gpt_result = data.get("gpt", {})

    granite_extracted = granite_result.get("extracted", [])
    granite_validated = granite_result.get("validated", [])
    granite_elapsed = granite_result.get("elapsed_seconds", "")
    granite_error = granite_result.get("error", "")

    gpt_extracted = gpt_result.get("extracted", [])
    gpt_validated = gpt_result.get("validated", [])
    gpt_elapsed = gpt_result.get("elapsed_seconds", "")
    gpt_error = gpt_result.get("error", "")

    # Determine max index to iterate over
    max_idx = max(len(granite_extracted), len(gpt_extracted))

    for i in range(max_idx):
        row = {"paper_id": paper_id, "statement_index": i}

        # Granite columns
        if i < len(granite_extracted) and not granite_error:
            g_stmt = granite_extracted[i]
            g_verdict = granite_validated[i] if i < len(granite_validated) else {}
            row["granite_statement"] = g_stmt.get("statement_text", "")
            row["granite_type"] = g_stmt.get("statement_type", "")
            row["granite_verdict"] = g_verdict.get("verdict", "")
            row["granite_confidence"] = g_stmt.get("confidence", "")
        else:
            row["granite_statement"] = ""
            row["granite_type"] = ""
            row["granite_verdict"] = granite_error if granite_error else "(no statement)"
            row["granite_confidence"] = ""

        # GPT columns
        if i < len(gpt_extracted) and not gpt_error:
            gpt_stmt = gpt_extracted[i]
            gpt_verdict = gpt_validated[i] if i < len(gpt_validated) else {}
            row["gpt_statement"] = gpt_stmt.get("statement_text", "")
            row["gpt_type"] = gpt_stmt.get("statement_type", "")
            row["gpt_verdict"] = gpt_verdict.get("verdict", "")
            row["gpt_confidence"] = gpt_stmt.get("confidence", "")
        else:
            row["gpt_statement"] = ""
            row["gpt_type"] = ""
            row["gpt_verdict"] = gpt_error if gpt_error else "(no statement)"
            row["gpt_confidence"] = ""

        # Add timing info (only on first row for each paper)
        if i == 0:
            row["granite_elapsed_sec"] = granite_elapsed
            row["gpt_elapsed_sec"] = gpt_elapsed
        else:
            row["granite_elapsed_sec"] = ""
            row["gpt_elapsed_sec"] = ""

        yield row


def main():
    parser = argparse.ArgumentParser(description="Flatten comparison JSON outputs into a side-by-side CSV.")
    parser.add_argument("--input-dir", default="../data/comparison", help="Directory with per-paper JSON files")
    parser.add_argument("--output", default="../data/comparison/comparison_sidebyside.csv", help="CSV output path")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    rows = []
    for path in sorted(input_dir.glob("*.json")):
        if path.name == "summary.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        paper_id = data.get("pmid") or data.get("pmcid") or path.stem
        rows.extend(flatten_sidebyside(paper_id, data))

    fieldnames = [
        "paper_id", "statement_index",
        "granite_statement", "granite_type", "granite_verdict", "granite_confidence",
        "gpt_statement", "gpt_type", "gpt_verdict", "gpt_confidence",
        "granite_elapsed_sec", "gpt_elapsed_sec",
    ]
    output_path = Path(args.output)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
