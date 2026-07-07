#!/usr/bin/env node
// humanise CLI. No dependencies; Node built-ins only.
//   humanise install [--provider=<name>] [--global]   install the skill into your AI tool
//   humanise detect <file> [dialect] [medium]          run the deterministic checker (Python)
//   humanise voiceprint <file> | --build               score/build voice distance (Python)
//   humanise init                                      scaffold a voice profile
//   humanise build                                     rebuild dist/ from skill/
import {
  existsSync,
  mkdirSync,
  cpSync,
  readFileSync,
  readdirSync,
} from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { PROVIDERS, DETECT } from "../providers.mjs";

const PKG_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const DIST = join(PKG_ROOT, "dist");
const SKILL = join(PKG_ROOT, "skill");

function detectProvider(cwd) {
  for (const [marker, provider] of Object.entries(DETECT)) {
    if (existsSync(join(cwd, marker))) return provider;
  }
  return null;
}

function ensureBuilt() {
  if (!existsSync(DIST)) {
    spawnSync(process.execPath, [join(PKG_ROOT, "scripts", "build.mjs")], {
      stdio: "inherit",
    });
  }
}

function ensurePython() {
  const probe = spawnSync("python3", ["--version"]);
  if (probe.error) {
    console.error(
      "humanise needs Python 3 for the checker, and `python3` isn't on your PATH.\n" +
        "Install Python 3 from https://www.python.org/downloads/ (or your package manager),\n" +
        "confirm `python3 --version` works, then re-run.",
    );
    process.exit(1);
  }
}

function install(args) {
  const flagProvider = (args.find((a) => a.startsWith("--provider=")) || "").split("=")[1];
  const global = args.includes("--global") || args.includes("-g");
  const cwd = process.cwd();
  const provider = flagProvider || detectProvider(cwd) || "universal";
  if (!PROVIDERS[provider]) {
    console.error(`Unknown provider "${provider}". Options: ${Object.keys(PROVIDERS).join(", ")}`);
    process.exit(1);
  }
  ensureBuilt();
  const rel = PROVIDERS[provider];
  const src = join(DIST, provider, rel);
  if (!existsSync(src)) {
    console.error(`No build for "${provider}". Run "humanise build" first.`);
    process.exit(1);
  }
  const dest = global ? join(homedir(), rel) : join(cwd, rel);
  mkdirSync(dirname(dest), { recursive: true });
  cpSync(src, dest, { recursive: true });
  console.log(`Installed humanise (${provider}) -> ${dest}`);
  console.log(`Next: run "/humanise init" inside your tool to set up your voice profile.`);
}

function detect(args) {
  const positional = args.filter((a) => !a.startsWith("-"));
  const file = positional[0];
  if (!file) {
    console.error("Usage: humanise detect <file> [dialect] [medium]");
    process.exit(1);
  }
  const dialect = positional[1] || "aus";
  const medium = positional[2] || "plain";
  const checker = join(SKILL, "evals", "assertions", "writing_checks.py");
  ensurePython();
  const r = spawnSync("python3", [checker, file, dialect, medium], { stdio: "inherit" });
  if (r.error) {
    console.error("Could not run the checker. Python 3 is required for `detect`.");
    process.exit(1);
  }
  process.exit(r.status ?? 0);
}

function profileBase() {
  const cwd = process.cwd();
  for (const rel of Object.values(PROVIDERS)) {
    if (existsSync(join(cwd, rel, "profile")) || existsSync(join(cwd, rel, "profile.template"))) {
      return join(cwd, rel);
    }
  }
  return SKILL;
}

function voiceprint(args) {
  const script = join(SKILL, "scripts", "build_voiceprint.py");
  const base = profileBase();
  const baseline =
    (args.find((a) => a.startsWith("--baseline=")) || "").split("=")[1] ||
    join(base, "profile", "voiceprint.json");
  if (args.includes("--build")) {
    const corpus =
      (args.find((a) => a.startsWith("--corpus=")) || "").split("=")[1] ||
      join(base, "profile");
    if (!existsSync(corpus)) {
      console.error(`No profile at ${corpus}. Run "/humanise init" first.`);
      process.exit(1);
    }
    if (!readdirSync(corpus).some((f) => /^sample-.*\.md$/.test(f))) {
      console.error(`No sample-*.md files in ${corpus}. Add samples (sample-<channel>-<slug>.md) before building a voiceprint.`);
      process.exit(1);
    }
    ensurePython();
    const r = spawnSync("python3", [script, "--corpus", corpus, "--out", baseline], { stdio: "inherit" });
    if (r.error) {
      console.error("Could not run the voiceprint builder. Python 3 is required.");
      process.exit(1);
    }
    process.exit(r.status ?? 0);
  }
  const file = args.filter((a) => !a.startsWith("-"))[0];
  if (!file) {
    console.error("Usage: humanise voiceprint <file> [--baseline=<path>]  |  humanise voiceprint --build [--corpus=<dir>]");
    process.exit(1);
  }
  if (!existsSync(baseline)) {
    console.error(`No voiceprint baseline at ${baseline}. Build one first: humanise voiceprint --build`);
    process.exit(1);
  }
  ensurePython();
  const r = spawnSync("python3", [script, "--score", file, "--baseline", baseline], { stdio: "inherit" });
  if (r.error) {
    console.error("Could not run the voiceprint scorer. Python 3 is required.");
    process.exit(1);
  }
  process.exit(r.status ?? 0);
}

function init() {
  const cwd = process.cwd();
  let base = null;
  for (const rel of Object.values(PROVIDERS)) {
    if (existsSync(join(cwd, rel, "profile.template"))) {
      base = join(cwd, rel);
      break;
    }
  }
  base = base || SKILL;
  const tpl = join(base, "profile.template");
  const dest = join(base, "profile");
  if (existsSync(dest)) {
    console.log(`profile/ already exists at ${dest}. Edit it directly.`);
    return;
  }
  if (!existsSync(tpl)) {
    console.error(`No profile.template found near ${base}. Install humanise first.`);
    process.exit(1);
  }
  cpSync(tpl, dest, { recursive: true });
  console.log(`Created ${dest} from profile.template.`);
  console.log("Next:");
  console.log("  1. Write profile/soul.md (see profile.example/soul.md for the bar).");
  console.log("  2. Collect 5-10 samples fast with scripts/corpus-questionnaire.md (flat in profile/ as sample-<channel>-*.md).");
  console.log("  3. Generate your fingerprint with scripts/generate-fingerprint.md (also builds the voiceprint).");
}

function build() {
  spawnSync(process.execPath, [join(PKG_ROOT, "scripts", "build.mjs")], { stdio: "inherit" });
}

function version() {
  const pkg = JSON.parse(readFileSync(join(PKG_ROOT, "package.json"), "utf8"));
  console.log(`humanise ${pkg.version}`);
}

function help() {
  console.log(`humanise - make AI writing sound human (body + soul)

Usage:
  npx humanise install [--provider=<name>] [--global]   install the skill into your AI tool
  npx humanise detect <file> [dialect] [medium]         run the deterministic checker (no LLM)
  npx humanise voiceprint <file>                        score a draft's distance from your voice (advisory)
  npx humanise voiceprint --build                       build the baseline from profile/ samples
  npx humanise init                                     scaffold your voice profile
  npx humanise build                                    rebuild dist/ from skill/
  npx humanise version

Providers: ${Object.keys(PROVIDERS).join(", ")}
Install auto-detects your harness (looks for .claude, .cursor, .gemini, .agents, ...).
After installing, run "/humanise init" inside your tool.`);
}

const [cmd, ...args] = process.argv.slice(2);
switch (cmd) {
  case "install":
    install(args);
    break;
  case "detect":
  case "check":
    detect(args);
    break;
  case "voiceprint":
    voiceprint(args);
    break;
  case "init":
    init();
    break;
  case "build":
    build();
    break;
  case "version":
  case "--version":
  case "-v":
    version();
    break;
  default:
    help();
}
