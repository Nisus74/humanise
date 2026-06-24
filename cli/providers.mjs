// Single source of truth: which harnesses humanise supports, and where the skill
// folder lands inside a project for each. The build emits dist/<provider>/<path>;
// `humanise install` copies that into the user's project (or ~/ for a global install).
export const PROVIDERS = {
  "claude-code": ".claude/skills/humanise",
  cursor: ".cursor/skills/humanise",
  gemini: ".gemini/skills/humanise",
  codex: ".agents/skills/humanise",
  github: ".github/skills/humanise",
  opencode: ".opencode/skills/humanise",
  universal: "humanise",
};

// Heuristic harness detection: which marker dirs in the project root imply which provider.
export const DETECT = {
  ".claude": "claude-code",
  ".cursor": "cursor",
  ".gemini": "gemini",
  ".agents": "codex",
  ".codex": "codex",
  ".opencode": "opencode",
  ".github": "github",
};
