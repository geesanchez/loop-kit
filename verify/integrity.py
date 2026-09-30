#!/usr/bin/env python3
"""Detect protected-file changes against an externally recorded manifest digest.

This is a before/after check, not a filesystem sandbox or protection against
concurrent writes. Keep the manifest and its recorded digest outside the
verifier's control. Python 3.8+; standard library only.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import sys


class IntegrityError(Exception):
    """Invalid input or an incomplete integrity check."""


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise IntegrityError("paths must be nonempty relative paths using '/' separators")
    path = PurePosixPath(value)
    if (path.is_absolute() or PureWindowsPath(value).drive
            or any(part in ("", ".", "..") for part in value.split("/"))):
        raise IntegrityError("invalid relative path: " + repr(value))
    return value


def exclusion_path(value):
    relative_path(value)
    if any(character in value for character in "*?[]"):
        raise IntegrityError("exclusions must be exact paths, not wildcard patterns: " + repr(value))
    return value


def excluded(name, exclusions):
    return any(name == item or name.startswith(item + "/") for item in exclusions)


def contains(root, path):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_paths(root_value, manifest_value):
    root_input = Path(root_value).expanduser()
    if root_input.is_symlink():
        raise IntegrityError("protected root must not be a symlink")
    root = root_input.resolve(strict=True)
    if not root.is_dir():
        raise IntegrityError("protected root must be an existing directory")
    # Resolve parent links, but refuse a symlink at the manifest itself.
    manifest_input = Path(manifest_value).expanduser()
    if manifest_input.is_symlink():
        raise IntegrityError("manifest must not be a symlink")
    manifest = manifest_input.resolve(strict=False)
    if contains(root, manifest):
        raise IntegrityError("manifest must be outside the protected root, even when excluded")
    return root, manifest


def signature(metadata):
    return (metadata.st_dev, metadata.st_ino, metadata.st_size,
            metadata.st_mtime_ns, metadata.st_ctime_ns)


def read_regular(path, digest_only=False):
    """Read a regular file without following a final-component symlink."""
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise IntegrityError("not a regular file (symlinks are unsupported): " + str(path))
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(str(path), flags)
    with os.fdopen(descriptor, "rb") as stream:
        opened = os.fstat(stream.fileno())
        if signature(before) != signature(opened) or not stat.S_ISREG(opened.st_mode):
            raise IntegrityError("file changed while opening: " + str(path))
        if digest_only:
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
            data = digest.hexdigest()
        else:
            data = stream.read()
        after = os.fstat(stream.fileno())
    if signature(opened) != signature(after) or signature(after) != signature(path.lstat()):
        raise IntegrityError("file changed while reading: " + str(path))
    return data


def hashes(root, exclusions):
    result = {}

    def visit(directory, prefix):
        with os.scandir(directory) as entries:
            children = sorted(entries, key=lambda item: item.name)
        for entry in children:
            name = prefix + entry.name
            if excluded(name, exclusions):
                continue
            relative_path(name)
            if entry.is_symlink():
                raise IntegrityError("protected symlink is unsupported: " + name)
            if entry.is_dir(follow_symlinks=False):
                visit(Path(entry.path), name + "/")
            elif entry.is_file(follow_symlinks=False):
                result[name] = read_regular(Path(entry.path), digest_only=True)
            else:
                raise IntegrityError("protected entry is not a regular file or directory: " + name)

    visit(root, "")
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntegrityError("duplicate manifest key: " + repr(key))
        result[key] = value
    return result


def valid_digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def load_manifest(path, expected_digest, root):
    if not valid_digest(expected_digest):
        raise IntegrityError("expected manifest digest must be 64 lowercase hexadecimal characters")
    data = read_regular(path)
    if hashlib.sha256(data).hexdigest() != expected_digest:
        raise IntegrityError("manifest digest mismatch; the baseline is not trusted")
    try:
        manifest = json.loads(data.decode("utf-8"), object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise IntegrityError("invalid manifest JSON: " + str(error)) from error
    if not isinstance(manifest, dict) or set(manifest) != {"version", "root", "exclusions", "hashes"}:
        raise IntegrityError("invalid manifest fields")
    if type(manifest["version"]) is not int or manifest["version"] != 1:
        raise IntegrityError("unsupported manifest version")
    if manifest["root"] != str(root):
        raise IntegrityError("manifest root does not match the protected root")
    exclusions = manifest["exclusions"]
    if not isinstance(exclusions, list):
        raise IntegrityError("invalid manifest exclusions")
    for value in exclusions:
        exclusion_path(value)
    if exclusions != sorted(set(exclusions)) or ".git" not in exclusions:
        raise IntegrityError("manifest exclusions must be sorted, unique, and include .git")
    if not isinstance(manifest["hashes"], dict):
        raise IntegrityError("invalid manifest hashes")
    for name, digest in manifest["hashes"].items():
        relative_path(name)
        if excluded(name, exclusions) or not valid_digest(digest):
            raise IntegrityError("invalid protected-file entry: " + repr(name))
    return manifest


def emit(value, stream=sys.stdout):
    print(json.dumps(value, sort_keys=True), file=stream)


def snapshot(args, root, manifest_path):
    exclusions = sorted(set([".git"] + [exclusion_path(item) for item in args.exclude]))
    manifest = {"version": 1, "root": str(root), "exclusions": exclusions,
                "hashes": hashes(root, exclusions)}
    data = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    # Exclusive creation prevents silently replacing an existing baseline.
    with manifest_path.open("xb") as stream:
        stream.write(data)
    emit({"status": "SNAPSHOT", "manifest": str(manifest_path),
          "manifest_sha256": hashlib.sha256(data).hexdigest(),
          "protected_files": len(manifest["hashes"])})
    return 0


def check(args, root, manifest_path):
    manifest = load_manifest(manifest_path, args.expected_manifest_sha256, root)
    before = manifest["hashes"]
    after = hashes(root, manifest["exclusions"])
    added = sorted(set(after) - set(before))
    deleted = sorted(set(before) - set(after))
    changed = sorted(name for name in set(before) & set(after) if before[name] != after[name])
    if added or deleted or changed:
        emit({"status": "CHANGED", "added": added, "deleted": deleted, "changed": changed})
        return 1
    emit({"status": "UNCHANGED", "protected_files": len(after)})
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    operations = parser.add_subparsers(dest="operation", required=True)
    capture = operations.add_parser("snapshot", help="create a new external baseline; never overwrite")
    compare = operations.add_parser("check", help="compare against the externally recorded baseline digest")
    for command in (capture, compare):
        command.add_argument("--root", required=True, help="protected directory (all regular files)")
        command.add_argument("--manifest", required=True, help="manifest path outside the protected root")
    capture.add_argument("--exclude", action="append", default=[], metavar="RELATIVE_PATH",
                         help="exact relative path/subtree; repeatable; .git is always excluded; wildcards rejected")
    compare.add_argument("--expected-manifest-sha256", required=True,
                         help="digest recorded at snapshot time outside verifier control")
    args = parser.parse_args(argv)
    try:
        root, manifest = resolve_paths(args.root, args.manifest)
        return snapshot(args, root, manifest) if args.operation == "snapshot" else check(args, root, manifest)
    except (IntegrityError, OSError, ValueError, RuntimeError) as error:
        emit({"status": "ERROR", "error": str(error)}, stream=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
