"""Main entry point for fetch_bib - delegates to paperkit CLI."""

from .paperkit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())

__all__ = ["main"]
