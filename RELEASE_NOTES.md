# Shiru Flatpak v6.8.0-beta.1

This release packages upstream **RockinChaos/Shiru v6.8.0-beta.1**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.8.0-beta.1
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.8.0-beta.1)

## Upstream Changelog
<div align="center">

### NOTICE: YOU WILL NOT BE ABLE TO DOWNGRADE AFTER UPDATING WITHOUT DATA LOSS!

</div>

---
* feat: shared cache across users
  * Introduces a shared cache between users for generic query data and media.
  * Improves performance by dropping nested query cache.
  * Extensions are now shared across profiles.
  * Bumps IndexedDB version from v1 to v2, migrating data from their old caches to the new structure.
  * **Note:** After upgrading, a downgrade will NOT be possible without data loss!
* feat: support relative paths in extension manifests (#167)
* feat: add scheduled cache eviction
* fix: memory leaks and navigation performance
  * Fixes performance issues across home, search, and navigation
  * Home sections outside viewport are no longer loaded
  * Cards outside viewport are hidden until visible
  * Fixes search page performance
  * Fixes AudioLabel causing slow navigation
  * Fixes store subscribe leaks
  * Fixes base font size calculation
* fix: loading local extensions from path (#170)
  * Fixes loading extensions from file path on Linux and macOS.
* fix: searching and resolving titles with ASCII characters
* fix: now playing button active condition
* fix: extension worker race conditions
* fix: show skip/resolver prompt
* fix: torrent card image spoiler
* chore: improve smart image fallback
  * Introduces proper placeholder images when an image fails to load.
  * Fixes resolving promises for image links.
* chore: reduce redundant mappings usage
* chore: adjust mappings cache strategy
* chore: add extensions cache reset options
* chore: update deps
