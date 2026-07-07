#!/usr/bin/env node
// Validate the BUILT skill against the Agent Skills spec (agentskills.io/specification).
// Mirrors the checks `skills-ref validate` performs, with zero dependencies (Node
// built-ins only, like scripts/check-no-deps.mjs), so spec compliance is verifiable on
// every build without taking on an external tool.
//
//   npm run build && npm run validate
//
// Runs against dist/ (the artifact that ships), NOT the source skill/. The source folder
// is named `skill/` on purpose; it builds and installs as `humanise/`, which is what the
// spec's name-matches-directory rule applies to (see docs/DEVELOP.md). Running
// `skills-ref validate ./skill` on the source would (correctly) flag that mismatch.
//
// Hard checks fail the run (exit 1). Advisory checks warn only.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, basename, relative } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const DIST = join(root, "dist");

const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/; // lowercase alnum + single hyphens
const MAX_NAME = 64;
const MAX_DESC = 1024;
const SOFT_LINES = 500;
const SOFT_TOKENS = 5000;

function walk(dir, onFile) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, onFile);
    else onFile(p);
  }
}

// Directories nested two or more levels below the skill root (a folder inside a folder).
function nestedDirs(skillRoot, dir = skillRoot, acc = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (!e.isDirectory()) continue;
    const p = join(dir, e.name);
    const rel = relative(skillRoot, p);
    if (rel.includes("/")) acc.push(rel);
    nestedDirs(skillRoot, p, acc);
  }
  return acc;
}

// Minimal YAML frontmatter reader: enough for `name` (plain/quoted scalar) and
// `description` (inline, or a folded `>` / literal `|` block). Not a general parser.
function parseFrontmatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") return null;
  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") { end = i; break; }
  }
  if (end === -1) return null;
  const fm = lines.slice(1, end);
  const out = {};
  for (let i = 0; i < fm.length; i++) {
    const m = fm[i].match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    let val = m[2];
    if (["", ">", "|", ">-", "|-"].includes(val)) {
      const block = [];
      for (let j = i + 1; j < fm.length; j++) {
        if (/^\s+\S/.test(fm[j]) || fm[j].trim() === "") { block.push(fm[j].trim()); i = j; }
        else break;
      }
      val = block.join(" ").replace(/\s+/g, " ").trim();
    } else {
      val = val.replace(/^["']|["']$/g, "").trim();
    }
    out[m[1]] = val;
  }
  return out;
}

function validateSkill(skillMdPath) {
  const skillDir = dirname(skillMdPath);
  const rel = relative(DIST, skillMdPath);
  const hard = [];
  const warn = [];
  const text = readFileSync(skillMdPath, "utf8");
  const fm = parseFrontmatter(text);
  if (!fm) {
    hard.push("SKILL.md has no valid YAML frontmatter");
    return { rel, hard, warn };
  }
  const { name, description } = fm;
  if (!name) {
    hard.push("frontmatter missing `name`");
  } else {
    if (name.length > MAX_NAME) hard.push(`name length ${name.length} exceeds ${MAX_NAME}`);
    if (!NAME_RE.test(name)) hard.push(`name "${name}" must be lowercase alphanumeric with single hyphens`);
    const parent = basename(skillDir);
    if (name !== parent) hard.push(`name "${name}" must match parent directory "${parent}"`);
  }
  if (!description) {
    hard.push("frontmatter missing `description`");
  } else {
    if (description.length > MAX_DESC) hard.push(`description length ${description.length} exceeds ${MAX_DESC}`);
    if (/[<>]/.test(description)) hard.push("description must not contain angle brackets (< or >)");
  }

  const lineCount = text.split(/\r?\n/).length;
  const tokenEst = Math.round(text.length / 4);
  if (lineCount > SOFT_LINES) warn.push(`SKILL.md is ${lineCount} lines (spec recommends < ${SOFT_LINES})`);
  if (tokenEst > SOFT_TOKENS) warn.push(`SKILL.md ~${tokenEst} tokens (spec recommends < ${SOFT_TOKENS})`);
  for (const d of nestedDirs(skillDir)) warn.push(`nested folder ${d} (spec prefers references one level deep)`);
  return { rel, hard, warn };
}

function main() {
  if (!existsSync(DIST)) {
    console.error("No dist/ found. Run `npm run build` first, then `npm run validate`.");
    process.exit(1);
  }
  const skillMds = [];
  walk(DIST, (p) => { if (basename(p) === "SKILL.md") skillMds.push(p); });
  if (!skillMds.length) {
    console.error("No SKILL.md found under dist/. Did the build succeed?");
    process.exit(1);
  }
  let failed = 0;
  for (const p of skillMds.sort()) {
    const { rel, hard, warn } = validateSkill(p);
    if (hard.length) {
      failed++;
      console.error(`FAIL ${rel}`);
      for (const h of hard) console.error("  - " + h);
    } else {
      console.log(`PASS ${rel}`);
    }
    for (const w of warn) console.log("  ! " + w);
  }
  // Validate the Claude Code plugin artifact: a valid plugin root has the manifest
  // under .claude-plugin/ and the skill auto-discovered at skills/<name>/SKILL.md.
  // A stale `skills` path (the old "../skill") breaks install, so flag it here.
  const pluginManifest = join(DIST, "claude-code", ".claude-plugin", "plugin.json");
  const pluginSkill = join(DIST, "claude-code", "skills", "humanise", "SKILL.md");
  const pErrs = [];
  if (!existsSync(pluginManifest)) {
    pErrs.push("missing dist/claude-code/.claude-plugin/plugin.json");
  } else {
    let pm = null;
    try {
      pm = JSON.parse(readFileSync(pluginManifest, "utf8"));
    } catch (e) {
      pErrs.push("plugin.json is not valid JSON: " + e.message);
    }
    if (pm) {
      if (!pm.name) pErrs.push("plugin.json missing `name`");
      else if (!NAME_RE.test(pm.name)) pErrs.push(`plugin name "${pm.name}" must be lowercase alphanumeric with single hyphens`);
      if (!pm.version) pErrs.push("plugin.json missing `version`");
      if (pm.description && /[<>]/.test(pm.description)) pErrs.push("plugin.json description must not contain angle brackets");
      if (pm.skills) pErrs.push("plugin.json should not declare a `skills` path; skills auto-discover from skills/<name>/, and a stale path breaks install");
    }
  }
  if (!existsSync(pluginSkill)) {
    pErrs.push("missing dist/claude-code/skills/humanise/SKILL.md (plugin auto-discovery layout)");
  }
  if (pErrs.length) {
    failed++;
    console.error("FAIL claude-code plugin artifact");
    for (const e of pErrs) console.error("  - " + e);
  } else {
    console.log("PASS claude-code plugin artifact");
  }

  if (failed) {
    console.error(`\nSpec validation failed for ${failed} built skill(s).`);
    process.exit(1);
  }
  console.log(`\nSpec validation passed for ${skillMds.length} built skill(s) (warnings are advisory).`);
}

main();
