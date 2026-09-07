# Project status

# Literature-Derived Clinical Rule Base for MDPT Status

## Current Status

**Project phase:** End-to-end tool POC complete; running the local-model-vs-GPT comparison.

**Overall health:** 🟢 On track

**Last update:** 2026-09-05

**Since last update:**

- Extraction and validation agent POCs completed.
- The complete end-to-end tool POC (ingestion → extraction → validation, rerunnable) is complete.
- Started the local IBM Granite model vs. GPT comparison on real PMC papers; a first batch run was interrupted partway through.
- Enabled GPU acceleration for the local Granite model (was CPU-only, several minutes per paper; now seconds per paper).
- Added `json_repair` as a fallback when the LLM's JSON output is truncated or malformed, to make extraction/validation less brittle.
- Rule database work is in progress.

**Current blocker:** Rule database is still in progress. The local-vs-GPT comparison needs to be rerun to completion now that GPU speed and JSON parsing are fixed.

**Next two weeks:**

- Finish the rule database.
- Rerun and complete the local-model-vs-GPT comparison on 10–15 papers.
- Refine prompts/agents based on comparison results and select a model/prompt version.
- Run the small-paper evaluation (5 papers) using one of Irina's datasets to look for anomalies.

## Milestones

| Milestone | Description | Owner | Target Date | Updated Target Date | Complete Date | Status |
|:---|:---|:---|:---|:---|:---|:---|
| Project kickoff | Define the project direction, initial POC, and connection to MDPT. | Almog Alfamon | 2026-07-20 |  | 2026-07-20 | 🟢 Complete |
| PubMed ingestion POC complete | Retrieve PubMed records for a selected date, save metadata, and optionally retrieve PMC full text. | Almog Alfamon | 2026-07-20 |  | 2026-07-20 | 🟢 Complete |
| Extraction agent POC complete | A working LLM-based extraction agent. | Almog Alfamon | 2026-08-09 |  | 2026-08-09 | 🟢 Complete |
| Validation agent POC complete | A working LLM-based validation agent. | Almog Alfamon | 2026-08-16 |  | 2026-08-16 | 🟢 Complete |
| Rule database | Store papers, candidate statements, validation results, evidence, and accepted statements. | Almog Alfamon | 2026-08-16 |  |  | 🟡 In progress |
| Complete tool POC | Connect ingestion, extraction, and validation into a rerunnable end-to-end tool. | Almog Alfamon | 2026-09-05 |  | 2026-09-05 | 🟢 Complete |
| Local IBM model vs. GPT comparison | Run 10–15 papers through both the local Granite model and GPT with the same prompts, and compare statements, evidence, verdicts, and processing time. | Almog Alfamon | 2026-09-10 |  |  | 🟡 In progress |
| Refine prompts and agents | Fix errors/disagreements found in the comparison and settle on a model and prompt version. | Almog Alfamon | 2026-09-17 |  |  | ⚪ Not started |
| Small-paper evaluation | Run the pipeline on 5 papers using one of Irina's datasets and classify anomalies. | Almog Alfamon | 2026-09-17 |  |  | ⚪ Not started |
| Connect tool to full MDPT pipeline | Connect validated statements to MDPT and confirm MDPT can run tests from them. | Almog Alfamon | 2026-09-24 |  |  | ⚪ Not started |
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