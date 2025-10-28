"""Test that the project structure works correctly.

Module Information:
    - Filename: test_smoke.py
    - Module: test_smoke
    - Location: tests/

This smoke test verifies that:
    - All modules can be imported
    - Basic project structure is intact
"""

from civic_interconnect import main, utils_logger


def test_imports_work():
    """Verify all modules can be imported."""
    # If we get here without ImportError, imports work
    assert utils_logger is not None
    assert main is not None
