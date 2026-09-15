# Config writer contract

The skill gathers evidenced parameters. `scripts/generate_config.py` validates and writes YAML.
The sole output location is `<workspace>/.talyx/config.yaml`; the installed plugin is never the
client workspace. `config.schema.json` is generated from the canonical build schema, version 3.
`config.template.yaml` illustrates shapes only. It is not an alternative writer.

## Runtime

Requires a POSIX runtime (for example macOS or Linux), Python 3.10+ and the packages in
`scripts/requirements.txt`. Native Windows execution is not supported by this writer's file-lock
and directory operations; an available supported runtime is required. Use an existing compatible
runtime or an explicitly authorized local environment. The helper does not install packages or
access the network. If execution or dependencies are unavailable, report that and collect
provisional answers; do not substitute model-written YAML. Python alone is insufficient.

Resolve the paths from the actual installed skill and chosen working folder. Pass paths as
separate arguments using the host's tool. If using a shell, quote them safely. Never treat client
text as executable command text. `PYTHON`, `SKILL` and `WORKSPACE` below are explanatory placeholders.

```text
PYTHON SKILL/scripts/generate_config.py inspect --workspace WORKSPACE
PYTHON SKILL/scripts/generate_config.py apply --workspace WORKSPACE --request REQUEST.json --dry-run
PYTHON SKILL/scripts/generate_config.py apply --workspace WORKSPACE --request REQUEST.json
PYTHON SKILL/scripts/generate_config.py validate --workspace WORKSPACE
```

Use absolute workspace and request paths. Keep the temporary request in the chosen workspace's
temporary area; it contains client evidence. Do not copy it into the installed skill or a remote
system. Apply reads only the named request and current config; it does not read referenced source
documents, run a workflow, create output folders or call external services.

## Change request

All six keys below are required. Additional request keys are rejected. This is an example for a
new file, not a client answer. For an existing file, use the digest returned by `inspect`.

```json
{
  "schema_version": 3,
  "base_sha256": null,
  "changes": {"org_name": "Example Company"},
  "evidence": {
    "org_name": {
      "kind": "user",
      "reference": "Current setup answer",
      "quote": "Use Example Company as our company name."
    }
  },
  "replacements": [],
  "unresolved": []
}
```

| Field | Meaning |
|---|---|
| `schema_version` | Integer 3. A different contract version is rejected. |
| `base_sha256` | Exact digest from `inspect`, or null only when no file exists. |
| `changes` | Known config keys with complete, typed values. Omitted keys are preserved. |
| `evidence` | One entry per changed key: `kind` is `user` or `document`; reference and exact quote are nonempty strings. |
| `replacements` | Changed top-level keys explicitly authorized for replacement by the user. A differing existing meaningful value requires this entry and user evidence. |
| `unresolved` | Entries have `question_id`, `fields` and `reason`. Any entry prevents applying the request. |

Evidence is a caller-declared link to the source. The helper validates its shape, not its truth or
the user's identity. The skill must check the actual conversation or document. A document alone
does not authorize replacing a meaningful existing value. A clear user replacement instruction
already supplies that authority; do not add a second approval step.

## Preservation and validation

- Known new fields and object properties must match the packaged schema. No coercion of strings
  into booleans, invented keys, implicit deletion or null-as-deletion.
- Existing unknown root or nested fields remain untouched and are reported as unvalidated.
  Replacing a list or object that would discard an unknown nested field is rejected. Resolve the
  compatibility issue explicitly; do not remove client data or invent a list-matching rule.
- Replacing an internally commented collection is also rejected when the writer cannot preserve
  those comments safely. The config remains unchanged. Do not delete client comments to bypass
  this limit; report that this structure needs a comment-preserving writer update.
- Duplicate JSON/YAML keys, malformed files, unsupported YAML constructs, invalid known values,
  stale digests and unsafe output paths are rejected without a normal config replacement.
- For `destination.kind: folder`, `to` must be a relative path confined to the workspace. Other
  existing descriptive destination kinds remain descriptive and do not grant access or delivery
  authority. Consumers must resolve their meaning before taking an action.
- Config file or config-directory symlinks are rejected. The writer uses a same-directory temporary
  file, a helper lock, a base recheck and atomic replacement, preserving existing file permissions.
  These protect cooperating writers; they are not a transaction against all external editors.
- On a stale-file error, inspect and reconcile again. On a lock error, establish whether the owning
  process is still running before any recovery; do not blindly delete its lock. After an interrupted
  or uncertain write, inspect and validate the actual file before retrying.
- An unchanged update preserves the existing bytes. Defaults are returned separately for absent
  keys; they are not inserted as client facts.

## Receipt and consumer acceptance

The JSON result reports status, schema version, digest, current values, effective defaults and
unknown fields where applicable. Only a successful apply/read-back followed by successful
validation establishes that this writer saved structurally valid known settings.

It does not establish fact accuracy, source access, permissions, compliance, or workflow readiness.
Each consuming skill must actually read the saved config, apply the relevant defaults and
constraints, and produce its requested result. Its integration remains open until the actual
skill exists and this behavior is demonstrated. Do not create a placeholder consumer as proof.
