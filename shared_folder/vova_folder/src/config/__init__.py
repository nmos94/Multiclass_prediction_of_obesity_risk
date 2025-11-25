"""Configuration helpers (column mappings, constants, etc.)."""

from pathlib import Path
from typing import Any, Dict

import yaml

CONFIG_DIR = Path(__file__).resolve().parent


def load_yaml(name: str) -> Dict[str, Any]:
    """
    Load YAML configuration by file name relative to the config directory.

    Example:
        columns = load_yaml("columns_mapping.yml")
    """
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


__all__ = ["load_yaml", "CONFIG_DIR"]
