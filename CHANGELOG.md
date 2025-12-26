# Changelog

## Project notes
This repository packages the official Shiru `.deb` releases into Flatpak for convenience.
It does not modify upstream source code.

## Upstream release v6.4.7
Custom message: Repackaged for Flatpak with automated caching and version-aware updates.

Upstream notes:
- feat: add window restore button to tray menu
  - Adds a "Restore" option to the tray context menu that resets the window to its default size and centers it on the primary display.
  - This helps users recover from off-screen or incorrectly sized windows caused by display configuration changes or multi-monitor setups.
- fix: auto-recover tray icon when destroyed
  - Prevents crashes when the tray icon is accidentally destroyed by users.
  - The app now automatically detects when the tray is missing or destroyed and recreates it.
- fix: centralize and dedupe media requests
  - Fixes a rare edge case that would result in the requested media being missing from the cache.
  - If the requested media is missing from the cache, an attempt will now be made to fetch it in most cases.
- fix: separate notch from system bar detection
  - Patches capacitor-plugin-safe-area to expose display cutout insets separately from system UI insets.
- fix: miniplayer position on settings page with active overlay
- fix: batches incorrectly displayed as episode 0
- fix: settings padding on Android
- fix: episode number validation
- chore: update deps
