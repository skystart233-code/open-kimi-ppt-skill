import assert from "node:assert/strict";
import { once } from "node:events";
import test from "node:test";
import { createEditorServer } from "../lib/editor-server.js";

async function withServer(callback) {
  const server = createEditorServer();
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address();

  try {
    await callback(`http://127.0.0.1:${address.port}`);
  } finally {
    server.close();
    await once(server, "close");
  }
}

test("serves the PPTD editor and its JavaScript modules", async () => {
  await withServer(async (url) => {
    const redirect = await fetch(`${url}/`, { redirect: "manual" });
    assert.equal(redirect.status, 302);
    assert.equal(redirect.headers.get("location"), "/editor/");

    const index = await fetch(`${url}/editor/`);
    assert.equal(index.status, 200);
    assert.match(index.headers.get("content-type"), /^text\/html/);
    assert.match(await index.text(), /open-pptd/);

    const app = await fetch(`${url}/editor/main.js`);
    assert.equal(app.status, 200);
    assert.match(app.headers.get("content-type"), /^text\/javascript/);

    const fonts = await fetch(`${url}/assets/fonts/registry.json`);
    assert.equal(fonts.status, 200);
    assert.match(fonts.headers.get("content-type"), /^application\/json/);
  });
});

test("returns 404 for files outside the packaged editor", async () => {
  await withServer(async (url) => {
    const response = await fetch(`${url}/missing.js`);
    assert.equal(response.status, 404);
  });
});

test("supports HEAD requests without a response body", async () => {
  await withServer(async (url) => {
    const response = await fetch(`${url}/editor/styles.css`, { method: "HEAD" });
    assert.equal(response.status, 200);
    assert.equal(await response.text(), "");
  });
});
