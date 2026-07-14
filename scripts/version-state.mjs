import { readFileSync } from "node:fs";
import { join } from "node:path";

const SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$/;

function json(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

export function readVersionState(root) {
  const canonical = json(join(root, "package.json")).version;
  const plugin = json(join(root, ".claude-plugin", "plugin.json")).version;
  const marketplace = json(join(root, ".claude-plugin", "marketplace.json")).plugins?.[0]?.version;
  const release = json(join(root, ".release-please-manifest.json"))["."];
  const readme = readFileSync(join(root, "README.md"), "utf8");
  const badge = readme.match(/shields\.io\/badge\/version-([0-9A-Za-z.+-]+)-/i)?.[1];
  return {
    canonical,
    surfaces: {
      ".claude-plugin/plugin.json": plugin,
      ".claude-plugin/marketplace.json": marketplace,
      ".release-please-manifest.json": release,
      "README.md": badge,
    },
  };
}

export function versionProblems(state) {
  const problems = [];
  if (!SEMVER.test(state.canonical ?? "")) {
    problems.push(`package.json=${state.canonical ?? "missing"} is not strict SemVer`);
    return problems;
  }
  for (const [surface, value] of Object.entries(state.surfaces)) {
    if (value !== state.canonical) {
      problems.push(`${surface}=${value ?? "missing"}, expected ${state.canonical}`);
    }
  }
  return problems;
}
