---
name: talyx-ping
description: Confirm the Talyx skills plugin is installed and running. Use when checking the plugin loaded, verifying setup, or troubleshooting a fresh install.
---

# Talyx Ping

**Outcome:** the user sees confirmation that the Talyx plugin is installed, which skills it carries, and where this skill is loaded from.

**Done:** the report below is printed. Nothing is written to disk and nothing is installed.

## Steps

1. Report the plugin name and version by reading the manifest at `../../plugin.json` relative to this file. If it cannot be read, say so plainly rather than guessing a version.

2. List the skills the plugin provides by naming the directories under `../` (this skill's parent `skills/` folder).

3. Report the absolute directory this `SKILL.md` was loaded from, so the install path is visible.

4. Print exactly this line last, unchanged:

```
TALYX_PLUGIN_OK
```

## Report shape

```
Talyx skills plugin — <name> v<version>
Loaded from: <absolute path>
Skills: <comma-separated list>
TALYX_PLUGIN_OK
```

Keep the whole response under ten lines. This skill exists to close the install loop, nothing more.
