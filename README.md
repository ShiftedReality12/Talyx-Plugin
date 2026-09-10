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

Prints `TALYX_PLUGIN_OK` and names the environment it is running in.

## Skills

| Skill | What it does |
|---|---|
| `talyx-ping` | Confirms the plugin is installed and reports which environment mounted it |
| `esdp-agent-builder` | Turns a knowledge base and team roster into ESDP v1.0 agent specs |

## Supported hosts

One `skills/` tree serves every host below. Each host reads its own manifest folder.

| Host | Manifest | Verified |
|---|---|---|
| Claude Code | `.claude-plugin/` | yes — install, run, update |
| Claude Cowork | `.claude-plugin/` | yes — private repo sync |
| Claude Chat | `.claude-plugin/` | yes |
| ChatGPT / Codex | `.codex-plugin/` | manifest written, not yet installed |
| Cursor | `.cursor-plugin/` | manifest written, not yet installed |
| Grok | `.grok-plugin/` | manifest written, not yet installed |
| Kimi | `.kimi-plugin/` | manifest written, not yet installed |
| Devin | `.devin-plugin/` | manifest written, not yet installed |
| OMP | `.omp-plugin/` | manifest written, not yet installed |

**Perplexity works differently.** It has no plugin manifest and no marketplace — skills
are uploaded one at a time as ZIP bundles, each holding exactly one top-level folder
with one `SKILL.md`. Those bundles are generated separately.

## Manifests are generated

Every manifest in this repo is produced from one source file by a build script kept
outside this repository. **Do not edit a manifest by hand** — the next build overwrites it.
Change the source and regenerate.

## Notes

No MCP servers, no hooks, no sub-agents, no bundled executables, no network calls.
Skills are plain markdown, read from the plugin cache. Nothing is written into your projects.

Skills read only inside their own directory and never above it, because plugin layouts
differ by host.
