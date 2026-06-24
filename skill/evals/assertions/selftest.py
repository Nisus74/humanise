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
from writing_checks import all_checks  # noqa: E402
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

    print()
    if FAILURES:
        print(f"SELFTEST FAILED: {len(FAILURES)} check(s) failed")
        return 1
    print("SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
