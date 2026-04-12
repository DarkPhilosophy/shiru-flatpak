# Shiru Flatpak v6.5.3-beta.1

This release packages upstream **RockinChaos/Shiru v6.5.3-beta.1**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.5.3-beta.1
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.1)

## Upstream Changelog
* feat: offline progress syncing
  * Changes to your list (e.g. progress and favourite changes) will now be tracked while offline and sync to AniList/MyAnimeList when back online.
  * Fixes a race condition where changes to your list during a user lists fetch could become stale for very large user lists.
  * User lists are now automatically fetched when the network or api comes back online.
* feat: player title position toggle ([#134](https://github.com/RockinChaos/Shiru/pull/134))
  * Adds a toggle to the player settings to change the title overlay location from the top left to the bottom left.
* fix: correct back/forward state after modal navigation
  * Fixed forward button incorrectly graying out after pressing back to reopen a modal.
  * Fixed navigating back twice after closing a modal returning to the wrong page instead of the modal.
* fix: visible progress in anime details
  * Fixes the indicated watch progress when audio labels are enabled not reactively updating when changing the progress via the list editor.
* fix: handling episode range
  * Fixes episode card batches showing the proper episode range.
* fix: resolving Hikuidori
  * Fixes resolving Hikuidori when release groups use the MyAnimeList titles.
* fix: webpack-dev-server connection
* chore: reduce ambiguous IPC usage
* chore: Android ui tweaks
* chore: bump to webtorrent v2.8.7
* chore: update deps
