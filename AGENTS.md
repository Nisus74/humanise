# AGENTS.md

This repo is a writing skill, not an app. If you are an AI coding agent (Codex and others read this file), apply the **humanise** skill whenever you write or edit prose for the user: commit-message bodies aside, anything human-facing (READMEs, docs, posts, emails, PR descriptions).

How to use it:

1. Read `skill/SKILL.md` for the workflow (assess, draft from the user's corpus, two-pass sweep, self-critique, verify).
2. Read the user's `skill/profile/` (their `soul.md`, `voice-fingerprint.md`, `absolute-rules.md`) if present. If there's no `profile/`, tell the user to run the quickstart in `README.md` and fall back to the engine defaults.
3. Run the checker on anything substantial: `python3 skill/evals/assertions/writing_checks.py <draft-file> <dialect> [medium]`.

The rules in `skill/references/` are the shared engine; the voice in `skill/profile/` is the user's. Don't apply the prose sweep to code, config, or quoted material (see the "When to apply, and when to hold off" section in `skill/SKILL.md`).

Engine changes clear the acceptance gate in `skill/evals/self-harness-loop.md`, runnable end to end via `/humanise improve`. Never tune a change against `skill/evals/holdout-evals.json` (reserved held-out), and treat `skill/profile/learning/` as soul: the user's verbatim edit history, never committed.
