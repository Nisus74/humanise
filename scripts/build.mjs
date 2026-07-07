#!/usr/bin/env node
// Compile the single source skill (skill/) into a per-provider build under dist/.
// Each provider gets the same portable skill, placed at the path that harness expects.
// The Python checker travels as-is; nothing is transpiled.
import { cpSync, mkdirSync, rmSync, readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { PROVIDERS } from "../cli/providers.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(ROOT, "skill");
const DIST = join(ROOT, "dist");

const pkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8"));
// Version stamp travels inside every built skill so an install's drift from the
// current engine is detectable (used by `humanise version` / a future `update`).
const STAMP =
  JSON.stringify({ version: pkg.version, built: new Date().toISOString() }, null, 2) + "\n";

const skip = (src) =>
  !src.includes("__pycache__") &&
  !src.endsWith(".pyc") &&
  !src.endsWith(".ruff_cache") &&
  !src.endsWith("/.DS_Store") &&
  !src.endsWith("/profile") && // never ship a user's filled-in profile
  !src.endsWith("/config.yml");

// The Claude Code plugin artifact. Per the plugin spec, a plugin root holds the
// manifest under .claude-plugin/ and the skill under skills/<name>/SKILL.md, which
// is auto-discovered (no `skills` path in the manifest, and NOT .claude/skills,
// which is the manual-copy install path the provider loop emits). The manifest's
// version is synced from package.json so the two never drift.
function writePlugin() {
  const manifest = JSON.parse(
    readFileSync(join(ROOT, ".claude-plugin", "plugin.json"), "utf8"),
  );
  manifest.version = pkg.version;
  const pluginRoot = join(DIST, "claude-code");
  const manifestDst = join(pluginRoot, ".claude-plugin", "plugin.json");
  mkdirSync(dirname(manifestDst), { recursive: true });
  writeFileSync(manifestDst, JSON.stringify(manifest, null, 2) + "\n");
  const skillDst = join(pluginRoot, "skills", "humanise");
  mkdirSync(dirname(skillDst), { recursive: true });
  cpSync(SRC, skillDst, { recursive: true, filter: skip });
  writeFileSync(join(skillDst, ".humanise-version"), STAMP);
}

function build() {
  rmSync(DIST, { recursive: true, force: true });
  for (const [provider, rel] of Object.entries(PROVIDERS)) {
    const dest = join(DIST, provider, rel);
    mkdirSync(dirname(dest), { recursive: true });
    cpSync(SRC, dest, { recursive: true, filter: skip });
    writeFileSync(join(dest, ".humanise-version"), STAMP);
  }
  // Claude Code also gets the plugin layout (manifest + auto-discovered skill).
  writePlugin();
  console.log(
    "Built dist/ for: " +
      Object.keys(PROVIDERS).join(", ") +
      " (+ claude-code plugin layout)",
  );
}

build();
