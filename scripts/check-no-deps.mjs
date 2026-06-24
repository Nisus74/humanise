#!/usr/bin/env node
// Enforce humanise's zero-dependency invariant: the CLI is Node built-ins, the
// checker is Python stdlib. Fails if package.json declares any dependencies, or
// if a lockfile is present. Tool-agnostic: run by pre-commit (local hook) and CI
// so the rule holds for every contributor, whatever AI tool or editor they use.
//
//   npm run check:deps
//
// If a dependency is ever genuinely justified, change this check in the same PR
// so the decision is explicit and reviewed (see CLAUDE.md).
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));
const problems = [];

for (const field of ["dependencies", "devDependencies", "optionalDependencies", "peerDependencies"]) {
  const deps = pkg[field];
  if (deps && Object.keys(deps).length > 0) {
    problems.push(`package.json "${field}" must be empty; found: ${Object.keys(deps).join(", ")}`);
  }
}
for (const lock of ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json"]) {
  if (existsSync(join(root, lock))) {
    problems.push(`lockfile ${lock} must not exist; the project ships no dependencies`);
  }
}

if (problems.length) {
  console.error("Zero-dependency check failed:");
  for (const p of problems) console.error("  - " + p);
  console.error("\nhumanise stays dependency-free on purpose (CLAUDE.md). If a dependency is genuinely");
  console.error("needed, change scripts/check-no-deps.mjs in the same PR so the call is explicit.");
  process.exit(1);
}
console.log("Zero-dependency check passed: no declared deps, no lockfile.");
