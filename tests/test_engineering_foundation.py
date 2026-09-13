from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from humanizer_support.catalog import pattern_ids, skill_version

ROOT = Path(__file__).resolve().parents[1]


def load_package_release():
    spec = importlib.util.spec_from_file_location(
        "package_release",
        ROOT / "scripts" / "package-release.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EngineeringFoundationTests(unittest.TestCase):
    def test_version_is_derived_from_skill(self) -> None:
        self.assertEqual(skill_version(ROOT), "1.1.0")

    def test_pattern_catalog_is_contiguous_without_fixed_maximum(self) -> None:
        ids = pattern_ids(ROOT)
        self.assertEqual(ids, list(range(1, len(ids) + 1)))
        self.assertGreaterEqual(len(ids), 36)

    def test_machine_readable_contracts_exist(self) -> None:
        expected = {
            "audit-response.schema.json",
            "eval-corpus.schema.json",
            "rewrite-response.schema.json",
        }
        found = {path.name for path in (ROOT / "contracts").glob("*.schema.json")}
        self.assertEqual(found, expected)
        for name in expected:
            data = json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))
            self.assertEqual(
                data["$schema"],
                "https://json-schema.org/draft/2020-12/schema",
            )
            self.assertTrue(
                data["$id"].startswith(
                    "https://blackspirits.dev/humanizer-pt-pt/contracts/"
                )
            )

    def test_release_uses_explicit_allowlist(self) -> None:
        module = load_package_release()
        self.assertIn("contracts", module.RELEASE_ENTRIES)
        self.assertIn("humanizer_support", module.RELEASE_ENTRIES)
        self.assertIn("docs", module.RELEASE_ENTRIES)

        old_root = module.ROOT
        old_entries = module.RELEASE_ENTRIES
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "SKILL.md").write_text("demo", encoding="utf-8")
                (root / "private-notes.txt").write_text("secret", encoding="utf-8")
                module.ROOT = root
                module.RELEASE_ENTRIES = {"SKILL.md"}
                files = module.iter_files()
                self.assertEqual(
                    [path.relative_to(root).as_posix() for path in files],
                    ["SKILL.md"],
                )
        finally:
            module.ROOT = old_root
            module.RELEASE_ENTRIES = old_entries


if __name__ == "__main__":
    unittest.main()
