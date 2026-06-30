# Body and soul

humanise is built on one idea: the rules that strip AI tells are universal, but the voice that replaces them is personal. So the skill splits in two.

## The body

The engine. Shared by everyone, never personalised:

- `references/ai-slop-dictionary.md` and `references/structural-tells.md`: the vocabulary and structural patterns that flag writing as machine-made.
- `references/mechanical-sweep.md` and `evals/assertions/writing_checks.py`: the two-pass sweep and the Python checker that automates most of it.
- `references/channel-playbooks.md`, `references/tone-register.md`, `references/dialect-*.md`: the coverage model across any channel, register and dialect.
- `evals/`: the test harness and the self-improvement loop.

AI tells are artefacts of how models generate text; they aren't facts about you. Everyone runs the same body.

## The soul

The profile. Entirely yours, never shared upstream:

- `soul.md`: what you believe about writing and won't budge on. The convictions, the taste, the hills you'll die on. This is the part the rules can't give you.
- `voice-fingerprint.md`: how you actually write, generated from your samples: opening moves, sentence habits, the things you never do.
- `sample-*.md` files: real samples of your writing, flat in `profile/`. The ground truth.
- `absolute-rules.md`, `identity.md`, `channels.md`: your dialect, your non-negotiables, your channel set.

## Why the split matters

A mechanical fingerprint can make writing clean and even rhythmically yours. It can't give it a point of view. That's what the soul is for: the fingerprint captures *how* you write, the soul captures *why*. When a mechanical rule and a conviction disagree, the soul wins.

It's also what makes humanise forkable. The body is the open-source project everyone improves together, behind a regression gate. The soul is the thing you keep private and never commit. Fork the body; transplant your soul.
