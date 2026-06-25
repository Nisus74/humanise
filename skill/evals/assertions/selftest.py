"""Self-test / held-in regression suite for the humanise checking engine.

Runs without a model: it grades fixed fixtures and validates every eval's
assertions resolve. This is the held-in split in the Self-Harness sense
(evals/self-harness-loop.md): any change to writing_checks.py or evals.json must
keep this green before promotion. The held-out split is the pairwise
indistinguishability test (evals/indistinguishability.md), which a rule change
must also not regress.

Run:  python3 selftest.py     (exit 0 = all green, 1 = a regression)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from writing_checks import (  # noqa: E402
    all_checks,
    voiceprint_features,
    voiceprint_distance,
)
from run_all import _evaluate_assertion  # noqa: E402

# --- Fixtures -------------------------------------------------------------
# Clean, AusE register: should pass every hard check. (Generic content; swap in
# samples from your own dialect if you fork.)
CLEAN_AUS = (
    "We shipped the new onboarding flow on Friday. The team asked whether it could "
    "handle 400 signups an hour, and we'd said yes before we built it. The harder "
    "problem was traceability; that audit layer we'd prioritised took longer to get "
    "right than the feature did. We're now processing 180 jobs a day at 99.2% "
    "uptime, and the support lead has recognised the difference. She hasn't chased "
    "a failed run by hand since. Next quarter we'll know whether the rollout we "
    "organised was worth it."
)

# Deliberately sloppy: em dash, sev-1 slop, slop opener, classic + negated-copula
# contrasts, and a no-"and" imperative triple. Should fail several hard checks.
SLOPPY = (
    "In today's rapidly evolving healthcare landscape, I've been thinking deeply "
    "about the multifaceted challenges. It's not about the technology — it's "
    "about people. The most pivotal factor isn't cutting-edge AI, it's the nuanced "
    "relationship. Ship fast, learn deeply, repeat endlessly."
)

# Clean US register: US spelling, no AusE leak.
CLEAN_US = (
    "Thanks for the call Tuesday. I've looped in our security lead so your IT team "
    "can dig into the integration specifics. Could we get 30 minutes next week to "
    "walk through the deployment model and your data-residency requirements? I'll "
    "send three time options today. We organize the pilot around your validation "
    "timeline, so the sooner we lock a date, the better."
)

# Clean but anonymous: no slop, no em dash, varied-enough rhythm, yet no numbers,
# no names, no first-person stance, all abstraction. The Phase-2 presence-of-human
# signals must flag it; the hard checks must NOT (advisory only, no Goodhart gate).
ANON_CLEAN = (
    "The approach delivers value across the organisation. Teams that adopt the "
    "process tend to see results over time. The system supports the workflow and "
    "adapts to changing needs. When alignment improves, execution follows. The "
    "outcome is a foundation for the work ahead, and a path for everyone involved."
)

# Clean, multi-section long-form (>300 words) in a board register: numbers, stance,
# varied rhythm, AusE visible, contractions. Exercises the density-scaled contrast
# budget (the >=300-word branch) and the structural_density dashboard, and guards
# against the engine false-firing on length (long-form is where it broke worst).
LONG_FORM = """## Where the quarter landed

We closed the quarter at 12 pilot sites, up from 8 in March. The two we lost were always marginal: one never got past procurement, and the other changed its lab manager twice. We'd rather report the real number than the flattering one. Revenue held at $1.4M annualised, which is roughly flat, and that's fine for a quarter where we prioritised the audit layer.

## What we built

The audit layer took longer than we'd planned. Traceability is the hard part in regulated work, and we'd rather get it right once than patch it for a year. It's done now. Every sample carries a signed chain from intake to result, and the lab managers have stopped chasing failed runs by hand. Support tickets about provenance dropped from 40 a week to 6, and the team has recognised the difference. We also cut median onboarding for a new site from 18 days to 9, mostly by scripting the steps the team used to run by hand. It's unglamorous work, and it's the kind that compounds over a year.

## The risk we're watching

Cash. We've got nine months of runway at the current burn, and the next raise depends on the US pilots converting. If two of the four convert by September, we're comfortable. If none do, we cut scope in October and stretch the runway to fifteen months. It's the number that keeps us awake, and we won't pretend otherwise.

## What we need from the board

Two things. An introduction to anyone running a pathology network in California, because that's where the next three pilots should come from. And a decision on the hire we flagged last month: a regulatory lead, full time, or we keep renting that expertise at twice the cost. My view is that we hire. The work isn't slowing down, and renting it has already cost us two slipped deadlines. One more thing for the minutes: we'd like sign-off to move the Melbourne lab onto the new chain in November, ahead of the others, because it's the site most ready for it."""

FAILURES = []


def check(cond, label):
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        FAILURES.append(label)


def main():
    here = Path(__file__).parent
    evals = json.loads((here.parent / "evals.json").read_text())["evals"]

    print("== eval assertion resolvability (every eval must be gradeable) ==")
    dummy = "We shipped the pilot. It went well, and we're happy. The team organised it."
    broken = []
    for ev in evals:
        checks = all_checks(
            dummy,
            ev.get("audience_tag", "aus"),
            medium=ev.get("medium", "plain"),
            formal=bool(ev.get("formal_channel")),
        )
        for a in ev["assertions"]:
            _, detail = _evaluate_assertion(a["check"], checks, draft=dummy)
            if "unparsed assertion" in detail or "not available" in detail:
                broken.append((ev["id"], a["name"], detail))
    check(not broken, f"all {len(evals)} evals resolvable (broken: {broken})")

    print("== clean AusE fixture (passes every hard check) ==")
    c = all_checks(CLEAN_AUS, "aus-pm")
    check(c["_summary"]["failed"] == [], f"no hard failures (got {c['_summary']['failed']})")
    check(c["em_dash"]["pass"], "no em dashes")
    check(c["severity_1_slop"]["pass"], "no severity-1 slop")
    check(c["ause_spelling_clean"]["pass"], "no US spelling leak")

    print("== sloppy fixture (the engine must catch the tells) ==")
    s = all_checks(SLOPPY, "aus-pm")
    check(not s["em_dash"]["pass"], "em dash flagged")
    check(not s["severity_1_slop"]["pass"], "severity-1 slop flagged")
    check(not s["slop_opener"]["pass"], "slop opener flagged")
    check(
        not s["structural_tells"]["pass"],
        f"structural tells flagged (count={s['structural_tells']['count']}, "
        f"hits={s['structural_tells']['hits']})",
    )

    print("== clean US fixture (US register, no AusE leak) ==")
    u = all_checks(CLEAN_US, "us-buyer")
    check(u["us_spelling_clean"]["pass"], "no AusE leak in US content")
    check(u["em_dash"]["pass"], "no em dashes")

    print("== impeccable.design additions caught ==")
    imp = all_checks(
        "This load-bearing, data-driven approach will elevate outcomes; "
        "it's less about speed, more about scale.",
        "aus",
    )
    check(not imp["severity_2_3_slop"]["pass"], f"new sev2-3 words flagged (found={imp['severity_2_3_slop']['found']})")
    check(any("negation_pivot" in h for h in imp["structural_tells"]["hits"]), "negation pivot flagged")

    print("== manufactured candour (2026 authenticity tells) ==")
    cand = all_checks(
        "Not gonna lie, the rollout was rough. Real talk: we missed the date. "
        "No sugarcoating it, the build slipped a week.",
        "aus",
    )
    check(
        not cand["self_narrated_honesty"]["pass"],
        f"manufactured candour flagged (found={cand['self_narrated_honesty']['found']})",
    )

    print("== transition-opener pileup ==")
    pile = all_checks(
        "Moreover, the rollout went well. Furthermore, the team stayed aligned. "
        "Additionally, the numbers held.",
        "aus",
    )
    check(
        not pile["transition_pileup"]["pass"],
        f"sentence-initial transition pileup flagged (count={pile['transition_pileup']['count']})",
    )
    # A single opener is not a pileup; it must stay green (no false-fire).
    one = all_checks("Additionally, we shipped the fix on Friday afternoon.", "aus")
    check(one["transition_pileup"]["pass"], "single transition opener does not flag")

    print("== cross-sentence reframe template ==")
    ref = all_checks(
        "This isn't a tooling problem. It's a trust problem. We rebuilt the review flow.",
        "aus",
    )
    check(
        any("sentence_reframe" in h for h in ref["structural_tells"]["hits"]),
        f"cross-sentence reframe flagged (hits={ref['structural_tells']['hits']})",
    )
    # A plain continuation (reveal is not a copula) must not false-fire.
    cont = all_checks("This isn't working. It needs a rewrite before Friday.", "aus")
    check(
        not any("sentence_reframe" in h for h in cont["structural_tells"]["hits"]),
        "plain continuation does not flag as a reframe",
    )

    print("== approximation hedges (advisory, never gates) ==")
    hedge = all_checks(
        "We shipped roughly 40 fixes, sort of on schedule, and pretty much hit the "
        "target. It was more or less what we planned, give or take.",
        "aus",
    )
    check(not hedge["approximation_hedges"]["pass"], "approximation-hedge pileup flagged")
    check(
        "approximation_hedges" in hedge["_summary"]["advisory_flagged"],
        "hedge flag is advisory (appears in advisory_flagged)",
    )
    check(
        "approximation_hedges" not in hedge["_summary"]["failed"],
        "hedge flag never gates the piece (not in failed) [Goodhart guard]",
    )
    # A single sanctioned 'roughly' aside must not flag.
    aside = all_checks(
        "We'd built it in three weeks (roughly three weeks longer than planned) "
        "and the tests passed.",
        "aus",
    )
    check(aside["approximation_hedges"]["pass"], "single 'roughly' aside does not flag")

    print("== dead metaphor-verb cluster (advisory) ==")
    soup = all_checks(
        "We'll pivot the narrative and unlock new value, then double down to "
        "amplify reach across the funnel.",
        "aus",
    )
    check(not soup["dead_verb_density"]["pass"], "metaphor-verb cluster flagged")
    check(
        "dead_verb_density" not in soup["_summary"]["failed"],
        "dead-verb flag never gates the piece (not in failed) [Goodhart guard]",
    )
    # A single metaphor verb is not a cluster; must stay green.
    oneverb = all_checks("We unlocked the next onboarding stage on Friday.", "aus")
    check(oneverb["dead_verb_density"]["pass"], "single metaphor verb does not flag")

    print("== balanced-pair anaphora (advisory) ==")
    mirror = all_checks(
        "When we ship fast, we learn fast. When we ship slow, we stall hard. "
        "When we stop, we die quietly.",
        "aus",
    )
    check(not mirror["balanced_pairs"]["pass"], "balanced-pair drumbeat flagged")
    check(
        "balanced_pairs" not in mirror["_summary"]["failed"],
        "balanced-pair flag never gates the piece (not in failed) [Goodhart guard]",
    )
    # A single balanced pair is common in real prose; must stay green.
    single = all_checks("When tests pass, we ship it. When they fail, we fix it.", "aus")
    check(single["balanced_pairs"]["pass"], "single balanced pair does not flag")

    print("== presence-of-human signals (advisory, Phase 2) ==")
    anon = all_checks(ANON_CLEAN, "aus")
    check(not anon["specificity_density"]["pass"], "anonymous prose: low specificity flagged")
    check(not anon["stance_signal"]["pass"], "anonymous prose: missing stance flagged")
    check(
        anon["_summary"]["failed"] == [],
        f"anonymous prose has NO hard failure (got {anon['_summary']['failed']}) "
        "[Goodhart guard: presence signals never gate]",
    )
    check(
        all(
            anon[k].get("advisory")
            for k in ("specificity_density", "stance_signal", "copula_ratio", "generic_to_specific")
        ),
        "all four presence-of-human signals are advisory",
    )
    # Specific, opinionated prose must NOT trip the presence signals.
    rich = all_checks(CLEAN_AUS, "aus-pm")
    check(rich["specificity_density"]["pass"], "specific prose passes the specificity signal")
    check(rich["stance_signal"]["pass"], "opinionated prose passes the stance signal")

    print("== orphaned-check coverage (had an eval lookup but no fixture) ==")
    en = all_checks("The result – a cleaner pipeline – shipped on Friday.", "aus")
    check(not en["en_dash_non_range"]["pass"] and en["en_dash_non_range"]["count"] >= 1, "spaced en dash flagged")
    rng = all_checks("The trial window ran 2015–18 across every site we opened.", "aus")
    check(rng["en_dash_non_range"]["pass"], "en dash in a numeric range is allowed")
    sh = all_checks("The result - a cleaner pipeline - shipped on Friday afternoon.", "aus")
    check(not sh["spaced_hyphen_dash"]["pass"] and sh["spaced_hyphen_dash"]["count"] >= 1, "spaced hyphen used as dash flagged")
    frag = all_checks(
        "The recommendation. Adopt the price book. The ask: More runway now. "
        "The risk: The timeline slips.",
        "aus",
    )
    check(frag["fragment_colon_headers"]["count"] >= 3 and not frag["fragment_colon_headers"]["pass"], "fragment-colon label cluster flagged")
    acad = all_checks(
        "The framework operationalises the strategy and stems from first principles, "
        "predicated on clear metrics.",
        "aus",
    )
    check(acad["academic_register"]["count"] >= 3 and not acad["academic_register"]["pass"], "academic-register cluster flagged")
    rhythm = all_checks("We shipped it today. The team was glad. The build went green. The tests passed clean.", "aus")
    check(rhythm["sentence_profile"]["runs_of_3"] >= 1, "sentence-length monotony flagged (advisory)")
    paras = all_checks(
        "We shipped the onboarding flow on Friday and the team checked the numbers all afternoon.\n\n"
        "The audit layer took longer than the feature did because traceability is the hard part here.\n\n"
        "Support has not chased a single failed run by hand since the rollout went live last week.",
        "aus",
    )
    check(paras["paragraph_shape"]["similar_runs"] >= 1, "paragraph-shape uniformity flagged (advisory)")
    binc = all_checks("It's not about speed, it's about trust on every call we make.", "aus")
    check(binc["binary_contrast_density"]["count"] >= 1, "binary contrast counted by the density view")

    print("== formal channel + docx medium coverage ==")
    formal_open = all_checks("I am writing to express my interest. I have led three teams.", "aus", formal=True)
    check(not formal_open["i_this_openers"]["pass"], "I/This opener hard-fails in a formal channel")
    casual_open = all_checks("I shipped it on Friday. I will follow up Monday.", "aus", formal=False)
    check(
        casual_open["i_this_openers"]["pass"] and casual_open["i_this_openers"]["advisory"],
        "I/This opener is advisory outside formal channels",
    )
    curly = "The team said “ship it” and we did."
    check(all_checks(curly, "aus", medium="docx")["curly_quotes"]["pass"], "docx medium accepts curly quotes (human default)")
    check(not all_checks(curly, "aus", medium="plain")["curly_quotes"]["pass"], "plain medium flags curly quotes")

    print("== long-form density plumbing (>300 words, clean) ==")
    lf = all_checks(LONG_FORM, "aus-board")
    check(lf["word_count"]["count"] >= 300, f"long-form fixture exceeds 300 words (got {lf['word_count']['count']})")
    check(lf["_summary"]["failed"] == [], f"clean long-form has no hard failure (got {lf['_summary']['failed']})")
    check("per_1000_words" in lf["binary_contrast_density"], "density view reports a per-1000-word rate")
    check("transition_openers" in lf["_summary"]["structural_density"], "structural_density dashboard exposes transition_openers")
    check(lf["binary_contrast_density"]["pass"], "clean long-form passes the density-scaled contrast budget")

    print("== voiceprint features + distance (advisory, baseline-gated) ==")
    feats = voiceprint_features(CLEAN_AUS)
    check("sentence_cov" in feats and "copula_ratio" in feats, "voiceprint feature vector computed")
    # A baseline built from a text scores that text at ~zero distance.
    base = {"samples": 5, "features": {k: {"mean": v, "stdev": max(abs(v) * 0.1, 0.5)} for k, v in feats.items()}}
    d = voiceprint_distance(CLEAN_AUS, base)
    check(d["aggregate"] < 1.0, f"self-distance is small (got {d['aggregate']})")
    check(d["advisory"] is True, "voiceprint distance is advisory, never a hard gate")
    # A thin baseline (<3 samples) refuses to flag, however far the draft drifts.
    thin = voiceprint_distance(ANON_CLEAN, {"samples": 1, "features": base["features"]})
    check(thin["pass"], "thin baseline does not flag (too few samples to be stable)")
    # all_checks omits the block by default, so existing callers are unaffected.
    check("voiceprint_distance" not in all_checks(CLEAN_AUS, "aus"), "no baseline -> no voiceprint block (default off)")
    withbase = all_checks(ANON_CLEAN, "aus", baseline=base)
    check("voiceprint_distance" in withbase, "baseline supplied -> voiceprint block present")
    check("voiceprint_distance" not in withbase["_summary"]["failed"], "voiceprint never gates the piece [Goodhart guard]")

    print()
    if FAILURES:
        print(f"SELFTEST FAILED: {len(FAILURES)} check(s) failed")
        return 1
    print("SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
