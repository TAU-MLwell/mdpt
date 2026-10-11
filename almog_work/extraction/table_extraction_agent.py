"""Extract a single named table (e.g., "Table 1") from a biomedical article's plain text.

Full-text articles converted from HTML/PDF to plain text often flatten tables so that
column headers and cell values appear out of their original visual order (fragmented
headers, values listed row-by-row but detached from their labels, etc.). This module:

1. Locates the raw text span belonging to a specific table (by its "Table N." caption).
2. Sends that span to an LLM with a prompt dedicated to reconstructing the row/column
   structure, using numeric consistency checks (sums, percentages) as disambiguation clues.
3. Returns a "tidy" list of per-cell records: one record per (row_label, column_label) pair.

The tidy cell-record format is intentionally simple (a flat list of facts) so that it can
be used both as the model's prediction and, after manual correction, as the gold-standard
annotation for scoring (precision/recall per cell).
"""
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

from json_repair import repair_json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from openai_client import run_gpt_chat

DEFAULT_MAX_NEW_TOKENS = 4000
# Safety cap on how much text we feed the model for a single table, in case no
# clear "next table" or section boundary is found after the requested table's caption.
MAX_TABLE_SECTION_CHARS = 20000

# Headings that typically mark the end of the results/tables portion of a paper.
_SECTION_END_PATTERN = re.compile(
    r"^(Discussion|Conclusions?|References|Acknowledg(e)?ments|Author Contributions)\b",
    re.MULTILINE,
)


def _table_heading_pattern(table_number: int) -> re.Pattern:
    """Match a real table caption line, e.g. 'Table 1. Comparison of ...'.

    Anchored to the start of a line and requiring a capitalized word after the period
    so that inline references like '(Table 1; Fig. 4b)' or 'Tables 1, 2' are not matched.
    """
    return re.compile(rf"^Table\s+{table_number}\.\s+[A-Z]", re.MULTILINE)


_ANY_TABLE_HEADING_PATTERN = re.compile(r"^Table\s+(\d+)\.\s+[A-Z]", re.MULTILINE)


def _parse_table_json(raw_text: str) -> Dict[str, Any]:
    """Parse a top-level JSON OBJECT from model output (not a bare JSON array).

    Handles markdown code fences and falls back to json_repair for malformed/truncated
    output, then slices between the outermost braces as a last resort.
    """
    text = raw_text.strip()
    if not text:
        return {}

    if "```" in text:
        match = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.S | re.I)
        if match:
            text = match[0].strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, (dict, list)):
            return parsed
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    candidate = text[start : end + 1] if (start != -1 and end != -1 and end > start) else text

    try:
        parsed = json.loads(candidate)
        if isinstance(parsed, (dict, list)):
            return parsed
    except json.JSONDecodeError:
        pass

    try:
        repaired = repair_json(candidate)
        parsed = json.loads(repaired)
        if isinstance(parsed, (dict, list)):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass

    raise ValueError(f"Could not parse model output as JSON object. Raw output: {raw_text[:500]}")


def find_table_section(
    article_text: str,
    table_number: int = 1,
    max_chars: int = MAX_TABLE_SECTION_CHARS,
) -> Optional[Tuple[str, int, int]]:
    """Find the raw text span for a given table's caption + body.

    Returns (section_text, start_index, end_index), or None if the table caption
    could not be located in the article text.
    """
    start_match = _table_heading_pattern(table_number).search(article_text)
    if not start_match:
        return None
    start_idx = start_match.start()

    # End boundary: the next "Table N." heading (any number other than this one),
    # or the start of a post-results section (Discussion, References, ...),
    # whichever comes first.
    end_idx = len(article_text)
    for match in _ANY_TABLE_HEADING_PATTERN.finditer(article_text, start_match.end()):
        if int(match.group(1)) != table_number:
            end_idx = match.start()
            break

    section_end_match = _SECTION_END_PATTERN.search(article_text, start_match.end())
    if section_end_match and section_end_match.start() < end_idx:
        end_idx = section_end_match.start()

    # Safety cap in case neither boundary was found nearby.
    if end_idx - start_idx > max_chars:
        end_idx = start_idx + max_chars

    return article_text[start_idx:end_idx], start_idx, end_idx


TABLE_EXTRACTION_SYSTEM_PROMPT = """
You are a meticulous biomedical table-reconstruction specialist. You will be given a block of
raw text that was mechanically extracted from a table in a scientific paper (an HTML or PDF
table flattened into plain text). Because of this flattening, numbers, labels, and column
headers are often out of their original visual order, split across lines, or interleaved with
fragments of neighboring columns.

Your task is to reconstruct the ORIGINAL table structure (column headers, row labels, and which
value belongs in which row x column cell) as faithfully as possible, using layout clues, numeric
consistency checks (subgroup counts should sum close to the stated total; percentages within a
category should sum to roughly 100%), and column-order clues (the raw text typically lists all
header fragments first, then proceeds row by row through the data, repeating the same column
order for every row).

Never invent a value that is not present in the raw text. If you cannot confidently determine
which column or row a value belongs to, set column_label (or row_label) to "[ambiguous]" instead
of guessing.

Return valid JSON only.
"""

TABLE_EXTRACTION_USER_PROMPT = """
Reconstruct the table below as structured JSON.

STEPS:
1. Identify the table title/caption (the text immediately after "Table N.").
2. Identify the column headers, in left-to-right order (e.g., "Total (n=370,298)",
   "Nonallergic infants (n=363,387)", "Allergic infants (n=6,911)", "p value", "SMD",
   "Relative risk"). Column header fragments (e.g., the "(n=...)" part and the label part)
   may appear on separate lines and out of order in the raw text -- merge them into one
   coherent column label string.
3. Identify each row label (e.g., "Sex (female), n (%)", "Jewish", "Arab"). Some rows are
   grouped under a row-group header (e.g., "Ethnicity, n (%)" groups "Jewish", "Arab",
   "Unknown"); record that group header in row_group for each of its rows. Use null for
   row_group when a row is not part of a subgroup.
4. For each row, assign each value to its correct column using this order: the raw text
   generally lists all values for one row across all columns, in the same left-to-right
   column order as the header, before moving to the next row. Use sanity checks: subgroup
   counts should sum close to the row-group's total; the "Total" column value should
   roughly equal the sum of the other population columns (e.g. "Nonallergic" + "Allergic").
5. Do NOT extract footnote text, legend definitions (e.g., "SMD, standardized mean
   difference"), or narrative text that is not part of the table grid itself.
6. Stop at the end of this table; do not include content from a different table.

OUTPUT JSON SCHEMA:
{
  "table_title": "<table caption, verbatim or closely paraphrased>",
  "columns": ["<column 1 label>", "<column 2 label>", ...],
  "cells": [
    {
      "row_label": "<row label text>",
      "row_group": "<group header string, or null>",
      "column_label": "<must be one of the strings in 'columns', or '[ambiguous]'>",
      "value": "<verbatim cell text, e.g. '3,003 (43.5)'>"
    }
  ]
}

RAW TABLE TEXT:
__TABLE_TEXT__
"""


def extract_table(
    article_text: str,
    table_number: int = 1,
    chat_fn=run_gpt_chat,
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
    paper_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Extract a single table from article text into a tidy cell-record structure.

    Returns a dict with:
        paper_id, table_number, found (bool),
        table_title, columns, cells (list of {row_label, row_group, column_label, value}),
        raw_table_text (the source span fed to the model, kept for provenance/debugging).
    """
    located = find_table_section(article_text, table_number=table_number)
    if located is None:
        return {
            "paper_id": paper_id,
            "table_number": table_number,
            "found": False,
            "table_title": None,
            "columns": [],
            "cells": [],
            "raw_table_text": "",
        }

    section_text, start_idx, end_idx = located

    raw_output = chat_fn(
        messages=[
            {"role": "system", "content": TABLE_EXTRACTION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": TABLE_EXTRACTION_USER_PROMPT.replace("__TABLE_TEXT__", section_text),
            },
        ],
        max_new_tokens=max_new_tokens,
    ) or "{}"

    parsed = _parse_table_json(raw_output)
    if isinstance(parsed, list):
        # Model returned a bare cells array instead of the wrapping object.
        parsed = {"cells": parsed}
    if not isinstance(parsed, dict):
        parsed = {}

    cells = parsed.get("cells", [])
    for cell in cells:
        if isinstance(cell, dict):
            cell.pop("confidence", None)

    return {
        "paper_id": paper_id,
        "table_number": table_number,
        "found": True,
        "table_title": parsed.get("table_title"),
        "columns": parsed.get("columns", []),
        "cells": cells,
        "raw_table_text": section_text,
    }


if __name__ == "__main__":
    sample_text = """
Table 1. Comparison of demographic and general parameters between the groups
Variable
Sex (female), n (%)
Total (n = 370,298)
180,469 (48.7)
Nonallergic infants (n = 363,387)
177,466 (48.8)
Allergic infants (n = 6,911)
3,003 (43.5)
p value
<0.001
SMD
0.108

Table 2. Variables correlated with the development of FA
"""
    result = extract_table(sample_text, table_number=1)
    print(json.dumps(result, indent=2))
