#!/usr/bin/env python3
import json
import os
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path

# Configuration
UPSTREAM_REPO = "RockinChaos/Shiru"
UPSTREAM_VERSION_FILE = Path("UPSTREAM_VERSION")
CHANGELOG_FILE = Path(".github/CHANGELOG.md")
RELEASE_NOTES_FILE = Path("RELEASE_NOTES.md")
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", "github_output.txt")

MARKER_START = "<!-- LATEST-VERSION-START -->"
MARKER_END = "<!-- LATEST-VERSION-END -->"

def get_latest_release():
    url = f"https://api.github.com/repos/{UPSTREAM_REPO}/releases/latest"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching release: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # 1. Fetch latest upstream release
    print(f"Fetching latest release for {UPSTREAM_REPO}...")
    release = get_latest_release()
    latest_tag = release.get("tag_name", "").strip()
    author = release.get("author", {}).get("login", "unknown")
    html_url = release.get("html_url", "")
    body = release.get("body", "") or "(no description)"
    
    if not latest_tag:
        print("Error: No tag found in release data.", file=sys.stderr)
        sys.exit(1)

    print(f"Latest upstream version: {latest_tag}")

    # 2. Check local version
    current_version = ""
    if UPSTREAM_VERSION_FILE.exists():
        current_version = UPSTREAM_VERSION_FILE.read_text("utf-8").strip()
    
    print(f"Current local version: {current_version}")

    # 3. Determine if update is needed
    force_update = os.environ.get("FORCE", "false").lower() == "true"
    should_build = force_update or (latest_tag != current_version)

    if not should_build:
        print("Versions match. No update needed.")
        with open(GITHUB_OUTPUT, "a") as f:
            f.write(f"should_build=false\n")
            f.write(f"tag={latest_tag}\n")
        return

    print("Update detected or forced.")

    # 4. Update UPSTREAM_VERSION file
    UPSTREAM_VERSION_FILE.write_text(latest_tag + "\n", encoding="utf-8")
    print(f"Updated {UPSTREAM_VERSION_FILE} to {latest_tag}")

    # 5. Update CHANGELOG.md with markers logic (Strict replacement inside markers)
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

    # 6. Generate RELEASE_NOTES.md for GitHub Release
    release_notes_content = f"""# Shiru Flatpak {latest_tag}

This release packages upstream **{UPSTREAM_REPO} {latest_tag}**.

## Upstream Details
- **Version:** {latest_tag}
- **Author:** @{author}
- **Original Release:** {html_url}

## Upstream Changelog
{body}
"""
    RELEASE_NOTES_FILE.write_text(release_notes_content, encoding="utf-8")
    print(f"Generated {RELEASE_NOTES_FILE}")

    # 7. Set outputs
    with open(GITHUB_OUTPUT, "a") as f:
        f.write("should_build=true\n")
        f.write(f"tag={latest_tag}\n")

if __name__ == "__main__":
    main()
