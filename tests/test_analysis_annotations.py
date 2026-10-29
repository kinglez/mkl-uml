# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""Executable-model evidence is required in positional PlantUML validators too."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ("mkl-uml-domain-modeler", "validate_domain_puml.py", "strict_good.puml"),
    ("mkl-uml-use-case-diagram", "validate_use_case_puml.py", "academic_enrollment_good.puml"),
    ("mkl-uml-robustness-diagram", "validate_robustness_puml.py", "reserva_hotel_good.puml"),
)


class AnalysisAnnotations(unittest.TestCase):
    def run_model(self, skill, script, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.puml"
            path.write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, str(ROOT / "skills" / skill / "scripts" / script),
                                   str(path)], capture_output=True, text=True,
                                  encoding="utf-8", timeout=20)

    def test_annotation_only_targets_are_rejected(self):
        for skill, script, fixture in CASES:
            source = (ROOT / "skills" / skill / "tests/examples" / fixture).read_text(encoding="utf-8")
            body = re.sub(r"/'[\s\S]*?'/", "", source)
            body = re.sub(r"^\s*@(?:start|end)uml[^\n]*", "", body, flags=re.M)
            for name, hidden in (("comment", "/'\n" + body + "\n'/"),
                                 ("note", "note as Hidden\n" + body + "\nend note"),
                                 ("hnote", "hnote over Hidden\n" + body + "\nend hnote"),
                                 ("legend", "legend\n" + body + "\nendlegend")):
                with self.subTest(skill=skill, annotation=name):
                    result = self.run_model(skill, script, "@startuml\n" + hidden + "\n@enduml\n")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_annotations_cannot_add_invalid_model_elements(self):
        hidden = ('class Repository {\n+bad(id : Integer) : void\n}\n'
                  'actor Intruder\nentity Ghost\nIntruder "1" --> "0..*" Ghost : forbidden\n')
        for skill, script, fixture in CASES:
            source = (ROOT / "skills" / skill / "tests/examples" / fixture).read_text(encoding="utf-8")
            baseline = self.run_model(skill, script, source)
            self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
            for annotation in ("/'\n" + hidden + "'/\n",
                               "note as N\n" + hidden + "end note\n",
                               'note right of "Context: Status"\n' + hidden + 'end note\n'):
                with self.subTest(skill=skill, annotation=annotation.splitlines()[0]):
                    text = source.replace("@enduml", annotation + "@enduml")
                    result = self.run_model(skill, script, text)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_quoted_note_header_colons_do_not_create_design_classes(self):
        model = ('@startuml\nclass Real <<solution>> {\n-id : Integer\n}\n'
                 'note right of "Real: Class"\nclass Ghost <<solution>> {\n'
                 '+missing() : void\n}\nend note\n@enduml\n')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "quoted-note.puml"
            path.write_text(model, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "skills/mkl-uml-design-class-model/scripts/validate_design_class_puml.py"),
                 "--clases", str(path)], capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Classes: 1 ", result.stdout)

    def test_quoted_note_header_colons_do_not_create_pdr_elements(self):
        model = ('@startuml\nboundary Console\ncontrol Booking\nConsole -- Booking : reserve\n'
                 'note right of "Console: Main"\nactor Ghost\nGhost -- Booking : hidden\n'
                 'end note\n@enduml\n')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "quoted-note.puml"
            path.write_text(model, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "skills/mkl-pdr-review/scripts/validate_pdr.py"),
                 "--robustez", str(path)], capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Ghost", result.stdout)

    def test_commented_specification_is_not_a_review_target(self):
        source = (ROOT / "skills/mkl-use-case-specifier/tests/examples/spec_good.md").read_text(encoding="utf-8")
        source = re.sub(r"<!--[\s\S]*?-->", "", source)
        result = self.run_model("mkl-use-case-specifier", "validate_use_case_spec.py",
                                "<!--\n" + source + "\n-->\n")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_pdr_commented_specification_does_not_supply_behavior(self):
        pipeline = ROOT / "tests/fixtures/pipeline"
        source = (pipeline / "especificacion.md").read_text(encoding="utf-8")
        source = re.sub(r"<!--[\s\S]*?-->", "", source)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "commented.md"
            path.write_text("<!--\n" + source + "\n-->\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "skills/mkl-pdr-review/scripts/validate_pdr.py"),
                 "--robustez", str(pipeline / "robustez.puml"),
                 "--dominio", str(pipeline / "dominio.puml"), "--spec", str(path)],
                capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT FULLY VERIFIED", result.stdout)
        self.assertNotIn("#10 highlighter test: executed", result.stdout)


if __name__ == "__main__":
    unittest.main()
