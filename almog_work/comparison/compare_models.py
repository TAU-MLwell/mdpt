"""Compare the local Granite pipeline against GPT (via OpenAI) on the same set of papers.

Fetches papers from PMC, runs extraction + validation with both backends on each paper,
and saves per-paper results plus a summary comparison.

Usage:
    .venv/bin/python compare_models.py --query "hypertension treatment" --n 10 \
        --output-dir ../data/comparison
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data_acquisition"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "extraction"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "validation"))

from local_granite_client import run_granite_chat
from openai_client import run_gpt_chat
from pmc_fetch import search_pmc, pmc_url_from_id, fetch_pmc_text
from extraction_agent import extract_clinical_statements
from validation_agent import validate_clinical_statements

BACKENDS = {
    "granite": run_granite_chat,
    "gpt": run_gpt_chat,
}


def run_pipeline_for_backend(article_text, chat_fn):
    """Run extraction then validation for a single backend, returning both results."""
    extracted = extract_clinical_statements(article_text, chat_fn=chat_fn)
    validated = validate_clinical_statements(extracted, chat_fn=chat_fn)
    return extracted, validated


def summarize(validated):
    """Count verdicts for a quick comparison signal."""
    counts = {}
    for item in validated:
        verdict = item.get("verdict", "unknown")
        counts[verdict] = counts.get(verdict, 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Compare local Granite vs GPT on the extraction/validation pipeline.")
    parser.add_argument("--query", required=True, help="PMC search query, e.g. 'hypertension treatment'")
    parser.add_argument("--n", type=int, default=10, help="Number of papers to fetch")
    parser.add_argument("--output-dir", default="../data/comparison", help="Directory to write results to")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Searching PMC for '{args.query}' ({args.n} papers)...")
    pmcids = search_pmc(args.query, retmax=args.n)
    print(f"Found {len(pmcids)} papers: {pmcids}")

    summary = []

    for pmcid in pmcids:
        print(f"\n--- {pmcid} ---")
        article_text = fetch_pmc_text(pmc_url_from_id(pmcid))
        if not article_text:
            print(f"Skipping {pmcid}: could not fetch text.")
            continue

        result = {"pmcid": pmcid}
        for backend_name, chat_fn in BACKENDS.items():
            print(f"Running {backend_name}...")
            start = time.perf_counter()
            try:
                extracted, validated = run_pipeline_for_backend(article_text, chat_fn)
                elapsed = time.perf_counter() - start
                result[backend_name] = {
                    "extracted": extracted,
                    "validated": validated,
                    "elapsed_seconds": round(elapsed, 2),
                }
                print(f"  {backend_name}: {len(extracted)} extracted, {len(validated)} validated, {elapsed:.1f}s")
            except Exception as exc:
                result[backend_name] = {"error": str(exc)}
                print(f"  {backend_name} failed: {exc}")

        paper_path = output_dir / f"{pmcid}.json"
        paper_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        summary.append({
            "pmcid": pmcid,
            "granite_count": len(result.get("granite", {}).get("extracted", [])),
            "gpt_count": len(result.get("gpt", {}).get("extracted", [])),
            "granite_verdicts": summarize(result.get("granite", {}).get("validated", [])),
            "gpt_verdicts": summarize(result.get("gpt", {}).get("validated", [])),
        })

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nDone. Per-paper results and summary.json written to {output_dir}/")


if __name__ == "__main__":
    main()
