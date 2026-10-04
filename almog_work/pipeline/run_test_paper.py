#!/usr/bin/env python
"""Test extraction pipeline on local paper file (e.g., food_allergy_paper.txt).

Runs extraction + validation on a paper already saved locally.
Output goes to dated folder.

Usage:
    .venv/bin/python run_test_paper.py --file ../data/food_allergy_paper.txt
    # Creates ../data/2026-09-19/food_allergy_paper.json
"""
import argparse
import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "extraction"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "validation"))

from openai_client import run_gpt_chat
from extraction_agent import extract_clinical_statements
from validation_agent import validate_clinical_statements

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main():
    parser = argparse.ArgumentParser(description="Test extraction on a local paper file.")
    parser.add_argument("--file", required=True, help="Path to paper text file")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: ../data/YYYY-MM-DD/)")
    parser.add_argument("--pmid", default="unknown", help="Paper ID for output JSON")
    args = parser.parse_args()

    # Load paper
    paper_path = Path(args.file)
    if not paper_path.exists():
        print(f"Error: {paper_path} not found")
        sys.exit(1)

    article_text = paper_path.read_text(encoding="utf-8")

    # Determine output directory
    if args.output_dir is None:
        today = datetime.now().strftime("%Y-%m-%d")
        args.output_dir = DATA_DIR / today

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Paper: {paper_path.name} ({len(article_text)} chars)")
    print(f"Output: {output_dir}/")
    print("=" * 80)

    # Extract
    print(f"\n1. Extracting population-statistics...")
    start = time.perf_counter()
    extracted = extract_clinical_statements(article_text, chat_fn=run_gpt_chat, max_new_tokens=8000)
    extract_time = time.perf_counter() - start
    print(f"   ✓ Extracted {len(extracted)} statements in {extract_time:.1f}s")

    # Validate
    print(f"\n2. Validating {len(extracted)} statements...")
    start = time.perf_counter()
    validated = validate_clinical_statements(extracted, chat_fn=run_gpt_chat, max_new_tokens=8000)
    validate_time = time.perf_counter() - start
    print(f"   ✓ Validated {len(validated)} statements in {validate_time:.1f}s")

    # Verdict summary
    verdicts = {}
    for v in validated:
        verdict = v.get("verdict", "unknown")
        verdicts[verdict] = verdicts.get(verdict, 0) + 1

    print(f"\n3. Verdict breakdown:")
    for verdict, count in sorted(verdicts.items()):
        print(f"   {verdict}: {count}")

    # Save result
    result = {
        "paper_id": args.pmid,
        "gpt": {
            "extracted": extracted,
            "validated": validated,
            "elapsed_seconds": round(extract_time + validate_time, 2),
            "extract_time": round(extract_time, 2),
            "validate_time": round(validate_time, 2),
        }
    }

    json_path = output_dir / f"{paper_path.stem}.json"
    json_path.write_text(json.dumps(result, indent=2))
    print(f"\n✅ Results saved: {json_path}")

    # Show samples
    print("\n" + "=" * 80)
    print("SAMPLE STATEMENTS (first 3)")
    print("=" * 80)
    for i, (stmt, valid) in enumerate(zip(extracted[:3], validated[:3]), 1):
        print(f"\n[{i}] {stmt.get('statistical_finding', '')[:80]}...")
        print(f"    Population: {stmt.get('population_description', '')[:60]}...")
        print(f"    Verdict: {valid.get('verdict', 'N/A')}")


if __name__ == "__main__":
    main()
