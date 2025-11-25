"""Utility helpers shared across notebooks."""

from pathlib import Path
from typing import Dict

import pandas as pd

from . import project_root
from .config import load_yaml


DATA_DIR = project_root() / "data"


def get_data_path(*relative: str) -> Path:
    """
    Resolve paths inside the data directory.

    Usage:
        raw = get_data_path("raw", "dataset.csv")
    """
    return DATA_DIR.joinpath(*relative)


def load_columns_mapping() -> Dict[str, str]:
    """
    Return dictionary that maps canonical column names to readable labels.

    Centralizing this logic avoids duplication across notebooks.
    """
    return load_yaml("columns_mapping.yml")


DEFAULT_RAW_DATASET = "ObesityDataSet.csv"


def load_csv(
    name: str = DEFAULT_RAW_DATASET,
    subdir: str = "processed",
    **kwargs,
) -> pd.DataFrame:
    """
    Read a CSV file located under the data directory.

    Args:
        name: File name, defaults to the main raw dataset.
        subdir: Which subfolder within data to use ("raw", "processed", ...).
        kwargs: Extra keyword arguments forwarded to ``pandas.read_csv``.
    """
    path = get_data_path(subdir, name)
    return pd.read_csv(path, **kwargs)


__all__ = [
    "get_data_path",
    "load_columns_mapping",
    "load_csv",
    "DATA_DIR",
    "DEFAULT_RAW_DATASET",
]
