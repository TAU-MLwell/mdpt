import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from openai_client import run_gpt_chat


# Articles longer than CHUNK_SIZE chars are split into overlapping chunks to avoid
# silent truncation; CHUNK_OVERLAP chars are repeated between chunks to preserve context.
CHUNK_SIZE = 80000
CHUNK_OVERLAP = 2000
DEFAULT_MAX_NEW_TOKENS = 4000


# Basic JSON repair fallback (if json_repair library is not available)
def _repair_json_fallback(text: str) -> str:
    """Minimal JSON repair: close unclosed lists/objects."""
    text = text.strip()
    if text.startswith("["):
        if not text.endswith("]"):
            text += "]"
    elif text.startswith("{"):
        if not text.endswith("}"):
            text += "}"
    return text


EXTRACTION_SYSTEM_PROMPT = """
You are a biomedical data extraction specialist. Your job is to extract DESCRIPTIVE STATISTICS
from biomedical articles, preserving exactly what the paper reports. Do not infer, synthesize,
or convert aggregate statistics to individual thresholds. Record one statistic per JSON record,
clearly identifying the population, variable, value, and source.

DESCRIPTIVE STATISTICS (focus of extraction):
- Means, standard deviations, medians, ranges
- Counts, frequencies, percentages, proportions, prevalence, incidence
- Stratified results (e.g., by age, sex, subgroup, timepoint)
- Sample sizes, denominators

DO NOT EXTRACT:
- Method explanations or guidance (e.g., "SMD ≥0.2 considered clinically significant" in Methods/footnotes)
- Statistical test thresholds or cutoffs used for analysis
- Interpretive scales or categorization schemes (unless they are themselves the study findings)
- Model parameters or hyperparameters
- General educational content that is not a study finding

POPULATIONS VS SUBGROUPS VS CATEGORIES:
- A POPULATION is a distinct group with explicit inclusion criteria or separate sample size (e.g., 
  "n=370,298 children born in CHS hospitals" or "allergic group, n=6,911").
- A SUBGROUP or CATEGORY is a stratification WITHIN a single population (e.g., "among the 370,298 children,
  6,911 were allergic and 363,387 were nonallergic"). Subgroups share the same underlying population definition.
- A TIMEPOINT is a measurement of the same population at different times (e.g., "baseline" and "6-month" 
  for the same 200 patients).
- Do NOT create separate populations for demographic categories unless the paper explicitly states they 
  have different inclusion criteria (e.g., "we enrolled 50 Jewish children and 50 Arab children separately").

SCOPE: Extract descriptive statistics only. Inferential statistics (RR, OR, p-value, CI) are secondary
when they express a comparison between subgroups; extract only if the paper explicitly reports them
(do not infer or calculate them). Preserve which groups or populations they compare.

CORE PRINCIPLES:
1. Record only what the paper explicitly reports. Do not guess missing data, convert aggregate statistics
   to individual thresholds, or infer population definitions.
2. Keep statistics from truly different populations (different inclusion/exclusion criteria) separate.
3. Use the paper's own language to identify populations. If a population is defined in Methods but a
   statistic appears in Results, preserve that link.
4. Preserve aggregate vs individual: "mean BMI 25.3 kg/m²" (aggregate mean across a group) ≠ "BMI > 30"
   (a threshold or criterion). Do not convert one to the other.
5. Use explicit markers for missing/ambiguous info:
   - "[ambiguous context]" = population or table context unclear despite review
   - "[not reported]" = expected data (denominator, CI) is missing from the paper
   - "[partial content]" = input text truncated and this statistic's context is incomplete
   - Do not guess; mark ambiguous instead.

OUTPUT RULES:
- One record per distinct reported statistic and group/subgroup/timepoint.
- Stratified result: If the paper reports a statistic stratified by subgroups within one population
  (e.g., "Female: 48.8%, Male: 56.5%"), create ONE record per subgroup with its own value, but both
  records share the same population_description. Alternatively, include both values in one record's
  statistical_finding if that better preserves the paper's presentation.
- Different populations: Use separate records with different population_descriptions.
- Do not combine statistics from different populations into one record.

Return valid JSON only. Ensure all text is valid UTF-8.
"""


EXTRACTION_USER_PROMPT = """
Extract ALL RELEVANT DESCRIPTIVE STATISTICS from this biomedical article and correctly match EACH
ONE to the exact population it was actually reported for. Include statistics from text, tables,
captions, and footnotes. Do not extract method guidance or interpretation thresholds. Do not assume
the whole paper describes one population — scan for ALL distinct populations defined (full cohort,
named subsets with separate inclusion criteria, separate arms, separate studies).

POPULATIONS VS SUBGROUPS:
The article may describe:
- ONE overall population (e.g., "1,359,480 children born during 2006-2021")
- Multiple SUBGROUPS or CATEGORIES within that population (e.g., "6,911 allergic, 363,387 nonallergic")
- Smaller SUBSETS due to data availability (e.g., "4,356 infants with blood type data")
- TIMEPOINTS of the same population (e.g., "baseline and 6-month follow-up")

Only use separate population_descriptions if the paper explicitly defines distinct populations with
different inclusion criteria. Use the SAME population_description for subgroups and timepoints of the
same underlying population.

WHAT NOT TO EXTRACT:
- Method explanations: "SMD ≥0.2 considered clinically significant" (this is how the authors analyze,
  not a study finding)
- Table footnotes explaining methodology: "Variables correlated with FA; SMD ≥0.5 medium, ≥0.8 large"
- Statistical test descriptions or cutoff guidance
- Model parameters or feature importance thresholds
- General claims about the field not directly reported as a finding

MATCHING POPULATIONS TO STATISTICS:
1. Scan the article for explicit population definitions (Methods, Results, table headers/captions).
2. Record the EXACT language the paper uses (e.g., "370,298 children born in CHS hospitals").
3. When you find a statistic, determine which population it applies to:
   - Is it labeled in the table header or row labels? (e.g., "Total (n=370,298)" or "Allergic infants (n=6,911)")
   - Does the text near the statistic name its population?
   - If not nearby, find the population definition elsewhere in the paper and cite it.
4. Use the SAME population_description string for all statistics that share identical criteria/sample size.
5. For subgroups/categories: Use ONE population_description for the entire cohort, but preserve subgroup
   labels in the statistical_finding or context.
6. For variable-specific subsets (e.g., "n=4,356 with blood type data"): If the paper defines this as
   a separate analysis population, use a distinct population_description.

HANDLING TABLES:
1. Identify column headers and what they represent:
   - POPULATIONS: "Total (n=370,298) | Allergic (n=6,911) | Nonallergic (n=363,387)" → use separate
     population_description for each
   - SUBGROUPS/CATEGORIES: "Overall | Jewish | Arab | Unknown" (all from same total population) →
     use ONE population_description; preserve subgroup in statistical_finding
   - TIMEPOINTS: "Baseline | 6-month | 12-month" (same patients) → ONE population_description;
     preserve timepoint in statistical_finding
   - TREATMENT ARMS: "Control (n=100) | Treatment (n=100)" → separate population_descriptions
2. Extract one record per row-column cell (or row-subgroup if columns are subgroups of one population).
3. Match values to headers by column position—never guess or interpolate.
4. Include precise table/column/row location in context (e.g., "Table 1, row 'Maternal age', 
   column 'Total (n=370,298)'").
5. If table structure is ambiguous, mark context as "[ambiguous context]".

OUTPUT SCHEMA (7 fields per record):
1. population_description: Plain description of the population this statistic was reported for.
   Examples: "n=370,298 children born in CHS hospitals (2006-2021)" or "subset with blood type data, n=4,356"
   or "allergic group, n=6,911". Keep it brief and factual. Reuse exact string across records for same population.

2. population_source_span: Exact verbatim text from the paper that defines this population.
   This may appear far from the statistic (in Methods while statistic is in Results).

3. statistical_finding: The reported numerical result, preserving the paper's exact wording and values.
   Examples: "Overall prevalence 1.87% (6,911/370,298)" or "Female: 48.8%, Male: 56.5%" or
   "Mean ± SD: 25.3 ± 4.5 kg/m²" or "RR 3.83 (95% CI 3.43–4.28)" or "Birthweight: 3,172.7±534.0 g".
   Preserve numerators, denominators, percentages, p-values, confidence intervals, and units exactly as reported.
   Do NOT extract interpretive text (e.g., "considered clinically significant").

4. statistical_source_span: Exact verbatim text from the paper that contains this statistic.

5. variables: Optional; only include if needed to clarify what was measured. Each entry:
   - name (string): e.g., "sex", "ethnicity", "birthweight", "food allergy"
   - type (string): e.g., "prevalence", "mean", "count", "categorical", or leave empty
   Example: {"name": "maternal age", "type": "mean"} for "Mean ± SD maternal age 30.1 ± 5.52 years".
   Keep simple; do NOT include redundant fields like "value" or "condition".

6. context: Exact location in the paper where this statistic appears.
   Examples: "Results section", "Table 1, row 'Maternal age', column 'Total (n=370,298)'",
   "Results section, second paragraph", "Figure 2 caption".
   Mark "[partial content]" if this section of the article was truncated in the input.

7. confidence: Decimal 0.0–1.0 representing extraction confidence.
   Use 0.95+ only if population_source_span and statistical_source_span are both clear verbatim quotes.
   Use 0.80–0.94 if reasonable inference was needed (e.g., from table headers).
   Use <0.80 if population attribution is ambiguous or required inference; mark population_description
   as "[ambiguous context]".

EXAMPLE: Food Allergy Paper Structure

The paper reports:
- Source population: "1,359,480 children born 2006-2021, insured by CHS"
- Analysis cohort: "370,298 born in CHS hospitals with perinatal data"
- Subgroups: Within the analysis cohort, "6,911 allergic, 363,387 nonallergic"
- Variable-specific subsets: "4,356 infants with blood type data" (a subset of the 370,298)

Correct extraction:
Record 1 (Overall prevalence in analysis cohort):
  population_description: "n=370,298 children born in CHS hospitals (2006-2021)"
  statistical_finding: "Food allergy diagnosed in 6,911 children (1.87%)"

Record 2 (Jewish vs Arab subgroup comparison):
  population_description: "n=370,298 children born in CHS hospitals (2006-2021)"
  statistical_finding: "Jewish infants: 2.13% FA (RR 3.83); Arab: 0.56%"

Record 3 (Blood type data, smaller subset):
  population_description: "n=4,356 infants with blood type data (subset of 370,298 analysis cohort)"
  statistical_finding: "Blood type A: 1,819/4,356 (41.76%)"
  context: "Table 2, Blood type row, Maternal A column; only 4,356 of 370,298 had blood typing"

Record 4 (Allergic subgroup only):
  population_description: "n=6,911 infants with food allergy (subgroup of 370,298)"
  statistical_finding: "Female: 3,003/6,911 (43.5%)"
  context: "Table 1, Sex row, Allergic infants column"

DO NOT extract:
- "SMD ≥0.2 considered clinically significant; ≥0.5 medium; ≥0.8 large" (this is method guidance, not a study result)
- Table footnote: "Variables correlated with development of FA" (heading, not a statistic)

ARTICLE:
__ARTICLE_TEXT__
"""


def _clean_json_payload(raw_text: str) -> tuple[Any, bool]:
    """Parse JSON from model output; return (parsed, was_repaired).
    
    Args:
        raw_text: Raw text from model, may contain markdown code blocks or malformed JSON.
    
    Returns:
        (parsed_data, was_repaired): Tuple where was_repaired=True if repair was needed.
        Returns ([], True) if parsing completely fails.
    """
    text = raw_text.strip()
    if not text:
        return [], False

    # Try extracting from markdown code block
    if "```" in text:
        match = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.S | re.I)
        if match:
            text = match[0].strip()

    # Try parsing as-is
    for candidate in [text, text[text.find("["): text.rfind("]") + 1]]:
        if candidate.strip().startswith("["):
            try:
                return json.loads(candidate), False
            except json.JSONDecodeError:
                pass

    # Try extracting the first list-like object
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1]), False
        except json.JSONDecodeError:
            pass

    # Last resort: basic JSON repair (close unclosed lists/objects)
    # This may produce truncated or incorrect output, so mark it as repaired
    repair_candidate = text[start:] if start != -1 else text
    try:
        repaired = _repair_json_fallback(repair_candidate)
        parsed = json.loads(repaired)
        if isinstance(parsed, (list, dict)):
            return parsed, True
    except (json.JSONDecodeError, ValueError):
        pass

    # Complete failure
    raise ValueError(f"Could not parse model output as JSON. Raw output: {raw_text[:500]}")


def _split_article_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[tuple[str, int, int]]:
    """Split a long article into overlapping chunks to preserve context.
    
    Args:
        text: Full article text.
        chunk_size: Approximate size per chunk in characters.
        overlap: Characters to overlap between chunks (for context preservation).
    
    Returns:
        List of (chunk_text, start_index, end_index) tuples.
    """
    chunks = []
    text_len = len(text)
    
    if text_len <= chunk_size:
        return [(text, 0, text_len)]
    
    pos = 0
    while pos < text_len:
        # Define end of this chunk
        end = min(pos + chunk_size, text_len)
        
        # Try to break at a section boundary (double newline)
        if end < text_len:
            search_start = max(pos, end - 1000)
            break_pos = text.rfind("\n\n", search_start, end)
            if break_pos > pos + chunk_size // 2:  # Only use if not too close to start
                end = break_pos
        
        chunk_text = text[pos:end]
        chunks.append((chunk_text, pos, end))
        
        # Move to next chunk start with overlap
        pos = end - overlap
        if pos >= text_len:
            break
    
    return chunks


def extract_clinical_statements(
    article_text: str,
    chat_fn=run_gpt_chat,
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS,
) -> List[Dict[str, Any]]:
    """Extract descriptive statistics from biomedical article text.

    This function uses Azure OpenAI (GPT-4o) by default. For long articles, it processes
    content in chunks to avoid silent truncation and loss of data.

    Args:
        article_text: Full article text. If longer than ~80k chars, the function will process
            it in overlapping chunks to preserve context.
        chat_fn: Callable with signature chat_fn(messages, max_new_tokens=...) -> str.
            Default: run_gpt_chat (Azure OpenAI GPT-4o).
        max_new_tokens: Maximum output tokens per extraction call (default 4000).

    Returns:
        List of extracted statements (empty list if parsing fails).
        Each statement includes 7 fields: population_description, population_source_span,
        statistical_finding, statistical_source_span, variables, context, confidence.

    Raises:
        ValueError: If article text cannot be parsed or model output is unrecoverable JSON.

    Processing notes:
        - Articles ≤ 80k chars: sent as-is in one call.
        - Articles > 80k chars: split into overlapping chunks (80k chars each, 2k char overlap).
        - Each chunk includes relevant population definitions from earlier sections.
        - Output from each chunk is validated and deduplicated.
        - Incomplete extractions are marked with "[partial content]" in context field.
    """
    # Ensure UTF-8 encoding
    article_text = str(article_text).encode("utf-8", errors="replace").decode("utf-8")
    
    # Determine if chunking is needed
    chunks = _split_article_into_chunks(article_text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    all_statements = []
    chunk_status = {"success": 0, "failed": 0, "repaired": 0}
    
    for chunk_idx, (chunk_text, start_idx, end_idx) in enumerate(chunks):
        is_final_chunk = (chunk_idx == len(chunks) - 1)
        
        # Build user message with chunk context
        if len(chunks) > 1:
            chunk_indicator = f"[CHUNK {chunk_idx + 1}/{len(chunks)}] "
            if not is_final_chunk:
                chunk_indicator += "(more content follows after this section)"
            else:
                chunk_indicator += "(final section)"
            user_text = chunk_indicator + "\n\n" + chunk_text
        else:
            user_text = chunk_text
        
        try:
            raw_output = chat_fn(
                messages=[
                    {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": EXTRACTION_USER_PROMPT.replace("__ARTICLE_TEXT__", user_text),
                    },
                ],
                max_new_tokens=max_new_tokens,
            ) or "[]"
            
            # Parse with tracking of repair
            parsed, was_repaired = _clean_json_payload(raw_output)
            
            if was_repaired:
                chunk_status["repaired"] += 1
            else:
                chunk_status["success"] += 1
            
            # Convert parsed output to list
            if isinstance(parsed, dict):
                statements = parsed.get("statements", [])
            elif isinstance(parsed, list):
                statements = parsed
            else:
                statements = []
            
            # Mark statements from non-final chunks with content indicator if needed
            if not is_final_chunk:
                for stmt in statements:
                    if isinstance(stmt, dict) and "context" in stmt:
                        context = stmt.get("context", "")
                        if "[partial content]" not in str(context):
                            # Don't mark incomplete yet; more chunks coming
                            pass
            
            all_statements.extend(statements)
            
        except (ValueError, json.JSONDecodeError) as e:
            chunk_status["failed"] += 1
            # Log failure but continue with other chunks
            print(f"Warning: Extraction failed for chunk {chunk_idx + 1}/{len(chunks)}: {str(e)[:100]}")
            continue
    
    # Deduplicate statements (by population + statistical_finding)
    seen = set()
    deduplicated = []
    for stmt in all_statements:
        if isinstance(stmt, dict):
            key = (stmt.get("population_description", ""), stmt.get("statistical_finding", ""))
            if key not in seen:
                seen.add(key)
                deduplicated.append(stmt)
    
    # Log processing summary if chunking was used
    if len(chunks) > 1:
        print(f"Extraction complete: {len(chunks)} chunks processed. "
              f"Success: {chunk_status['success']}, Repaired: {chunk_status['repaired']}, "
              f"Failed: {chunk_status['failed']}. Statements: {len(deduplicated)}")
    
    return deduplicated


if __name__ == "__main__":
    sample_text = """
    In this cohort of 1,245 adults with hypertension, systolic blood pressure was reduced by 12 mmHg after 6 months of treatment.
    The reduction was greater in patients with baseline systolic blood pressure >150 mmHg.
    
    Methods: We measured blood pressure at baseline and 6 months using a validated home monitoring device.
    
    Results: Among the 1,245 participants, mean systolic BP decreased from 155±12 mmHg to 140±10 mmHg (p<0.001).
    In the subgroup with baseline >150 mmHg (n=450), the reduction was 18±8 mmHg vs 10±7 mmHg in those with baseline ≤150 mmHg.
    """
    result = extract_clinical_statements(sample_text)
    print(json.dumps(result, indent=2))
