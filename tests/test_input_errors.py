# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""All validator CLIs distinguish unreadable input from a model defect."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("mkl-uml-domain-modeler", "validate_domain_puml.py", ()),
    ("mkl-uml-use-case-diagram", "validate_use_case_puml.py", ()),
    ("mkl-use-case-specifier", "validate_use_case_spec.py", ()),
    ("mkl-uml-robustness-diagram", "validate_robustness_puml.py", ()),
    ("mkl-pdr-review", "validate_pdr.py", ("--robustez",)),
    ("mkl-uml-sequence-diagram", "validate_sequence_puml.py", ("--secuencia",)),
    ("mkl-uml-design-class-model", "validate_design_class_puml.py", ("--clases",)),
    ("mkl-cdr-review", "validate_cdr.py", ("--clases",)),
)


class InputErrors(unittest.TestCase):
    def check_all(self, bad_input):
        for skill, filename, flags in CASES:
            with self.subTest(skill=skill):
                args = [sys.executable, str(ROOT / "skills" / skill / "scripts" / filename),
                        *flags, str(bad_input)]
                if skill == "mkl-cdr-review":
                    args.extend(["--secuencia", str(ROOT / "tests/fixtures/pipeline/secuencia.puml")])
                result = subprocess.run(args, capture_output=True, text=True,
                                        encoding="utf-8", timeout=20)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                self.assertIn(str(bad_input), result.stdout + result.stderr)

    def test_invalid_utf8_is_an_input_error_for_every_validator(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid-input.puml"
            path.write_bytes(b"\xff\xfe\x80")
            self.check_all(path)

    def test_directory_is_an_input_error_for_every_validator(self):
        with tempfile.TemporaryDirectory() as directory:
            self.check_all(Path(directory))


if __name__ == "__main__":
    unittest.main()
