#!/usr/bin/env python3
import json
import re
import sys

# Usage: python3 resolve_asset.py <DEB_ASSET_REGEX> <DEB_ARCH_REGEX> <DEB_ASSET_FALLBACKS>
# Stdin: release.json content

if len(sys.argv) < 4:
    print("Usage: resolve_asset.py <asset_regex> <arch_regex> <fallbacks>", file=sys.stderr)
    sys.exit(1)

asset_regex_str = sys.argv[1]
arch_regex_str = sys.argv[2]
fallbacks_str = sys.argv[3]

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

tag = data.get("tag_name") or ""
asset_regex = re.compile(asset_regex_str)
arch_regex = re.compile(arch_regex_str)
fallbacks = [f.strip() for f in fallbacks_str.split(",") if f.strip()]

assets = data.get("assets") or []
match = None

# Priority 1: Matches both asset regex (e.g., .deb) AND architecture regex
for asset in assets:
    name = asset.get("name", "")
    url = asset.get("browser_download_url", "")
    if not asset_regex.search(name):
        continue
    if arch_regex.search(name):
        match = (name, url)
        break

# Priority 2: Matches asset regex (any arch) if no specific arch match found
if match is None:
    for asset in assets:
        name = asset.get("name", "")
        url = asset.get("browser_download_url", "")
        if asset_regex.search(name):
            match = (name, url)
            break

# Priority 3: Fallback keywords check
if match is None and fallbacks:
    for asset in assets:
        name = asset.get("name", "")
        url = asset.get("browser_download_url", "")
        if not asset_regex.search(name):
            continue
        lower = name.lower()
        if any(f in lower for f in fallbacks):
            match = (name, url)
            break

if not tag or match is None:
    sys.exit(1)

print(f"{tag}|{match[0]}|{match[1]}")
