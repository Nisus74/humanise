#!/usr/bin/env python3
"""Build or apply a voiceprint baseline. Standard library only.

The voiceprint baseline is the machine-readable twin of the voice-fingerprint
diagnostic table (see `generate-fingerprint.md`): per-feature mean and standard
deviation across the user's own corpus samples. It lives in `profile/` (the soul)
and never ships; `scripts/build.mjs` excludes `/profile` from `dist/`.

Distance is advisory. It flags a drifted draft for the held-out judge to look at;
it is never a target to tune a draft toward (see `evals/self-harness-loop.md`).

Build:  python3 build_voiceprint.py --corpus ../profile/voice-corpus --out ../profile/voiceprint.json
Score:  python3 build_voiceprint.py --score draft.md --baseline ../profile/voiceprint.json
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
SKIP_NAMES = {"README.md", "SAMPLE_TEMPLATE.md"}


def _read_samples(corpus_dir):
    """Every corpus sample's body (frontmatter stripped), long enough to measure."""
    texts = []
    for path in sorted(Path(corpus_dir).rglob("*.md")):
        if path.name in SKIP_NAMES:
            continue
        raw = path.read_text(encoding="utf-8")
        body = re.sub(r"^---.*?---\s*", "", raw, flags=re.DOTALL)
        if len(body.split()) >= MIN_SAMPLE_WORDS:
            texts.append(body)
    return texts


def build(corpus_dir, out_path):
    texts = _read_samples(corpus_dir)
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


def main():
    ap = argparse.ArgumentParser(description="Build or apply a voiceprint baseline.")
    ap.add_argument("--corpus", help="directory of corpus samples to build from")
    ap.add_argument("--out", help="output baseline path (default: <corpus>/../voiceprint.json)")
    ap.add_argument("--score", help="a draft file to score against a baseline")
    ap.add_argument("--baseline", help="baseline JSON to score against")
    args = ap.parse_args()

    if args.score:
        if not args.baseline:
            ap.error("--score requires --baseline")
        return score(args.score, args.baseline)
    if args.corpus:
        out = args.out or str(Path(args.corpus).resolve().parent / "voiceprint.json")
        return build(args.corpus, out)
    ap.error("provide --corpus to build, or --score with --baseline to score")


if __name__ == "__main__":
    sys.exit(main())
