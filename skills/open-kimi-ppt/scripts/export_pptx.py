#!/usr/bin/env python3
"""Export PPTD to PPTX with the bundled Open-PPTD writer.

The export is local and does not load Kimi or Moonshot web resources. The
bundled writer understands PPTD v2 and preserves unsupported metadata when a
project is edited. Kimi-specific element animations remain in PPTD, but the
Open-PPTD writer currently exports the static slide state only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


SKILL_DIR = Path(__file__).resolve().parent.parent
OPEN_PPTD_ROOT = SKILL_DIR / "vendor" / "open-pptd"
OPEN_PPTD_CLI = OPEN_PPTD_ROOT / "bin" / "open-pptd.js"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
ET.register_namespace("p", P_NS)


class ExportError(RuntimeError):
    """Raised when the local export pipeline cannot produce a valid PPTX."""


def log(message: str) -> None:
    print(f"[open-kimi-ppt] {message}", file=sys.stderr, flush=True)


def find_manifest(source: Path) -> Path:
    source = source.expanduser().resolve()
    if source.is_file():
        if source.suffix.lower() != ".pptd":
            raise ExportError(f"input must be a .pptd file or project directory: {source}")
        return source
    if not source.is_dir():
        raise ExportError(f"input does not exist: {source}")
    manifests = sorted(source.rglob("*.pptd"))
    if not manifests:
        raise ExportError(f"no .pptd manifest found under: {source}")
    if len(manifests) != 1:
        choices = "\n  ".join(str(path) for path in manifests)
        raise ExportError(
            "multiple .pptd manifests found; pass one manifest explicitly:\n  " + choices
        )
    return manifests[0]


def ensure_runtime() -> None:
    if not OPEN_PPTD_CLI.is_file():
        raise ExportError(f"bundled Open-PPTD runtime is incomplete: {OPEN_PPTD_CLI}")
    try:
        process = subprocess.run(
            ["node", "--version"], capture_output=True, encoding="utf-8",
            errors="replace", timeout=20, check=False
        )
    except FileNotFoundError as exc:
        raise ExportError("Node.js 18+ is required for local PPTX export") from exc
    if process.returncode != 0:
        raise ExportError(f"could not run Node.js: {process.stderr.strip()}")
    try:
        major = int(process.stdout.strip().lstrip("v").split(".", 1)[0])
    except (ValueError, IndexError) as exc:
        raise ExportError(f"could not parse Node.js version: {process.stdout.strip()}") from exc
    if major < 18:
        raise ExportError(f"Node.js 18+ is required; found {process.stdout.strip()}")


def run_open_pptd(arguments: Sequence[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    ensure_runtime()
    process = subprocess.run(
        ["node", str(OPEN_PPTD_CLI), *map(str, arguments)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
        cwd=str(OPEN_PPTD_ROOT),
    )
    if process.returncode != 0:
        detail = (process.stderr or process.stdout).strip()
        raise ExportError(f"Open-PPTD failed ({process.returncode}): {detail[-4000:]}")
    return process


def _transition_index(root: ET.Element) -> int:
    index = 0
    for position, child in enumerate(list(root)):
        if child.tag in {f"{{{P_NS}}}cSld", f"{{{P_NS}}}clrMapOvr"}:
            index = position + 1
    return index


def patch_transitions(path: Path, transition: str) -> int:
    """Ensure each slide has one root-level fade transition, or none."""
    if transition not in {"fade", "none"}:
        raise ExportError(f"unsupported transition: {transition}")
    with zipfile.ZipFile(path, "r") as source:
        entries = [(info, source.read(info.filename)) for info in source.infolist()]
    slide_names = {
        info.filename
        for info, _ in entries
        if info.filename.startswith("ppt/slides/slide") and info.filename.endswith(".xml")
    }
    if not slide_names:
        raise ExportError("exported PPTX contains no slide XML")
    rewritten = []
    for info, data in entries:
        if info.filename not in slide_names:
            rewritten.append((info, data))
            continue
        root = ET.fromstring(data)
        for node in list(root.findall(f"{{{P_NS}}}transition")):
            root.remove(node)
        if transition == "fade":
            node = ET.Element(f"{{{P_NS}}}transition", {"spd": "fast", "advClick": "1"})
            ET.SubElement(node, f"{{{P_NS}}}fade")
            root.insert(_transition_index(root), node)
        rewritten.append((info, ET.tostring(root, encoding="utf-8", xml_declaration=True)))
    handle, temp_name = tempfile.mkstemp(prefix="open-pptd-transition-", suffix=".pptx", dir=path.parent)
    os.close(handle)
    temp_path = Path(temp_name)
    try:
        with zipfile.ZipFile(temp_path, "w") as target:
            for info, data in rewritten:
                target.writestr(info, data)
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)
    return len(slide_names)


def verify_output(path: Path, transition: str, embed_fonts: bool) -> Dict[str, Any]:
    if not path.is_file() or path.stat().st_size == 0:
        raise ExportError(f"PPTX was not created: {path}")
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ExportError(f"PPTX ZIP integrity failed at: {bad}")
        names = archive.namelist()
        slides = sorted(
            name for name in names
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        if not slides:
            raise ExportError("PPTX contains no slides")
        for name in slides:
            root = ET.fromstring(archive.read(name))
            nodes = root.findall(f"{{{P_NS}}}transition")
            expected = 1 if transition == "fade" else 0
            if len(nodes) != expected:
                raise ExportError(f"{name} has {len(nodes)} root transitions; expected {expected}")
            if transition == "fade" and nodes[0].find(f"{{{P_NS}}}fade") is None:
                raise ExportError(f"{name} transition is not fade")
        embedded = [name for name in names if name.startswith("ppt/fonts/")]
    return {
        "engine": "open-pptd",
        "slides": len(slides),
        "transition": transition,
        "fontEmbeddingRequested": embed_fonts,
        "embeddedFontParts": len(embedded),
        "zipIntegrity": "ok",
    }


def export_pptx(
    source: Path,
    output: Path,
    transition: str = "fade",
    embed_fonts: bool = True,
    keep_browser_raw: bool = False,
    force: bool = False,
) -> Dict[str, Any]:
    manifest = find_manifest(source)
    output = output.expanduser().resolve()
    if output.exists() and not force:
        raise ExportError(f"output already exists (pass --force): {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="open-pptd-export-") as temp_name:
        raw = Path(temp_name) / "raw.pptx"
        arguments = ["export", str(manifest), "-o", str(raw)]
        if not embed_fonts:
            arguments.append("--no-embed-fonts")
        log(f"exporting with bundled Open-PPTD: {manifest}")
        run_open_pptd(arguments)
        if not raw.is_file():
            raise ExportError("Open-PPTD reported success but produced no PPTX")
        shutil.copy2(raw, output)
        if keep_browser_raw:
            shutil.copy2(raw, output.with_name(f"{output.stem}.open-pptd-raw.pptx"))
    patched = patch_transitions(output, transition)
    summary = verify_output(output, transition, embed_fonts)
    summary["transitionPatchedSlides"] = patched
    summary["output"] = str(output)
    summary["compatibility"] = {
        "kimiTemplates": "supported via PPTD v2",
        "kimiElementAnimations": "preserved in PPTD; not rendered by Open-PPTD",
    }
    return summary


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export PPTD to PPTX with the bundled local Open-PPTD writer."
    )
    parser.add_argument("input", type=Path, help=".pptd manifest or project directory")
    parser.add_argument("--output", "-o", type=Path, help="output .pptx path")
    parser.add_argument(
        "--transition", choices=("fade", "none"), default="fade",
        help="slide transition written to every slide (default: fade)",
    )
    fonts = parser.add_mutually_exclusive_group()
    fonts.add_argument("--embed-fonts", dest="embed_fonts", action="store_true", default=True)
    fonts.add_argument("--no-embed-fonts", dest="embed_fonts", action="store_false")
    parser.add_argument(
        "--keep-browser-raw", action="store_true",
        help="compatibility alias: keep the unpatched Open-PPTD output",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        manifest = find_manifest(args.input)
        output = args.output or manifest.with_suffix(".pptx")
        summary = export_pptx(
            args.input, output, args.transition, args.embed_fonts,
            args.keep_browser_raw, args.force,
        )
    except (ExportError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print(f"open-kimi-ppt export failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
