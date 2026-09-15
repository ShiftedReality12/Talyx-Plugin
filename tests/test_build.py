"""Local packaging checks using the marketplace source, generator and config writer."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = (Path(temporary.name) / "plugin").resolve()
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", "dist", "__pycache__", ".venv", "*.pyc", ".DS_Store"))
        self.bundle = self.root / "dist/perplexity/talyx-setup.zip"

    def marketplace_payload(self):
        marketplace = json.loads((self.root / ".claude-plugin/marketplace.json").read_text())
        entry, = marketplace["plugins"]
        payload = (self.root / entry["source"]).resolve()
        self.assertEqual(payload, self.root / "plugins/talyx-skills")
        return payload

    def generate(self):
        return subprocess.run([sys.executable, "build/generate.py"], cwd=self.root,
                              capture_output=True, text=True, timeout=15)

    def snapshot(self):
        return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob("*") if path.is_file()
                and "dist" not in path.relative_to(self.root).parts}

    def test_repeatable_build_and_extracted_writer(self):
        result = self.generate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        before = self.snapshot()
        result = self.generate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.snapshot(), before)

        source = json.loads((self.root / "build/plugin.source.json").read_text())
        payload = self.marketplace_payload()
        for path in payload.glob(".*-plugin/plugin.json"):
            self.assertEqual(json.loads(path.read_text())["version"], source["version"])
        codex = json.loads((payload / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(codex["interface"]["displayName"], source["displayName"])

        extracted = self.root.parent / "extracted"
        skill = payload / "skills/talyx-setup"
        with zipfile.ZipFile(self.bundle) as bundle:
            files = bundle.namelist()
            self.assertIn("SKILL.md", files)
            self.assertIn("scripts/generate_config.py", files)
            for name in files:
                self.assertEqual(bundle.read(name), (skill / name).read_bytes())
            bundle.extractall(extracted)
        workspace = self.root.parent / "client"
        workspace.mkdir()
        result = subprocess.run([
            sys.executable, str(extracted / "scripts/generate_config.py"),
            "inspect", "--workspace", str(workspace),
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["current_values"], {})
        self.assertIs(receipt["effective_defaults"]["review_required"], True)
        self.assertFalse((workspace / ".talyx").exists())

    def test_marketplace_installs_runtime_only_and_writer_saves_config(self):
        result = self.generate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = self.marketplace_payload()
        for manifest in self.root.glob(".*-plugin/marketplace.json"):
            entry, = json.loads(manifest.read_text())["plugins"]
            self.assertEqual((self.root / entry["source"]).resolve(), payload)

        self.assertFalse(list(self.root.glob(".*-plugin/plugin.json")))
        self.assertFalse((self.root / "gemini-extension.json").exists())
        self.assertFalse((self.root / "skills").exists())
        for path in ("build/generate.py", "tests/test_build.py", "tests/test_generate_config.py",
                     "adapters/gemini/README.md", "adapters/m365-copilot/README.md"):
            self.assertTrue((self.root / path).is_file(), path)

        installed = self.root.parent / "installed"
        shutil.copytree(payload, installed)
        self.assertEqual({path.name for path in installed.iterdir()}, {
            ".claude-plugin", ".codex-plugin", ".cursor-plugin", ".devin-plugin",
            ".grok-plugin", "gemini-extension.json", "skills", "assets", "README.md", "LICENSE",
        })
        forbidden = {"build", "tests", "evals", "dist", "adapters", ".git", ".venv",
                     "__pycache__", ".DS_Store", "plugin.source.json", "config-schema.json"}
        for path in installed.rglob("*"):
            self.assertFalse(forbidden.intersection(path.relative_to(installed).parts), path)
            self.assertFalse(path.name.startswith("test_"), path)

        codex = json.loads((installed / ".codex-plugin/plugin.json").read_text())
        self.assertTrue((installed / codex["skills"]).is_dir())
        for key in ("logo", "logoDark"):
            self.assertTrue((installed / codex["interface"][key]).is_file())
        script = installed / "skills/talyx-setup/scripts/generate_config.py"
        workspace = self.root.parent / "client"
        workspace.mkdir()
        result = subprocess.run([
            sys.executable, str(script), "inspect", "--workspace", str(workspace),
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        inspected = json.loads(result.stdout)
        request = self.root.parent / "request.json"
        request.write_text(json.dumps({
            "schema_version": inspected["schema_version"],
            "base_sha256": inspected["sha256"],
            "changes": {"org_name": "Installed package check"},
            "evidence": {"org_name": {"kind": "user", "reference": "Packaging acceptance check",
                                      "quote": "Installed package check"}},
            "replacements": [], "unresolved": [],
        }))
        result = subprocess.run([
            sys.executable, str(script), "apply", "--workspace", str(workspace),
            "--request", str(request),
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((workspace / ".talyx/config.yaml").is_file())
        result = subprocess.run([
            sys.executable, str(script), "inspect", "--workspace", str(workspace),
        ], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["current_values"]["org_name"],
                         "Installed package check")

    def test_invalid_skill_fails_without_creating_or_replacing_bundle(self):
        skill = self.marketplace_payload() / "skills/talyx-setup/SKILL.md"
        skill.write_text(skill.read_text().replace("name: talyx-setup", "name: INVALID_NAME", 1))
        result = self.generate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[FAIL]", result.stdout)
        self.assertFalse(self.bundle.exists())

        self.bundle.parent.mkdir(parents=True)
        self.bundle.write_bytes(b"previous bundle must remain unchanged")
        result = self.generate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.bundle.read_bytes(), b"previous bundle must remain unchanged")


if __name__ == "__main__":
    unittest.main()
