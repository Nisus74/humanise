#!/usr/bin/env node
// Fail a release when private profile data or generated local state can enter
// the npm package. Check both the package whitelist and built artifacts.
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));
const problems = [];

for (const entry of pkg.files || []) {
  const clean = entry.replace(/^\.\//, "");
  if (clean === "skill" || clean.startsWith("skill/")) {
    problems.push(`package.json files includes private-capable source path: ${entry}`);
  }
}

function walk(dir) {
  if (!existsSync(dir)) return;
  for (const item of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, item.name);
    if (item.isDirectory()) {
      if (item.name === "profile" || item.name === "__pycache__") {
        problems.push(`built artifact contains excluded directory: ${relative(root, path)}`);
      } else {
        walk(path);
      }
    } else if (item.name === "config.yml" || item.name.endsWith(".pyc")) {
      problems.push(`built artifact contains excluded file: ${relative(root, path)}`);
    }
  }
}

walk(join(root, "dist"));

if (problems.length) {
  console.error("Package privacy check failed:");
  for (const problem of problems) console.error(`  - ${problem}`);
  process.exit(1);
}

console.log("Package privacy check passed: no private profile, config or cache files can ship.");
