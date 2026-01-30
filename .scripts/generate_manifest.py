#!/usr/bin/env python3
import sys

# Usage: python3 generate_manifest.py <source_manifest> <target_manifest> <metadata_file_path>

if len(sys.argv) < 4:
    print("Usage: generate_manifest.py <source> <target> <metadata_file>", file=sys.stderr)
    sys.exit(1)

source = sys.argv[1]
target = sys.argv[2]
metadata_file = sys.argv[3]

with open(source, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

out = []
inserted = False
for line in lines:
    if line.strip().startswith("metadata:"):
        continue
    out.append(line)
    if not inserted and line.strip().startswith("command:"):
        out.append(f"metadata: {metadata_file}")
        inserted = True

with open(target, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
