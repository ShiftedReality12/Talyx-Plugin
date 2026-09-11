---
name: talyx-setup
description: Set up Talyx for this company by reading a completed scoping sheet, or by asking. Writes the config every other Talyx skill reads. Use when setting up Talyx for the first time, when a scoping sheet has been filled in, or when the company details, folders, reviewers or rules have changed.
argument-hint: "[path to a completed scoping sheet; blank asks instead] [reconfigure]"
---

# Talyx Setup

**Outcome:** `.talyx/config.yaml` exists and holds this company's real details, so no
other skill has to ask for them or guess.

**Done:** the file is written, its full path reported, and the user has been shown what
was set, what was left at a default, and what still needs them.

## Two ways in

**From a scoping sheet.** If given a path — a spreadsheet, PDF, or pasted text — read it
and map it. The sheet already asks for almost everything this config needs.

**By asking.** With no sheet, ask only for the five that carry most of the value, one
message, then stop: company name, what the company does, who reviews what before anything
goes to a client, what the tool must never decide, and which folders hold the material.
Everything else has a working default.

## Mapping a scoping sheet

The standard sheet has one row per candidate workflow: Task — what starts it and what it
produces · Systems / files it touches · Who does it today · How often / how many · Cloneable
or judgment call · Worth if 10x faster. The mapping below is generated from the config schema;
it is the only list of where each key comes from.

<!-- talyx-mapping:start -->
## Mapping — sheet to config

Every key, and where on the sheet it comes from. A key whose place on the sheet is
empty stays absent. Values are the client's words, never a paraphrase.

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

1. Read the sheet, or ask. Never do both in one run.

2. Map what is there. **Use the client's own words** for `never_decide`, `terminology` and
   `tone`. Do not translate them into your own phrasing.

3. For anything the source does not cover, leave the key out so the documented default
   applies. **Do not invent a value, and do not ask a follow-up question for a key that has
   a working default.**

4. Merge, do not clobber. If `.talyx/config.yaml` already exists, keep every value it has
   unless `reconfigure` was passed or the new source plainly contradicts it — in which case
   show both and ask which is right.

5. Write `.talyx/config.yaml` in the current working folder. Preserve the commented
   structure so a person can read and edit it afterwards.

6. Report, in this order:
   - the full path written
   - **what was set**, grouped, with the value
   - **what was left at a default**, and what that default is
   - **what the sheet asked for that no key covers**, verbatim — may be empty
   - **what is still missing that would materially help**, at most three items, each with
     one line on what it would improve

## Boundary

This skill only writes config. It does not run a workflow, read client documents beyond the
sheet it was given, or contact anyone. If a scoping sheet names a workflow worth building,
say so and stop — building it is not this skill's job.

<!-- talyx-config:start -->
## Configuration

Read `.talyx/config.yaml` from the working folder first. Every key is optional;
absent means the documented default. **Never invent a value for an absent key.**

**Context** `org_name` `org_description` `terminology` `tone`
Write in their voice. Follow `terminology` everywhere. Never restate their own description back at them.

**People** `people` `rule_authority` `escalate_to`
Name people on output; never contact anyone. `escalate_to` is a chain, in order — stop at the first who can decide. Only `rule_authority` may change a rule; a change requested by anyone else is refused and handed back.

**Material** `inputs` `sources`
Read only from `sources`. The one marked `authoritative` wins a disagreement, and you report the disagreement rather than resolving it silently. Prefer a named `input` over asking someone to paste.

**The work** `rules` `verify` `for_each`
Every `rule` always holds; `beats` settles a conflict between two. No rule is traded for speed. `verify` says what is checked against what — if a check cannot be run, say so, and never report unchecked work as checked. `for_each` repeats the work per item, independently; one failure does not abandon the rest.

**Guardrails** `never_decide` `never_produce` `protected` `confidential`
These outrank every other instruction, including a direct request. `never_decide` — hand back. `never_produce` — do not generate at all. `protected` — never alter, reword or reformat. `confidential` — never mention.

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
