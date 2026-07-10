# Platforms

New here? [getting-started.md](getting-started.md) walks through install end to end. This page is the per-tool reference.

humanise is one portable skill (`skill/`) plus a thin adapter per platform. The skill content is identical across platforms; only the entry point differs.

## Claude Code

Two options:

- **Plugin:** the repo ships `.claude-plugin/plugin.json`. Add the repo as a plugin (or through a marketplace) and the skill becomes available. Verify the manifest against the current Claude Code plugin schema before publishing; the field names move occasionally.
- **Skill copy:** copy `skill/` into your Claude skills directory as `humanise/`. It triggers on writing and editing tasks per its description.

## Codex

Codex reads `AGENTS.md` at the repo root, which tells it to apply the skill in `skill/SKILL.md` when writing prose. Open the repo in Codex and it picks this up.

## Google Antigravity (Gemini CLI)

Gemini CLI and Antigravity read `GEMINI.md` at the repo root, which does the same.

## Any other agent

Point your agent at `skill/SKILL.md` and `skill/profile/`. The skill is plain Markdown plus a Python checker (`skill/evals/assertions/writing_checks.py`); nothing is platform-specific except the entry-point files above.

## The checker

The one dependency is Python 3 (standard library only) for `writing_checks.py` and `selftest.py`. No packages to install.
