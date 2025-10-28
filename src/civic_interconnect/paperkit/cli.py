"""Command-line interface for the paperkit tool.

This module provides the main CLI entry point for fetching public data
for bibliography references, including argument parsing and orchestration
of the fetch process.

File: src/civic_interconnect/paperkit/cli.py
"""

import argparse
from pathlib import Path

import requests

from .http_client import HttpClient
from .log import configure, logger
from .orchestrate import DEFAULT_OUTPUT_ROOT, run


def main() -> int:
    """Run the paperkit CLI."""
    ap = argparse.ArgumentParser(description="Fetch public data for .bib references")
    ap.add_argument("--bib", type=Path, default=Path("paper/refs.bib"))
    ap.add_argument("--meta", type=Path, default=Path("paper/refs_meta.yaml"))
    ap.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_ROOT)
    ap.add_argument("--log-level", type=str, default="INFO", help="DEBUG, INFO, WARNING, ERROR")
    args = ap.parse_args()

    configure(args.log_level)
    logger.info("Starting paperkit fetch with bib=%s meta=%s out=%s", args.bib, args.meta, args.out)

    client: HttpClient = HttpClient(session=requests.Session())
    summary = run(args.bib, args.meta, args.out, client)

    for rec in summary.processed:
        for p in rec.paths:
            logger.info("[%s] saved %s", rec.bibkey, p)
        for e in rec.errors:
            logger.error("[%s] ERROR %s", rec.bibkey, e)
    return 0
