# Voice corpus

Real samples of your writing, annotated so the skill learns what your voice actually sounds like. Without this, the skill only knows what to avoid; it doesn't know what to aim for. This is the single highest-leverage asset in your profile.

## What to add

5 to 10 samples to start, more over time. Rough is fine; this is ground truth, not a showcase. Prioritise the channels you write most and the ones most prone to sounding AI-generated (LinkedIn, blog, email, anything public).

The fastest way to collect them is `scripts/corpus-questionnaire.md`: it walks you channel by channel with concrete fetch prompts and drafts the annotations by asking, so you correct rather than write from scratch.

One file per sample, named `YYYY-MM-DD-short-description.md`, using `SAMPLE_TEMPLATE.md`. Drop them into a subfolder per channel (`linkedin/`, `email/`, `blog/`, etc.) so the generator can spot per-channel habits.

## How it's used

The fingerprint (`../voice-fingerprint.md`) is synthesised from these samples by `scripts/generate-fingerprint.md`. When you add samples, regenerate the fingerprint. The samples are the territory; the fingerprint is the map.

## Annotation

Fill in every field of `SAMPLE_TEMPLATE.md`. The `what_worked` and `characteristic_of_you` fields matter most: name the specific moves ("opens on the ask, not a pleasantry"; "uses numbers instead of adjectives for size"), not generic praise ("clear communication"). If you catch yourself writing something that would fit any sample, force yourself to be specific.
