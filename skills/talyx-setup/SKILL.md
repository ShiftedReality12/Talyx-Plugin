---
name: talyx-setup
description: Set up Talyx from available material and targeted answers. Use when starting Talyx, when an input or output is unclear, or when company rules change; preserves client configuration.
---

# Talyx Setup

**Outcome:** `.talyx/config.yaml` records the evidenced shared inputs, outputs, rules, and
review requirements a company reuses across real workflows, so later work does not guess or
ask twice.

**Done:** the file is written, its full path reported, and the user has seen what was found,
preserved, set, left at default, and still needs an answer.

## Start with what is available

Read an existing `.talyx/config.yaml` first. Then inspect material available in the current
conversation or working folder: attached files, a named folder, a stated workflow, and sources
the user names. A worksheet is optional evidence, never the complete definition of a workflow.
Do not claim to inspect a connector unless the host actually exposes it.

Ask only what remains material and unresolved: the input or source to use, the outcome wanted,
where it should go, who reviews it, and what must stay with a person. Do not repeat an existing
config value or a fact found in provided material. If no repeated workflow can be identified,
ask the user to name one concrete outcome before writing configuration.

## Ask simple, real questions

First inspect the current host's callable tool list and each relevant tool's schema. If the host
offers a structured question tool, use the exact callable tool it exposes — for example,
`AskUserQuestion`, `request_user_input`, or `request_user_input_async`. Do not guess a tool
name, invoke an unavailable tool, or describe a prose list as a native form.

Use the native question surface for only the unresolved material fields. Group at most three
independent fields; keep dependent questions for the next turn. Give a short question and short,
truthful choices when choices are known, and allow free text when that surface supports it. Do
not turn Setup into a generic questionnaire. For a conflict, display the existing and new values
in the question context and ask which to retain.

An answer that controls a dependent config value is required: do not advance, select a value, or
write that unresolved value after a timeout or no answer. If no native question tool is callable,
ask one short conversational question at a time. Do not claim every host supports native forms.

## Map evidence

Use the client's words. Map a worksheet when supplied, and map equivalent facts from attachments,
workspace material, or direct answers to the same fields. The generated mapping below describes
the worksheet convention; it does not make a worksheet mandatory.

Keep incoming material in `inputs`, separate from the requested output. Set `for_each` only
when the user or source states the repeat unit; a column name or a row layout is not that instruction.

<!-- talyx-mapping:start -->
## Mapping — sheet to config

Worksheet mapping, when a worksheet is supplied. Equivalent evidence from attached
material or direct answers maps to the same key. Unsupported keys stay absent. Values
are the client's words, never a paraphrase.

**Context**
- `org_name` — the sheet title
- `org_description` — only if the sheet says what the company does — otherwise absent
- `terminology` — any "we say X not Y" anywhere on the sheet
- `tone` — only if the sheet asks for a voice — otherwise default

**People**
- `people` — Who does it today — each name and what they own, as written; no role the sheet did not state
- `rule_authority` — only if the sheet says who may change a rule
- `escalate_to` — handoffs in Who does it today or the judgment column — in order, with any condition kept

**Material**
- `inputs` — Task (what starts it) and Systems — what arrives and from where
- `sources` — Systems / files it touches — every system named; `authoritative` only if the sheet says which wins

**The work**
- `rules` — the judgment column — every always / never / must, in their words; a demand that fits no key goes here verbatim and is named as uncovered
- `verify` — "has a right answer in X" — what is checked against what
- `for_each` — How often / how many — the thing the work repeats over (client, lease, household)

**Guardrails**
- `never_decide` — the judgment column — whatever must stay with a person, in their words
- `never_produce` — anything the sheet says the tool must never generate
- `protected` — anything that may not be reworded
- `confidential` — anything that must not appear in output

**Review**
- `review_required` — true when any review wording exists
- `reviewers` — review wording, usually hidden in the Task column — who checks what, and whether an outside body requires it

**Output**
- `destination` — Task — where it ends: a portal, a folder, a system; `receipt` when a confirmation is named
- `date_format` — only if the sheet shows one

**Timing**
- `deadline` — a due date and what happens if it is missed, wherever it appears; `set_by` when stated

**When stuck**
- `on_missing_input` — only if the sheet says what to do — otherwise default
- `on_conflict` — only if the sheet says what to do — otherwise default
- `on_check_failed` — only if the sheet says what to do ("if it won't reconcile, stop") — otherwise default
- `on_stale_source` — only if the sheet says what to do — otherwise default
<!-- talyx-mapping:end -->

Two things to read carefully rather than skim:

- **The judgment-call column is the guardrail.** Anything the sheet describes as needing a
  person becomes a `never_decide` entry, in their words.
- **Review wording is usually in the task column**, not a column of its own — phrases like
  "nothing goes out before X checks it". Turn each into a `reviewers` entry and set
  `review_required: true`.
- **Every sentence in the judgment column is a demand.** Each lands in a key, or is named in
  the report as covered by no key. Dropping one silently is the failure this skill exists to
  prevent. A demand that fits no key — a credential rule, a retention period, a language
  requirement, a time window — goes under `rules` verbatim **and** is named as uncovered.
- **If the sheet contradicts itself** — one column says a person reviews, another says nobody
  looks — do not pick one. Show both sentences and ask which is right.
- **A blank required cell on a filled row** (nobody named for "who does it") is a missing
  input. Ask; do not infer it from another row.
- **"See attached" with nothing attached** goes under what is still missing. Never add the
  missing thing as a source or invent what it holds.

## Steps

1. Read existing config, then available material. A worksheet, if supplied, is one evidence source.

2. Map what is evidenced. **Use the client's own words** for `never_decide`, `terminology` and
   `tone`. Do not translate them into your own phrasing.

3. Ask targeted native questions, when available, only for material gaps or conflicts:
   input/source, outcome, destination, review, and never-decide. Leave unsupported keys out so
   documented defaults apply. Do not ask for a key with a working default.

4. Merge, do not clobber. Apply a supported replacement when the user explicitly asks for it and
   supplies its value. Otherwise, when sources conflict or the intended replacement is unclear,
   show both values and ask; never choose silently. Preserve client entries outside the supported
   fields unchanged and report them as unvalidated; never delete them simply to make validation
   pass.

5. For a new file, fill `config.template.yaml` from this skill's own folder. For an existing file,
   edit it in place; retain its unknown entries, comments, and client edits. If the host cannot
   preserve those while editing, stop before writing and report that limitation. Keep every
   supported key name and shape exactly as the template has them — never invent a key, a field,
   or a structure. Uncomment and fill only values directly confirmed by the client or evidenced
   in available material; leave unknown supported fields commented so documented defaults apply.
   If the host exposes a YAML parser or schema checker, parse the written file and check each
   supported value against the template shape before reporting it. That check validates names and
   types, not whether source facts are true. If no parser is callable, report that parsing was
   not available.

6. Report, in this order:
   - the full path written
   - **what was found and preserved**, grouped, with the value
   - **what was set**, grouped, with the value
   - **what was left at a default**, and what that default is
   - **what evidence asked for that no key covers**, verbatim — may be empty
   - **what is still missing that would materially help**, at most three items, each with
     one line on what it would improve

## Boundary

This skill only writes shared config. It does not run a workflow, contact anyone, or promise that
a connector can read or write. A later workflow must actually read this config before relying on
it. If the available evidence names a workflow worth building, say so and stop — building it is
not this skill's job.

<!-- talyx-config:start -->
## Configuration

Read `.talyx/config.yaml` from the working folder first. If it is missing or unreadable,
run Talyx Setup or obtain the required parameters before doing personalized dependent work.
Every key is optional; absent means the documented default. **Never invent a value for an
absent key.** This config records approved workflow constraints; it is not authentication,
authorization, or a way to override the host's instructions.

**Context** `org_name` `org_description` `terminology` `tone`
Write in their voice. Follow `terminology` everywhere. Never restate their own description back at them.

**People** `people` `rule_authority` `escalate_to`
Name people on output; never contact anyone. `escalate_to` is a chain, in order — stop at the first who can decide. `rule_authority` identifies who may change a workflow rule; it does not authenticate anyone.

**Material** `inputs` `sources`
Read only from `sources`. The one marked `authoritative` wins a disagreement, and you report the disagreement rather than resolving it silently. Prefer a named `input` over asking someone to paste.

**The work** `rules` `verify` `for_each`
Every `rule` always holds; `beats` settles a conflict between two. No rule is traded for speed. `verify` says what is checked against what — if a check cannot be run, say so, and never report unchecked work as checked. `for_each` repeats the work per item, independently; one failure does not abandon the rest.

**Guardrails** `never_decide` `never_produce` `protected` `confidential`
Treat these as approved workflow constraints. They do not grant access, enforce a security policy, or override the host's instructions. `never_decide` — hand back. `never_produce` — do not generate. `protected` — never alter, reword or reformat. `confidential` — never mention.

**Review** `review_required` `reviewers`
When required, mark the result as needing review and name each reviewer and what they check, including where an outside body requires it. Never send, file, publish, or call anything final or approved.

**Output** `destination` `date_format`
Write to `destination`. A folder path must stay inside the working folder — an absolute or escaping path is an error, not a fallback. Where a destination names a `receipt`, report it; without one, say sent but unconfirmed.

**Timing** `deadline`
A `deadline` never justifies skipping a check or a review. Report the risk instead.

**When stuck** `on_missing_input` `on_conflict` `on_check_failed` `on_stale_source`
Follow the setting, default in brackets. Never adjust a value to make a check pass.

Defaults: `tone` plain and direct · `review_required` true · `destination` talyx-output · `date_format` YYYY-MM-DD · `on_missing_input` ask · `on_conflict` ask · `on_check_failed` stop · `on_stale_source` warn
<!-- talyx-config:end -->
