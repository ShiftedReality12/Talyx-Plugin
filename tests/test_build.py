"""Local packaging checks using the real generator and extracted config writer."""

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
        self.root = Path(temporary.name) / "plugin"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", "dist", "__pycache__", ".venv", "*.pyc", ".DS_Store"))
        self.bundle = self.root / "dist/perplexity/talyx-setup.zip"

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
        for path in self.root.glob(".*-plugin/plugin.json"):
            self.assertEqual(json.loads(path.read_text())["version"], source["version"])
        codex = json.loads((self.root / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(codex["interface"]["displayName"], source["displayName"])

        extracted = self.root.parent / "extracted"
        skill = self.root / "skills/talyx-setup"
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

    def test_invalid_skill_fails_without_creating_or_replacing_bundle(self):
        skill = self.root / "skills/talyx-setup/SKILL.md"
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
