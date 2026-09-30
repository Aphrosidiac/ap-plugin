# ap-plugin

AP for Claude Code **cloud sessions**. Cloud VMs don't read `~/.claude/` or
APMemory from Fakhrul's Mac, so this repo carries the part of AP that has to
travel:

- `plugins/ap/hooks/identity.md`: identity, hard rules, cloud limits, and the
  handoff block.
- `plugins/ap/skills/`: copies of reference-clone, engineering-atlas, geo-aeo
  and visual-report.

No credentials, session logs, client names or project states live here. The
repo is public so a cloud VM can fetch it.

## How it reaches a cloud session

Cloud sessions ignore plugins from a repo's `.claude/settings.json` and from
the claude.ai account (verified 2026-09-30; only org-managed settings install
plugins there). What does run in every cloud VM is the **environment setup
script**. [`cloud-setup.sh`](cloud-setup.sh) downloads this repo and writes:

- `identity.md` → `~/.claude/CLAUDE.md` (user-level memory in the VM)
- `skills/*` → `~/.claude/skills/`

Paste the script into claude.ai/code → your environment → Setup script. It
applies to every repo you open in cloud, and nothing is committed to the
project repos.

The plugin layout (`.claude-plugin/`, `hooks/hooks.json`) is kept so the same
repo can be installed as a plugin wherever plugins do load.

## Update

- Rules or identity: edit `plugins/ap/hooks/identity.md`, then commit and push.
- Skills: run `./sync-skills.sh` to copy them from `apmemory/skills` and
  `~/.claude/skills`, then commit and push.

The next cloud session picks up the change. Setup-script results are cached
for a while, so expect some lag.

## Round trip

Cloud session → pushes its branch and ends with an `## AP handoff` block →
locally, `git pull` or `claude --teleport`, then say `save` so AP files the
handoff into `apmemory/core/SESSION_LOG.md`.
