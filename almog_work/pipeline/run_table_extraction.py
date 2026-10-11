#!/usr/bin/env python
"""Extract a single table (e.g., Table 1) from a local paper text file and save it as JSON.

This is the first step of building the Table-1 gold validation set: run this on each
candidate paper to get the model's reconstructed table, then manually correct the output
JSON to produce the gold-standard file (see --output naming below).

Usage:
    .venv/bin/python run_table_extraction.py --file ../data/test_paper.txt
    # Writes ../data/gold_tables/test_paper_table_1_pred.json

    .venv/bin/python run_table_extraction.py --file ../data/test_paper.txt --table-number 2
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "extraction"))

from openai_client import run_gpt_chat
from table_extraction_agent import extract_table

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main():
    parser = argparse.ArgumentParser(description="Extract a single table from a local paper file.")
    parser.add_argument("--file", required=True, help="Path to paper text file")
    parser.add_argument("--table-number", type=int, default=1, help="Which table to extract (default: 1)")
    parser.add_argument("--pmid", default=None, help="Paper ID to record in the output (default: filename stem)")
    parser.add_argument("--output", default=None, help="Output JSON path (default: ../data/gold_tables/<paper_id>_table_<n>_pred.json)")
    args = parser.parse_args()

    paper_path = Path(args.file)
    if not paper_path.exists():
        print(f"Error: {paper_path} not found")
        sys.exit(1)

    paper_id = args.pmid or paper_path.stem
    article_text = paper_path.read_text(encoding="utf-8")

    print(f"Paper: {paper_path.name} ({len(article_text)} chars)")
    print(f"Extracting Table {args.table_number}...")

    result = extract_table(
        article_text,
        table_number=args.table_number,
        chat_fn=run_gpt_chat,
        paper_id=paper_id,
    )

    if not result["found"]:
        print(f"  Table {args.table_number} caption not found in article text.")
        sys.exit(1)

    print(f"  Title: {result['table_title']}")
    print(f"  Columns: {result['columns']}")
    print(f"  Cells extracted: {len(result['cells'])}")

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = DATA_DIR / "gold_tables" / f"{paper_id}_table_{args.table_number}_pred.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Saved: {output_path}")
    print("   Review and hand-correct this file, then save the corrected copy as "
          f"{paper_id}_table_{args.table_number}_gold.json in the same folder to build the gold set.")


if __name__ == "__main__":
    main()
