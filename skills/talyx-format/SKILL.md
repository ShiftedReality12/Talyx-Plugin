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
