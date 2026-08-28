import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(".");
const metadata = JSON.parse(readFileSync(resolve(root, "package.json"), "utf8"));

test("publishes under the renamed project identity", () => {
  assert.equal(metadata.name, "pptd-studio-skill");
  assert.equal(metadata.version, "2.0.1");
  assert.equal(metadata.bin["pptd-studio-skill"], "bin/pptd-studio-skill.js");
  assert.match(metadata.repository.url, /skystart233-code\/pptd-studio-skill/);
  assert.equal(metadata.keywords.includes("kimi"), false);
});

test("keeps source and redistributed license material in the project", () => {
  for (const path of [
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_NOTICES.md",
    "TRADEMARKS.md",
    "RIGHTS_POLICY.md",
    "PROVENANCE.md",
    "LICENSES/Apache-2.0.txt",
    "LICENSES/BSD-3-Clause-d3.txt",
    "skills/pptd-studio/LICENSE.txt",
    "skills/pptd-studio/NOTICE",
    "skills/pptd-studio/TRADEMARKS.md",
    "skills/pptd-studio/RIGHTS_POLICY.md",
    "skills/pptd-studio/vendor/open-pptd/THIRD_PARTY_NOTICES.md",
    "skills/pptd-studio/vendor/open-pptd/LICENSES/MIT-KaTeX.txt",
  ]) {
    assert.equal(existsSync(resolve(root, path)), true, path);
  }
});

test("retains bundled presets and historical examples", () => {
  const designRoot = resolve(root, "skills/pptd-studio/reference/design_system");
  assert.equal(
    existsSync(resolve(designRoot, "consulting/pine-green-strategy/design.md")),
    true,
  );
  assert.equal(existsSync(resolve(root, "docs/images/editor-overview.png")), true);
  assert.equal(existsSync(resolve(root, "example/dji-pocket4/dji-pocket4.pptd")), true);
});
