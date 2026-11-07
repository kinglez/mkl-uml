# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Review declarations preserve modeled contracts or expose conversion gaps."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills/mkl-cdr-review/scripts"
HEADERS = BASE / "generate_code_headers.py"
CDR = BASE / "validate_cdr.py"
DESIGN = ROOT / "skills/mkl-uml-design-class-model/scripts/validate_design_class_puml.py"


class ReviewHeaders(unittest.TestCase):
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

    def test_enum_literals_properties_operations_and_gaps_are_distinct(self):
        model = self.file("mode.puml", "@startuml\nenum Mode {\nFIRST\nSECOND\n"
                          "-label : String\n+accepts(value : String) : Boolean\n}\n@enduml\n")
        result = self.cli(HEADERS, "--clases", model)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FIRST, SECOND;", result.stdout)
        self.assertIn("String label;", result.stdout)
        self.assertIn("Boolean accepts(String value)", result.stdout)
        self.assertNotIn("FIRST, SECOND, label", result.stdout)
        incomplete = self.file("incomplete.puml", "@startuml\nenum Mode {\nFIRST\n"
                               "+accepts(value)\n}\n@enduml\n")
        sequence = self.file("sequence.puml", "@startuml\nparticipant Caller\nparticipant Mode\n"
                             "Caller -> Mode : accepts(value)\n@enduml\n")
        for script, extra in ((DESIGN, ()), (CDR, ("--secuencia", sequence))):
            result = self.cli(script, "--clases", incomplete, *extra)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("accepts", result.stdout)
            self.assertIn("not typed", result.stdout)
        result = self.cli(HEADERS, "--clases", incomplete)
        self.assertIn("accepts", result.stdout)
        self.assertIn("???", result.stdout)
        self.assertNotIn("No typing gaps found", result.stdout)

    def test_interface_generalization_uses_extends_and_realization_implements(self):
        source = ("@startuml\ninterface Readable {\n+read() : String\n}\n"
                  "interface Writable {\n+write(value : String) : void\n}\n"
                  "interface Combined\nCombined --|> Readable\nCombined --|> Writable\n"
                  "class Processor\nProcessor ..|> Readable\n@enduml\n")
        result = self.cli(HEADERS, "--clases", self.file("interfaces.puml", source))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("interface Combined extends Readable, Writable", result.stdout)
        self.assertNotIn("interface Combined implements", result.stdout)
        self.assertIn("class Processor implements Readable", result.stdout)

    def test_parameter_directions_are_metadata_with_explicit_mapping_gaps(self):
        model = self.file("directions.puml", "@startuml\nclass Processor {\n"
                          "+evaluate(in key : String, out result : String, inout cursor : Cursor) : Boolean\n"
                          "}\n@enduml\n")
        result = self.cli(HEADERS, "--clases", model)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for direction, name in (("in", "key"), ("out", "result"), ("inout", "cursor")):
            self.assertIn("/* " + direction + " */", result.stdout)
            self.assertNotIn("String " + direction + " " + name, result.stdout)
        self.assertIn("language-specific mapping", result.stdout)
        self.assertNotIn("No typing gaps found", result.stdout)
        ordinary = self.file("input.puml", "@startuml\nclass Processor {\n"
                             "+evaluate(in value : Map<String, List<Integer>>) : Boolean\n}\n@enduml\n")
        result = self.cli(HEADERS, "--clases", ordinary)
        self.assertIn("Map<String, List<Integer>> value", result.stdout)
        self.assertIn("No typing gaps found", result.stdout)

    def test_multiple_interface_contracts_are_order_independent(self):
        source = ("@startuml\ninterface Readable <<solution>> {\n+read() : String\n}\n"
                  "interface Writable <<solution>> {\n+write(value : String) : void\n}\n"
                  "class Processor <<solution>> {\n+read() : String\n+write(value : String) : void\n}\n")
        sequence = self.file("sequence.puml", "@startuml\nparticipant Caller\nparticipant Readable\n"
                             "participant Writable\nCaller -> Readable : read()\n"
                             "Caller -> Writable : write(value)\n@enduml\n")
        for relations in ("Processor ..|> Readable\nProcessor ..|> Writable\n",
                          "Processor ..|> Writable\nProcessor ..|> Readable\n"):
            result = self.cli(DESIGN, "--clases", self.file("interfaces.puml", source + relations + "@enduml\n"),
                              "--secuencia", sequence)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("It may be on the wrong class", result.stdout)


if __name__ == "__main__":
    unittest.main()
