"""Table-1-only extraction for the separate experiment.

Boundary detection on flattened text is heuristic, not a completeness guarantee.
Only prompt and source text are sent to the model; scoring is a separate step.
"""
import json
import re
from pathlib import Path


def validate_table_result(result: dict) -> None:
    """Prediction schema checks only; no reference tables or model dependencies.

    Blank cells have no record; a reported zero is a nonempty string.
    Category-level statistics use row_label=null and a nonempty row_group.
    """
    if not isinstance(result, dict):
        raise ValueError("Table result must be an object")
    required = {"paper_id", "table_number", "found", "table_title", "columns",
                "cells", "raw_table_text"}
    if not required <= result.keys():
        raise ValueError("Table result is missing required fields")
    if result["paper_id"] is not None and not isinstance(result["paper_id"], str):
        raise ValueError("paper_id must be a string or null")
    if type(result["table_number"]) is not int or result["table_number"] != 1:
        raise ValueError("This experiment requires table_number=1")
    if type(result["found"]) is not bool:
        raise ValueError("found must be a boolean")
    if not isinstance(result["raw_table_text"], str):
        raise ValueError("raw_table_text must be a string")
    columns, cells = result["columns"], result["cells"]
    if not isinstance(columns, list) or not isinstance(cells, list):
        raise ValueError("columns and cells must be lists")
    if not result["found"]:
        if columns or cells or result["table_title"] is not None:
            raise ValueError("A missing table must have no title, columns or cells")
        return
    if not isinstance(result["table_title"], str) or not result["table_title"].strip():
        raise ValueError("A found table requires a nonempty title")
    if not columns or any(not isinstance(c, str) or not c.strip() for c in columns):
        raise ValueError("A found table requires nonempty string column labels")
    if len(set(" ".join(c.split()) for c in columns)) != len(columns):
        raise ValueError("Duplicate column labels")
    if not cells:
        raise ValueError("A found table requires at least one extracted cell")
    seen = set()
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or set(cell) != {
            "row_label", "row_group", "column_label", "value"
        }:
            raise ValueError(f"Cell {index} must contain exactly the four schema fields")
        row, group, column, value = (cell[k] for k in (
            "row_label", "row_group", "column_label", "value"))
        if row is not None and (not isinstance(row, str) or not row.strip()):
            raise ValueError(f"Cell {index} has invalid row_label")
        if group is not None and (not isinstance(group, str) or not group.strip()):
            raise ValueError(f"Cell {index} has invalid row_group")
        if row is None and group is None:
            raise ValueError(f"Cell {index} requires a row label or group")
        if not isinstance(column, str) or column not in columns:
            raise ValueError(f"Cell {index} references an undeclared column")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Cell {index} value must be a nonempty string; omit blank source cells")
        key = tuple(" ".join(v.split()) if v is not None else None
                    for v in (group, row, column))
        if key in seen:
            raise ValueError(f"Cell {index} duplicates a row/group/column key")
        seen.add(key)


DEFAULT_MAX_NEW_TOKENS = 16000
DEFAULT_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "baseline.json"
MAX_TABLE_SECTION_CHARS = 20000
_SECTION_END_PATTERN = re.compile(
    r"^[ \t]*(Discussion|Conclusions?|References|Acknowledg(e)?ments|Author Contributions)[ \t]*$",
    re.MULTILINE | re.IGNORECASE,
)
_TABLE_END_PATTERN = re.compile(
    r"^[ \t]*(?:Fig(?:ure)?\.?[ \t]+\d+\b|Footnote\b|Note:|Abbreviations:|"
    r"Data (?:are|presented)\b|Values are presented\b)",
    re.MULTILINE | re.IGNORECASE,
)
_ANY_TABLE_HEADING_PATTERN = re.compile(
    r"^[ \t]*Table[ \t]+(\d+)[ \t]*[.:][ \t]*[^\r\n]*",
    re.MULTILINE | re.IGNORECASE,
)


class InvalidModelOutput(ValueError):
    """The model's reply is unusable (bad JSON or schema); a prompt problem, not a fault."""


def _parse_table_json(raw_text: str) -> dict:
    """Accept a complete JSON object, optionally fenced; never repair it."""
    if not isinstance(raw_text, str):
        raise ValueError("Model output must be a JSON string")
    text = raw_text.strip()
    if not text:
        raise ValueError("Model returned empty output")
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.S | re.I)
    if fence:
        text = fence.group(1)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("Model output is invalid or truncated JSON; no prediction was accepted") from None
    if not isinstance(parsed, dict):
        raise ValueError("Model output must be a JSON object")
    return parsed


def find_table_section(article_text: str, table_number=1,
                       max_chars=MAX_TABLE_SECTION_CHARS):
    """Locate a caption and stop at the next table, section or footnote."""
    if table_number != 1:
        raise ValueError("This experiment extracts Table 1 only")
    start = re.search(r"^[ \t]*Table[ \t]+1[ \t]*[.:][ \t]*[^\r\n]*",
                      article_text, flags=re.MULTILINE | re.IGNORECASE)
    if start is None:
        return None
    end = len(article_text)
    for match in _ANY_TABLE_HEADING_PATTERN.finditer(article_text, start.end()):
        if int(match.group(1)) != 1:
            end = match.start()
            break
    for pattern in (_SECTION_END_PATTERN, _TABLE_END_PATTERN):
        match = pattern.search(article_text, start.end())
        if match is not None:
            end = min(end, match.start())
    if end - start.start() > max_chars:
        raise ValueError("Table source exceeds the size limit; refusing to truncate it")
    return article_text[start.start():end], start.start(), end


def validate_prompt_config(config: dict) -> None:
    if not isinstance(config, dict) or any(
        not isinstance(config.get(key), str) or not config[key].strip()
        for key in ("system", "user")
    ):
        raise ValueError("Prompt config requires nonempty system and user strings")
    if config["user"].count("__TABLE_TEXT__") != 1:
        raise ValueError("User prompt must contain exactly one __TABLE_TEXT__ placeholder")
    # Optional editable guidance: the fixed contract lives in `user`, and only
    # `guidance` is meant to change between optimizer iterations.
    if "guidance" in config:
        guidance = config["guidance"]
        if not isinstance(guidance, str) or not guidance.strip():
            raise ValueError("guidance must be a nonempty string")
        if config["user"].count("__GUIDANCE__") != 1:
            raise ValueError("User prompt must contain exactly one __GUIDANCE__ placeholder")
        if "__GUIDANCE__" in guidance or "__TABLE_TEXT__" in guidance:
            raise ValueError("guidance must not contain placeholders")
    elif "__GUIDANCE__" in config["user"]:
        raise ValueError("User prompt has a __GUIDANCE__ placeholder but no guidance")


def render_user_prompt(config: dict, table_text: str) -> str:
    user = config["user"]
    if "guidance" in config:
        user = user.replace("__GUIDANCE__", config["guidance"])
    return user.replace("__TABLE_TEXT__", table_text)


def _drop_repeated_keys(cells: list) -> tuple:
    """Keep the first cell for each (row_group, row_label, column_label); count the rest."""
    seen, kept, dropped = set(), [], 0
    for cell in cells:
        parts = [cell.get(k) for k in ("row_group", "row_label", "column_label")] \
            if isinstance(cell, dict) else None
        if parts is None or any(p is not None and not isinstance(p, str) for p in parts):
            kept.append(cell)  # malformed cells are left for strict validation
            continue
        key = tuple(" ".join(p.split()) if p is not None else None for p in parts)
        if key in seen:
            dropped += 1
            continue
        seen.add(key)
        kept.append(cell)
    return kept, dropped


def extract_table_one(article_text: str, *, paper_id=None, chat_fn=None,
                      prompt_config=None, max_new_tokens=DEFAULT_MAX_NEW_TOKENS,
                      stats=None) -> dict:
    """Extract without scoring or gold access; injected chat needs no model SDK.

    If `stats` is a dict, it receives `duplicates_dropped` (a count, never content).
    """
    if type(max_new_tokens) is not int or max_new_tokens <= 0:
        raise ValueError("max_new_tokens must be a positive integer")
    if prompt_config is None:
        prompt_config = json.loads(DEFAULT_PROMPT_PATH.read_text(encoding="utf-8"))
    validate_prompt_config(prompt_config)
    result = {"paper_id": paper_id, "table_number": 1, "found": False,
              "table_title": None, "columns": [], "cells": [], "raw_table_text": ""}
    located = find_table_section(article_text)
    if located is None:
        validate_table_result(result)
        return result
    section_text, _, _ = located
    if chat_fn is None:
        from almog_work.common.openai_client import run_gpt_chat
        chat_fn = run_gpt_chat
    raw_output = chat_fn(
        messages=[{"role": "system", "content": prompt_config["system"]},
                  {"role": "user", "content": render_user_prompt(prompt_config, section_text)}],
        max_new_tokens=max_new_tokens,
    )
    try:
        parsed = _parse_table_json(raw_output)
        cells = parsed.get("cells", [])
        if isinstance(cells, list):
            # A blank source cell has no record, so an echoed blank is dropped, not an error.
            cells = [c for c in cells if not (
                isinstance(c, dict) and (c.get("value") is None or (
                    isinstance(c.get("value"), str) and not c["value"].strip())))]
            # A repeated row/group/column key is a model slip; keep the first, count the rest.
            cells, duplicates = _drop_repeated_keys(cells)
            if stats is not None:
                stats["duplicates_dropped"] = duplicates
        result.update(found=True, table_title=parsed.get("table_title"),
                      columns=parsed.get("columns", []), cells=cells,
                      raw_table_text=section_text)
        validate_table_result(result)
    except ValueError as error:
        raise InvalidModelOutput(str(error)) from None
    return result