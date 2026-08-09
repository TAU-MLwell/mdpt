"""PubMed day snapshot POC.

Fetch all PubMed records for a publication day, extract a compact metadata
set, and save the results to CSV or SQLite.

Example:
    /home/almogalfamon/mdpt/.venv/bin/python almog_work/pubmed_day_snapshot.py \
        --date 2024-01-15 --format csv
"""

from __future__ import annotations

import argparse
import csv
import os
import sqlite3
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Optional, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pmc_fetch import fetch_pmc_text


ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
DEFAULT_BATCH_SIZE = 200
DEFAULT_TOOL = "mdpt_pubmed_day_snapshot"
DEFAULT_EMAIL = "agent@medical.search"
DEFAULT_REQUEST_DELAY = 0.4

MONTH_MAP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


@dataclass(frozen=True)
class RunConfig:
    publication_date: str
    output_format: str
    output_path: Path
    batch_size: int
    email: str
    api_key: Optional[str]
    download_full_text: bool
    full_text_dir: Path
    full_text_char_limit: int
    full_text_max: Optional[int]


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(
        description="Fetch all PubMed articles for one publication day and save metadata."
    )
    parser.add_argument(
        "--date",
        required=True,
        help="Publication day in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--format",
        choices=("csv", "sqlite"),
        default="csv",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path. If omitted, a file is created under almog_work/pubmed_day_snapshot_output/.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Number of PubMed IDs to fetch per request.",
    )
    parser.add_argument(
        "--email",
        default=os.getenv("NCBI_EMAIL", DEFAULT_EMAIL),
        help="Contact email passed to NCBI E-utilities.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("NCBI_API_KEY"),
        help="Optional NCBI API key.",
    )
    parser.add_argument(
        "--download-full-text",
        action="store_true",
        help="Download full text for records with PMC links.",
    )
    parser.add_argument(
        "--full-text-dir",
        default=None,
        help="Directory for downloaded full-text files. Defaults to almog_work/pubmed_day_snapshot_output/full_text_<date>/.",
    )
    parser.add_argument(
        "--full-text-char-limit",
        type=int,
        default=30000,
        help="Maximum characters to keep per downloaded full-text file.",
    )
    parser.add_argument(
        "--full-text-max",
        type=int,
        default=None,
        help="Optional cap for number of full-text files to download in a run.",
    )

    args = parser.parse_args()
    publication_date = validate_date(args.date)
    output_path = resolve_output_path(publication_date, args.format, args.output)
    full_text_dir = resolve_full_text_dir(publication_date, args.full_text_dir)
    return RunConfig(
        publication_date=publication_date,
        output_format=args.format,
        output_path=output_path,
        batch_size=max(1, args.batch_size),
        email=args.email,
        api_key=args.api_key,
        download_full_text=bool(args.download_full_text),
        full_text_dir=full_text_dir,
        full_text_char_limit=max(1000, int(args.full_text_char_limit)),
        full_text_max=max(1, args.full_text_max) if args.full_text_max else None,
    )


def validate_date(date_text: str) -> str:
    try:
        parsed = datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit("--date must use YYYY-MM-DD format") from exc
    return parsed.strftime("%Y-%m-%d")


def resolve_output_path(date_text: str, output_format: str, output_arg: Optional[str]) -> Path:
    if output_arg:
        return Path(output_arg).expanduser().resolve()

    base_dir = Path(__file__).resolve().parent / "pubmed_day_snapshot_output"
    base_dir.mkdir(parents=True, exist_ok=True)
    suffix = "csv" if output_format == "csv" else "sqlite"
    filename = f"pubmed_snapshot_{date_text}.{suffix}"
    return base_dir / filename


def resolve_full_text_dir(date_text: str, dir_arg: Optional[str]) -> Path:
    if dir_arg:
        return Path(dir_arg).expanduser().resolve()
    return Path(__file__).resolve().parent / "pubmed_day_snapshot_output" / f"full_text_{date_text}"


def chunked(items: Sequence[str], size: int) -> Iterator[List[str]]:
    for start in range(0, len(items), size):
        yield list(items[start : start + size])


def collapse_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def element_text(element: Optional[ET.Element]) -> str:
    if element is None:
        return ""
    return collapse_text("".join(element.itertext()))


def month_to_number(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    cleaned = value.strip().lower()
    if not cleaned:
        return None
    if cleaned.isdigit():
        return int(cleaned)
    return MONTH_MAP.get(cleaned)


def format_pubmed_date(date_element: Optional[ET.Element]) -> str:
    if date_element is None:
        return ""

    medline_date = element_text(date_element.find("MedlineDate"))
    if medline_date:
        return medline_date

    year = element_text(date_element.find("Year"))
    if not year:
        return ""

    month = month_to_number(element_text(date_element.find("Month")))
    day_text = element_text(date_element.find("Day"))
    if month is None or not day_text.isdigit():
        return year

    try:
        formatted = datetime(int(year), month, int(day_text))
    except ValueError:
        return year
    return formatted.strftime("%Y-%m-%d")


def extract_publication_date(article: ET.Element) -> tuple[str, str]:
    article_date = article.find(".//Article/ArticleDate")
    if article_date is not None:
        value = format_pubmed_date(article_date)
        if value:
            return value, "article_date"

    pub_date = article.find(".//Article/Journal/JournalIssue/PubDate")
    if pub_date is not None:
        value = format_pubmed_date(pub_date)
        if value:
            return value, "journal_pub_date"

    history_dates = article.findall(".//PubmedData/History/PubMedPubDate")
    for history_date in history_dates:
        value = format_pubmed_date(history_date)
        if value:
            return value, "pubmed_history"

    return "", ""


def extract_article_ids(article: ET.Element) -> dict[str, str]:
    pmc_id = ""
    doi = ""
    for article_id in article.findall(".//PubmedData/ArticleIdList/ArticleId"):
        id_type = (article_id.get("IdType") or "").lower()
        value = element_text(article_id)
        if not value:
            continue
        if id_type == "pmc" and not pmc_id:
            pmc_id = value
        if id_type == "doi" and not doi:
            doi = value
    return {"pmc_id": pmc_id, "doi": doi}


def extract_publication_types(article: ET.Element) -> str:
    publication_types = []
    for pub_type in article.findall(".//Article/PublicationTypeList/PublicationType"):
        value = element_text(pub_type)
        if value and value not in publication_types:
            publication_types.append(value)
    return "; ".join(publication_types)


def extract_abstract(article: ET.Element) -> str:
    abstract_parts = []
    for abstract_text in article.findall(".//Article/Abstract/AbstractText"):
        part = element_text(abstract_text)
        if not part:
            continue
        label = abstract_text.get("Label")
        if label:
            abstract_parts.append(f"{label}: {part}")
        else:
            abstract_parts.append(part)
    return "\n".join(abstract_parts)


def extract_article_record(article: ET.Element) -> dict[str, str]:
    pmid = element_text(article.find(".//MedlineCitation/PMID"))
    title = element_text(article.find(".//Article/ArticleTitle"))
    abstract = extract_abstract(article)
    publication_date, publication_date_source = extract_publication_date(article)
    journal = element_text(article.find(".//Article/Journal/Title"))
    publication_type = extract_publication_types(article)
    ids = extract_article_ids(article)

    pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""
    pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{ids['pmc_id']}/" if ids["pmc_id"] else ""
    doi_url = f"https://doi.org/{ids['doi']}" if ids["doi"] else ""
    full_text_url = pmc_url or doi_url
    full_text_sources = "; ".join(source for source in ("PMC" if pmc_url else "", "DOI" if doi_url else "") if source)

    return {
        "pmid": pmid,
        "title": title,
        "abstract": abstract,
        "publication_date": publication_date,
        "publication_date_source": publication_date_source,
        "journal": journal,
        "publication_type": publication_type,
        "pubmed_url": pubmed_url,
        "pmc_url": pmc_url,
        "doi_url": doi_url,
        "full_text_url": full_text_url,
        "full_text_sources": full_text_sources,
        "record_status": "success",
        "error": "",
    }


def extract_book_record(book_article: ET.Element) -> dict[str, str]:
    pmid = element_text(book_article.find(".//PMID"))
    title = element_text(book_article.find(".//BookDocument/ArticleTitle"))
    if not title:
        title = element_text(book_article.find(".//BookDocument/Book/BookTitle"))

    abstract = extract_abstract(book_article)

    publication_date = ""
    publication_date_source = ""
    book_pub_date = book_article.find(".//BookDocument/Book/PubDate")
    if book_pub_date is not None:
        publication_date = format_pubmed_date(book_pub_date)
        if publication_date:
            publication_date_source = "book_pub_date"
    if not publication_date:
        pubmed_pub_date = book_article.find(".//PubmedBookData/PubMedPubDate[@PubStatus='pubmed']")
        if pubmed_pub_date is not None:
            publication_date = format_pubmed_date(pubmed_pub_date)
            if publication_date:
                publication_date_source = "pubmed_book_date"

    journal = element_text(book_article.find(".//BookDocument/Book/BookTitle"))
    publication_type = "Book"

    pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""

    return {
        "pmid": pmid,
        "title": title,
        "abstract": abstract,
        "publication_date": publication_date,
        "publication_date_source": publication_date_source,
        "journal": journal,
        "publication_type": publication_type,
        "pubmed_url": pubmed_url,
        "pmc_url": "",
        "doi_url": "",
        "full_text_url": "",
        "full_text_sources": "",
        "full_text_download_status": "not_attempted",
        "full_text_file": "",
        "full_text_download_error": "",
        "record_status": "success",
        "error": "",
    }


def fetch_ids_for_day(session: requests.Session, config: RunConfig) -> List[str]:
    collected_ids: List[str] = []
    count = None
    retstart = 0

    while True:
        params = {
            "db": "pubmed",
            "datetype": "pdat",
            "mindate": config.publication_date,
            "maxdate": config.publication_date,
            "retmode": "xml",
            "retstart": retstart,
            "retmax": config.batch_size,
            "tool": DEFAULT_TOOL,
            "email": config.email,
        }
        if config.api_key:
            params["api_key"] = config.api_key

        if not config.api_key:
            time.sleep(DEFAULT_REQUEST_DELAY)
        response = session.get(ESEARCH_URL, params=params, timeout=60)
        response.raise_for_status()
        root = ET.fromstring(response.text)

        if count is None:
            count_text = root.findtext(".//Count") or "0"
            count = int(count_text)

        for id_element in root.findall(".//IdList/Id"):
            pmid = element_text(id_element)
            if pmid:
                collected_ids.append(pmid)

        if count == 0 or len(collected_ids) >= count:
            break

        retstart += config.batch_size

    seen = set()
    ordered_unique_ids = []
    for pmid in collected_ids:
        if pmid not in seen:
            seen.add(pmid)
            ordered_unique_ids.append(pmid)
    return ordered_unique_ids


def fetch_articles_for_ids(session: requests.Session, pmids: Sequence[str], config: RunConfig) -> List[dict[str, str]]:
    records: List[dict[str, str]] = []

    for batch in chunked(list(pmids), config.batch_size):
        params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "xml",
            "tool": DEFAULT_TOOL,
            "email": config.email,
        }
        if config.api_key:
            params["api_key"] = config.api_key

        if not config.api_key:
            time.sleep(DEFAULT_REQUEST_DELAY)
        response = session.get(EFETCH_URL, params=params, timeout=120)
        response.raise_for_status()

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as exc:
            for pmid in batch:
                records.append(
                    {
                        "pmid": pmid,
                        "title": "",
                        "abstract": "",
                        "publication_date": "",
                        "publication_date_source": "",
                        "journal": "",
                        "publication_type": "",
                        "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "pmc_url": "",
                        "doi_url": "",
                        "full_text_url": "",
                        "full_text_sources": "",
                        "full_text_download_status": "not_attempted",
                        "full_text_file": "",
                        "full_text_download_error": "",
                        "record_status": "parse_error",
                        "error": f"XML parse error: {exc}",
                    }
                )
            continue

        articles_by_pmid: dict[str, dict[str, str]] = {}
        for article in root.findall(".//PubmedArticle"):
            record = extract_article_record(article)
            if record["pmid"]:
                articles_by_pmid[record["pmid"]] = record

        for book_article in root.findall(".//PubmedBookArticle"):
            record = extract_book_record(book_article)
            if record["pmid"]:
                articles_by_pmid[record["pmid"]] = record

        for pmid in batch:
            record = articles_by_pmid.get(pmid)
            if record is None:
                records.append(
                    {
                        "pmid": pmid,
                        "title": "",
                        "abstract": "",
                        "publication_date": "",
                        "publication_date_source": "",
                        "journal": "",
                        "publication_type": "",
                        "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "pmc_url": "",
                        "doi_url": "",
                        "full_text_url": "",
                        "full_text_sources": "",
                        "full_text_download_status": "not_attempted",
                        "full_text_file": "",
                        "full_text_download_error": "",
                        "record_status": "missing_from_fetch",
                        "error": "Article not returned by EFetch",
                    }
                )
            else:
                records.append(record)

    return records


def save_as_csv(records: Sequence[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys()) if records else [
        "pmid",
        "title",
        "abstract",
        "publication_date",
        "publication_date_source",
        "journal",
        "publication_type",
        "pubmed_url",
        "pmc_url",
        "doi_url",
        "full_text_url",
        "full_text_sources",
        "full_text_download_status",
        "full_text_file",
        "full_text_download_error",
        "record_status",
        "error",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def save_as_sqlite(records: Sequence[dict[str, str]], output_path: Path, config: RunConfig) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(output_path) as connection:
        connection.execute("DROP TABLE IF EXISTS pubmed_articles")
        connection.execute("DROP TABLE IF EXISTS run_metadata")
        connection.execute(
            """
            CREATE TABLE pubmed_articles (
                pmid TEXT PRIMARY KEY,
                title TEXT,
                abstract TEXT,
                publication_date TEXT,
                publication_date_source TEXT,
                journal TEXT,
                publication_type TEXT,
                pubmed_url TEXT,
                pmc_url TEXT,
                doi_url TEXT,
                full_text_url TEXT,
                full_text_sources TEXT,
                full_text_download_status TEXT,
                full_text_file TEXT,
                full_text_download_error TEXT,
                record_status TEXT,
                error TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE run_metadata (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                publication_date TEXT,
                output_format TEXT,
                output_path TEXT,
                batch_size INTEGER,
                fetched_at TEXT,
                requested_by_email TEXT,
                download_full_text INTEGER,
                full_text_dir TEXT,
                full_text_char_limit INTEGER,
                full_text_max INTEGER
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO pubmed_articles (
                pmid, title, abstract, publication_date, publication_date_source,
                journal, publication_type, pubmed_url, pmc_url, doi_url,
                full_text_url, full_text_sources,
                full_text_download_status, full_text_file, full_text_download_error,
                record_status, error
            ) VALUES (
                :pmid, :title, :abstract, :publication_date, :publication_date_source,
                :journal, :publication_type, :pubmed_url, :pmc_url, :doi_url,
                :full_text_url, :full_text_sources,
                :full_text_download_status, :full_text_file, :full_text_download_error,
                :record_status, :error
            )
            """,
            records,
        )
        connection.execute(
            """
            INSERT INTO run_metadata (
                id, publication_date, output_format, output_path,
                batch_size, fetched_at, requested_by_email,
                download_full_text, full_text_dir, full_text_char_limit, full_text_max
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                config.publication_date,
                config.output_format,
                str(output_path),
                config.batch_size,
                datetime.utcnow().isoformat(),
                config.email,
                1 if config.download_full_text else 0,
                str(config.full_text_dir),
                config.full_text_char_limit,
                config.full_text_max,
            ),
        )
        connection.commit()


def initialize_full_text_status(records: Sequence[dict[str, str]]) -> None:
    for record in records:
        record.setdefault("full_text_download_status", "not_attempted")
        record.setdefault("full_text_file", "")
        record.setdefault("full_text_download_error", "")


def download_pmc_full_text(records: Sequence[dict[str, str]], config: RunConfig) -> None:
    if not config.download_full_text:
        return

    config.full_text_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    for record in records:
        pmid = (record.get("pmid") or "").strip()
        pmc_url = (record.get("pmc_url") or "").strip()

        if not pmid:
            record["full_text_download_status"] = "skipped_no_pmid"
            continue

        if config.full_text_max is not None and downloaded >= config.full_text_max:
            record["full_text_download_status"] = "skipped_full_text_max"
            continue

        if not pmc_url:
            record["full_text_download_status"] = "unavailable_no_pmc"
            continue

        text = fetch_pmc_text(
            pmc_url=pmc_url,
            char_limit=config.full_text_char_limit,
            timeout=30,
        )
        if not text:
            record["full_text_download_status"] = "download_failed"
            record["full_text_download_error"] = "PMC fetch returned empty content"
            continue

        output_file = config.full_text_dir / f"{pmid}.txt"
        output_file.write_text(text, encoding="utf-8")
        record["full_text_download_status"] = "downloaded"
        record["full_text_file"] = str(output_file)
        record["full_text_download_error"] = ""
        downloaded += 1


def print_summary(records: Sequence[dict[str, str]], config: RunConfig) -> None:
    success_count = sum(1 for record in records if record.get("record_status") == "success")
    error_count = len(records) - success_count
    full_text_downloaded = sum(1 for record in records if record.get("full_text_download_status") == "downloaded")
    full_text_available = sum(1 for record in records if (record.get("pmc_url") or "").strip())
    print("=" * 72)
    print("PubMed day snapshot complete")
    print(f"Date: {config.publication_date}")
    print(f"Records fetched: {len(records)}")
    print(f"Successful parses: {success_count}")
    print(f"Fallback records: {error_count}")
    print(f"PMC full-text available: {full_text_available}")
    if config.download_full_text:
        print(f"Full-text files downloaded: {full_text_downloaded}")
        print(f"Full-text directory: {config.full_text_dir}")
    else:
        print("Full-text download mode: disabled")
    print(f"Output: {config.output_path}")
    print("=" * 72)


def main() -> int:
    config = parse_args()
    session = requests.Session()
    session.headers.update({"User-Agent": f"{DEFAULT_TOOL}/1.0"})
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    print(f"Fetching PubMed IDs for {config.publication_date}...")
    pmids = fetch_ids_for_day(session, config)
    print(f"Found {len(pmids)} IDs.")

    if not pmids:
        records: List[dict[str, str]] = []
    else:
        print(f"Fetching metadata in batches of {config.batch_size}...")
        records = fetch_articles_for_ids(session, pmids, config)

    initialize_full_text_status(records)
    if config.download_full_text:
        print("Downloading PMC full text for eligible records...")
    download_pmc_full_text(records, config)

    if config.output_format == "csv":
        save_as_csv(records, config.output_path)
    elif config.output_format == "sqlite":
        save_as_sqlite(records, config.output_path, config)
    else:
        raise SystemExit(f"Unsupported output format: {config.output_format}")

    print_summary(records, config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())