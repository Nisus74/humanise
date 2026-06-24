# Example profile: Travis (scrubbed)

A real, working profile trimmed to what's safe to publish. It ships `identity.md`, `soul.md`, and `absolute-rules.md`, so you can see the shape of a filled-in profile and, in particular, a real `soul.md`.

**Deliberately not here:** the voice fingerprint and the voice corpus. Those are generated from private writing samples and stay private. That's the whole point of the body/soul split: the engine is public, the soul is yours.

To start from this example:

```
cp -r profile.example profile
```

then replace the contents with your own. To start clean instead, `cp -r profile.template profile`. Either way, generate your fingerprint from your own samples (`scripts/generate-fingerprint.md`); don't inherit someone else's.
