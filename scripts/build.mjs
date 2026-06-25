#!/usr/bin/env node
// Compile the single source skill (skill/) into a per-provider build under dist/.
// Each provider gets the same portable skill, placed at the path that harness expects.
// The Python checker travels as-is; nothing is transpiled.
import { cpSync, mkdirSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { PROVIDERS } from "../cli/providers.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(ROOT, "skill");
const DIST = join(ROOT, "dist");

const skip = (src) =>
  !src.includes("__pycache__") &&
  !src.endsWith(".pyc") &&
  !src.endsWith(".ruff_cache") &&
  !src.endsWith("/profile") && // never ship a user's filled-in profile
  !src.endsWith("/config.yml");

function build() {
  rmSync(DIST, { recursive: true, force: true });
  for (const [provider, rel] of Object.entries(PROVIDERS)) {
    const dest = join(DIST, provider, rel);
    mkdirSync(dirname(dest), { recursive: true });
    cpSync(SRC, dest, { recursive: true, filter: skip });
  }
  // Claude Code also gets the plugin manifest at the build root.
  const pluginSrc = join(ROOT, ".claude-plugin", "plugin.json");
  const pluginDst = join(DIST, "claude-code", ".claude-plugin", "plugin.json");
  mkdirSync(dirname(pluginDst), { recursive: true });
  cpSync(pluginSrc, pluginDst);
  console.log("Built dist/ for: " + Object.keys(PROVIDERS).join(", "));
}

build();
