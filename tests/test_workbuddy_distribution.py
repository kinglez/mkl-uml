"""WorkBuddy packages retain standalone resources within the platform depth limit."""
from pathlib import Path
import json
import re
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import zipfile

from tools.package_workbuddy_skill import flatten_payload, package
from tools.skill_payload import ROOT, build_payload


class WorkBuddyDistributionTests(unittest.TestCase):
    def test_archive_is_reproducible_and_preserves_resources(self):
        catalog = json.loads((ROOT / "docs/workbuddy/skills.json").read_text(encoding="utf-8"))
        for name in catalog:
            with self.subTest(skill=name):
                self.check_archive(name)

    def check_archive(self, name):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = package(name, root)
            first = path.read_bytes()
            self.assertEqual(package(name, root).read_bytes(), first)
            source = build_payload(name)
            expected = flatten_payload(source)
            with zipfile.ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
                self.assertTrue(all(len(Path(item).parts) <= 3 for item in archive.namelist()))
                archive.extractall(root / "unpacked")
            skill = (root / "unpacked" / name).resolve()
            for relative, content in expected.items():
                if relative != "SKILL.md":
                    self.assertEqual((skill / relative).read_bytes(), content)
            self.assertEqual((skill / "SKILL.md").read_bytes().split(b"\n---\n", 1)[1],
                             expected["SKILL.md"].split(b"\n---\n", 1)[1])
            self.assertLess(len(first), 3 * 1024 * 1024)
            for document in skill.rglob("*.md"):
                for destination in re.findall(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)", document.read_text(encoding="utf-8")):
                    url = urlsplit(destination.strip("<>"))
                    if url.scheme or url.netloc or not url.path:
                        continue
                    target = (document.parent / unquote(url.path)).resolve()
                    self.assertTrue(target.is_relative_to(skill), destination)
                    self.assertTrue(target.exists(), f"{document}: {destination}")

    def test_flatten_collision_is_rejected(self):
        with self.assertRaises(ValueError):
            flatten_payload({"references/a/b.md": b"one", "references/a__b.md": b"two"})


if __name__ == "__main__":
    unittest.main()
