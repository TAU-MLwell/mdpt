import json
import os
import re
import sys
from typing import Any, Dict, List

from json_repair import repair_json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from openai_client import run_gpt_chat


VALIDATION_SYSTEM_PROMPT = """
You are a careful biomedical evidence validation assistant.
Your job is to check whether each extracted statement is actually supported by its evidence_span,
AND whether the statistic was matched to the CORRECT population (not misattributed to the wrong
cohort/subset, e.g. a statistic about a smaller subset incorrectly labeled as being about the full
study cohort, or vice versa).
Do not invent missing details. Do not assume anything beyond the given evidence_span.
Return valid JSON only.
"""


VALIDATION_USER_PROMPT = """
For each extracted population-statistic statement below, validate THREE things:
1. Does population_source_span actually describe the population_description (population is accurately worded)?
2. Does statistical_source_span actually support the statistical_finding (statistic is accurately worded)?
3. POPULATION MATCH: Does the statistic in statistical_source_span actually apply to the population
   named in population_description — or was it misattributed? Watch for cases where a statistic
   belongs to a smaller/different subset (e.g., "among the 4,356 with blood type data available") but
   was incorrectly labeled with the main cohort's population_description, or vice versa.

Classify each item with a "verdict" of one of:
- supported (population wording, statistic wording, AND population match are all correct)
- partially_supported (population or statistic is unclear/incomplete, or there's a minor discrepancy)
- unsupported (either population or statistic is contradicted, not found in source spans, or the
  statistic is misattributed to the wrong population)
- too_vague (the statement lacks sufficient specificity to validate)

For each item, return a JSON object with these fields:
- population_description
- statistical_finding
- verdict
- confidence (0.0-1.0)
- explanation
- population_ok (boolean: is population_description supported by population_source_span?)
- statistic_ok (boolean: is statistical_finding supported by statistical_source_span?)
- population_match_ok (boolean: does the statistic actually apply to the stated population, i.e. is
  it NOT misattributed to a different cohort/subset?)

Rules:
1. Base the verdict ONLY on the given source spans, not on outside knowledge.
2. Check the population_source_span, the statistical_source_span, AND whether they truly refer to the
   same population (same inclusion criteria / sample size), not just whether each span is individually
   well-formed.
3. If all three checks pass clearly, verdict = "supported" and confidence should be high (0.9-1.0).
4. If one part is unclear or partially stated, verdict = "partially_supported" (0.6-0.8).
5. If a source span doesn't actually contain what the extracted statement claims, OR the statistic is
   attributed to the wrong population (population_match_ok = false), verdict = "unsupported" (0.1-0.3).

Output format:
[
  {
    "population_description": "n=370,298 children...",
    "statistical_finding": "Jewish vs Arab: RR 3.83...",
    "verdict": "supported",
    "confidence": 0.97,
    "explanation": "Both population and RR are clearly stated in results, and the RR applies to the full cohort as stated.",
    "population_ok": true,
    "statistic_ok": true,
    "population_match_ok": true
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


def validate_clinical_statements(
    statements: List[Dict[str, Any]],
    chat_fn=run_gpt_chat,
    max_new_tokens: int = 4000,
) -> List[Dict[str, Any]]:
    """Send extracted statements to a chat model and validate each against its evidence_span.

    chat_fn defaults to Azure OpenAI GPT-4o. Any callable with the signature
    chat_fn(messages, max_new_tokens=...) -> str can be passed instead.
    max_new_tokens defaults higher than the chat_fn's own default since each validated
    statement's verdict/explanation/corrected_wording is verbose JSON output.
    """
    if not statements:
        return []

    raw_output = chat_fn(
        messages=[
            {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": VALIDATION_USER_PROMPT.replace(
                    "__STATEMENTS_JSON__", json.dumps(statements, indent=2)[:500000]
                ),
            },
        ],
        max_new_tokens=max_new_tokens,
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
