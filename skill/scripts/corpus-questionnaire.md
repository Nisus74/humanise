# Corpus questionnaire: pull your samples fast

The corpus is valuable and easy to turn into homework. Start with one sample related to the current
task. Use this questionnaire later to deepen the channels that matter.

It pairs with `generate-fingerprint.md`: this collects the samples, that turns them into your fingerprint.

## How to run it

Work one channel at a time. The model gives a concrete fetch prompt, the user pastes what they have,
and the model drafts the annotation for correction. Stop after one when onboarding. Continue towards
5 to 10 only when the user wants deeper coverage.

## The fetch prompts (concrete beats "share some writing")

Don't ask "share some writing". Ask for a specific, recent, real artefact:

- **LinkedIn / blog:** "Paste your last LinkedIn post, or the most recent thing you published." (Start here: the most AI-prone channels.)
- **Email:** "Paste the last substantial email you sent that wasn't logistics: a pitch, a piece of feedback, a follow-up after a meeting."
- **Slack / chat:** "Paste your bluntest internal message this week, the one where you said the real thing."
- **Investor update / board paper / status update:** "Paste your last update to investors or the board, or the last status update you wrote."
- **Long-form (memo, PRD, strategy):** "Paste a memo, PRD intro, or strategy doc. Even one section is enough, and long-form is where voice breaks worst, so it matters most."

Aim for spread across channels: a few covered beats ten LinkedIn posts. Rough is fine; this is ground truth, and polish isn't the point. An unedited sample is worth more than a polished one (record that in `dogfood_status`).

## Extract the annotations by asking (don't leave them blank)

Do not make the writer fill annotations cold. Ask two or three targeted questions:

- "What were you trying to do here, in one line?" feeds `context`.
- "What about this one lands for you? What would you have hated to see written the bland way?" feeds `what_worked`.
- "What decision in here feels like yours: what you included, judged, put first or left out?" feeds
  `characteristic_of_you`. If the answer is generic, push once: "Point to the sentence and name the choice."
- "How much help did this receive before it was sent?" feeds `assistance_status`.

The model then writes the sample to `profile/sample-<channel>-<short-description>.md` using `SAMPLE_TEMPLATE.md`, annotations filled from the answers. You correct anything that doesn't ring true.

## When you're done

Run `scripts/generate-fingerprint.md` to synthesise `profile/voice-fingerprint.md` and build the voiceprint baseline. Refresh both after roughly every five new samples, or when a channel first gets real coverage.

## Discipline

- Real over representative. The sample you actually sent beats the one you'd write for show.
- Specific over generic. "Opens on the number, not the story" beats "data-driven". If an annotation would fit any sample, it's too vague.
- Spread over volume. Five channels lightly covered beats one channel ten times.
- Don't block on volume. One real sample plus the user's correction is a working start.
