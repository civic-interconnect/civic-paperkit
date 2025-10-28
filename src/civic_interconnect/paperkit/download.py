"""File download utilities with checksum validation and safe filename handling.

This module provides:
- ensure_dir: Create directories recursively if they don't exist
- safe_filename: Convert strings to filesystem-safe filenames
- sha256_file: Calculate SHA256 hash of a file
- write_bytes: Write bytes to a file with directory creation
- download_file: Download files with optional checksum verification

File: src/civic_interconnect/paperkit/download.py
"""

import hashlib
from html import unescape
from pathlib import Path
import re
from typing import Any

from .log import logger


def ensure_dir(p: Path) -> None:
    """Create the directory at the given path, including any necessary parent directories.

    Parameters
    ----------
    p : Path
        The directory path to create.
    """
    p.mkdir(parents=True, exist_ok=True)


def safe_filename(name: str) -> str:
    """Convert a string to a filesystem-safe filename.

    Parameters
    ----------
    name : str
        The original filename or string.

    Returns
    -------
    str
        A sanitized, filesystem-safe filename.
    """
    name = unescape(name).strip()
    name = re.sub(r"[\\/:*?\"<>|\s]+", "_", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "file"


def sha256_file(path: Path) -> str:
    """Calculate the SHA256 hash of a file.

    Parameters
    ----------
    path : Path
        The path to the file to hash.

    Returns
    -------
    str
        The SHA256 hexadecimal digest of the file.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_bytes(path: Path, content: bytes) -> None:
    """Write bytes to a file, creating parent directories if necessary.

    Parameters
    ----------
    path : Path
        The file path to write to.
    content : bytes
        The bytes content to write.

    Returns
    -------
    None
    """
    ensure_dir(path.parent)
    with path.open("wb") as f:
        f.write(content)
    logger.info("Saved %s", path)


def download_file(client: Any, url: str, out_path: Path, checksum: str | None = None) -> Path:
    """Download a file from a URL, save it to a path, and optionally verify its checksum.

    Parameters
    ----------
    client : Any
        HTTP client with a .get(url) method returning a response with .content.
    url : str
        The URL to download the file from.
    out_path : Path
        The path to save the downloaded file.
    checksum : str | None, optional
        Optional SHA256 checksum to verify the downloaded file.

    Returns
    -------
    Path
        The path to the saved file.

    Raises
    ------
    ValueError
        If the checksum does not match.
    """
    logger.info("Downloading %s -> %s", url, out_path)
    resp = client.get(url)
    write_bytes(out_path, resp.content)
    if checksum:
        actual = sha256_file(out_path)
        if actual.lower() != checksum.lower():
            logger.error("Checksum mismatch for %s", out_path)
            raise ValueError(f"checksum mismatch for {out_path}")
    return out_path
