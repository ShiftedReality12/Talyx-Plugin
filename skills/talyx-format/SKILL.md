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
