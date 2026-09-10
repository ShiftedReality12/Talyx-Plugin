# Talyx Skills

Talyx skills, packaged so they load into your own AI environment in one step.

## Install

```
/plugin marketplace add ShiftedReality12/Talyx-Plugin
/plugin install talyx-skills@talyx
```

Start a **new chat** after installing — plugins do not activate mid-conversation.

### Turn on auto-update

Third-party marketplaces have auto-update **off by default**, so new versions will not
arrive on their own until you enable it. Do this once:

1. Run `/plugin`
2. Select **Marketplaces**
3. Choose **talyx**
4. Select **Enable auto-update**

After that, Claude refreshes the marketplace and updates the plugin in the background
shortly after each session starts, then prompts you to run `/reload-plugins`.

Without it, update by hand whenever you want the latest:

```
/plugin marketplace update talyx
/plugin update talyx-skills
```

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

One `skills/` tree serves every host below. Each reads its own manifest folder.

| Host | Manifest | Verified |
|---|---|---|
| Claude Code | `.claude-plugin/` | yes — install, run, update |
| Claude Cowork | `.claude-plugin/` | yes — private repo sync |
| Claude Chat | `.claude-plugin/` | yes |
| Grok Build | `.grok-plugin/` | yes — install, run, update |
| ChatGPT Work / Codex | `.codex-plugin/` | yes — install and run |
| ChatGPT chat | `.codex-plugin/` | **no** — needs public listing or a workspace admin import |
| Cursor | `.cursor-plugin/` | manifest written, not installed |
| Devin | `.devin-plugin/` | manifest written, not installed |

**Perplexity works differently.** No plugin manifest, no marketplace — skills are uploaded
one at a time under **Skills → + Create skill**, either as a bare `.md` or as a `.zip`
holding exactly one top-level folder with one `SKILL.md`. Bundles are generated separately
to `dist/perplexity/`.

## Manifests are generated

Every manifest in this repo is produced from one source file by a build script kept
outside this repository. **Do not edit a manifest by hand** — the next build overwrites it.
Change the source and regenerate.

## Notes

No MCP servers, no hooks, no sub-agents, no bundled executables, no network calls.
Skills are plain markdown, read from the plugin cache. Nothing is written into your projects.

Skills read only inside their own directory and never above it, because plugin layouts
differ by host.
