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

## Where the file goes

<!-- talyx-output-root:start -->
**Resolve the output root before composing any path.**

- **Read** `output_root` from `.talyx/config.yaml` in the current working directory.
  Unset, missing file, or unreadable → the root is `talyx-output`.
- **Validate** a set value: a relative directory that stays inside the working directory.
  An absolute path, or one that escapes upward, is an error — name the key and the value
  and stop. Never silently fall back to the default after rejecting a value.
- **Use** it as the sole location. Create it if absent. Compose the path as
  `<root>/briefs/<name>.md`.
<!-- talyx-output-root:end -->

## Steps

1. Resolve the output root using the block above.

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

5. Save to `<root>/briefs/<name>.md`. If the file exists, do not overwrite it silently —
   append `-2`, `-3` and so on, and say which name was used.

6. Report the **full path** of the file written, and its approximate length. If the write
   fails, say what failed and where it tried to write. Do not report success without a
   file.

## Boundary

Keep it to one page. If the source is too large for that, say so and name what was left
out rather than writing three pages.

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
