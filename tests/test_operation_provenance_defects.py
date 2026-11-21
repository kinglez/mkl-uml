"""Located non-message origins and honest single-model design checks."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATORS = {
    "mkl-uml-design-class-model": "validate_design_class_puml.py",
    "mkl-cdr-review": "validate_cdr.py",
}
MODEL = """@startuml
skinparam classAttributeIconSize 0
skinparam linetype ortho
skinparam shadowing false
class Worker <<solution>> {
 +evaluate() : String
 +shutdown() : void
}
@enduml
"""
SEQUENCE = """@startuml
participant Caller
participant Worker
Caller -> Worker : evaluate()
@enduml
"""


class OperationProvenanceDefects(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="operation evidence ")
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        self.model = self.write("classes.puml", MODEL)
        self.sequence = self.write("sequence.puml", SEQUENCE)
        self.quote = "Worker.shutdown() is required by the framework lifecycle contract."
        self.source = self.write("contract.md", "# Lifecycle\n" + self.quote + "\n")
        self.record = {"schema_version": 1, "operations": [{
            "classifier": "Worker", "operation": "shutdown", "kind": "contract",
            "source": "contract.md", "line": 2, "quote": self.quote,
            "rationale": "Required lifecycle operation outside the selected evaluate interaction.",
        }]}

    def write(self, name, text):
        path = self.work / name
        path.write_text(text, encoding="utf-8")
        return path

    def evidence(self, record=None):
        return self.write("origins.json", json.dumps(self.record if record is None else record))

    def cli(self, skill, *extra, sequence=True, directory=None):
        directory = directory or ROOT / "skills" / skill
        args = ["--clases", str(self.model)]
        if sequence:
            args += ["--secuencia", str(self.sequence)]
        result = subprocess.run([sys.executable, "-I", "-B",
                                 str(directory / "scripts" / VALIDATORS[skill]), *args, *map(str, extra)],
                                cwd=self.work, capture_output=True, text=True, timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_declared_contract_resolves_only_the_exact_operation(self):
        for skill in VALIDATORS:
            with self.subTest(skill=skill):
                original = self.cli(skill)
                self.assertEqual(original.returncode, 1, original.stdout + original.stderr)
                self.assertIn("Worker.shutdown()", original.stdout)
                accepted = self.cli(skill, "--operation-evidence", self.evidence())
                self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
                self.assertIn("declared contract", accepted.stdout)
                self.assertIn(str(self.source) + ":2", accepted.stdout)
                self.assertIn("semantic adequacy requires review", accepted.stdout)
                self.model.write_text(MODEL.replace(" +shutdown()", " +unexplained() : void\n +shutdown()"))
                unexplained = self.cli(skill, "--operation-evidence", self.evidence())
                self.assertEqual(unexplained.returncode, 1, unexplained.stdout)
                self.assertIn("Worker.unexplained()", unexplained.stdout)
                self.model.write_text(MODEL)

    def test_invalid_or_stale_evidence_cannot_exempt_an_operation(self):
        variants = []
        for key, value in (("classifier", "Other"), ("operation", "absent"),
                           ("kind", "assumption"), ("line", True), ("line", 999),
                           ("quote", "old source"), ("source", "missing.md"),
                           ("source", "../outside.md"), ("rationale", ""),
                           ("parameters", "unknown : Integer")):
            record = copy.deepcopy(self.record)
            record["operations"][0][key] = value
            variants.append((key + str(value), record))
        duplicate = copy.deepcopy(self.record)
        duplicate["operations"].append(duplicate["operations"][0])
        variants.extend([("duplicate", duplicate), ("empty", {"schema_version": 1, "operations": []})])
        for skill in VALIDATORS:
            for label, record in variants:
                with self.subTest(skill=skill, invalid=label):
                    result = self.cli(skill, "--operation-evidence", self.evidence(record))
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("operation evidence", result.stderr)

    def test_duplicate_json_keys_are_rejected(self):
        record = self.write("duplicate.json", '{"schema_version":1,"schema_version":1,"operations":[]}')
        for skill in VALIDATORS:
            result = self.cli(skill, "--operation-evidence", record)
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate JSON key", result.stderr)

    def test_overloads_require_exact_parameters_and_do_not_cover_other_overloads(self):
        self.model.write_text(MODEL.replace(" +shutdown() : void", " +shutdown() : void\n"
                                           " +shutdown(graceful : Boolean) : void"))
        for skill in VALIDATORS:
            with self.subTest(skill=skill):
                ambiguous = self.cli(skill, "--operation-evidence", self.evidence())
                self.assertEqual(ambiguous.returncode, 2)
                self.assertIn("ambiguous", ambiguous.stderr)
                exact = copy.deepcopy(self.record)
                exact["operations"][0]["parameters"] = ""
                remainder = self.cli(skill, "--operation-evidence", self.evidence(exact))
                self.assertEqual(remainder.returncode, 1, remainder.stdout)
                # One exact declaration remains unsupported, despite sharing its name.
                self.assertIn("ERRORS: 1", remainder.stdout)
                second = copy.deepcopy(exact["operations"][0])
                second["parameters"] = "graceful:Boolean"
                exact["operations"].append(second)
                complete = self.cli(skill, "--operation-evidence", self.evidence(exact))
                self.assertEqual(complete.returncode, 0, complete.stdout + complete.stderr)

    def test_real_query_contract_is_not_called_a_trivial_accessor(self):
        self.model.write_text(MODEL.replace(" +shutdown() : void", " +isAvailable() : Boolean"))
        self.sequence.write_text(SEQUENCE.replace("evaluate()", "isAvailable()"))
        # Supply the other required ordinary operation too.
        self.sequence.write_text(self.sequence.read_text().replace("@enduml", "Caller -> Worker : evaluate()\n@enduml"))
        result = self.cli("mkl-uml-design-class-model")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("accessor(s)", result.stdout)
        for skill in VALIDATORS:
            self.sequence.write_text(SEQUENCE)
            result = self.cli(skill)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("Worker.isAvailable()", result.stdout)

    def test_matching_field_accessor_still_gets_a_proportionate_hint(self):
        self.model.write_text(MODEL.replace(" +shutdown() : void", " -name : String\n +getName() : String"))
        result = self.cli("mkl-uml-design-class-model")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("accessor(s)", result.stdout)
        self.assertIn("review candidates", result.stdout)

    def test_existing_interface_query_is_a_capability_not_a_field_accessor(self):
        self.model.write_text("@startuml\ninterface CopyQuery <<solution>> {\n"
                              "+isAvailable(copyId : String) : Boolean\n}\n@enduml\n")
        self.sequence.write_text("@startuml\nparticipant Caller\nparticipant CopyQuery\n"
                                 "Caller -> CopyQuery : isAvailable(copyId)\n@enduml\n")
        result = self.cli("mkl-uml-design-class-model")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("accessor(s)", result.stdout)

    def test_cdr_class_only_executes_static_checks_without_inventing_dynamic_checks(self):
        self.model.write_text(MODEL.replace("evaluate() : String", "evaluate(untyped)"))
        result = self.cli("mkl-cdr-review", sequence=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("does not declare a return value", result.stdout)
        self.assertIn("not typed", result.stdout)
        self.assertIn("rule 3 (types and signatures): executed", result.stdout)
        self.assertIn("rule 8 (assignment): NOT EXECUTED - sequence diagram missing", result.stdout)
        self.assertIn("rule 9 (alternative courses): NOT EXECUTED - sequence diagram missing", result.stdout)
        self.assertIn("PROPOSED VERDICT: NOT FULLY VERIFIED", result.stdout)
        self.assertNotIn("Worker.shutdown()' does not correspond", result.stdout)

    def test_cdr_missing_or_empty_supplied_targets_are_not_class_only_success(self):
        self.model.write_text("@startuml\n@enduml\n")
        result = self.cli("mkl-cdr-review", sequence=False)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.model.write_text(MODEL)
        self.sequence.write_text("@startuml\nparticipant Worker\n@enduml\n")
        result = self.cli("mkl-cdr-review")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("ENTRY CRITERIA NOT MET", result.stdout)

    def test_blank_lines_and_next_line_braces_preserve_diagnostic_locations(self):
        self.model.write_text("@startuml\n\nclass Snapshot {\n +missingType\n}\n\n"
                              "class Worker <<solution>>\n{\n +evaluate(untyped)\n}\n@enduml\n")
        for skill in VALIDATORS:
            with self.subTest(skill=skill):
                result = self.cli(skill, sequence=False)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                attribute = next(line for line in result.stdout.splitlines()
                                 if "Snapshot.missingType'" in line)
                operation = next(line for line in result.stdout.splitlines()
                                 if "Worker.evaluate()'" in line)
                self.assertIn("L4:", attribute)
                self.assertIn("L9:", operation)
                if skill == "mkl-cdr-review":
                    declaration = next(line for line in result.stdout.splitlines()
                                       if "'Snapshot' has" in line)
                    self.assertIn("L3:", declaration)

    def test_single_skill_source_copies_carry_their_own_evidence_helper(self):
        helpers = []
        for skill in VALIDATORS:
            installed = self.work / "installed" / skill
            shutil.copytree(ROOT / "skills" / skill, installed,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            helpers.append((installed / "scripts" / "operation_evidence.py").read_bytes())
            result = self.cli(skill, "--operation-evidence", self.evidence(), directory=installed)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            if skill == "mkl-cdr-review":
                result = self.cli(skill, sequence=False, directory=installed)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("NOT FULLY VERIFIED", result.stdout)
        self.assertEqual(helpers[0], helpers[1])

    def test_call_arguments_and_shared_word_fragments_cannot_supply_another_operation(self):
        cases = [
            ("saveRecord", "deleteRecord", "saveRecord(record)"),
            ("evaluate", "shutdown", 'evaluate("shutdown")'),
            ("approve", "Approve", "approve()"),
        ]
        for called, missing, label in cases:
            self.model.write_text(MODEL.replace("evaluate", called).replace("shutdown", missing))
            self.sequence.write_text(SEQUENCE.replace("evaluate()", label))
            for skill in VALIDATORS:
                with self.subTest(skill=skill, label=label):
                    result = self.cli(skill)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("Worker." + missing + "()", result.stdout)

    def test_receiver_classifier_is_exact_and_explicit_instance_type_is_supported(self):
        self.model.write_text(MODEL.replace(" +shutdown() : void\n", ""))
        for label in ('"worker : Worker" as Target', '"Worker" as Target'):
            self.sequence.write_text('@startuml\nparticipant Caller\nparticipant ' + label +
                                     '\nCaller -> Target : evaluate()\n@enduml\n')
            for skill in VALIDATORS:
                result = self.cli(skill)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("unresolved operation provenance", result.stdout)
        self.sequence.write_text('@startuml\nparticipant Caller\nparticipant "Work er" as Target\n'
                                 'Caller -> Target : evaluate()\n@enduml\n')
        for skill in VALIDATORS:
            result = self.cli(skill)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("wrong class", result.stdout)
            self.assertIn("NOT FULLY VERIFIED", result.stdout)

    def test_legacy_natural_language_is_a_candidate_not_clean_success_or_invented_error(self):
        self.model.write_text(MODEL.replace(" +shutdown() : void\n", "")
                              .replace("evaluate", "checkAvailability"))
        for label in ("check availability", "checks whether the resource can be used"):
            self.sequence.write_text(SEQUENCE.replace("evaluate()", label))
            for skill in VALIDATORS:
                with self.subTest(skill=skill, label=label):
                    result = self.cli(skill)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertIn("unresolved operation provenance", result.stdout)
                    self.assertIn("NOT FULLY VERIFIED", result.stdout)
                    self.assertIn("ERRORS: none", result.stdout)

    def test_message_arguments_do_not_disambiguate_overloaded_operation_types(self):
        self.model.write_text(MODEL.replace(" +shutdown() : void", "")
                              .replace("+evaluate() : String", "+evaluate(value : String) : String\n"
                                       "+evaluate(value : Integer) : String"))
        self.sequence.write_text(SEQUENCE.replace("evaluate()", 'evaluate("text")'))
        for skill in VALIDATORS:
            result = self.cli(skill)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("ambiguous", result.stdout)
            self.assertIn("NOT FULLY VERIFIED", result.stdout)

    def test_inheritance_forwards_calls_not_uninvoked_ancestor_declarations(self):
        self.model.write_text('@startuml\nclass Base <<solution>> {\n+approve() : void\n}\n'
                              'class Derived <<solution>> {\n+approve() : void\n}\n'
                              'Derived --|> Base\n@enduml\n')
        self.sequence.write_text('@startuml\nparticipant Caller\nparticipant Base\n'
                                 'Caller -> Base : unrelated()\n@enduml\n')
        for skill in VALIDATORS:
            result = self.cli(skill)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("Base.approve()", result.stdout)
            self.assertIn("Derived.approve()", result.stdout)
        self.sequence.write_text(self.sequence.read_text().replace('unrelated()', 'approve()'))
        for skill in VALIDATORS:
            result = self.cli(skill)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inherited_name_with_different_declared_parameters_is_partial(self):
        self.model.write_text('@startuml\nclass Base <<solution>> {\n'
                              '+approve(value : String) : void\n}\n'
                              'class Derived <<solution>> {\n'
                              '+approve(value : Integer) : void\n}\n'
                              'Derived --|> Base\n@enduml\n')
        self.sequence.write_text('@startuml\nparticipant Caller\nparticipant Base\n'
                                 'Caller -> Base : approve(value)\n@enduml\n')
        for skill in VALIDATORS:
            result = self.cli(skill)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Derived.approve()", result.stdout)
            self.assertIn("ambiguous", result.stdout)
            self.assertIn("NOT FULLY VERIFIED", result.stdout)
            self.assertIn("ERRORS: none", result.stdout)


if __name__ == "__main__":
    unittest.main()
