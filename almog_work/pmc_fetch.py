"""
Simple PMC fetch helper
Fetches PMC full text and returns cleaned plain text (limited length).
"""
import re
import requests
import xml.etree.ElementTree as ET
from html import unescape


PMC_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


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


def clean_xml_to_text(xml_text: str) -> str:
    """Extract body/abstract text from PMC XML and collapse whitespace."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return ""

    text_parts = []

    # Prefer main article body.
    for node in root.findall(".//body"):
        content = " ".join("".join(node.itertext()).split())
        if content:
            text_parts.append(content)

    # Include abstract if body is unavailable or very short.
    if not text_parts:
        for node in root.findall(".//abstract"):
            content = " ".join("".join(node.itertext()).split())
            if content:
                text_parts.append(content)

    return "\n\n".join(text_parts).strip()


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
