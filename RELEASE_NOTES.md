# Shiru Flatpak v6.8.0-beta.3

This release packages upstream **RockinChaos/Shiru v6.8.0-beta.3**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.8.0-beta.3
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.8.0-beta.3)

## Upstream Changelog
<div align="center">

### NOTICE: AS OF `v6.8.0-beta.1` YOU WILL NOT BE ABLE TO DOWNGRADE AFTER UPDATING WITHOUT DATA LOSS!

</div>

---
* feat: splash screen
  * A splash screen will now be shown between switching profiles and when a reload is triggered on settings reset or when clearing caches.
* fix: show correct changelog for latest update
  * The GitHub API can be slow to update the releases feed, if our update version is missing we will just fetch it directly instead of showing the previous releases changelog.
* fix: crash on file change with stats overlay
* fix: sync user extension settings with shared database
* fix: incorrectly showing buffering
* fix: persisted video cover
* chore: improve Android TV navigation (#163)
* chore: increase maximum transfer speed to 1GiB
* chore: update deps
