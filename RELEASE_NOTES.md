# Shiru Flatpak v6.6.1-beta.2

This release packages upstream **RockinChaos/Shiru v6.6.1-beta.2**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.6.1-beta.2
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.2)

## Upstream Changelog
* fix: improve w2g peer discovery and session stability (#148)
* fix: episode list race conditions
* chore: faster offline detection
  * Intercept all fetch requests to detect outages immediately, abort in-flight requests when offline, and ping on startup to catch offline state before any requests are made.
* chore: improve notification card images
* chore: reduce ambiguous event listeners
* chore: update deps
