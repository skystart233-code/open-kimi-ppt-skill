from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
SPEC = importlib.util.spec_from_file_location("export_images", SCRIPTS_DIR / "export_images.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal" / "minimal.pptd"


class ExportImagesTests(unittest.TestCase):
    def test_page_sort_key_uses_trailing_page_number(self) -> None:
        paths = [Path("deck-10.png"), Path("deck-2.png"), Path("deck-01.png")]
        self.assertEqual(
            [path.name for path in sorted(paths, key=MODULE.page_sort_key)],
            ["deck-01.png", "deck-2.png", "deck-10.png"],
        )

    def test_rendered_pages_are_stitched_and_mapped(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is unavailable")

        def fake_render(arguments, timeout=0):
            del timeout
            pages = Path(arguments[arguments.index("-o") + 1])
            Image.new("RGB", (960, 540), "white").save(pages / "minimal-01.png")

        with tempfile.TemporaryDirectory() as temp_name:
            output = Path(temp_name) / "qa"
            with patch.object(MODULE, "run_open_pptd", side_effect=fake_render):
                summary = MODULE.export_images(FIXTURE, output)
            self.assertEqual(summary["engine"], "open-pptd")
            self.assertEqual(summary["pages"], 1)
            self.assertTrue((output / "overview.jpg").is_file())
            self.assertEqual(summary["images"][0]["page"], "pages/01.page")


if __name__ == "__main__":
    unittest.main()
