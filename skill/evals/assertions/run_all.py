"""Aggregator for the humanise evals harness.

Reads `evals/evals.json` and, for each eval, loads a draft file from a given
output directory, runs the assertion battery from `writing_checks.py`, and
produces a `benchmark.json` (and human-readable `benchmark.md`) summarising
pass/fail per eval and overall.

June 2026: assertions may carry `"advisory": true`. Advisory assertions are
graded and reported but excluded from the pass rate; they exist for tripwire
metrics (AusE visibility, contraction count) where failing the draft would
pressure the model into padding, which the skill explicitly bans ("Tripwires,
not targets"). Compound checks ("X and Y") were removed from evals.json because
this parser never supported them; keep each assertion to one comparison.

Expected layout of the outputs directory:

    <outputs_dir>/
        eval-1.txt
        eval-2.txt
        ...

(File can also be `.md`; the script auto-probes both extensions.)

Usage:
    python run_all.py --evals ../evals.json --outputs <dir> --report <out>

Typically called once for the `with_skill` run and once for the `baseline` run,
then the two benchmark.json files are compared. For the pairwise voice test,
see ../indistinguishability.md (judge-based, not runnable from this script).
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

# Allow running from the assertions directory directly.
sys.path.insert(0, str(Path(__file__).parent))
from writing_checks import all_checks  # noqa: E402


def _load_evals(evals_path):
    try:
        with open(evals_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"evals file not found: {evals_path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"evals file is not valid JSON ({evals_path}): {e}")
    if not isinstance(data, dict) or "evals" not in data:
        raise SystemExit(f"evals file missing top-level 'evals' key: {evals_path}")
    return data


def _find_draft(outputs_dir, eval_id):
    """Look for eval-<id>.txt or eval-<id>.md in the outputs directory."""
    base = Path(outputs_dir)
    for ext in (".txt", ".md"):
        p = base / f"eval-{eval_id}{ext}"
        if p.exists():
            return p
    return None


def _evaluate_assertion(check_str, check_results, draft=""):
    """Evaluate a single assertion string against check_results.

    The assertion language is deliberately tiny. Supported forms:
        em_dash_count == 0
        severity_1_slop_count == 0
        ause_count >= 2
        word_count <= 60
        120 <= word_count <= 200
        us_spelling_clean == true
        no_slop_openers == true
        structural_tell_count <= 1
        contains_any(['out of scope', 'non-goals']) == true

    One comparison per assertion. No "and"/"or"; split compound conditions into
    separate assertions.
    """
    s = check_str.strip()

    # contains_any form: `contains_any(['a', 'b']) == true|false`
    # (optional `, case_insensitive=true` is accepted and ignored; the check is
    # always case-insensitive). Previously unparsed; fixed June 2026.
    m = re.match(
        r"^contains_any\(\[(.*?)\]\s*(?:,\s*case_insensitive=\w+\s*)?\)\s*==\s*(true|false)$",
        s,
        re.IGNORECASE,
    )
    if m:
        # Parse the bracketed list as a Python literal so phrases containing an
        # apostrophe ("in today's") are not truncated by a naive quote regex.
        try:
            phrases = list(ast.literal_eval("[" + m.group(1) + "]"))
        except (ValueError, SyntaxError):
            phrases = re.findall(r"""['"](.*?)['"]""", m.group(1))
        expected = m.group(2).lower() == "true"
        lower = draft.lower()
        hit = next((p for p in phrases if p.lower() in lower), None)
        actual = hit is not None
        return actual == expected, (
            f"contains_any: found '{hit}'" if hit else "contains_any: no phrase found"
        )

    # Map assertion names to (category_key, sub_field) in the all_checks dict.
    lookups = {
        "em_dash_count": ("em_dash", "count"),
        "en_dash_count": ("en_dash_non_range", "count"),
        "spaced_hyphen_count": ("spaced_hyphen_dash", "count"),
        "curly_quote_count": ("curly_quotes", "count"),
        "severity_1_slop_count": ("severity_1_slop", "count"),
        "severity_2_3_slop_count": ("severity_2_3_slop", "count"),
        "ause_count": ("ause_visible", "count"),
        "contraction_types": ("contractions", "distinct_types"),
        "word_count": ("word_count", "count"),
        "number_count": ("numbers", "count"),
        "structural_tell_count": ("structural_tells", "count"),
        "binary_contrast_count": ("binary_contrast_density", "count"),
        "fragment_colon_count": ("fragment_colon_headers", "count"),
        "self_narrated_honesty_count": ("self_narrated_honesty", "count"),
        "academic_register_count": ("academic_register", "count"),
        "i_this_opener_count": ("i_this_openers", "count"),
        "sentence_similarity_runs": ("sentence_profile", "runs_of_3"),
        "paragraph_similarity_runs": ("paragraph_shape", "similar_runs"),
        "us_spelling_clean": ("us_spelling_clean", "pass"),
        "ause_spelling_clean": ("ause_spelling_clean", "pass"),
        "no_slop_openers": ("slop_opener", "pass"),
    }

    def value_of(name):
        if name not in lookups:
            return None
        cat, field = lookups[name]
        if cat not in check_results:
            return None
        return check_results[cat].get(field)

    # Boolean form: `<name> == true` / `== false`
    m = re.match(r"^(\w+)\s*==\s*(true|false)$", s, re.IGNORECASE)
    if m:
        name, expected = m.group(1), m.group(2).lower() == "true"
        actual = value_of(name)
        if actual is None:
            return False, f"{name} not available"
        return actual is expected, f"{name}={actual}, expected {expected}"

    # Equality form: `<name> == <int>`
    m = re.match(r"^(\w+)\s*==\s*(\d+)$", s)
    if m:
        name, n = m.group(1), int(m.group(2))
        actual = value_of(name)
        if actual is None:
            return False, f"{name} not available"
        return actual == n, f"{name}={actual}, expected =={n}"

    # Single comparator: `<name> <op> <int>`
    m = re.match(r"^(\w+)\s*(<=|>=|<|>)\s*(\d+)$", s)
    if m:
        name, op, n = m.group(1), m.group(2), int(m.group(3))
        actual = value_of(name)
        if actual is None:
            return False, f"{name} not available"
        passed = {
            "<=": actual <= n,
            ">=": actual >= n,
            "<": actual < n,
            ">": actual > n,
        }[op]
        return passed, f"{name}={actual} {op} {n}"

    # Range form: `<int> <= <name> <= <int>`
    m = re.match(r"^(\d+)\s*<=\s*(\w+)\s*<=\s*(\d+)$", s)
    if m:
        low, name, high = int(m.group(1)), m.group(2), int(m.group(3))
        actual = value_of(name)
        if actual is None:
            return False, f"{name} not available"
        return low <= actual <= high, f"{name}={actual}, expected {low}..{high}"

    return False, f"unparsed assertion: {s}"


def grade_one(eval_def, draft_path):
    """Grade a single eval. Returns a dict with results."""
    hard_assertions = [
        a for a in eval_def.get("assertions", []) if not a.get("advisory")
    ]
    if draft_path is None or not Path(draft_path).exists():
        return {
            "eval_id": eval_def["id"],
            "channel": eval_def.get("channel"),
            "status": "missing_draft",
            "passed": 0,
            "total": len(hard_assertions),
            "assertions": [],
            "checks": {},
        }

    with open(draft_path, "r", encoding="utf-8") as f:
        draft = f.read()

    audience = eval_def.get("audience_tag", "aus")
    medium = eval_def.get("medium", "plain")
    formal = bool(eval_def.get("formal_channel", False))
    checks = all_checks(draft, audience_tag=audience, medium=medium, formal=formal)

    results = []
    for a in eval_def.get("assertions", []):
        passed, detail = _evaluate_assertion(a["check"], checks, draft=draft)
        results.append(
            {
                "name": a["name"],
                "check": a["check"],
                "advisory": bool(a.get("advisory")),
                "passed": passed,
                "evidence": detail,
            }
        )

    hard_results = [r for r in results if not r["advisory"]]
    passed_count = sum(1 for r in hard_results if r["passed"])
    return {
        "eval_id": eval_def["id"],
        "channel": eval_def.get("channel"),
        "workflow": eval_def.get("workflow"),
        "audience_tag": audience,
        "draft_path": str(draft_path),
        "status": "graded",
        "passed": passed_count,
        "total": len(hard_results),
        "pass_rate": passed_count / len(hard_results) if hard_results else 0,
        "advisory_flagged": [
            r["name"] for r in results if r["advisory"] and not r["passed"]
        ],
        "assertions": results,
        "checks": checks,
    }


def aggregate(eval_results):
    total_assertions = sum(r["total"] for r in eval_results)
    passed_assertions = sum(r["passed"] for r in eval_results)
    graded = [r for r in eval_results if r["status"] == "graded"]
    missing = [r for r in eval_results if r["status"] == "missing_draft"]

    advisory_flags = {}
    for r in graded:
        for name in r.get("advisory_flagged", []):
            advisory_flags[name] = advisory_flags.get(name, 0) + 1

    per_channel = {}
    for r in graded:
        ch = r["channel"] or "unknown"
        per_channel.setdefault(ch, {"passed": 0, "total": 0, "evals": 0})
        per_channel[ch]["passed"] += r["passed"]
        per_channel[ch]["total"] += r["total"]
        per_channel[ch]["evals"] += 1

    return {
        "total_evals": len(eval_results),
        "graded_evals": len(graded),
        "missing_drafts": len(missing),
        "assertions_passed": passed_assertions,
        "assertions_total": total_assertions,
        "overall_pass_rate": passed_assertions / total_assertions
        if total_assertions
        else 0,
        "advisory_flag_counts": advisory_flags,
        "per_channel": per_channel,
        "missing_ids": [r["eval_id"] for r in missing],
    }


def write_markdown(report, out_path):
    lines = []
    agg = report["aggregate"]
    lines.append("# Writing-style eval benchmark\n")
    lines.append(f"Outputs scored: {agg['graded_evals']}/{agg['total_evals']}  ")
    lines.append(
        f"Assertions passed: {agg['assertions_passed']}/{agg['assertions_total']}  "
    )
    lines.append(f"Overall pass rate: {agg['overall_pass_rate']:.1%}\n")

    if agg["missing_drafts"]:
        lines.append(f"**Missing drafts:** {agg['missing_ids']}\n")

    if agg.get("advisory_flag_counts"):
        lines.append(
            "**Advisory tripwires flagged (not counted in pass rate):** "
            + ", ".join(
                f"{k} ({v} eval(s))"
                for k, v in sorted(agg["advisory_flag_counts"].items())
            )
            + "\n"
        )

    lines.append("## Per-channel summary\n")
    lines.append("| Channel | Evals | Assertions passed | Pass rate |")
    lines.append("|---|---|---|---|")
    for ch, stats in sorted(report["aggregate"]["per_channel"].items()):
        rate = stats["passed"] / stats["total"] if stats["total"] else 0
        lines.append(
            f"| {ch} | {stats['evals']} | {stats['passed']}/{stats['total']} | {rate:.1%} |"
        )
    lines.append("")

    lines.append("## Per-eval detail\n")
    for r in report["results"]:
        if r["status"] != "graded":
            lines.append(
                f"### Eval {r['eval_id']} ({r.get('channel', '?')}): MISSING DRAFT\n"
            )
            continue
        lines.append(
            f"### Eval {r['eval_id']}: {r['channel']} / {r['workflow']} / {r['audience_tag']}"
        )
        lines.append(f"Passed {r['passed']}/{r['total']} ({r['pass_rate']:.0%})\n")
        for a in r["assertions"]:
            mark = "[x]" if a["passed"] else "[ ]"
            tag = " _(advisory)_" if a["advisory"] else ""
            lines.append(
                f"- {mark} **{a['name']}**{tag} (`{a['check']}`): {a['evidence']}"
            )
        lines.append("")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Grade humanise eval drafts.")
    parser.add_argument(
        "--evals",
        default=str(Path(__file__).parent.parent / "evals.json"),
        help="Path to evals.json",
    )
    parser.add_argument(
        "--outputs",
        required=True,
        help="Directory containing eval-<id>.txt or eval-<id>.md files",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Base path for benchmark.json + benchmark.md (default: <outputs>/benchmark)",
    )
    args = parser.parse_args()

    evals_data = _load_evals(args.evals)
    evals = evals_data["evals"]

    results = []
    for eval_def in evals:
        draft_path = _find_draft(args.outputs, eval_def["id"])
        results.append(grade_one(eval_def, draft_path))

    agg = aggregate(results)
    report = {
        "skill_name": evals_data.get("skill_name", "humanise"),
        "evals_file": args.evals,
        "outputs_dir": args.outputs,
        "aggregate": agg,
        "results": results,
    }

    base = args.report or os.path.join(args.outputs, "benchmark")
    json_path = f"{base}.json"
    md_path = f"{base}.md"

    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    write_markdown(report, md_path)

    print(f"Graded {agg['graded_evals']}/{agg['total_evals']} evals")
    print(
        f"Assertions: {agg['assertions_passed']}/{agg['assertions_total']} passed "
        f"({agg['overall_pass_rate']:.1%})"
    )
    if agg.get("advisory_flag_counts"):
        print(f"Advisory tripwires flagged: {agg['advisory_flag_counts']}")
    if agg["missing_drafts"]:
        print(f"Missing drafts for eval IDs: {agg['missing_ids']}")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")

    # Exit non-zero if any hard assertion failed or any draft was missing, so the
    # harness can gate CI instead of always reporting success.
    ok = (
        agg["missing_drafts"] == 0
        and agg["assertions_passed"] == agg["assertions_total"]
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
