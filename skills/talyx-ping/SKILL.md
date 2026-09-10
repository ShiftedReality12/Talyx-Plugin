---
name: talyx-ping
description: Confirm the Talyx plugin is installed and report which environment it is running in. Use when checking the plugin loaded, verifying a fresh install, or troubleshooting where skills are mounted.
---

# Talyx Ping

**Outcome:** the user sees that the Talyx plugin is loaded and which environment mounted it.

**Done:** the four lines below are printed. Nothing is read outside this skill's own
directory, nothing is written, nothing is installed.

## Steps

1. Determine the absolute directory this `SKILL.md` was loaded from.

2. Name the environment by checking that path against this table **in order**, first
   match wins. Several hosts use `plugins/cache`, so the earlier rows are what
   separate them.

   | Path contains | Environment |
   |---|---|
   | `/.codex/` | ChatGPT / Codex |
   | `/.cursor/` | Cursor |
   | `/plugins/synced/` | Claude Cowork |
   | `/mnt/skills/plugins/` | Claude Chat |
   | `/.claude/` | Claude Code |

   No match: report `unrecognized layout` and print the path. Do not guess.

3. Print exactly this, and nothing else:

```
Talyx plugin — loaded
Environment: <name from the table>
Path:        <absolute directory>
TALYX_PLUGIN_OK
```

Do not list other skills, and do not look for a manifest. Both require reading above
this directory, which is not portable across hosts.
