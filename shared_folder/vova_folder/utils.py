"""Utility helpers shared across notebooks."""

from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import yaml


def project_root() -> Path:
    """Return absolute path to the project root (current file directory)."""
    return Path(__file__).resolve().parent


def load_yaml(path: Path | str) -> Dict[str, Any]:
    """Read a YAML file located relative to the project root."""
    target = project_root() / Path(path)
    with target.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


DATA_DIR = project_root()


def get_data_path(*relative: str) -> Path:
    """
    Resolve paths relative to the project directory.

    Usage:
        raw = get_data_path("dataset.csv")
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
    subdir: str = "",
    **kwargs,
) -> pd.DataFrame:
    """
    Read a CSV file located in the project folder (optionally within a subfolder).

    Args:
        name: File name, defaults to the main dataset.
        subdir: Optional subfolder within the project root.
        kwargs: Extra keyword arguments forwarded to ``pandas.read_csv``.
    """
    path = get_data_path(subdir, name)
    return pd.read_csv(path, **kwargs)


def _rename_columns(df: pd.DataFrame, column_names: Optional[str]) -> pd.DataFrame:
    """
    Rename columns using mapping from YAML.

    If ``column_names`` is None — no переименование.
    If строка — берётся значение по этому ключу из маппинга (например,
    ``short_ru``, ``description_ru``, ``description_en`` или любой новый
    ключ, который появится в YAML).
    """
    if column_names is None:
        return df

    mapping = load_columns_mapping()
    rename_map = {}
    for col, meta in mapping.items():
        if isinstance(meta, dict):
            rename_map[col] = meta.get(column_names, col)
    # Если в df есть колонки, отсутствующие в маппинге, оставляем их как есть.
    rename_map.update({col: col for col in df.columns if col not in rename_map})
    return df.rename(columns=rename_map)


def load_raw_df(column_names: Optional[str] = None) -> pd.DataFrame:
    """
    Load the raw obesity dataset stored directly in the project directory.

    Args:
        column_names: optional renaming scheme: "short_names", "long_names", or None.
    """
    df = load_csv(name=DEFAULT_RAW_DATASET, subdir="")
    return _rename_columns(df, column_names)


def load_clean_df(
    column_names: Optional[str] = None,
) -> pd.DataFrame:
    """
    Load and clean the raw dataset by removing duplicate rows and
    resetting the index. Adds укрупнённую целевую переменную
    ``NObeyesdad_norm`` согласно маппингу в columns_mapping.yml.
    Returns a fresh DataFrame.

    Args:
        column_names: optional renaming scheme: "short_names", "long_names", or None.
    """
    # Всегда работаем с исходными именами колонок, затем переименовываем в конце.
    df = load_raw_df(column_names=None)
    df = df.drop_duplicates().reset_index(drop=True)

    # Добавляем агрегированную целевую переменную, если есть маппинг.
    mapping = load_columns_mapping()
    norm_mapping = mapping.get("NObeyesdad_norm", {}).get("mapping", {})
    if "NObeyesdad" in df.columns and norm_mapping:
        df["NObeyesdad_norm"] = df["NObeyesdad"].map(norm_mapping)

    # Добавляем индекс массы тела (BMI), если доступны вес и рост.
    if {"Weight", "Height"}.issubset(df.columns):
        height_sq = pd.to_numeric(df["Height"], errors="coerce") ** 2
        weight = pd.to_numeric(df["Weight"], errors="coerce")
        df["BMI"] = weight / height_sq
        df["BMI"] = df["BMI"].replace([float("inf"), -float("inf")], pd.NA)

    # Переименовываем колонки согласно маппингу, если указана схема.
    df = _rename_columns(df, column_names)

    return df


__all__ = [
    "project_root",
    "load_yaml",
    "get_data_path",
    "load_columns_mapping",
    "load_csv",
    "DATA_DIR",
    "DEFAULT_RAW_DATASET",
    "load_raw_df",
    "load_clean_df",
]
