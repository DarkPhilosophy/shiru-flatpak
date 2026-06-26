# Shiru Flatpak v6.7.2-beta.1

This release packages upstream **RockinChaos/Shiru v6.7.2-beta.1**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.7.2-beta.1
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.7.2-beta.1)

## Upstream Changelog
* feat: URL array support for update and main fields
  * Supports an array of URLs for extension update and repository main fields.
  * Attempts each URL in order, falling back to subsequent URLs if unavailable.
* feat: skip update prompt for ignored version on restart (#166)
* fix: allow batch lookup for multi-episode movies
* fix: add missing extensions on update check
* fix: make dedupe case insensitive
* chore: notify on change of repository manifest
* chore: simplify extension cards
