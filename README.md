# shiru-flatpak

Flatpak repackaging for the Shiru desktop app using the official upstream `.deb` releases.
This repo intentionally **does not** include Shiru source code.

## What this repo does
- Fetches the latest Shiru `.deb` from upstream releases.
- Extracts it and packages it into a Flatpak.
- Caches extracted files for fast rebuilds.
- Injects version metadata so the installed Flatpak reports the upstream version.

## Requirements
- `flatpak`
- `flatpak-builder`
- `curl`
- `python3`
- `ar`
- `tar`

## Quick start
```bash
./flatpak-build.sh --clean
```

### Force reinstall
```bash
./flatpak-build.sh --clean --force-install
```

### Force update (re-download + re-extract)
```bash
./flatpak-build.sh --clean --update
```

## How version checks work
- Latest upstream tag is read from GitHub releases.
- Installed Flatpak version is read from Flatpak metadata.
- If installed version matches the latest tag, the build is skipped (unless `--force-install` or `--update`).

## Cache behavior
- Cache root: `~/.cache/shiru-flatpak`
- Extracted files are cached per version and reused.
- `.deb` files are deleted after extraction to reduce IO.
- After a successful build, only the latest version is retained.

## Files in this repo
- `.flatpak-manifest.yaml` - Flatpak manifest
- `flatpak-build.sh` - build + update script
- `flatpak-build.conf` - configuration
- `com.github.rockinchaos.shiru.metainfo.xml` - metadata
- `VERSION` - last upstream version handled by this repo

## Upstream
- Shiru releases: https://github.com/RockinChaos/Shiru/releases

## License
See `LICENSE`.
