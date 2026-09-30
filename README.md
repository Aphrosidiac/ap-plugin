# ap-plugin

AP for Claude Code **cloud sessions**. Cloud VMs don't read `~/.claude/` or
APMemory, so this plugin carries the part of AP that has to travel:

- `plugins/ap/hooks/identity.md`: identity, hard rules, cloud limits, and the
  handoff block. It's injected by a SessionStart hook, and only when APMemory
  isn't on disk, so local sessions (which already load AP) stay unchanged.
- `plugins/ap/skills/`: copies of reference-clone, engineering-atlas, geo-aeo
  and visual-report. They're invoked as `ap:<skill>`.

No credentials, session logs or project states live here.

## Opt a repo in

Commit `.claude/settings.json` in the repo:

```json
{
  "extraKnownMarketplaces": {
    "ap": { "source": { "source": "github", "repo": "Aphrosidiac/ap-plugin" } }
  },
  "enabledPlugins": { "ap@ap": true }
}
```

## Update

- Rules or identity: edit `plugins/ap/hooks/identity.md`, then commit and push.
- Skills: run `./sync-skills.sh` to copy them from `apmemory/skills` and
  `~/.claude/skills`, then commit and push.
- Bump `version` in `plugins/ap/.claude-plugin/plugin.json` whenever you push.

## Round trip

Cloud session → pushes its branch and ends with an `## AP handoff` block →
locally, `git pull` or `claude --teleport`, then say `save` so AP files the
handoff into `apmemory/core/SESSION_LOG.md`.
