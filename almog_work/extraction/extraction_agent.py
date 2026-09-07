import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

from json_repair import repair_json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from local_granite_client import run_granite_chat


EXTRACTION_SYSTEM_PROMPT = """
You are a careful biomedical evidence extraction assistant.
Your job is to extract only statements that are explicitly supported by the article text.
Do not infer beyond the text. Do not generalize. Do not merge unrelated claims.
If a statement is not directly supported, do not include it.
Return valid JSON only.
"""


EXTRACTION_USER_PROMPT = """
Extract clinically relevant statements from the following biomedical article.

For each extracted statement, return a JSON object with these fields:
- statement_text
- statement_type
- variables
- conditions
- expected_value_or_relationship
- context
- evidence_span
- source_paper
- confidence

Rules:
1. Only include statements directly supported by the article text.
2. If a statement is multi-variable, keep one primary relationship and list all variables with name, role, value, and condition when available.
3. Use an exact or near-exact evidence span taken from the article.
4. If a paper has no usable statements, return an empty list.
5. Output must be valid JSON like:
[
  {
    "statement_text": "...",
    "statement_type": "quantitative",
    "variables": [
      {"name": "BMI", "role": "exposure", "value": "25", "condition": "adults"}
    ],
    "conditions": ["adults", "follow-up 12 months"],
    "expected_value_or_relationship": "BMI was associated with higher risk",
    "context": "Results section",
    "evidence_span": "...exact text from article...",
    "source_paper": {"pmid": "", "title": "", "journal": "", "year": ""},
    "confidence": 0.9
  }
]

ARTICLE:
__ARTICLE_TEXT__
"""


def _clean_json_payload(raw_text: str) -> Any:
    text = raw_text.strip()
    if not text:
        return []

    if "```" in text:
        match = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.S | re.I)
        if match:
            text = match[0].strip()

    for candidate in [text, text[text.find("["): text.rfind("]") + 1]]:
        if candidate.strip().startswith("["):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

    # fallback: attempt to extract the first list-like object
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    # fallback: model output was truncated or slightly malformed. Try to repair it
    # (e.g. close an unfinished list/object) before giving up.
    repair_candidate = text[start:] if start != -1 else text
    try:
        repaired = repair_json(repair_candidate)
        parsed = json.loads(repaired)
        if isinstance(parsed, (list, dict)):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass

    raise ValueError(f"Could not parse model output as JSON: {raw_text[:500]}")


def extract_clinical_statements(
    article_text: str,
    chat_fn=run_granite_chat,
    max_new_tokens: int = 4000,
) -> List[Dict[str, Any]]:
    """Send article text to a chat model and extract evidence-backed clinical statements.

    chat_fn defaults to the local Granite model, but any callable with the signature
    chat_fn(messages, max_new_tokens=...) -> str can be passed instead (e.g. run_gpt_chat).
    max_new_tokens defaults higher than the chat_fn's own default since a full paper can
    contain many statements, and each one takes ~150-200 tokens of verbose JSON output.
    """
    raw_output = chat_fn(
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": EXTRACTION_USER_PROMPT.replace("__ARTICLE_TEXT__", article_text[:100000]),
            },
        ],
        max_new_tokens=max_new_tokens,
    ) or "[]"
    parsed = _clean_json_payload(raw_output)

    if isinstance(parsed, dict):
        return parsed.get("statements", [])
    if isinstance(parsed, list):
        return parsed
    return []


if __name__ == "__main__":
    sample_text = """
    In this cohort of 1,245 adults with hypertension, systolic blood pressure was reduced by 12 mmHg after 6 months of treatment.
    The reduction was greater in patients with baseline systolic blood pressure >150 mmHg.
    """
    result = extract_clinical_statements(sample_text)
    print(json.dumps(result, indent=2))
