#!/usr/bin/env bash
# Convenience runner for humanise.
#   ./scripts/run-checks.sh                 run the held-in self-test
#   ./scripts/run-checks.sh path/to/draft   run the checker on a draft
# Dialect for the draft run comes from $DIALECT (default: aus). Medium is arg 2 (default: plain).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSERT="$ROOT/skill/evals/assertions"
if [ -z "$1" ]; then
  cd "$ASSERT" && python3 selftest.py
else
  DIALECT="${DIALECT:-aus}"
  python3 "$ASSERT/writing_checks.py" "$1" "$DIALECT" "${2:-plain}"
fi
