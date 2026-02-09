
# Changelog

## Project notes
This repository packages the official Shiru `.deb` releases into Flatpak for convenience.
It does not modify upstream source code.

## v1.0.2
- Fix input mapping issues on high-DPI Wayland displays.
- Implement smart launcher script to auto-detect Wayland and enable native Ozone platform.
- Move documentation files to `.github/` for cleaner root directory.

## v1.0.1
- Move Flatpak runtime and SDK to 25.08.
- Track upstream releases in `UPSTREAM_VERSION` while keeping project versioning separate.
- Update workflow naming and release logic to compare against `UPSTREAM_VERSION`.
- Improve build script handling for runtime changes and repo URL updates.

<!-- LATEST-VERSION-START -->
<details open>
<summary><strong>Upstream release v6.5.0</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.0](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.0)

### Notes
* feat: Android logs and debugging
  * Adds the ability to export logs from the UI and persists debug logs through app restarts.
* feat: android .torrent file association
* feat: custom tracker list
  * You can now remove default trackers or add additional trackers to the custom tracker list in the client settings.
* feat: reannounce
  * You can now manually attempt to reconnect to trackers using the reannounce button under the dropdown for each torrent.
* feat: auto scrape toggle
  * You can now disable auto-scraping of extension results for up-to-date peer data in the extension settings. Scraping can often be slow, and sometimes it isn't always needed.
  * A manual scrape button has been added to the torrent menu to allow for manual scraping as needed.
* fix: invalid relative url when adding extensions
  * Fixes weird behavior where fetching an extensions source sometimes returns stub modules instead of the full implementation.
* fix: storage permissions on older android devices
  * Fixes storage permission issues with older Android devices when using an external download location.
  * Users will now be prompted when selecting a download location to allow storage permissions.
* fix: android stuck updater edge case
  * Fixes a potential issue where the update prompt would remain locked when canceling the apk update.
* fix: modal escape key with stacked modals
  * Fixed escape key not closing open modals.
  * Added a check to only close the topmost modal when stacked.
  * Changed escape to first escape text inputs, second escape closes the modal.
* fix: multi-part movie and special episodes
  * The episode list now better handles series that split up movies or specials into multiple episodes for streaming release. E.g. Love is War.
* fix: incorrectly listing zero episodes
  * Fixes and edge case where AniList randomly lists a zero episode under their streaming episode list, despite having a separate dedicated entry.
* fix: incorrect torrent results for zero episode series
  * Zero episode series now properly returns the expected results for the episode that was queried.
* fix: dub batch delays
  * Dub batches that are delayed now properly show in the episode list with the proper dates.
* fix: negative episode number results
  * Fixes negative episode numbers by returning a positive result.
  * Fixes negative episode numbers (failed result) falsely being marked as a successful result.
* fix: android safe area padding on search and w2g pages
* fix: android image search preview
* fix: duplicate terms on torrent card
* fix: completed and repeating card color in file manager and notifications.
* fix: resolving series with hyphens
* fix: dub aired count with zero episodes
* fix: oversized episode list card
* fix: prefer dub in schedule feed
* chore: rework episodes by air date
  * Fixes issues getting results from extensions during an AniList outage.
  * Fixes getting existing torrents through extension results while offline or during an AniList outage.
  * Implements fallbacks for episode air date for single episodes.
* chore: improve update experience with progress indication
  * Added a visual progress bar to the update button and informative toasts to keep users informed during the download and installation process.
* chore: improve and simplify changelog
  * Changelog is now properly sanitized rather than only handling certain cases. API calls to get the changelog have been deduplicated and simplified.
* chore: properly sanitize synopsis
  * Fixes issues with certain characters not being displayed, and now supports html tags.
* chore: improve modal navigation and refactor
  * Improves modal handling, making navigation less janky.
  * Adds navigation history support for all previously missing modals.
* chore: episode card scaling on small screens
  * Episode cards will now shrink slightly, allowing them to be centered properly on small screens.
* chore: add confirmations
  * Changes dangerous buttons that permanently erase data to have a confirmation to ensure you want to perform that action.
* chore: update minimize modal
  * Updates the minimize prompt to use the new custom soft modal.
* chore: improve example extension
  * Redesigned the example extension as a functional reference implementation for developers.
  * You can test this extension locally via direct path to the index.json or hosted via `gh:RockinChaos/Shiru/extensions`.
* chore: hide watch prompt in image search
* chore: debounce complex search inputs
* chore: allow options for current torrent
* chore: tweak mappings cache duration
* chore: add raw term
* chore: update deps
* chore: refactor
</details>

<details>
<summary><strong>Upstream release v6.4.8</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.4.8](https://github.com/RockinChaos/Shiru/releases/tag/v6.4.8)

### Notes
* fix: recover from IndexedDB corruption
  * Fixes an issue where the app won't start if the cache is corrupted.
  * Separates database transactions to reduce the chances of data getting corrupted during writes.
* fix: id filtering in user list search
  * Ensures that id arrays are filtered for valid values before being used in search filters. Prevents empty or invalid ids from affecting search results and improves robustness of the anime filtering logic.
* fix: stop infinite skeletons when no extensions
  * Fixes an issue where skeleton cards would render indefinitely when no extensions were found, causing the query to appear stuck.
* fix: correct myanimelist dates
  * Adjusts start and completed dates to ensure the timeline is valid on MyAnimeList, preventing entries where the completed date would be earlier than the start date.
* fix: missing banner images
  * Fixes banner images vanishing after navigating to series that do not have banner images.
* fix: scroll position jumping when marking notifications as read
* fix: losing miniplayer when navigating
* fix: logging stack traces in electron
* fix: null/undefined checks
* chore: update deps
</details>
<!-- LATEST-VERSION-END -->