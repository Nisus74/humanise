# Security policy

## Reporting a vulnerability

Please report security issues privately. Open a [GitHub security advisory](https://github.com/Nisus74/humanise/security/advisories/new) on this repository rather than a public issue, or contact the maintainer via their GitHub profile. You can expect an acknowledgement within a few days.

Please do not open a public issue or pull request for an unfixed vulnerability.

If you suspect a malicious or compromised update, disable that version and compare it with the
previous release tag. Report the version, install source and changed files privately. Do not paste
credentials or private profile text into the report.

## Supported versions

humanise ships from the `main` branch and the latest npm release. Fixes land on `main` and go out in the next release; older versions are not patched separately.

## Scope

In scope: the CLI (`cli/`), the build (`scripts/`), the checker (`skill/evals/assertions/writing_checks.py`), and the CI and hook configuration.

Out of scope: a user's own voice profile and corpus (these stay in their fork and never reach this repo), and the output of any third-party AI tool that runs the skill.

## How the project protects itself

- Secrets are scanned on every commit (gitleaks via pre-commit) and again in CI.
- The project ships zero runtime dependencies; a check in pre-commit and CI fails if a dependency or lockfile appears.
- GitHub Actions are pinned to commit SHAs and updated by Dependabot.
- CodeQL scans the JavaScript and Python on every push and pull request, and weekly, once the repository is public.
- Changes to the skill, hooks, workflows, package boundary and release configuration request owner review through CODEOWNERS.
