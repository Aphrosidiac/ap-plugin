#!/usr/bin/env bash
# Refresh the plugin's skill copies from their local sources of truth.
# Run after editing a skill, then commit and push.
set -euo pipefail
cd "$(dirname "$0")"
DEST=plugins/ap/skills
SOURCES=(
  "$HOME/Desktop/dev/apmemory/skills/reference-clone"
  "$HOME/Desktop/dev/apmemory/skills/engineering-atlas"
  "$HOME/.claude/skills/geo-aeo"
  "$HOME/.claude/skills/visual-report"
)
for src in "${SOURCES[@]}"; do
  rsync -aL --delete --exclude '__pycache__' --exclude '.DS_Store' "$src/" "$DEST/$(basename "$src")/"
  echo "synced $(basename "$src")"
done

# Cloud VMs can only reach raw.githubusercontent.com, so cloud-setup.sh
# fetches file by file from this list.
(cd plugins/ap && find hooks/identity.md skills -type f ! -name '.DS_Store' ! -path '*/__pycache__/*' | sort) > manifest.txt
echo "manifest: $(wc -l < manifest.txt | tr -d ' ') files"
