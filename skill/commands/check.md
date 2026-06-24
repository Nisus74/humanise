# /humanise check

Run the deterministic checker on a draft (no LLM). Wraps `evals/assertions/writing_checks.py`.

- Terminal: `npx humanise detect <file> [dialect] [medium]`
- In-tool: write the draft to a temp file, run `python3 evals/assertions/writing_checks.py <file> <dialect> [medium]`, then read the `_summary` (the `failed` list and the `structural_density` block).

Use to gate a draft before shipping, or in CI. The checker is the body; it never sees the soul, so a clean checker run is necessary, not sufficient. Pair it with the read-aloud test and, for external pieces, the adversarial reviewer (`agents/adversarial-reviewer.md`).
