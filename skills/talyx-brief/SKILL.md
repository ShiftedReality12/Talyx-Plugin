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
