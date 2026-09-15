# Talyx Setup — provisional answers for the free Talyx plugin

Generated from Talyx's canonical schema and question definitions. This file collects
answers; it is not an activated configuration. The local config writer must validate
and save them against the actual current file. Do not handwrite YAML.

## Current configuration — preserve an existing copy verbatim

No existing configuration supplied. Do not infer this means the local file is absent.

## Provisional answers — update this section only

```json
{
  "schema_version": 3,
  "changes": {},
  "evidence": {},
  "replacements": [],
  "unresolved": []
}
```

Each changed field needs evidence: kind (user or document), reference and exact quote.
Replacements name keys the user explicitly instructed to replace. Unresolved entries
have question_id, fields and reason. Do not add a digest without inspecting the actual
local config. These partial answers are not an executable apply request.

# Setup questions for the free Talyx plugin

<!-- Generated from build/config-schema.json. -->

Use these question IDs and their conditions. Ask only unresolved questions that affect
the requested setup; this is not a checklist to ask every client. Keep wording as written
except to insert evidenced task, output, person or source names and conflicting values. For a gap in
another existing field, use Q_FIELD below. Never invent a new config field.

## Q_FOLDER

**Ask:** Where should Talyx save your settings? Choose an existing working folder, or give a new folder name and where to create it.

- **Fields:** Workspace location only; no stored config key.
- **Ask when:** Only when no current or previously chosen working folder is established and local setup can save a config. Reuse an unambiguous folder answer; ask only for a missing location, never whether its name means a test.
- **Choices:** Use the host's actual folder picker when available, or accept a path. For a new folder, obtain access to its existing parent if needed, create it using available tools, and verify it. Request manual creation only after establishing the specific capability or access blocker. The working folder is not automatically a data source.

## Q_WORK

**Ask:** What recurring task would you like help with, and what should it produce?

- **Fields:** Context for question routing only; no stored config key.
- **Ask when:** The task or desired result is unclear and is needed to identify material setup gaps. Skip when the user already named the task, is changing a known setting, or only wants company-wide preferences. Do not impose a workflow menu.
- **Choices:** Free text, or concrete tasks the user already named. Use the answer to target questions; do not invent a workflow-name or outcome config field.

## Q_CONTEXT

**Ask:** What company and role should Talyx use as context?

- **Fields:** `org_name`, `org_description`, `people`
- **Ask when:** Reusable company or role context is relevant and the material does not establish it. Keep unneeded context absent; a self-contained task does not require a company profile.
- **Choices:** Free text. Extract company, role and responsibilities only when stated.

## Q_INPUT

**Ask:** Which services or folders should Talyx use, and what should it use each for?

- **Fields:** `inputs`, `sources`
- **Ask when:** On first setup when the service/source choice is not already explicit, even without a selected workflow. On updates, ask only when service choices or purposes need changing or clarification. An explicit files/folders-only or decide-later answer resolves the choice. One-off files and dates stay with the workflow run.
- **Choices:** Offer relevant connections discovered through actual host tools, files/folders only, or decide later. Accept another service by name. If only the service is answered, ask only for its purpose and store that wording verbatim in sources.holds. Do not assume the working folder is a data source or that an available tool is authorized.
- **If access missing:** For a selected service, ask: Connect {service} through {host}, use an export/upload, or leave it for later? Use a native connection flow only when exposed, otherwise verified host instructions. Recheck actual access after authorization. Save known preferences even if connecting is deferred; never store credentials or an invented connected flag.

## Q_DESTINATION

**Ask:** Where should Talyx save the results?

- **Fields:** `destination`
- **Ask when:** The requested destination is unclear or differs from the documented local talyx-output folder. Otherwise apply the existing destination or report the default without asking.
- **Choices:** The local output folder or another user-named permitted destination. An external destination is a preference, not permission to send.

## Q_REVIEW

**Ask:** Who should review the results before they are used or shared?

- **Fields:** `reviewers`, `review_required`
- **Ask when:** A reviewer is material to this client's workflow and has not been identified. Review stays required by default; never invent a reviewer.
- **Choices:** Me, or someone else (ask for their name and what they review). Map Me only when the person's identity is supplied; otherwise retain the unresolved identity.

## Q_HUMAN

**Ask:** Which decisions must always stay with you or another person?

- **Fields:** `never_decide`
- **Ask when:** The client describes judgments needing a person but the boundary is ambiguous. Do not require a generic risk questionnaire when no material gap exists.
- **Choices:** Use the client's wording; examples may come only from their stated workflow.

## Q_EXCLUDE

**Ask:** What information must never appear in the output?

- **Fields:** `confidential`, `never_produce`
- **Ask when:** A stated confidentiality or forbidden-output requirement needs clarification.
- **Choices:** Free text. Record exclusions verbatim; naming a requirement does not prove it is technically enforced.

## Q_PRESERVE

**Ask:** What wording must stay exactly as written?

- **Fields:** `protected`, `terminology`
- **Ask when:** Provided material requires exact wording or terminology but does not specify it clearly.
- **Choices:** Free text or exact passages from supplied material.

## Q_CONFLICT

**Ask:** I found two different values for {field}: {existing} and {proposed}. Which should I keep?

- **Fields:** The identified existing field; no new key.
- **Ask when:** A material conflict or ambiguous replacement remains. Show both evidence sources. An explicit user instruction supplying the replacement already resolves it.
- **Choices:** Keep existing; use proposed; or supply the correct value. Silence is unresolved.

## Q_FIELD

**Ask:** For {stated_requirement}, what should {missing_detail} be?

- **Fields:** The identified existing field; no new key.
- **Ask when:** A client-stated requirement maps to another existing schema field but lacks a required detail. Name that requirement, the exact field and its missing detail. Do not introduce requirements or ask about every optional field.
- **Choices:** Use only evidence-backed choices allowed by that field's schema, otherwise free text.

## Canonical field schema — reference, never client facts

All fields are optional. Defaults are effective behavior, not invented client answers.
Existing unknown fields must be preserved and reported as unvalidated by the writer.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Talyx company configuration",
  "x-talyx-schema-version": 3,
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "org_name": {
      "type": "string",
      "minLength": 1,
      "pattern": "\\S",
      "description": "Company name as it should appear in anything written."
    },
    "org_description": {
      "type": "string",
      "minLength": 1,
      "pattern": "\\S",
      "description": "What the company does. Context only; never restate it back at them."
    },
    "terminology": {
      "type": "object",
      "additionalProperties": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Word to avoid mapped onto word to use. Follow it everywhere."
    },
    "tone": {
      "type": "string",
      "minLength": 1,
      "pattern": "\\S",
      "description": "Style instruction for anything written.",
      "default": "plain and direct"
    },
    "people": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "role": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "owns": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          }
        },
        "required": [
          "name",
          "owns"
        ],
        "additionalProperties": false
      },
      "description": "Name, role, what each owns. Name them on output; never contact anyone."
    },
    "rule_authority": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Recorded owner for changes to a workflow rule. This is not authentication or access control."
    },
    "escalate_to": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Escalation chain, in order. Stop at the first person who can decide."
    },
    "inputs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "from": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "provides": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "pattern": "\\S"
            }
          }
        },
        "required": [
          "name",
          "from"
        ],
        "additionalProperties": false
      },
      "description": "What arrives, from where, and which facts it reliably carries. Prefer a named input over asking someone to paste."
    },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "holds": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "authoritative": {
            "type": "boolean"
          }
        },
        "required": [
          "path",
          "holds"
        ],
        "additionalProperties": false
      },
      "description": "Where to read from when the host actually has access. Set authoritative: true only when the client evidence explicitly grants that source priority. Apply an unambiguous priority and report the disagreement; otherwise ask."
    },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rule": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "because": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "beats": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          }
        },
        "required": [
          "rule"
        ],
        "additionalProperties": false
      },
      "description": "What must always hold, in the client's own words. Each may carry `because` and `beats` to settle a conflict with another rule. A rule is never traded away for speed or a deadline."
    },
    "verify": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "check": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "against": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "match": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          }
        },
        "required": [
          "check",
          "against"
        ],
        "additionalProperties": false
      },
      "description": "What is checked against what, and how exactly it must match. If a check cannot be run, say so — never report unchecked work as checked."
    },
    "for_each": {
      "type": "string",
      "minLength": 1,
      "pattern": "\\S",
      "description": "The thing the work repeats over — one per client, lease, household. Each run is independent; one failure does not abandon the rest."
    },
    "never_decide": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Judgements to hand back to a person, even when the answer looks obvious and even when asked directly."
    },
    "never_produce": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Kinds of output never to generate at all — a recommendation, a projection, a forecast. Different from a judgement: refusing to decide is not enough if the artefact itself is forbidden."
    },
    "protected": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Content that may be filled around but never altered, reworded or reformatted."
    },
    "confidential": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "pattern": "\\S"
      },
      "description": "Must not appear in anything written."
    },
    "review_required": {
      "type": "boolean",
      "description": "Mark the result as needing review and name who must check it. Never send, file, publish, or call anything final or approved.",
      "default": true
    },
    "reviewers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "who": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "checks": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "required_by": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          }
        },
        "required": [
          "who",
          "checks"
        ],
        "additionalProperties": false
      },
      "description": "Who checks what, and whether it is required by an outside body rather than internal preference. State that reason on the output."
    },
    "destination": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "to": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "kind": {
            "type": "string",
            "minLength": 1,
            "description": "Use folder for a local directory; system or submission for external destinations. Existing descriptive labels remain labels and grant no action permission.",
            "pattern": "\\S"
          },
          "receipt": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          }
        },
        "required": [
          "to",
          "kind"
        ],
        "additionalProperties": false
      },
      "description": "Preferred output location: a folder, a system or a submission destination. Folder paths must stay inside the working folder. Default: local talyx-output folder. A destination is not permission to send. Report saved, delivered or confirmed only when an actual tool result establishes it; a receipt preference alone proves nothing.",
      "default": [
        {
          "to": "talyx-output",
          "kind": "folder"
        }
      ]
    },
    "date_format": {
      "type": "string",
      "minLength": 1,
      "pattern": "\\S",
      "description": "How dates are written.",
      "default": "YYYY-MM-DD"
    },
    "deadline": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "what": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "when": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "set_by": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          },
          "consequence": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S"
          }
        },
        "required": [
          "what",
          "when"
        ],
        "additionalProperties": false
      },
      "description": "When work is due, who sets it, and the consequence of missing it. A deadline never justifies skipping a check or a review — report the risk instead."
    },
    "on_missing_input": {
      "type": "string",
      "enum": [
        "ask",
        "note"
      ],
      "description": "A required fact is missing. ask stops and asks; note continues and marks the gap plainly.",
      "default": "ask"
    },
    "on_conflict": {
      "type": "string",
      "enum": [
        "ask",
        "note"
      ],
      "description": "Two sources disagree and none is authoritative. ask stops and asks; note records both and flags it, resolving nothing.",
      "default": "ask"
    },
    "on_check_failed": {
      "type": "string",
      "enum": [
        "stop",
        "note"
      ],
      "description": "A check in `verify` did not pass. stop refuses to produce the result; note produces it marked failed. Never adjust a value to make a check pass.",
      "default": "stop"
    },
    "on_stale_source": {
      "type": "string",
      "enum": [
        "warn",
        "stop"
      ],
      "description": "A source looks out of date. warn uses it and says so; stop does not use it.",
      "default": "warn"
    }
  }
}
```
