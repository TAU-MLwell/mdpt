# Project status

# Literature-Derived Clinical Rule Base for MDPT Status

## Current Status

**Project phase:** PubMed ingestion POC complete; preparing the clinical-statement format and local LLM integration.

**Overall health:** 🟡 At risk

**Last update:** 2026-08-13

**Since last update:**

- The PubMed day-snapshot POC was completed.
- PubMed metadata can be saved to CSV or SQLite.
- Optional PMC full-text retrieval is available.
- The extraction and validation prompt drafts are available.
- The initial plan is to test a local LLM instead of depending on Azure.

**Current blocker:** A local LLM model and runtime still need to be selected, installed, and connected to the existing agents.

**Next two weeks:**

- Finalize the clinical-statement schema and prompt.
- Build the rule database structure.
- Select and set up a local LLM model.
- Connect the existing agents to the local model.
- Run the first LLM-based extraction and validation test on one paper.

## Milestones

| Milestone | Description | Owner | Target Date | Updated Target Date | Complete Date | Status |
|:---|:---|:---|:---|:---|:---|:---|
| Project kickoff | Define the project direction, initial POC, and connection to MDPT. | Almog Alfamon | 2026-07-20 |  | 2026-07-20 | 🟢 Complete |
| PubMed ingestion POC complete | Retrieve PubMed records for a selected date, save metadata, and optionally retrieve PMC full text. | Almog Alfamon | 2026-07-20 |  | 2026-07-20 | 🟢 Complete |
| Clinical statement format and prompt | Define the LLM output format and prompts for extraction, validation, and database storage. | Almog Alfamon | 2026-08-09 | 2026-08-20 |  | 🟡 In progress |
| Rule database | Store papers, candidate statements, validation results, evidence, and accepted statements. | Almog Alfamon | 2026-08-16 |  |  | ⚪ Not started |
| Local LLM integration | Select and run a local LLM, then connect the existing extraction and validation agents to it. | Almog Alfamon | 2026-08-30 |  |  | 🟡 In progress |
| One-paper POC | Run LLM-based extraction, validation, and database storage on one paper. | Almog Alfamon | 2026-09-20 |  |  | ⚪ Not started |
| Small evaluation and MDPT connection | Test the pipeline on a small paper set and demonstrate how validated statements can connect to MDPT. | Almog Alfamon and Ran Gilad-Bachrach | 2026-10-11 |  |  | ⚪ Not started |
| Final thesis and poster | Complete the thesis, poster, figures, code documentation, and final deliverables. | Almog Alfamon | 2026-10-31 |  |  | ⚪ Not started |

## Blockers and Dependencies

| Item | Type | Impact on Project | Owner | Target Resolution Date | Status |
|:---|:---|:---|:---|:---|:---|
| Local LLM setup | Dependency | Blocks LLM-based extraction and validation tests until a suitable model is running and connected to the agents. | Almog Alfamon | 2026-08-20 | 🔴 Open |

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