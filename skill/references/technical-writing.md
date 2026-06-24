# Technical writing

Technical writing has its own rules. A commit message, a code comment, and a design doc are not prose. Applying the prose skill directly to them produces something worse than the default.

This file covers the technical formats the user writes in most: code comments, commit messages, pull request descriptions, ADRs, RFCs, and PRDs. The general prose rules still apply where they make sense; specific overrides are called out here.

---

## Code comments

Code comments explain the reasoning behind the code, not the code itself.

**What to include:**

- Why this approach was chosen over obvious alternatives
- What invariants the code assumes
- Non-obvious side effects or coupling
- References to external context (ticket, RFC, paper, standard)
- Known limitations and their rationale

**What not to include:**

- Restating what the code does ("// increment counter")
- Generic good-code platitudes
- Verbose preamble before a function definition
- Out-of-date instructions left from earlier iterations

**Tone:** Direct and technical. Contractions are fine. Specific language matters more than polish.

**AusE doesn't apply to identifiers and technical terms.** `color` as a variable name is conventional even in Australian codebases. Prose comments can use AusE (`// The calibration routine summarises three samples`) but naming should follow the surrounding codebase's convention.

**Examples:**

Good:

```python
# Using polling here rather than websockets because the sensor firmware
# drops idle connections after 30s. Revisit if firmware v2 fixes this.
```

Bad:

```python
# This function increments the counter by one.
```

---

## Commit messages

Conventional-commit format is standard: `type(scope): subject`.

- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`, `build`
- Scope: the component or area affected, one word
- Subject: imperative present tense, under 50 characters, no trailing period

**Body (if needed):** Blank line after subject, then wrapped at 72 characters. Body explains the why. Subject explains the what.

**Examples:**

Good:

```
fix(sensor-ingest): handle missing timestamp in calibration records

Device firmware v1.3 sends calibration records without timestamps when
the sensor is in self-test mode. We were dropping these silently;
now we backfill with the system timestamp and log a warning.

Closes #142
```

Bad:

```
Fixed the bug that was causing issues with calibration.
```

**The prose skill doesn't apply to commit subjects.** "feat(auth): add JWT validation" is correct. "Adding a robust, seamless authentication layer" is wrong both as a commit message and as prose. Don't rewrite commit messages to sound more human.

---

## Pull request descriptions

**Structure:**

- What changed (one line)
- Why (one paragraph)
- How tested (bullet list)
- Follow-ups (bullet list, if any)
- Screenshots or log output (if relevant)

**Voice:** Terse and specific. PR descriptions are read by reviewers deciding whether to LGTM. Every sentence earns its place.

**Templates:** If the repo has a PR template, follow it exactly. Don't inject "According to best practices..." or marketing-style summaries.

**Example:**

```
What changed: Moves sensor calibration logic out of the ingest
pipeline into a dedicated calibration service.

Why: Calibration was blocking ingest when recalibration ran.
Pilot sites are adding sensors faster than expected; separating
the concerns lets us scale calibration independently.

How tested:
- Unit tests for the new calibration service (coverage 94%)
- Integration test covering the ingest → calibration handoff
- Load-tested at 1000 samples/sec against the RPA pilot fixture

Follow-ups:
- Migrate the remaining two callsites (tracked in #201)
- Add telemetry once the service is deployed to staging
```

---

## Architecture Decision Records (ADRs)

**Format:**

- Title (imperative: "Use TimescaleDB for sensor telemetry")
- Status (proposed / accepted / deprecated / superseded)
- Context (what problem are we solving, what's the current state)
- Decision (what we're doing)
- Consequences (what becomes easier, what becomes harder, what's uncertain)

**Voice:** Direct, specific, decisive. ADRs that read like "one could consider" documents don't serve their purpose.

**Length:** Usually 200–600 words. If shorter, the decision probably doesn't need an ADR. If longer, it's probably an RFC.

**What to avoid:**

- Hedging the decision itself (the decision is the point)
- Skipping the consequences section (this is where the honesty lives)
- Writing consequences as all-positives (a real decision has trade-offs)

---

## RFCs and design docs

**Audience:** Engineers and tech-literate stakeholders who will review the approach before implementation.

**Structure (one common shape):**

- Summary
- Goals and non-goals
- Background / current state
- Proposed design
- Alternatives considered (and why rejected)
- Open questions
- Timeline and ownership

**Length:** 1000–4000 words typical. Longer means either the design is too complex or the document is padded.

**Voice:** Opinionated. The author has a position; the RFC defends it while remaining open to counter-arguments. RFCs with no position don't drive decisions.

**Alternatives section:** Critical. List two to four real alternatives and explain why they were rejected. If every alternative looks terrible, the comparison isn't credible.

**Open questions:** Leave them visible. Don't pretend every question is answered. A good RFC has three to five open questions near the end.

**Diagrams:** Include where helpful. ASCII, Mermaid, or inline images. Don't embed diagrams the reader can't see.

**Prose rules:** Mostly apply. Specific exceptions: technical precision beats readability where they conflict; acronyms and jargon are fine once defined; AusE spelling applies in prose but not in code blocks or technical identifiers.

---

## PRDs

Covered in detail in `channel-playbooks.md`. Short summary here:

**The difference between a PRD and an RFC:** a PRD asks "what should we build?" and an RFC asks "how should we build it?". Both can coexist for the same feature; the PRD comes first.

**Opening:** Problem statement with a specific user and a specific unmet need. Not "users want more features."

**Success criteria:** Measurable. "Reduces calibration time from 3 hours to under 30 minutes" beats "improves calibration speed."

**Scope:** What's in and what's out, explicitly. A PRD without an "out of scope" section is ambiguous by default.

**Voice:** Direct. PRDs are decision documents; they need a position.

---

## Status docs, runbooks, operational docs

**Runbooks** are instructions for humans under pressure. Write them accordingly: numbered steps, explicit commands, expected output, what to do if output differs.

**Voice for runbooks:**

- Imperative ("Check the queue depth in Grafana") not hedged ("You might want to check the queue depth")
- No preamble ("In this document we will..."). First line is the first step.
- Verification steps after each action ("Output should show <100; if higher, proceed to step 5")
- Escalation path explicit at the bottom

**Status docs** like `STATUS.md` or `NOTES.md` in a repo are written for a future reader (often yourself) who's picking up context. Include the what, when, and why. Skip the persuasion.

---

## General principle

Technical writing trades ornamentation for precision. The reader is deciding whether to merge, deploy, trust, or approve. Every word should help them decide.

If the prose skill's rules conflict with the technical conventions of a format (commit message imperative, runbook step numbering), the technical convention wins. Don't rewrite a commit subject as a flowing sentence to avoid the imperative.
