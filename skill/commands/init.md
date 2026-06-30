# /humanise init

One-time setup. Writes the user's voice profile so every later command sounds like them. Run when the user says "set up humanise", runs `/humanise init`, or has no `profile/` yet.

Steps:

1. If `profile/` doesn't exist, copy `profile.template/` to `profile/` (or the user runs `npx humanise init` in the terminal).
2. Ask the soul questions and write `profile/soul.md`: what they believe about writing, what they'll die on, what they refuse to do, how they want to sound. Concrete, first-person; `profile.example/soul.md` is the bar. Reject vibes ("authentic storytelling").
3. Set `profile/identity.md` (name, dialect, role, audiences) and copy `config.example.yml` to `profile/config.yml` (name, dialect, channels).
4. Set `profile/absolute-rules.md` (their 3 to 6 non-negotiables).
5. Collect 5 to 10 writing samples with `scripts/corpus-questionnaire.md` (it gives a concrete fetch prompt per channel and fills the annotations by asking); save them flat in `profile/` as `sample-<channel>-<slug>.md`. Then run `scripts/generate-fingerprint.md` to write `profile/voice-fingerprint.md` and build the voiceprint baseline.
6. Confirm the engine: `npx humanise detect <file>`, or `python3 evals/assertions/writing_checks.py <file> <dialect>`.

The soul and the corpus are the whole point. Don't skip them; without them the output is competent and anonymous.
