#!/usr/bin/env bash
# Paste into claude.ai/code → environment → Setup script.
# Installs AP into the cloud VM's own ~/.claude so every session, in any repo,
# starts as AP: identity as user-level CLAUDE.md, custom skills as user skills.
# The VM's proxy allows raw.githubusercontent.com but blocks github.com,
# codeload and api.github.com, so files are fetched one by one from a manifest.
set -u
RAW="https://raw.githubusercontent.com/Aphrosidiac/ap-plugin/main"
manifest="$(curl -fsSL -m 20 --retry 3 --retry-all-errors "$RAW/manifest.txt")" || { echo "AP install skipped: no manifest" >&2; exit 0; }
ok=0; fail=0
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in
    hooks/identity.md) dest="$HOME/.claude/CLAUDE.md" ;;
    skills/*) dest="$HOME/.claude/$f" ;;
    *) continue ;;
  esac
  mkdir -p "$(dirname "$dest")"
  if curl -fsSL -m 20 --retry 3 --retry-all-errors "$RAW/plugins/ap/$f" -o "$dest"; then ok=$((ok+1)); else fail=$((fail+1)); fi
done <<< "$manifest"
echo "AP installed: $ok files, $fail failed"
exit 0
