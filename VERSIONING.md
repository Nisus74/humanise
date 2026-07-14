# Versioning humanise

humanise follows [Semantic Versioning 2.0.0](https://semver.org/). `package.json` is the version
authority. CI fails when the Claude plugin, marketplace listing, README badge or release manifest
does not match it.

## What changes each number

- **Major:** incompatible CLI options, profile or config migrations, renamed modes, changed install
  paths, removed providers, or changes that invalidate documented use.
- **Minor:** backward-compatible modes, providers, language packs, detectors, commands or profile
  fields.
- **Patch:** backward-compatible fixes, documentation corrections, rule clarifications and detector
  precision improvements.
- **Pre-release:** unstable candidates such as `1.1.0-beta.1`. They use an npm pre-release tag and
  never replace `latest` until promoted.

Published versions and Git tags are immutable. Release Please prepares the version pull request from
conventional commits. A maintainer reviews the complete diff and the release gate before creating a
release.
