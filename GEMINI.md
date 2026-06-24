# GEMINI.md

Gemini CLI and Google Antigravity read this file. This repo is the **humanise** writing skill: it makes AI-generated prose sound like a specific human wrote it.

Apply it whenever you write or edit human-facing prose for the user:

1. Read `skill/SKILL.md` for the workflow.
2. Read the user's `skill/profile/` (`soul.md`, `voice-fingerprint.md`, `absolute-rules.md`) if it exists; otherwise point them at the quickstart in `README.md`.
3. Run `python3 skill/evals/assertions/writing_checks.py <draft-file> <dialect> [medium]` on substantial drafts.

The engine (`skill/references/`) is shared; the voice (`skill/profile/`) is the user's. Leave code, config, and quoted material out of the prose sweep.
