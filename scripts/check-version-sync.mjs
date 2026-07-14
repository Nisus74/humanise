#!/usr/bin/env node
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { readVersionState, versionProblems } from "./version-state.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const state = readVersionState(root);
const problems = versionProblems(state);
if (problems.length) {
  console.error("Version sync check failed:");
  for (const problem of problems) console.error(`  - ${problem}`);
  process.exit(1);
}
console.log(`Version sync check passed: ${state.canonical}`);
