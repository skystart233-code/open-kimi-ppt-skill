# Vendored Open-PPTD runtime

- Source: https://github.com/Shingwha/open-pptd
- Pinned commit: `d7ee121a0c07538fad39c1d67a5e3ecfae56a116`
- Imported: 2026-08-27
- Included paths: `editor/`, `lib/`, `bin/`, `assets/`, and `package.json`
- Purpose: local PPTD editing, rendering, and PPTX export without a hosted-editor dependency

Local compatibility patches:

- page-background images are included in the editor's preload, persistence, and package-export image map;
- the renderer resolves page-background image paths through that image map, matching normal image elements.
- historical third-party brand references in comments were replaced with neutral interoperability wording; runtime behavior is unchanged.

The upstream `README.md` and `package.json` declare the project as MIT-licensed.
The pinned source revision did not include a standalone `LICENSE` file, so this
fork records the upstream declaration and source revision explicitly.
