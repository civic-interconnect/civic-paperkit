"""Orchestration module for downloading and managing assets linked to bibliography entries.

This module provides:
- DownloadRecord and Summary dataclasses for tracking downloads,
- Functions to guess filenames, run the download process, and handle asset scraping.

File: src/civic_interconnect/paperkit/orchestrate.py
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .bib import load_bib_keys
from .config import DEFAULT_ALLOWED_EXTS, load_meta
from .download import download_file, ensure_dir, safe_filename
from .log import logger
from .scrape import extract_links

DEFAULT_OUTPUT_ROOT = Path("data/raw")


@dataclass
class DownloadRecord:
    """Represents a record of downloaded assets for a bibliography entry.

    Attributes
    ----------
    bibkey : str
        The bibliography key associated with the entry.
    paths : list[Path]
        List of file paths to successfully downloaded assets.
    errors : list[str]
        List of error messages encountered during download.
    """

    bibkey: str
    paths: list[Path] = field(default_factory=lambda: [])
    errors: list[str] = field(default_factory=lambda: [])


@dataclass
class Summary:
    """Summary of the download process for bibliography entries.

    Attributes
    ----------
    processed : list[DownloadRecord]
        List of records for processed entries.
    skipped : list[str]
        List of keys that were skipped.
    """

    processed: list[DownloadRecord] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def guess_filename_from_url(url: str) -> str:
    """Guess a safe filename from a URL.

    Parameters
    ----------
    url : str
        The URL from which to extract the filename.

    Returns
    -------
    str
        A sanitized filename derived from the URL.
    """
    base = Path(urlparse(url).path).name or "download"
    return safe_filename(base)


def run(bib_path: Path, meta_path: Path, out_root: Path, client: Any) -> Summary:
    """Orchestrate the download of assets for bibliography entries.

    Parameters
    ----------
    bib_path : Path
        Path to the bibliography file.
    meta_path : Path
        Path to the metadata file.
    out_root : Path
        Root directory for output files.
    client : any
        HTTP client for downloading files.

    Returns
    -------
    Summary
        Summary of processed entries and any errors encountered.
    """
    keys = set(load_bib_keys(bib_path))
    meta = load_meta(meta_path)
    common = sorted(keys.intersection(meta.keys()))
    summary = Summary()

    if not common:
        logger.warning("No overlapping keys between .bib and meta; nothing to do.")
        return summary

    for key in common:
        rec = DownloadRecord(bibkey=key)
        entry_meta = meta[key] or {}
        subdir = entry_meta.get("out_dir")
        assets = entry_meta.get("assets", [])

        for a in assets:
            try:
                # direct file
                if "url" in a:
                    out_dir = out_root / key / (subdir or ".")
                    ensure_dir(out_dir)
                    fname = a.get("filename") or guess_filename_from_url(a["url"])
                    p = out_dir / fname
                    download_file(client, a["url"], p, a.get("checksum"))
                    rec.paths.append(p)
                # page scrape
                elif "page_url" in a:
                    logger.info("[%s] Scraping page %s", key, a["page_url"])
                    allow = a.get("allow_ext") or DEFAULT_ALLOWED_EXTS
                    rx = a.get("href_regex")
                    limit = a.get("limit")
                    resp = client.get(a["page_url"])
                    links = extract_links(resp.text, a.get("base_url") or a["page_url"], allow, rx)
                    if limit is not None:
                        links = links[: int(limit)]
                    out_dir = out_root / key / (subdir or ".")
                    ensure_dir(out_dir)
                    for u in links:
                        p = out_dir / guess_filename_from_url(u)
                        download_file(client, u, p)
                        rec.paths.append(p)
                else:
                    msg = "unknown asset type"
                    rec.errors.append(msg)
                    logger.warning("[%s] %s", key, msg)
            except Exception as exc:
                rec.errors.append(str(exc))
                logger.error("[%s] %s", key, exc)
        summary.processed.append(rec)
    return summary
