"""The candidate validator replay retains exact reviewed runtime verification."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "examples/order-pricing/scripts/verify.py"


class ReferenceRuntimeTest(unittest.TestCase):
    def test_drift_requires_candidate_mode_and_records_the_bundled_helper(self):
        spec = importlib.util.spec_from_file_location("reference_verify", VERIFY)
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "skills/sample/scripts"
            scripts.mkdir(parents=True)
            validator = scripts / "validate.py"
            validator.write_text("# reviewed\n", encoding="utf-8")
            expected = {validator.relative_to(root).as_posix(): verifier.text_sha256(validator)}
            self.assertTrue(verifier.inspect_skill_runtime(root, expected)["matches_reviewed_hashes"])

            validator.write_text("# changed\n", encoding="utf-8")
            helper = scripts / "helper.py"
            helper.write_text("# bundled helper\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "differs from the reviewed baseline"):
                verifier.inspect_skill_runtime(root, expected)
            candidate = verifier.inspect_skill_runtime(root, expected, candidate=True)

            self.assertEqual(candidate["mode"], "candidate")
            self.assertFalse(candidate["matches_reviewed_hashes"])
            self.assertEqual(candidate["sha256"][helper.relative_to(root).as_posix()],
                             verifier.text_sha256(helper))
