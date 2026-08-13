# Project description

##### [**Undermind**](https://undermind.ai)

---


## Table of Contents

- [Project Description](#project-description)
  - [Project Summary](#project-summary)
  - [Research Description](#research-description)
  - [Success Criteria](#success-criteria)
  - [Reproducibility](#reproducibility)
  - [Key Decisions](#key-decisions)
  - [Key Achievements and Findings](#key-achievements-and-findings)
  - [Current Roadmap](#current-roadmap)
  - [Current Code and Project Files](#current-code-and-project-files)
  - [Immediate Next Task](#immediate-next-task)

# Project Description

## Project Summary

**Project name:** Literature-Derived Clinical Rule Base for MDPT

**Project owner:** Almog Alfamon

**Advisor:** Ran Gilad-Bachrach

**Start date:** Not recorded

**Target completion date:** 2026-10-31

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

MSc thesis, research poster, reproducible code, documented prompts, and stored outputs from the POC and evaluation.

**Go/no-go decision rule:**

If the one-paper POC produces structured rules with usable evidence and validation results, continue to the small paper-set evaluation. If not, narrow the rule schema and focus the thesis on the one-paper extraction and validation POC.

**Target completion date:** 2026-10-31

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

## Current Roadmap

| Main task | What needs to be done | Output when finished | Questions | Deadline | Status |
|:---|:---|:---|:---|---:|:---|
| **1. PubMed ingestion POC** | 1\. Create a small Python project.\<br\>2. Choose a past publication day.\<br\>3. Retrieve all PubMed IDs.\<br\>4. Collect PMID, title, abstract, publication date, journal, publication type, and full-text links when available.\<br\>5. Save the results to CSV or SQLite.\<br\>6. Make the script reusable for another date.\<br\>7. Optionally retrieve and clean PMC full text. | `pubmed_day_snapshot.py`, `pmc_fetch.py`, and documentation. The POC fetches PubMed records, saves metadata, can be rerun for another date, and optionally retrieves PMC full text. | How much full text is available? What is the cost and storage requirement at larger scale? | 2026-07-20 | **Completed** |
| **2. Paper-filter placeholder** | 1\. Keep a placeholder for possible future filtering of papers.\<br\>2. Do not implement filtering at this stage. | Placeholder for a possible future component. | Is this needed for the final system? | — | Placeholder only |
| **3. Define the clinical statement format and initial prompt** | 1\. Define the structured output that the LLM should produce.\<br\>2. Define fields for statement text, statement type, variables, conditions, expected value or relationship, context, evidence span, source paper, confidence, and validation verdict.\<br\>3. Decide how multi-variable statements are represented.\<br\>4. Create 5–10 manually curated examples.\<br\>5. Draft the extraction prompt.\<br\>6. Draft the source-validation prompt.\<br\>7. Define the database-friendly output format. | A written statement schema, example records, and an initial LLM prompt. | What information should the LLM extract? Which quantitative and relational statements should be included? | 2026-08-09 |  |
| **4. Build the rule database** | 1\. Create tables for papers, candidate statements, validation results, and accepted statements.\<br\>2. Link each statement to its paper and evidence span.\<br\>3. Add fields for paper quality, statement quality, update date, and possible conflicts.\<br\>4. Insert the manually curated examples.\<br\>5. Test storing and retrieving statements. | A database that stores and retrieves validated statements with provenance. | How should quality and conflicting statements be represented? | 2026-08-16 |  |
| **5. Add Azure LLM statement extraction** | 1\. Connect the existing extraction agent to Azure.\<br\>2. Load the initial prompt and statement schema.\<br\>3. Send one paper to the LLM at a time.\<br\>4. Require structured output and evidence spans.\<br\>5. Parse the response.\<br\>6. Save candidate statements in the database.\<br\>7. Test the agent on the initial paper. | An LLM-based extraction agent that produces candidate statements in the database format. | How well does the LLM extract the intended information? | 2026-08-30 |  |
| **6. Add Azure LLM statement validation** | 1\. Give the validation agent one candidate statement and the relevant paper text.\<br\>2. Require a supported, partially supported, unsupported, or too-vague verdict.\<br\>3. Require supporting evidence.\<br\>4. Require a short explanation.\<br\>5. Store the verdict and confidence.\<br\>6. Store corrected wording when needed.\<br\>7. Define which statements enter the final rule base. | An LLM-based validation agent that identifies unsupported or weakly grounded statements. | Which statements should be accepted into the final rule base? | 2026-09-13 |  |
| **7. Run the complete one-paper POC** | 1\. Choose one full-text paper.\<br\>2. Load its metadata and text.\<br\>3. Run LLM-based extraction.\<br\>4. Run LLM-based validation.\<br\>5. Store the results in the database.\<br\>6. Review every output manually.\<br\>7. Record hallucinations, missing context, wrong variables, overly broad statements, and weak evidence.\<br\>8. Demonstrate use of the database on available cases.\<br\>9. Refine the prompts and schema. | A documented end-to-end POC and an improved pipeline. | How can the validated statements be used in a real data-validation example? | 2026-09-20 |  |
| **8. Build the general rule-base workflow** | 1\. Connect PubMed ingestion to selected papers.\<br\>2. Connect selected papers to LLM-based extraction.\<br\>3. Connect extraction to LLM-based validation.\<br\>4. Connect validation to the database.\<br\>5. Add a simple paper-quality score version 1.\<br\>6. Define how new papers update existing statements.\<br\>7. Store conflicting statements with their sources and scores. | A small working prototype of an updateable clinical rule base. | How should the database be refreshed and how should conflicts be handled? | 2026-10-04 |  |
| **9. Evaluate, demonstrate use, and write** | 1\. Select a small paper set, ideally 8–12 papers.\<br\>2. Run the pipeline on the selected papers.\<br\>3. Compare candidate statements before and after validation.\<br\>4. Count supported, rejected, and unclear statements.\<br\>5. Document common failure cases.\<br\>6. Link selected validated statements to structured-data variables.\<br\>7. Connect the demonstration to the existing MDPT pipeline.\<br\>8. Write the methods, results, limitations, and future work. | Thesis-ready results, figures, system description, MDPT connection, and a downstream semantic-auditing example. | What is the minimum demonstration needed to show usefulness? | 2026-10-31 |  |

## Current Code and Project Files

- `almog_work/`

## Immediate Next Task
