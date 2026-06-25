# Changelog: humanise (engine)

Auditable lineage of engine changes, per `evals/self-harness-loop.md`. Each entry names the target, surface, evidence, and eval result. Newest first.

## 2026-06-25 — checker performance and aggregator cleanup (no behaviour change)

**Target:** wasted work and minor duplication in the detector and eval aggregator. **Surface:** in `evals/assertions/writing_checks.py`, compiled the dialect-ending, contraction, triple, sentence-template and transition-slop regexes once at import rather than per call; cached per-term slop matchers (`_term_re`); scanned the five binary-contrast regexes once per draft and shared the result between `structural_tell_count` and `binary_contrast_density`; hoisted the metaphorical-`landscape` regex and the `ACADEMIC_VERBS + ACADEMIC_PHRASES` join to module scope; extracted the transition-slop list to a reusable module constant; unified the unused `en_dash_count(allow_in_ranges=False)` return shape with the default path. In `evals/assertions/run_all.py`, aggregated advisory flags with `collections.Counter` and per-channel totals with `defaultdict` (returned as plain dicts). **Evidence:** pure refactor, no rule or threshold changed; full `all_checks` output diffed against the prior version across 10 drafts (AusE, US, sloppy, long-form, docx, empty, contraction-heavy, transition-slop) and was identical, the only intentional difference being the dead `allow_in_ranges=False` branch now returning the default branch's keys. **Result:** selftest green; held-out pairwise voice test unaffected (no detector behaviour changed).

## 2026-06-24 — impeccable.design rule additions

**Target:** missing 2025-era tells. **Surface:** added stolen-engineer / marketing words (load-bearing, highest-leverage, biggest unlock, data-driven, elevate, underscore) to `SEVERITY_2_3_SLOP`; openers (gone are the days, let's dive in, whether you're) to `SLOP_OPENERS`; a `negation_pivot` detector ("less about X, more about Y") to the binary-contrast family; dictionary section 2.6 plus a structural-tells variant note. **Evidence:** impeccable.design STYLE.md denylist (Paul Bakaus). **Result:** selftest green with a new fixture covering the additions.

## 2026-06-24 — initial open-source release

Engine extracted from a personal writing skill into a forkable body/soul structure. The engine (`SKILL.md`, `references/`, `evals/`, `scripts/`) is universal; the profile (soul, fingerprint, corpus, dialect, absolute rules) is per-user. Ships a blank `profile.template/`, a scrubbed `profile.example/`, the fingerprint generator, the held-in `selftest.py`, dialect packs (en-AU, en-US, en-GB), and the Self-Harness self-improvement loop as the contribution gate. Defines two agents (`agents/adversarial-reviewer.md`, `agents/indistinguishability-judge.md`) and wires them into the verification steps and the self-harness gate. selftest green on the generic example evals.
