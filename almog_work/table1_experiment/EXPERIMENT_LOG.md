# Table 1 prompt-optimization experiment: log

Single place for the whole history of this work: how it started, what was built, what was run, what came out, and what it means. Add new events to section 0 (newest at the bottom), new results to section 6, and update sections 7 and 8; do not rewrite earlier results.

Last updated: 2026-10-23

---

## 0. Timeline of the whole project

Dates are 2026. Details after 2026-10-11 come from the chat session record; the first days of data collection (before the first entry below) are known only from the files they left (`almog_work/data_acquisition/`, `almog_work/data/`).

| Date | What happened |
|---|---|
| before 10-08 | PubMed day snapshot of 2026-09-01 and PMC full-text fetching (`data_acquisition/`). Earlier Granite/GPU extraction work was removed in favor of GPT-4o via Azure (git history). `test_paper` already existed from this work. |
| 10-08 | Advisor meeting. Agreed: work on Table extraction only; use a fixed set of 10 manually checked papers as a validation set; build a scoring tool that returns a score plus a few mistake examples (not all, to avoid overfitting); give that tool to an AI framework so it can improve prompts like gradient descent; version every prompt with its score; plot a learning curve; later measure generalization on unseen papers. Open question: one git branch per run. |
| 10-10 | Repository review (`almog_work`) to prepare a plan. |
| 10-11 | Paper pool for the validation set: `test_paper` plus 9 PMC papers with a Table 1 of baseline characteristics. Issues found and fixed while checking the extracted tables: papers fetched with no Table 1; nested column headers (leaf columns became the columns, group name goes into the label); `row_group` null instead of the section name (for example Demographics, Medication); missing first-column header (for example `Clinical parameters`); blank cells in grouped rows. |
| 10-11 | All 10 gold tables manually reviewed and validated (9 files at first, the 10th, `PMC13651901`, added shortly after) in `almog_work/data/gold_tables/` using one schema: `paper_id, table_number, found, table_title, columns, cells, raw_table_text`; a blank cell has no record, a zero is a record. |
| 10-11 | Built the deterministic scorer `validation/score_table_extraction.py` (no LLM). Requirement: the pipeline's models must never see gold. Intended loop: extractor -> JSON in gold format -> scorer -> score plus a few mistakes -> prompt adjusted (possibly by a separate prompt-engineer agent). Discussed the advisor's per-run git branch idea against this repo being part of the larger `mdpt` project; no per-run branches were created; the loop writes versioned run folders under `data/table1_experiments/` instead. Committed and pushed (commit `43d007b`, gold tables, extraction updates, scorer), after asking that no API key be exposed. |
| 10-13 | Built a separate Table-1 extractor (`table1_experiment/`) with a configurable prompt; the original extractor and runner stay unchanged. Matches the gold schema. Single-run pipeline: paper text -> extract -> save -> score -> log. 63 synthetic tests passed. No real model run yet. |
| 10-15 | Status review: one extraction-and-scoring run existed; no optimizer, no dev/holdout split, no real baseline. Discussed isolation of gold files and git history from the agents (enforcement not yet built). Considered Langfuse (visualization only) and OpenEvolve (optional, would replace the planned loop); neither adopted. Experiment folder consolidated from 7 code files to 4 (39 experiment tests, 24 scorer tests). Plan agreed: split dev/holdout, scoring service with budgets, baseline run, `optimizer.py` loop, then a holdout evaluation. |
| 10-15 | Added the dev/holdout split (`config.json`, seed 42), a service budget per run, and the optimizer loop. Rule from you: the loop must run by itself, with no manual prompt editing. |
| 10-18 morning | Loops run from the terminal. Failed loops (deleted at your request, output not kept): `...082302`, `...083545` and `...091748` (optimizer guidance rejected), `...082713` (scorer token missing in the shell; fixed by reading it from `.env`), `...084634` (a paper's invalid model output aborted the baseline; fixed by retry, then scored as empty). Fixes listed in section 4. |
| 10-18 | Loops 1 to 4 and the two holdout runs (section 6). Analysis and re-scoring of loop 4 (sections 6.4 and 6.5). |
| 10-23 | This log created; every new test and analysis is to be added here. |

---

## 1. Goal and design

- **Task:** extract "Table 1" of a biomedical paper into cells `(row_group, row_label, column_label, value)`.
- **Question:** can an automatic loop improve the extraction prompt without ever showing the extractor the gold tables?
- **Loop:** extractor model reads paper text -> predictions saved as JSON -> private scorer returns metrics plus a few bounded mistake examples -> optimizer model rewrites only the `guidance` text of the prompt -> repeat.
- **Models:** Azure OpenAI deployment `almog-gpt-5.1` for both extractor and optimizer (`almog_work/common/openai_client.py`).
- **Fixed vs editable prompt:** `prompts/baseline.json` holds a fixed `system` and `user` template (output-format rules) and an editable `guidance`. The baseline guidance is one sentence (101 characters): "Extract the whole table faithfully, including every row and every reported value, exactly as written."
- **Optimizer sees:** the fixed template, all earlier guidance texts, aggregate scores per paper, how many papers were invalid or had repeated cells, and the scorer's bounded mistake examples. It never sees gold tables, article text or file paths.

## 2. Data and split

10 papers with gold tables. Split fixed before any run, from file names only, `split_seed = 42` (a seed fixes the shuffle order; it is not a count). Defined in `config.json`.

| Role | Papers |
|---|---|
| Dev (6), used by the loop | `test_paper`, `PMC13651293`, `PMC13652250`, `PMC13652315`, `PMC13651901`, `PMC13652390` |
| Holdout (4), final test only | `PMC13650419`, `PMC13652246`, `PMC13649618`, `PMC13649870` |

`test_paper` is dev because it was used earlier while building the extractor. Paper texts are in `almog_work/data/table1_papers/`, gold in `almog_work/data/gold_tables/`.

## 3. Metric and scorer

- **Cell F1 (main):** micro precision, recall and F1 over exact `(row_group, row_label, column_label, value)` cells. A cell is right only if all four fields match after normalization (`validation/score_table_extraction.py`: non-breaking and thin spaces, dash variants, `>=`/`<=` symbols, spacing after `<`/`>`). A blank cell has no record; zero, N/A and dashes are kept as strings.
- **Also reported:** key-only metrics and value accuracy on matched keys.
- **Service:** `validation/scoring_service.py`, loopback HTTP `POST /score`, bearer token `TABLE_SCORER_TOKEN` (64 random characters in `almog_work/.env`, loaded by the loop and the service; unrelated to the Azure key). Budgets are per process and reset on restart. `--keys` limits a service to one split.
- **Dev scorer:** port 18765. Final loop: 20 evaluations, 66 feedback examples, 6 examples per evaluation.
- **Holdout scorer:** port 18766, 1 evaluation, 0 feedback, 0 examples, restarted once between the two holdout runs.

## 4. Pipeline code (all under `almog_work/table1_experiment/`)

| File | Role |
|---|---|
| `extractor.py` | prompt rendering, JSON parsing, validation, `extract_table_one` |
| `run_experiment.py` | one run over a split, retries, writes `run.json`, `scores.json`; CLI `--split dev|holdout --final` |
| `optimizer.py` | the loop (`run_loop`), guidance proposal, stop rules; writes `results.csv`, `best_prompt.json`, `loop.json` |
| `scorer_client.py` | token loading, scorer calls, report validation |
| `config.json` | split, scorer URLs, loop settings (`max_iterations 10`, `min_improvement 0.005`, `patience null` = no early stop) |
| `analyze_dev_runs.py` | read-only: failure categories and paper features for a finished loop |
| `rescore_normalized.py` | read-only: re-scores saved dev predictions with spacing/footnote normalization |

Unchanged originals: `extraction/table_extraction_agent.py`, `pipeline/run_table_extraction.py`, `extraction_agent.py`, `export_model_csvs.py`. Tests: `python3 -m unittest discover -s almog_work/table1_experiment -p 'test_*.py' -t .` from `/home/almogalfamon/mdpt` (68 passing at last run).

### Behaviour changes made during the work (in order)

1. Guidance length cap raised to 8000 characters, with a reason-aware retry; optimizer token cap raised to 8000 so replies are not cut off.
2. Scorer token read from `.env` when the environment variable is unset.
3. Blank-value cells are dropped before validation (a whole table was being rejected for one blank cell).
4. Invalid model output is retried up to 3 times; after that the paper is scored as an empty prediction and reported to the optimizer by key only. Real faults still abort.
5. Repeated cells (same row group, row label, column label) are no longer a table-level rejection: the first copy is kept, the rest dropped and counted (`duplicates_dropped` in `run.json`, shown to the optimizer as counts only).
6. Optimizer prompt now states the 8000-character limit as hard, asks for about 3000, and tells it to merge and delete rules instead of extending them (the previous version made the optimizer write 11-12k characters and abort a run).
7. Early stopping (`patience`) can be disabled with `null`; default config now runs all iterations.

## 5. Folder index (`almog_work/data/table1_experiments/`)

| Folder | What |
|---|---|
| `loop_20261018T093513Z_59566af0` | loop 1 (kept for reference) |
| `loop_20261018T095907Z_5638a483` | loop 2, failed at iteration 2 |
| `loop_20261018T101412Z_62eff73c` | loop 3 |
| `loop_20261018T115610Z_3e75ae0c` | loop 4, the final 10-iteration loop; has `analysis/` |
| `holdout_baseline` | baseline prompt on the 4 holdout papers |
| `holdout_best_v02` | loop-4 `v02` on the 4 holdout papers |

Each loop folder: `prompts/vNN.json`, `runs/vNN/{prompt.json,run.json,scores.json,predictions/}`, `results.csv`, `loop.json`, `best_prompt.json`.

## 6. Results

### 6.1 Loops 1 to 3 (preliminary, shorter loops)

| Loop | Settings | Outcome | Cell F1 by version |
|---|---|---|---|
| 1 (`...093513`) | 4 iterations, patience 2 | stopped: no improvement, baseline best | baseline 0.573, v01 0.498, v02 0.304 |
| 2 (`...095907`) | 4 iterations, patience 2 | failed at iteration 2: optimizer wrote 11-12k-character guidance three times (limit 8000) | baseline 0.334, v01 0.459 |
| 3 (`...101412`) | 4 iterations, patience 2 | stopped: no improvement, baseline best | baseline 0.672, v01 0.435, v02 0.425 |

Code changed between these loops (see section 4), so the baseline numbers are not from identical conditions. Even so, the same 101-character baseline scored 0.573, 0.334, 0.672 and 0.310 across the four loops (range 0.31 to 0.67).

### 6.2 Loop 4, the final loop (baseline plus 10 iterations, no early stop, 6 examples per evaluation)

Dev cell F1 (strict scorer):

| Version | Cell F1 | Guidance chars |
|---|---|---|
| baseline | 0.310 | 101 |
| v01 | 0.649 | 3602 |
| **v02 (best)** | **0.698** | 3434 |
| v03 | 0.554 | 3478 |
| v04 | 0.430 | 3861 |
| v05 | 0.437 | 3912 |
| v06 | 0.442 | 4031 |
| v07 | 0.343 | 4114 |
| v08 | 0.439 | 4000 |
| v09 | 0.448 | 3717 |
| v10 | 0.397 | 4006 |

Stop reason `max_iterations`; best version `v02` (`best_prompt.json`). Feedback budget was fully used (0 left).

Per dev paper, baseline versus `v02`:

| Paper | baseline | v02 | later versions |
|---|---|---|---|
| `test_paper` | 0.08 | 0.68 | 0.17 to 0.59 |
| `PMC13651293` | 0.48 | 0.48 | 0.48 |
| `PMC13652250` | 0.88 | 0.92 | 0.95 to 0.99 |
| `PMC13652315` | 0.03 | 0.89 | 0.00 from v04 on (v03 0.89) |
| `PMC13651901` | 1.00 | 1.00 | 1.00 |
| `PMC13652390` | 0.27 | 0.27 | 0.25 to 0.27 |

### 6.3 Holdout test (one run per prompt, 4 unseen papers)

| Paper | baseline | v02 |
|---|---|---|
| `PMC13650419` | 0.61 | 0.91 |
| `PMC13652246` | 0.90 | 0.90 |
| `PMC13649618` | 0.16 | 0.14 |
| `PMC13649870` | 0.08 | 0.08 |
| **Overall cell F1** | **0.414** | **0.455** |

Gain +0.04, all from `PMC13650419`. The holdout scorer was spent after one evaluation per prompt, so these cannot be repeated without invalidating the test.

### 6.4 Analysis of loop-4 dev results (read-only; `analysis/` inside the loop folder)

Every gold cell is put in one category (summed over all 11 versions, percent of gold cells):

| Paper | Mean F1 (sd) | Exact | Value differs | Column label wrong | Row missing or wrong | Gold cells |
|---|---|---|---|---|---|---|
| `PMC13651901` | 1.00 (0.00) | 100 | 0 | 0 | 0 | 30 |
| `PMC13652250` | 0.95 (0.03) | 93 | 1 | 0 | 0 | 44 |
| `PMC13651293` | 0.48 (0.00) | 48 | 8 | 45 | 0 | 130 |
| `test_paper` | 0.44 (0.19) | 42 | 8 | 18 | 18 | 150 |
| `PMC13652390` | 0.27 (0.01) | 27 | 0 | 20 | 53 | 30 |
| `PMC13652315` | 0.25 (0.39) | 25 | 4 | 68 | 3 | 130 |

Findings:

- Value errors are small (at most 8% of gold cells). Most loss is label mismatch, which makes a whole cell fail even when the value is right.
- **Spacing only:** `PMC13651293` loses 45% of cells because the model copies `20–30 years(n = 20)` (no space before the parenthesis, as in the source) while the gold has `20-30 years (n = 20)`. Identical in every version.
- **Text added or cut:** `PMC13652390`. Gold `Internet hospital, n (%)`, predicted `Internet hospital`; gold `Total hospitals (N=158)`, predicted `Total hospitals`; footnote letters appended (`...(IQR)c`).
- **Different structure:** `PMC13652315` has a two-level header. The model alternates between `SCHEDULE: Everolimus (n = 38)` (matches) and `SCHEDULE (n = 83) a: Everolimus (n = 38)` (does not). This is why its score swings between 0.89 and 0.00 and depends on guidance wording.
- `test_paper` mixes column mismatches, missing rows, ungenerated cells and wrong row groups, and is the least stable paper.
- Paper features versus mean F1 (Spearman, 6 papers, descriptive only): table text length -0.66, share of rows with a row group -0.66, share of nested column headers -0.65, number of columns -0.53, share of columns with `n =` -0.50. Larger, grouped, nested tables score lower. Not statistically meaningful with n = 6.

### 6.5 Re-scoring with normalized label matching (read-only, dev only)

Spacing rule: labels compared case-insensitively with all whitespace removed (values unchanged). Footnote rule: spacing plus trailing footnote markers removed from labels. The script reproduces the official strict F1 exactly (max difference 0.0000).

| Version | Strict | Spacing | Spacing + footnote |
|---|---|---|---|
| baseline | 0.310 | 0.427 | 0.435 |
| v01 | 0.649 | 0.763 | 0.771 |
| v02 | 0.698 | 0.813 | 0.821 |
| v03 | 0.554 | 0.669 | 0.676 |
| v10 | 0.397 | 0.510 | 0.518 |

Per paper (mean over versions, strict / spacing / spacing + footnote): `PMC13651293` 0.48 / 0.92 / 0.92; `PMC13652390` 0.27 / 0.27 / 0.40; `PMC13652315`, `test_paper`, `PMC13652250`, `PMC13651901` unchanged.

- Spacing alone lifts every version by about 0.11; footnote markers add under 0.01.
- Version ranking and the gain over baseline are the same under all three rules (+0.388 strict, +0.386 spacing). The formatting problem is a constant offset, not the reason the loop plateaued.
- The scorer service and saved results were not changed. Holdout was not re-scored.

## 7. Conclusions so far

1. Dev gain (0.31 to 0.70) is inflated: best of 10 versions chosen on the same 6 papers, plus an unusually low baseline run.
2. On unseen papers the best prompt gains only +0.04 (0.414 to 0.455), from one paper, one run each. This is within the observed noise.
3. The extractor model is noisy: the same prompt scored 0.31 to 0.67 across loops. One validation failure or one flipped header format can move a paper's score a lot.
4. The weak papers fail mostly on label conventions (spacing, added or cut text, header combination), not extraction. The loop saw few such examples because the dev set is small, so guidance fixed dev-specific cases and did not generalize.
5. The loop never recovered `PMC13652315` after v03; the header-combination rule is unstable.

## 8. Open items and ideas (not started)

- Add more and more varied dev papers; keep the holdout unchanged. Most direct protection against overfitting.
- Score each prompt on 2 to 3 extraction passes and average; require the best version to beat baseline by a margin.
- Put the gold's label conventions in the fixed prompt template (needs your advisor to state them, not read from holdout gold).
- Decide whether the scorer should normalize spacing (and footnote markers). A normalization-only change is low risk; fuzzy or partial matching is higher risk. Keep strict and normalized scores side by side. Ask which matters downstream.
- Ask about re-scoring the holdout runs with the normalized rules (would use holdout gold for a metric check only).

## 9. Integrity notes

- Gold tables were never given to the extractor or the optimizer. The optimizer received only scores and the scorer's bounded examples.
- Holdout papers were never used by the loop. The two saved holdout runs were scored once each.
- After the holdout runs, the assistant inspected the predictions and source texts of `PMC13649618` and `PMC13649870` (not their gold tables) to look for causes of the low scores. The holdout gold was not read for any analysis. No prompts or code were changed as a result.
- Scorer token and Azure key live only in `almog_work/.env`; neither is printed or logged.
- Nothing has been committed or pushed.

## 10. How to reproduce

From `/home/almogalfamon/mdpt`:

```
# dev scorer (fresh budget)
cd almog_work/validation && nohup env -u TABLE_SCORER_TOKEN python3 scoring_service.py --gold-dir ../data/gold_tables --port 18765 --max-evaluations 20 --feedback-budget 66 --max-examples 6 --keys test_paper,PMC13651293,PMC13652250,PMC13652315,PMC13651901,PMC13652390 > /tmp/scorer18765.log 2>&1 &

# loop (new baseline, config.json settings)
PYTHONPATH=. almog_work/.venv/bin/python -m almog_work.table1_experiment.optimizer --timeout 120

# read-only analyses on a finished loop
PYTHONPATH=. almog_work/.venv/bin/python almog_work/table1_experiment/analyze_dev_runs.py <loop_dir>
PYTHONPATH=. almog_work/.venv/bin/python almog_work/table1_experiment/rescore_normalized.py <loop_dir>
```

Holdout (once per prompt, restart the holdout scorer between prompts): scorer on port 18766 with `--max-evaluations 1 --feedback-budget 0 --max-examples 0 --keys PMC13650419,PMC13652246,PMC13649618,PMC13649870`, then `run_experiment --split holdout --final --run-dir <new dir> [--prompt-config <best_prompt.json>]`.
