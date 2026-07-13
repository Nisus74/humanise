#!/usr/bin/env bash
# humanise: PostToolUse hook after Write/Edit. Two non-blocking "dogfood" checks.
# Always exits 0 (never blocks an edit). Disable by removing the hook from
# .claude/settings.json. Requires jq; the prose check also needs python3.
#
#   1. Markdown doc edited -> run the humanise checker, surface a one-line slop
#      summary (only when something fails, to stay quiet).
#   2. The checker or a rule file edited -> run the held-in selftest (npm test),
#      the acceptance gate from skill/evals/self-harness-loop.md.

input="$(cat)"
f="$(printf '%s' "$input" | jq -r '.tool_response.filePath // .tool_input.file_path // empty' 2>/dev/null)"
[ -n "$f" ] || exit 0
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# 1) Prose check on shipped Markdown docs.
case "$f" in
  *.md)
    case "$f" in
      */dist/*|*CHANGELOG*|*/skill/references/*|*/skill/evals/*) : ;;  # generated / rules / eval docs: skip
      *)
        summary="$(node "$root/cli/bin/cli.js" detect "$f" 2>/dev/null | python3 -c '
import sys, json
try:
    s = json.load(sys.stdin).get("_summary", {})
    failed = s.get("failed") or []
    if failed:
        adv = len(s.get("advisory_flagged") or [])
        extra = " (+%d advisory)" % adv if adv else ""
        print("%d/%d checks pass; FAILED: %s%s" % (s.get("passed", 0), s.get("total_checks", 0), ", ".join(failed), extra))
except Exception:
    pass
' 2>/dev/null)"
        [ -n "$summary" ] && echo "humanise checker [$f]: $summary"
        ;;
    esac
    ;;
esac

# 2) Selftest when the engine's rules or checker change.
case "$f" in
  *skill/evals/assertions/writing_checks.py|*skill/references/*)
    echo "humanise: rule file changed, running held-in selftest (npm test)..."
    ( cd "$root" && npm test ) 2>&1 | tail -n 20
    ;;
esac

exit 0
