import json
import os
import re
import sys
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from local_granite_client import run_granite_chat


VALIDATION_SYSTEM_PROMPT = """
You are a careful biomedical evidence validation assistant.
Your job is to check whether each extracted statement is actually supported by its evidence_span.
Do not invent missing details. Do not assume anything beyond the given evidence_span.
Return valid JSON only.
"""


VALIDATION_USER_PROMPT = """
For each extracted statement below, check whether the evidence_span actually supports the
statement_text and expected_value_or_relationship.

Classify each item with a "verdict" of one of:
- supported
- partially supported
- unsupported
- too vague

For each item, return a JSON object with these fields:
- statement_text
- verdict
- confidence
- explanation
- corrected_wording (revised wording if the original statement should be corrected, otherwise same as statement_text)
- evidence_span (the exact evidence_span used to justify the verdict)

Rules:
1. Base the verdict only on the given evidence_span, not on outside knowledge.
2. If the statement is unsupported, explain why and do not invent missing details.
3. Output must be a valid JSON array, one object per input statement, like:
[
  {
    "statement_text": "...",
    "verdict": "supported",
    "confidence": 0.9,
    "explanation": "...",
    "corrected_wording": "...",
    "evidence_span": "..."
  }
]

EXTRACTED STATEMENTS (JSON):
__STATEMENTS_JSON__
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

    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse model output as JSON: {raw_text[:500]}")


def validate_clinical_statements(
    statements: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Send extracted statements to the local Granite model and validate each against its evidence_span."""
    if not statements:
        return []

    raw_output = run_granite_chat(
        messages=[
            {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": VALIDATION_USER_PROMPT.replace(
                    "__STATEMENTS_JSON__", json.dumps(statements, indent=2)[:20000]
                ),
            },
        ],
    ) or "[]"
    parsed = _clean_json_payload(raw_output)

    if isinstance(parsed, dict):
        return parsed.get("validations", [])
    if isinstance(parsed, list):
        return parsed
    return []


if __name__ == "__main__":
    sample_statements = [
        {
            "statement_text": "Systolic blood pressure was reduced by 12 mmHg after 6 months of treatment with an ACE inhibitor.",
            "expected_value_or_relationship": "reduction of 12 mmHg",
            "evidence_span": "Systolic blood pressure was reduced by 12 mmHg after 6 months of treatment with an ACE inhibitor.",
        }
    ]
    result = validate_clinical_statements(sample_statements)
    print(json.dumps(result, indent=2))
