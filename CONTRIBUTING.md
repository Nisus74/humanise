# Contributing to humanise

Thanks for your interest in contributing. Here's what you need to know.

## How to contribute

1. Fork the repository
2. Create a branch: `git checkout -b your-feature-name`
3. Make your changes
4. Open a pull request with a clear description of what you've changed and why

## Reporting bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) to file an issue.

## Suggesting features

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) to propose new ideas.

## Pull request guidelines

- Keep PRs focused: one change per PR
- Include a clear description of the problem you're solving
- If you're adding or changing skill behaviour, update the README accordingly

## What's engine vs profile

- **Engine** (`skill/SKILL.md`, `skill/references/`, `skill/evals/`, `skill/agents/`, `skill/scripts/`): universal. PRs welcome.
- **Profile** (`skill/profile/`): personal. Never PR your own voice, soul, or corpus into the shared engine. Keep your profile in your fork.

If a change only helps your writing, it's a profile change. If it helps everyone's, it's an engine change.

## The bar (the acceptance gate)

humanise improves the way it tells you to write: evidence first, regression-gated. The model is `skill/evals/self-harness-loop.md`. Every engine change names four things: the **target** (the failure it fixes), the **surface** (what it edits), the **evidence** (why), and the **eval result** (the gate it cleared). Then:

- **Held-in:** `cd skill/evals/assertions && python3 selftest.py` stays green. Add a fixture if you add a detector.
- **Held-out:** the pairwise indistinguishability test (`skill/evals/indistinguishability.md`) doesn't get worse.

Promote only if the change improves at least one split and degrades neither. CI runs the held-in suite on every PR.

## Good first contributions

- **A dialect pack.** Add `skill/references/dialects/<code>.md` plus the spelling lists in `writing_checks.py`. en-CA, en-IE and others are wanted.
- **A channel playbook.** Add a row to the mapping table or a full entry in `skill/references/channel-playbooks.md`.
- **A slop word or a 2026-era tell.** Add it to `skill/references/ai-slop-dictionary.md` and the relevant list in `writing_checks.py`, with a fixture.

## Security

humanise works across AI tools (Claude Code, Codex, Gemini, Antigravity and others), so the protections that matter run at the git and CI layers, not inside any one tool.

After cloning, turn on the local hooks once with `pre-commit install`. Every commit is then checked by [gitleaks](https://github.com/gitleaks/gitleaks) (no secrets) and a zero-dependency check (the CLI stays Node built-ins, the checker stays Python stdlib). CI runs the same checks on every push and pull request, and adds dependency review and CodeQL once the repository is public, so anything missed locally is still caught before merge.

Never commit a real credential; use an environment variable or a gitignored file. To add a dependency, change `scripts/check-no-deps.mjs` in the same PR so the call is explicit and reviewed. Claude Code users also get these guards as instant local feedback via `.claude/`; other tools rely on the git and CI layers.

To report a vulnerability, follow [SECURITY.md](SECURITY.md).

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be kind and constructive.
