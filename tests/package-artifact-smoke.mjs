import test, { after, before } from "node:test";
import assert from "node:assert/strict";
import {
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
} from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
let fixtureRoot;
let installedPackage;
let installedCli;

function run(command, args, options = {}) {
  return spawnSync(command, args, {
    encoding: "utf8",
    ...options,
    env: { ...process.env, ...options.env },
  });
}

function assertSuccess(result, label) {
  assert.equal(
    result.status,
    0,
    `${label} failed\nstdout:\n${result.stdout || ""}\nstderr:\n${result.stderr || ""}`,
  );
}

function assertInstalledSkill(skillRoot) {
  const skill = readFileSync(join(skillRoot, "SKILL.md"), "utf8");
  assert.match(skill, /^name: humanise$/m);

  for (const relativePath of [
    "commands/rewrite.md",
    "references/meaning-and-voice.md",
    "profile.template/soul.md",
    "config.example.yml",
  ]) {
    assert.equal(existsSync(join(skillRoot, relativePath)), true, `${relativePath} is missing`);
  }

  assert.equal(existsSync(join(skillRoot, "profile")), false);
  assert.equal(existsSync(join(skillRoot, "config.yml")), false);
}

function assertNoPrivateState(root) {
  const pending = [root];
  while (pending.length) {
    const current = pending.pop();
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const path = join(current, entry.name);
      if (entry.isDirectory()) {
        assert.notEqual(entry.name, "profile", `private profile directory packaged at ${path}`);
        assert.notEqual(entry.name, "__pycache__", `Python cache packaged at ${path}`);
        pending.push(path);
      } else {
        assert.notEqual(entry.name, "config.yml", `private configuration packaged at ${path}`);
        assert.equal(entry.name.endsWith(".pyc"), false, `Python bytecode packaged at ${path}`);
      }
    }
  }
}

before(() => {
  fixtureRoot = mkdtempSync(join(tmpdir(), "humanise-package-artifact-"));
  const packDirectory = join(fixtureRoot, "pack");
  const consumer = join(fixtureRoot, "consumer");
  const cache = join(fixtureRoot, "npm-cache");
  mkdirSync(packDirectory);
  mkdirSync(consumer);

  const pack = run(
    "npm",
    ["pack", "--pack-destination", packDirectory, "--cache", cache],
    { cwd: ROOT },
  );
  assertSuccess(pack, "npm pack");

  const archives = readdirSync(packDirectory).filter((file) => file.endsWith(".tgz"));
  assert.deepEqual(archives, ["humanise-1.0.0.tgz"]);

  const install = run(
    "npm",
    [
      "install",
      "--ignore-scripts",
      "--no-audit",
      "--no-fund",
      "--prefix",
      consumer,
      "--cache",
      cache,
      join(packDirectory, archives[0]),
    ],
    { cwd: consumer, env: { HOME: join(fixtureRoot, "install-home") } },
  );
  assertSuccess(install, "npm install from tarball");

  installedPackage = join(consumer, "node_modules", "humanise");
  installedCli = join(installedPackage, "cli", "bin", "cli.js");
});

after(() => {
  if (fixtureRoot) rmSync(fixtureRoot, { recursive: true, force: true });
});

test("the npm tarball contains the named skill and no private profile state", () => {
  const pkg = JSON.parse(readFileSync(join(installedPackage, "package.json"), "utf8"));
  assert.equal(pkg.name, "humanise");
  assert.equal(pkg.version, "1.0.0");
  assert.equal(existsSync(join(installedPackage, "skill")), false);
  assertInstalledSkill(join(installedPackage, "dist", "humanise"));
  assertNoPrivateState(installedPackage);
});

for (const [provider, relativePath] of [
  ["codex", ".agents/skills/humanise"],
  ["claude-code", ".claude/skills/humanise"],
]) {
  test(`the npm tarball installs and passes doctor for ${provider} in an isolated HOME`, () => {
    const home = join(fixtureRoot, `${provider}-home`);
    const project = join(fixtureRoot, `${provider}-project`);
    mkdirSync(home);
    mkdirSync(project);
    const env = { HOME: home };

    const install = run(
      process.execPath,
      [installedCli, "install", `--provider=${provider}`, "--global"],
      { cwd: project, env },
    );
    assertSuccess(install, `${provider} install`);

    const skillRoot = join(home, relativePath);
    assertInstalledSkill(skillRoot);

    const doctor = run(
      process.execPath,
      [installedCli, "doctor", `--provider=${provider}`, "--global"],
      { cwd: project, env },
    );
    assertSuccess(doctor, `${provider} doctor`);
    assert.match(doctor.stdout, /OK  skill:/);
  });
}
