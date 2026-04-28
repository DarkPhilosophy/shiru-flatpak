# Shiru Flatpak v6.5.3-beta.6

This release packages upstream **RockinChaos/Shiru v6.5.3-beta.6**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.5.3-beta.6
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.6)

## Upstream Changelog
* feat: extension custom settings
  * Extensions can now declare custom settings in their manifest. Values are persisted alongside the enabled state and passed to the worker on load and on change.
* feat: respect extension enabled state in worker lifecycle
  * Extensions that are disabled no longer load or validate their workers on startup or network recovery. Toggling an extension off terminates its worker immediately, and toggling it on loads and validates it on demand.
* fix: infinitely awaiting network check
* fix: preview card spoilers
