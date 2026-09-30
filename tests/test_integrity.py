"""End-to-end contract checks for the optional stdlib integrity helper."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "verify" / "integrity.py"


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "project"
        self.root.mkdir()
        self.source = self.root / "source.txt"
        self.source.write_text("original\n")
        self.manifest = self.base / "baseline.json"

    def run_cli(self, operation, *extra, root=None, manifest=None, expected=None):
        command = [sys.executable, str(HELPER), operation, "--root", str(root or self.root),
                   "--manifest", str(manifest or self.manifest)]
        if operation == "check":
            command.extend(["--expected-manifest-sha256", expected or self.digest])
        command.extend(extra)
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def snapshot(self, *extra):
        result = self.run_cli("snapshot", *extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.digest = output["manifest_sha256"]
        self.assertEqual(self.digest, hashlib.sha256(self.manifest.read_bytes()).hexdigest())
        return output

    def test_unchanged_passes_without_writing_project_or_manifest(self):
        output = self.snapshot()
        before = self.manifest.read_bytes()
        result = self.run_cli("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"status": "UNCHANGED", "protected_files": 1})
        self.assertEqual(output["protected_files"], 1)
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertEqual(list(self.root.iterdir()), [self.source])
        self.assertEqual(self.source.read_text(), "original\n")

    def test_edit_addition_and_deletion_are_reported_in_sorted_order(self):
        (self.root / "removed.txt").write_text("remove me")
        self.snapshot()
        (self.root / "removed.txt").unlink()
        self.source.write_text("edited")
        (self.root / "z-untracked.txt").write_text("z")
        (self.root / "a-untracked.txt").write_text("a")
        result = self.run_cli("check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "status": "CHANGED", "added": ["a-untracked.txt", "z-untracked.txt"],
            "deleted": ["removed.txt"], "changed": ["source.txt"]})

    def test_explicit_cache_subtree_and_git_are_excluded(self):
        self.snapshot("--exclude", "cache")
        for name in ("cache", ".git"):
            (self.root / name).mkdir()
            (self.root / name / "new.txt").write_text("ignored")
        self.assertEqual(self.run_cli("check").returncode, 0)
        (self.root / "cache-other.txt").write_text("protected")
        result = self.run_cli("check")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["added"], ["cache-other.txt"])

    def test_check_cannot_add_exclusions(self):
        self.snapshot()
        result = self.run_cli("check", "--exclude", "source.txt")
        self.assertEqual(result.returncode, 2)

    def test_modified_manifest_is_rejected_even_if_it_hides_changes(self):
        self.snapshot()
        manifest = json.loads(self.manifest.read_text())
        manifest["exclusions"].append("source.txt")
        manifest["hashes"] = {}
        self.manifest.write_text(json.dumps(manifest))
        self.source.write_text("tampered")
        result = self.run_cli("check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("manifest digest mismatch", result.stderr)

    def test_missing_manifest_fails_closed(self):
        result = self.run_cli("check", expected="0" * 64)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["status"], "ERROR")

    def test_invalid_json_and_schema_fail_even_with_matching_digest(self):
        cases = [b"not JSON", b"[]", b'{"version":1,"version":1}',
                 json.dumps({"version": 1, "root": str(self.root),
                             "exclusions": [".git", "../outside"], "hashes": {}}).encode()]
        for data in cases:
            with self.subTest(data=data):
                self.manifest.write_bytes(data)
                result = self.run_cli("check", expected=hashlib.sha256(data).hexdigest())
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stderr)["status"], "ERROR")

    def test_manifest_must_be_outside_root_even_if_excluded(self):
        for name in ("baseline.json", ".git/baseline.json"):
            with self.subTest(name=name):
                result = self.run_cli("snapshot", manifest=self.root / name)
                self.assertEqual(result.returncode, 2)
                self.assertIn("outside the protected root", result.stderr)

    def test_invalid_exclusions_fail_without_writing_a_manifest(self):
        for value in ("", ".", "..", "../outside", "nested/../outside", "/absolute", "C:/absolute",
                      "a\\b", "*.py", "cache?", "[abc]"):
            with self.subTest(value=value):
                result = self.run_cli("snapshot", "--exclude", value)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.manifest.exists())

    def test_root_mismatch_fails(self):
        self.snapshot()
        other_root = self.base / "other"
        other_root.mkdir()
        result = self.run_cli("check", root=other_root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("root does not match", result.stderr)

    def test_invalid_roots_fail(self):
        for root in (self.base / "absent", self.source):
            with self.subTest(root=root):
                self.assertEqual(self.run_cli("snapshot", root=root).returncode, 2)

    def test_symlink_root_fails(self):
        linked = self.base / "linked-root"
        linked.symlink_to(self.root, target_is_directory=True)
        result = self.run_cli("snapshot", root=linked)
        self.assertEqual(result.returncode, 2)
        self.assertIn("root must not be a symlink", result.stderr)

    def test_protected_file_symlink_fails_without_reading_target(self):
        (self.root / "linked.txt").symlink_to(self.base / "missing-target")
        result = self.run_cli("snapshot")
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", result.stderr)
        self.assertFalse(self.manifest.exists())

    def test_added_directory_symlink_invalidates_check(self):
        self.snapshot()
        (self.root / "linked-directory").symlink_to(self.base, target_is_directory=True)
        result = self.run_cli("check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", result.stderr)

    def test_manifest_symlink_fails(self):
        self.snapshot()
        linked = self.base / "linked-manifest.json"
        linked.symlink_to(self.manifest)
        result = self.run_cli("check", manifest=linked)
        self.assertEqual(result.returncode, 2)
        self.assertIn("manifest must not be a symlink", result.stderr)

    def test_snapshot_never_overwrites_existing_manifest(self):
        self.snapshot()
        original = self.manifest.read_bytes()
        self.source.write_text("edited")
        result = self.run_cli("snapshot")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.manifest.read_bytes(), original)

    def test_manifest_bytes_are_deterministic(self):
        (self.root / "z.txt").write_text("z")
        self.snapshot("--exclude", "cache", "--exclude", "cache")
        other_manifest = self.base / "other-baseline.json"
        result = self.run_cli("snapshot", "--exclude", "cache", manifest=other_manifest)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.manifest.read_bytes(), other_manifest.read_bytes())

    def test_check_requires_external_digest(self):
        self.snapshot()
        result = subprocess.run([sys.executable, str(HELPER), "check", "--root", str(self.root),
                                 "--manifest", str(self.manifest)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--expected-manifest-sha256", result.stderr)

    def test_invalid_external_digest_fails(self):
        self.snapshot()
        result = self.run_cli("check", expected="not-a-digest")
        self.assertEqual(result.returncode, 2)
        self.assertIn("64 lowercase hexadecimal", result.stderr)


if __name__ == "__main__":
    unittest.main()
