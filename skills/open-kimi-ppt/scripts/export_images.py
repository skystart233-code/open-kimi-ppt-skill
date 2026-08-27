#!/usr/bin/env python3
"""Render PPTD pages with the bundled Open-PPTD renderer for visual QA."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from export_pptx import ExportError, find_manifest, log, run_open_pptd


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
OVERVIEW_COLUMNS = 3
OVERVIEW_THUMB_WIDTH = 640
OVERVIEW_LABEL_HEIGHT = 32
OVERVIEW_GAP = 12


def ensure_pillow() -> Tuple[Any, Any, Any]:
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        log("Pillow is required for stitching; installing pillow with pip --user")
        process = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "pillow"],
            capture_output=True, encoding="utf-8", errors="replace", timeout=300, check=False,
        )
        if process.returncode != 0:
            raise ExportError(f"failed to install Pillow: {process.stderr[-2000:]}")
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont


def page_sort_key(path: Path) -> Tuple[int, str]:
    match = re.search(r"(\d+)(?=\.[^.]+$)", path.name)
    return (int(match.group(1)) if match else sys.maxsize, path.name)


def label_font(image_font: Any) -> Any:
    try:
        return image_font.load_default(size=18)
    except TypeError:
        return image_font.load_default()


def stitch_overview(
    images: Sequence[Path], output: Path, image_cls: Any, draw_cls: Any, image_font: Any
) -> Path:
    if not images:
        raise ExportError("Open-PPTD rendered no page images")
    thumbs: List[Tuple[str, Any]] = []
    for index, path in enumerate(images, start=1):
        with image_cls.open(path) as opened:
            frame = opened.convert("RGB")
            ratio = OVERVIEW_THUMB_WIDTH / frame.width
            thumb = frame.resize((OVERVIEW_THUMB_WIDTH, max(1, round(frame.height * ratio))))
        thumbs.append((f"P{index}", thumb))
    rows = math.ceil(len(thumbs) / OVERVIEW_COLUMNS)
    cell_height = OVERVIEW_LABEL_HEIGHT + max(thumb.height for _, thumb in thumbs)
    width = OVERVIEW_COLUMNS * OVERVIEW_THUMB_WIDTH + (OVERVIEW_COLUMNS + 1) * OVERVIEW_GAP
    height = rows * cell_height + (rows + 1) * OVERVIEW_GAP
    overview = image_cls.new("RGB", (width, height), "#e5e7eb")
    draw = draw_cls.Draw(overview)
    font = label_font(image_font)
    for position, (label, thumb) in enumerate(thumbs):
        column = position % OVERVIEW_COLUMNS
        row = position // OVERVIEW_COLUMNS
        x = OVERVIEW_GAP + column * (OVERVIEW_THUMB_WIDTH + OVERVIEW_GAP)
        y = OVERVIEW_GAP + row * (cell_height + OVERVIEW_GAP)
        draw.rectangle(
            (x, y, x + OVERVIEW_THUMB_WIDTH, y + OVERVIEW_LABEL_HEIGHT - 4), fill="#111827"
        )
        draw.text((x + 8, y + 5), label, fill="#ffffff", font=font)
        overview.paste(thumb, (x, y + OVERVIEW_LABEL_HEIGHT))
    overview.save(output, "JPEG", quality=85)
    return output


def manifest_page_paths(manifest: Path) -> List[str]:
    try:
        import yaml
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        return [str(item) for item in data.get("pages", [])]
    except Exception:
        return []


def export_images(
    source: Path, output: Path, keep_download: bool = False, force: bool = False
) -> Dict[str, Any]:
    del keep_download  # retained for CLI compatibility; rendered pages are always kept
    manifest = find_manifest(source)
    output = output.expanduser().resolve()
    if output.exists():
        if not force:
            raise ExportError(f"output already exists (pass --force): {output}")
        if output.is_dir():
            shutil.rmtree(output)
        else:
            output.unlink()
    pages_dir = output / "pages"
    pages_dir.mkdir(parents=True)
    image_cls, draw_cls, image_font = ensure_pillow()
    log(f"rendering with bundled Open-PPTD: {manifest}")
    run_open_pptd(
        ["render", str(manifest), "-o", str(pages_dir), "--page", "all", "--scale", "1"],
        timeout=600,
    )
    images = sorted(
        [path for path in pages_dir.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES],
        key=page_sort_key,
    )
    overview = stitch_overview(images, output / "overview.jpg", image_cls, draw_cls, image_font)
    page_paths = manifest_page_paths(manifest)
    mapping = [
        {
            "index": index,
            "image": f"pages/{path.name}",
            "page": page_paths[index - 1] if index - 1 < len(page_paths) else None,
        }
        for index, path in enumerate(images, start=1)
    ]
    return {
        "engine": "open-pptd",
        "pages": len(images),
        "overview": str(overview),
        "output": str(output),
        "images": mapping,
    }


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render PPTD pages with bundled Open-PPTD and stitch a QA overview."
    )
    parser.add_argument("input", type=Path, help=".pptd manifest or project directory")
    parser.add_argument(
        "--output", "-o", type=Path,
        help="output directory (default: <project>/.qa-images)",
    )
    parser.add_argument(
        "--keep-browser-raw", action="store_true",
        help="compatibility alias; rendered pages are already kept",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing output directory")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        manifest = find_manifest(args.input)
        output = args.output or manifest.parent / ".qa-images"
        summary = export_images(args.input, output, args.keep_browser_raw, args.force)
    except (ExportError, OSError, subprocess.SubprocessError) as exc:
        print(f"open-kimi-ppt image export failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
