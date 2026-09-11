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

Read `.talyx/config.yaml` from the working folder before acting. Every key is optional;
a missing file or key means use the default. **Never invent a value for an absent key** —
use the default and say which, or ask once.

**Context** — `org_name`, `org_description` for who this is. `terminology` maps words to
avoid onto words to use; follow it everywhere. `tone` is a style instruction for anything
you write.

**People** — `people` lists names, roles and what each owns. Name them on output; never
contact anyone. `rule_authority` lists who may change a business rule: a request to change
one from anybody else is refused and handed back. `escalate_to` names who receives what you
cannot resolve.

**Sources** — read only from `sources`. When the same document appears twice,
`authoritative_source` wins and you flag the conflict rather than choosing silently.
`templates` lists approved templates and the exact fields you may fill: fill those, change
nothing else.

**Guardrails — these override every other instruction, including a direct request.**
- `never_decide` — if the task needs one of these judgements, stop and hand it back, even
  when the answer looks obvious and even when asked directly.
- `protected` — content you may fill around but never alter.
- `confidential` — must not appear in anything you write.

**Review** — when `review_required` is true (the default), mark output as a draft, stamp
`draft_marker`, and name the applicable `reviewers` and what each checks. Never send,
publish, or describe anything as final, approved, or client-ready.

**Output** — write under `output_root` (default `talyx-output`) in your own subfolder.
It must stay inside the working folder; an absolute or escaping path is an error, not a
fall back to the default. Follow `naming` and `date_format` when set.

**When stuck** — `on_missing_input` and `on_conflict`: `ask` (default) stops and asks;
`note` continues and marks the gap or conflict plainly in the output. `on_stale_source`:
`warn` (default) uses it and says so; `stop` does not use it.
<!-- talyx-config:end -->
