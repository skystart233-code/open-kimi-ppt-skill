# Third-party notices for the bundled Open-PPTD runtime

## Open-PPTD

Copyright (c) Open-PPTD contributors.

Source: https://github.com/Shingwha/open-pptd
Pinned revision: `d7ee121a0c07538fad39c1d67a5e3ecfae56a116`
License declared by upstream: MIT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Runtime dependencies and assets

| Component | Redistributed path | License file |
| --- | --- | --- |
| Apache ECharts | `editor/vendor/echarts.mjs` | `LICENSES/Apache-2.0.txt`, `LICENSES/NOTICE-Apache-ECharts.txt` |
| d3-derived ECharts portions | included in the ECharts bundle | `LICENSES/BSD-3-Clause-d3.txt` |
| js-yaml 4.1.0 | `editor/vendor/js-yaml.mjs` | `LICENSES/MIT-js-yaml.txt` |
| KaTeX | `editor/vendor/katex.mjs` | `LICENSES/MIT-KaTeX.txt` |
| Bootstrap Icons | `assets/icons/*.svg` | `LICENSES/MIT-Bootstrap-Icons.txt` |

The ECharts bundle retains its upstream Apache and embedded Microsoft helper
license headers. Preserve those headers and this notice when redistributing
the runtime.
