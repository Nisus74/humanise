import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { readVersionState, versionProblems } from "../scripts/version-state.mjs";

function fixture(versions = {}) {
  const root = mkdtempSync(join(tmpdir(), "humanise-version-"));
  mkdirSync(join(root, ".claude-plugin"), { recursive: true });
  writeFileSync(join(root, "package.json"), JSON.stringify({ version: versions.package ?? "1.0.0" }));
  writeFileSync(
    join(root, ".claude-plugin", "plugin.json"),
    JSON.stringify({ version: versions.plugin ?? "1.0.0" }),
  );
  writeFileSync(
    join(root, ".claude-plugin", "marketplace.json"),
    JSON.stringify({ plugins: [{ version: versions.marketplace ?? "1.0.0" }] }),
  );
  writeFileSync(
    join(root, ".release-please-manifest.json"),
    JSON.stringify({ ".": versions.release ?? "1.0.0" }),
  );
  writeFileSync(
    join(root, "README.md"),
    `![version](https://img.shields.io/badge/version-${versions.readme ?? "1.0.0"}-E9764A) <!-- x-release-please-version -->\n`,
  );
  return root;
}

test("all public version surfaces agree", () => {
  const state = readVersionState(fixture());
  assert.equal(state.canonical, "1.0.0");
  assert.deepEqual(versionProblems(state), []);
});

test("plugin drift fails with the exact surface", () => {
  const state = readVersionState(fixture({ plugin: "0.2.0" }));
  assert.deepEqual(versionProblems(state), [
    ".claude-plugin/plugin.json=0.2.0, expected 1.0.0",
  ]);
});

test("README badge drift fails", () => {
  const state = readVersionState(fixture({ readme: "1.0.1" }));
  assert.deepEqual(versionProblems(state), ["README.md=1.0.1, expected 1.0.0"]);
});

test("canonical version must be strict SemVer", () => {
  for (const version of ["1.0", "1.0.0-01", "1.0.0-alpha..1", "1.0.0-alpha."]) {
    const state = readVersionState(fixture({ package: version }));
    assert.match(versionProblems(state)[0], /strict SemVer/, version);
  }
});
