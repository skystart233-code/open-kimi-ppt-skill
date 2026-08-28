# Third-party notices

This file records software and inherited material redistributed by PPTD Studio
Skill. It is informational and does not replace the applicable license texts.

| Component | Included material | License | Source / license |
| --- | --- | --- | --- |
| Predecessor project | Skill workflow, PPTD and slide-design references, and project history | MIT | [source repository](https://github.com/acnlie/open-kimi-ppt-skill), root [LICENSE](LICENSE) |
| Open-PPTD | Bundled editor, renderer, CLI, and OOXML writer, pinned at `d7ee121a0c07538fad39c1d67a5e3ecfae56a116` and locally patched | MIT as declared by upstream | [Shingwha/open-pptd](https://github.com/Shingwha/open-pptd), [vendored notice](skills/pptd-studio/vendor/open-pptd/THIRD_PARTY_NOTICES.md) |
| Apache ECharts | `editor/vendor/echarts.mjs` | Apache-2.0; bundled d3-derived portions are BSD-3-Clause | [Apache ECharts](https://github.com/apache/echarts), [Apache-2.0](LICENSES/Apache-2.0.txt), [ECharts NOTICE](LICENSES/NOTICE-Apache-ECharts.txt), [d3 license](LICENSES/BSD-3-Clause-d3.txt) |
| js-yaml 4.1.0 | `editor/vendor/js-yaml.mjs` | MIT | [nodeca/js-yaml](https://github.com/nodeca/js-yaml), [license](LICENSES/MIT-js-yaml.txt) |
| KaTeX | `editor/vendor/katex.mjs` | MIT | [KaTeX/KaTeX](https://github.com/KaTeX/KaTeX), [license](LICENSES/MIT-KaTeX.txt) |
| Bootstrap Icons | `assets/icons/*.svg` | MIT | [twbs/icons](https://github.com/twbs/icons), [license](LICENSES/MIT-Bootstrap-Icons.txt) |

The ECharts bundle retains its upstream license header, including embedded
notices for Microsoft helper code. The original headers in vendored JavaScript
and SVG files must not be removed when redistributing modified copies.

No trademark license is granted. See [TRADEMARKS.md](TRADEMARKS.md).
