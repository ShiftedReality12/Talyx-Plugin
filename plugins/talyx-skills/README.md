# Talyx Skills

Free Talyx skills work with your own material and already-authorized tools. This release
includes **Talyx Setup**, which saves reusable company settings for free Talyx workflows.
No Talyx subscription or tier selection is required. Your AI app's plan and access are separate.

## Install

Use this repository address when adding the marketplace:

```text
https://github.com/ShiftedReality12/Talyx-Plugin
```

**Claude desktop with Cowork**

1. Open **Cowork → Customize → Plugins**.
2. Under **Personal plugins**, choose **+ → Add marketplace → Add from a repository**.
   Paste the address above and confirm.
3. Choose **Browse plugins**, find **talyx-skills** in the **talyx** marketplace, and install it.
4. Start a new Cowork task. Type **/** or click **+**, then select **talyx-setup**.

**ChatGPT desktop with Work locally**

1. Open **Plugins → Add → Add a marketplace**.
2. Paste the address above into **Source**. Leave **Git ref** and **Sparse paths** blank,
   then choose **Add marketplace**.
3. Find **talyx-skills** in the **talyx** marketplace and install it.
4. Start a **Work locally** task, choose your work folder, then type **@** and select **talyx-setup**.

If these menus are missing, check your app/account access with your administrator or Talyx contact.

<details>
<summary>Claude Code</summary>

Enter these commands inside a Claude Code conversation:

```text
/plugin marketplace add ShiftedReality12/Talyx-Plugin
/plugin install talyx-skills@talyx
/reload-plugins
/talyx-skills:talyx-setup
```

</details>

## Run Setup

Ask “Set up Talyx.” Setup asks which services or folders to use, offers existing connections when
available, and asks only for missing company preferences. You can choose files/folders only or
connect services later. It uses your app's question forms when available and short chat questions
otherwise. A worksheet is optional. The host owns sign-in and permissions.

[Setup](skills/talyx-setup/SKILL.md) reads existing settings and supplied material, then passes
evidenced parameters to [the bundled writer](skills/talyx-setup/scripts/generate_config.py).
The writer validates [the schema](skills/talyx-setup/config.schema.json), preserves comments and
unrelated settings, and saves `.talyx/config.yaml` in your working folder. It rejects ambiguous
replacements and stale updates. Unknown fields are preserved and reported as unvalidated.

The [runtime contract](skills/talyx-setup/references/runtime.md) describes runtime requirements,
validation and recovery. Hosts without the required runtime collect **provisional setup answers**;
Setup is complete only after the local writer validates and saves the actual configuration.
Missing service access does not block saving known preferences, but access must be checked before
dependent work. Configuration validation checks structure; each consuming workflow needs its own
check with the saved settings and real inputs.

<details>
<summary>Configuration reference — all 25 parameters</summary>

Every key is optional. ★ marks useful starting parameters. Setup asks only for what the
current work needs. Key names, types and defaults come from the executable schema.
The [template](skills/talyx-setup/config.template.yaml) illustrates their shapes.

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
| `sources` ★ | Where to read from when the host actually has access. Set authoritative: true only when the client evidence explicitly grants that source priority. Apply an unambiguous priority and report the disagreement; otherwise ask. | — |
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
| `destination` | Preferred output location: a folder, a system or a submission destination. Folder paths must stay inside the working folder. Default: local talyx-output folder. A destination is not permission to send. Report saved, delivered or confirmed only when an actual tool result establishes it; a receipt preference alone proves nothing. | `talyx-output (folder)` |
| `date_format` | How dates are written. | `YYYY-MM-DD` |
| **Timing** | *when it is due and what happens if it is late* | |
| `deadline` | When work is due, who sets it, and the consequence of missing it. A deadline never justifies skipping a check or a review — report the risk instead. | — |
| **When stuck** | *what to do instead of guessing* | |
| `on_missing_input` | A required fact is missing. ask stops and asks; note continues and marks the gap plainly. | `ask` |
| `on_conflict` | Two sources disagree and none is authoritative. ask stops and asks; note records both and flags it, resolving nothing. | `ask` |
| `on_check_failed` | A check in `verify` did not pass. stop refuses to produce the result; note produces it marked failed. Never adjust a value to make a check pass. | `stop` |
| `on_stale_source` | A source looks out of date. warn uses it and says so; stop does not use it. | `warn` |
<!-- config-reference:end -->

</details>
