# Deepen your voice profile

Start with [Getting started](getting-started.md) and get one useful rewrite first. This page takes the
next step: turning that one-sample calibration into a reliable multi-channel profile.

## The first three minutes

Invoke humanise and ask it to initialise your voice. The agent will create `profile/` and `config.yml`
inside the installed skill when they do not exist.

Give it:

1. One short piece you wrote and like.
2. The reader and relationship.
3. What you wanted the writing to achieve.
4. Any part that feels particularly like you.

Choose between the resulting rewrite directions and correct the closest one. The resulting voice
decisions remain provisional until more evidence confirms them.

## Build a useful profile

Grow towards five to ten real samples across the channels you use. Prefer:

- writing you actually sent or published;
- raw or lightly edited work;
- examples with different relationships and stakes;
- the skill's draft paired with your final edit;
- short negative examples with a precise reason you rejected them.

Save samples as `profile/sample-<channel>-<slug>.md` using `profile/SAMPLE_TEMPLATE.md`. The guided
questionnaire in `scripts/corpus-questionnaire.md` helps collect and annotate them.

## Write the soul after seeing real choices

`profile/soul.md` records what you believe about writing and what you will not trade away. Use claims
specific enough that another writer might disagree:

- "I never use a number I cannot source."
- "I state bad news before the recovery plan."
- "I challenge the decision while respecting the person."

Avoid generic values such as clarity, authenticity and impact. They do not distinguish a voice.

Keep `profile/absolute-rules.md` to explicit non-negotiables. Inferred habits belong in
`profile/voice-decisions.md` until the evidence is strong.

## Model relationships

Channel alone is not enough. Use `profile/relationships.md` to record confirmed differences between
writing to a trusted colleague, a customer with a problem, an investor, a regulator or a public
audience. Do not create an overlay without direct evidence.

## Generate the fingerprint

After several useful samples, ask humanise to run `fingerprint`. It will synthesise:

- what you choose to mention;
- how you reach and express judgements;
- how you handle readers and disagreement;
- how you structure a case;
- cadence, diction and punctuation;
- channel and relationship gaps;
- evidence and confidence for every pattern.

Regenerate after roughly five useful additions or when a channel first gets direct coverage.

## Configuration

The canonical configuration is `config.yml` beside `SKILL.md`. Set your name, dialect, default
register, profile directory and common channels there. Do not create a second configuration inside
`profile/`.

## Keep it private

Run the installation diagnostic whenever the skill moves:

```sh
npx humanise@1.0.0 doctor --provider=<name> [--project]
```

For a project install, confirm the profile does not appear in `git status` and is not returned by
`git ls-files`. Redact samples before saving them.
