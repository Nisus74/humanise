#!/usr/bin/env bash
# humanise: PreToolUse guard for Bash commands.
# Committed and shared, so it runs in every contributor's Claude Code session.
# It BLOCKS (exit 2) two classes of risk; everything else falls through to exit 0
# and is never blocked.
#
#   1. Supply chain: adding a dependency, or piping a remote script into a shell.
#      humanise is deliberately zero-dependency (Node built-ins, Python stdlib).
#   2. Secrets: a `git commit` whose diff matches a known credential format.
#
# Requires jq (to read the command) and git (for the secret scan). If jq is
# absent the guard no-ops; the repo pre-commit hook and CI still cover secrets.
# Warn instead of block: change the `exit 2` lines to `exit 0`.
# Disable entirely: remove the PreToolUse hook from .claude/settings.json.
#
# Deliberately no `set -e`: an unexpected failure must fall through to exit 0,
# never accidentally block a benign command. Only intentional risks exit 2.

input="$(cat)"
cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)"
[ -n "$cmd" ] || exit 0

# 1) Supply chain ------------------------------------------------------------
# A dependency install (a non-flag package argument is present).
if printf '%s\n' "$cmd" | grep -qE '(^|[;&|[:space:]])(npm|pnpm|yarn)[[:space:]]+(install|add|i)[[:space:]]+[^-[:space:]]'; then
  echo "BLOCKED (supply chain): adding a dependency. humanise is zero-dependency by design (Node built-ins, Python stdlib). Raise it with a maintainer before adding one. See CLAUDE.md." >&2
  exit 2
fi
if printf '%s\n' "$cmd" | grep -qE '(^|[;&|[:space:]])(pip|pip3)[[:space:]]+install'; then
  echo "BLOCKED (supply chain): pip install. The checker is Python stdlib only; security tooling is installed once by a maintainer, not added per task." >&2
  exit 2
fi
# A remote script piped straight into a shell.
if printf '%s\n' "$cmd" | grep -qE '(curl|wget)[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(ba)?sh\b'; then
  echo "BLOCKED (supply chain): piping a remote script into a shell. Download it, read it, then run it deliberately if you trust it." >&2
  exit 2
fi

# 2) Secrets (only when a commit is about to capture them) --------------------
case "$cmd" in
  *"git commit"*)
    root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
    # Lines a commit would add (staged plus unstaged tracked, to cover commit -a).
    added="$({ git -C "$root" diff --cached; git -C "$root" diff; } 2>/dev/null | grep -E '^\+' | grep -vE '^\+\+\+')"
    if printf '%s\n' "$added" | grep -qEi '(-----BEGIN [A-Z ]*PRIVATE KEY-----|A(KIA|SIA)[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|sk-(ant-)?[A-Za-z0-9_-]{20,})'; then
      echo "BLOCKED (secret): the diff this commit would capture matches a known credential format (AWS / GitHub / Slack / Google / OpenAI / Anthropic key, or a PEM private key)." >&2
      echo "Files staged:" >&2
      git -C "$root" diff --cached --name-only 2>/dev/null | sed 's/^/  - /' >&2
      echo "Move the secret to an env var or a gitignored file. False positive? Commit outside Claude, or disable the hook in .claude/settings.json." >&2
      exit 2
    fi
    ;;
esac

exit 0
