# Shiru Flatpak v6.4.8

This release packages upstream **RockinChaos/Shiru v6.4.8**.

## Upstream Details
- **Version:** v6.4.8
- **Author:** @github-actions[bot]
- **Original Release:** https://github.com/RockinChaos/Shiru/releases/tag/v6.4.8

## Upstream Changelog
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
