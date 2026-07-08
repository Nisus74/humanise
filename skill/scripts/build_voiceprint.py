#!/usr/bin/env python3
"""Build or apply a voiceprint baseline, and report corpus status. Standard library only.

The voiceprint baseline is the machine-readable twin of the voice-fingerprint
diagnostic table (see `generate-fingerprint.md`): per-feature mean and standard
deviation across the user's own corpus samples. It lives in `profile/` (the soul)
and never ships; `scripts/build.mjs` excludes `/profile` from `dist/`.

Distance is advisory. It flags a drifted draft for the held-out judge to look at;
it is never a target to tune a draft toward (see `evals/self-harness-loop.md`).

Build:   python3 build_voiceprint.py --corpus ../profile
Score:   python3 build_voiceprint.py --score draft.md --baseline ../profile/voiceprint.json
Status:  python3 build_voiceprint.py --status [--profile ../profile] [--json]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Reuse the engine's feature extractor: the body computes features, the soul
# stores the baseline. Keeps the voiceprint and the live checker in lockstep.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "evals" / "assertions"))
from writing_checks import voiceprint_features, voiceprint_distance  # noqa: E402

MIN_SAMPLE_WORDS = 30
# Per-channel floor for the pairwise voice test: one sample to hold out, one to draft from.
ELIGIBLE_MIN_SAMPLES = 2

# Longest names first so hyphenated channels win the filename match when a sample
# has no `channel:` frontmatter.
KNOWN_CHANNELS = (
    "investor-update",
    "status-update",
    "cover-letter",
    "board-paper",
    "long-form",
    "linkedin",
    "email",
    "slack",
    "chat",
    "prd",
    "blog",
)

_FM_LINE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")


def parse_frontmatter(raw):
    """Split a sample into (frontmatter dict, body).

    Single-line `key: value` pairs only; multi-line list values are skipped, which
    covers every field the sample template needs read here (channel, date,
    dogfood_status, context).
    """
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    meta = {}
    for line in raw[3:end].splitlines():
        m = _FM_LINE.match(line)
        if m:
            meta[m.group(1)] = m.group(2).strip()
    return meta, raw[end + 4:].lstrip("\n")


def _channel_from_name(path):
    stem = path.stem
    rest = stem[len("sample-"):] if stem.startswith("sample-") else stem
    for ch in KNOWN_CHANNELS:
        if rest == ch or rest.startswith(ch + "-"):
            return ch
    return rest.split("-")[0] if rest else "unknown"


def discover_samples(profile_dir):
    """[(channel, path, frontmatter, body)] for every flat sample-*.md in profile_dir.

    Flat is the only layout: samples live directly in profile/ as
    sample-<channel>-<slug>.md, so the glob keeps soul/config files (soul.md,
    identity.md, voiceprint.json) out. Channel comes from `channel:` frontmatter
    first, the filename second. A leftover nested voice-corpus/ dir is ignored
    with a migration pointer.
    """
    profile = Path(profile_dir)
    legacy = profile / "voice-corpus"
    if legacy.is_dir():
        print(
            f"Ignoring legacy nested corpus at {legacy}. Move each sample to a flat "
            "profile/sample-<channel>-<slug>.md file (see the profile's CORPUS.md).",
            file=sys.stderr,
        )
    samples = []
    for path in sorted(profile.glob("sample-*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        channel = meta.get("channel") or _channel_from_name(path)
        samples.append((channel, path, meta, body))
    return samples


def build(corpus_dir, out_path):
    texts = [
        body
        for _, _, _, body in discover_samples(corpus_dir)
        if len(body.split()) >= MIN_SAMPLE_WORDS
    ]
    if not texts:
        print(
            f"No usable samples (>= {MIN_SAMPLE_WORDS} words) under {corpus_dir}.",
            file=sys.stderr,
        )
        return 1
    vectors = [voiceprint_features(t) for t in texts]
    features = {}
    for key in vectors[0]:
        vals = [v[key] for v in vectors]
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        features[key] = {"mean": round(mean, 4), "stdev": round(var ** 0.5, 4)}
    baseline = {"samples": len(texts), "features": features}
    Path(out_path).write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote voiceprint baseline from {len(texts)} sample(s) to {out_path}")
    if len(texts) < 3:
        print(
            "Note: fewer than 3 samples. The baseline is unstable and distance will "
            "not flag until the corpus grows.",
            file=sys.stderr,
        )
    return 0


def score(draft_path, baseline_path):
    baseline = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    draft = Path(draft_path).read_text(encoding="utf-8")
    print(json.dumps(voiceprint_distance(draft, baseline), indent=2))
    return 0


def status_report(profile_dir, baseline_path):
    """Corpus and voiceprint state as a dict: the preflight for /humanise improve."""
    samples = discover_samples(profile_dir)
    channels = {}
    newest_sample = 0.0
    for channel, path, meta, body in samples:
        entry = channels.setdefault(channel, {"samples": 0, "usable": 0, "eligible": False})
        entry["samples"] += 1
        usable = len(body.split()) >= MIN_SAMPLE_WORDS
        ghostwritten = "fully ghostwritten" in meta.get("dogfood_status", "")
        if usable and not ghostwritten:
            entry["usable"] += 1
        newest_sample = max(newest_sample, path.stat().st_mtime)
    for entry in channels.values():
        entry["eligible"] = entry["usable"] >= ELIGIBLE_MIN_SAMPLES
    baseline = Path(baseline_path)
    if not baseline.exists():
        vp = {"path": str(baseline), "state": "missing", "samples_in_baseline": 0}
    else:
        built_from = json.loads(baseline.read_text(encoding="utf-8")).get("samples", 0)
        state = "stale" if newest_sample > baseline.stat().st_mtime else "fresh"
        vp = {"path": str(baseline), "state": state, "samples_in_baseline": built_from}
    return {
        "profile": str(Path(profile_dir).resolve()),
        "samples_total": len(samples),
        "channels": channels,
        "eligible_channels": sorted(ch for ch, e in channels.items() if e["eligible"]),
        "voiceprint": vp,
    }


def print_status(report):
    print(f"Profile: {report['profile']}")
    print(f"Samples: {report['samples_total']}")
    for ch in sorted(report["channels"]):
        entry = report["channels"][ch]
        if entry["eligible"]:
            note = "eligible for the pairwise voice test"
        else:
            need = ELIGIBLE_MIN_SAMPLES - entry["usable"]
            note = f"needs {need} more usable sample(s) for the pairwise voice test"
        print(f"  {ch}: {entry['samples']} sample(s), {entry['usable']} usable; {note}")
    vp = report["voiceprint"]
    print(f"Voiceprint: {vp['state']} ({vp['path']}, built from {vp['samples_in_baseline']} sample(s))")
    if not report["eligible_channels"]:
        print(
            "No channel is ready for the pairwise voice test yet. The profile's "
            "CORPUS.md lists which samples to paste next, highest impact first."
        )


def main():
    ap = argparse.ArgumentParser(
        description="Build or apply a voiceprint baseline, or report corpus status."
    )
    ap.add_argument("--corpus", help="directory of corpus samples to build from")
    ap.add_argument("--out", help="output baseline path (default: <corpus>/voiceprint.json)")
    ap.add_argument("--score", help="a draft file to score against a baseline")
    ap.add_argument("--baseline", help="baseline JSON to score against or report on")
    ap.add_argument("--status", action="store_true", help="report corpus and voiceprint state")
    ap.add_argument("--profile", help="profile directory for --status (default: ../profile)")
    ap.add_argument("--json", action="store_true", help="emit --status output as JSON")
    args = ap.parse_args()

    if args.status:
        profile = args.profile or args.corpus or str(
            Path(__file__).resolve().parent.parent / "profile"
        )
        if not Path(profile).is_dir():
            print(f"No profile directory at {profile}.", file=sys.stderr)
            return 1
        baseline = args.baseline or str(Path(profile) / "voiceprint.json")
        report = status_report(profile, baseline)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_status(report)
        return 0
    if args.score:
        if not args.baseline:
            ap.error("--score requires --baseline")
        return score(args.score, args.baseline)
    if args.corpus:
        out = args.out or str(Path(args.corpus).resolve() / "voiceprint.json")
        return build(args.corpus, out)
    ap.error("provide --corpus to build, --score with --baseline to score, or --status")


if __name__ == "__main__":
    sys.exit(main())
