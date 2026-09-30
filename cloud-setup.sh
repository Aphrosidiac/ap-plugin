#!/usr/bin/env bash
# Paste into claude.ai/code → environment → Setup script.
# Installs AP into the cloud VM's own ~/.claude so every session, in any repo,
# starts as AP: identity as user-level CLAUDE.md, custom skills as user skills.
# Requires Aphrosidiac/ap-plugin to be public (the VM can only auth to the
# session's own repo).
set -u
AP_TARBALL="https://codeload.github.com/Aphrosidiac/ap-plugin/tar.gz/refs/heads/main"
tmp="$(mktemp -d)"
if curl -fsSL "$AP_TARBALL" | tar -xz -C "$tmp" --strip-components=1; then
  mkdir -p ~/.claude/skills
  cp "$tmp/plugins/ap/hooks/identity.md" ~/.claude/CLAUDE.md
  cp -R "$tmp/plugins/ap/skills/." ~/.claude/skills/
  echo "AP installed: $(ls ~/.claude/skills | tr '\n' ' ')"
else
  echo "AP install skipped: could not fetch ap-plugin" >&2
fi
rm -rf "$tmp"
