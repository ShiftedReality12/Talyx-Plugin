# Talyx skills

The free package contains Talyx Setup, which prepares reusable company settings. Each workflow
skill can read the same settings when it is added to the package.

```text
skills/
├── README.md
└── talyx-setup/
    ├── SKILL.md
    ├── config.schema.json
    ├── config.template.yaml
    ├── references/
    │   ├── questions.md
    │   ├── field-mapping.md
    │   └── runtime.md
    └── scripts/
        ├── generate_config.py
        └── requirements.txt
```

[Setup](talyx-setup/SKILL.md) gathers evidenced, reusable company preferences and passes them to
[the writer](talyx-setup/scripts/generate_config.py). It writes the client's working-folder
`.talyx/config.yaml`, outside the installed plugin. The [schema](talyx-setup/config.schema.json)
defines fields and types; [questions](talyx-setup/references/questions.md) define conditional
prompts; [runtime.md](talyx-setup/references/runtime.md) defines the request, validation and recovery.
Hosts without the required runtime collect provisional answers only.

Add each workflow skill as a sibling of `talyx-setup/` when supplied. Its acceptance must show
that it reads the writer's saved config and follows the relevant settings in its actual output.
No placeholder workflow establishes that connection.

The canonical [schema definitions](../build/config-schema.json), [generator](../build/generate.py)
and [CLI tests](../tests/test_generate_config.py) live in this repository.
Generated schema, question reference, mapping, default documentation and chat adaptations must
be regenerated together. Subscription onboarding and connector work stay outside this free package.

See the [plugin README](../README.md) for installation and host limitations.
