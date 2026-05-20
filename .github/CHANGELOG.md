
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
<summary><strong>Upstream release v6.6.1-beta.4</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.6.1-beta.4](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.4)

### Notes
* fix: Android safe area insets on older webview
* fix: Android status transition
* fix: navigation bar border
* chore: exit fullscreen before navigating on Android
* chore: improve Android landscape visual
* chore: always log errors
* chore: update deps
</details>

<details>
<summary><strong>Upstream release v6.6.1-beta.3</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.6.1-beta.3](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.3)

### Notes
* fix: WebTorrent debug on Android
* chore: improve debugging on startup
</details>

<details>
<summary><strong>Upstream release v6.6.1-beta.2</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.6.1-beta.2](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.2)

### Notes
* fix: improve w2g peer discovery and session stability (#148)
* fix: episode list race conditions
* chore: faster offline detection
  * Intercept all fetch requests to detect outages immediately, abort in-flight requests when offline, and ping on startup to catch offline state before any requests are made.
* chore: improve notification card images
* chore: reduce ambiguous event listeners
* chore: update deps
</details>

<details>
<summary><strong>Upstream release v6.6.1-beta.1</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.6.1-beta.1](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.1-beta.1)

### Notes
* chore: block local network access in android fetch proxy
  * Extensions on Android that require the fetch proxy to reach external sources are now prevented from accessing private or local network addresses, stripping sensitive request options.
* chore: cache pending notifications
  * Fixes a bug where pending notifications were lost if the app was closed before they were sent.
* chore: improve notifications refresh
</details>

<details>
<summary><strong>Upstream release v6.6.0</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.6.0](https://github.com/RockinChaos/Shiru/releases/tag/v6.6.0)

### Notes
* feat: offline progress syncing
    * Changes to your list (e.g. progress and favourite changes) will now be tracked while offline and sync to AniList/MyAnimeList when the connection is restored.
    * Fixes a race condition where changes to your list during a user lists fetch could become stale for very large user lists.
    * User lists are now automatically fetched when the network or api comes back online.
* feat: player title position toggle ([#134](https://github.com/RockinChaos/Shiru/pull/134))
    * Adds a toggle to the player settings to change the title overlay location from the top left to the bottom left.
* feat: spoiler control settings
    * Adds a configurable spoiler control system that hides episode and series content based on watch progress. Users can choose from five protection levels (Minimal, Moderate, Strict, Hermit) and define which list status types the control applies to.
    * This is set to off by default, which will result in all episode cards showing their images regardless of watch progress. You can set it to Minimal and add your preferred list statuses to return to the previous spoiler behavior.
* feat: video cover toggle
    * Adds a toggle in the player dropdown to enable or disable filling the video to the full width.
    * The toggle and its keybind now persist across restarts.
* feat: respect extension enabled state in worker lifecycle
    * Extensions that are disabled no longer load or validate their workers on startup or network recovery. Toggling an extension off terminates its worker immediately, and toggling it on loads and validates it on demand.
* feat: extension custom settings
    * Extensions can now declare custom settings in their manifest. Values are persisted alongside the enabled state and passed to the worker on load and on change.
* feat: more extension options
    * Now directly passes the season, beforeSeason, afterSeason, absoluteEpisode, beforeEpisode, and afterEpisode values.
* feat: FileManager plugin
    * Replaced the WebView-based NativeBridge with a single unified Capacitor plugin handling all files access permission and folder picking.
* feat: separate android debug/release app variant
* fix: back/forward state after modal navigation
    * Fixed the forward button incorrectly graying out after pressing the back button to reopen a modal.
    * Fixed navigating back twice after closing a modal, returning to the wrong page instead of the modal.
* fix: visible progress in anime details
    * Fixes the indicated watch progress when audio labels are enabled, not reactively updating when changing the progress via the list editor.
* fix: android single-button notification activation
* fix: hiding android status bar
    * Switches to using capacitors new built-in StatusBars plugin.
    * Fixes status bar overlaying on older Android devices.
* fix: continue watching preferred dubs
    * Fixes series not properly hiding when prefer dubs is set to true from the continue watching section due to the release being a multi-header.
* fix: watch together playback
    * Playback is now slightly more stable.
    * The lobby host now controls the loaded torrent for all peers.
    * Peers are rejected on version mismatch with a toast indicating whether the host or connecting peer needs updating. Versioning allows future protocol changes without breaking existing sessions.
* fix: prevent status bar transition on orientation change
    * Disabled the status bar transition during orientation changes on Android to prevent the bar from slowly resizing when rotating the device.
* fix: prevent list mutation race conditions
    * Entry updates and deletions are now chained to prevent race conditions and ensure errors are surfaced correctly.
* fix: instant progress updates
    * Episode progress in anime details now updates immediately after watching, instead of waiting for the user list to finish refreshing.
* fix: throttle outage checking
* fix: handling episode range
    * Fixes episode card batches showing the proper episode range.
* fix: resolving Hikuidori
    * Fixes resolving Hikuidori when release groups use the MyAnimeList titles.
* fix: webpack-dev-server connection
* fix: search page preview cards on small screens
* fix: updating source repositories
* chore: improve android splash screen and colors
    * The transition when starting the app is now a lot smoother and implements proper theme colors.
* chore: remove custom safe area insets
    * Capacitor v8 introduces proper inset handling natively.
* chore: remove custom keyboard scroll-into-view
    * Capacitor v8 now handles this natively, utilizing proper inset padding.
* chore(temp): enable watch together toggle
    * Adds a toggle to enable Watch Together in the app settings, which will be disabled by default.
    * This is a temporary setting while Watch Together is in an experimental state.
* chore: improve resolving series while offline
    * RSS feeds will now attempt to resolve while the AniList API is down or if you are offline.
* chore: separate network debug
    * Adds "Network" as a debug option.
* chore: rework notifications modal
    * Improves notification reliability and fixes a bug where watched episodes were not always being marked as read correctly.
* chore: scale audio labels with card size
    * Audio labels are now scaled down proportionally when the card shrinks below its natural size, preventing labels from looking oversized on smaller cards.
* chore: disable extensions by default
    * Adding new extension sources will no longer automatically enable the extensions.
* chore: improve episode skeleton card
* chore: clamp external player duration
* chore: keep highest accuracy extension results
* chore: enforce extension type
* chore: increase the number of displayed season years
* chore: remove ambiguous IPC usage
* chore: improve protocol handling
* chore: Android ui tweaks
* chore: bump to webtorrent v2.8.7
* chore: bump to electron v39.8.7
* chore: bump to capacitor v8.3.1
* chore: update deps
* chore: refactor
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.8</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.8](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.8)

### Notes
* feat: more extension options
  * Now directly passes the season, beforeSeason, afterSeason, absoluteEpisode, beforeEpisode, and afterEpisode values.
* chore: rework notifications modal
  * Improves notification reliability and fixes a bug where watched episodes were not always being marked as read correctly.
* chore: scale audio labels with card size
  * Audio labels are now scaled down proportionally when the card shrinks below its natural size, preventing labels from looking oversized on smaller cards.
* chore: update deps
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.7</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.7](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.7)

### Notes
* feat: multiselect extension setting
* fix: search page preview cards on small screens
* fix: network throttle
* chore: disable extensions by default
  * Adding new extension sources will no longer automatically enable the extensions.
* chore: improve episode skeleton card
* chore: clamp external player duration
* chore: keep highest accuracy results
* chore: enforce extension type
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.6</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.6](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.6)

### Notes
* feat: extension custom settings
  * Extensions can now declare custom settings in their manifest. Values are persisted alongside the enabled state and passed to the worker on load and on change.
* feat: respect extension enabled state in worker lifecycle
  * Extensions that are disabled no longer load or validate their workers on startup or network recovery. Toggling an extension off terminates its worker immediately, and toggling it on loads and validates it on demand.
* fix: infinitely awaiting network check
* fix: preview card spoilers
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.5</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.5](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.5)

### Notes
* feat: spoiler control settings
  * Adds a configurable spoiler control system that hides episode and series content based on watch progress. Users can choose from five protection levels (Minimal, Moderate, Strict, Hermit) and define which list status types the control applies to.
  * This is set to off by default, which will result in all episode cards showing their images regardless of watch progress. You can set it to Minimal and add your preferred list statuses to return to the previous behavior.
* feat: video cover toggle
  * Adds a toggle in the player dropdown to enable or disable filling the video to the full width.
  * The toggle and its keybind now persist across restarts.
* fix: prevent list mutation race conditions
  * Entry updates and deletions are now chained to prevent race conditions and ensure errors are surfaced correctly.
* chore: increase the number of displayed season years
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.3</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.3](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.3)

### Notes
* chore: remove ambiguous IPC usage
* chore: improve protocol handling
* chore: update deps
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.2</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.2](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.2)

### Notes
* feat: separate android debug/release app variant
* feat: FileManager plugin
  * Replaced the WebView-based NativeBridge with a single unified Capacitor plugin handling all files access permission and folder picking.
* fix: android single-button notification activation
* fix: hiding android status bar
  * Switches to using capacitors new built-in StatusBars plugin.
  * Fixes status bar overlaying on older Android devices.
* fix: continue watching preferred dubs
  * Fixes series not properly hiding when prefer dubs is set to true from the continue watching section due to the release being a multi-header.
* chore: improve android splash screen and colors
  * The transition when starting the app is now a lot smoother and implements proper theme colors.
* chore: remove custom safe area insets
  * Capacitor v8 introduces proper inset handling natively.
* chore: remove custom keyboard scroll-into-view
  * Capacitor v8 now handles this natively, utilizing proper inset padding.
* chore: bump to electron v39.8.7
* chore: bump to capacitor v8.3.1
* chore: update deps
</details>

<details>
<summary><strong>Upstream release v6.5.3-beta.1</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.3-beta.1](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.1)

### Notes
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
</details>

<details>
<summary><strong>Upstream release v6.5.2</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.2](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.2)

### Notes
* fix: unable to scroll in file manager
  * Also fixes scrolling dropdowns on the player page.
* fix: torrent card regex
  * Titles for certain series were not being properly restored after cleaning the file name.
* fix: incorrect volume scroll capture
* fix: play/pause jitter
* chore: improve wheel volume control
  * Moves volume boost guard from 150% to 100%.
  * Volume now snaps to 100% before triggering the volume boost guard.
  * Volume boost guard is now visually indicated with a color change until the guard is passed.
* chore: improve search page
  * Improves infinite scroll visual and fixes potential edge cases where infinite scroll would get stuck.
* chore: improve card scaling
* chore: general cross-platform ui improvements
* chore: stats re-render
* chore: update deps
</details>

<details>
<summary><strong>Upstream release v6.5.1</strong></summary>

- **Author:** @github-actions[bot]
- **Source:** [v6.5.1](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.1)

### Notes
* feat: nightly build update channel
  * Adds an update channels setting to the app settings to allow switching between Stable and Nightly release channels with appropriate warnings for pre-release builds.
* feat: auto-hide miniplayer
  * The miniplayer will now automatically be shelved when playback is paused. This can be disabled in the player settings to instead allow for manual shelving.
  * Fixed miniplayer jumping when being repositioned.
* feat: subtitle delay keybinds (#127)
  * Adds keybinds to adjust subtitle delay: `,` / `Shift+`, (−0.1s / −1.0s) and `.` / `Shift+`. (+0.1s / +1.0s).
* feat: wheel volume control (#128)
  * Adds wheel volume control when hovering over the miniplayer and while on the player page.
* fix: zero episode correction
  * Fixes requesting the incorrect episode in the torrent modal when using Next/Previous buttons, as well as the Watch Now/Continue Watching buttons.
  * Fixes incorrectly showing an unwatched episode as completed on the seekbar.
* fix: showing dubs in continue watching
  * Fixes an edge case where preferred dubs weren't hiding series in continue watching after completing the latest episode due to the next week's episode being a double-header release.
* fix: incorrect dub dates in episode list
  * Fixes an edge case where dub dates were incorrect when the next week's episode is a double-header.
* fix: show unseeded results during torrent search
  * Unseeded results were incorrectly being hidden despite some extensions resolving faster than others.
* fix: pause on external player
  * Properly resets the current time and pauses the playback when manually launching the external player.
* fix: dragging keybinds
  * Fixes not being able to drag-and-drop keybinds to change the set key.
  * Implements a patch to fix responsiveness and webpack warnings.
* fix: trailer button vanishing during navigation
* fix: incorrect dub prediction date
* fix: show movie not episode
* fix: enable webSecurity (#124)
* chore: invalidate cached stub module code
  * If the cached code for an extension is detected to contain a stub-only implementation, an attempt will automatically be made to fetch the latest extension code before failing.
* chore: add extension error cards
  * If an extension finds no results or has a severe error, a respective warning or error card will be shown for that extension at the bottom of the results list, showing why the lookup failed.
* chore: modernize seekbar
  * Fixes progress desync from thumb.
* chore: improve volume keybinds
  * Volume up/down/scrolling keybinds will automatically unmute playback.
  * Volume up and down keybinds now flash the volume percentage on screen.
* chore: improve torrent card regex
  * Improves the cleaning of the file name displayed on torrent cards.
  * Fixes incorrect RAW term detection.
  * Adds Uncensored term.
* chore: add more extension options
  * Adds a deprecation option to mark the extension as no longer maintained, or the extension source has been removed.
  * Adds support for some markdown and html tags in the extension description.
  * Exposes anitomyscript for extensions to utilize. This will vastly help with plain text searches, so it's recommended to use this.
  * Adds more options for result queries; the media entry, mappings data, tvdb ids, imdb id, and mvdb id. This additional data will vastly help in improving search accuracy.
  * Fixed incorrectly passing modified titles instead of both the original and the modified titles.
* chore: re-render subtitles on delay update
* chore: cache and reuse manually scraped peer counts
* chore: update deps
</details>

<details>
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