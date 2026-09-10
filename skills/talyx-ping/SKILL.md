---
name: talyx-ping
description: Confirm the Talyx plugin is installed and report which environment it is running in. Use when checking the plugin loaded, verifying a fresh install, or troubleshooting where skills are mounted.
---

# Talyx Ping

**Outcome:** the user sees that the Talyx plugin is loaded, which environment mounted it, and where its files live.

**Done:** the report below is printed. Nothing is written to disk and nothing is installed.

## Rule this skill obeys

Read only inside this skill's own directory. Never read a path above it — plugin
layouts differ by environment and a parent path that exists in one is absent in
another. Report what is observable; never infer a value you could not read.

## Steps

1. Determine the absolute directory this `SKILL.md` was loaded from.

2. Name the environment by matching that path against the table below. If none match,
   report `unrecognized layout` and print the path — do not guess.

   | Path contains | Environment |
   |---|---|
   | `/plugins/cache/` | Claude Code |
   | `/plugins/synced/` | Cowork |
   | `/mnt/skills/plugins/` | Claude Chat |

3. List the other Talyx skills visible alongside this one. The sibling location
   depends on the layout: in Claude Code and Cowork they are directories beside this
   one; in Chat they are separate top-level entries named `talyx-skills:<skill>`.
   If siblings cannot be listed, say so rather than assuming.

4. Print exactly this line last, unchanged:

```
TALYX_PLUGIN_OK
```

## Report shape

```
Talyx plugin — loaded
Environment: <Claude Code | Cowork | Claude Chat | unrecognized layout>
Path:        <absolute directory>
Skills:      <comma-separated list, or "could not enumerate">
TALYX_PLUGIN_OK
```

Keep the whole response under ten lines. This skill exists to confirm the install
and identify the environment, nothing more.
