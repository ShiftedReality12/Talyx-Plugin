# Talyx company setup

This file carries the same configuration parameters as Talyx's `.talyx/config.yaml`.
It is packaged as Markdown for apps that use Knowledge files. Setup fills the configuration;
you do not need to complete this template yourself.

## Current configuration

```yaml
{}
```

## Parameter reference - do not fill this section

The following commented template is generated from Talyx's canonical schema. Copy only
evidenced fields into Current configuration, keeping their names and types. Empty or unknown
fields stay absent. Comments and example values below are not company facts.

```yaml
# .talyx/config.yaml — written by talyx-setup from available evidence.
# Every key is optional. A key unsupported by the available evidence stays commented out;
# the skills then use its documented default. Values are the client's own words.
# Key names and shapes come from the config schema — keep them exactly.

# ---- Context — who this is, so skills never ask twice
# org_name: "<company name as it should appear>"
# org_description: "<what they do, in their words>"
# terminology:
#   <word to avoid>: "<word to use>"
# tone: "<their voice, if the sheet asks for one>"

# ---- People — who owns what; skills name them, never contact them
# people:
#   - { name: "<name>", role: "<role, only if stated>", owns: "<what they own, as written>" }
# rule_authority: ["<who may change a rule>"]
# escalate_to: ["<first>", "<then>"]          # in order; keep any condition in the name, e.g. "Beth Cantu — only if the RRC issues a notice"

# ---- Material — what arrives and where the truth lives
# inputs:
#   - { name: "<what arrives>", from: "<where>", provides: ["<what it reliably carries>"] }
# sources:
#   - { path: "<system or folder>", holds: "<what>", authoritative: true }   # authoritative only if the sheet says it wins

# ---- The work — what must always hold, and how the result is checked
# rules:
#   - { rule: "<always / never / must, verbatim>", because: "<their reason, if given>", beats: "<the rule it overrides, if stated>" }
# verify:
#   - { check: "<what>", against: "<which source>", match: "<how exactly, if stated>" }
# for_each: "<the thing the work repeats over>"

# ---- Guardrails — constraints for work prepared from this configuration
# never_decide:
#   - "<judgement that stays with a person, verbatim>"
# never_produce:
#   - "<kind of output never to generate, verbatim>"
# protected:
#   - "<content never to reword>"
# confidential:
#   - "<what must not appear in output>"

# ---- Review — nothing reaches anyone outside without a person
# review_required: true
# reviewers:
#   - { who: "<name>", checks: "<what>", required_by: "<outside body, if the sheet says so>" }

# ---- Output — where the result goes and what proves it arrived
# destination:
#   - { to: "<folder, system or portal>", kind: "<folder | system | submission>", receipt: "<what proves it arrived, if named>" }
# date_format: "YYYY-MM-DD"

# ---- Timing — when it is due and what happens if it is late
# deadline:
#   - { what: "<what is due>", when: "<when>", set_by: "<who or what sets it>", consequence: "<what happens if missed>" }

# ---- When stuck — what to do instead of guessing
# on_missing_input: ask     # ask | note
# on_conflict: ask          # ask | note
# on_check_failed: stop     # stop | note
# on_stale_source: warn     # warn | stop
```

## Types and defaults

- `org_name`: string. Default: unset.
- `org_description`: string. Default: unset.
- `terminology`: map. Default: unset.
- `tone`: string. Default: plain and direct.
- `people`: list<object>. Default: unset.
- `rule_authority`: list<string>. Default: unset.
- `escalate_to`: list<string>. Default: unset.
- `inputs`: list<object>. Default: unset.
- `sources`: list<object>. Default: unset.
- `rules`: list<object>. Default: unset.
- `verify`: list<object>. Default: unset.
- `for_each`: string. Default: unset.
- `never_decide`: list<string>. Default: unset.
- `never_produce`: list<string>. Default: unset.
- `protected`: list<string>. Default: unset.
- `confidential`: list<string>. Default: unset.
- `review_required`: boolean. Default: true.
- `reviewers`: list<object>. Default: unset.
- `destination`: list<object>. Default: talyx-output.
- `date_format`: string. Default: YYYY-MM-DD.
- `deadline`: list<object>. Default: unset.
- `on_missing_input`: ask | note. Default: ask.
- `on_conflict`: ask | note. Default: ask.
- `on_check_failed`: stop | note. Default: stop.
- `on_stale_source`: warn | stop. Default: warn.

## Shared use

The YAML under Current configuration is the company configuration. Later Talyx skills must read it before personalized work. Making this file available to another Gem or agent requires adding the same current file to its Knowledge; it is not automatic. In a file-capable Talyx workspace, save that YAML as `.talyx/config.yaml`. Preserve existing values and unknown extension keys; do not treat a schema example as an answer.
