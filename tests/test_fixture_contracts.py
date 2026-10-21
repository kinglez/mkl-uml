#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. mkl regression contracts.
"""Run real validator CLIs against reviewed behavioral fixture contracts.

Run from the repository root with:
    python3 -m unittest discover -s tests -p 'test_fixture_contracts.py' -v

The JSON stores independent, reviewed expected statuses and diagnostic fragments.
It deliberately does not infer correctness from fixture names or validator code.
Warnings are part of the public behavior even when the process exits zero.
"""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "tests" / "fixture_expectations.json"
CONTRACTS = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))["cases"]
PIPELINE = "tests/fixtures/pipeline/"

# Static input ownership; never import expected outcomes from code under test.
VALIDATORS = {
    "mkl-uml-domain-modeler": ("validate_domain_puml.py", {"": "dominio.puml"}),
    "mkl-uml-use-case-diagram": ("validate_use_case_puml.py", {"": "casos_uso.puml"}),
    "mkl-use-case-specifier": ("validate_use_case_spec.py", {"": "especificacion.md"}),
    "mkl-uml-robustness-diagram": ("validate_robustness_puml.py", {"": "robustez.puml"}),
    "mkl-pdr-review": ("validate_pdr.py", {
        "--dominio": "dominio.puml", "--casos-uso": "casos_uso.puml",
        "--robustez": "robustez.puml", "--spec": "especificacion.md"}),
    "mkl-uml-sequence-diagram": ("validate_sequence_puml.py", {
        "--secuencia": "secuencia.puml", "--robustez": "robustez.puml",
        "--spec": "especificacion.md", "--dominio": "dominio.puml"}),
    "mkl-uml-design-class-model": ("validate_design_class_puml.py", {
        "--clases": "modelo_clases_diseno.puml", "--dominio": "dominio.puml",
        "--secuencia": "secuencia.puml", "--spec": "especificacion.md"}),
    "mkl-cdr-review": ("validate_cdr.py", {
        "--clases": "modelo_clases_diseno.puml", "--secuencia": "secuencia.puml",
        "--spec": "especificacion.md", "--robustez": "robustez.puml",
        "--dominio": "dominio.puml", "--requisitos": "requisitos.md",
        "--pruebas": "plan_pruebas.md"}),
}


def pipeline_args(skill, keep=None):
    args = []
    for flag, filename in VALIDATORS[skill][1].items():
        if keep is not None and flag not in keep:
            continue
        if flag:
            args.append(flag)
        args.append(PIPELINE + filename)
    return args


class CLIContracts(unittest.TestCase):
    maxDiff = None

    def assert_cli(self, script, args, exit_code, contains, excludes=()):
        proc = subprocess.run(
            [sys.executable, str(ROOT / script), *args],
            cwd=ROOT, capture_output=True, text=True, timeout=20,
        )
        output = proc.stdout + proc.stderr
        context = f"{script} {' '.join(args)}\n{output}"
        self.assertEqual(proc.returncode, exit_code, context)
        self.assertNotIn("Traceback (most recent call last)", output, context)
        for fragment in contains:
            self.assertIn(fragment, output, context)
        for fragment in excludes:
            self.assertNotIn(fragment, output, context)
        return output

    def test_contract_inventory_is_complete(self):
        ids = [case["id"] for case in CONTRACTS]
        self.assertEqual(len(ids), 85, "Review the manifest when adding/removing example scenarios")
        self.assertEqual(len(ids), len(set(ids)), "Duplicate fixture contracts")
        discovered = set()
        for skill in VALIDATORS:
            base = ROOT / "skills" / skill / "tests" / "examples"
            if "" in VALIDATORS[skill][1]:
                extension = "*.md" if skill == "mkl-use-case-specifier" else "*.puml"
                discovered.update(skill + "/" + item.name for item in base.glob(extension))
            else:
                discovered.update(skill + "/" + item.name for item in base.iterdir() if item.is_dir())
        self.assertEqual(set(ids), discovered, "Every example must have a reviewed contract")
        self.assertEqual({case["id"].split("/")[0] for case in CONTRACTS}, set(VALIDATORS))
        for case in CONTRACTS:
            self.assertIn(case["exit_code"], (0, 1))
            self.assertTrue(case["contains"], case["id"] + " needs a behavioral assertion")
            self.assertTrue((ROOT / case["script"]).is_file())
            for argument in case["args"]:
                if not argument.startswith("--"):
                    self.assertTrue((ROOT / argument).is_file(), argument)

    def test_use_case_diagram_rejects_class_declarations(self):
        source = (ROOT / PIPELINE / "casos_uso.puml").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "class_in_use_case.puml"
            invalid.write_text(source.replace("@enduml", "class InternalRecord\n@enduml"), encoding="utf-8")
            self.assert_cli(
                "skills/mkl-uml-use-case-diagram/scripts/validate_use_case_puml.py",
                [str(invalid)], 1, ["use case diagram must not declare classes"],
            )

    def test_pipeline_identifiers_and_test_derivation(self):
        # IDs are the handoff contract across independently consumed artifacts.
        expected = {
            "especificacion.md": ["CU-07", "DR-07", "DS-07", "MC-07", "FA-01", "FA-02"],
            "robustez.puml": ["CU-07", "DR-07", "FA-01", "FA-02"],
            "secuencia.puml": ["CU-07", "DS-07", "FA-01", "FA-02"],
            "modelo_clases_diseno.puml": ["CU-07", "MC-07"],
            "plan_pruebas.md": ["CU-07", "DR-07", "CP-01", "CP-02", "CP-03", "CP-04", "CP-05", "CP-06", "FA-01", "FA-02"],
        }
        for filename, identifiers in expected.items():
            text = (ROOT / PIPELINE / filename).read_text(encoding="utf-8")
            for identifier in identifiers:
                with self.subTest(filename=filename, identifier=identifier):
                    self.assertIn(identifier, text)


def add_fixture_test(case):
    def test(self):
        self.assert_cli(case["script"], case["args"], case["exit_code"], case["contains"])
    test.__doc__ = case["id"]
    name = "test_fixture_" + re.sub(r"\W+", "_", case["id"])
    setattr(CLIContracts, name, test)


for _case in CONTRACTS:
    add_fixture_test(_case)


def add_pipeline_test(skill, contains):
    def test(self):
        self.assert_cli("skills/" + skill + "/scripts/" + VALIDATORS[skill][0],
                        pipeline_args(skill), 0, ["ERRORS: none", *contains])
    setattr(CLIContracts, "test_pipeline_" + skill.replace("-", "_"), test)


for _skill, _diagnostics in {
    "mkl-uml-domain-modeler": ["WARNINGS: none"],
    "mkl-uml-use-case-diagram": ["WARNINGS: none"],
    "mkl-use-case-specifier": ["Basic-flow steps: 6", "WARNINGS: none"],
    "mkl-uml-robustness-diagram": ["WARNINGS: none"],
    "mkl-pdr-review": ["highlighter coverage......... 100%", "ACCEPTED"],
    "mkl-uml-sequence-diagram": ["Uncovered Controllers ......... 0", "Flows without fragments ....... 0"],
    "mkl-uml-design-class-model": ["classes without provenance .. 0", "operations without message .. 0", "STATUS: READY FOR CDR"],
    "mkl-cdr-review": ["rule 1 (test plan): executed", "rule 5 (traceability): executed", "PROPOSED VERDICT: ACCEPTED"],
}.items():
    add_pipeline_test(_skill, _diagnostics)


def add_degradation_test(skill, flags, contains, excludes):
    def test(self):
        self.assert_cli("skills/" + skill + "/scripts/" + VALIDATORS[skill][0],
                        pipeline_args(skill, flags), 0, contains, excludes)
    setattr(CLIContracts, "test_missing_inputs_" + skill.replace("-", "_"), test)


add_degradation_test("mkl-pdr-review", {"--robustez"},
                     ["NOT EXECUTED - textual specification missing", "NOT EXECUTED - domain model missing",
                      "NOT FULLY VERIFIED", "package cannot be declared fully verified"],
                     ["\n  ACCEPTED\n", "\n  ACCEPTED WITH REWORK VERIFICATION\n"])
add_degradation_test("mkl-uml-sequence-diagram", {"--secuencia"},
                     ["NOT EXECUTED - specification missing", "NOT EXECUTED - domain model missing",
                      "NOT EXECUTED - robustness diagram missing", "Uncovered Controllers ......... n/a"],
                     ["Uncovered Controllers ......... 0"])
add_degradation_test("mkl-uml-design-class-model", {"--clases"},
                     ["NOT EXECUTED - specification missing", "NOT EXECUTED - domain model missing",
                      "NOT EXECUTED - sequence diagram missing", "STATUS: NOT FULLY VERIFIED"],
                     ["STATUS: READY FOR CDR"])
add_degradation_test("mkl-cdr-review", {"--clases", "--secuencia"},
                     ["NOT EXECUTED - test plan missing", "NOT EXECUTED - requirements are missing",
                      "NOT EXECUTED - use case specification missing", "PROPOSED VERDICT: NOT FULLY VERIFIED"],
                     ["PROPOSED VERDICT: ACCEPTED"])


if __name__ == "__main__":
    unittest.main()
