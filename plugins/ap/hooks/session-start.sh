#!/usr/bin/env bash
# Local sessions already load AP from ~/.claude/CLAUDE.md and apmemory/,
# so only speak up where that memory is absent (cloud VMs).
if [ -z "${CLAUDE_CODE_REMOTE:-}" ] && [ -d "$HOME/Desktop/dev/apmemory" ]; then
  exit 0
fi

cat "${CLAUDE_PLUGIN_ROOT}/hooks/identity.md"
echo
echo "_(ap-plugin: loaded; CLAUDE_CODE_REMOTE=${CLAUDE_CODE_REMOTE:-unset})_"
exit 0
