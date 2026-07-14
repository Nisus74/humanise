import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { PROVIDERS } from "../cli/providers.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (path) => readFileSync(resolve(ROOT, path), "utf8");
const README = read("README.md");
const GETTING_STARTED = read("docs/getting-started.md");
const PLATFORMS = read("docs/platforms.md");

test("getting started covers the complete beginner journey", () => {
  for (const heading of [
    "What you are installing",
    "Step 1: check Node.js and Python",
    "Step 2: choose your host and scope",
    "Step 3: install humanise",
    "Step 4: check the installation",
    "Step 5: get a useful rewrite before setup",
    "Step 6: create the profile and configuration",
    "Step 7: set the basic configuration",
    "Step 8: teach humanise with one sample",
    "Step 9: run the personalised comparison",
    "Step 10: run the final health and privacy check",
    "Troubleshooting",
  ]) {
    assert.match(GETTING_STARTED, new RegExp(`^## ${heading}$`, "m"));
  }
});

test("platform guide covers every installer provider", () => {
  const hostNames = {
    "claude-code": "Claude Code",
    cursor: "Cursor",
    gemini: "Gemini CLI",
    codex: "Codex",
    github: "GitHub Copilot",
    opencode: "OpenCode",
    antigravity: "Antigravity",
    universal: "Universal install",
  };

  assert.deepEqual(Object.keys(hostNames).sort(), Object.keys(PROVIDERS).sort());
  for (const host of Object.values(hostNames)) {
    assert.match(PLATFORMS, new RegExp(`^## ${host}$`, "m"));
  }
  assert.match(PLATFORMS, /^## Gemini CLI$/m);
  assert.match(PLATFORMS, /^## Antigravity$/m);
});

test("released commands are pinned and Antigravity uses the supported 1.0.0 fallback", () => {
  const docs = `${README}\n${GETTING_STARTED}\n${PLATFORMS}`;
  assert.match(docs, /npx humanise@1\.0\.0 install --provider=codex/);
  assert.match(docs, /npx humanise@1\.0\.0 install --provider=universal/);
  assert.match(docs, /\.gemini\/config\/skills\/humanise/);
  assert.doesNotMatch(docs, /humanise@1\.0\.0 install --provider=antigravity/);
  assert.doesNotMatch(docs, /gh skill install Nisus74\/humanise skill\/SKILL\.md/);
});

test("npm README links resolve outside the repository", () => {
  const relativeLinks = [...README.matchAll(/\]\((?!https?:\/\/|#|mailto:)([^)]+)\)/g)].map(
    (match) => match[1],
  );
  assert.deepEqual(relativeLinks, ["LICENSE", "LICENSE"]);
});

test("published docs contain no pre-release install instructions", () => {
  const docs = `${README}\n${GETTING_STARTED}\n${PLATFORMS}`;
  assert.doesNotMatch(docs, /Until npm (?:is )?published/i);
  assert.doesNotMatch(docs, /node cli\/bin\/cli\.js install/);
});
