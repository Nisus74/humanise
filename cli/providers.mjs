// One source of truth for provider discovery, installation paths and the
// invocation users see after install. Project and user paths differ on some
// hosts, so never derive one from the other.
export const PROVIDERS = {
  "claude-code": {
    projectPath: ".claude/skills/humanise",
    globalPath: ".claude/skills/humanise",
    markers: [".claude"],
    invoke: "/humanise",
  },
  cursor: {
    projectPath: ".cursor/skills/humanise",
    globalPath: ".cursor/skills/humanise",
    markers: [".cursor"],
    invoke: "/humanise",
  },
  gemini: {
    projectPath: ".gemini/skills/humanise",
    globalPath: ".gemini/skills/humanise",
    markers: [".gemini"],
    invoke: "/skills enable humanise, then ask normally",
  },
  codex: {
    projectPath: ".agents/skills/humanise",
    globalPath: ".agents/skills/humanise",
    markers: [".agents", ".codex"],
    invoke: "$humanise",
  },
  github: {
    projectPath: ".github/skills/humanise",
    globalPath: ".copilot/skills/humanise",
    // .github is deliberately not a marker. Almost every GitHub repository has
    // one, whether or not the user runs Copilot.
    markers: [],
    invoke: "/humanise",
  },
  opencode: {
    projectPath: ".opencode/skills/humanise",
    globalPath: ".config/opencode/skills/humanise",
    markers: [".opencode"],
    invoke: "ask normally or load the humanise skill",
  },
  universal: {
    projectPath: "humanise",
    globalPath: ".agents/skills/humanise",
    markers: [],
    invoke: "ask your agent to use the humanise skill",
  },
};

export function detectProviders(cwd, exists) {
  const found = [];
  for (const [provider, config] of Object.entries(PROVIDERS)) {
    if (config.markers.some((marker) => exists(cwd, marker))) found.push(provider);
  }
  return [...new Set(found)];
}
