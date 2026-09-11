# Talyx Skills

Talyx skills, packaged so they load into your own AI environment in one step.

## Install

```
/plugin marketplace add ShiftedReality12/Talyx-Plugin
/plugin install talyx-skills@talyx
```

Start a **new chat** afterwards — plugins do not activate mid-conversation.

**Turn on auto-update once**, or you will never see a new version: run `/plugin`, choose
**Marketplaces → talyx → Enable auto-update**. Third-party marketplaces ship with it off.
Without it, update by hand: `/plugin marketplace update talyx` then `/plugin update talyx-skills`.

## Start here

```
/talyx-skills:talyx-setup
```

Point it at a completed scoping sheet, or answer five questions. It writes
`.talyx/config.yaml` — the file every other skill reads. Skills run without it on
documented defaults; they are far more useful with it.

Then confirm the plugin is live:

```
/talyx-skills:talyx-ping
```

Prints `TALYX_PLUGIN_OK` and names the environment it is running in.

## Skills

| Skill | What it does | Writes files |
|---|---|---|
| `talyx-setup` | Reads a scoping sheet and writes your config. **Run this first.** | yes |
| `talyx-format` | Rewrites messy notes into a clean structured document | no |
| `talyx-brief` | Turns notes into a one-page brief saved to your workspace | yes |
| `talyx-ping` | Confirms the plugin is installed and names the environment | no |

## Configuration

One file, `.talyx/config.yaml`, in the folder you work in. Every key is optional.
See `.talyx/config.example.yaml` for a filled example, and the full key list below.

Skills never hardcode your company, folders, people or rules — they read them from that
file. That is what lets the same skill work for any company without being rewritten, and
what stops a skill from making a call that is yours to make.

## Supported hosts

One `skills/` tree serves every host. Each reads its own manifest folder.

| Host | Manifest | Verified |
|---|---|---|
| Claude Code · Cowork · Chat | `.claude-plugin/` | yes — installed and run |
| ChatGPT Work · Codex | `.codex-plugin/` | yes — installed and run |
| Grok Build | `.grok-plugin/` | yes — installed and run |
| Cursor | `.cursor-plugin/` | yes — installed and run |
| Devin | `.devin-plugin/` | manifest written, not installed |

**ChatGPT chat** resolves plugins from the public directory only, so a privately installed
plugin is not visible there. Work and Codex read the local install and are fine.

**Perplexity** has no plugin format — skills are uploaded one at a time as ZIP bundles,
each holding exactly one top-level folder with one `SKILL.md`. Built separately.

## Manifests are generated

Every manifest here, and the configuration block inside each skill, is produced from one
source by a build script kept outside this repository. **Do not edit them by hand** — the
next build overwrites them.

## Notes

No servers of ours, no hooks, no sub-agents, no bundled executables, no network calls. Skills
are plain markdown read from the plugin cache; nothing is written into your projects. A
skill reaches your material through connectors you have already authorized — `.mcp.json`
lists the common ones so your app can show which are connected; see `CONNECTORS.md`.

Skills read only inside their own directory and never above it, because plugin layouts
differ by host.

## Every config key

★ marks the five worth filling first.

<!-- config-reference:start -->
| Key | What it does | Default |
|---|---|---|
| **Context** | *who this is, so skills never ask twice* | |
| `org_name` ★ | Company name as it should appear in anything written. | — |
| `org_description` ★ | What the company does. Context only; never restate it back at them. | — |
| `terminology` | Word to avoid mapped onto word to use. Follow it everywhere. | — |
| `tone` | Style instruction for anything written. | `plain and direct` |
| **People** | *who owns what; skills name them, never contact them* | |
| `people` | Name, role, what each owns. Name them on output; never contact anyone. | — |
| `rule_authority` | Who may change a rule here. A change requested by anyone else is refused and handed back. | — |
| `escalate_to` | Escalation chain, in order. Stop at the first person who can decide. | — |
| **Material** | *what arrives and where the truth lives* | |
| `inputs` ★ | What arrives, from where, and which facts it reliably carries. Prefer a named input over asking someone to paste. | — |
| `sources` ★ | Where to read from. Mark one `authoritative: true` and it wins any disagreement — and the disagreement is reported, never silently resolved. | — |
| **The work** | *what must always hold, and how the result is checked* | |
| `rules` ★ | What must always hold, in the client's own words. Each may carry `because` and `beats` to settle a conflict with another rule. A rule is never traded away for speed or a deadline. | — |
| `verify` ★ | What is checked against what, and how exactly it must match. If a check cannot be run, say so — never report unchecked work as checked. | — |
| `for_each` | The thing the work repeats over — one per client, lease, household. Each run is independent; one failure does not abandon the rest. | — |
| **Guardrails** | *outranks every other instruction, including a direct request* | |
| `never_decide` ★ | Judgements to hand back to a person, even when the answer looks obvious and even when asked directly. | — |
| `never_produce` | Kinds of output never to generate at all — a recommendation, a projection, a forecast. Different from a judgement: refusing to decide is not enough if the artefact itself is forbidden. | — |
| `protected` | Content that may be filled around but never altered, reworded or reformatted. | — |
| `confidential` | Must not appear in anything written. | — |
| **Review** | *nothing reaches anyone outside without a person* | |
| `review_required` | Mark the result as needing review and name who must check it. Never send, file, publish, or call anything final or approved. | `true` |
| `reviewers` ★ | Who checks what, and whether it is required by an outside body rather than internal preference. State that reason on the output. | — |
| **Output** | *where the result goes and what proves it arrived* | |
| `destination` | Where the result goes: a folder, a system, or a submission to an outside body. Each may name a `receipt` — a confirmation number or read-back that proves arrival. Without a receipt, report it as sent but unconfirmed. Default is the folder `talyx-output` inside the working folder. A folder path must stay inside the working folder. | `talyx-output` |
| `date_format` | How dates are written. | `YYYY-MM-DD` |
| **Timing** | *when it is due and what happens if it is late* | |
| `deadline` | When work is due, who sets it, and the consequence of missing it. A deadline never justifies skipping a check or a review — report the risk instead. | — |
| **When stuck** | *what to do instead of guessing* | |
| `on_missing_input` | A required fact is missing. ask stops and asks; note continues and marks the gap plainly. | `ask` |
| `on_conflict` | Two sources disagree and none is authoritative. ask stops and asks; note records both and flags it, resolving nothing. | `ask` |
| `on_check_failed` | A check in `verify` did not pass. stop refuses to produce the result; note produces it marked failed. Never adjust a value to make a check pass. | `stop` |
| `on_stale_source` | A source looks out of date. warn uses it and says so; stop does not use it. | `warn` |
<!-- config-reference:end -->
