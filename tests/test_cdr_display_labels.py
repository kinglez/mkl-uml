# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Visible control labels should survive PlantUML display wrapping in CDR."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CDR = ROOT / "skills/mkl-cdr-review/scripts/validate_cdr.py"
PIPELINE = ROOT / "tests/fixtures/pipeline"


class CDRDisplayLabels(unittest.TestCase):
    def run_review(self, label, plan):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            robustness = folder / "robustness.puml"
            robustness.write_text('@startuml\ncontrol "' + label +
                                  '" as RefusalControl\n@enduml\n', encoding="utf-8")
            tests = folder / "test-plan.md"
            tests.write_text(plan, encoding="utf-8")
            command = [sys.executable, "-B", str(CDR), "--clases",
                       str(PIPELINE / "modelo_clases_diseno.puml"), "--secuencia",
                       str(PIPELINE / "secuencia.puml"), "--robustez", str(robustness),
                       "--pruebas", str(tests)]
            result = subprocess.run(command, capture_output=True, text=True,
                                    encoding="utf-8", timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            return result.stdout

    def test_wrapped_control_matches_the_same_visible_test_responsibility(self):
        plan = ("| Case | Stimulus | Observable result |\n"
                "| --- | --- | --- |\n"
                "| CP-01 | Submit an invalid quote request | Refusal reason; no quote |\n")
        for label in (r"Return\nrefusal", r"Return\r\nrefusal"):
            with self.subTest(label=label):
                output = self.run_review(label, plan)
                self.assertNotIn("Controller '", output)
                self.assertIn("NOT FULLY VERIFIED", output)

    def test_wrapping_does_not_cover_an_unrelated_control(self):
        output = self.run_review(r"Render\ninvoice",
                                 "CP-01: Invalid quote returns refusal and no quote.\n")
        self.assertIn("does not appear in the plan evidence", output)

    def test_commented_test_text_does_not_cover_a_wrapped_control(self):
        output = self.run_review(r"Return\nrefusal",
                                 "CP-01: Unrelated smoke case.\n"
                                 "<!-- Return refusal; no quote -->\n")
        self.assertIn("does not appear in the plan evidence", output)


if __name__ == "__main__":
    unittest.main()
