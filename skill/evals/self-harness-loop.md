# Self-improvement loop (how this skill changes itself)

The memory loop (`references/memory-loop.md`) captures single corrections. This file defines how those accumulate into a disciplined change to the skill, and the gate every change clears before it ships. It adapts the Self-Harness protocol (Zhang et al., 2026, arXiv:2606.09498): a fixed model improves its own harness through propose → evaluate → accept, where edits are grounded in behavioural evidence and promoted only if they don't regress.

A skill is a harness. The same loop applies.

---

## The three stages

### 1. Weakness mining (evidence, not anecdote)

Don't patch one-off corrections. Cluster them by **failure signature**: `(which check or tell fired, the channel/audience, the mechanism that produced it)`. Two misses belong to the same cluster only when they agree on all three. Example signature: `(binary_contrast, linkedin, "diagnosed the source contrast and rewrote it with the same shape")`.

Build an **evidence bundle** before changing anything: the dominant signatures, how often each recurs, and a representative example each. A signature seen once is a note; a signature seen three or more times across sessions is a candidate for a rule change. This is the promotion trigger already named in `memory-loop.md`, sharpened.

### 2. Bounded proposal (minimal, evidence-tied, diverse)

Each proposed change to the skill must name four things, or it isn't ready:

- **Target.** The specific failure signature it fixes.
- **Surface.** The exact file and section it edits (a rule in SKILL.md, a word in `ai-slop-dictionary.md`, a regex in `writing_checks.py`, a threshold).
- **Evidence.** The cluster from stage 1 that motivates it.
- **Expected effect.** What the held-in suite should show after.

Keep edits minimal: change only the surface needed, preserve everything that already passes, no broad rewrites. When several fixes are plausible, prefer the narrowest that addresses the mechanism. Breadth is for exploring options, not for shipping; ship the smallest edit that works.

### 3. Regression-gated validation (the acceptance rule)

A change is promoted only if it clears a non-regressive gate across two splits:

- **Held-in** = the assertion battery (`evals.json`) and `evals/assertions/selftest.py`. The change must keep these green (and ideally turn a red case green).
- **Held-out** = the pairwise indistinguishability test (`evals/indistinguishability.md`) plus the reserved fixtures in `evals/holdout-evals.json`, which nobody tunes against: no editing a rule until a holdout draft passes, no drafting to their assertions. The change must not lower judge-confusion, voice fidelity, or the holdout pass rate.

Acceptance rule (from the paper): promote only if the change **improves at least one split and degrades neither**. A change that lifts the battery but makes the voice test worse is rejected, because tuning to the regex instead of the voice is its own failure. Log rejected proposals too; a rejection is evidence.

---

## Tiered gates by stakes

The paper's stated limit: pass-rate non-regression alone isn't enough for high-stakes edits. So scale the gate to the blast radius.

| Change | Gate |
| --- | --- |
| New slop word, new channel mapping row, comment | Held-in green |
| New detector, threshold change, structural rule | Held-in green + held-out not regressed |
| Absolute rule (the voice-fingerprint "absolute rules" section) | The above + an adversarial read (`../agents/adversarial-reviewer.md`) **and** the user's sign-off |

The last row exists because an absolute-rule change alters the voice the skill is built to protect, which a green battery alone does not authorise.

---

## Running the loop

The three stages are executed by `/humanise improve` (`commands/improve.md`); this file stays the authority on what counts as evidence and what clears the gate. The deterministic parts are scripted: `scripts/capture_edit.py` turns the user's real edits into ledger records, `evals/assertions/mine_weaknesses.py` clusters the ledger, benchmark reports, and judge signals into `candidates.json` (stage 1), the `improvement-proposer` subagent drafts the bounded proposals (stage 2), and the orchestrator runs the tiered gate before anything ships (stage 3). Evidence accumulates in `profile/learning/ledger.jsonl`, which holds the user's verbatim text and therefore never leaves `profile/`. Rejected proposals are appended to the ledger too; a rejection is evidence.

---

## Auditable, reversible lineage

Every promoted change gets a `CHANGELOG.md` entry in the four-part schema (target, surface, evidence, eval result). Keep the folder under git so any change is reversible to the previous working version; that reversibility is what makes bold edits safe to try. A change with no changelog entry is unfinished.

---

## Known limits (carried from the paper)

- **The battery can overfit.** It rewards passing the checks, which is not the same as sounding like the user. The held-out voice test and the real corpus are the guard; never tune a draft to the detector.
- **Verifier coverage bounds the loop.** A weakness the script can't see can't be mined. Gaps in `writing_checks.py` cap what self-improvement can reach, which is why detector coverage is itself a tracked surface.
- **Evidence quality bounds the loop.** Thin corpus, thin signal. The single highest-value input remains real `profile/sample-*.md` samples, not more rules.
- **The voiceprint is a tripwire, not a gate.** The voiceprint distance (`writing_checks.py` `voiceprint_distance`, built by `scripts/build_voiceprint.py`) is advisory: it flags a draft that drifts from the corpus baseline so the held-out judge knows where to look. It reports a distance, never a direction, and a thin baseline (fewer than three samples) refuses to flag at all. Treat it as the cheap early-warning that decides when to spend the judge, never as the voice verdict itself.
