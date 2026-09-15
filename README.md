# Talyx Skills repository

The free Talyx plugin currently contains **Talyx Setup**, which prepares reusable company
settings for free workflows. See the [client installation and configuration guide](plugins/talyx-skills/README.md)
for installation and use.

## What is installed

The installable plugin is [`plugins/talyx-skills/`](plugins/talyx-skills/). Repository marketplace
entries point to that directory. It contains the host manifests, skills and their runtime resources,
icons, license and client guide. Development tests, build tooling and separate chat adapters stay
outside that directory and outside the installed plugin.

```text
.claude-plugin/marketplace.json  Repository catalogue → ./plugins/talyx-skills
.cursor-plugin/marketplace.json Existing Cursor catalogue → same payload
.grok-plugin/marketplace.json   Existing Grok catalogue → same payload
plugins/talyx-skills/
  .*-plugin/plugin.json         Host plugin manifests
  gemini-extension.json        Gemini CLI extension manifest
  skills/
    README.md                  Skill layout
    talyx-setup/
      SKILL.md                 Setup instructions
      config.schema.json       Generated executable field contract
      config.template.yaml     Reference shapes
      references/              Questions, field mapping and runtime contract
      scripts/                 Config writer and runtime dependencies
  assets/                      Talyx icons
  LICENSE                      Payload license
  README.md                    Client installation and configuration reference
build/                         Canonical definitions and generator
tests/                         Version-controlled development acceptance tests
adapters/                      Separate Gemini Apps and Copilot setup materials
LICENSE                        Repository license
README.md                      Repository and maintainer guide
```

Each released workflow skill belongs beside `talyx-setup/` inside the payload's `skills/`
directory. Keep its required resources inside its own folder. Its acceptance must demonstrate
that the actual workflow reads the writer's saved configuration and follows the applicable
settings in its output. Existing manifests alone do not establish compatibility in each host.

## Other host materials

- **Gemini Apps:** follow [the Gem setup instructions](adapters/gemini/README.md).
- **Microsoft 365 Copilot:** follow [the Agent Builder instructions](adapters/m365-copilot/README.md).
- **Perplexity Computer:** upload the separately generated skill ZIP from `dist/perplexity/`.
- **Gemini CLI:** after obtaining this repository, install the local payload from the repository
  directory with `gemini extensions install ./plugins/talyx-skills`. The repository root is a
  marketplace source and is not a directly installable Gemini extension.

The chat adapters collect provisional answers from the same canonical schema and questions.
A supported local writer must validate and save them against the current company configuration.
Client PDFs, presentations and submission materials are separate deliverables.

## Maintainer checks

Host identity comes from [plugin.source.json](build/plugin.source.json). Field definitions,
questions and defaults come from [config-schema.json](build/config-schema.json); shared chat
instructions come from [free-setup-chat-instructions.txt](build/free-setup-chat-instructions.txt).
Change those definitions and regenerate the outputs together. The installed README's marked
configuration reference is generated from the schema.

Use Python 3.10+ with the packages in
[requirements.txt](plugins/talyx-skills/skills/talyx-setup/scripts/requirements.txt), then run:

```text
python build/generate.py
python -m unittest discover -s tests -v
```

[The generator](build/generate.py) rebuilds root marketplace catalogues, nested runtime manifests,
configuration references, chat adapters and skill ZIPs. ZIPs go in ignored `dist/`; failed skill
checks stop before creating or replacing a ZIP.

[Packaging tests](tests/test_build.py) resolve the actual marketplace source, copy that payload,
check that development files are excluded, and execute the installed writer through saving and
reading back configuration. They also verify repeatable generation, execution from an extracted
skill ZIP, and failed-build bundle preservation. [Writer tests](tests/test_generate_config.py)
cover validation, preservation, rejection and recovery, including denied deletion, interrupted
writers and competing writers. These are local executions in temporary workspaces. Installation
and workflow use in each target app require separate execution evidence.
