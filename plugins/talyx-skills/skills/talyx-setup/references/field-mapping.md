<!-- Generated from build/config-schema.json. -->

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
