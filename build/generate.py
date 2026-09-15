#!/usr/bin/env python3
"""
Generate every host manifest and the Perplexity skill bundles from one source file.

Nothing here is hand-enumerated: hosts are declared as data in HOSTS, and every
output is derived from build/plugin.source.json. To change the plugin's identity,
edit that file and re-run this script. Never edit a generated manifest directly.

These canonical build sources live in the repository. The free Setup skill ships one
local Python config writer, its pinned dependencies and a generated JSON Schema.
The writer does not install dependencies, contact services or run workflows.
Only plugins/talyx-skills is installed; root catalogues select that payload while
build tooling, tests and chat adapters remain separate repository materials.

Usage:  python3 build/generate.py
"""

import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLUGIN_SOURCE = "./plugins/talyx-skills"
PLUGIN = os.path.join(ROOT, "plugins", "talyx-skills")
DIST = os.path.join(ROOT, "dist")
SOURCE = os.path.join(HERE, "plugin.source.json")

# Keys every host manifest carries.
BASE = ["name", "version", "description", "author", "homepage",
        "repository", "license", "keywords"]

# Host profiles. `extra` names additional keys; `marketplace` picks the catalogue
# shape, or None for hosts that use none.
#   manifest-only  -> plugin.json
#   claude-style   -> metadata carries version, plugin entry does not
#   omp-style      -> plugin entry carries version, metadata does not
HOSTS = {
    "claude":  {"dir": ".claude-plugin",  "extra": [], "marketplace": "claude-style"},
    "codex":   {"dir": ".codex-plugin",   "extra": ["skills", "interface"], "marketplace": None},
    "cursor":  {"dir": ".cursor-plugin",  "extra": ["displayName"], "marketplace": "claude-style"},
    "grok":    {"dir": ".grok-plugin",    "extra": ["skills"], "marketplace": "claude-style"},
    "devin":   {"dir": ".devin-plugin",   "extra": [], "marketplace": None},
}


CONFIG_START = "<!-- talyx-config:start -->"
CONFIG_END = "<!-- talyx-config:end -->"


def inject_config_block(skills, schema):
    """Write the shared config contract into every skill, between markers.

    Skills cannot read a file above their own directory -- layouts differ by host --
    so each one carries its own copy. Hand-maintaining N copies guarantees drift,
    so the block is generated once from build/config-schema.json and injected here.
    A skill with no markers gets them appended.
    """
    block = build_config_block(schema).strip()
    wrapped = "%s\n%s\n%s" % (CONFIG_START, block, CONFIG_END)
    touched = []
    for skill in skills:
        path = os.path.join(PLUGIN, "skills", skill, "SKILL.md")
        text = open(path, encoding="utf-8").read()
        if "talyx-config: none" in text.split("---")[1] if text.startswith("---") else False:
            continue  # skill opts out: it reads no config
        if CONFIG_START in text and CONFIG_END in text:
            a = text.index(CONFIG_START)
            b = text.index(CONFIG_END) + len(CONFIG_END)
            new = text[:a] + wrapped + text[b:]
        else:
            new = text.rstrip() + "\n\n" + wrapped + "\n"
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
            touched.append(skill)
    return touched



SCHEMA = os.path.join(HERE, "config-schema.json")


def load_schema():
    return json.load(open(SCHEMA, encoding="utf-8"))


def display_default(key):
    if "default_label" in key:
        return key["default_label"]
    value = key["default"]
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def write_setup_resources(schema):
    """Compile the executable schema and question/mapping references from one source."""
    base = os.path.join(PLUGIN, "skills", "talyx-setup")
    properties = {}
    for key in schema["keys"]:
        definition = dict(key["validation"])
        definition["description"] = key["does"]
        if key["default"] is not None:
            definition["default"] = key["default"]
        properties[key["name"]] = definition
    write_json(os.path.join(base, "config.schema.json"), {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Talyx company configuration",
        "x-talyx-schema-version": schema["version"],
        "type": "object", "additionalProperties": False, "properties": properties,
    })
    refs = os.path.join(base, "references")
    os.makedirs(refs, exist_ok=True)
    open(os.path.join(refs, "field-mapping.md"), "w", encoding="utf-8").write(
        "<!-- Generated from build/config-schema.json. -->\n\n" + build_mapping_block(schema))
    rows = ["# Setup questions for the free Talyx plugin", "",
            "<!-- Generated from build/config-schema.json. -->", "",
            "Use these question IDs and their conditions. Ask only unresolved questions that affect",
            "the requested setup; this is not a checklist to ask every client. Keep wording as written",
            "except to insert evidenced task, output, person or source names and conflicting values. For a gap in",
            "another existing field, use Q_FIELD below. Never invent a new config field.", ""]
    for question in schema["setup_questions"]:
        rows += ["## " + question["id"], "", "**Ask:** " + question["prompt"], ""]
        for name, value in question.items():
            if name in ("id", "prompt"):
                continue
            label = name.replace("_", " ").capitalize()
            rendered = ", ".join("`%s`" % v for v in value) if isinstance(value, list) else value
            if name == "fields" and not value:
                rendered = {
                    "Q_WORK": "Context for question routing only; no stored config key.",
                    "Q_FOLDER": "Workspace location only; no stored config key.",
                }.get(question["id"], "The identified existing field; no new key.")
            rows.append("- **%s:** %s" % (label, rendered))
        rows.append("")
    open(os.path.join(refs, "questions.md"), "w", encoding="utf-8").write("\n".join(rows))


def write_chat_adapters(schema):
    """Chat-only collection uses the same questions/types, without a second YAML writer."""
    base = os.path.join(PLUGIN, "skills", "talyx-setup")
    questions = open(os.path.join(base, "references", "questions.md"), encoding="utf-8").read()
    contract = open(os.path.join(base, "config.schema.json"), encoding="utf-8").read()
    instructions = open(os.path.join(HERE, "free-setup-chat-instructions.txt"), encoding="utf-8").read()
    for host, filename, instruction_filename in (
        ("gemini", "talyx-company-setup.md", "gemini-gem-instructions.txt"),
        ("m365-copilot", "talyx-company-setup.txt", "copilot-agent-instructions.txt"),
    ):
        folder = os.path.join(ROOT, "adapters", host)
        open(os.path.join(folder, instruction_filename), "w", encoding="utf-8").write(
            instructions.replace("{knowledge_file}", filename))
        provisional = {"schema_version": schema["version"], "changes": {}, "evidence": {},
                       "replacements": [], "unresolved": []}
        text = "\n".join([
            "# Talyx Setup — provisional answers for the free Talyx plugin", "",
            "Generated from Talyx's canonical schema and question definitions. This file collects",
            "answers; it is not an activated configuration. The local config writer must validate",
            "and save them against the actual current file. Do not handwrite YAML.", "",
            "## Current configuration — preserve an existing copy verbatim", "",
            "No existing configuration supplied. Do not infer this means the local file is absent.", "",
            "## Provisional answers — update this section only", "", "```json",
            json.dumps(provisional, indent=2), "```", "",
            "Each changed field needs evidence: kind (user or document), reference and exact quote.",
            "Replacements name keys the user explicitly instructed to replace. Unresolved entries",
            "have question_id, fields and reason. Do not add a digest without inspecting the actual",
            "local config. These partial answers are not an executable apply request.", "",
            questions, "## Canonical field schema — reference, never client facts", "",
            "All fields are optional. Defaults are effective behavior, not invented client answers.",
            "Existing unknown fields must be preserved and reported as unvalidated by the writer.", "",
            "```json", contract.rstrip(), "```", "",
        ])
        open(os.path.join(folder, filename), "w", encoding="utf-8").write(text)


def build_config_block(schema):
    """Generate the shared behavior contract, grouped by configuration purpose."""
    out = ["## Configuration", "",
           "Workflow consumers read `.talyx/config.yaml` from the working folder first. If it is missing",
           "or unreadable, run Talyx Setup or obtain the required parameters before personalized dependent",
           "work. Setup itself uses the writer's `inspect` operation; it does not invoke itself.",
           "Every key is optional; absent means the documented default. **Never invent a value for an",
           "absent key.** This config records approved workflow constraints; it is not authentication,",
           "authorization, or a way to override the host's instructions.", ""]
    by_group = {}
    for k in schema["keys"]:
        by_group.setdefault(k["group"], []).append(k)
    for g in schema["groups"]:
        keys = by_group.get(g["id"], [])
        if not keys:
            continue
        names = " ".join("`%s`" % k["name"] for k in keys)
        out.append("**%s** %s" % (g["title"], names))
        out.append(g["contract"])
        out.append("")
    defaults = [k for k in schema["keys"] if k["default"] is not None]
    out.append("Defaults: " + " · ".join("`%s` %s" % (k["name"], display_default(k)) for k in defaults))
    return "\n".join(out).strip() + "\n"


def build_mapping_block(schema):
    """Sheet -> config, generated from the schema so no key can exist without a mapping."""
    missing = [k["name"] for k in schema["keys"] if not k.get("sheet")]
    if missing:
        sys.exit("config-schema.json: no `sheet` mapping for: " + ", ".join(missing))
    by_group = {}
    for k in schema["keys"]:
        by_group.setdefault(k["group"], []).append(k)
    out = ["## Mapping — sheet to config", "",
           "Worksheet mapping, when a worksheet is supplied. Equivalent evidence from attached",
           "material or direct answers maps to the same key. Unsupported keys stay absent. Values",
           "are the client's words, never a paraphrase.", ""]
    for gr in schema["groups"]:
        keys = by_group.get(gr["id"], [])
        if not keys:
            continue
        out.append("**%s**" % gr["title"])
        for k in keys:
            out.append("- `%s` — %s" % (k["name"], k["sheet"]))
        out.append("")
    return "\n".join(out).strip() + "\n"


def write_config_template(schema):
    """A human reference: every key in its exact shape, all commented out.

    Lives inside the skill's own folder because a skill may read only its own directory.
    Generated from the schema, so key names and shapes cannot drift between clients.
    """
    missing = [k["name"] for k in schema["keys"] if not k.get("shape")]
    if missing:
        sys.exit("config-schema.json: no `shape` for: " + ", ".join(missing))
    by_group = {}
    for k in schema["keys"]:
        by_group.setdefault(k["group"], []).append(k)
    out = ["# .talyx/config.yaml — reference shapes, not a file to fill by hand.",
           "# Talyx Setup passes evidenced values to scripts/generate_config.py.",
           "# Every key is optional; absent keys use their documented defaults.",
           "# Examples are not client facts. config.schema.json defines the executable types.", ""]
    for gr in schema["groups"]:
        keys = by_group.get(gr["id"], [])
        if not keys:
            continue
        out.append("# ---- %s — %s" % (gr["title"], gr["intent"]))
        for k in keys:
            for line in k["shape"].split("\n"):
                out.append("# " + line)
        out.append("")
    path = os.path.join(PLUGIN, "skills", "talyx-setup", "config.template.yaml")
    text = "\n".join(out).rstrip() + "\n"
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if text != old:
        open(path, "w", encoding="utf-8").write(text)
    return text != old


def sync_readme_reference(schema):
    """Write the full key reference into the README, between markers.

    The README is where a client looks up what exists, so it must be complete, and
    it is generated so it cannot fall behind.
    """
    path = os.path.join(PLUGIN, "README.md")
    text = open(path, encoding="utf-8").read()
    rows = ["| Key | What it does | Default |", "|---|---|---|"]
    by_group = {}
    for k in schema["keys"]:
        by_group.setdefault(k["group"], []).append(k)
    for g in schema["groups"]:
        keys = by_group.get(g["id"], [])
        if not keys:
            continue
        rows.append("| **%s** | *%s* | |" % (g["title"], g["intent"]))
        for k in keys:
            star = " ★" if k.get("star") else ""
            d = "`%s`" % display_default(k) if k["default"] is not None else "—"
            rows.append("| `%s`%s | %s | %s |" % (k["name"], star, k["does"], d))
    block = "<!-- config-reference:start -->\n" + "\n".join(rows) + "\n<!-- config-reference:end -->"
    a, b = "<!-- config-reference:start -->", "<!-- config-reference:end -->"
    if a in text and b in text:
        new = text[:text.index(a)] + block + text[text.index(b) + len(b):]
    else:
        new = text.rstrip() + "\n\n## Every config key\n\n" + block + "\n"
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
        return True
    return False


def check_config_coverage(schema):
    """Every schema key must be documented in the README. Generated, so always true —
    this guards against the generator itself being bypassed."""
    text = open(os.path.join(PLUGIN, "README.md"), encoding="utf-8").read()
    return sorted(k["name"] for k in schema["keys"] if "`%s`" % k["name"] not in text)


def load_source():
    with open(SOURCE, encoding="utf-8") as fh:
        src = json.load(fh)
    return {k: v for k, v in src.items() if not k.startswith("_")}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    return path


def build_manifest(src, profile):
    out = {}
    for key in BASE:
        if key in src:
            out[key] = src[key]
    for key in profile["extra"] or []:
        if key == "skills":
            out["skills"] = "./skills/"
        elif key == "interface":
            out[key] = {
                "displayName": src["displayName"],
                "developerName": src["author"]["name"],
                "websiteURL": src["homepage"],
                **src["interface"],
            }
        elif key in src:
            out[key] = src[key]
    return out


def build_gemini_manifest(src):
    """Gemini CLI extension manifest at the installable payload root.

    The extension is installed from that local directory. Only name, version and
    description are ours to set; skills use the adjacent `skills/` directory.
    """
    return {k: src[k] for k in ("name", "version", "description")}


def build_marketplace(src, style):
    mkt = src["marketplace"]
    entry = {
        "name": src["name"],
        "description": src["description"],
        "author": src["author"],
        "homepage": src["homepage"],
        "tags": mkt["tags"],
        "source": PLUGIN_SOURCE,
    }
    meta = {"description": mkt["description"]}
    if style == "claude-style":
        meta["version"] = src["version"]
    else:                      # omp-style
        entry["version"] = src["version"]
    return {"name": mkt["name"], "owner": mkt["owner"], "metadata": meta, "plugins": [entry]}


def discover_skills():
    skills_dir = os.path.join(PLUGIN, "skills")
    return sorted(d for d in os.listdir(skills_dir)
                  if os.path.isdir(os.path.join(skills_dir, d)))


def build_perplexity_bundles(skills):
    """One ZIP per skill with SKILL.md at the ZIP root.

    Perplexity has no plugin manifest and no marketplace -- skills are uploaded
    individually. Limits: 32 MiB, 100 files, 255-char names.
    """
    out_dir = os.path.join(DIST, "perplexity")
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    made = []
    for skill in skills:
        src_dir = os.path.join(PLUGIN, "skills", skill)
        zip_path = os.path.join(out_dir, skill + ".zip")
        count = 0
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(src_dir):
                dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                for fn in sorted(filenames):
                    if fn == ".DS_Store":
                        continue
                    full = os.path.join(dirpath, fn)
                    rel = os.path.relpath(full, src_dir)
                    zf.write(full, rel)
                    count += 1
        size = os.path.getsize(zip_path)
        assert count <= 100, "%s exceeds Perplexity's 100-file limit" % skill
        assert size <= 32 * 1024 * 1024, "%s exceeds Perplexity's 32 MiB limit" % skill
        made.append((skill, count, size))
    return made



def check_skills(skills):
    """Check skill metadata and portability before packaging."""
    import re
    report = []
    for skill in skills:
        path = os.path.join(PLUGIN, "skills", skill, "SKILL.md")
        text = open(path, encoding="utf-8").read()
        fm = text.split("---")[1] if text.startswith("---") else ""
        body = text[len(fm) + 6:] if fm else text
        # the injected contract is ours, not the author's -- exclude it from author checks
        if CONFIG_START in body:
            body = body[:body.index(CONFIG_START)]
        fails, warns = [], []

        name = re.search(r"^name:\s*(.+)$", fm, re.M)
        desc = re.search(r"^description:\s*(.+)$", fm, re.M | re.S)

        # -- loads at all --
        if not name:
            fails.append("no `name` in frontmatter")
        elif not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name.group(1).strip()):
            fails.append("`name` must be lowercase-with-hyphens (Perplexity rejects otherwise)")
        elif len(name.group(1).strip()) > 64:
            fails.append("`name` over 64 chars")

        if not desc:
            fails.append("no `description` — without it the skill never auto-invokes")
        else:
            d = desc.group(1).strip()
            if len(d.encode("utf-8")) > 1024:
                fails.append("`description` over 1024 bytes (Perplexity limit)")
            if not re.search(r"\bUse (when|for|to)\b", d, re.I):
                warns.append("`description` has no 'Use when/for' trigger phrase — auto-invoke will be unreliable")

        # -- portability: the rule that broke Chat --
        for m in re.finditer(r"\.\./", body):
            fails.append("reads above its own directory (`../`) — breaks in Claude Chat")
            break

        # -- environment assumptions: written for a terminal, not a business user --
        if re.search(r"\bgit (rev-parse|status|diff|log|branch|commit|add|push)\b", body):
            fails.append("invokes git — a business user has no repo")
        if re.search(r"^```bash", body, re.M):
            warns.append("uses a bash fence — verify the target host allows shell")
        for m in re.finditer(r"(/Users/[A-Za-z0-9._-]+|~/\.[a-z]+)", body):
            fails.append("machine-local path `%s` — will not exist for a client" % m.group(1))
            break

        # -- generic, not wired to one client --
        sysname = re.search(r"\b(SharePoint|OneDrive|Outlook|Google Drive|Dropbox|Teams|Slack)\b", body)
        if sysname:
            warns.append("names `%s` in prose — should come from `sources` in config, not be hardcoded"
                         % sysname.group(1))

        # -- config contract --
        if "talyx-config: none" not in fm and "talyx-config:start" not in text:
            warns.append("config contract not injected — run the generator")

        size = len(text.encode("utf-8"))
        report.append((skill, fails, warns, size))
    return report



def main():
    src = load_source()
    schema = load_schema()
    written = []

    for host, profile in sorted(HOSTS.items()):
        target = os.path.join(PLUGIN, profile["dir"])
        if profile["extra"] is not None:
            written.append(write_json(os.path.join(target, "plugin.json"),
                                      build_manifest(src, profile)))
        if profile["marketplace"]:
            written.append(write_json(os.path.join(ROOT, profile["dir"], "marketplace.json"),
                                      build_marketplace(src, profile["marketplace"])))

    written.append(write_json(os.path.join(PLUGIN, "gemini-extension.json"),
                              build_gemini_manifest(src)))

    skills = discover_skills()
    write_setup_resources(schema)
    write_chat_adapters(schema)
    injected = inject_config_block(skills, schema)
    templated = write_config_template(schema)

    print("Source      : %s v%s" % (src["name"], src["version"]))
    print("Hosts       : %d" % len(HOSTS))
    print("Skills      : %s" % ", ".join(skills))
    print()
    print("Manifests written:")
    for p in written:
        print("  %s" % os.path.relpath(p, ROOT))

    print()
    print("Config contract injected into: %s" % (", ".join(injected) if injected else "no change"))
    print("Config template: %s" % ("rewritten" if templated else "no change"))

    sync_readme_reference(schema)
    missing = check_config_coverage(schema)
    print()
    print("Config schema: %d keys in %d groups" % (len(schema["keys"]), len(schema["groups"])))
    if missing:
        print("  ! README does not document: %s" % ", ".join(missing))
    else:
        print("  every key documented in README")

    print()
    print("Skill intake check")
    allclear = True
    for skill, fails, warns, size in check_skills(skills):
        mark = "FAIL" if fails else ("warn" if warns else "ok  ")
        print("  [%s] %-18s %5d bytes" % (mark, skill, size))
        for f in fails:
            allclear = False
            print("         ! %s" % f)
        for w in warns:
            print("         ~ %s" % w)
    if allclear:
        print("  -- no blocking problems")

    if not allclear or missing:
        sys.exit("Build failed — fix the items above. No bundles were created or replaced.")

    print()
    print("Perplexity bundles (one skill per ZIP):")
    for skill, count, size in build_perplexity_bundles(skills):
        print("  dist/perplexity/%s.zip  (%d files, %d bytes)" % (skill, count, size))

    print()
    print("Generated artifacts passed static checks for v%s." % src["version"])
    print("Runtime, host installation and actual workflow consumption require separate verification.")


if __name__ == "__main__":
    main()
