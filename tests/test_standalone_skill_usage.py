# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Every single-skill install runs without the checkout or sibling skills."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools.install_skills import install

ROOT = Path(__file__).resolve().parents[1]
MODEL = ("@startuml\nskinparam classAttributeIconSize 0\nskinparam linetype ortho\n"
         "skinparam shadowing false\nclass Processor <<solution>> {\n+evaluate() : String\n}\n@enduml\n")
SEQUENCE = ("@startuml\nskinparam style strictuml\nskinparam shadowing false\n"
            "skinparam responseMessageBelowArrow true\nparticipant Caller\nparticipant Processor\n"
            "Caller -> Processor : evaluate()\n@enduml\n")
ROBUSTNESS = ("@startuml\nleft to right direction\nskinparam linetype ortho\nskinparam shadowing false\n"
              'actor "User" as ACT_User\nboundary "Console" as B_Console\ncontrol "Evaluate" as C_Evaluate\n'
              "ACT_User -- B_Console\nB_Console -- C_Evaluate\n@enduml\n")
SPEC = ("# CU-01 Complete goal\nPrimary actor: User\nTrigger: The User starts.\nPreconditions: Ready.\n"
        "## Basic flow\n1. The User submits a request.\n2. The System returns a result under RN-01.\n"
        "## Postconditions\nThe result is available.\n## Business rules\nRN-01: Input must be valid.\n"
        "## Acceptance criteria\nCA-01: Given valid input, when submitted, then return a result.\n")
CASES = [
    ("mkl-uml-domain-modeler", "validate_domain_puml.py", ["domain.puml"]),
    ("mkl-uml-use-case-diagram", "validate_use_case_puml.py", ["use-cases.puml"]),
    ("mkl-use-case-specifier", "validate_use_case_spec.py", ["spec.md"]),
    ("mkl-uml-robustness-diagram", "validate_robustness_puml.py", ["robustness.puml"]),
    ("mkl-pdr-review", "validate_pdr.py", ["--robustez", "robustness.puml"]),
    ("mkl-uml-c4-architecture", "validate_c4.py", ["context.puml", "--level", "context"]),
    ("mkl-uml-sequence-diagram", "validate_sequence_puml.py", ["--secuencia", "sequence.puml"]),
    ("mkl-uml-design-class-model", "validate_design_class_puml.py", ["--clases", "classes.puml"]),
    ("mkl-cdr-review", "validate_cdr.py", ["--clases", "classes.puml", "--secuencia", "sequence.puml"]),
]


class StandaloneSkillUsage(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="mkl standalone ")
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name)
        self.work = self.temp / "unrelated project"
        self.work.mkdir()
        sources = {
            "domain.puml": "@startuml\nskinparam linetype ortho\nskinparam classAttributeIconSize 0\n"
                           "hide methods\nhide empty members\nclass Record\nclass Kind\nRecord -- Kind : belongs to\n@enduml\n",
            "use-cases.puml": '@startuml\nleft to right direction\nskinparam linetype ortho\n'
                              'skinparam packageStyle rectangle\nskinparam shadowing false\nactor User\n'
                              'rectangle "Subject" {\nusecase "Complete goal" as CU_Main\n}\nUser -- CU_Main\n@enduml\n',
            "spec.md": SPEC, "robustness.puml": ROBUSTNESS, "classes.puml": MODEL, "sequence.puml": SEQUENCE,
            "context.puml": '@startuml\n!include <C4/C4_Context>\nPerson(user, "User")\n'
                            'System(target, "Target")\nRel(user, target, "Uses")\n@enduml\n',
        }
        for name, text in sources.items():
            (self.work / name).write_text(text, encoding="utf-8")

    def installed(self, name, transport):
        destination = self.temp / transport / name
        if transport == "payload":
            directory = install(destination, [name])[0]
        else:
            directory = destination / name
            shutil.copytree(ROOT / "skills" / name, directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.assertEqual([p.name for p in destination.iterdir()], [name])
        return directory

    def cli(self, directory, script, args):
        argv = [str(self.work / value) if (self.work / value).is_file() else value for value in args]
        # -I excludes PYTHONPATH and the checkout; CDR carries its own imported helper.
        result = subprocess.run([sys.executable, "-I", "-B", str(directory / "scripts" / script), *argv],
                                cwd=self.work, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_each_skill_runs_with_only_its_own_minimum_targets(self):
        for name, script, args in CASES:
            for transport in ("payload", "source-copy"):
                with self.subTest(skill=name, transport=transport):
                    directory = self.installed(name, transport)
                    result = self.cli(directory, script, args)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    if name in ("mkl-pdr-review", "mkl-cdr-review", "mkl-uml-design-class-model"):
                        self.assertIn("NOT FULLY VERIFIED", result.stdout)
                    elif name == "mkl-uml-sequence-diagram":
                        self.assertIn("NOT EXECUTED - specification missing", result.stdout)

    def test_cdr_headers_import_their_helper_from_the_same_single_skill(self):
        directory = self.installed("mkl-cdr-review", "payload")
        result = self.cli(directory, "generate_code_headers.py", ["--clases", "classes.puml"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("String evaluate()", result.stdout)

    def test_missing_review_target_is_actionable_without_creating_predecessors(self):
        for name, script, _args in CASES:
            if name not in ("mkl-pdr-review", "mkl-cdr-review", "mkl-uml-design-class-model",
                            "mkl-uml-sequence-diagram"):
                continue
            with self.subTest(skill=name):
                directory = self.installed(name, "payload")
                result = self.cli(directory, script, [])
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("required", result.stderr)
                self.assertNotIn("No such file", result.stderr)


if __name__ == "__main__":
    unittest.main()
