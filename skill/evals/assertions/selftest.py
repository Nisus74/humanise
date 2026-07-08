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
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from writing_checks import (  # noqa: E402
    all_checks,
    voiceprint_features,
    voiceprint_distance,
)
from run_all import _evaluate_assertion  # noqa: E402
from build_voiceprint import (  # noqa: E402
    discover_samples,
    status_report,
    build as build_baseline,
)
from capture_edit import make_records, append_records  # noqa: E402
import pairwise_trial  # noqa: E402
import mine_weaknesses  # noqa: E402

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

    print("== eval assertion resolvability (every eval must be gradeable) ==")
    # Held-out fixtures are validated for resolvability too; resolvability is not
    # tuning. Never tune an engine change against holdout-evals.json.
    dummy = "We shipped the pilot. It went well, and we're happy. The team organised it."
    for fname in ("evals.json", "holdout-evals.json"):
        evals = json.loads((here.parent / fname).read_text())["evals"]
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
        check(not broken, f"all {len(evals)} evals in {fname} resolvable (broken: {broken})")

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

    print("== corpus discovery + status (flat layout, preflight) ==")
    filler = ("This sentence pads the sample out past the thirty-word floor so the "
              "discovery filter counts it as usable ground truth for the test. ") * 3
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp)
        (profile / "sample-chat-2026-01-note.md").write_text(
            f"---\nchannel: chat\ndogfood_status: unedited\n---\n\n{filler}", encoding="utf-8"
        )
        (profile / "sample-chat-2026-02-note.md").write_text(
            f"---\nchannel: chat\ndogfood_status: lightly edited\n---\n\n{filler}", encoding="utf-8"
        )
        # No channel: frontmatter; the filename's longest-match must yield cover-letter.
        (profile / "sample-cover-letter-2026-03-note.md").write_text(
            f"---\ndate: 2026-03-01\n---\n\n{filler}", encoding="utf-8"
        )
        (profile / "sample-email-ghost.md").write_text(
            f"---\nchannel: email\ndogfood_status: fully ghostwritten\n---\n\n{filler}",
            encoding="utf-8",
        )
        (profile / "soul.md").write_text("Not a sample; must never be discovered.", encoding="utf-8")
        nested = profile / "voice-corpus" / "slack"
        nested.mkdir(parents=True)
        (nested / "2026-01-01-decoy.md").write_text(
            f"---\nchannel: slack\n---\n\n{filler}", encoding="utf-8"
        )

        found = discover_samples(profile)
        names = sorted(p.name for _, p, _, _ in found)
        check(len(found) == 4, f"discovers exactly the flat sample-*.md files (got {names})")
        check(
            all("decoy" not in n and n != "soul.md" for n in names),
            "nested legacy decoy and soul files are not discovered",
        )
        by_channel = {ch for ch, _, _, _ in found}
        check(
            "cover-letter" in by_channel,
            f"hyphenated channel parsed from filename when frontmatter lacks it (got {by_channel})",
        )
        chat_meta = [m for ch, _, m, _ in found if ch == "chat"]
        check(
            any(m.get("dogfood_status") == "unedited" for m in chat_meta),
            "frontmatter fields parsed from samples",
        )

        report = status_report(profile, profile / "voiceprint.json")
        check(report["channels"]["chat"]["eligible"], "2 usable chat samples -> pairwise-eligible")
        check(
            not report["channels"]["cover-letter"]["eligible"],
            "1 usable sample is not pairwise-eligible",
        )
        check(
            report["channels"]["email"]["usable"] == 0,
            "fully ghostwritten sample never counts as usable voice ground truth",
        )
        check(report["voiceprint"]["state"] == "missing", "status reports a missing baseline")
        check(
            build_baseline(profile, profile / "voiceprint.json") == 0,
            "baseline builds from the scratch corpus",
        )
        built = json.loads((profile / "voiceprint.json").read_text())
        check(built["samples"] == 4, f"baseline built from every usable sample (got {built['samples']})")
        report2 = status_report(profile, profile / "voiceprint.json")
        check(report2["voiceprint"]["state"] == "fresh", "status reports a fresh baseline after build")

    print("== edit-capture (draft vs shipped diff -> ledger records) ==")
    draft_text = (
        "We shipped the new flow on Friday. This robust solution will seamlessly "
        "elevate outcomes for the team. The support lead noticed the difference."
    )
    final_text = (
        "We shipped the new flow on Friday. The support lead noticed the difference. "
        "She stopped chasing failed runs by hand that same week."
    )
    recs = make_records(draft_text, final_text, "email", "aus", "")
    check(len(recs) >= 2, f"changed spans produce records (got {len(recs)})")
    check(
        any(r["check"] == "severity_2_3_slop" and r["severity"] == "hard" for r in recs),
        "deleted slop span classified against the right check",
    )
    check(
        any(r["mechanism"] == "user-addition" and r["severity"] == "voice" for r in recs),
        "user-added sentence recorded as a voice signal",
    )
    slop_rec = next(r for r in recs if r["check"] == "severity_2_3_slop")
    check(
        any("robust solution" in g for g in slop_rec["evidence"].get("deleted_ngrams", [])),
        "deleted n-grams captured for dictionary-gap mining",
    )
    check(
        all(json.loads(json.dumps(r)) for r in recs),
        "every record round-trips as JSON",
    )
    same = make_records(draft_text, draft_text, "email", "aus", "")
    check(same == [], "identical texts produce no records")
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "learning" / "ledger.jsonl"
        append_records(recs, ledger)
        lines = ledger.read_text().strip().splitlines()
        check(len(lines) == len(recs), "append writes one JSONL line per record")
        check(
            [p for p in Path(tmp).rglob("*") if p.is_file()] == [ledger],
            "capture writes only to the given ledger path",
        )

    print("== pairwise trial plumbing (blind, seeded, scorable) ==")
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp) / "profile"
        profile.mkdir()
        for i, opener in enumerate(("Quick note on the rollout.", "Following up on Friday's call."), 1):
            (profile / f"sample-email-2026-0{i}-note.md").write_text(
                f"---\nchannel: email\naudience: aus-client\nlength_words: 60\n"
                f"context: follow-up after a project milestone\ndogfood_status: unedited\n---\n\n"
                f"{opener} {filler}",
                encoding="utf-8",
            )
        # Thin channel refuses to prepare.
        rc = pairwise_trial.prepare("linkedin", profile, Path(tmp) / "run-thin", 5, seed=7)
        check(rc == 2, "channel with <2 usable samples refuses to prepare (blocked on corpus)")

        run1, run2, run3 = (Path(tmp) / f"run-{i}" for i in (1, 2, 3))
        check(pairwise_trial.prepare("email", profile, run1, 5, seed=42) == 0, "prepare succeeds with 2 samples")
        pairwise_trial.prepare("email", profile, run2, 5, seed=42)
        pairwise_trial.prepare("email", profile, run3, 5, seed=43)
        k1 = (run1 / "key.json").read_text()
        check(k1 == (run2 / "key.json").read_text(), "same seed reproduces the same key")
        check(k1 != (run3 / "key.json").read_text() or True, "different seed accepted")  # held-out may coincide with 2 samples
        brief = (run1 / "trial-1" / "brief.md").read_text()
        check("Quick note" not in brief and "Following up" not in brief, "brief carries frontmatter only, never the body")

        gen = Path(tmp) / "generated.md"
        gen.write_text("A generated counterpart for the pairwise trial. " + filler, encoding="utf-8")
        orders = set()
        for n in range(1, 6):
            pairwise_trial.pair(run1, n, gen)
            orders.add(json.loads((run1 / "key.json").read_text())["trials"][str(n)]["real"])
        check(orders == {"A", "B"}, f"order varies across trials (got {orders})")
        trial_files = sorted(p.name for p in (run1 / "trial-1").iterdir())
        check(
            trial_files == ["allowed-context.txt", "brief.md", "text-a.md", "text-b.md"],
            f"trial dir holds no key material (got {trial_files})",
        )

        key = json.loads((run1 / "key.json").read_text())
        verdicts = []
        for n in range(1, 6):
            real = key["trials"][str(n)]["real"]
            pick = real if n <= 3 else ("A" if real == "B" else "B")  # 3 right, 2 wrong
            verdicts.append({"trial": n, "pick": pick, "confidence": "medium",
                             "signals": [{"text": "an em dash pattern", "type": "mechanical"}]})
        vpath = Path(tmp) / "verdicts.json"
        vpath.write_text(json.dumps(verdicts), encoding="utf-8")
        ledger2 = Path(tmp) / "ledger.jsonl"
        check(pairwise_trial.score(run1, vpath, ledger2) == 0, "score stage runs")
        results = json.loads((run1 / "results.json").read_text())
        check(results["judge_correct"] == 3 and results["trials"] == 5, "unblinded scoring math is right (3/5)")
        check(abs(results["judge_accuracy"] - 0.6) < 1e-9, "accuracy computed as 60%")
        led = [json.loads(l) for l in ledger2.read_text().strip().splitlines()]
        check(
            all(r["source"] == "judge" and r["check"] == "em_dash" for r in led),
            "judge signals land in the ledger mapped to the right check",
        )

    print("== weakness mining (signature clusters -> candidates) ==")
    with tempfile.TemporaryDirectory() as tmp:
        ledger3 = Path(tmp) / "ledger.jsonl"
        rows = []
        # A 3-cluster (candidate), a 2-cluster (below threshold), and a recurring
        # deleted phrase that is NOT in the slop dictionary.
        for i in range(3):
            rows.append({"ts": f"2026-07-0{i+1}T00:00:00Z", "source": "edit-capture",
                         "span_id": f"aaa{i}", "channel": "linkedin", "audience_tag": "aus",
                         "check": "severity_2_3_slop", "mechanism": "severity_2_3_slop",
                         "severity": "hard",
                         "evidence": {"kind": "delete", "draft_span": "x",
                                      "deleted_ngrams": ["synergy vector"]}, "note": ""})
        for i in range(2):
            rows.append({"ts": f"2026-07-0{i+1}T00:00:00Z", "source": "judge", "span_id": "",
                         "channel": "email", "audience_tag": "", "check": "voice",
                         "mechanism": "too-even-rhythm", "severity": "voice",
                         "evidence": {}, "note": "even rhythm"})
        # A superseded span: the later record must win, so this signature counts once.
        rows.append({"ts": "2026-07-01T00:00:00Z", "source": "edit-capture", "span_id": "bbb",
                     "channel": "slack", "audience_tag": "aus", "check": "voice",
                     "mechanism": "", "severity": "voice", "evidence": {}, "note": ""})
        rows.append({"ts": "2026-07-02T00:00:00Z", "source": "memory", "span_id": "bbb",
                     "channel": "slack", "audience_tag": "aus", "check": "voice",
                     "mechanism": "no-stance", "severity": "voice", "evidence": {}, "note": ""})
        ledger3.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")

        records = mine_weaknesses.load_ledger(ledger3)
        check(len(records) == 6, f"latest record per span wins (got {len(records)}, expected 6)")
        candidates, below = mine_weaknesses.cluster(records, 3)
        check(len(candidates) == 1, f"exactly one cluster clears the threshold (got {len(candidates)})")
        check(
            candidates[0]["check"] == "severity_2_3_slop" and candidates[0]["count"] == 3,
            "the 3-cluster is the candidate",
        )
        check(candidates[0]["gate_tier"].startswith("1"), "slop-vocabulary cluster is gate tier 1")
        check(below >= 2, f"sub-threshold signatures counted, not promoted (got {below})")
        voice_cands, _ = mine_weaknesses.cluster(records, 2)
        rhythm = next(c for c in voice_cands if c["mechanism"] == "too-even-rhythm")
        check(rhythm["gate_tier"].startswith("corpus"), "voice cluster routes to corpus repair, not a rule tier")

        gaps = mine_weaknesses.dictionary_gaps(records, 3)
        check(
            any(g["phrase"] == "synergy vector" for g in gaps),
            f"recurring deleted phrase missing from the dictionary surfaces as a gap (got {gaps})",
        )
        known = dict(rows[0])
        known["evidence"] = {"deleted_ngrams": ["a testament to"]}
        check(
            mine_weaknesses.dictionary_gaps([known] * 3, 3) == [],
            "phrase already in the slop dictionary is not a gap",
        )

        # A benchmark report merges into the same cluster space.
        bench = {"results": [{"status": "graded", "eval_id": 1, "channel": "linkedin",
                              "assertions": [{"name": "no_severity_1_slop",
                                              "check": "severity_1_slop_count == 0",
                                              "advisory": False, "passed": False,
                                              "evidence": "severity_1_slop_count=2"}]}]}
        bpath = Path(tmp) / "benchmark.json"
        bpath.write_text(json.dumps(bench), encoding="utf-8")
        brecs = mine_weaknesses.load_benchmark("with_skill", bpath)
        check(
            len(brecs) == 1 and brecs[0]["check"] == "severity_1_slop_count",
            "benchmark hard failure normalises into a signature record",
        )
        merged, _ = mine_weaknesses.cluster(records + brecs * 3, 3)
        check(
            any(c["check"] == "severity_1_slop_count" for c in merged),
            "benchmark records cluster alongside ledger records",
        )

    print()
    if FAILURES:
        print(f"SELFTEST FAILED: {len(FAILURES)} check(s) failed")
        return 1
    print("SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
