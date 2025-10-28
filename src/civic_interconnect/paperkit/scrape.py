"""Functions for extracting and filtering links from HTML documents.

This module provides utilities to parse HTML, extract anchor links,
filter them by extension and regular expression, and log the results.

File: src/civic_interconnect/paperkit/scrape.py
"""

from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .log import logger


def extract_links(
    html: str, base_url: str, allow_ext: list[str], href_regex: str | None
) -> list[str]:
    """Extract and filter anchor links from an HTML document.

    Parameters
    ----------
    html : str
        The HTML content to parse.
    base_url : str
        The base URL to resolve relative links.
    allow_ext : list[str]
        List of allowed file extensions (e.g., ['.pdf', '.html']).
    href_regex : str | None
        Optional regular expression to further filter hrefs.

    Returns
    -------
    list[str]
        List of filtered, absolute URLs extracted from the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    rx = re.compile(href_regex, re.I) if href_regex else None
    out: list[str] = []
    seen: set[str] = set()

    allow = [e.lower() for e in allow_ext] if allow_ext else []

    for a in soup.find_all("a", href=True):
        href = str(a["href"]).strip()
        full = urljoin(base_url, href)
        ext = Path(urlparse(full).path).suffix.lower()
        if allow and ext not in allow:
            continue
        if rx and not rx.search(href):
            continue
        if full not in seen:
            seen.add(full)
            out.append(full)
    logger.debug("Extracted %d links from %s", len(out), base_url)
    return out
