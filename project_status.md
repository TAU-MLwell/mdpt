# Project status

# Literature-Derived Clinical Rule Base for MDPT Status

## Current Status

**Project phase:** End-to-end tool POC complete; running the local-model-vs-GPT comparison.

**Overall health:** 🟢 On track

**Last update:** 2026-09-17

**Since last update:**

- Fixed 3 real pipeline bugs discovered via testing: (1) article text truncated at 20k chars before reaching model (100k fix); (2) extraction/validation output capped at 1500 tokens (4000→8000 token budget fix); (3) PMC fetch defaulting to 30k char limit (500k fix).
- Updated extraction prompt to maximize statement coverage (extract all facts from abstract/methods/results/tables/discussion, not just obvious ones).
- Ran comparison tests on 1 paper with fixed pipeline: GPT now extracts 27 statements (vs. 14 before fixes), validated to 14. Granite extracts 17, validates to 16.
- Created side-by-side CSV export tool (`export_sidebyside_csv.py`) for easier manual evaluation of model differences.
- GPU acceleration working (Granite: ~3-8s per paper vs. minutes on CPU).
- Added `json_repair` fallback for truncated/malformed LLM JSON output.
- Rule database: **still untouched, zero code implementation despite being marked in progress**.

**Current blocker:** Full 10-paper comparison batch and prompt refinement need to complete first (2026-09-24); rule database implementation follows after, utilizing finalized extraction/validation agents.

**Next two weeks:**

- By 2026-09-22: Implement rule database (schema, storage, insert/query methods). This is overdue and blocking pipeline connection.
- By 2026-09-22: Complete 10-paper comparison batch; manually review results using side-by-side CSV (run in parallel with DB implementation).
- By 2026-09-24: Refine extraction/validation prompts based on comparison findings; select final model (Granite vs. GPT).
- By 2026-09-24: Run small-paper evaluation on 5 papers from one of Irina's datasets; classify anomalies.

## Milestones

| Milestone | Description | Owner | Target Date | Updated Target Date | Complete Date | Status |
|:---|:---|:---|:---|:---|:---|:---|
| Project kickoff | Define the project direction, initial POC, and connection to MDPT. | Almog Alfamon | 2026-07-20 |  | 2026-07-20 | 🟢 Complete |
| PubMed ingestion POC complete | Retrieve PubMed records for a selected date, save metadata, and optionally retrieve PMC full text. | Almog Alfamon | 2026-07-20 |  | 2026-07-20 | 🟢 Complete |
| Extraction agent POC complete | A working LLM-based extraction agent. | Almog Alfamon | 2026-08-09 |  | 2026-08-09 | 🟢 Complete |
| Validation agent POC complete | A working LLM-based validation agent. | Almog Alfamon | 2026-08-16 |  | 2026-08-16 | 🟢 Complete |
| Rule database | Store papers, candidate statements, validation results, evidence, and accepted statements. | Almog Alfamon | 2026-08-16 | 2026-09-29 |  | ⚪ Not started (scheduled after prompt finalization) |
| Complete tool POC | Connect ingestion, extraction, and validation into a rerunnable end-to-end tool. | Almog Alfamon | 2026-09-05 |  | 2026-09-05 | 🟢 Complete |
| Local IBM model vs. GPT comparison | Run 10–15 papers through both the local Granite model and GPT with the same prompts, and compare statements, evidence, verdicts, and processing time. | Almog Alfamon | 2026-09-10 | 2026-09-22 |  | 🟡 In progress |
| Refine prompts and agents | Fix errors/disagreements found in the comparison and settle on a model and prompt version. | Almog Alfamon | 2026-09-24 |  |  | ⚪ Not started |
| Small-paper evaluation | Run the pipeline on 5 papers using one of Irina's datasets and classify anomalies. | Almog Alfamon | 2026-09-24 |  |  | ⚪ Not started |
| Connect tool to full MDPT pipeline | Connect validated statements to MDPT and confirm MDPT can run tests from them. | Almog Alfamon | 2026-10-01 |  |  | ⚪ Not started |
| Test connected pipeline on real data | Run the connected pipeline on the All of Us dataset and Irena's datasets, recording anomalies per paper/dataset. | Almog Alfamon | 2026-10-01 |  |  | ⚪ Not started |
| Sample and classify data anomalies | Manually review a sample of anomalies and classify each as an extraction error, data-testing error, or real data problem. | Almog Alfamon | 2026-10-09 |  |  | ⚪ Not started |
| First thesis draft | Write methods, model comparison, prompt/agent iterations, MDPT integration, real-data evaluation, and limitations. | Almog Alfamon | 2026-10-22 |  |  | ⚪ Not started |
| Draft submitted to Rani for review | Submit the draft and revise per feedback. | Almog Alfamon | 2026-10-30 |  |  | ⚪ Not started |
| Final thesis | Complete the final MSc thesis. | Almog Alfamon | 2026-11-30 |  |  | ⚪ Not started |

## Blockers and Dependencies

| Item | Type | Impact on Project | Owner | Target Resolution Date | Status |
|:---|:---|:---|:---|:---|:---|


## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation | Owner | Trigger Date | Escalation Threshold |
|:---|:---|:---|:---|:---|:---|:---|


## Decisions to Be Made

| Decision Needed | Why It Matters | Decision Owner | Target Decision Date | Current Options |
|:---|:---|:---|:---|:---|
<details>
<summary><strong>How to Fill This Status Update</strong></summary>

Use this document for recurring project updates. Keep entries short, current, and action-oriented. Replace bracketed placeholders, delete example text that does not apply, and keep dates in `YYYY-MM-DD` format.

For status marking in GitHub Markdown, use emoji markers instead of text color:

- `🟢` Good state: on track, no action needed, or complete.
- `🟡` Watch state: some risk or drift, but still recoverable without escalation.
- `🔴` Bad state: blocked, off track, or needs immediate intervention.

Recommended usage:

- `Overall health:` `🟢 On track`, `🟡 At risk`, or `🔴 Off track`
- Milestone `Status` column: `🟢 Complete`, `🟡 In progress`, `🟡 Needs decision`, `🔴 Blocked`, `⚪ Not started`
- Blockers and dependencies `Status` column: `🟢 Closed`, `🟡 Watching`, `🔴 Open`
- Risks and mitigations: put the emoji at the start of the `Risk` text or `Mitigation` text when you need a quick visual signal.

Example: `🟡 Waiting on dataset approval; analysis plan is ready once access is granted.`

</details>