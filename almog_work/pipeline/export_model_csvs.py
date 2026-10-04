"""Export GPT extraction results as CSV with paper links.

One CSV per model, consolidates all statements from all papers.
One row per extracted population-statistic pair.
Includes link to source paper for manual verification.

Usage:
    .venv/bin/python export_model_csvs.py --input-dir ../data/2026-09-19/
    # Outputs gpt.csv to same directory
"""
import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def pmc_url_from_id(pmcid: str) -> str:
    """Build the standard PMC article page URL for a given PMCID."""
    return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"


def export_model_csv(model_name, paper_id, pmcid, extracted, validated, output_dir):
    """Export extracted population-statistic pairs to CSV."""
    rows = []
    for i, stmt in enumerate(extracted):
        # Find matching validated item
        verdict_item = {}
        if i < len(validated):
            verdict_item = validated[i]
        
        rows.append({
            "paper_id": paper_id,
            "paper_url": pmc_url_from_id(pmcid),
            "statement_index": i + 1,
            "population_description": stmt.get("population_description", ""),
            "population_source_span": stmt.get("population_source_span", ""),
            "statistical_finding": stmt.get("statistical_finding", ""),
            "statistical_source_span": stmt.get("statistical_source_span", ""),
            "variables": json.dumps(stmt.get("variables", [])),
            "context": stmt.get("context", ""),
            "confidence": stmt.get("confidence", ""),
            "verdict": verdict_item.get("verdict", "NOT_VALIDATED"),
        })

    fieldnames = [
        "paper_id", "paper_url", "statement_index",
        "population_description", "population_source_span",
        "statistical_finding", "statistical_source_span",
        "variables", "context", "confidence", "verdict",
    ]

    csv_path = Path(output_dir) / f"{model_name}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main():
    parser = argparse.ArgumentParser(description="Export extraction results as CSV.")
    parser.add_argument("--input-dir", default=None, help="Directory with per-paper JSON files (default: ../data/YYYY-MM-DD/)")
    parser.add_argument("--output-dir", default=None, help="Directory to write CSVs to (default: same as input-dir)")
    args = parser.parse_args()

    # Use dated folder if not specified
    if args.input_dir is None:
        today = datetime.now().strftime("%Y-%m-%d")
        args.input_dir = DATA_DIR / today
    
    # Output dir defaults to input dir
    if args.output_dir is None:
        args.output_dir = args.input_dir

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(input_dir.glob("*.json")):
        if path.name == "summary.json":
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        paper_id = data.get("pmid") or data.get("pmcid") or path.stem
        pmcid = data.get("pmcid", "")

        for model_name in ("gpt",):
            model_result = data.get(model_name, {})
            if "error" in model_result:
                print(f"  {model_name}: ERROR — {model_result['error']}")
                continue

            extracted = model_result.get("extracted", [])
            validated = model_result.get("validated", [])
            count = export_model_csv(model_name, paper_id, pmcid, extracted, validated, output_dir)
            print(f"  {model_name}: {count} statements → {model_name}.csv")


if __name__ == "__main__":
    main()
