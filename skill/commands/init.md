# humanise: init

Set up the user's voice without making them complete a profile before seeing value.

## Quick setup, about three minutes

1. Resolve the private profile path. In a Claude Code marketplace plugin, use
   `${CLAUDE_PLUGIN_DATA}/profile`; otherwise use the configured path or `profile/` beside the skill.
   If it is missing, copy `profile.template/` there. For a direct skill install, copy
   `config.example.yml` to `config.yml` beside `SKILL.md`.
2. Ask the user to paste one short piece they wrote and like. A sent email, post, message or document
   paragraph is enough. Ask them to remove anything sensitive first.
3. Ask what the sample was trying to achieve and who read it. Do not ask a long style questionnaire.
4. If the user supplied text to improve, create up to three versions:
   - close: minimal change;
   - direct: point and ask moved forward;
   - conversational: warmer and closer to speech.
5. Ask which version is closest and what they would change. The choice and correction are stronger
   evidence than abstract style adjectives.
6. Save the original sample as `profile/sample-<channel>-<slug>.md` using `SAMPLE_TEMPLATE.md`.
7. Write the observed decisions to `profile/voice-decisions.md` with `provisional` confidence. Record
   any rejected moves in `profile/negative-examples.md`.
8. Fill only the known fields in `profile/identity.md` and `config.yml`. Leave unknowns explicit.

At this point, produce a useful personalised draft. Do not block on a full fingerprint.

## Deeper setup, offered after value is visible

When the user wants better coverage:

1. Use `scripts/corpus-questionnaire.md` to collect five to ten real samples across the channels they
   actually use.
2. Write `profile/soul.md` from concrete convictions, not generic values.
3. Keep `profile/absolute-rules.md` to explicit non-negotiables. Do not install engine defaults as
   personal absolutes.
4. Run `scripts/generate-fingerprint.md` to build `profile/voice-fingerprint.md`. Label every pattern
   confirmed, supported or provisional and name its evidence.
5. Add relationship-specific differences to `profile/relationships.md` only when direct evidence
   supports them.

## Privacy gate

Before saving samples, confirm the profile path is not tracked by Git. If uncertain, run
`humanise doctor --provider=<name> --project` or inspect `git status`. Stop and warn the user if a
private profile is tracked.

The user can begin with one sample. More evidence should improve an active channel, not become
onboarding homework.
