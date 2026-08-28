from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "export_pptx.py"
SPEC = importlib.util.spec_from_file_location("export_pptx", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal" / "minimal.pptd"


class ExportPptxTests(unittest.TestCase):
    def test_open_pptd_export_produces_valid_fade_pptx(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            output = Path(temp_name) / "deck.pptx"
            summary = MODULE.export_pptx(
                FIXTURE, output, transition="fade", embed_fonts=False
            )
            self.assertEqual(summary["engine"], "open-pptd")
            self.assertEqual(summary["slides"], 1)
            self.assertEqual(summary["zipIntegrity"], "ok")
            self.assertTrue(output.is_file())
            with zipfile.ZipFile(output) as archive:
                self.assertIsNone(archive.testzip())

    def test_transition_none_removes_root_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            output = Path(temp_name) / "deck.pptx"
            summary = MODULE.export_pptx(
                FIXTURE, output, transition="none", embed_fonts=False
            )
            self.assertEqual(summary["transition"], "none")
            self.assertEqual(summary["slides"], 1)

    def test_existing_output_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            output = Path(temp_name) / "deck.pptx"
            output.write_bytes(b"existing")
            with self.assertRaisesRegex(MODULE.ExportError, "already exists"):
                MODULE.export_pptx(FIXTURE, output, embed_fonts=False)


if __name__ == "__main__":
    unittest.main()
