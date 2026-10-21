#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. mkl standalone distribution tests.
"""Archive and directory installs must carry the same standalone payload."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
import zipfile

from tools import install_skills, package_skill, skill_payload

ROOT = Path(__file__).resolve().parents[1]
SKILL = "mkl-uml-domain-modeler"


class DistributionTests(unittest.TestCase):
    def test_source_skill_folders_include_license_and_upstream_notice(self):
        for name in skill_payload.skill_names():
            for filename in ("LICENSE", "NOTICE"):
                with self.subTest(skill=name, notice=filename):
                    source = ROOT / "skills" / name / filename
                    self.assertTrue(source.is_file(), str(source))
                    self.assertEqual(source.read_bytes(), (ROOT / filename).read_bytes())

    def test_source_skill_links_work_when_copied_without_repository_root(self):
        for name in skill_payload.skill_names():
            self.assert_markdown_links_resolve(ROOT / "skills" / name)

    def assert_markdown_links_resolve(self, skill_dir):
        for document in skill_dir.rglob("*.md"):
            text = document.read_text(encoding="utf-8")
            for destination in re.findall(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)", text):
                url = urlsplit(destination.strip("<>"))
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (document.parent / unquote(url.path)).resolve()
                with self.subTest(skill=skill_dir.name, document=str(document), link=destination):
                    self.assertTrue(target.is_relative_to(skill_dir.resolve()), destination)
                    self.assertTrue(target.exists(), destination)

    def test_archive_and_directory_have_identical_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            installed = install_skills.install(target / "installed", [SKILL])[0]
            with patch.object(package_skill, "DIST", target / "archives"):
                archive = package_skill.package(ROOT / "skills" / SKILL)
            with zipfile.ZipFile(archive) as zipped:
                archive_files = {name.split("/", 1)[1]: zipped.read(name) for name in zipped.namelist()}
                zipped.extractall(target / "extracted")
            self.assert_markdown_links_resolve(target / "extracted" / SKILL)
            directory_files = {path.relative_to(installed).as_posix(): path.read_bytes()
                               for path in installed.rglob("*") if path.is_file()}
            self.assertEqual(archive_files, directory_files)
            for filename in ("LICENSE", "NOTICE"):
                self.assertEqual(directory_files[filename], (ROOT / filename).read_bytes())
            self.assertIn("package-docs/README.md", directory_files)
            for filename in ("BIBLIOGRAPHY.md", "MKL_METHODOLOGY.md", "INSTALLATION.md"):
                self.assertIn("package-docs/docs/" + filename, directory_files)
            self.assertFalse(any("__pycache__" in name or name.endswith((".pyc", ".DS_Store"))
                                 for name in directory_files))

    def test_all_installed_markdown_links_resolve_within_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = install_skills.install(Path(directory))[0:]
            self.assertEqual(len(installed), 8)
            for skill_dir in installed:
                self.assert_markdown_links_resolve(skill_dir)

    def test_existing_target_preserved_and_all_install_is_preflighted(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            occupied = target / "mkl-uml-sequence-diagram"
            occupied.mkdir()
            sentinel = occupied / "keep.txt"
            sentinel.write_text("existing content")
            with self.assertRaises(FileExistsError):
                install_skills.install(target)
            self.assertEqual(sentinel.read_text(), "existing content")
            self.assertEqual(sorted(path.name for path in target.iterdir()), [occupied.name])

    def test_reject_invalid_names(self):
        for name in ("../mkl-uml-domain-modeler", "/tmp/outside", "..", "skills/mkl-uml-domain-modeler", "unknown-skill"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                skill_payload.build_payload(name)

    def test_symlink_is_rejected_without_reading_external_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "safe-name"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# safe-name\n")
            external = root / "outside.txt"
            external.write_text("private outside content")
            (skill / "escape.txt").symlink_to(external)
            with self.assertRaises(ValueError):
                skill_payload.build_payload("safe-name", root=root)

    def test_documentation_symlink_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            skill = root / "skills" / "safe-name"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# safe-name\n")
            for name in ("LICENSE", "NOTICE"):
                (root / name).write_text("notice")
            outside = Path(directory) / "outside"
            outside.mkdir()
            (outside / "INSTALLATION.md").write_text("outside document")
            (root / "docs").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                skill_payload.build_payload("safe-name", root=root)

    def test_packaging_cli_rejects_traversal_name(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "package_skill.py"), "../mkl-uml-domain-modeler"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Invalid skill name", result.stderr)

    def test_operating_contract_is_bundled_when_present(self):
        # Work against a synthetic root so this stays true before/after authoring
        # the repository's contract and proves payload reads docs at build time.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "safe-name"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# safe-name\n")
            (skill / "README.md").write_text("[contract](../../docs/OPERATING_CONTRACT.md)\n")
            for name in ("LICENSE", "NOTICE"):
                (root / name).write_text("notice")
            (root / "docs").mkdir()
            contract = root / "docs" / "OPERATING_CONTRACT.md"
            contract.write_bytes(b"# Contract version 1\n")
            first = skill_payload.build_payload("safe-name", root=root)
            contract.write_bytes(b"# Contract version 2\n")
            second = skill_payload.build_payload("safe-name", root=root)
            self.assertEqual(first["package-docs/docs/OPERATING_CONTRACT.md"], b"# Contract version 1\n")
            self.assertEqual(second["package-docs/docs/OPERATING_CONTRACT.md"], b"# Contract version 2\n")
            self.assertIn(b"package-docs/docs/OPERATING_CONTRACT.md", second["README.md"])

    def test_cli_requires_destination_and_rejects_existing_target(self):
        script = ROOT / "tools" / "install_skills.py"
        result = subprocess.run([sys.executable, str(script), SKILL], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--destination", result.stderr)
        with tempfile.TemporaryDirectory() as directory:
            args = [sys.executable, str(script), "--destination", directory, SKILL]
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(directory) / SKILL / "SKILL.md").is_file())
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
