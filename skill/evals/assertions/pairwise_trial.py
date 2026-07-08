#!/usr/bin/env python3
"""Deterministic plumbing for the pairwise indistinguishability test. Stdlib only.

The protocol lives in `evals/indistinguishability.md`; this script automates the
parts that must be repeatable and blind: hold-out selection, brief reconstruction
(frontmatter only, never the body), order randomisation, unblinding, and scoring.
The judgement itself stays with LLM subagents (`agents/eval-generator.md` writes
the counterpart, `agents/indistinguishability-judge.md` judges), spawned by
`/humanise improve`.

Blinding contract: each `trial-<n>/` directory contains only what its reader may
see. The generator reads `brief.md` and the files in `allowed-context.txt`; the
judge reads `text-a.md` and `text-b.md`. The mapping lives in `key.json` at the
run root, which only this script and the orchestrator touch.

All randomness comes from one seeded `random.Random`; the default seed is derived
from the date and channel and printed, so a run can be replayed exactly with
`--seed`.

Stages:
  --prepare --channel <ch> --profile <dir> --run-dir <dir> [--trials 5] [--seed N]
  --pair    --run-dir <dir> --trial <n> --generated <file>
  --score   --run-dir <dir> --verdicts <verdicts.json> [--ledger <path>]
"""

import argparse
import hashlib
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from build_voiceprint import discover_samples, MIN_SAMPLE_WORDS  # noqa: E402

DEFAULT_TRIALS = 5
DEFAULT_LEDGER = (
    Path(__file__).resolve().parent.parent.parent / "profile" / "learning" / "ledger.jsonl"
)

# Keyword map for tagging judge signals. Mechanical signals mean the sweep is
# leaking (fix rules); voice-level signals mean the imitation is anonymous
# (fix corpus). The judge's own wording decides via these keywords; explicit
# `"type"` on a signal object takes precedence.
MECHANICAL_KEYWORDS = {
    "em_dash": ("em dash", "em-dash", "dash"),
    "curly_quotes": ("curly quote", "smart quote", "quotation mark"),
    "severity_2_3_slop": ("slop", "buzzword", "leverage", "seamless", "robust", "delve"),
    "ause_spelling_clean": ("spelling", "dialect", "americanism", "-ize", "-ise"),
    "structural_tells": ("contrast", "triple", "rule of three", "template", "not about", "reframe"),
    "transition_pileup": ("moreover", "furthermore", "transition"),
    "fragment_colon_headers": ("colon", "fragment header", "label"),
    "contraction_types": ("contraction",),
}
VOICE_KEYWORDS = {
    "too-even-rhythm": ("rhythm", "even", "uniform", "same length", "cadence", "burstiness"),
    "no-stance": ("opinion", "stance", "position", "hedge", "committed"),
    "too-generic": ("generic", "specific", "abstraction", "vague", "concrete", "number"),
    "opener-template": ("opening", "opener", "closing", "sign-off"),
    "register-miss": ("register", "formal", "casual", "tone"),
}


def _now():
    return datetime.now(timezone.utc)


def _default_seed(channel):
    stamp = _now().strftime("%Y-%m-%d")
    return int(hashlib.sha256(f"{stamp}-{channel}".encode("utf-8")).hexdigest()[:8], 16)


def _eligible(profile_dir, channel):
    out = []
    for ch, path, meta, body in discover_samples(profile_dir):
        if ch != channel:
            continue
        if len(body.split()) < MIN_SAMPLE_WORDS:
            continue
        if "fully ghostwritten" in meta.get("dogfood_status", ""):
            continue
        out.append((path, meta, body))
    return out


def prepare(channel, profile_dir, run_dir, trials, seed):
    samples = _eligible(profile_dir, channel)
    if len(samples) < 2:
        print(
            f"Blocked on corpus: channel '{channel}' has {len(samples)} usable sample(s); "
            "the pairwise test needs at least 2 (one to hold out, one to draft from). "
            "The profile's CORPUS.md lists which samples to paste next.",
            file=sys.stderr,
        )
        return 2
    seed = _default_seed(channel) if seed is None else seed
    rng = random.Random(seed)
    run = Path(run_dir)
    run.mkdir(parents=True, exist_ok=True)

    key = {"channel": channel, "seed": seed, "trials": {}}
    for n in range(1, trials + 1):
        held_path, held_meta, _ = samples[rng.randrange(len(samples))]
        trial = run / f"trial-{n}"
        trial.mkdir(exist_ok=True)
        brief = [
            "# Brief (reconstructed from the held-out sample's frontmatter only)",
            "",
            f"- channel: {channel}",
            f"- audience: {held_meta.get('audience', 'unspecified')}",
            f"- approximate length: {held_meta.get('length_words', 'match the channel norm')} words",
            f"- context / the ask: {held_meta.get('context', 'unspecified')}",
            "",
            "Write the piece this brief describes, in the user's voice, using only the "
            "corpus files listed in allowed-context.txt plus the engine. Same topic "
            "territory, same audience, same approximate length. You have not seen the "
            "real piece and must not look for it.",
        ]
        (trial / "brief.md").write_text("\n".join(brief) + "\n", encoding="utf-8")
        allowed = [str(p) for p, _, _ in samples if p != held_path]
        (trial / "allowed-context.txt").write_text("\n".join(allowed) + "\n", encoding="utf-8")
        key["trials"][str(n)] = {"held_out": str(held_path)}

    (run / "key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {trials} trial(s) for '{channel}' in {run} (seed {seed}).")
    print("Spawn the eval-generator per trial with brief.md + allowed-context.txt, "
          "then run --pair per trial with the generated file.")
    return 0


def pair(run_dir, trial_n, generated_path):
    run = Path(run_dir)
    key_path = run / "key.json"
    key = json.loads(key_path.read_text(encoding="utf-8"))
    entry = key["trials"].get(str(trial_n))
    if entry is None:
        print(f"No trial {trial_n} in {key_path}.", file=sys.stderr)
        return 1
    # Strip frontmatter from the real sample so the judge compares prose, not metadata.
    from build_voiceprint import parse_frontmatter
    _, real_body = parse_frontmatter(Path(entry["held_out"]).read_text(encoding="utf-8"))
    generated = Path(generated_path).read_text(encoding="utf-8").strip()

    rng = random.Random(f"{key['seed']}-pair-{trial_n}")
    real_is_a = rng.random() < 0.5
    trial = run / f"trial-{trial_n}"
    (trial / "text-a.md").write_text((real_body.strip() if real_is_a else generated) + "\n", encoding="utf-8")
    (trial / "text-b.md").write_text((generated if real_is_a else real_body.strip()) + "\n", encoding="utf-8")
    entry["real"] = "A" if real_is_a else "B"
    entry["generated_from"] = str(generated_path)
    key_path.write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    print(f"Paired trial {trial_n}: text-a.md and text-b.md written (order seeded).")
    return 0


def _tag_signal(signal):
    """(text, type, slug): mechanical -> a check name, voice-level -> a mechanism."""
    if isinstance(signal, dict):
        text = signal.get("text", "")
        explicit = signal.get("type", "")
        if explicit in ("mechanical", "voice-level", "voice"):
            forced = explicit if explicit != "voice" else "voice-level"
        else:
            forced = None
    else:
        text, forced = str(signal), None
    lower = text.lower()
    for check, words in MECHANICAL_KEYWORDS.items():
        if any(w in lower for w in words):
            return text, forced or "mechanical", check
    for mech, words in VOICE_KEYWORDS.items():
        if any(w in lower for w in words):
            return text, forced or "voice-level", mech
    return text, forced or "voice-level", "unclassified"


def score(run_dir, verdicts_path, ledger_path):
    run = Path(run_dir)
    key = json.loads((run / "key.json").read_text(encoding="utf-8"))
    verdicts = json.loads(Path(verdicts_path).read_text(encoding="utf-8"))
    if isinstance(verdicts, dict):
        verdicts = verdicts.get("verdicts", [])

    total, correct, signals = 0, 0, []
    for v in verdicts:
        entry = key["trials"].get(str(v.get("trial")))
        if entry is None or "real" not in entry:
            continue
        total += 1
        hit = str(v.get("pick", "")).strip().upper() == entry["real"]
        correct += hit
        for s in v.get("signals", []):
            text, kind, slug = _tag_signal(s)
            signals.append({"text": text, "type": kind, "slug": slug, "trial": v.get("trial"), "judge_correct": hit})

    if not total:
        print("No scorable verdicts (trials must be paired before judging).", file=sys.stderr)
        return 1
    accuracy = correct / total
    results = {
        "channel": key["channel"],
        "seed": key["seed"],
        "trials": total,
        "judge_correct": correct,
        "judge_accuracy": round(accuracy, 3),
        "signals": signals,
    }
    (run / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    # Judge signals feed the same ledger the edit-capture records land in; slugs
    # only (no verbatim signal text is needed for clustering).
    ts = _now().strftime("%Y-%m-%dT%H:%M:%SZ")
    ledger = Path(ledger_path)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        for s in signals:
            record = {
                "ts": ts,
                "source": "judge",
                "span_id": "",
                "channel": key["channel"],
                "audience_tag": "",
                "check": s["slug"] if s["type"] == "mechanical" else "voice",
                "mechanism": s["slug"],
                "severity": "hard" if s["type"] == "mechanical" else "voice",
                "evidence": {"trial": s["trial"], "judge_correct": s["judge_correct"]},
                "note": s["text"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # The committed log gets aggregates and slugs only, never the user's text.
    top = {}
    for s in signals:
        top[s["slug"]] = top.get(s["slug"], 0) + 1
    top_str = ", ".join(f"{slug} ({n})" for slug, n in sorted(top.items(), key=lambda kv: -kv[1])[:4]) or "none recorded"
    row = (
        f"| {_now().strftime('%Y-%m-%d')} | {key['channel']} | {total} | "
        f"{accuracy:.0%} ({correct}/{total}) | {top_str} | _pending_ |"
    )
    print(f"Judge accuracy: {correct}/{total} ({accuracy:.0%}); target is 50% (chance).")
    print("Append this row to evals/indistinguishability-log.md:")
    print(row)
    return 0


def main():
    ap = argparse.ArgumentParser(description="Pairwise indistinguishability trial plumbing.")
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--pair", action="store_true")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--channel")
    ap.add_argument("--profile")
    ap.add_argument("--run-dir")
    ap.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--trial", type=int)
    ap.add_argument("--generated")
    ap.add_argument("--verdicts")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    args = ap.parse_args()

    if args.prepare:
        if not (args.channel and args.profile and args.run_dir):
            ap.error("--prepare needs --channel, --profile, --run-dir")
        return prepare(args.channel, args.profile, args.run_dir, args.trials, args.seed)
    if args.pair:
        if not (args.run_dir and args.trial and args.generated):
            ap.error("--pair needs --run-dir, --trial, --generated")
        return pair(args.run_dir, args.trial, args.generated)
    if args.score:
        if not (args.run_dir and args.verdicts):
            ap.error("--score needs --run-dir and --verdicts")
        return score(args.run_dir, args.verdicts, args.ledger)
    ap.error("pick a stage: --prepare, --pair, or --score")


if __name__ == "__main__":
    sys.exit(main())
