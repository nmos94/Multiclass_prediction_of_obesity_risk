"""Shared library code for the project."""

from pathlib import Path


def project_root() -> Path:
    """
    Return absolute path to repository root.

    Jupyter notebooks can use this helper to resolve paths without
    hard-coding user-specific directories.
    """
    return Path(__file__).resolve().parent.parent


__all__ = ["project_root"]
