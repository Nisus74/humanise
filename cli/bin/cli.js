#!/usr/bin/env node
// humanise CLI. No dependencies; Node built-ins only.
//   humanise install --provider=<name> [--global|--project]  install the skill
//   humanise doctor --provider=<name> [--global|--project]   verify discovery and privacy
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
  appendFileSync,
} from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { PROVIDERS, detectProviders } from "../providers.mjs";

const PKG_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const DIST = join(PKG_ROOT, "dist");
const SOURCE_SKILL = join(PKG_ROOT, "skill");
const SKILL = existsSync(SOURCE_SKILL) ? SOURCE_SKILL : join(DIST, "humanise");

function providerNames() {
  return Object.keys(PROVIDERS);
}

function providerPath(provider, scope) {
  const config = PROVIDERS[provider];
  return scope === "global" ? config.globalPath : config.projectPath;
}

function parseScope(args, fallback = "global") {
  if (args.includes("--project") || args.includes("--scope=project")) return "project";
  if (args.includes("--global") || args.includes("-g") || args.includes("--scope=user")) return "global";
  return fallback;
}

function resolveProvider(args, cwd) {
  const explicit = (args.find((a) => a.startsWith("--provider=")) || "").split("=")[1];
  if (explicit) return explicit;
  const candidates = detectProviders(cwd, (base, marker) => existsSync(join(base, marker)));
  if (candidates.length === 1) return candidates[0];
  if (candidates.length > 1) {
    console.error(`More than one supported agent was detected: ${candidates.join(", ")}.`);
    console.error("Choose one with --provider=<name>, or install each one separately.");
    process.exit(1);
  }
  console.error("No supported agent could be detected from this directory.");
  console.error(`Choose one with --provider=<name>. Options: ${providerNames().join(", ")}`);
  process.exit(1);
}

function ensureBuilt() {
  if (!existsSync(DIST)) {
    spawnSync(process.execPath, [join(PKG_ROOT, "scripts", "build.mjs")], {
      stdio: "inherit",
    });
  }
}

function protectProjectProfile(cwd, rel) {
  const probe = spawnSync("git", ["rev-parse", "--git-path", "info/exclude"], {
    cwd,
    encoding: "utf8",
  });
  if (probe.status !== 0) return null;
  const raw = probe.stdout.trim();
  if (!raw) return null;
  const exclude = resolve(cwd, raw);
  mkdirSync(dirname(exclude), { recursive: true });
  const existing = existsSync(exclude) ? readFileSync(exclude, "utf8") : "";
  const entries = [`/${rel}/profile/`, `/${rel}/config.yml`];
  const missing = entries.filter((entry) => !existing.split(/\r?\n/).includes(entry));
  if (missing.length) {
    appendFileSync(exclude, `${existing && !existing.endsWith("\n") ? "\n" : ""}# humanise private voice profile\n${missing.join("\n")}\n`);
  }
  return exclude;
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
  const cwd = process.cwd();
  const provider = resolveProvider(args, cwd);
  const scope = parseScope(args);
  if (!PROVIDERS[provider]) {
    console.error(`Unknown provider "${provider}". Options: ${providerNames().join(", ")}`);
    process.exit(1);
  }
  ensureBuilt();
  const rel = providerPath(provider, scope);
  const src = join(DIST, "humanise");
  if (!existsSync(src)) {
    spawnSync(process.execPath, [join(PKG_ROOT, "scripts", "build.mjs")], { stdio: "inherit" });
  }
  if (!existsSync(src)) {
    console.error(`Could not build the install artifact for "${provider}".`);
    process.exit(1);
  }
  const dest = scope === "global" ? join(homedir(), rel) : join(cwd, rel);
  mkdirSync(dirname(dest), { recursive: true });
  cpSync(src, dest, { recursive: true });
  const exclude = scope === "project" ? protectProjectProfile(cwd, rel) : null;
  console.log(`Installed humanise for ${provider} (${scope}) -> ${dest}`);
  if (exclude) console.log(`Protected the private profile locally in ${exclude}`);
  console.log(`Next in ${provider}: ${PROVIDERS[provider].invoke}. Ask it to set up humanise.`);
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

function profileBase(args = []) {
  const cwd = process.cwd();
  const explicit = (args.find((a) => a.startsWith("--provider=")) || "").split("=")[1];
  if (explicit) {
    if (!PROVIDERS[explicit]) {
      console.error(`Unknown provider "${explicit}". Options: ${providerNames().join(", ")}`);
      process.exit(1);
    }
    const scope = parseScope(args);
    const root = scope === "global" ? homedir() : cwd;
    return join(root, providerPath(explicit, scope));
  }
  const roots = [cwd, homedir()];
  const matches = [];
  for (const root of roots) {
    for (const config of Object.values(PROVIDERS)) {
      for (const rel of new Set([config.projectPath, config.globalPath])) {
        if (existsSync(join(root, rel, "profile")) || existsSync(join(root, rel, "profile.template"))) {
          matches.push(join(root, rel));
        }
      }
    }
  }
  const unique = [...new Set(matches)];
  if (unique.length === 1) return unique[0];
  if (unique.length > 1) {
    console.error("More than one humanise installation was found:");
    for (const match of unique) console.error(`  ${match}`);
    console.error("Choose one with --provider=<name> and --global or --project.");
    process.exit(1);
  }
  return SKILL;
}

function voiceprint(args) {
  const script = join(SKILL, "scripts", "build_voiceprint.py");
  const base = profileBase(args);
  const baseline =
    (args.find((a) => a.startsWith("--baseline=")) || "").split("=")[1] ||
    join(base, "profile", "voiceprint.json");
  if (args.includes("--status")) {
    const profile = join(base, "profile");
    if (!existsSync(profile)) {
      console.error(`No profile at ${profile}. Run "/humanise init" first.`);
      process.exit(1);
    }
    ensurePython();
    const statusArgs = [script, "--status", "--profile", profile, "--baseline", baseline];
    if (args.includes("--json")) statusArgs.push("--json");
    const r = spawnSync("python3", statusArgs, { stdio: "inherit" });
    if (r.error) {
      console.error("Could not run the voiceprint status report. Python 3 is required.");
      process.exit(1);
    }
    process.exit(r.status ?? 0);
  }
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
    console.error("Usage: humanise voiceprint <file> [--baseline=<path>]  |  humanise voiceprint --build [--corpus=<dir>]  |  humanise voiceprint --status [--json]");
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

function init(args) {
  const base = profileBase(args);
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
  const config = join(base, "config.yml");
  if (!existsSync(config) && existsSync(join(base, "config.example.yml"))) {
    cpSync(join(base, "config.example.yml"), config);
  }
  console.log(`Created ${dest} from profile.template.`);
  console.log(`Created ${config}.`);
  console.log("Next: open your agent, invoke humanise, and ask for the three-minute voice setup.");
  console.log("One real writing sample is enough to start. Add more channels when the first result is useful.");
}

function doctor(args) {
  const cwd = process.cwd();
  const provider = resolveProvider(args, cwd);
  const scope = parseScope(args);
  const rel = providerPath(provider, scope);
  const base = scope === "global" ? join(homedir(), rel) : join(cwd, rel);
  let failed = false;
  const checks = [
    ["skill", join(base, "SKILL.md")],
    ["profile template", join(base, "profile.template")],
    ["configuration template", join(base, "config.example.yml")],
  ];
  for (const [label, path] of checks) {
    const ok = existsSync(path);
    console.log(`${ok ? "OK" : "MISSING"}  ${label}: ${path}`);
    if (!ok) failed = true;
  }
  const profile = join(base, "profile");
  console.log(`${existsSync(profile) ? "OK" : "NOT SET UP"}  private profile: ${profile}`);
  if (scope === "project" && existsSync(profile)) {
    const tracked = spawnSync("git", ["ls-files", "--error-unmatch", profile], { cwd, encoding: "utf8" });
    if (tracked.status === 0) {
      console.log("UNSAFE  the private profile is tracked by Git");
      failed = true;
    } else {
      console.log("OK  the private profile is not tracked by Git");
    }
  }
  console.log(`Invoke in ${provider}: ${PROVIDERS[provider].invoke}`);
  process.exit(failed ? 1 : 0);
}

function build() {
  if (!existsSync(SOURCE_SKILL)) {
    console.error("The build command is available only in a source checkout. Published packages already contain built artefacts.");
    process.exit(1);
  }
  spawnSync(process.execPath, [join(PKG_ROOT, "scripts", "build.mjs")], { stdio: "inherit" });
}

function version() {
  const pkg = JSON.parse(readFileSync(join(PKG_ROOT, "package.json"), "utf8"));
  console.log(`humanise ${pkg.version}`);
}

function help() {
  console.log(`humanise - make AI writing sound human (body + soul)

Usage:
  npx humanise install --provider=<name> [--global|--project]
                                                      install the skill (user scope is default)
  npx humanise doctor --provider=<name> [--global|--project]
                                                      verify discovery, profile and privacy
  npx humanise detect <file> [dialect] [medium]         run the deterministic checker (no LLM)
  npx humanise voiceprint <file>                        score a draft's distance from your voice (advisory)
  npx humanise voiceprint --build                       build the baseline from profile/ samples
  npx humanise voiceprint --status [--json]             corpus and voiceprint state per channel
  npx humanise init [--provider=<name>] [--global|--project]
                                                      scaffold your voice profile
  npx humanise build                                    rebuild dist/ from skill/
  npx humanise version

Providers: ${Object.keys(PROVIDERS).join(", ")}
Install auto-detects only when exactly one supported harness marker is present.
After installing, invoke the skill in your tool and ask to set up humanise.`);
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
    init(args);
    break;
  case "doctor":
    doctor(args);
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
