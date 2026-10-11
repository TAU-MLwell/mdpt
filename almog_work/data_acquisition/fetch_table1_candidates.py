#!/usr/bin/env python
"""Find and download PMC papers whose Table 1 looks like a descriptive-statistics /
"baseline characteristics" table (similar in shape to almog_work/data/test_paper.txt),
so they can be fed into the Table-1 extraction pipeline.

Since PMC search can't filter on "does Table 1 contain descriptive stats" directly, this
script does it in two steps:
  1. Search PMC with a query biased toward observational studies that typically carry a
     classic "Table 1" baseline-characteristics table (cohort/case-control studies with
     "baseline characteristics" / "table 1" wording).
  2. For each candidate, fetch full text, locate the Table 1 section (same boundary logic
     used by the extraction agent), and score it with a cheap heuristic that checks for the
     hallmarks of a descriptive table: many "n (%)" / "%" occurrences, and at least one of
     p-value / SMD / mean±SD wording. Only candidates that pass are kept.

Usage:
    .venv/bin/python fetch_table1_candidates.py --n 9
    # Searches, filters, and saves full text to ../data/table1_papers/<pmcid>.txt
    # plus a manifest at ../data/table1_papers/manifest.json
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "extraction"))

from pmc_fetch import search_pmc, pmc_url_from_id, fetch_pmc_text
from table_extraction_agent import find_table_section

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_OUTPUT_DIR = DATA_DIR / "table1_papers"

# Biased toward papers that typically include a classic baseline-characteristics Table 1.
# Note: PMC's esearch doesn't support PubMed-only field tags like [Title/Abstract] or
# [Filter], so this uses plain keyword terms instead.
DEFAULT_QUERY = (
    '"baseline characteristics" AND (cohort OR "case-control" OR retrospective) '
    'AND "table 1" AND "open access"[filter]'
)

MIN_SECTION_CHARS = 400
MAX_SECTION_CHARS = 20000
MIN_PERCENT_OCCURRENCES = 5
# Require an actual comparison-stat column (not just incidental % mentions).
COMPARISON_STAT_KEYWORDS = ("p value", "p-value", "pvalue", "smd")
# Require the caption to explicitly describe a characteristics/comparison table.
CAPTION_KEYWORDS = ("characteristic", "comparison", "demographic")
# Require at least 2 distinct group-size markers like '(n = 83)' / '(n=40)' to confirm
# this is a multi-group comparison table, not a single-group listing.
_GROUP_SIZE_PATTERN = re.compile(r"\(\s*n\s*=\s*[\d,]+\s*\)", re.IGNORECASE)
MIN_GROUP_SIZE_MARKERS = 2


def looks_like_descriptive_table(section_text: str) -> bool:
    """Heuristic: does this table section look like a Table 1 of descriptive stats
    comparing 2+ groups (like the reference test_paper), rather than some other table
    type (study design overview, single-group listing, composition table, etc.)?
    """
    length = len(section_text)
    if length < MIN_SECTION_CHARS or length > MAX_SECTION_CHARS:
        return False

    percent_count = section_text.count("%")
    if percent_count < MIN_PERCENT_OCCURRENCES:
        return False

    lowered = section_text.lower()
    if not any(keyword in lowered for keyword in COMPARISON_STAT_KEYWORDS):
        return False

    # Caption is the first line of the section text.
    caption_line = section_text.split("\n", 1)[0].lower()
    if not any(keyword in caption_line for keyword in CAPTION_KEYWORDS):
        return False

    if len(_GROUP_SIZE_PATTERN.findall(section_text)) < MIN_GROUP_SIZE_MARKERS:
        return False

    return True


def find_candidates(query: str, n_needed: int, search_pool: int, char_limit: int, delay: float, exclude_pmcids=()):
    """Search PMC and return up to n_needed candidates whose Table 1 passes the heuristic."""
    print(f"Searching PMC: {query}")
    pmcids = search_pmc(query, retmax=search_pool)
    print(f"Found {len(pmcids)} candidate PMCIDs to screen.\n")

    exclude_set = set(exclude_pmcids)
    kept = []
    for pmcid in pmcids:
        if len(kept) >= n_needed:
            break

        if pmcid in exclude_set:
            continue

        print(f"--- {pmcid} ---")
        article_text = fetch_pmc_text(pmc_url_from_id(pmcid), char_limit=char_limit)
        if not article_text:
            print("  skip: could not fetch full text")
            time.sleep(delay)
            continue

        section = find_table_section(article_text, table_number=1)
        if not section:
            print("  skip: no Table 1 caption found")
            time.sleep(delay)
            continue

        section_text, _, _ = section
        if not looks_like_descriptive_table(section_text):
            print(f"  skip: Table 1 doesn't look like descriptive stats ({len(section_text)} chars)")
            time.sleep(delay)
            continue

        print(f"  keep: Table 1 looks like descriptive stats ({len(section_text)} chars)")
        kept.append({
            "pmcid": pmcid,
            "pmc_url": pmc_url_from_id(pmcid),
            "article_text": article_text,
            "table1_char_count": len(section_text),
        })
        time.sleep(delay)

    return kept


def main():
    parser = argparse.ArgumentParser(description="Find PMC papers with a Table 1 of descriptive statistics.")
    parser.add_argument("--n", type=int, default=9, help="Number of papers to keep (default: 9)")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="PMC search query override")
    parser.add_argument("--search-pool", type=int, default=60, help="How many PMC search results to screen")
    parser.add_argument("--char-limit", type=int, default=200000, help="Max chars of full text to fetch per paper")
    parser.add_argument("--delay", type=float, default=0.4, help="Seconds to sleep between PMC requests")
    parser.add_argument("--output-dir", default=None, help="Directory to save full text + manifest")
    parser.add_argument("--exclude", default=None, help="Comma-separated PMCIDs to skip (e.g. already-kept ones)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    exclude_pmcids = {p.strip() for p in args.exclude.split(",")} if args.exclude else set()

    kept = find_candidates(
        query=args.query,
        n_needed=args.n,
        search_pool=args.search_pool,
        char_limit=args.char_limit,
        delay=args.delay,
        exclude_pmcids=exclude_pmcids,
    )

    manifest = []
    for item in kept:
        pmcid = item["pmcid"]
        text_path = output_dir / f"{pmcid}.txt"
        text_path.write_text(item["article_text"], encoding="utf-8")
        manifest.append({
            "pmcid": pmcid,
            "pmc_url": item["pmc_url"],
            "file": str(text_path.relative_to(DATA_DIR)),
            "table1_char_count": item["table1_char_count"],
        })

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\n✅ Kept {len(kept)}/{args.n} requested papers.")
    print(f"   Full text saved to: {output_dir}/")
    print(f"   Manifest: {manifest_path}")
    if len(kept) < args.n:
        print("   Fewer than requested were found — try a larger --search-pool or a broader --query.")


if __name__ == "__main__":
    main()
