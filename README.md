# Talyx Skills

Talyx skills, packaged so they load into your own AI environment in one step.

## Install

```
/plugin marketplace add ShiftedReality12/Talyx-Plugin
/plugin install talyx-skills@talyx
```

Start a **new chat** after installing — plugins do not activate mid-conversation.

## Verify

```
/talyx-skills:talyx-ping
```

Prints `TALYX_PLUGIN_OK` when the plugin is loaded correctly.

## Skills

| Skill | What it does |
|---|---|
| `talyx-ping` | Confirms the plugin is installed and reports which environment mounted it |
| `esdp-agent-builder` | Turns a knowledge base and team roster into ESDP v1.0 agent specs |

## Notes

No MCP servers, no hooks, no bundled executables, no network calls. Skills are plain
markdown and are read from the plugin cache — nothing is written into your projects.
