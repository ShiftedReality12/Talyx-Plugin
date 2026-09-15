# Talyx skills

This is the plugin's shared skills directory. Each skill has its own folder containing
`SKILL.md` and any resources it needs. The current package contains:

```text
skills/
├── README.md
└── talyx-setup/
    ├── SKILL.md
    └── config.template.yaml
```

[Talyx Setup](talyx-setup/SKILL.md) creates or updates the company's configuration using the
[existing template](talyx-setup/config.template.yaml). The company configuration is saved in
the user's working folder as `.talyx/config.yaml`, outside the installed plugin.

Add each released workflow skill as another folder directly inside `skills/`, alongside
`talyx-setup/`. Workflow skills must read the shared company configuration before personalized
work. They do not belong inside the Setup folder.

The package still discovers skills from this directory. Removing the demonstration skills
changed the current inventory, not this layout. See the [plugin README](../README.md) for
installation and current limitations. Client handouts and generated downloads are distributed
separately from the plugin.
