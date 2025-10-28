"""Bibliography handling utilities for the paper kit.

This module provides functionality for loading and processing BibTeX files:
- BibEntry: TypedDict for bibliography entries
- BibDatabaseLike: Protocol for bibliography database objects
- load_bib_keys: Function to extract citation keys from BibTeX files

File: src/civic_interconnect/paperkit/bib.py

"""

from pathlib import Path
from typing import Protocol, TypedDict

import bibtexparser  # pyright: ignore[reportMissingTypeStubs]

from .log import logger


class BibEntry(TypedDict, total=False):
    """A bibliography entry from a BibTeX file.

    Attributes
    ----------
    ID : str
        The citation key/identifier for the bibliography entry.
    """

    ID: str


class BibDatabaseLike(Protocol):
    """Protocol for bibliography database objects.

    This protocol defines the interface for bibliography database objects
    that contain a list of bibliography entries and support attribute access.

    Attributes
    ----------
    entries : List[BibEntry]
        A list of bibliography entries from the database.

    Methods
    -------
    __getattr__(name: str) -> object
        Provide access to additional attributes on the database object.
    """

    entries: list[BibEntry]

    def __getattr__(self, name: str) -> object:
        """Provide access to additional attributes on the database object."""
        ...


def load_bib_keys(bib_path: Path) -> list[str]:
    """Load citation keys from a BibTeX file."""
    with bib_path.open("r", encoding="utf-8") as f:
        db_raw: BibDatabaseLike = bibtexparser.load(f)  # type: ignore[assignment]

    entries: list[BibEntry] = db_raw.entries
    keys: list[str] = [e["ID"] for e in entries if "ID" in e]

    logger.debug("Loaded %d keys from %s", len(keys), bib_path)
    return keys
