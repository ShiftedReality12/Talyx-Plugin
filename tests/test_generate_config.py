"""Local CLI acceptance checks; fault-injection checks are named explicitly."""

import hashlib
import json
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/talyx-setup/scripts/generate_config.py"


class GenerateConfigTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name) / "client"
        self.workspace.mkdir()
        self.config = self.workspace / ".talyx/config.yaml"
        self.request_path = Path(self.temporary.name) / "request.json"

    def run_cli(self, operation, *arguments, expected=0, python_flags=()):
        result = subprocess.run(
            [sys.executable, *python_flags, str(SCRIPT), operation, "--workspace", str(self.workspace), *arguments],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", result.stderr)
        return json.loads(result.stdout)

    def write_config(self, content, mode=0o640):
        self.config.parent.mkdir(exist_ok=True)
        self.config.write_bytes(content)
        self.config.chmod(mode)

    def request(self, changes, *, replacements=(), unresolved=(), evidence_kind="document"):
        content = self.config.read_bytes() if self.config.exists() else None
        return {
            "schema_version": 3,
            "base_sha256": None if content is None else hashlib.sha256(content).hexdigest(),
            "changes": changes,
            "evidence": {key: {"kind": evidence_kind, "reference": "User-supplied setup worksheet, section 1", "quote": str(value)} for key, value in changes.items()},
            "replacements": list(replacements),
            "unresolved": list(unresolved),
        }

    def apply(self, request, *, expected=0, dry_run=False):
        self.request_path.write_text(json.dumps(request), encoding="utf-8")
        arguments = ["--request", str(self.request_path)]
        if dry_run:
            arguments.append("--dry-run")
        return self.run_cli("apply", *arguments, expected=expected)

    def assert_rejected(self, request, code=None):
        before = self.config.read_bytes() if self.config.exists() else None
        result = self.apply(request, expected=1)
        if code:
            self.assertEqual(result["error"]["code"], code, result)
        self.assertEqual(self.config.read_bytes() if self.config.exists() else None, before)
        return result

    def test_inspect_defaults_are_typed_and_not_written(self):
        receipt = self.run_cli("inspect")
        self.assertIsNone(receipt["sha256"])
        self.assertEqual(receipt["current_values"], {})
        self.assertIs(receipt["effective_defaults"]["review_required"], True)
        self.assertEqual(receipt["effective_defaults"]["destination"], [{"to": "talyx-output", "kind": "folder"}])
        self.assertFalse(self.config.parent.exists())
        self.assertEqual(receipt["schema_version"], 3)
        self.assertEqual(receipt["validation_scope"], "structural_only")
        self.assertIn("workflow readiness are not verified", receipt["validation_note"])
        for prohibited in ("entitled", "activated", "authorized", "pcp_ready", "paid", "unlocked"):
            self.assertNotIn(prohibited, receipt)

    def test_success_readback_and_noop_preserve_bytes(self):
        changes = {
            "org_name": "Example Company",
            "review_required": True,
            "sources": [{"path": "Shared folder", "holds": "Incoming records", "authoritative": True}],
            "destination": [{"kind": "folder", "to": "reports/client"}],
        }
        first = self.apply(self.request(changes))
        saved = self.config.read_bytes()
        self.assertEqual(first["status"], "written")
        self.assertEqual(first["current_values"], changes)
        self.assertEqual(first["sha256"], hashlib.sha256(saved).hexdigest())
        self.assertEqual(stat.S_IMODE(self.config.stat().st_mode), 0o600)
        self.assertNotIn("tone:", saved.decode())
        second = self.apply(self.request(changes))
        self.assertEqual(second["status"], "unchanged")
        self.assertFalse(second["written"])
        self.assertEqual(self.config.read_bytes(), saved)
        self.assertEqual(self.run_cli("validate")["sha256"], first["sha256"])
        self.assertEqual(list(self.config.parent.iterdir()), [self.config])

    def test_empty_and_comment_only_files_are_supported(self):
        for content in (b"", b"# Client notes\n\n# Keep this exactly"):
            with self.subTest(content=content):
                self.write_config(content)
                self.run_cli("validate")
                self.apply(self.request({"org_name": "Acme"}))
                self.assertTrue(self.config.read_bytes().startswith(content))

    def test_dry_run_has_no_side_effects(self):
        receipt = self.apply(self.request({"org_name": "Acme"}), dry_run=True)
        self.assertEqual(receipt["status"], "dry_run")
        self.assertFalse(receipt["written"])
        self.assertFalse(self.config.parent.exists())

    def test_explicit_empty_apply_creates_valid_config_without_saving_defaults(self):
        receipt = self.apply(self.request({}))
        self.assertEqual(receipt["status"], "written")
        self.assertTrue(receipt["written"])
        self.assertEqual(receipt["current_values"], {})
        self.assertEqual(self.config.read_bytes(), b"{}\n")
        self.assertEqual(self.run_cli("validate")["status"], "valid")
        before = self.config.read_bytes()
        self.assertEqual(self.apply(self.request({}))["status"], "unchanged")
        self.assertEqual(self.config.read_bytes(), before)

    def test_strict_types_enums_and_unknown_fields(self):
        examples = [
            {"review_required": "true"},
            {"review_required": 1},
            {"people": [{"name": "Beth", "owns": ["review"]}]},
            {"people": [{"name": "Beth"}]},
            {"sources": [{"path": "Sheet", "holds": "Inputs", "authoritative": "yes"}]},
            {"destination": [{"to": "reports", "kind": True}]},
            {"inputs": [{"name": "Report", "from": "Team", "provides": "facts"}]},
            {"on_conflict": "ignore"},
            {"people": [{"name": "Beth", "owns": "Review", "admin": True}]},
            {"terminology": {"customer": True}},
            {"paid": True},
            {"pcp_ready": True},
            {"org_name": None},
        ]
        for changes in examples:
            with self.subTest(changes=changes):
                self.assert_rejected(self.request(changes), "INVALID_REQUEST")
                self.assertFalse(self.config.parent.exists())

    def test_evidence_and_exact_request_contract(self):
        missing = self.request({"org_name": "Acme"})
        missing["evidence"] = {}
        self.assert_rejected(missing, "MISSING_EVIDENCE")
        for changed in ("missing_required", "extra_key", "empty_quote", "wrong_kind", "wrong_version"):
            request = self.request({"org_name": "Acme"})
            if changed == "missing_required":
                del request["unresolved"]
            elif changed == "extra_key":
                request["approved"] = True
            elif changed == "empty_quote":
                request["evidence"]["org_name"]["quote"] = " "
            elif changed == "wrong_kind":
                request["evidence"]["org_name"]["kind"] = "inferred"
            else:
                request["schema_version"] = 2
            with self.subTest(changed=changed):
                self.assert_rejected(request, "INVALID_REQUEST")

    def test_unresolved_questions_block_every_change(self):
        self.write_config(b"org_name: Existing\n")
        request = self.request({"tone": "Formal"}, unresolved=[{"question_id": "source-owner", "fields": ["sources"], "reason": "Authority conflict"}])
        self.assert_rejected(request, "UNRESOLVED_QUESTIONS")

    def test_explicit_user_replacement_declaration_is_required(self):
        self.write_config(b"org_name: Existing\nreview_required: false\n")
        self.assert_rejected(self.request({"org_name": "New"}), "REPLACEMENT_AUTHORITY_REQUIRED")
        self.assert_rejected(self.request({"org_name": "New"}, replacements=["org_name"]), "REPLACEMENT_AUTHORITY_REQUIRED")
        self.assert_rejected(self.request({"review_required": True}, evidence_kind="user"), "REPLACEMENT_AUTHORITY_REQUIRED")
        receipt = self.apply(self.request({"org_name": "New"}, replacements=["org_name"], evidence_kind="user"))
        self.assertEqual(receipt["current_values"], {"org_name": "New", "review_required": False})
        self.assertEqual(stat.S_IMODE(self.config.stat().st_mode), 0o640)

    def test_comments_unknown_root_and_nested_values_survive(self):
        self.write_config(b'# Company note\norg_name: "Existing"  # Preserve spelling\nclient_extension: {code: "001"} # Keep extension\npeople:\n  - name: Beth\n    owns: Review\n    client_id: "001" # Keep nested data\n')
        receipt = self.apply(self.request({"tone": "Formal"}))
        text = self.config.read_text()
        for expected in ("# Company note", "# Preserve spelling", "# Keep extension", "# Keep nested data", 'client_id: "001"', 'org_name: "Existing"'):
            self.assertIn(expected, text)
        self.assertEqual({entry["path"] for entry in receipt["unknown_fields"]}, {"/client_extension", "/people/0/client_id"})
        self.assertTrue(all(entry["validation"] == "unvalidated" for entry in receipt["unknown_fields"]))
        self.assertEqual(receipt["current_values"]["client_extension"], {"code": "001"})
        self.assert_rejected(self.request({"people": [{"name": "Beth", "owns": "Review"}]}, replacements=["people"], evidence_kind="user"), "UNKNOWN_DATA_LOSS")

    def test_unknown_fields_do_not_hide_invalid_known_fields(self):
        self.write_config(b'people:\n  - name: Beth\n    owns: [Review]\n    client_id: "001"\n')
        result = self.run_cli("validate", expected=1)
        self.assertEqual(result["error"]["code"], "INVALID_EXISTING_CONFIG")
        self.assert_rejected(self.request({"tone": "Formal"}), "INVALID_EXISTING_CONFIG")

    def test_legacy_destination_descriptions_and_unknown_what_survive(self):
        self.write_config(b'destination:\n  - to: Client portal\n    kind: Portal upload after review\n    what: Draft report # Client wording\n')
        receipt = self.apply(self.request({"org_name": "Acme"}))
        self.assertEqual(receipt["unknown_fields"], [{"path": "/destination/0/what", "value": "Draft report", "validation": "unvalidated"}])
        self.assertIn("# Client wording", self.config.read_text())
        self.assertEqual(receipt["current_values"]["destination"][0]["kind"], "Portal upload after review")

    def test_commented_nested_replacement_is_rejected_without_losing_comments(self):
        self.write_config(b"people:\n  - name: Beth # Client spelling\n    owns: Review\n    # Client role note\n    role: Director\n")
        request = self.request(
            {"people": [{"name": "Beth", "owns": "Review", "role": "Partner"}]},
            replacements=["people"], evidence_kind="user",
        )
        result = self.assert_rejected(request, "COMMENT_PRESERVATION_REQUIRED")
        self.assertIn("config unchanged", result["error"]["message"])

    def test_commented_block_scalar_replacement_is_rejected_without_losing_comments(self):
        self.write_config(b"tone: | # Client voice note\n  Plain and direct\n")
        self.assert_rejected(self.request({"tone": "Formal"}, replacements=["tone"], evidence_kind="user"), "COMMENT_PRESERVATION_REQUIRED")

    def test_duplicate_malformed_and_unsupported_yaml(self):
        invalid = [
            b"org_name: One\norg_name: Two\n",
            b"people: [{name: Beth, name: Jo, owns: Review}]\n",
            b"org_name: [unterminated\n",
            b"---\norg_name: One\n---\norg_name: Two\n",
            b"org_name: !!python/object/apply:os.system ['echo unsafe']\n",
            b"org_name: &company Acme\ntone: *company\n",
            b"<<: {org_name: Acme}\n",
            b"org_name: null\n",
            b"[org_name, Acme]\n",
            b"null\n",
            b"extension: .nan\n",
        ]
        for content in invalid:
            with self.subTest(content=content):
                self.write_config(content)
                self.run_cli("validate", expected=1)
                self.assert_rejected(self.request({"tone": "Formal"}))

    def test_duplicate_and_malformed_json_request(self):
        for content in ('{"changes":{},"changes":{}}', '{"changes":', '{"changes":{"org_name":NaN}}'):
            with self.subTest(content=content):
                self.request_path.write_text(content)
                self.run_cli("apply", "--request", str(self.request_path), expected=1)
                self.assertFalse(self.config.parent.exists())

    def test_stale_digest_preserves_external_change(self):
        self.write_config(b"org_name: Original\n")
        request = self.request({"tone": "Formal"})
        self.config.write_bytes(b"org_name: Edited elsewhere\n")
        self.assert_rejected(request, "STALE_BASE")

    def test_lock_has_actionable_recovery_and_preserves_original(self):
        self.write_config(b"org_name: Original\n")
        lock = self.config.parent / ".config.yaml.lock"
        lock.write_text('{"pid": 123456789, "operation": "apply"}\n')
        result = self.assert_rejected(self.request({"tone": "Formal"}), "CONFIG_LOCKED")
        self.assertIn("Confirm no helper is running", result["error"]["recovery"])
        self.assertTrue(lock.exists())

    def run_fault_injected_cli(self, prelude):
        request = self.request({"tone": "Formal"})
        self.request_path.write_text(json.dumps(request))
        arguments = [str(SCRIPT), "apply", "--workspace", str(self.workspace), "--request", str(self.request_path)]
        code = "import os, runpy, signal, sys\n" + prelude + "\nsys.argv = " + repr(arguments) + "\nrunpy.run_path(sys.argv[0], run_name='__main__')\n"
        return subprocess.run([sys.executable, "-c", code], text=True, capture_output=True, timeout=15)

    @unittest.skipUnless(hasattr(signal, "SIGTERM"), "Requires POSIX signals")
    def test_fault_injected_interruption_before_replace_keeps_original_and_lock(self):
        original = b"org_name: Original\n"
        self.write_config(original)
        result = self.run_fault_injected_cli("os.replace = lambda *args, **kwargs: os.kill(os.getpid(), signal.SIGTERM)")
        self.assertEqual(result.returncode, -signal.SIGTERM, result.stdout + result.stderr)
        self.assertEqual(self.config.read_bytes(), original)
        self.assertTrue((self.config.parent / ".config.yaml.lock").exists())
        self.assert_rejected(self.request({"tone": "Formal"}), "CONFIG_LOCKED")
        self.run_cli("validate")

    def test_fault_injected_external_write_is_caught_before_replace(self):
        self.write_config(b"org_name: Original\n")
        prelude = f"""original_fsync = os.fsync
calls = 0
def fsync_with_external_write(fd):
    global calls
    calls += 1
    original_fsync(fd)
    if calls == 2:
        with open({str(self.config)!r}, 'wb') as stream:
            stream.write(b'org_name: External edit\\n')
os.fsync = fsync_with_external_write
"""
        result = self.run_fault_injected_cli(prelude)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["error"]["code"], "CONCURRENT_CHANGE")
        self.assertEqual(self.config.read_bytes(), b"org_name: External edit\n")
        self.assertEqual(list(self.config.parent.iterdir()), [self.config])

    def test_folder_destinations_reject_absolute_traversal_and_symlink_escape(self):
        (self.workspace / "escape").symlink_to(Path(self.temporary.name))
        for target in ("/tmp/output", "../output", "reports/../../out", "C:\\output", "C:output", "reports\\..\\out", "escape/output"):
            with self.subTest(target=target):
                self.assert_rejected(self.request({"destination": [{"kind": "folder", "to": target}]}), "UNSAFE_DESTINATION")
        self.apply(self.request({"destination": [{"kind": "system", "to": "Client portal"}]}))

    def test_existing_and_default_destination_paths_are_checked(self):
        self.write_config(b"destination: [{kind: folder, to: ../escape}]\n")
        self.assertEqual(self.run_cli("validate", expected=1)["error"]["code"], "UNSAFE_DESTINATION")
        self.write_config(b"org_name: Acme\n")
        (self.workspace / "talyx-output").symlink_to(Path(self.temporary.name))
        self.assertEqual(self.run_cli("inspect", expected=1)["error"]["code"], "UNSAFE_DESTINATION")

    def test_config_file_symlink_is_rejected(self):
        target = Path(self.temporary.name) / "outside.yaml"
        target.write_bytes(b"org_name: Outside\n")
        self.config.parent.mkdir()
        self.config.symlink_to(target)
        self.assertEqual(self.run_cli("inspect", expected=1)["error"]["code"], "UNSAFE_CONFIG_PATH")
        self.assert_rejected(self.request({"tone": "Formal"}), "UNSAFE_CONFIG_PATH")
        self.assertEqual(target.read_bytes(), b"org_name: Outside\n")

    def test_config_directory_symlink_is_rejected(self):
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        self.config.parent.symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_cli("inspect", expected=1)["error"]["code"], "UNSAFE_CONFIG_PATH")
        self.assert_rejected(self.request({"tone": "Formal"}), "UNSAFE_CONFIG_PATH")
        self.assertEqual(list(outside.iterdir()), [])

    def test_missing_dependencies_give_json_instructions_without_changes(self):
        result = self.run_cli("inspect", expected=1, python_flags=("-S",))
        self.assertEqual(result["error"]["code"], "MISSING_DEPENDENCY")
        self.assertTrue(result["error"]["requirements"].endswith("scripts/requirements.txt"))
        self.assertFalse(self.config.parent.exists())

    def test_fault_injected_unsupported_platform_gives_actionable_json(self):
        result = self.run_fault_injected_cli("del os.O_NOFOLLOW")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        error = json.loads(result.stdout)["error"]
        self.assertEqual(error["code"], "UNSUPPORTED_PLATFORM")
        self.assertIn("macOS or Linux", error["message"])
        self.assertFalse(self.config.parent.exists())


if __name__ == "__main__":
    unittest.main()
