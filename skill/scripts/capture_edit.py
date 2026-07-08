#!/usr/bin/env python3
"""Capture what the user changed between the skill's draft and the shipped text.

Every span the user rewrote or deleted is a correction the loop can learn from.
This script diffs the two texts sentence by sentence, classifies each changed
draft span against the deterministic checks in `writing_checks.py`, and appends
one JSON record per finding to the learning ledger. The ledger is the durable,
cross-harness accumulation point that `mine_weaknesses.py` clusters into
rule-change candidates (see `evals/self-harness-loop.md`).

The ledger lives in `profile/learning/` (the soul): it holds the user's verbatim
text, so it never ships and is never committed. Records are append-only; a later,
better classification of the same span is a new record with the same `span_id`,
and mining takes the latest record per span.

Usage:
  python3 capture_edit.py --draft draft.md --final final.md \
      [--channel email] [--audience aus] [--ledger <path>] [--note "..."]
"""

import argparse
import difflib
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "evals" / "assertions"))
from writing_checks import all_checks, _sentences  # noqa: E402

DEFAULT_LEDGER = Path(__file__).resolve().parent.parent / "profile" / "learning" / "ledger.jsonl"

# Checks whose failure on a short span is attributable to that span. The
# presence-of-human signals (stance, specificity, burstiness, shape) are
# document-level and would false-fire on any sentence, so they stay out.
SPAN_CHECKS = (
    "em_dash",
    "en_dash_non_range",
    "spaced_hyphen_dash",
    "curly_quotes",
    "severity_1_slop",
    "severity_2_3_slop",
    "academic_register",
    "self_narrated_honesty",
    "slop_opener",
    "transition_pileup",
    "i_this_openers",
    "structural_tells",
    "fragment_colon_headers",
    "approximation_hedges",
    "dead_verb_density",
    "balanced_pairs",
    "ause_spelling_clean",
    "us_spelling_clean",
)

STOPWORDS = frozenset(
    "a an and are as at be but by for from has have i in is it of on or "
    "that the this to was we were will with you your".split()
)


def span_id(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:12]


def deleted_ngrams(text, max_phrases=20):
    """Lowercased 2-4-grams from a deleted span, minus pure-stopword runs.

    Recurrence is mining's job (`mine_weaknesses.py --dictionary-gaps` counts
    these across records); this just makes the raw material cheap to count.
    """
    words = [w.strip(".,;:!?()[]\"'").lower() for w in text.split()]
    words = [w for w in words if w]
    phrases = []
    for n in (2, 3, 4):
        for i in range(len(words) - n + 1):
            gram = words[i:i + n]
            if all(w in STOPWORDS for w in gram):
                continue
            phrases.append(" ".join(gram))
    seen, out = set(), []
    for p in phrases:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out[:max_phrases]


def classify_span(span, audience_tag):
    """(check, severity) pairs for every span-attributable check the span fails."""
    results = all_checks(span, audience_tag)
    findings = []
    for name in SPAN_CHECKS:
        r = results.get(name)
        if r and not r.get("pass", True):
            findings.append((name, "advisory" if r.get("advisory") else "hard"))
    return findings


def diff_spans(draft, final):
    """Changed spans as (kind, draft_span, final_span); kind in replace|delete|insert."""
    a, b = _sentences(draft), _sentences(final)
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    spans = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        spans.append((op, " ".join(a[i1:i2]).strip(), " ".join(b[j1:j2]).strip()))
    return spans


def make_records(draft, final, channel, audience_tag, note):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    records = []
    for kind, draft_span, final_span in diff_spans(draft, final):
        base = {
            "ts": ts,
            "source": "edit-capture",
            "span_id": span_id(draft_span or final_span),
            "channel": channel,
            "audience_tag": audience_tag,
            "evidence": {"kind": kind, "draft_span": draft_span, "final_span": final_span},
            "note": note,
        }
        if kind == "insert":
            # The user added texture the draft lacked; a voice-level signal.
            records.append({**base, "check": "voice", "mechanism": "user-addition", "severity": "voice"})
            continue
        if kind == "delete":
            base["evidence"]["deleted_ngrams"] = deleted_ngrams(draft_span)
        findings = classify_span(draft_span, audience_tag)
        if not findings:
            # No deterministic check explains the edit; /humanise learn classifies
            # it with the controlled mechanism vocabulary in a superseding record.
            records.append({**base, "check": "voice", "mechanism": "", "severity": "voice"})
            continue
        for check, severity in findings:
            records.append({**base, "check": check, "mechanism": check, "severity": severity})
    return records


def append_records(records, ledger_path):
    ledger = Path(ledger_path)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="Diff a draft against the shipped text into the learning ledger.")
    ap.add_argument("--draft", required=True, help="the skill's draft")
    ap.add_argument("--final", required=True, help="the text the user actually shipped")
    ap.add_argument("--channel", default="unknown", help="channel of the piece (email, linkedin, ...)")
    ap.add_argument("--audience", default="aus", help="audience tag used at draft time")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER), help="ledger path (JSONL, append-only)")
    ap.add_argument("--note", default="", help="one-line context for the records")
    args = ap.parse_args()

    draft = Path(args.draft).read_text(encoding="utf-8")
    final = Path(args.final).read_text(encoding="utf-8")
    records = make_records(draft, final, args.channel, args.audience, args.note)
    if not records:
        print("No changed spans: the shipped text matches the draft.")
        return 0
    append_records(records, args.ledger)
    unclassified = sum(1 for r in records if r["check"] == "voice" and not r["mechanism"])
    print(f"Wrote {len(records)} record(s) to {args.ledger}")
    for r in records:
        label = r["mechanism"] or "voice (unclassified)"
        print(f"  [{r['evidence']['kind']}] {label}: {r['evidence']['draft_span'][:70] or r['evidence']['final_span'][:70]}")
    if unclassified:
        print(
            f"{unclassified} span(s) have no deterministic explanation. Classify them "
            "with the mechanism vocabulary in commands/learn.md (append superseding records)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
