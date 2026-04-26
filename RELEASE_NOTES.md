# Shiru Flatpak v6.5.3-beta.5

This release packages upstream **RockinChaos/Shiru v6.5.3-beta.5**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.5.3-beta.5
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.5)

## Upstream Changelog
* feat: spoiler control settings
  * Adds a configurable spoiler control system that hides episode and series content based on watch progress. Users can choose from five protection levels (Minimal, Moderate, Strict, Hermit) and define which list status types the control applies to.
  * This is set to off by default, which will result in all episode cards showing their images regardless of watch progress. You can set it to Minimal and add your preferred list statuses to return to the previous behavior.
* feat: video cover toggle
  * Adds a toggle in the player dropdown to enable or disable filling the video to the full width.
  * The toggle and its keybind now persist across restarts.
* fix: prevent list mutation race conditions
  * Entry updates and deletions are now chained to prevent race conditions and ensure errors are surfaced correctly.
* chore: increase the number of displayed season years
