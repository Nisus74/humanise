# Tests

The test suite lives with the skill, at `../skill/evals/`. It runs without a model.

## Run it

```
cd ../skill/evals/assertions
python3 selftest.py
```

Or from the repo root: `./scripts/run-checks.sh`.

Green means the engine catches what it claims and every example eval resolves. CI runs this on every push and PR (`.github/workflows/ci.yml`).

## What's in it

- `selftest.py`: the **held-in** regression suite. Fixed clean and sloppy fixtures, plus a check that every eval in `evals.json` is gradeable. This is the gate every engine change must keep green.
- `writing_checks.py`: the assertion engine, also used live by the skill's mechanical sweep.
- `evals.json`: example evals across channels; replace or extend with your own.
- `indistinguishability.md`: the **held-out** pairwise voice test (judge-based, not run from this script).
- `self-harness-loop.md`: how a change is proposed, gated, and promoted.

See `../skill/evals/self-harness-loop.md` for the full acceptance model.
