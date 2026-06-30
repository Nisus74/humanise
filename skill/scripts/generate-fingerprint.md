# Generate your voice fingerprint

Turns your writing samples into `profile/voice-fingerprint.md`, the distilled model the skill reads on every draft. Run it after adding `profile/sample-*.md` samples, and again whenever you add more.

This is a prompt and procedure, not a binary: run it with Claude (or any capable model) pointed at your corpus. The method is "extract structured descriptors from real samples, then write to those descriptors", which beats open-ended "write like me".

## Inputs

- Every `profile/sample-*.md` and its annotations.
- `profile/identity.md` and `profile/soul.md` for orientation.

## Procedure

1. **Read every sample raw.** Don't skim. Note what recurs across samples versus what's one-off.
2. **Extract descriptors, with evidence.** For each section below, name concrete, checkable habits and cite at least one verbatim example. Anything you can't ground in a sample, mark _(thin signal)_ or leave out.
3. **Measure the tripwires.** Run `evals/assertions/writing_checks.py` on two or three samples and record the ranges (sentence-length spread, contraction types, dialect markers, burstiness). These become the diagnostic table, as tripwires not targets. Then build the machine-readable twin: `scripts/build_voiceprint.py --corpus profile` writes per-feature mean and standard deviation across your samples to `profile/voiceprint.json`, which `humanise voiceprint <file>` uses to flag a draft that drifts from your own distribution (advisory: a distance, never a target).
4. **Write `voice-fingerprint.md`** to the structure below.
5. **Note the gaps.** Which channels have no samples? List them so the skill knows where it's inferring.

## Output structure (write to profile/voice-fingerprint.md)

Write each behavioural section as **moves**, not adjectives. A move names a concrete habit, shows a verbatim example from the corpus, and where it sharpens the picture, an anti-example: the bland version you would never write. "Opens investor updates on the quarter's biggest number, never on a pleasantry" is a move; "clear and direct" is an adjective. The stats table is one section, not the whole fingerprint; the moves are what make a draft sound like the writer rather than merely clean.

- **Status and evidence sources:** what it's built from; what can't be re-verified.
- **The absolute rules:** pull from `absolute-rules.md`; the few that override everything.
- **Opening moves** and **closing moves:** the shapes that recur, each with a verbatim example and, where it sharpens it, an anti-example.
- **Recurring phrasings** and **words that never appear.**
- **Sentence habits:** length variation (burstiness), word choice (perplexity), active voice, fragment discipline.
- **How disagreement is handled. Humour. Things never done.**
- **Channel-specific adjustments:** per channel with samples; mark the rest thin-signal.
- **Calibration examples:** verbatim sentences to anchor drafting.
- **Diagnostic profile:** the measured tripwire table (the human-readable side; `profile/voiceprint.json` is its machine-readable twin, built in step 3).

## Discipline

- Specific over generic. "Opens on the ask, not a pleasantry" beats "clear and direct".
- Evidence or it doesn't go in. A fingerprint of guesses produces generic output.
- Tripwires, not quotas. The numbers flag a draft for another look; never pad prose to hit them.
- Regenerate, don't patch, when the corpus grows enough to change the picture. Promotion of a new pattern goes through the gate in `evals/self-harness-loop.md`.
