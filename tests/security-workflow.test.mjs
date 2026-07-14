import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const WORKFLOW = readFileSync(resolve(ROOT, ".github/workflows/security.yml"), "utf8");

test("Gitleaks receives the pull request token required to scan", () => {
  assert.match(WORKFLOW, /GITHUB_TOKEN: \$\{\{ secrets\.GITHUB_TOKEN \}\}/);
});

test("Security jobs use the Node 24 action releases", () => {
  assert.match(
    WORKFLOW,
    /gitleaks\/gitleaks-action@e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e # v3\.0\.0/,
  );
  assert.equal(
    WORKFLOW.match(/actions\/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10/g)?.length,
    2,
  );
});
