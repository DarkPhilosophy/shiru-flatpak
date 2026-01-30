
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