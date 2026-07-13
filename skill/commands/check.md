# humanise: check

Run the deterministic checker on a draft (no LLM). Wraps `evals/assertions/writing_checks.py`.

- Terminal: `npx humanise detect <file> [dialect] [medium]`
- In-tool: write the draft to a temp file, run `python3 evals/assertions/writing_checks.py <file> <dialect> [medium]`, then read the `_summary` (the `failed` list and the `structural_density` block).

Use to catch mechanical and structural risks. The checker never sees the meaning contract, the reader
or the user's voice, so a clean result is not proof that a draft is good. Treat advisory counts as
prompts for review rather than targets. Use a separate adversarial reviewer only when the stakes or
length justify it.
