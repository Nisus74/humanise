import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { PROVIDERS } from "../cli/providers.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (path) => readFileSync(resolve(ROOT, path), "utf8");
const README = read("README.md");
const GETTING_STARTED = read("docs/getting-started.md");
const PLATFORMS = read("docs/platforms.md");
const COMPATIBILITY = existsSync(resolve(ROOT, "docs/compatibility.md"))
  ? read("docs/compatibility.md")
  : "";
const AGENTS = read("AGENTS.md");
const PACKAGE = JSON.parse(read("package.json"));
const PLUGIN = JSON.parse(read(".claude-plugin/plugin.json"));
const MARKETPLACE = JSON.parse(read(".claude-plugin/marketplace.json"));

const HEADLINE = "Your AI should write like you, not like AI.";
const DESCRIPTION =
  "An open-source Agent Skill that preserves what you mean and learns how you write from real examples.";
const PRIVACY =
  "Your profile is stored locally. Humanise itself does not upload it, although the AI host you use still has its own data policy.";

test("public launch surfaces use the canonical positioning", () => {
  assert.match(README, new RegExp(`^## ${HEADLINE.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(README, new RegExp(`^${DESCRIPTION.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(README, new RegExp(`^${PRIVACY.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(
    README,
    /\[compatibility evidence\]\(https:\/\/github\.com\/Nisus74\/humanise\/blob\/main\/docs\/compatibility\.md\)/,
  );

  assert.equal(PACKAGE.description, DESCRIPTION);
  assert.equal(PLUGIN.description, DESCRIPTION);
  assert.equal(MARKETPLACE.description, DESCRIPTION);
  assert.equal(MARKETPLACE.plugins[0].description, DESCRIPTION);
});

test("launch documentation rules are explicit for future contributors", () => {
  for (const rule of [
    "Never invent testimonials, metrics or compatibility claims.",
    "Keep privacy language technically precise.",
    "Do not change the engine during a launch-surface task.",
    "Run `npm run quality` before completion.",
    "Do not add dependencies without explicit approval.",
  ]) {
    assert.match(AGENTS, new RegExp(rule.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")));
  }
});

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

test("compatibility evidence distinguishes installation checks from host verification", () => {
  const columns = [
    "Host",
    "Installation method",
    "Invocation",
    "Last tested date",
    "Operating system",
    "Host or CLI version",
    "Status",
    "Known limitations",
    "Evidence or test command",
  ];
  assert.match(COMPATIBILITY, new RegExp(`^\\| ${columns.join(" \\| ")} \\|$`, "m"));

  for (const host of [
    "Codex",
    "Claude Code",
    "Cursor",
    "Gemini CLI",
    "GitHub Copilot",
    "OpenCode",
    "Antigravity",
    "Universal Agent Skills hosts",
  ]) {
    assert.match(COMPATIBILITY, new RegExp(`^\\| ${host.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")} \\|`, "m"));
  }

  assert.match(COMPATIBILITY, /Host invocation was not run/);
  assert.match(COMPATIBILITY, /Claude Code 2\.1\.209/);
  assert.match(COMPATIBILITY, /Codex CLI 0\.144\.3/);
  assert.match(COMPATIBILITY, /skills 1\.5\.17/);
  assert.match(COMPATIBILITY, /native installer.*installs.*as `skill`/is);
  assert.match(COMPATIBILITY, /npm 1\.0\.0.*`universal`.*unreleased branch.*`antigravity`/is);
});

test("README and platform guide link to the evidence-backed compatibility matrix", () => {
  const link = "https://github.com/Nisus74/humanise/blob/main/docs/compatibility.md";
  assert.match(README, new RegExp(link.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")));
  assert.match(PLATFORMS, new RegExp(link.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")));
});

test("released commands are pinned and Antigravity uses the supported 1.0.0 fallback", () => {
  const docs = `${README}\n${GETTING_STARTED}\n${PLATFORMS}`;
  assert.match(docs, /npx humanise@1\.0\.0 install --provider=codex/);
  assert.match(docs, /npx humanise@1\.0\.0 install --provider=universal/);
  assert.match(docs, /\.gemini\/config\/skills\/humanise/);
  assert.doesNotMatch(docs, /humanise@1\.0\.0 install --provider=antigravity/);
  assert.doesNotMatch(docs, /gh skill install Nisus74\/humanise skill\/SKILL\.md/);
  assert.match(
    PLATFORMS,
    /native `gh skill install` command is available.*installs this release as `skill`.*canonical `humanise` directory/s,
  );
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
