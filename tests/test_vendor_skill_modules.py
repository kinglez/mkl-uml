from pathlib import Path
import tempfile
import unittest

from tools.sync_skill_modules import MODULES, ROOT, sync_modules


class VendorSkillModulesTests(unittest.TestCase):
    def test_distribution_copies_match_their_owners(self):
        self.assertEqual(sync_modules(ROOT), [])

    def test_read_only_check_and_explicit_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pairs = []
            for module, owner, consumer in MODULES:
                source = root / "skills" / owner / "scripts" / module
                target = root / "skills" / consumer / "scripts" / module
                for path, content in ((source, b"# authoritative\n"), (target, b"# stale\n")):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                pairs.append((source, target))
            expected = [target.relative_to(root) for _, target in pairs]
            self.assertEqual(sync_modules(root), expected)
            self.assertTrue(all(target.read_bytes() == b"# stale\n" for _, target in pairs))
            self.assertEqual(sync_modules(root, write=True), expected)
            self.assertEqual(sync_modules(root), [])
