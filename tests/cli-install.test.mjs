import test, { after } from "node:test";
import assert from "node:assert/strict";
import {
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
} from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { PROVIDERS } from "../cli/providers.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CLI = join(ROOT, "cli", "bin", "cli.js");
const roots = [];

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "humanise-cli-"));
  const home = join(root, "home");
  const project = join(root, "project");
  mkdirSync(home);
  mkdirSync(project);
  roots.push(root);
  return { home, project };
}

function run(args, cwd, home) {
  return spawnSync(process.execPath, [CLI, ...args], {
    cwd,
    env: { ...process.env, HOME: home },
    encoding: "utf8",
  });
}

after(() => {
  for (const root of roots) rmSync(root, { recursive: true, force: true });
});

for (const [provider, config] of Object.entries(PROVIDERS)) {
  test(`${provider} installs and passes doctor at personal scope`, () => {
    const { home, project } = fixture();
    const install = run(["install", `--provider=${provider}`, "--global"], project, home);
    assert.equal(install.status, 0, install.stderr);
    assert.match(install.stdout, new RegExp(`Installed humanise for ${provider}`));
    assert.equal(existsSync(join(home, config.globalPath, "SKILL.md")), true);

    const doctor = run(["doctor", `--provider=${provider}`, "--global"], project, home);
    assert.equal(doctor.status, 0, doctor.stderr);
    assert.match(doctor.stdout, /OK  skill:/);
    assert.match(doctor.stdout, new RegExp(`Invoke in ${provider}:`));
  });

  test(`${provider} installs and passes doctor at project scope`, () => {
    const { home, project } = fixture();
    const install = run(["install", `--provider=${provider}`, "--project"], project, home);
    assert.equal(install.status, 0, install.stderr);
    assert.equal(existsSync(join(project, config.projectPath, "SKILL.md")), true);

    const doctor = run(["doctor", `--provider=${provider}`, "--project"], project, home);
    assert.equal(doctor.status, 0, doctor.stderr);
    assert.match(doctor.stdout, /OK  skill:/);
  });
}

test("project init creates private files protected by the local Git exclude", () => {
  const { home, project } = fixture();
  const gitInit = spawnSync("git", ["init", "--quiet"], { cwd: project, encoding: "utf8" });
  assert.equal(gitInit.status, 0, gitInit.stderr);

  const install = run(["install", "--provider=codex", "--project"], project, home);
  assert.equal(install.status, 0, install.stderr);
  const init = run(["init", "--provider=codex", "--project"], project, home);
  assert.equal(init.status, 0, init.stderr);

  const base = join(project, PROVIDERS.codex.projectPath);
  assert.equal(existsSync(join(base, "profile", "soul.md")), true);
  assert.equal(existsSync(join(base, "config.yml")), true);

  const exclude = readFileSync(join(project, ".git", "info", "exclude"), "utf8");
  assert.match(exclude, /\.agents\/skills\/humanise\/profile\//);
  assert.match(exclude, /\.agents\/skills\/humanise\/config\.yml/);

  const ignored = spawnSync(
    "git",
    ["check-ignore", "-q", ".agents/skills/humanise/profile/soul.md"],
    { cwd: project },
  );
  assert.equal(ignored.status, 0);

  const doctor = run(["doctor", "--provider=codex", "--project"], project, home);
  assert.equal(doctor.status, 0, doctor.stderr);
  assert.match(doctor.stdout, /OK  the private profile is not tracked by Git/);
});
