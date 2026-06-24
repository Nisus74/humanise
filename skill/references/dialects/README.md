# Dialect packs

Each pack is the spelling and idiom essence of one dialect. `en-AU`, `en-US`, and `en-GB` ship. The cross-variant switching logic and consistency checks live in `../cultural-calibration.md`; the matching regex lists live in `../../evals/assertions/writing_checks.py`.

Set your dialect in `config.yml` (`dialect: en-AU`). Audiences that need a different variant are handled per-piece via the audience tag.

**Adding a dialect** (a good first contribution): add `<code>.md` here, add the spelling lists to `writing_checks.py`, add a fixture to `selftest.py`, and confirm the suite stays green. See `../../CONTRIBUTING.md`.
