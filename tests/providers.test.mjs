import test from "node:test";
import assert from "node:assert/strict";
import { PROVIDERS, detectProviders } from "../cli/providers.mjs";

const EXPECTED = {
  "claude-code": {
    projectPath: ".claude/skills/humanise",
    globalPath: ".claude/skills/humanise",
    markers: [".claude"],
    invoke: "/humanise",
  },
  cursor: {
    projectPath: ".cursor/skills/humanise",
    globalPath: ".cursor/skills/humanise",
    markers: [".cursor"],
    invoke: "/humanise",
  },
  gemini: {
    projectPath: ".gemini/skills/humanise",
    globalPath: ".gemini/skills/humanise",
    markers: [".gemini"],
    invoke: "/skills enable humanise, then ask normally",
  },
  codex: {
    projectPath: ".agents/skills/humanise",
    globalPath: ".agents/skills/humanise",
    markers: [".agents", ".codex"],
    invoke: "$humanise",
  },
  github: {
    projectPath: ".github/skills/humanise",
    globalPath: ".copilot/skills/humanise",
    markers: [],
    invoke: "/humanise",
  },
  opencode: {
    projectPath: ".opencode/skills/humanise",
    globalPath: ".config/opencode/skills/humanise",
    markers: [".opencode"],
    invoke: "ask normally or load the humanise skill",
  },
  antigravity: {
    projectPath: ".agents/skills/humanise",
    globalPath: ".gemini/config/skills/humanise",
    markers: [],
    invoke: "mention humanise by name",
  },
  universal: {
    projectPath: "humanise",
    globalPath: ".agents/skills/humanise",
    markers: [],
    invoke: "ask your agent to use the humanise skill",
  },
};

test("provider metadata matches current host paths", () => {
  assert.deepEqual(PROVIDERS, EXPECTED);
});

test("Antigravity is never inferred from shared markers", () => {
  const present = new Set([".agents", ".gemini"]);
  const detected = detectProviders("/repo", (_cwd, marker) => present.has(marker));
  assert.deepEqual(new Set(detected), new Set(["gemini", "codex"]));
  assert.equal(detected.includes("antigravity"), false);
});

test("providers without reliable markers require an explicit flag", () => {
  const detected = detectProviders("/repo", () => false);
  assert.deepEqual(detected, []);
  for (const provider of ["github", "antigravity", "universal"]) {
    assert.deepEqual(PROVIDERS[provider].markers, []);
  }
});
