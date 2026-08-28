import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";
import { parseDeck, serializeDeck } from "../skills/pptd-studio/vendor/open-pptd/editor/core/pptd-io.js";
import { mediaFilesOfDeck } from "../skills/pptd-studio/vendor/open-pptd/editor/app/project/images.js";
import { exportDeck } from "../skills/pptd-studio/vendor/open-pptd/lib/pptd-export.js";

test("preserves Kimi-only animation metadata during an Open-PPTD round trip", () => {
  const manifest = `version: v2\ntitle: compatibility\nsize: [960, 540]\npages: [pages/1.page]\n`;
  const page = `pageType: content\nelements:\n  - elementId: title\n    elementType: text\n    bounds: [20, 20, 300, 80]\n    text: Hello\n    animations:\n      - type: fadeIn\n        duration: 0.5\n`;
  const deck = parseDeck(manifest, new Map([["pages/1.page", page]]));
  assert.deepEqual(deck.pages[0].elements[0].extra.animations, [
    { type: "fadeIn", duration: 0.5 },
  ]);
  const files = serializeDeck(deck);
  const savedPage = files.find((entry) => entry.path === "pages/1.page").content;
  assert.match(savedPage, /animations:/);
  assert.match(savedPage, /fadeIn/);
});

test("exports the packaged PPTD fixture with the Open-PPTD writer", async () => {
  const root = resolve("skills/pptd-studio/tests/fixtures/minimal");
  const temp = mkdtempSync(join(tmpdir(), "open-pptd-compat-"));
  const output = join(temp, "minimal.pptx");
  try {
    await exportDeck({ manifest: join(root, "minimal.pptd"), outPath: output, embedFonts: false });
    const bytes = readFileSync(output);
    assert.equal(bytes[0], 0x50);
    assert.equal(bytes[1], 0x4b);
    assert.equal(bytes.includes(Buffer.from("ppt/slides/slide1.xml")), true);
  } finally {
    rmSync(temp, { recursive: true, force: true });
  }
});

test("exports a PPTD page background image into the PPTX package", async () => {
  const root = mkdtempSync(join(tmpdir(), "open-pptd-background-"));
  const output = join(root, "background.pptx");
  mkdirSync(join(root, "pages"), { recursive: true });
  mkdirSync(join(root, "media"), { recursive: true });
  writeFileSync(
    join(root, "deck.pptd"),
    "version: v2\ntitle: image background\nsize: [960, 540]\npages: [pages/01.page]\n",
  );
  writeFileSync(
    join(root, "pages", "01.page"),
    "pageType: content\nbackground:\n  type: image\n  src: media/background.png\n  fit: {mode: cover}\nelements: []\n",
  );
  writeFileSync(
    join(root, "media", "background.png"),
    Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Z5qAAAAAASUVORK5CYII=", "base64"),
  );

  try {
    await exportDeck({ manifest: join(root, "deck.pptd"), outPath: output, embedFonts: false });
    const bytes = readFileSync(output);
    assert.equal(bytes.includes(Buffer.from("ppt/media/image1.png")), true);
    assert.equal(bytes.includes(Buffer.from("ppt/slides/_rels/slide1.xml.rels")), true);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("persists an inline page background when exporting an editable PPTD project", () => {
  const dataUrl = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Z5qAAAAAASUVORK5CYII=";
  const deck = {
    pages: [{ background: { type: "image", src: dataUrl }, elements: [] }],
  };
  const files = mediaFilesOfDeck(deck, {});
  assert.equal(files.length, 1);
  assert.equal(files[0].path, "media/background-1.png");
  assert.equal(deck.pages[0].background.src, "media/background-1.png");
});
