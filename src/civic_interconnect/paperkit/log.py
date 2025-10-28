"""Logging utilities for the civic_interconnect.paperkit module.

Provides a library-wide logger and optional configuration for console output.

File: src/civic_interconnect/paperkit/log.py
"""

# src/civic_interconnect/paperkit/log.py
import logging

# Library-wide logger
logger = logging.getLogger("civic_interconnect.paperkit")


def configure(level: str = "INFO") -> None:
    """Configure basic console output for logging.

    Only used by the CLI or by applications that explicitly opt in.
    """
    level = level.upper()
    # If root already has handlers, do not reconfigure.
    if logging.getLogger().handlers:
        logging.getLogger().setLevel(getattr(logging, level, logging.INFO))
        return

    fmt = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
    logging.basicConfig(level=getattr(logging, level, logging.INFO), format=fmt)
