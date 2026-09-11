---
name: talyx-format
description: Rewrite messy notes, transcripts or pasted text into a clean structured document. Use when text needs tidying into headings and bullets, when notes are unstructured, or when the user asks to format, clean up or tidy something.
argument-hint: "[style:brief|notes|memo] [text or file path; blank uses what is already in the conversation]"
---

# Talyx Format

**Outcome:** the user gets their own text back, restructured and readable, with nothing
added and nothing dropped.

**Done:** the formatted text is printed in the conversation. No files are written.

## Arguments

Read tokens from the invocation. Anything left after removing them is the text, or a path
to it. If nothing remains, use the most recent substantial text in the conversation.

| Token | Meaning | Default |
|---|---|---|
| `style:brief` | Short. A one-line summary, then the key points. | |
| `style:notes` | Headings with bullets underneath, grouped by topic. | **this one** |
| `style:memo` | Prose paragraphs under headings, no bullets. | |

An unrecognised `style:` value is an error, not a guess — say which values are valid and stop.

## Steps

1. Read the text. If given a path, read that file.

2. Identify its natural structure: topics, decisions, questions, actions. Group by topic,
   not by the order things were said.

3. Rewrite in the requested style. **Preserve every fact, name, number and date exactly.**
   Fix grammar, remove filler and repetition, and drop conversational noise.

4. Do not add anything. No summaries of what the user "should" do, no recommendations, no
   invented headings for content that is not there. If something is ambiguous, keep the
   original wording rather than resolving it.

5. Print the result. End with one line naming the style used and the approximate input and
   output word counts, so the user can see what was compressed.

## Boundary

This skill only reformats. It does not analyse, advise, summarise beyond the requested
style, or write files. If the user wants an output file, that is `talyx-brief`.

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
