# Shiru Flatpak v6.6.1-beta.1

This release packages upstream **RockinChaos/Shiru v6.6.1-beta.1**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.6.1-beta.1
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.1)

## Upstream Changelog
* chore: block local network access in android fetch proxy
  * Extensions on Android that require the fetch proxy to reach external sources are now prevented from accessing private or local network addresses, stripping sensitive request options.
* chore: cache pending notifications
  * Fixes a bug where pending notifications were lost if the app was closed before they were sent.
* chore: improve notifications refresh
