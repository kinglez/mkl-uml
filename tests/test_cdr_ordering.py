"""Declared ordering uses the modeled path and the current review source."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills/mkl-cdr-review/scripts/validate_cdr.py"
PREREQUISITE = "Store --> Service : commitSucceeded"
CONTROLLED = "Service --> Client : outcomePublished"


class CdrOrderingTests(unittest.TestCase):
    def setUp(self):
        staging = tempfile.TemporaryDirectory(prefix="cdr-ordering-")
        self.addCleanup(staging.cleanup)
        self.work = Path(staging.name)
        self.classes = self.write("classes.puml", textwrap.dedent("""\
            @startuml
            class Service <<solution>> {
              +run() : void
            }
            @enduml
            """))
        self.sequence = self.work / "interaction.puml"
        self.quote = "Publish the outcome only after the commit has succeeded."
        self.write("contract.md", f"# Commit contract\n{self.quote}\n")
        self.record = {
            "schema_version": 1,
            "rules": [{
                "id": "ORD-01",
                "sequence": "interaction.puml",
                "source": "contract.md",
                "line": 2,
                "quote": self.quote,
                "before": {"sender": "Store", "receiver": "Service", "label": "commitSucceeded"},
                "after": {"sender": "Service", "receiver": "Client", "label": "outcomePublished"},
            }],
        }

    def write(self, name, text):
        path = self.work / name
        path.write_text(text, encoding="utf-8")
        return path

    def check_cli(self, scenario, *, mapping=True, interaction=True):
        text = ("@startuml\nactor Client\ncontrol Service\nparticipant Store\n"
                "Client -> Service : run()\n" + scenario + "\n@enduml\n")
        self.sequence.write_text(text, encoding="utf-8")
        args = ["--clases", str(self.classes)]
        if interaction:
            args += ["--secuencia", str(self.sequence)]
        if mapping:
            args += ["--ordering-evidence", str(self.write("ordering.json", json.dumps(self.record)))]
        result = subprocess.run([sys.executable, "-I", "-B", str(VALIDATOR), *args],
                                cwd=self.work, capture_output=True, text=True, timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_late_or_missing_prerequisite_rejects_the_controlled_message(self):
        for suffix in (PREREQUISITE, ""):
            with self.subTest(suffix=suffix):
                result = self.check_cli(CONTROLLED + "\n" + suffix)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("L6: a modeled path reaches 'outcomePublished' without prior", result.stdout)
                self.assertIn("PROPOSED VERDICT: REINSPECTION REQUIRED", result.stdout)

    def test_prerequisite_in_another_operand_does_not_satisfy_the_rule(self):
        scenario = (f"alt committed\n{PREREQUISITE}\nelse\n{CONTROLLED}\nend")
        result = self.check_cli(scenario)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("L9: a modeled path reaches", result.stdout)

    def test_safe_branch_and_common_continuation(self):
        scenarios = (
            f"alt committed\n{PREREQUISITE}\n{CONTROLLED}\nelse\n"
            "Service --> Client : no outcome\nend",
            f"alt commit primary\n{PREREQUISITE}\nelse\n{PREREQUISITE}\nend\n{CONTROLLED}",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                result = self.check_cli(scenario)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("declared message ordering: executed", result.stdout)

    def test_skippable_and_terminated_operands_do_not_grant_the_continuation(self):
        for kind in ("alt", "opt", "loop", "break"):
            with self.subTest(kind=kind):
                result = self.check_cli(f"{kind} guarded\n{PREREQUISITE}\nend\n{CONTROLLED}")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("without prior 'commitSucceeded'", result.stdout)

    def test_unsupported_or_unmatched_evidence_is_partial(self):
        cases = (
            (f"par commit\n{PREREQUISITE}\nelse publish\n{CONTROLLED}\nend",
             "unsupported par fragment"),
            (f"ref over Service : Commit interaction\n{CONTROLLED}", "unsupported sequence statement"),
            (PREREQUISITE, "no message matches the after selector"),
        )
        for scenario, explanation in cases:
            with self.subTest(scenario=scenario):
                result = self.check_cli(scenario)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("declared message ordering: PARTIAL", result.stdout)
                self.assertIn(explanation, result.stdout)

    def test_standalone_scope_keeps_previous_exit_status(self):
        sequence_only = self.check_cli(CONTROLLED, mapping=False)
        self.assertEqual(sequence_only.returncode, 0, sequence_only.stdout + sequence_only.stderr)
        self.assertIn("NOT EXECUTED - no explicit ordering evidence supplied", sequence_only.stdout)
        class_only = self.check_cli(CONTROLLED, interaction=False)
        self.assertEqual(class_only.returncode, 0, class_only.stdout + class_only.stderr)
        self.assertIn("declared message ordering: PARTIAL", class_only.stdout)
        self.assertIn("was not supplied with --secuencia", class_only.stdout)

    def test_invalid_or_stale_evidence_is_an_input_error(self):
        rule = self.record["rules"][0]
        for field, value in (("quote", "old requirement"), ("line", True),
                             ("source", "../contract.md"), ("after", rule["before"])):
            with self.subTest(field=field):
                original = rule[field]
                rule[field] = value
                try:
                    result = self.check_cli(f"{PREREQUISITE}\n{CONTROLLED}")
                finally:
                    rule[field] = original
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("ordering evidence", result.stderr)
