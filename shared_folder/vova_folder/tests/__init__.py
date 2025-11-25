"""Tests for the ``slutskiy_v`` profile.

Because ``python -m unittest`` ignores `.env`, we replicate the notebook
PYTHONPATH configuration here so ``import src`` keeps working.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROFILE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROFILE_ROOT.parents[1]
_extra_paths = [PROFILE_ROOT, REPO_ROOT]

for extra_path in _extra_paths:
    as_str = str(extra_path)
    if as_str not in sys.path:
        sys.path.insert(0, as_str)

current_env = os.environ.get('PYTHONPATH')
joined_extra = ':'.join(str(p) for p in _extra_paths)
if current_env:
    if joined_extra not in current_env:
        os.environ['PYTHONPATH'] = f"{joined_extra}:{current_env}"
else:
    os.environ['PYTHONPATH'] = joined_extra
