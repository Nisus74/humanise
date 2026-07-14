# Contributing to humanise

Contributions are welcome when they make humanise easier to install, safer to ship or better at
preserving a writer's meaning and voice.

## Set up

You need Node 18 or later, Python 3 and [`pre-commit`](https://pre-commit.com/#install).

```sh
git clone https://github.com/<your-name>/humanise.git
cd humanise
pre-commit install --hook-type pre-commit --hook-type pre-push
npm run quality
```

Fork the repository, create a focused branch and show the failure or user need your change addresses.
Run `npm run quality` before opening a pull request.

## Reporting bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) to file an issue.

## Suggesting features

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) to propose new ideas.

## Pull request guidelines

- Keep PRs focused: one change per PR
- Include a clear description of the problem you're solving
- If you're adding or changing skill behaviour, update the README accordingly
- List the exact checks you ran and their results
- Do not add a dependency or lockfile without prior maintainer agreement
- Never include a real voice profile, writing sample, credential or local configuration

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

- **A language or regional pack.** Start with [Adding a language](docs/languages.md) and agree on the evidence and fluent review plan before implementation.
- **A channel playbook.** Add a row to the mapping table or a full entry in `skill/references/channel-playbooks.md`.
- **A slop word or a 2026-era tell.** Add it to `skill/references/ai-slop-dictionary.md` and the relevant list in `writing_checks.py`, with a fixture.

## Security

humanise works across AI tools (Claude Code, Codex, Gemini, Antigravity and others), so the protections that matter run at the git and CI layers, not inside any one tool.

The pre-commit hook scans secrets and rejects dependencies. The pre-push hook runs the same quality
gate as CI: version consistency, build validation, package privacy and the held-in regression suite.

Never commit a real credential. Use an environment variable or a gitignored file. Claude Code and
Codex provide earlier local warnings, but Git hooks and CI are the shared enforcement layer.

To report a vulnerability, follow [SECURITY.md](SECURITY.md).

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be kind and constructive.
