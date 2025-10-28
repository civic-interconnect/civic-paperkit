"""Configuration module for paper kit metadata handling.

This module provides:
- TypedDict definitions for asset and metadata configuration
- Functions to load and normalize metadata from YAML files
- Default file extension configurations for allowed assets

File: src/civic_interconnect/paperkit/config.py
"""

from pathlib import Path
from typing import Any, NotRequired, TypedDict, cast

import yaml

from .log import logger

DEFAULT_ALLOWED_EXTS: list[str] = [".csv", ".xlsx", ".xls", ".zip", ".tsv", ".json", ".xml", ".pdf"]


class DirectAssetTD(TypedDict, total=False):
    """TypedDict for direct asset configuration.

    Attributes
    ----------
    url : str
        The URL of the asset.
    filename : NotRequired[str]
        Optional filename for the asset.
    checksum : NotRequired[str]
        Optional checksum for the asset.
    """

    url: str
    filename: NotRequired[str]
    checksum: NotRequired[str]


class PageAssetTD(TypedDict, total=False):
    """TypedDict for page-based asset configuration.

    Attributes
    ----------
    page_url : str
        The URL of the page to scrape for assets.
    allow_ext : NotRequired[list[str]]
        Optional list of allowed file extensions.
    href_regex : NotRequired[str]
        Optional regex pattern to match href attributes.
    limit : NotRequired[int]
        Optional limit on number of assets to collect.
    base_url : NotRequired[str]
        Optional base URL for relative links.
    """

    page_url: str
    allow_ext: NotRequired[list[str]]
    href_regex: NotRequired[str]
    limit: NotRequired[int]
    base_url: NotRequired[str]


AssetTD = DirectAssetTD | PageAssetTD


class EntryMetaTD(TypedDict, total=False):
    """TypedDict for entry metadata configuration.

    Attributes
    ----------
    notes : NotRequired[str]
        Optional notes about the entry.
    out_dir : NotRequired[str]
        Optional output directory for the entry.
    assets : NotRequired[list[AssetTD]]
        Optional list of assets associated with the entry.
    """

    notes: NotRequired[str]
    out_dir: NotRequired[str]
    assets: NotRequired[list[AssetTD]]


MetaTD = dict[str, EntryMetaTD]


def _normalize_entry(entry: EntryMetaTD) -> EntryMetaTD:
    # Ensure assets list exists if present and normalize allow_ext
    assets = entry.get("assets")
    if isinstance(assets, list):
        norm_assets: list[AssetTD] = []
        for a in assets:
            # If page_url asset and allow_ext is missing or None, fill defaults
            if ("page_url" in a) and ("allow_ext" not in a or a.get("allow_ext") is None):
                a["allow_ext"] = list(DEFAULT_ALLOWED_EXTS)
            norm_assets.append(a)
        entry["assets"] = norm_assets
    return entry


def load_meta(meta_path: Path) -> MetaTD:
    """Load metadata from a YAML file.

    Parameters
    ----------
    meta_path : Path
        Path to the YAML metadata file.

    Returns
    -------
    MetaTD
        Dictionary containing the loaded and normalized metadata entries.

    Raises
    ------
    ValueError
        If the YAML file does not contain a mapping of bibkeys.
    """
    raw_text = meta_path.read_text(encoding="utf-8")
    loaded: Any = yaml.safe_load(raw_text)
    if loaded is None:
        data: MetaTD = {}
    elif isinstance(loaded, dict):
        data = cast("MetaTD", loaded)
    else:
        raise ValueError("refs_meta.yaml must be a mapping of bibkeys")

    # Normalize each entry
    for key, entry in list(data.items()):
        data[key] = _normalize_entry(entry)

    logger.info("Loaded meta for %d keys from %s", len(data), meta_path)
    return data
