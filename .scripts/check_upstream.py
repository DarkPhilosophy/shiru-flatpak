#!/usr/bin/env python3
import json
import os
import sys
import re
import tempfile
import urllib.request
import urllib.error
from pathlib import Path

# Configuration
UPSTREAM_REPO = "RockinChaos/Shiru"
UPSTREAM_VERSION_FILE = Path("UPSTREAM_VERSION")
LOCAL_VERSION_FILE = Path("VERSION")  # Flatpak version tracking
CHANGELOG_FILE = Path(".github/CHANGELOG.md")
RELEASE_NOTES_FILE = Path("RELEASE_NOTES.md")
METAINFO_FILE = Path("com.github.rockinchaos.shiru.metainfo.xml")
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT")

# Allow pre-releases to be considered as latest (default: True for more frequent updates)
INCLUDE_PRERELEASES = os.environ.get("INCLUDE_PRERELEASES", "true").lower() == "true"

MARKER_START = "<!-- LATEST-VERSION-START -->"
MARKER_END = "<!-- LATEST-VERSION-END -->"

def get_output_path():
    if GITHUB_OUTPUT:
        return GITHUB_OUTPUT
    return os.path.join(tempfile.gettempdir(), "shiru-github-output.txt")

def get_latest_release(include_prereleases=True):
    if include_prereleases:
        # Use /releases endpoint to include pre-releases
        url = f"https://api.github.com/repos/{UPSTREAM_REPO}/releases"
        try:
            with urllib.request.urlopen(url) as response:
                releases = json.loads(response.read().decode())
                # Return the first release (most recent, including pre-releases)
                if releases:
                    return releases[0]
                return None
        except urllib.error.HTTPError as e:
            print(f"Error fetching releases: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Use /releases/latest endpoint for stable releases only
        url = f"https://api.github.com/repos/{UPSTREAM_REPO}/releases/latest"
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            print(f"Error fetching release: {e}", file=sys.stderr)
            sys.exit(1)

def is_valid_version(version_str):
    """Validate version string format (e.g., v6.5.3-beta.1)"""
    if not version_str:
        return False
    # Match version pattern: v{major}.{minor}.{patch}[-prerelease]
    return bool(re.match(r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$', version_str))

def normalize_version(version_str):
    """Normalize version for comparison: v6.5.3-beta.1 -> 6.5.3-beta.1"""
    return version_str.strip().lstrip('v')

def update_metainfo(version, date_str):
    if not METAINFO_FILE.exists():
        print(f"Warning: {METAINFO_FILE} not found. Skipping metainfo update.")
        return

    if not version or not date_str:
        print("Warning: Missing version/date for metainfo update. Skipping.")
        return

    content = METAINFO_FILE.read_text("utf-8")

    if f'version="{version}"' in content:
        print(f"Metainfo already contains version {version}")
        return

    new_release = f'    <release version="{version}" date="{date_str}" />'

    if "<releases>" in content:
        pattern = re.compile(r"(<releases>)", re.MULTILINE)
        if pattern.search(content):
            new_content = pattern.sub(f"\\1\n{new_release}", content, count=1)
            METAINFO_FILE.write_text(new_content, encoding="utf-8")
            print(f"Updated {METAINFO_FILE} with version {version}")
    else:
        print(f"Warning: <releases> tag not found in {METAINFO_FILE}")

def write_outputs(should_build, latest_tag, is_prerelease):
    output_path = get_output_path()
    mode = "a" if GITHUB_OUTPUT else "w"
    with open(output_path, mode, encoding="utf-8") as f:
        f.write(f"should_build={'true' if should_build else 'false'}\n")
        f.write(f"tag={latest_tag}\n")
        f.write(f"prerelease={str(is_prerelease).lower()}\n")

def compare_versions(v1, v2):
    """Compare two version strings. Returns: -1, 0, or 1"""
    def parse(v):
        # Remove 'v' prefix
        v = v.lstrip('v')
        # Split into base and prerelease
        parts = v.split('-', 1)
        base = parts[0].split('.')
        prerelease = parts[1] if len(parts) > 1 else ''
        return [int(x) for x in base], prerelease
    
    base1, pre1 = parse(v1)
    base2, pre2 = parse(v2)
    
    # Compare base version
    for i in range(max(len(base1), len(base2))):
        b1 = base1[i] if i < len(base1) else 0
        b2 = base2[i] if i < len(base2) else 0
        if b1 != b2:
            return -1 if b1 < b2 else 1
    
    # Compare prerelease: stable > prerelease
    if pre1 and not pre2:
        return 1
    if not pre1 and pre2:
        return -1
    if pre1 < pre2:
        return -1
    if pre1 > pre2:
        return 1
    
    return 0

def main():
    # 1. Fetch latest upstream release
    print(f"Fetching latest release for {UPSTREAM_REPO} (include_prereleases={INCLUDE_PRERELEASES})...")
    release = get_latest_release(include_prereleases=INCLUDE_PRERELEASES)
    latest_tag = release.get("tag_name", "").strip()
    is_prerelease = release.get("prerelease", False)
    author = release.get("author", {}).get("login", "unknown")
    html_url = release.get("html_url", "")
    body = release.get("body", "") or "(no description)"
    published_at = release.get("published_at", "")
    if "T" not in published_at:
        print("Error: Missing or invalid published_at in upstream release payload.", file=sys.stderr)
        sys.exit(1)
    date_str = published_at.split("T", 1)[0]
    
    if not latest_tag:
        print("Error: No tag found in release data.", file=sys.stderr)
        sys.exit(1)

    print(f"Latest upstream version: {latest_tag} (pre-release: {is_prerelease})")

    # 2. Check local upstream version
    current_upstream_version = ""
    if UPSTREAM_VERSION_FILE.exists():
        current_upstream_version = UPSTREAM_VERSION_FILE.read_text("utf-8").strip()
    
    print(f"Current upstream version: {current_upstream_version}")

    # 3. Check local flatpak version (from VERSION file)
    current_flatpak_version = ""
    if LOCAL_VERSION_FILE.exists():
        current_flatpak_version = LOCAL_VERSION_FILE.read_text("utf-8").strip()
    
    print(f"Current flatpak version: {current_flatpak_version}")

    # 4. Determine if update is needed (compare upstream versions)
    force_update = os.environ.get("FORCE", "false").lower() == "true"
    
    # Use proper version comparison
    version_changed = False
    if force_update:
        version_changed = True
    elif current_upstream_version and latest_tag:
        version_changed = compare_versions(latest_tag, current_upstream_version) != 0
    elif not current_upstream_version:
        version_changed = True
    
    should_build = version_changed

    if not should_build:
        print("Versions match. No update needed.")
        write_outputs(False, latest_tag, is_prerelease)
        return

    print("Update detected or forced.")

    # 5. Update UPSTREAM_VERSION file
    UPSTREAM_VERSION_FILE.write_text(latest_tag + "\n", encoding="utf-8")
    print(f"Updated {UPSTREAM_VERSION_FILE} to {latest_tag}")

    # 6. Update VERSION file to match upstream version exactly
    # Use full tag without "v" prefix - e.g., v6.5.3-beta.1 -> 6.5.3-beta.1
    # This ensures each beta/RC gets its own unique version
    flatpak_version = latest_tag.lstrip('v')
    
    LOCAL_VERSION_FILE.write_text(flatpak_version + "\n", encoding="utf-8")
    print(f"Updated {LOCAL_VERSION_FILE} to {flatpak_version} (exact upstream version)")

    update_metainfo(flatpak_version, date_str)

    # 7. Update CHANGELOG.md with markers logic (Strict replacement inside markers)
    new_entry_content = f"""<details open>
<summary><strong>Upstream release {latest_tag}</strong></summary>

- **Author:** @{author}
- **Source:** [{latest_tag}]({html_url})

### Notes
{body}
</details>"""

    current_changelog = ""
    if CHANGELOG_FILE.exists():
        current_changelog = CHANGELOG_FILE.read_text("utf-8")
    
    # Regex to find the block
    pattern = re.compile(f"({re.escape(MARKER_START)})(.*?)({re.escape(MARKER_END)})", re.DOTALL)
    match = pattern.search(current_changelog)
    
    if match:
        old_inner = match.group(2)
        
        # Advanced Logic:
        # We want to ensure that the CURRENT version is represented ONCE, at the top, open.
        # Any OLDER versions should be collapsed below.
        # Any DUPLICATE blocks of the CURRENT version (like the "bad data" one) should be REMOVED.
        
        # 1. Parse existing blocks
        # We split by <details (open or not)
        blocks = re.split(r"(?=<details)", old_inner)
        cleaned_history = []
        
        for block in blocks:
            if not block.strip(): continue
            
            # Check if this block is for the current version
            if f"Upstream release {latest_tag}" in block:
                # Skip it! We will add the fresh, correct one at the top.
                continue
                
            # Validation: Only keep blocks that look like valid release entries
            # This filters out garbage/test artifacts inside the markers
            if "Upstream release v" not in block:
                continue
            
            # If it's another version, ensure it's collapsed and keep it
            block = re.sub(r"<details\s+open>", "<details>", block)
            cleaned_history.append(block.strip())
            
        # 2. Reconstruct: New Entry + Cleaned History
        history_str = "\n\n".join(cleaned_history)
        if history_str:
            new_inner = f"\n{new_entry_content}\n\n{history_str}\n"
        else:
            new_inner = f"\n{new_entry_content}\n"
        
        # Replace content between markers
        final_changelog = (
            current_changelog[:match.start(2)] + 
            new_inner + 
            current_changelog[match.end(2):]
        )
        print("Updated existing marker block (with cleanup).")
    else:
        # Markers not found: Initialize them at the top (fallback)
        final_changelog = f"{MARKER_START}\n{new_entry_content}\n{MARKER_END}\n\n{current_changelog}"
        print("Markers not found; prepended new block.")

    if final_changelog != current_changelog:
        CHANGELOG_FILE.write_text(final_changelog, encoding="utf-8")
        print(f"Updated {CHANGELOG_FILE}")

    # 8. Generate RELEASE_NOTES.md for GitHub Release
    release_notes_content = f"""# Shiru Flatpak {latest_tag}

This release packages upstream **{UPSTREAM_REPO} {latest_tag}**.
"""
    # Add pre-release warning if applicable
    if is_prerelease:
        release_notes_content += """
> ⚠️ **This is a pre-release version.** It may contain experimental features or bugs.
"""

    release_notes_content += f"""
## Upstream Details
- **Version:** {latest_tag}
- **Author:** @{author}
- **Original Release:** [GitHub Release]({html_url})

## Upstream Changelog
{body}
"""
    RELEASE_NOTES_FILE.write_text(release_notes_content, encoding="utf-8")
    print(f"Generated {RELEASE_NOTES_FILE}")

    # 9. Set outputs
    write_outputs(True, latest_tag, is_prerelease)

if __name__ == "__main__":
    main()
