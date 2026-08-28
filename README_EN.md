# PPTD Studio Skill

[简体中文](README.md) | [English](README_EN.md)

A local-first presentation toolchain for AI coding agents. It uses readable,
versionable PPTD v2 projects, provides browser-based editing and visual QA,
and exports PPTX files whose text, shapes, images, and charts remain editable.

> [!IMPORTANT]
> PPTD Studio Skill is an independently maintained open-source derivative. It
> is not an official product of Kimi, Moonshot AI, Open-PPTD, Microsoft, or any
> other vendor. Provenance, modifications, and redistributed licenses are
> documented here and in [NOTICE](NOTICE).

## Capabilities

- Create, edit, replicate, and inspect PPTD/PPTX presentations with an agent.
- Deliver both the complete PPTD project and a matching PPTX by default.
- Edit PPTD locally in a browser and save changes back to the project folder.
- Export editable text, shapes, images, charts, and fade slide transitions.
- Render every page and stitch an overview image for multimodal visual QA.
- Reuse the legacy design-system references inherited from the predecessor;
  they continue to generate standard PPTD v2.

## Editor migration

Since 2.0.0, the project no longer loads the Kimi web editor or Moonshot static
assets. Editing, rendering, and PPTX writing use a bundled, pinned
[Open-PPTD](https://github.com/Shingwha/open-pptd) runtime.

This integration adds:

1. a loopback-only editor served by `pptd-studio-skill serve`;
2. local OOXML export without browser-driven downloads;
3. local headless rendering for visual QA;
4. complete page-background image preload, persistence, preview, and package
   export mapping;
5. ZIP, slide-count, and transition-structure checks for generated PPTX files.

### Legacy template compatibility

| Content | Status |
| --- | --- |
| PPTD v2 manifest, pages, themes, and layouts | Supported |
| Text, shapes, images, backgrounds, tables, and charts | Supported |
| Predecessor design-system references | Supported; they generate PPTD v2 |
| Unknown PPTD fields | Preserved during edit/save |
| Slide-level fade transitions | Supported |
| Kimi-specific on-slide element animations | Metadata preserved; not played or exported by Open-PPTD |

The practical boundary is the proprietary animation executor, not ordinary
template layout. Keep the metadata when needed and disclose that the current
PPTX export contains the static slide state.

## Requirements

- Node.js 18+;
- Python 3 for the export helper scripts;
- Chrome or Edge only for interactive editing and image rendering;
- Pillow for the QA overview; the helper attempts installation when missing;
- font files are optional: available files can be embedded, otherwise Office
  applications fall back to installed fonts.

## Install

The current release is installed from GitHub. This README does not claim that
the renamed npm package has already been published.

```bash
# Install non-interactively into ~/.agents/skills/pptd-studio
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz install -y

# Install into one or more agent skill directories
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz install \
  --target ~/.codex/skills \
  --target ~/.claude/skills

# Install into every detected agent directory
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz install --all
```

Or run from source:

```bash
git clone https://github.com/skystart233-code/pptd-studio-skill.git
cd pptd-studio-skill
node bin/pptd-studio-skill.js install -y
```

Re-running installation atomically updates the `pptd-studio` directory and
does not modify presentations you already created.

### Migrating from 1.x

Version 2.0.0 renames the skill directory from `open-kimi-ppt` to
`pptd-studio`. After installing and verifying the new version, remove the old
directory to prevent duplicate skill discovery. The installer intentionally
does not delete that directory without user action.

## Quick start

After installation, describe the content, page count, and visual direction:

```text
Use pptd-studio to create a 10-slide product-launch deck with a dark technical
style and image backgrounds. Deliver both the editable PPTD project and PPTX,
and perform visual QA before export.
```

### Start the local editor

```bash
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz serve --open
```

Or, from a source checkout:

```bash
node bin/pptd-studio-skill.js serve --open
```

The default URL is <http://127.0.0.1:55173/editor/>. In Chrome or Edge, select
the complete folder containing `.pptd`, `pages/`, and `media/`. Writable folder
access is granted only after the user chooses the directory.

### Export directly

```bash
python ~/.agents/skills/pptd-studio/scripts/export_pptx.py \
  /path/to/deck.pptd --output /path/to/deck.pptx

python ~/.agents/skills/pptd-studio/scripts/export_images.py \
  /path/to/deck.pptd --output /path/to/qa-images
```

On Windows, use `python` or `py` and the corresponding `%USERPROFILE%` path.

## PPTD project layout

```text
deck/
├── deck.pptd
├── pages/
│   ├── 01-cover.page
│   └── 02-content.page
└── media/
    └── hero.jpg
```

PPTD is a YAML-based presentation DSL. See the
[PPTD reference](skills/pptd-studio/reference/pptd.md) and
[theme index](theme_EN.md).

## Development and verification

```bash
npm test
python -m unittest discover -s skills/pptd-studio/tests -p "test_*.py" -v
npm run pack:check
```

Renderer or writer changes should also be checked using a real multi-page
project, including the visual overview and the PPTX ZIP structure. See
[CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and
[CHANGELOG_EN.md](CHANGELOG_EN.md).

## Security and privacy

- The server listens on `127.0.0.1` by default.
- PPTD parsing, editing, and PPTX conversion run locally.
- A deck may still fetch remote image or font URLs it explicitly references.
- Treat external PPTD, PPTX, fonts, and media as untrusted input.
- The project does not provide or inject Kimi login tokens.

## Open-source provenance and licenses

PPTD Studio Skill is distributed under the [MIT License](LICENSE). It is a
derivative project: original copyright notices are preserved and third-party
code is not represented as original work of this project.

- Predecessor: [acnlie/open-kimi-ppt-skill](https://github.com/acnlie/open-kimi-ppt-skill), MIT;
- bundled runtime: [Shingwha/open-pptd](https://github.com/Shingwha/open-pptd),
  with the pinned revision and modifications recorded in
  [UPSTREAM.md](skills/pptd-studio/vendor/open-pptd/UPSTREAM.md);
- redistributed ECharts, js-yaml, KaTeX, Bootstrap Icons, and d3 material is
  listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSES](LICENSES/);
- Kimi, Kimi Slides, Moonshot AI, Open-PPTD, PowerPoint, WPS, Keynote, and
  other names and marks belong to their respective owners and are used only to
  identify provenance or compatibility, not affiliation or endorsement.

Keep `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, and `LICENSES/` with any
redistribution.
