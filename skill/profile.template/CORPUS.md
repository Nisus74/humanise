# Voice corpus

Real samples of your writing, annotated so the skill learns the decisions behind your voice. One sample
is enough to begin calibration. Several channels and edit pairs make the model reliable.

## What to add

Start with one sample for the task in front of you. Grow towards 5 to 10 across the channels and
relationships you use. Rough is fine; it is ground truth rather than a showcase. A proposed draft paired
with your final edit is especially valuable.

The fastest way to collect them is `scripts/corpus-questionnaire.md`: it walks you channel by channel with concrete fetch prompts and drafts the annotations by asking, so you correct rather than write from scratch.

One file per sample, kept flat in `profile/` (no subfolders), named `sample-<channel>-<short-description>.md` (e.g. `sample-email-q3-board-update.md`, `sample-long-form-strategy-memo.md`), using `SAMPLE_TEMPLATE.md`. The channel in the filename, and the `channel:` field in the frontmatter, let the generator spot per-channel habits.

## How it's used

The fingerprint (`voice-fingerprint.md`) is synthesised from these samples by `scripts/generate-fingerprint.md`. When you add samples, regenerate the fingerprint. The samples are the territory; the fingerprint is the map.

## Annotation

Fill in every field of `SAMPLE_TEMPLATE.md`. Name decisions rather than generic qualities: “states the
miss before the recovery plan” is evidence; “clear communication” is not. Record assistance honestly so
the fingerprint can downweight model-written or heavily polished samples.
