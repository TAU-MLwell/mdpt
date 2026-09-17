# Project Description

## Project Summary

**Project name:** Literature-Derived Clinical Rule Base for MDPT

**Project owner:** Almog Alfamon

**Advisor:** Ran Gilad-Bachrach

**Start date:** Not recorded

**Target completion date:** 2026-11-30

## Research Description

**What are we trying to do?**

This project extends the existing MDPT pipeline by building its upstream knowledge layer. The planned system will collect medical papers from PubMed, use an LLM-based extraction agent to generate candidate clinical rules, use a separate validation agent to check those rules against the source paper, and store the supported rules with provenance.

The validated rule base will later be connected to the existing MDPT pipeline, where literature-derived rules can support semantic checks of structured medical data.

**What are the limits of current practice?**

LLMs can extract clinical information from medical papers, but they may produce unsupported claims, miss context, or over-generalize the source.

**What is new in our approach?**

The system separates:

- PubMed paper collection
- LLM-based clinical-rule extraction
- LLM-based source-grounded validation
- provenance-linked storage

The aim is to design and evaluate a reusable rule base that can later be used by MDPT, rather than generating knowledge only for one predefined user question. Rule extraction and validation are performed by LLM-based agents; the thesis focuses on designing, integrating, and evaluating this pipeline.

**If we are successful, what difference will it make?**

The result will be a reusable, updateable source of validated clinical rules that can be connected to MDPT and used for semantic auditing of structured medical data.

**Scope:**

The main scope is the first stage: building and evaluating the clinical rule base. Patient-level validation, missing-value completion, and conditional-probability modelling are possible future uses. A small connection to the existing MDPT pipeline may be demonstrated if the rule-base POC is stable.

## Success Criteria

**Primary success metric:**

The LLM-based pipeline can process a paper through rule extraction, source validation, and structured storage, producing rules that include supporting evidence and provenance.

**Minimum acceptable result:**

- PubMed ingestion works for selected publication dates.
- The LLM-based extraction agent produces structured candidate rules.
- The LLM-based validation agent identifies whether rules are supported by the source.
- Validated rules are stored with their evidence and source paper.
- The process is demonstrated on one paper and then tested on a small paper set.

**Publication or deliverable standard:**

MSc thesis, reproducible code, documented prompts, and stored outputs from the POC and evaluation.

**Go/no-go decision rule:**

If the one-paper POC produces structured rules with usable evidence and validation results, continue to the small paper-set evaluation. If not, narrow the rule schema and focus the thesis on the one-paper extraction and validation POC.

**Target completion date:** 2026-10-15

## Reproducibility

**Code repository:**

Local project repository. The remote repository location has not yet been recorded.

**Data location:**

Lab computer. PubMed metadata and experiment outputs will be stored as CSV or SQLite files. PMC full text will be used when available; papers without accessible full text will remain as metadata records for the POC.

**Environment:**

Python virtual environment using `requirements.txt`. LLM access will use the Azure connection helper. Credentials must remain outside the repository.

**Versioned datasets:**

- PubMed day snapshots
- selected paper lists
- optional PMC full-text outputs
- extracted candidate rules
- validation results
- final validated rules
- prompt versions and example outputs

**Analysis freeze date:** 2026-10-18

## Key Decisions

| Date | Decision | Rationale | Owner | Notes |
|:-----|:---------|:----------|:------|:------|
|      |          |           |       |       |

## Key Achievements and Findings

| Description | Significance or implication | Pointer to code/data/results | Date |
|:---|:---|:---|:---|
| PubMed day-snapshot ingestion is implemented. | The script retrieves PubMed IDs for a chosen date and extracts paper metadata. | `pubmed_day_snapshot.py` | 2026-08-13 |
| Extraction and validation agent POCs are complete, and a full end-to-end run (ingestion → extraction → validation) works and is rerunnable. | Core pipeline shape is proven on real PMC papers. | `almog_work/extraction/extraction_agent.py`, `almog_work/validation/validation_agent.py` | 2026-09-05 |
| Local IBM Granite model runs on GPU by default, and JSON parsing from LLM output is more resilient (falls back to `json_repair` on truncated/malformed output). | Makes the local-vs-GPT comparison (task 7) practical to run at scale instead of taking minutes per paper on CPU. | `almog_work/common/local_granite_client.py`, `almog_work/extraction/extraction_agent.py`, `almog_work/validation/validation_agent.py` | 2026-09-05 |

## Current Roadmap

| Main task | What needs to be done | Output when finished | Questions | Deadline | Status |
|:---|:---|:---|:---|---:|:---|
| **1. PubMed ingestion POC** | 1\. Create a Python project.\<br\>2. Choose a publication day.\<br\>3. Retrieve PubMed IDs.\<br\>4. Collect metadata.\<br\>5. Save results to CSV or SQLite.\<br\>6. Make the script reusable.\<br\>7. Optionally retrieve PMC full text. | `pubmed_day_snapshot.py`, `pmc_fetch.py`, and documentation. | Is it realistic to download 4,000–5,000 papers per day? We don't have to actually do it — we can show it's possible by downloading for a few days at a limited rate. Do we need to save the papers, or can we delete them and keep only the reference? Is it feasible to download thousands of papers a day at scale — need to try it and report back (e.g. download 100 papers, note how many are missing full text) so we can estimate scaling and cost later. | 2026-07-20 | **Completed** |
| **2. Paper-filter placeholder** | 1\. Keep a placeholder for possible future filtering.\<br\>2. Do not implement filtering at this stage. | Placeholder for a possible future component. |  | — | Placeholder only |
| **3. Build the extraction agent POC** | 1\. Define the structured output that the LLM should produce.\<br\>2. Define fields for the output.\<br\>3. Create the initial prompt. | A working LLM-based extraction agent. |  | 2026-08-09 | **Completed** |
| **4. Build the validation agent POC** | 1\. Define the output format.\<br\>2. Create the initial prompt. | A working LLM-based validation agent. |  | 2026-08-16 | **Completed** |
| **5. Build the complete tool POC** | 1\. Connect PubMed ingestion, extraction, and validation.\<br\>2. Run the complete process on a paper.\<br\>3. Save statements, evidence, and validation results.\<br\>4. Confirm that the tool can be rerun. | A working end-to-end tool POC. |  | 2026-09-05 | **Completed** |
| **6. Compare the local IBM model with GPT** | 1\. Select 10–15 papers.\<br\>2. Run the same papers with the local IBM model.\<br\>3. Run the same papers with GPT.\<br\>4. Use the same prompts and process.\<br\>5. Compare extracted statements, evidence, validation results, and processing time.\<br\>6. Manually review differences and errors. | A comparison of the local IBM model and GPT. |  | 2026-09-10 | In progress |
| **7. Refine the prompts and agents** | 1\. Identify errors and disagreements.\<br\>2. Modify the prompts or agent logic.\<br\>3. Run both models again on the same papers.\<br\>4. Repeat the comparison.\<br\>5. Select the model and prompt version for data testing. | A stable model and prompt configuration for the next stage. |  | 2026-09-24 |  |
| **8. Build the rule database** | 1\. Create tables for papers, candidate statements, validation results, and accepted statements.\<br\>2. Link each statement to its paper and evidence span.\<br\>3. Add fields for paper quality, statement quality, update date, and possible conflicts.\<br\>4. Insert the manually curated examples. | A database that stores and retrieves validated statements with provenance. |  | 2026-09-29 | Not started |
| **9. Small-paper evaluation** | 1\. Run the current pipeline on 5 papers.\<br\>2. Use one of Irina's datasets to try to find anomalies in the data set.\<br\>3. Classify the anomalies as extraction errors or real data problems.\<br\>4. Use the results to improve the prompt if needed. | A manually reviewed anomaly sample. |  | 2026-09-24 |  |
| **10. Connect the tool to the full MDPT pipeline** | 1\. Connect the validated statements to MDPT.\<br\>2. Confirm that MDPT can use them to create or run data tests.\<br\>3. Run an end-to-end test.\<br\>4. Document the connection. | A working connection between the tool and MDPT. |  | 2026-10-01 |  |
| **11. Test the connected pipeline on real data** | 1\. Prepare the All of Us dataset.\<br\>2. Prepare the datasets used by Irena.\<br\>3. Simulate a stream of incoming papers.\<br\>4. Extract and validate statements using the selected model.\<br\>5. Pass the statements to MDPT.\<br\>6. Record the number of data anomalies detected for each paper and dataset. | Anomaly results linked to the source paper, extracted statement, MDPT test, and dataset. |  | 2026-10-01 |  |
| **12. Sample and classify data anomalies** | 1\. Sample detected anomalies.\<br\>2. Review the source paper.\<br\>3. Review the extracted statement.\<br\>4. Review the MDPT test.\<br\>5. Review the affected data.\<br\>6. Classify each case as an extraction error, data-testing error, or real data problem. | Manually reviewed anomaly results and error classification. | We need to sample the resulting anomalies and grade them as true or false: (1) was the extraction wrong? (2) was the data testing wrong? (3) or was it right and there is actually something wrong with the data? | 2026-10-09 |  |
| **13. Create first thesis draft** | 1\. Write the methods.\<br\>2. Report the model comparison.\<br\>3. Report the prompt and agent iterations.\<br\>4. Report the MDPT integration.\<br\>5. Report the real-data evaluation.\<br\>6. Document limitations. | Thesis draft. |  | 2026-10-22 |  |
| **14. Submit draft to Rani for review** | Submit the draft for review and revise according to feedback. | Feedback incorporated into the draft. |  | 2026-10-30 |  |
| **15. Finalize the thesis** | Incorporate final feedback and complete the document. | Final MSc thesis. |  | 2026-11-30 |  |

<details>
<summary><strong>How to Fill This Project Description</summary></strong>

Use this document for the stable project baseline. Fill it out at project start, then update it only when the scope, success criteria, reproducibility setup, or core decisions materially change. Replace bracketed placeholders and keep dates in `YYYY-MM-DD` format.

</details>
