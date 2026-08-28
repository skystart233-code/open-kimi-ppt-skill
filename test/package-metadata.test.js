import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(".");
const metadata = JSON.parse(readFileSync(resolve(root, "package.json"), "utf8"));

test("publishes under the renamed project identity", () => {
  assert.equal(metadata.name, "pptd-studio-skill");
  assert.equal(metadata.version, "2.0.0");
  assert.equal(metadata.bin["pptd-studio-skill"], "bin/pptd-studio-skill.js");
  assert.match(metadata.repository.url, /skystart233-code\/pptd-studio-skill/);
  assert.equal(metadata.keywords.includes("kimi"), false);
});

test("keeps source and redistributed license material in the project", () => {
  for (const path of [
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_NOTICES.md",
    "LICENSES/Apache-2.0.txt",
    "LICENSES/BSD-3-Clause-d3.txt",
    "skills/pptd-studio/LICENSE.txt",
    "skills/pptd-studio/NOTICE",
    "skills/pptd-studio/vendor/open-pptd/THIRD_PARTY_NOTICES.md",
    "skills/pptd-studio/vendor/open-pptd/LICENSES/MIT-KaTeX.txt",
  ]) {
    assert.equal(existsSync(resolve(root, path)), true, path);
  }
});
