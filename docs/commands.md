# Commands and modes

humanise is one skill with optional mode words. Invocation depends on the host:

```text
Codex:                      $humanise rewrite
Claude Code, direct skill:  /humanise rewrite
Claude Code plugin:         /humanise:humanise rewrite
Cursor:                     /humanise rewrite
Gemini CLI:                 enable humanise, then ask normally
GitHub Copilot:             /humanise rewrite where supported
OpenCode:                   ask the agent to use humanise
Antigravity:                mention humanise by name
Other hosts:                ask the agent to use humanise in rewrite mode
```

The agent may also select humanise automatically when a request matches the skill description.

## `init`

Starts progressive voice setup. One real sample is enough for the quick path. Humanise learns the
sample's purpose and reader, offers distinct rewrite directions, records the user's choice as
provisional evidence and produces a personalised result.

Use deeper setup later to add a soul, several channels, negative examples, relationship overlays and
an evidence-backed fingerprint.

Terminal `humanise init` only scaffolds `profile/` and the canonical `config.yml`; the in-agent mode
runs the interview and calibration.

## `guide`

Drafts new material. Humanise builds a meaning contract and reader model, loads the nearest direct
samples, assesses evidence confidence and writes through separate content, rhetoric, voice and surface
passes.

Example:

```text
$humanise guide
Draft an email asking our pilot customer to approve the revised timeline. They are frustrated about
the previous slip. The new date is 18 August and the validation plan is attached.
```

## `rewrite`

Edits existing text at one of three strengths:

- light edit for errors and friction;
- voice rewrite for new sentences and flow without changing the argument;
- editorial reconstruction when the user asks to challenge the structure or point.

Humanise defaults to the least invasive mode that can satisfy the request.

## `check`

Inspects mechanical and structural risks without pretending that a clean result proves voice quality.

```sh
humanise detect <file> [dialect] [medium]
```

The checker is local and requires Python 3. Advisory counts prompt a review. Never treat them as
targets.

## `fingerprint`

Rebuilds `profile/voice-fingerprint.md` after useful evidence is added. It reads raw samples, negative
examples and draft-to-final edits. Every pattern should include scope, evidence and a confidence label.

Run it after roughly five useful additions or when a channel first gains direct coverage.

## `learn`

Captures the difference between the skill's proposed draft and the text the user actually sent. Record
the changed decision, channel, relationship and reason, when known. The final edit is stronger evidence
than the draft it replaced.

Ask permission before storing user text. Skip code, quotations, changed briefs and facts corrected only
because the source was wrong.

## `improve`

Runs the advanced engine-maintenance workflow. Maintainers use it to improve the shared skill. It does
not belong in ordinary writing work. It benchmarks, mines repeated failures and proposes bounded
changes behind the project's acceptance gate.

Personal voice corrections usually belong in the private profile. Reserve the shared engine for
behaviour that generalises.

## CLI commands

```text
humanise install --provider=<name> [--global|--project]
humanise doctor --provider=<name> [--global|--project]
humanise init [--provider=<name>] [--global|--project]
humanise detect <file> [dialect] [medium]
humanise voiceprint <file>
humanise voiceprint --build
humanise voiceprint --status
humanise build
humanise version
```
