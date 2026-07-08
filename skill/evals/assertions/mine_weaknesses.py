#!/usr/bin/env python3
"""Weakness mining for the self-improvement loop. Stdlib only, deterministic.

Stage one of `evals/self-harness-loop.md`: cluster every recorded correction by
its failure signature `(check, channel, mechanism)` and surface the clusters
that clear the promotion threshold (three occurrences) as rule-change
candidates. Sources:

- the learning ledger (`profile/learning/ledger.jsonl`): edit-capture and judge
  records, appended by `scripts/capture_edit.py` and `pairwise_trial.py --score`;
- benchmark reports (`run_all.py` output): hard assertion failures;
- indistinguishability results (`pairwise_trial.py` results.json): pass these
  ONLY for runs whose signals were not already appended to the ledger at score
  time, or the same signal counts twice.

This script never edits the engine. It emits `candidates.json`; the
improvement-proposer subagent drafts bounded edits from it, and every edit still
clears the tiered gate in `self-harness-loop.md`.

Usage:
  python3 mine_weaknesses.py [--ledger <path>] [--benchmark label=path.json ...]
      [--indist path.json ...] [--threshold 3] [--dictionary-gaps]
      [--out candidates.json] [--summary]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LEDGER = (
    Path(__file__).resolve().parent.parent.parent / "profile" / "learning" / "ledger.jsonl"
)
DICTIONARY = (
    Path(__file__).resolve().parent.parent.parent / "references" / "ai-slop-dictionary.md"
)

# Gate tier per self-harness-loop.md. Vocabulary checks repair with a dictionary
# entry (tier 1); mechanical checks repair with a detector or threshold change
# (tier 2); voice clusters usually repair with corpus, and an absolute-rule
# change is tier 3 with user sign-off.
TIER_1_CHECKS = frozenset(
    ("severity_1_slop", "severity_2_3_slop", "academic_register", "self_narrated_honesty",
     "slop_opener", "dead_verb_density", "approximation_hedges")
)


def _tier(check):
    if check == "voice":
        return "corpus (tier 3 + user sign-off if the repair is an absolute rule)"
    if check in TIER_1_CHECKS:
        return "1 (held-in green)"
    return "2 (held-in green + held-out not regressed)"


def _check_key_from_assertion(assertion):
    m = re.search(r"[A-Za-z_]\w*", assertion.get("check", ""))
    return m.group(0) if m else assertion.get("name", "unknown")


def load_ledger(path):
    """Ledger records, latest record per non-empty span_id winning."""
    records, by_span = [], {}
    p = Path(path)
    if not p.exists():
        return records
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        span = r.get("span_id") or ""
        if span:
            by_span[span] = r  # file order is append order; last one wins
        else:
            records.append(r)
    records.extend(by_span.values())
    return records


def load_benchmark(label, path):
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    records = []
    for result in report.get("results", []):
        if result.get("status") != "graded":
            continue
        for a in result.get("assertions", []):
            if a.get("advisory") or a.get("passed"):
                continue
            records.append({
                "source": "benchmark",
                "channel": result.get("channel") or "unknown",
                "check": _check_key_from_assertion(a),
                "mechanism": _check_key_from_assertion(a),
                "severity": "hard",
                "note": f"{label}: eval {result.get('eval_id')} failed {a.get('name')} ({a.get('evidence')})",
            })
    return records


def load_indist(path):
    results = json.loads(Path(path).read_text(encoding="utf-8"))
    records = []
    for s in results.get("signals", []):
        mechanical = s.get("type") == "mechanical"
        records.append({
            "source": "judge",
            "channel": results.get("channel") or "unknown",
            "check": s.get("slug") if mechanical else "voice",
            "mechanism": s.get("slug", "unclassified"),
            "severity": "hard" if mechanical else "voice",
            "note": s.get("text", ""),
        })
    return records


def cluster(records, threshold):
    groups = defaultdict(list)
    for r in records:
        key = (r.get("check", "unknown"), r.get("channel", "unknown"), r.get("mechanism", ""))
        groups[key].append(r)
    candidates, below = [], 0
    for (check, channel, mechanism), rs in sorted(groups.items()):
        if len(rs) < threshold:
            below += 1
            continue
        notes = []
        for r in rs:
            text = r.get("note") or r.get("evidence", {}).get("draft_span", "")
            if text:
                notes.append(text[:140])
            if len(notes) == 3:
                break
        candidates.append({
            "type": "signature-cluster",
            "check": check,
            "channel": channel,
            "mechanism": mechanism,
            "count": len(rs),
            "sources": sorted({r.get("source", "?") for r in rs}),
            "gate_tier": _tier(check),
            "evidence": notes,
        })
    candidates.sort(key=lambda c: (-c["count"], c["check"], c["channel"]))
    return candidates, below


def dictionary_gaps(records, threshold):
    """Recurring user-deleted phrases missing from the shared slop dictionary."""
    counts = defaultdict(int)
    for r in records:
        for phrase in r.get("evidence", {}).get("deleted_ngrams", []):
            counts[phrase] += 1
    if not counts:
        return []
    dictionary = DICTIONARY.read_text(encoding="utf-8").lower() if DICTIONARY.exists() else ""

    def covered(phrase):
        # A phrase is covered when it, or any contiguous multi-word part of it,
        # already appears in the dictionary ("a testament to" is covered by the
        # "testament to" entry). Single words are too fuzzy to match against prose.
        words = phrase.split()
        for size in range(len(words), 1, -1):
            for i in range(len(words) - size + 1):
                if " ".join(words[i:i + size]) in dictionary:
                    return True
        return False

    gaps = []
    for phrase, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if n < threshold or covered(phrase):
            continue
        gaps.append({
            "type": "dictionary-gap",
            "phrase": phrase,
            "count": n,
            "gate_tier": "1 (held-in green)",
        })
    return gaps


def main():
    ap = argparse.ArgumentParser(description="Cluster recorded corrections into rule-change candidates.")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--benchmark", action="append", default=[], metavar="label=path",
                    help="a run_all.py benchmark.json, prefixed with a label")
    ap.add_argument("--indist", action="append", default=[],
                    help="a pairwise_trial.py results.json NOT already folded into the ledger")
    ap.add_argument("--threshold", type=int, default=3)
    ap.add_argument("--dictionary-gaps", action="store_true")
    ap.add_argument("--out", help="write candidates.json here (default: print)")
    ap.add_argument("--summary", action="store_true", help="print cluster counts only")
    args = ap.parse_args()

    records = load_ledger(args.ledger)
    for spec in args.benchmark:
        label, _, path = spec.partition("=")
        if not path:
            ap.error(f"--benchmark needs label=path, got: {spec}")
        records.extend(load_benchmark(label, path))
    for path in args.indist:
        records.extend(load_indist(path))

    candidates, below = cluster(records, args.threshold)
    if args.dictionary_gaps:
        candidates.extend(dictionary_gaps(records, args.threshold))

    if args.summary:
        groups = defaultdict(int)
        for r in records:
            groups[(r.get("check", "?"), r.get("channel", "?"), r.get("mechanism", ""))] += 1
        print(f"{len(records)} record(s), {len(groups)} signature(s), threshold {args.threshold}:")
        for (check, channel, mechanism), n in sorted(groups.items(), key=lambda kv: -kv[1]):
            mark = "CANDIDATE" if n >= args.threshold else f"{args.threshold - n} more to candidate"
            print(f"  {n}x {check} / {channel} / {mechanism or '(unclassified)'} [{mark}]")
        return 0

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "threshold": args.threshold,
        "records_considered": len(records),
        "clusters_below_threshold": below,
        "candidates": candidates,
    }
    payload = json.dumps(out, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(payload + "\n", encoding="utf-8")
        print(f"Wrote {len(candidates)} candidate(s) to {args.out}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
