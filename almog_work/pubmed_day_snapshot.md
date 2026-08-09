# PubMed Day Snapshot POC

Small CLI utility for collecting PubMed metadata for every article published on a single day, with an optional mode to download full-text content when a PMC link is available.

## What it captures

- PMID
- title
- abstract
- publication date
- journal
- publication type
- full-text links when available

## Run

```bash
/home/almogalfamon/mdpt/.venv/bin/python almog_work/pubmed_day_snapshot.py \
  --date 2026-07-11 \
  --format csv
```

To write SQLite instead:

```bash
/home/almogalfamon/mdpt/.venv/bin/python almog_work/pubmed_day_snapshot.py \
  --date 2026-07-11 \
  --format sqlite
```

If `--output` is omitted, results are saved under `almog_work/pubmed_day_snapshot_output/`.

## Download Full Paper Text

Enable full-text download mode:

```bash
/home/almogalfamon/mdpt/.venv/bin/python almog_work/pubmed_day_snapshot.py \
  --date 2026-07-11 \
  --format csv \
  --download-full-text
```

Useful options:

- `--full-text-dir /path/to/folder`: custom output folder for text files.
- `--full-text-char-limit 50000`: keep more characters per downloaded paper.
- `--full-text-max 20`: cap download count for quick testing.

Important note:

- Full-text download currently uses PMC links (open-access availability). Not every PubMed record has a downloadable full paper.
- Download status is tracked in output columns: `full_text_download_status`, `full_text_file`, `full_text_download_error`.

## Validation

The POC has been run successfully on multiple publication days and writes both CSV and SQLite outputs.

- It fetches all PubMed IDs for the chosen date.
- It extracts metadata for standard journal articles and PubMed book records.
- It can be rerun with a different `--date` without changing the code.

## Next Stage

Stage 3 is not a hard-coded rule engine. It is a prompt-driven LLM workflow that extracts structured clinical statements from article text.

The initial schema should capture:

- rule text
- rule type
- variables
- conditions
- expected value or relationship
- context
- evidence span
- source paper
- confidence
- validation verdict

For multi-variable statements, represent one primary relationship and attach each variable with a role, value, and condition when needed.

The first prompt should have three parts:

- extraction from the article
- validation that the extraction is supported by the source text
- formatting the output so it is easy to store in a database

The next step is to create 5 to 10 manually curated example records from papers so the schema can be tested before running the LLM at scale.