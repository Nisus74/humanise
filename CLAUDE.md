# CLAUDE.md

Guidance for Claude (and contributors) working on **humanise**: an open-source skill that strips AI tells from writing and drafts in a specific person's voice. Cross-platform (Claude Code, Codex, Gemini, Cursor and more), shipped as a skill plus an npm CLI.

## The one rule: body vs soul

- **Body (engine)**: `skill/SKILL.md`, `skill/references/`, `skill/evals/`, `skill/agents/`, `skill/commands/`, `skill/scripts/`. Universal and shared. Improve this.
- **Soul (profile)**: `skill/profile/` holds a user's own soul, plus the voice corpus (flat `sample-*.md` files) and fingerprint. Personal. **Never commit a `profile/`. Never put one person's voice into the engine.** The repo ships `skill/profile.template/` and `skill/profile.example/` only.

If a change only helps one person's writing, it's a profile change (their fork). If it helps everyone, it's an engine change (a PR).

## Repo map

- `skill/`: the source skill. This is what ships and installs.
- `cli/`: the zero-dependency Node CLI (`bin/cli.js`) and the provider map (`providers.mjs`).
- `scripts/build.mjs`: compiles `skill/` into `dist/<provider>/`. **`dist/` is generated; never hand-edit it.** Edit `skill/` and rebuild.
- `docs/`: `SETUP.md`, `body-and-soul.md`, `platforms.md`, `DEVELOP.md`.
- The detector is Python (`skill/evals/assertions/writing_checks.py`), standard library only. The CLI shells to it; it is not ported to JS.
- Tests and evals live in `skill/evals/assertions/`: `selftest.py` is the held-in battery (`npm test`); `run_all.py` runs the full `evals.json` suite into `benchmark.json`. (Top-level `tests/` is a placeholder.)
- `skill/config.example.yml`: the per-user engine config to copy to `skill/config.yml` (gitignored). Sets dialect, register, channels and a custom slop overlay.
- `.claude-plugin/plugin.json`: the plugin manifest. Release-critical; verify it and the per-harness skill paths before publishing.

## The acceptance gate (read before changing the engine)

Every engine change clears the gate in `skill/evals/self-harness-loop.md`:

1. **Held-in green:** `npm test` (the Python selftest) passes. Add a fixture if you add a detector.
2. **Held-out not regressed:** the pairwise voice test (`skill/evals/indistinguishability.md`) does not get worse.
3. **Auditable:** add a `skill/CHANGELOG.md` entry (target, surface, evidence, eval result).

Keep edits minimal: change only the surface the failure needs, preserve what already passes, no broad rewrites.

## Commands

```
npm run build                                  compile skill/ -> dist/<provider>/
npm test                                       held-in selftest (Python)
node cli/bin/cli.js detect <file> [dialect] [medium]    run the checker on a draft
```

## Conventions

- **Three agent-guidance files, one rule set.** `CLAUDE.md` (here), `AGENTS.md` (Codex and others), and `GEMINI.md` (Gemini, Antigravity) each restate the body/soul rule, the "don't sweep code/config" rule, and how to run the checker. They drift: change a shared rule in one, change all three. Canonical checker entry point is `node cli/bin/cli.js detect` (it shells to `writing_checks.py`); `python3 skill/evals/assertions/writing_checks.py <file> <dialect> [medium]` is the same checker without the CLI.
- **Dogfood the prose.** Write the repo's own docs (README, `docs/`, this file) to humanise's standard: no em dashes or slop, and specifics over fluff. Run the checker on substantial docs before committing (`node cli/bin/cli.js detect <file>`). A writing tool whose own README reads like AI undercuts itself.
- No new dependencies without a strong reason (CLI = Node built-ins; checker = Python stdlib).
- Don't apply the prose sweep to code, config, or quoted material (see SKILL.md, "When to apply").
- Rules live in `references/` and detectors in `writing_checks.py`; subagents in `agents/`.
- Add a provider: a row in `cli/providers.mjs` (`PROVIDERS` and `DETECT`), then rebuild.
