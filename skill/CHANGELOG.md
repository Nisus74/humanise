# Changelog: humanise (engine)

Auditable lineage of engine changes, per `evals/self-harness-loop.md`. Each entry names the target, surface, evidence, and eval result. Newest first.

## 2026-06-24 — impeccable.design rule additions

**Target:** missing 2025-era tells. **Surface:** added stolen-engineer / marketing words (load-bearing, highest-leverage, biggest unlock, data-driven, elevate, underscore) to `SEVERITY_2_3_SLOP`; openers (gone are the days, let's dive in, whether you're) to `SLOP_OPENERS`; a `negation_pivot` detector ("less about X, more about Y") to the binary-contrast family; dictionary section 2.6 plus a structural-tells variant note. **Evidence:** impeccable.design STYLE.md denylist (Paul Bakaus). **Result:** selftest green with a new fixture covering the additions.

## 2026-06-24 — initial open-source release

Engine extracted from a personal writing skill into a forkable body/soul structure. The engine (`SKILL.md`, `references/`, `evals/`, `scripts/`) is universal; the profile (soul, fingerprint, corpus, dialect, absolute rules) is per-user. Ships a blank `profile.template/`, a scrubbed `profile.example/`, the fingerprint generator, the held-in `selftest.py`, dialect packs (en-AU, en-US, en-GB), and the Self-Harness self-improvement loop as the contribution gate. Defines two agents (`agents/adversarial-reviewer.md`, `agents/indistinguishability-judge.md`) and wires them into the verification steps and the self-harness gate. selftest green on the generic example evals.
