# Stage 3 Prompt Draft

This file is the editable draft for the LLM prompt used in stage 3.

## Goal

Extract structured clinical statements from article text, validate that they are supported by the source, and format them for database storage.

## Extraction Prompt

You are given a biomedical article. Extract clinically relevant statements that are explicitly supported by the text.

A clinical statement is a factual, quantitative, or relational claim about a disease, population, variable, outcome, threshold, association, intervention, measurement, or context.

Extract only statements that are grounded in the article text. Do not infer beyond the text. Do not generalize. Do not merge unrelated claims.

For each statement, identify:
- statement_text: a concise paraphrase or exact quote
- statement_type: quantitative, qualitative, association, comparison, threshold, outcome, definition, methodology, or other
- variables: the clinical variables involved
- conditions: any inclusion criteria, subgroup, setting, timeframe, or other context
- expected_value_or_relationship: the number, range, direction, comparison, or relation stated in the paper
- context: where the statement appears and what it refers to
- evidence_span: the exact supporting text span from the article
- source_paper: PMID, title, journal, year
- confidence: your confidence that the statement is directly supported by the text

If the paper contains a multi-variable statement, represent it as one primary relationship plus a list of variables, each with:
- name
- role
- value if available
- condition if relevant

Only return statements that are supported by explicit evidence in the article.

## Validation Prompt

For each extracted statement, check whether the evidence_span actually supports the statement_text and expected_value_or_relationship.

Classify each item as one of:
- supported
- partially supported
- unsupported
- too vague

For each item, provide:
- verdict
- confidence
- short explanation
- corrected wording if the original statement should be revised
- the exact evidence_span used to justify the verdict

If the statement is unsupported, explain why and do not invent missing details.

## Formatting Prompt

Return the final output in a clean structured format suitable for database storage.

Use one record per statement, with fields:
- source_paper
- statement_text
- statement_type
- variables
- conditions
- expected_value_or_relationship
- context
- evidence_span
- confidence
- validation_verdict
- validation_explanation
- corrected_wording

If a paper has no usable statements, return an empty list.

## Style Rules

- Do not hallucinate missing details.
- Prefer explicit evidence over interpretation.
- Keep statements short and precise.
- Preserve numerical values exactly as written when possible.
- If a statement contains multiple variables, keep the relationship clear and unambiguous.

## Notes

This prompt is meant to be edited and refined as the schema improves and more examples are added.