# CLAUDE.md

Guidance for Claude (and contributors) working on **humanise**: an open-source skill that strips AI tells from writing and drafts in a specific person's voice. Cross-platform (Claude Code, Codex, Gemini, Cursor, and more), shipped as a skill plus an npm CLI.

## The one rule: body vs soul

- **Body (engine)**: `skill/SKILL.md`, `skill/references/`, `skill/evals/`, `skill/agents/`, `skill/commands/`, `skill/scripts/`. Universal and shared. Improve this.
- **Soul (profile)**: `skill/profile/` holds a user's own soul, fingerprint, and corpus. Personal. **Never commit a `profile/`. Never put one person's voice into the engine.** The repo ships `profile.template/` and `profile.example/` only.

If a change only helps one person's writing, it's a profile change (their fork). If it helps everyone, it's an engine change (a PR).

## Repo map

- `skill/`: the source skill. This is what ships and installs.
- `cli/`: the zero-dependency Node CLI (`bin/cli.js`) and the provider map (`providers.mjs`).
- `scripts/build.mjs`: compiles `skill/` into `dist/<provider>/`. **`dist/` is generated; never hand-edit it.** Edit `skill/` and rebuild.
- `docs/`: setup, body-and-soul, platforms, DEVELOP.
- The detector is Python (`skill/evals/assertions/writing_checks.py`), standard library only. The CLI shells to it; it is not ported to JS.

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
node cli/bin/cli.js detect <file> [dialect]    run the checker on a draft
```

## Conventions

- **Dogfood the prose.** Write the repo's own docs (README, `docs/`, this file) to humanise's standard: no em dashes, no slop, specifics over fluff. Run the checker on substantial docs before committing (`node cli/bin/cli.js detect <file>`). A writing tool whose own README reads like AI undercuts itself.
- No new dependencies without a strong reason (CLI = Node built-ins; checker = Python stdlib).
- Don't apply the prose sweep to code, config, or quoted material (see SKILL.md, "When to apply").
- Rules live in `references/`, detectors in `writing_checks.py`, subagents in `agents/`.
- Add a provider: a row in `cli/providers.mjs` (`PROVIDERS` and `DETECT`), then rebuild.
