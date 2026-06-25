# /humanise fingerprint

(Re)generate the user's voice fingerprint from their corpus. Run after adding samples to `profile/voice-corpus/`.

Follow `scripts/generate-fingerprint.md`: read every sample, extract descriptors with evidence, measure the tripwires, write `profile/voice-fingerprint.md`, and note the gaps (channels with no samples). The same step also builds the voiceprint baseline (`humanise voiceprint --build`, or `scripts/build_voiceprint.py`), the machine-readable twin used to flag drafts that drift from your voice. Promotion of newly confirmed patterns goes through the gate in `evals/self-harness-loop.md`.

More samples, better voice. The fingerprint is the highest-leverage thing the user can refresh; everything else is rules. Regenerate it (and rebuild the voiceprint) after roughly every five new samples, or whenever a channel first gets real coverage.
