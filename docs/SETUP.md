# Setup: your first 15 minutes

The goal is a working, personalised skill, fast. The corpus is the bottleneck for everyone, so the steps are ordered to get you drafting in your voice with the least friction.

## 1. Make your profile (1 min)

```
cp -r profile.template profile     # blank
# or
cp -r profile.example profile      # start from a real example, then replace it
```

## 2. Write your soul and absolute rules (5 min)

Open `profile/soul.md` and write your convictions: concrete, first-person, no vibes. `profile.example/soul.md` is the bar. Then set `profile/identity.md` (name, dialect, role) and `profile/absolute-rules.md` (your 3 to 6 non-negotiables).

This alone gets you usable output with a point of view, before any samples.

## 3. Add samples and generate your fingerprint (8 min)

Drop 5 to 10 real samples into `profile/voice-corpus/` (one file each, per `SAMPLE_TEMPLATE.md`, in channel subfolders). Then run `scripts/generate-fingerprint.md` with Claude pointed at the corpus, and paste the result into `profile/voice-fingerprint.md`.

More samples, better voice. LinkedIn and blog first; they're the most AI-prone.

## 4. Set config (1 min)

```
cp config.example.yml config.yml
```

Set `name`, `dialect`, `default_register`, and `channels`.

## 5. Check the engine

```
cd evals/assertions && python3 selftest.py
```

Green means the checker works. Now ask Claude to write something with the skill active, and run `writing_checks.py` on the draft.

## Keeping it sharp

As you accept and reject the skill's output, log the patterns per `references/memory-loop.md`, and promote the confirmed ones into the fingerprint through the gate in `evals/self-harness-loop.md`. Regenerate the fingerprint when the corpus grows.
