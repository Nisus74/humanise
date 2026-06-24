# /humanise fingerprint

(Re)generate the user's voice fingerprint from their corpus. Run after adding samples to `profile/voice-corpus/`.

Follow `scripts/generate-fingerprint.md`: read every sample, extract descriptors with evidence, measure the tripwires, write `profile/voice-fingerprint.md`, and note the gaps (channels with no samples). Promotion of newly confirmed patterns goes through the gate in `evals/self-harness-loop.md`.

More samples, better voice. The fingerprint is the highest-leverage thing the user can refresh; everything else is rules.
