# Shiru Flatpak v6.5.3-beta.2

This release packages upstream **RockinChaos/Shiru v6.5.3-beta.2**.

> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.

## Upstream Details
- **Version:** v6.5.3-beta.2
- **Author:** @github-actions[bot]
- **Original Release:** [GitHub Release](https://github.com/RockinChaos/Shiru/releases/tag/v6.5.3-beta.2)

## Upstream Changelog
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
