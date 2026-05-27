# Shiru Flatpak v6.6.1-beta.5

This release packages upstream **RockinChaos/Shiru v6.6.1-beta.5**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.6.1-beta.5
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.5)

## Upstream Changelog
* feat: rewrite sidebar and bottombar navigation
  * Redesigned the sidebar and bottombar navigation with a cleaner, more flexible system. Both now share the same components and automatically move lower-priority buttons into an overflow "More" menu when space runs out.
  * Adds togglable labels to the navigation buttons. This is enabled by default and can be disabled via Settings -> Interface -> Accessibility Settings -> Show Labels.
* feat: handle AniList token expiry
* feat: Android toast
* fix: launch external player after rejecting prompt
* fix: suppress install prompt on Android
* chore: improve scrolling on the manager page
* chore: improve modal scaling on small screens
* chore: simplify Android insets
* chore: update deps
* chore: refactor
