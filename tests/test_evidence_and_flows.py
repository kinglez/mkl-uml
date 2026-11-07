# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Public CLI contracts for usable evidence and realized interaction flows."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "skills/mkl-uml-design-class-model/scripts/validate_design_class_puml.py"
SEQUENCE = ROOT / "skills/mkl-uml-sequence-diagram/scripts/validate_sequence_puml.py"
PDR = ROOT / "skills/mkl-pdr-review/scripts/validate_pdr.py"
CDR = ROOT / "skills/mkl-cdr-review/scripts/validate_cdr.py"
DIRECTIVES = ("skinparam style strictuml\nskinparam shadowing false\n"
              "skinparam responseMessageBelowArrow true\n")
MODEL = ("@startuml\nclass Processor <<solution>> {\n"
         "+evaluate() : String\n}\n@enduml\n")
INTERACTION = ("@startuml\n" + DIRECTIVES + "participant Caller\nparticipant Processor\n"
               "Caller -> Processor : evaluate()\n@enduml\n")


class EvidenceAndFlows(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name)

    def file(self, name, text):
        path = self.temp / name
        path.write_text(text, encoding="utf-8")
        return path

    def cli(self, script, *args):
        result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_unusable_support_cannot_complete_design_or_sequence_checks(self):
        model = self.file("model.puml", MODEL)
        sequence = self.file("interaction.puml", INTERACTION)
        for name, body in (("empty", ""), ("unrecognized", "unrelated words"),
                           ("annotations", "@startuml\nnote as N\nclass Phantom\n"
                            "1. System evaluates.\nend note\n@enduml\n"),
                           ("legend", "@startuml\nlegend\nclass Phantom\n"
                            "1. System evaluates.\nendlegend\n@enduml\n")):
            with self.subTest(body=name):
                support = self.file(name + ".txt", body)
                result = self.cli(DESIGN, "--clases", model, "--secuencia", sequence,
                                  "--dominio", support, "--spec", support)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("NOT FULLY VERIFIED", result.stdout)
                self.assertNotIn("STATUS: READY FOR CDR", result.stdout)
                result = self.cli(SEQUENCE, "--secuencia", sequence, "--dominio", support,
                                  "--robustez", support, "--spec", support)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for layer in ("entity closure against domain", "participant closure against DR-XX",
                              "alternate-flow coverage"):
                    self.assertIn(layer + ": NOT EXECUTED", result.stdout)

    def test_unusable_sequence_cannot_complete_operation_provenance(self):
        model = self.file("model.puml", MODEL)
        for name, body in (("empty", ""), ("note", "@startuml\nnote as N\n"
                           "Caller -> Processor : evaluate()\nend note\n@enduml\n")):
            with self.subTest(body=name):
                result = self.cli(DESIGN, "--clases", model, "--secuencia",
                                  self.file(name + ".puml", body))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("operation provenance: NOT EXECUTED", result.stdout)
                self.assertIn("NOT FULLY VERIFIED", result.stdout)

    def test_pdr_basic_dialogue_cannot_borrow_exception_responses(self):
        rob = self.file("rob.puml", "@startuml\ntitle CU-01 Handle request\n"
                        "actor User\nboundary Console\ncontrol Evaluation\n"
                        "User -- Console : request\nConsole -- Evaluation : evaluate result FE-01\n@enduml\n")
        for basic in ("TBD.", "1. The User submits the request."):
            for heading, label in (("Exception flows", "### FE-01"),
                                   ("Alternate flows", "FE-01")):
                with self.subTest(basic=basic, heading=heading):
                    spec = self.file("spec.md", "# CU-01 Handle request\n## Basic flow\n"
                                     + basic + "\n## " + heading + "\n" + label
                                     + " Unavailable\n1. The System returns an unavailable result.\n")
                    result = self.cli(PDR, "--robustez", rob, "--spec", spec)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("guideline #6", result.stdout)
        spec = self.file("complete.md", "# CU-01 Handle request\n## Basic flow\n"
                         "1. The User submits the request.\n2. The System returns the result.\n")
        result = self.cli(PDR, "--robustez", rob, "--spec", spec)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("guideline #6 -", result.stdout)

    def test_empty_labeled_operands_do_not_implement_required_flows(self):
        model = self.file("model.puml", MODEL)
        spec = self.file("spec.md", "# CU-01 Evaluate input\n## Basic flow\n"
                         "1. The System evaluates the input and returns a result.\n"
                         "## FA-01 Invalid input\n"
                         "1. The System returns an invalid-input result and terminates.\n")
        for alternative in ("alt FA-01 invalid\nelse valid\n"
                            "Processor --> Caller : <<reply>> result\nend\n",
                            "alt valid\nProcessor --> Caller : <<reply>> result\n"
                            "else FA-01 invalid\nend\n"):
            with self.subTest(branch=alternative):
                for body, expected in (("", 1),
                                       ("Processor --> Caller : <<reply>> invalidInput\n", 0)):
                    label = "alt FA-01 invalid\n" if alternative.startswith("alt FA-01") else "else FA-01 invalid\n"
                    branch = alternative.replace(label, label + body)
                    source = INTERACTION.replace("@startuml", "@startuml\ntitle CU-01 Evaluate input")
                    seq = self.file("sequence.puml", source.replace("@enduml", branch + "@enduml"))
                    for script, args in ((SEQUENCE, ("--secuencia", seq, "--spec", spec)),
                                         (CDR, ("--clases", model, "--secuencia", seq, "--spec", spec))):
                        result = self.cli(script, *args)
                        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                        if expected:
                            self.assertIn("FA-01", result.stdout)

    def test_break_skips_suffix_on_its_selected_path(self):
        body = ("boundary Gateway\nparticipant Processor\nGateway -> Processor ++ : evaluate()\n"
                "break unavailable\nProcessor --> Gateway -- : <<reply>> unavailable\nend\n"
                "Processor --> Gateway -- : <<reply>> result\n")
        for wrapper in ("", "group evaluation\n"):
            with self.subTest(wrapper=wrapper):
                source = "@startuml\n" + DIRECTIVES + wrapper + body
                source += ("end\n" if wrapper else "") + "@enduml\n"
                result = self.cli(SEQUENCE, "--secuencia", self.file("break.puml", source),
                                  "--con-activaciones")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                bad = source.replace("<<reply>> unavailable\n", "<<reply>> unavailable\ndeactivate Processor\n")
                result = self.cli(SEQUENCE, "--secuencia", self.file("bad-break.puml", bad),
                                  "--con-activaciones")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("without an open activation", result.stdout)

    def test_parallel_operands_all_execute_and_retain_real_leaks(self):
        source = ("@startuml\n" + DIRECTIVES + "boundary Gateway\nparticipant First\nparticipant Second\n"
                  "Gateway ->> First ++ : <<asynchCall>> evaluate()\n"
                  "Gateway ->> Second ++ : <<asynchCall>> evaluate()\n"
                  "par first result\nFirst ->> Gateway -- : <<asynchSignal>> firstReady\n"
                  "else second result\nSecond ->> Gateway -- : <<asynchSignal>> secondReady\nend\n@enduml\n")
        result = self.cli(SEQUENCE, "--secuencia", self.file("parallel.puml", source), "--con-activaciones")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        bad = source.replace("Second ->> Gateway --", "Second ->> Gateway")
        result = self.cli(SEQUENCE, "--secuencia", self.file("parallel-leak.puml", bad), "--con-activaciones")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("'Second' remains active", result.stdout)

    def test_domain_aliases_do_not_erase_pdr_attributes(self):
        rob = self.file("rob.puml", "@startuml\nboundary Console\ncontrol Evaluation\nentity Record\n"
                        "Console -- Evaluation\nEvaluation -- Record\n@enduml\n")
        for declaration in ("class Record", 'class "Record" as record',
                            'class "Record" as record <<entity>>'):
            with self.subTest(declaration=declaration):
                domain = self.file("domain.puml", "@startuml\n" + declaration + " {\nvalue\n}\n@enduml\n")
                result = self.cli(PDR, "--robustez", rob, "--dominio", domain)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("guideline #8 -", result.stdout)


if __name__ == "__main__":
    unittest.main()
