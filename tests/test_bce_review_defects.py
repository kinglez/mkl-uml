# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""BCE link checks distinguish proved violations from missing parser evidence."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ROBUSTNESS = ("mkl-uml-robustness-diagram", "validate_robustness_puml.py", [])
PDR = ("mkl-pdr-review", "validate_pdr.py", ["--robustez"])
MODEL = """@startuml
left to right direction
skinparam linetype ortho
skinparam shadowing false
actor "Reader" as ACT_Reader
boundary "Service Desk" as B_Desk <<interface>> #LightBlue
control C_Book as "Book Item" <<coordination>>
entity "Stored Item" <<catalog>> as E_Item
ACT_Reader -- B_Desk
B_Desk -- C_Book
C_Book -- E_Item
"""


class BCEReviewDefects(unittest.TestCase):
    def cli(self, validator, source, extra=()):
        skill, script, flags = validator
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "model.puml"
            target.write_text(source, encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-I", "-B", str(ROOT / "skills" / skill / "scripts" / script),
                 *flags, str(target), *extra],
                capture_output=True, text=True, encoding="utf-8", timeout=20,
            )

    def test_stereotypes_preserve_typed_endpoints_in_both_validators(self):
        for validator in (ROBUSTNESS, PDR):
            with self.subTest(skill=validator[0]):
                valid = self.cli(validator, MODEL + "B_Desk -[hidden]- E_Item\n@enduml\n")
                self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
                self.assertNotIn("unresolved endpoint", valid.stdout)
                self.assertNotIn("unsupported", valid.stdout)
                if validator == ROBUSTNESS:
                    self.assertIn("relationships: 3", valid.stdout)
                blocked = self.cli(validator, MODEL + "B_Desk -- E_Item\n@enduml\n")
                self.assertEqual(blocked.returncode, 1, blocked.stdout + blocked.stderr)
                self.assertIn("Service Desk", blocked.stdout)
                self.assertIn("Stored Item", blocked.stdout)
                self.assertRegex(blocked.stdout, r"(?:line |L)12:")
                self.assertNotIn("unresolved endpoint", blocked.stdout)

    def test_unknown_and_unsupported_links_leave_located_partial_coverage(self):
        source = MODEL + "B_Typo -- E_Typo\nB_Desk *-- E_Item\n@enduml\n"
        for validator in (ROBUSTNESS, PDR):
            with self.subTest(skill=validator[0]):
                result = self.cli(validator, source)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertRegex(result.stdout, r"(?:line |L)12:.*unresolved endpoint.*B_Typo.*E_Typo")
                self.assertIn("no typed declaration in this source", result.stdout)
                self.assertRegex(result.stdout, r"(?:line |L)13:.*relationship-like syntax")
                self.assertIn("partial", result.stdout)
                self.assertIn("ERRORS: none", result.stdout)

    def test_plantuml_layout_words_do_not_hide_forbidden_links(self):
        for connector in ("-left-", "--right--", "-do->", "<-u-"):
            for validator in (ROBUSTNESS, PDR):
                with self.subTest(skill=validator[0], connector=connector):
                    result = self.cli(validator, MODEL + f'B_Desk {connector} "E_Item"\n@enduml\n')
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertRegex(result.stdout, r"(?:line |L)12:.*Service Desk.*Stored Item")
                    self.assertNotIn("could not be parsed", result.stdout)

    def test_layout_constraints_and_links_to_notes_are_excluded(self):
        source = (MODEL + 'B_Desk -[hidden]le- E_Item\n'
                  'note "Review context" as N_Review\nB_Desk .. N_Review\n@enduml\n')
        for validator in (ROBUSTNESS, PDR):
            with self.subTest(skill=validator[0]):
                result = self.cli(validator, source)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("WARNINGS: none", result.stdout)
                if validator == ROBUSTNESS:
                    self.assertIn("relationships: 3", result.stdout)

    def test_incomplete_declarations_are_not_reported_as_proved_missing(self):
        source = MODEL + '!include external.puml\nC_Book -- E_External\n@enduml\n'
        for validator in (ROBUSTNESS, PDR):
            with self.subTest(skill=validator[0]):
                result = self.cli(validator, source)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertRegex(result.stdout, r"(?:line |L)12:.*preprocessing is not checked")
                self.assertRegex(result.stdout, r"(?:line |L)13:.*E_External.*preprocessing may supply")
                self.assertNotIn("no typed declaration in this source", result.stdout)

    def test_unresolved_pdr_links_withhold_verdict_even_with_all_input_types(self):
        fixtures = ROOT / "tests" / "fixtures" / "pipeline"
        source = (fixtures / "robustez.puml").read_text(encoding="utf-8")
        source = source.replace("B_Form -- C_Agreement : FA-02", "B_Form -- C_Typo : FA-02")
        result = self.cli(PDR, source, (
            "--spec", str(fixtures / "especificacion.md"),
            "--dominio", str(fixtures / "dominio.puml"),
            "--casos-uso", str(fixtures / "casos_uso.puml"),
        ))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("C_Typo", result.stdout)
        self.assertIn("#5 robustness syntax: partial", result.stdout)
        self.assertIn("#7 alternate courses: partial", result.stdout)
        self.assertIn("\n  NOT FULLY VERIFIED\n", result.stdout)
        self.assertNotIn("has no branch in the diagram", result.stdout)


if __name__ == "__main__":
    unittest.main()
