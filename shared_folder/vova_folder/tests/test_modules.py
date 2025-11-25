"""Smoke tests that ensure every Python module under ``src`` executes."""

from __future__ import annotations

import runpy
import unittest
from typing import List

from src import project_root


def _collect_modules() -> List[str]:
    src_dir = project_root() / "src"
    modules: List[str] = []
    for path in src_dir.glob("*.py"):
        if path.name == "__init__.py":
            continue
        modules.append(f"src.{path.stem}")
    return sorted(modules)


class TestModuleExecution(unittest.TestCase):
    def test_every_module_runs(self) -> None:
        modules = _collect_modules()
        self.assertTrue(
            modules,
            "В каталоге src не найдено ни одного python-модуля для тестирования.",
        )
        for module_name in modules:
            with self.subTest(module=module_name):
                runpy.run_module(module_name, run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    unittest.main()
