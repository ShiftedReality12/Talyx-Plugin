#!/usr/bin/env python3
"""Inspect, validate, or update only the current workspace's Talyx configuration."""

from __future__ import annotations

import argparse
import copy
import errno
import hashlib
import io
import json
import math
import os
from pathlib import Path, PureWindowsPath
import stat
import sys
import uuid
from contextlib import contextmanager
from dataclasses import dataclass


SCHEMA_VERSION = 3
CONFIG_NAME = "config.yaml"
LOCK_NAME = ".config.yaml.lock"
VALIDATION_NOTE = (
    "Structural validation of known fields and local folder paths only. Evidence, "
    "user authority, connections, access, and workflow readiness are not verified."
)


class ConfigError(Exception):
    def __init__(self, code, message, **details):
        super().__init__(message)
        self.code = code
        self.details = details


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ConfigError("ARGUMENT_ERROR", message)


def emit(value):
    print(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2))


def digest(content):
    return None if content is None else hashlib.sha256(content).hexdigest()


def pointer(parts):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError("DUPLICATE_JSON_KEY", f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    def reject_constant(value):
        raise ConfigError("INVALID_JSON", f"Non-finite JSON number: {value}")

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (ValueError, UnicodeError) as exc:
        raise ConfigError("INVALID_JSON", f"Cannot read JSON: {exc}") from exc


def plain(value, parts=()):
    """Keep YAML values JSON-compatible, without stringifying unsupported types."""
    if isinstance(value, dict):
        if getattr(value, "merge", None):
            raise ConfigError("UNSUPPORTED_YAML", "YAML merge keys are not supported.", path=pointer(parts))
        result = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ConfigError("INVALID_YAML", "Mapping keys must be strings.", path=pointer(parts))
            result[str(key)] = plain(item, (*parts, key))
        return result
    if isinstance(value, list):
        return [plain(item, (*parts, index)) for index, item in enumerate(value)]
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float) and math.isfinite(value):
        return float(value)
    raise ConfigError("INVALID_YAML", "Only JSON-compatible YAML values are supported.", path=pointer(parts))


def has_internal_comments(value):
    """Whole-field replacement cannot safely relocate comments inside that field."""
    comments = getattr(value, "ca", None)
    if comments and (comments.comment or comments.items or comments.end):
        return True
    if getattr(value, "comment", None):
        return True
    if isinstance(value, dict):
        return any(has_internal_comments(item) for item in value.values())
    if isinstance(value, list):
        return any(has_internal_comments(item) for item in value)
    return False


@dataclass
class Snapshot:
    content: bytes | None
    data: object
    values: dict
    mode: int | None
    prefix: str = ""


class ConfigHelper:
    def __init__(self, workspace):
        required_flags = ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK")
        required_dir_fd = (os.open, os.mkdir, os.stat, os.unlink, os.rename)
        if (
            os.name != "posix"
            or any(not hasattr(os, flag) for flag in required_flags)
            or not all(function in os.supports_dir_fd for function in required_dir_fd)
        ):
            raise ConfigError(
                "UNSUPPORTED_PLATFORM",
                "Run this helper with Python 3.10+ on macOS or Linux, which provide the required safe filesystem operations. Native Windows is not supported.",
            )
        try:
            from ruamel.yaml import YAML
            from ruamel.yaml.comments import CommentedMap
            from ruamel.yaml.events import AliasEvent
            from ruamel.yaml.error import YAMLError
            from jsonschema import Draft202012Validator
            from jsonschema.exceptions import SchemaError
        except ImportError as exc:
            requirements = Path(__file__).with_name("requirements.txt")
            raise ConfigError(
                "MISSING_DEPENDENCY",
                "Install the pinned requirements into a Python 3.10+ virtual environment, then retry with its Python.",
                requirements=str(requirements),
                missing_module=exc.name,
            ) from exc
        self.YAML = YAML
        self.CommentedMap = CommentedMap
        self.AliasEvent = AliasEvent
        self.YAMLError = YAMLError
        self.Validator = Draft202012Validator
        requested = Path(workspace)
        if not requested.is_absolute() or not requested.is_dir():
            raise ConfigError("INVALID_WORKSPACE", "--workspace must be an existing absolute directory.")
        self.workspace = requested.resolve()
        self.config_dir = self.workspace / ".talyx"
        self.config_path = self.config_dir / CONFIG_NAME
        self.schema = read_json(Path(__file__).resolve().parents[1] / "config.schema.json")
        if not isinstance(self.schema, dict) or self.schema.get("x-talyx-schema-version") != SCHEMA_VERSION:
            raise ConfigError("SCHEMA_VERSION_MISMATCH", "The packaged schema version must be 3.")
        try:
            Draft202012Validator.check_schema(self.schema)
        except SchemaError as exc:
            raise ConfigError("INVALID_SCHEMA", "The packaged configuration schema is invalid.") from exc
        self.fields = self.schema.get("properties")
        if not isinstance(self.fields, dict):
            raise ConfigError("INVALID_SCHEMA", "The packaged schema must define configuration properties.")

    def yaml(self):
        yaml = self.YAML(typ="rt")
        yaml.allow_duplicate_keys = False
        yaml.preserve_quotes = True
        return yaml

    def parse(self, content, mode):
        if content is None:
            return Snapshot(None, self.CommentedMap(), {}, mode)
        try:
            source = content.decode("utf-8")
            yaml = self.yaml()
            allowed_tags = {"tag:yaml.org,2002:" + t for t in ("str", "bool", "int", "float", "null", "seq", "map")}
            for event in yaml.parse(source):
                if isinstance(event, self.AliasEvent) or getattr(event, "anchor", None):
                    raise ConfigError("UNSUPPORTED_YAML", "YAML anchors and aliases are not supported.")
                if getattr(event, "tag", None) not in allowed_tags | {None}:
                    raise ConfigError("UNSUPPORTED_YAML", "Custom or unsafe YAML tags are not supported.")
            data = yaml.load(source)
        except (UnicodeError, self.YAMLError) as exc:
            raise ConfigError("INVALID_YAML", f"Cannot parse config.yaml: {exc}") from exc
        prefix = ""
        if data is None and all(not line.strip() or line.lstrip().startswith("#") for line in source.splitlines()):
            data = self.CommentedMap()
            prefix = source
        if not isinstance(data, dict):
            raise ConfigError("INVALID_YAML", "config.yaml must contain a mapping or be empty.")
        return Snapshot(content, data, plain(data), mode, prefix)

    @contextmanager
    def directory(self, create=False):
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        workspace_fd = os.open(self.workspace, flags)
        directory_fd = None
        try:
            if create:
                try:
                    os.mkdir(".talyx", 0o700, dir_fd=workspace_fd)
                except FileExistsError:
                    pass
            try:
                directory_fd = os.open(".talyx", flags, dir_fd=workspace_fd)
            except FileNotFoundError:
                if create:
                    raise
            except OSError as exc:
                raise ConfigError("UNSAFE_CONFIG_PATH", ".talyx must be a real directory, never a symlink.") from exc
            yield directory_fd
        finally:
            if directory_fd is not None:
                os.close(directory_fd)
            os.close(workspace_fd)

    def read(self, directory_fd):
        if directory_fd is None:
            return self.parse(None, None)
        try:
            fd = os.open(CONFIG_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
        except FileNotFoundError:
            return self.parse(None, None)
        except OSError as exc:
            raise ConfigError("UNSAFE_CONFIG_PATH", "config.yaml must be a regular file, never a symlink.") from exc
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode):
                raise ConfigError("UNSAFE_CONFIG_PATH", "config.yaml must be a regular file.")
            content = stream.read()
        return self.parse(content, stat.S_IMODE(info.st_mode))

    def project_known(self, value, schema, parts=()):
        """Report existing extensions separately; validate every recognized value."""
        if "$ref" in schema:
            ref = schema["$ref"]
            if not ref.startswith("#/"):
                raise ConfigError("INVALID_SCHEMA", "Only local schema references are supported.")
            resolved = self.schema
            for part in ref[2:].split("/"):
                resolved = resolved[part.replace("~1", "/").replace("~0", "~")]
            schema = resolved
        unknown = []
        if isinstance(value, dict) and schema.get("type") == "object":
            result = {}
            properties = schema.get("properties", {})
            additional = schema.get("additionalProperties", True)
            for key, item in value.items():
                child = properties.get(key)
                if child is None and additional is False:
                    unknown.append({"path": pointer((*parts, key)), "value": item, "validation": "unvalidated"})
                    continue
                child = child if child is not None else (additional if isinstance(additional, dict) else {})
                result[key], nested = self.project_known(item, child, (*parts, key))
                unknown.extend(nested)
            return result, unknown
        if isinstance(value, list) and schema.get("type") == "array":
            result = []
            for index, item in enumerate(value):
                projected, nested = self.project_known(item, schema.get("items", {}), (*parts, index))
                result.append(projected)
                unknown.extend(nested)
            return result, unknown
        return value, unknown

    def check_schema(self, value, schema, code):
        errors = sorted(self.Validator(schema).iter_errors(value), key=lambda error: str(list(error.absolute_path)))
        if errors:
            raise ConfigError(code, "Configuration does not match the schema.", errors=[
                {"path": pointer(error.absolute_path), "message": error.message} for error in errors
            ])

    def check_paths(self, values):
        for index, destination in enumerate(values.get("destination", [])):
            if destination.get("kind") != "folder":
                continue
            target = destination["to"]
            path = Path(target)
            if not target.strip() or path.is_absolute() or PureWindowsPath(target).drive or "\\" in target or ".." in path.parts:
                raise ConfigError("UNSAFE_DESTINATION", "Folder destinations must be relative paths within the workspace.", path=f"/destination/{index}/to")
            try:
                (self.workspace / path).resolve().relative_to(self.workspace)
            except (ValueError, OSError, RuntimeError) as exc:
                raise ConfigError("UNSAFE_DESTINATION", "Folder destination escapes the workspace or has an invalid symlink.", path=f"/destination/{index}/to") from exc

    def validate(self, values):
        known, unknown = self.project_known(values, self.schema)
        self.check_schema(known, self.schema, "INVALID_EXISTING_CONFIG")
        self.check_paths(known)
        defaults = {key: copy.deepcopy(schema["default"]) for key, schema in self.fields.items() if key not in values and "default" in schema}
        self.check_paths({**defaults, **known})
        return unknown, defaults

    def receipt(self, operation, snapshot, **extra):
        unknown, defaults = self.validate(snapshot.values)
        return {
            "ok": True,
            "operation": operation,
            "schema_version": SCHEMA_VERSION,
            "config_path": str(self.config_path),
            "sha256": digest(snapshot.content),
            "current_values": snapshot.values,
            "effective_defaults": defaults,
            "unknown_fields": unknown,
            "validation_scope": "structural_only",
            "validation_note": VALIDATION_NOTE,
            **extra,
        }

    def request(self, path):
        request = read_json(Path(path))
        nonempty = {"type": "string", "minLength": 1, "pattern": "\\S"}
        field_names = {"type": "string", "enum": list(self.fields)}
        contract = {
            "type": "object", "additionalProperties": False,
            "required": ["schema_version", "base_sha256", "changes", "evidence", "replacements", "unresolved"],
            "properties": {
                "schema_version": {"type": "integer", "const": SCHEMA_VERSION},
                "base_sha256": {"oneOf": [{"type": "null"}, {"type": "string", "pattern": "^[a-f0-9]{64}$"}]},
                "changes": self.schema,
                "evidence": {"type": "object", "additionalProperties": {
                    "type": "object", "additionalProperties": False,
                    "required": ["kind", "reference", "quote"],
                    "properties": {"kind": {"enum": ["user", "document"]}, "reference": nonempty, "quote": nonempty},
                }},
                "replacements": {"type": "array", "items": field_names, "uniqueItems": True},
                "unresolved": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["question_id", "fields", "reason"],
                    "properties": {"question_id": nonempty, "fields": {"type": "array", "items": field_names, "minItems": 1, "uniqueItems": True}, "reason": nonempty},
                }},
            },
        }
        self.check_schema(request, contract, "INVALID_REQUEST")
        if set(request["evidence"]) != set(request["changes"]):
            raise ConfigError("MISSING_EVIDENCE", "Provide exactly one evidence record for every changed field.")
        if not set(request["replacements"]).issubset(request["changes"]):
            raise ConfigError("INVALID_REQUEST", "Replacement fields must also appear in changes.")
        if any(value is None for value in request["changes"].values()):
            raise ConfigError("INVALID_REQUEST", "Null cannot delete configuration fields.")
        if request["unresolved"]:
            raise ConfigError("UNRESOLVED_QUESTIONS", "Resolve every question before applying any configuration changes.", unresolved=request["unresolved"])
        self.check_paths(request["changes"])
        return request

    def prepare(self, snapshot, request):
        if request["base_sha256"] != digest(snapshot.content):
            raise ConfigError("STALE_BASE", "config.yaml changed since inspection. Inspect it again and rebuild the request.", current_sha256=digest(snapshot.content))
        unknown, _ = self.validate(snapshot.values)
        changes = request["changes"]
        modified = [key for key, value in changes.items() if key not in snapshot.values or snapshot.values[key] != value]
        for key in modified:
            if any(item["path"].startswith(pointer((key,)) + "/") for item in unknown):
                raise ConfigError("UNKNOWN_DATA_LOSS", "Replacing this field would discard existing unvalidated nested data. Preserve it and resolve its contract before replacing the field.", field=key)
            if key in snapshot.data and has_internal_comments(snapshot.data[key]):
                raise ConfigError(
                    "COMMENT_PRESERVATION_REQUIRED",
                    "config unchanged; the current helper cannot safely update this commented structure. Keep the existing field and arrange a human edit that preserves its comments, then inspect again.",
                    field=key,
                )
            if key in snapshot.values and snapshot.values[key] not in (None, "", [], {}):
                if key not in request["replacements"] or request["evidence"][key]["kind"] != "user":
                    raise ConfigError("REPLACEMENT_AUTHORITY_REQUIRED", "Replacing an existing nonempty value requires its field in replacements and user evidence explicitly authorizing that replacement.", field=key)
        if not modified and snapshot.content is not None:
            return snapshot, modified
        data = copy.deepcopy(snapshot.data)
        for key in modified:
            data[key] = changes[key]
        stream = io.StringIO()
        if snapshot.prefix:
            stream.write(snapshot.prefix)
            if not snapshot.prefix.endswith("\n"):
                stream.write("\n")
        self.yaml().dump(data, stream)
        result = self.parse(stream.getvalue().encode("utf-8"), snapshot.mode)
        expected = {**snapshot.values, **changes}
        if result.values != expected:
            raise ConfigError("ROUNDTRIP_MISMATCH", "YAML serialization changed the proposed values. Original preserved.")
        self.validate(result.values)
        return result, modified

    def lock(self, directory_fd):
        """Hold a kernel lock until directory() closes this fd, even after errors.

        A fresh open tests local lock exclusion on this filesystem. No lock file
        needs deleting, and process exit releases the lock after interruption.
        """
        import fcntl

        contention = {errno.EAGAIN, errno.EWOULDBLOCK, errno.EACCES}
        try:
            fcntl.flock(directory_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            if exc.errno in contention:
                raise ConfigError(
                    "CONFIG_LOCKED", "Cannot acquire the configuration lock; another update may be running.",
                    recovery="Wait for the other update to finish, then inspect config.yaml and retry. Do not delete lock files.",
                ) from exc
            raise ConfigError(
                "LOCK_UNSUPPORTED", "This workspace does not support the required directory locking. Configuration was not changed.",
                recovery="Use a local workspace with working advisory locks and atomic file replacement.",
            ) from exc
        probe_fd = os.open(".", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd)
        try:
            try:
                fcntl.flock(probe_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                if exc.errno not in contention:
                    raise ConfigError("LOCK_UNSUPPORTED", "Could not verify exclusive workspace locking. Configuration was not changed.") from exc
            else:
                raise ConfigError("LOCK_UNSUPPORTED", "The workspace did not enforce exclusive locking. Configuration was not changed.")
        finally:
            os.close(probe_fd)
        self.check_legacy_lock(directory_fd)

    def check_legacy_lock(self, directory_fd):
        try:
            os.stat(LOCK_NAME, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise ConfigError(
            "CONFIG_LOCKED", "A lock from an older helper exists. It has been left untouched.",
            lock_path=str(self.config_dir / LOCK_NAME),
            recovery="Confirm no helper is running. Have the existing legacy lock reviewed before removing it, then inspect config.yaml and retry with the updated helper.",
        )

    def check_directory(self, directory_fd):
        current = self.config_dir.lstat()
        opened = os.fstat(directory_fd)
        if not stat.S_ISDIR(current.st_mode) or (current.st_dev, current.st_ino) != (opened.st_dev, opened.st_ino):
            raise ConfigError("CONCURRENT_CHANGE", ".talyx changed during the update. Inspect the workspace again.")

    def write(self, directory_fd, original, proposed):
        temporary = f".config.yaml.{uuid.uuid4().hex}.tmp"
        temporary_pending = False
        replaced = False
        try:
            fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600, dir_fd=directory_fd)
            temporary_pending = True
            with os.fdopen(fd, "wb") as stream:
                os.fchmod(stream.fileno(), original.mode if original.mode is not None else 0o600)
                stream.write(proposed.content)
                stream.flush()
                os.fsync(stream.fileno())
            self.check_directory(directory_fd)
            latest = self.read(directory_fd)
            if digest(latest.content) != digest(original.content) or latest.mode != original.mode:
                raise ConfigError("CONCURRENT_CHANGE", "config.yaml changed while preparing the update. Original external change preserved; inspect again.")
            self.check_legacy_lock(directory_fd)
            # The lock coordinates this helper. External writers do not participate;
            # the final digest check cannot eliminate their check/replace race.
            os.replace(temporary, CONFIG_NAME, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
            temporary_pending = False
            replaced = True
            os.fsync(directory_fd)
            self.check_directory(directory_fd)
            committed = self.read(directory_fd)
            if committed.content != proposed.content or committed.values != proposed.values:
                raise ConfigError("READBACK_MISMATCH", "Committed configuration failed read-back verification. Inspect the current file before retrying.", write_may_have_committed=True)
            self.validate(committed.values)
            return committed
        except (Exception, KeyboardInterrupt) as exc:
            failure = exc if isinstance(exc, ConfigError) else ConfigError(
                "INTERRUPTED" if isinstance(exc, KeyboardInterrupt) else "IO_ERROR",
                str(exc) or "Update interrupted.",
            )
            failure.details.setdefault("write_may_have_committed", replaced)
            if temporary_pending:
                try:
                    os.unlink(temporary, dir_fd=directory_fd)
                except FileNotFoundError:
                    pass
                except OSError as cleanup_error:
                    failure.details["cleanup"] = {
                        "temporary_path": str(self.config_dir / temporary),
                        "message": str(cleanup_error),
                        "recovery": "An uncommitted temporary file remains. It is not a lock and will not block a new request; inspect config.yaml before retrying.",
                    }
            if failure is exc:
                raise
            raise failure from exc

    def apply(self, request_path, dry_run):
        request = self.request(request_path)
        with self.directory() as directory_fd:
            original = self.read(directory_fd)
        proposed, modified = self.prepare(original, request)
        if dry_run or (not modified and original.content is not None):
            return self.receipt("apply", proposed, status="dry_run" if dry_run else "unchanged", written=False,
                                base_sha256=digest(original.content), changed_fields=modified)
        committed = None
        try:
            with self.directory(create=True) as directory_fd:
                self.lock(directory_fd)
                self.check_directory(directory_fd)
                current = self.read(directory_fd)
                if digest(current.content) != digest(original.content):
                    raise ConfigError("CONCURRENT_CHANGE", "config.yaml changed before the update lock was acquired. Inspect again.")
                committed = self.write(directory_fd, current, proposed)
        except OSError as exc:
            raise ConfigError("IO_ERROR", str(exc), write_may_have_committed=committed is not None) from exc
        return self.receipt("apply", committed, status="written", written=True,
                            base_sha256=digest(original.content), changed_fields=modified,
                            concurrency_note="Updated helpers sharing this directory use an advisory lock. Older helpers and external writers do not participate; digest checks detect observed changes but cannot eliminate their final replacement race.")


def main(argv=None):
    try:
        if sys.version_info < (3, 10):
            raise ConfigError("UNSUPPORTED_PYTHON", "Use Python 3.10 or newer.")
        parser = Parser(description=__doc__)
        commands = parser.add_subparsers(dest="command", required=True, parser_class=Parser)
        for name in ("inspect", "validate", "apply"):
            command = commands.add_parser(name)
            command.add_argument("--workspace", required=True)
            if name == "apply":
                command.add_argument("--request", required=True)
                command.add_argument("--dry-run", action="store_true")
        args = parser.parse_args(argv)
        helper = ConfigHelper(args.workspace)
        if args.command == "apply":
            receipt = helper.apply(args.request, args.dry_run)
        else:
            with helper.directory() as directory_fd:
                snapshot = helper.read(directory_fd)
            receipt = helper.receipt(args.command, snapshot, status="valid" if snapshot.content is not None else "absent")
        emit(receipt)
        return 0
    except ConfigError as exc:
        emit({"ok": False, "error": {"code": exc.code, "message": str(exc), **exc.details}, "validation_scope": "structural_only"})
        return 1
    except (OSError, ValueError) as exc:
        emit({"ok": False, "error": {"code": "IO_ERROR", "message": str(exc), "recovery": "Inspect the current configuration before retrying; an I/O failure may occur after replacement."}})
        return 1
    except KeyboardInterrupt:
        emit({"ok": False, "error": {"code": "INTERRUPTED", "message": "Update interrupted. Inspect config.yaml before retrying."}})
        return 130
    except RecursionError:
        emit({"ok": False, "error": {"code": "INPUT_TOO_DEEP", "message": "Input nesting exceeds the supported limit. Inspect config.yaml before retrying."}})
        return 1


if __name__ == "__main__":
    sys.exit(main())
