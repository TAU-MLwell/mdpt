"""Extract population-specific statistics from papers using GPT.

Fetches papers from PMC, runs extraction + validation with GPT on each paper,
and saves per-paper results plus a summary to a dated folder.

Usage:
    .venv/bin/python run_batch_pipeline.py --query "hypertension treatment" --n 10
    # Creates ../data/2026-09-19/ automatically (or specify --output-dir)
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data_acquisition"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "extraction"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "validation"))

from openai_client import run_gpt_chat
from pmc_fetch import search_pmc, pmc_url_from_id, fetch_pmc_text
from extraction_agent import extract_clinical_statements
from validation_agent import validate_clinical_statements

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def run_extraction_pipeline(article_text, chat_fn, max_new_tokens=8000):
    """Run extraction then validation, returning both results."""
    extracted = extract_clinical_statements(article_text, chat_fn=chat_fn, max_new_tokens=max_new_tokens)
    validated = validate_clinical_statements(extracted, chat_fn=chat_fn, max_new_tokens=max_new_tokens)
    return extracted, validated


def summarize(validated):
    """Count verdicts for a quick summary."""
    counts = {}
    for item in validated:
        verdict = item.get("verdict", "unknown")
        counts[verdict] = counts.get(verdict, 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Extract population-specific statistics from papers using GPT.")
    parser.add_argument("--query", required=True, help="PMC search query, e.g. 'hypertension treatment'")
    parser.add_argument("--n", type=int, default=10, help="Number of papers to fetch")
    parser.add_argument("--output-dir", default=None, help="Directory to write results to (default: ../data/YYYY-MM-DD/)")
    args = parser.parse_args()

    # Use dated folder if not specified
    if args.output_dir is None:
        today = datetime.now().strftime("%Y-%m-%d")
        args.output_dir = DATA_DIR / today

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Searching PMC for '{args.query}' ({args.n} papers)...")
    pmcids = search_pmc(args.query, retmax=args.n)
    print(f"Found {len(pmcids)} papers: {pmcids}")
    print(f"Output folder: {output_dir}/\n")

    summary = []

    for pmcid in pmcids:
        print(f"--- {pmcid} ---")
        article_text = fetch_pmc_text(pmc_url_from_id(pmcid), char_limit=500000)
        if not article_text:
            print(f"Skipping {pmcid}: could not fetch text.")
            continue

        result = {"pmcid": pmcid}
        print(f"Running extraction + validation...")
        start = time.perf_counter()
        try:
            extracted, validated = run_extraction_pipeline(article_text, run_gpt_chat, max_new_tokens=8000)
            elapsed = time.perf_counter() - start
            result["gpt"] = {
                "extracted": extracted,
                "validated": validated,
                "elapsed_seconds": round(elapsed, 2),
            }
            print(f"  ✓ {len(extracted)} extracted, {len(validated)} validated, {elapsed:.1f}s")
        except Exception as exc:
            result["gpt"] = {"error": str(exc)}
            print(f"  ✗ Error: {exc}")

        paper_path = output_dir / f"{pmcid}.json"
        paper_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        summary.append({
            "pmcid": pmcid,
            "gpt_count": len(result.get("gpt", {}).get("extracted", [])),
            "gpt_verdicts": summarize(result.get("gpt", {}).get("validated", [])),
        })

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n✅ Done. Results written to {output_dir}/")


if __name__ == "__main__":
    main()
