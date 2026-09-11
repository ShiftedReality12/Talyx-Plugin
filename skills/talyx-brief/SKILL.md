---
name: talyx-brief
description: Turn notes, a transcript or a conversation into a one-page brief saved as a file. Use when the user wants a written brief, a handover note, or a summary they can keep and share rather than read in chat.
argument-hint: "[name:my-brief] [text or file path; blank uses the conversation]"
---

# Talyx Brief

**Outcome:** a one-page brief is written to a file in the user's own workspace, and the
user is told exactly where it landed.

**Done:** the file exists, its full path has been reported, and the brief fits on one page.

## Arguments

| Token | Meaning | Default |
|---|---|---|
| `name:<slug>` | Filename stem. Lowercase, hyphens. | derived from the subject |

Anything left after removing tokens is the source text, or a path to it. If nothing
remains, use the conversation.


## Steps

1. Resolve where the file goes: the folder named by `destination` in config, default
   `talyx-output` (see Configuration below). The path is `<folder>/briefs/<name>.md`.

2. Read the source text. If given a path, read that file.

3. Write the brief with these sections, omitting any that the source genuinely does not
   support rather than padding them:

   - **What this is** — one or two sentences
   - **Key points** — the substance, grouped by topic
   - **Decisions** — what was settled, and by whom if stated
   - **Open** — what is unresolved, and who owns it if stated
   - **Next** — concrete actions only if the source names them

4. **Every line must trace to the source.** No recommendations, no invented owners, no
   invented dates. Where the source is unclear, say so in the brief instead of resolving it.

5. Save to `<folder>/briefs/<name>.md`. If the file exists, do not overwrite it silently —
   append `-2`, `-3` and so on, and say which name was used.

6. Report the **full path** of the file written, and its approximate length. If the write
   fails, say what failed and where it tried to write. Do not report success without a
   file.

## Boundary

Keep it to one page. If the source is too large for that, say so and name what was left
out rather than writing three pages.

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
