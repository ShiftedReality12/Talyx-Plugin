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

The standard sheet has one row per candidate workflow and these columns:

| Column | Holds | Maps to |
|---|---|---|
| Task — what starts it, what it produces | the trigger and the deliverable | `inputs`, and the review wording usually hides in here |
| Systems / files it touches | named systems and folders | `sources`, `inputs` |
| Who does it today | the single owner, and handoffs | `people`, `escalate_to` |
| How often / how many | volume | context only, not a config key |
| Cloneable, or judgment call? | **what must stay human** | `never_decide` |
| Worth if 10x faster | value | context only, not a config key |

Two things to read carefully rather than skim:

- **The judgment-call column is the guardrail.** Anything the sheet describes as needing a
  person becomes a `never_decide` entry, in their words.
- **Review wording is usually in the task column**, not a column of its own — phrases like
  "nothing goes out before X checks it". Turn each into a `reviewers` entry and set
  `review_required: true`.

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
   - **what is still missing that would materially help**, at most three items, each with
     one line on what it would improve

## Boundary

This skill only writes config. It does not run a workflow, read client documents beyond the
sheet it was given, or contact anyone. If a scoping sheet names a workflow worth building,
say so and stop — building it is not this skill's job.

<!-- talyx-config:start -->
## Configuration

Read `.talyx/config.yaml` from the working folder before acting. Every key is
optional; a missing file or key means use the default. **Never invent a value for
an absent key** -- use the default and say which, or ask once.

**Context** -- who this is, so skills do not ask every run

- `org_name` (unset) -- Company name as it should appear in anything written.
- `org_description` (unset) -- What the company actually does. Use for context; never restate it back at them.
- `terminology` (unset) -- Word to avoid mapped onto word to use. Follow it in everything written.

**People** -- who owns what; skills name them, never contact them

- `people` (unset) -- Names, roles and what each owns. Name them on output; never contact anyone.
- `rule_authority` (unset) -- Who may change a business rule. A request to change one from anyone else is refused and handed back.
- `escalate_to` (unset) -- Who receives anything the skill cannot resolve.

**Inputs** -- what arrives, where from, and what it reliably contains

- `inputs` (unset) -- What arrives, where from, and which facts it reliably carries. Prefer a named input over asking the user to paste.

**Sources** -- where material lives and which copy is authoritative

- `sources` (unset) -- Folders to read from. Read only from these; never guess a location.
- `authoritative_source` (unset) -- When the same document appears twice, this one wins — and the conflict is flagged, not silently resolved.
- `templates` (unset) -- Approved templates and the exact fields that may be filled. Fill those; change nothing else.

**Output** -- where files go, what they are called, how they read

- `output_root` (default `talyx-output`) -- Where files are written, relative to the working folder. Must stay inside it — an absolute or escaping path is an error, not a fall back to the default.
- `naming` (default `{name}`) -- Filename pattern. Available: {client} {document} {date} {name}.
- `date_format` (default `YYYY-MM-DD`) -- How dates are written.
- `tone` (default `plain and direct`) -- Style instruction to follow in anything written.

**Guardrails** -- overrides every other instruction, including a direct request

- `never_decide` (unset) -- Judgements the skill must NOT make. Stop and hand back, even when the answer looks obvious and even when asked directly.
- `protected` (unset) -- Content that may be filled around but never altered.
- `confidential` (unset) -- Must not appear in anything the skill writes.

**Review** -- nothing reaches a client without a person

- `review_required` (default `true`) -- Mark output as a draft needing review. Never send, publish, or call anything final, approved or client-ready.
- `reviewers` (unset) -- Who checks what. Name them and what they check on the output.
- `draft_marker` (default `DRAFT — not for release`) -- Line stamped on every draft so nobody mistakes it for final.

**When stuck** -- what to do instead of guessing

- `on_missing_input` (default `ask`) -- A required fact is missing. ask stops and asks; note continues and marks the gap plainly.
- `on_conflict` (default `ask`) -- Two sources disagree. ask stops and asks; note records both and flags it, resolving nothing.
- `on_stale_source` (default `warn`) -- A source looks out of date. warn uses it and says so; stop does not use it.
<!-- talyx-config:end -->
