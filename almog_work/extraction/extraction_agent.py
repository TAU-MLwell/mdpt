import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

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

    raise ValueError(f"Could not parse model output as JSON: {raw_text[:500]}")


def extract_clinical_statements(
    article_text: str,
) -> List[Dict[str, Any]]:
    """Send article text to the local Granite model and extract evidence-backed clinical statements."""
    raw_output = run_granite_chat(
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": EXTRACTION_USER_PROMPT.replace("__ARTICLE_TEXT__", article_text[:20000]),
            },
        ],
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
