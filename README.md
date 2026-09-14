# Talyx Skills

The free Talyx plugin provides reusable skills for work with your own material and existing
tools. Setup creates the shared company configuration those skills use.
After the requested placeholder cleanup, this local preview contains Setup only; the next
workflow package is pending. That describes this preview's inventory, not the scope of the free product.

## Choose your app

Open your one-page guide and follow the steps. Talyx is free; your AI app's plan and access are separate.

| App | One-page guide | What to use |
|---|---|---|
| Claude desktop with Cowork | [Install guide](docs/install/talyx-claude-cowork-one-pager.pdf) | Add the Talyx marketplace, install the plugin, then start Setup. |
| ChatGPT desktop with Work locally | [Install guide](docs/install/talyx-chatgpt-work-one-pager.pdf) | **Plugins → Add → Add a marketplace**, then install Talyx. |
| Perplexity Computer | [Upload guide](docs/install/talyx-perplexity-computer-one-pager.pdf) | Upload [talyx-setup.zip](docs/install/talyx-setup.zip). |
| Gemini Apps | [Gem guide](docs/install/talyx-gemini-apps-one-pager.pdf) | Copy the entire [instruction text](docs/install/gemini-gem-instructions.txt), then upload the supplied [company setup file](docs/install/talyx-company-setup.md). |
| Microsoft 365 Copilot Agent Builder | [Agent guide](docs/install/talyx-m365-copilot-agent-builder-one-pager.pdf) | Use the [agent instructions](docs/install/m365-copilot-agent-builder-instructions.md) and [company configuration file](docs/install/talyx-company-setup.txt). |

Gemini and Microsoft 365 use prepared adaptations, with a manual step to save and reuse the
configuration in Knowledge. They are not repository-plugin installations. These guides were
checked against documentation; fresh installation and configuration reuse in each app remain
to be tested. Microsoft 365 requires an eligible work tenant, not consumer or GitHub Copilot.

For Gemini, create your Gem once at **gemini.google.com → Settings and help → Gems**.
Use the same Google account on your other devices. Mobile: **Menu → Gems → Talyx Setup**.
If your desktop or mobile app does not show Gems, open Gemini in your browser. Native desktop
Gem access remains unverified; Gemini Live does not support Gems. The [Gemini instructions and
file-saving help](docs/install/gemini-gem-instructions.md) explain how to retain your setup.

For Claude Code, enter these commands inside its conversation:

```text
/plugin marketplace add ShiftedReality12/Talyx-Plugin
/plugin install talyx-skills@talyx
/reload-plugins
/talyx-skills:talyx-setup
```

## Start here

Run `talyx-setup` first. It reads what is already available in your workspace or chat, including
an optional worksheet, then asks only for unresolved inputs, outcome, destination, review, and
guardrails. It uses the app's real question tool where available, with short conversational
questions otherwise. It fills the existing schema in `.talyx/config.yaml` and preserves existing
values, comments and client extensions. Explicit updates apply without asking twice; ambiguous
conflicts are put back to you. Review the reported values before relying on them.

Setup is free. It establishes reusable configuration; it does not run a workflow or claim a
connector can access material the host has not exposed. A released client workflow is not yet
included in this package.

## Skills

| Skill | What it does | Writes files |
|---|---|---|
| `talyx-setup` | Discovers available material, asks only material gaps, and writes reusable configuration. A worksheet is optional. | yes |

## Configuration

One file, `.talyx/config.yaml`, in the folder you work in. Every key is optional. `talyx-setup`
writes it with comments so you can read and edit it; the full key list is below.

Skills never hardcode your company, folders, people or rules — they read them from that
file. That is what lets the same skill work for any company without being rewritten, and
what stops a skill from making a call that is yours to make.

Other generated manifests remain development artifacts and are not client-install promises.

## Manifests are generated

Every manifest here, and the configuration block inside each skill, is produced from one
source by a build script kept outside this repository. **Do not edit them by hand** — the
next build overwrites them.

## Notes

This package adds no server, hooks, bundled executable or connector endpoints. Setup may use
material already available through your app and its authorized tools. It does not install or
authorize connectors. Bundled resources live inside the skill folder; your company configuration
lives in the working folder. Schema checks validate structure, not the truth of source facts.

## Every config key

★ marks useful starting parameters; Setup asks only for information the current work needs.

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
| `rule_authority` | Recorded owner for changes to a workflow rule. This is not authentication or access control. | — |
| `escalate_to` | Escalation chain, in order. Stop at the first person who can decide. | — |
| **Material** | *what arrives and where the truth lives* | |
| `inputs` ★ | What arrives, from where, and which facts it reliably carries. Prefer a named input over asking someone to paste. | — |
| `sources` ★ | Where to read from. Mark one `authoritative: true` and it wins any disagreement — and the disagreement is reported, never silently resolved. | — |
| **The work** | *what must always hold, and how the result is checked* | |
| `rules` ★ | What must always hold, in the client's own words. Each may carry `because` and `beats` to settle a conflict with another rule. A rule is never traded away for speed or a deadline. | — |
| `verify` ★ | What is checked against what, and how exactly it must match. If a check cannot be run, say so — never report unchecked work as checked. | — |
| `for_each` | The thing the work repeats over — one per client, lease, household. Each run is independent; one failure does not abandon the rest. | — |
| **Guardrails** | *constraints for work prepared from this configuration* | |
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
