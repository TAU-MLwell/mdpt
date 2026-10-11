"""
Simple PMC fetch helper
Fetches PMC full text and returns cleaned plain text (limited length).
"""
import re
from typing import List

import requests
import xml.etree.ElementTree as ET
from html import unescape


PMC_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PMC_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def search_pmc(query: str, retmax: int = 10, timeout: int = 15) -> List[str]:
    """Search PMC for a query and return a list of PMCIDs (e.g. ['PMC1234567', ...])."""
    resp = requests.get(
        PMC_ESEARCH_URL,
        params={"db": "pmc", "term": query, "retmax": retmax, "retmode": "json"},
        timeout=timeout,
    )
    resp.raise_for_status()
    ids = resp.json().get("esearchresult", {}).get("idlist", [])
    return [f"PMC{i}" for i in ids]


def pmc_url_from_id(pmcid: str) -> str:
    """Build the standard PMC article page URL for a given PMCID."""
    return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"


def clean_html_to_text(html: str) -> str:
    # Remove script/style
    html = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", " ", html)
    # Replace tags with spaces
    text = re.sub(r"(?s)<.*?>", " ", html)
    # Unescape HTML entities
    text = unescape(text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _cell_text(cell: ET.Element) -> str:
    return " ".join("".join(cell.itertext()).split())


def _render_table_wrap(table_wrap: ET.Element) -> List[str]:
    """Render a <table-wrap> as 'Table N. <caption>' followed by one cell per line.

    This mirrors the jumbled, line-per-fragment style typical of PDF-to-text table
    extraction, which is the format the table extraction agent expects (so that the
    same '^Table N. ' caption regex and LLM reconstruction prompt work unchanged
    regardless of whether the source paper came from PDF text or PMC XML).
    """
    label = (table_wrap.findtext("label") or "").strip()
    caption_el = table_wrap.find("caption")
    caption_text = _cell_text(caption_el) if caption_el is not None else ""

    number_match = re.search(r"(\d+)", label)
    if number_match:
        heading = f"Table {number_match.group(1)}. {caption_text}".strip()
    else:
        heading = f"{label}. {caption_text}".strip()

    lines = [heading] if heading else []

    # Some table-wraps nest the real <table> inside <alternatives> alongside a
    # <graphic> fallback image, so search recursively rather than only direct children.
    table = table_wrap.find(".//table")
    if table is not None:
        for section_tag in ("thead", "tbody", "tfoot"):
            section = table.find(section_tag)
            if section is None:
                continue
            for row in section.findall("tr"):
                for cell in list(row):
                    cell_text = _cell_text(cell)
                    if cell_text:
                        lines.append(cell_text)

    foot = table_wrap.find("table-wrap-foot")
    if foot is not None:
        foot_text = _cell_text(foot)
        if foot_text:
            lines.append(foot_text)

    return lines


def _iter_body_lines(elem: ET.Element) -> List[str]:
    """Walk an XML element in document order, emitting one line per text fragment.

    Table-wrap elements are rendered specially (see _render_table_wrap) so table
    captions land at the start of a line and can be matched by the caption regex.
    """
    if elem.tag == "table-wrap":
        return _render_table_wrap(elem)

    lines: List[str] = []
    if elem.text and elem.text.strip():
        lines.append(elem.text.strip())
    for child in elem:
        lines.extend(_iter_body_lines(child))
        if child.tail and child.tail.strip():
            lines.append(child.tail.strip())
    return lines


def clean_xml_to_text(xml_text: str) -> str:
    """Extract body/abstract text from PMC XML, preserving line breaks.

    Tables are flattened one-cell-per-line (see _render_table_wrap) and section
    titles/paragraphs each get their own line, so downstream regexes that match
    table captions ('^Table N. ...') or section boundaries ('^Discussion', etc.)
    at the start of a line continue to work.
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return ""

    lines: List[str] = []

    # Prefer main article body.
    for node in root.findall(".//body"):
        lines.extend(_iter_body_lines(node))

    # Include abstract if body is unavailable or very short.
    if not lines:
        for node in root.findall(".//abstract"):
            lines.extend(_iter_body_lines(node))

    return "\n".join(lines).strip()


def extract_pmcid_from_url(pmc_url: str) -> str:
    match = re.search(r"/articles/(PMC\d+)/?", pmc_url or "", re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).upper()


def fetch_pmc_text(pmc_url: str, char_limit: int = 30000, timeout: int = 15) -> str:
    """
    Fetch the PMC page and return a cleaned plain-text version.

    Args:
        pmc_url: URL to PMC article page (e.g. https://www.ncbi.nlm.nih.gov/pmc/articles/PMCID/)
        char_limit: Maximum number of characters to return
        timeout: Request timeout

    Returns:
        Cleaned text (possibly empty string on failure)
    """
    if not pmc_url:
        return ""

    pmcid = extract_pmcid_from_url(pmc_url)

    # First choice: EFetch XML endpoint, which is stable for scripted access.
    if pmcid:
        try:
            resp = requests.get(
                PMC_EFETCH_URL,
                params={"db": "pmc", "id": pmcid, "retmode": "xml"},
                timeout=timeout,
            )
            resp.raise_for_status()
            text = clean_xml_to_text(resp.text)
            if text:
                if len(text) > char_limit:
                    text = text[:char_limit]
                return text
        except Exception:
            pass

    # Fallback: fetch page HTML when XML is unavailable.
    try:
        resp = requests.get(pmc_url, timeout=timeout)
        resp.raise_for_status()

        # Some requests may get anti-bot intermediary pages instead of paper content.
        head = (resp.text or "")[:2000].lower()
        if "checking your browser" in head or "recaptcha" in head:
            return ""

        text = clean_html_to_text(resp.text)
        if len(text) > char_limit:
            text = text[:char_limit]
        return text
    except Exception:
        return ""
