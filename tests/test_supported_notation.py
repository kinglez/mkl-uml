# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Equivalent supported model notation preserves public validator behavior."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = ROOT / "skills/mkl-uml-domain-modeler/scripts/validate_domain_puml.py"
USECASE = ROOT / "skills/mkl-uml-use-case-diagram/scripts/validate_use_case_puml.py"
ROBUSTNESS = ROOT / "skills/mkl-uml-robustness-diagram/scripts/validate_robustness_puml.py"
SPEC = ROOT / "skills/mkl-use-case-specifier/scripts/validate_use_case_spec.py"
DOMAIN_STYLE = ("skinparam linetype ortho\nskinparam classAttributeIconSize 0\n"
                "hide methods\nhide empty members\n")
USECASE_STYLE = ("left to right direction\nskinparam linetype ortho\n"
                 "skinparam packageStyle rectangle\nskinparam shadowing false\n")


class SupportedNotation(unittest.TestCase):
    def cli(self, script, text, *args):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ("input.md" if script == SPEC else "input.puml")
            path.write_text(text, encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(script), str(path), *args],
                                    capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_domain_declaration_decoration_cannot_disable_member_rules(self):
        for declaration in ("class Record", "class Record <<entity>>",
                            'class "Recorded Item" as Record'):
            with self.subTest(declaration=declaration):
                result = self.cli(DOMAIN, "@startuml\n" + DOMAIN_STYLE + "class Item\n"
                                  + declaration + " {\n+evaluate()\n}\nItem -- Record : records\n@enduml\n")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Operation-like member", result.stdout)
                self.assertIn("Visibility marker", result.stdout)

    def test_quoted_domain_aliases_preserve_classes_and_relationships(self):
        result = self.cli(DOMAIN, "@startuml\n" + DOMAIN_STYLE
                          + 'class "Recorded Item" as Record\nclass "Item Kind" as Kind\n'
                          + "Record -- Kind : belongs to\n@enduml\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("no detected relationship", result.stdout)
        self.assertNotIn("no usable class", result.stdout)

    def test_standard_dotted_use_case_relationships_are_reviewed(self):
        for kind, count in (("include", 9), ("extend", 5)):
            for arrow in ("..>", ".>"):
                with self.subTest(kind=kind, arrow=arrow):
                    source = "@startuml\n" + USECASE_STYLE + 'actor User\nrectangle "Subject" {\n'
                    source += 'usecase "Complete goal" as Main\n'
                    source += "".join('usecase "Goal ' + str(i) + '" as Goal' + str(i) + '\n'
                                      for i in range(count)) + "}\nUser -- Main\n"
                    source += "".join("Main " + arrow + " Goal" + str(i) + " : <<" + kind + ">>\n"
                                      for i in range(count)) + "@enduml\n"
                    result = self.cli(USECASE, source)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn("high " + kind + " count", result.stdout)

    def test_hidden_layout_edges_are_not_bce_communications(self):
        source = ("@startuml\nleft to right direction\nskinparam linetype ortho\n"
                  "skinparam shadowing false\nactor User\nboundary Console\n"
                  "control Evaluation\nentity Record\nUser -- Console\n"
                  "Console -- Evaluation\nEvaluation -- Record\n")
        for edge, expected in (("", 0), ("Console -[hidden]- Record\n", 0),
                               ("Console -[#red]- Record\n", 1),
                               ("Console -- Record\n", 1)):
            with self.subTest(edge=edge):
                result = self.cli(ROBUSTNESS, source + edge + "@enduml\n")
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_actor_associations_accept_recommended_undirected_notation(self):
        source = ("@startuml\n" + USECASE_STYLE + 'actor User\nrectangle "Subject" {\n'
                  'usecase "Complete goal" as CU_Main\n}\n')
        for association in ("User -- CU_Main", "User --> CU_Main", "CU_Main <-- User",
                            "User -- CU_Main : participates"):
            with self.subTest(association=association):
                result = self.cli(USECASE, source + association + "\n@enduml\n", "--dominant", "Complete goal")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("not directly associated", result.stdout)
        result = self.cli(USECASE, source + "@enduml\n", "--dominant", "Complete goal")
        self.assertIn("not directly associated", result.stdout)

    def test_outcomes_require_whole_words_not_substrings(self):
        source = ("# CU-01 Complete goal\nPrimary actor: User\nTrigger: The User starts.\n"
                  "Preconditions: Ready.\n## Basic flow\n1. The User submits a request.\n"
                  "2. The System evaluates the request under RN-01.\n"
                  "3. The System returns the result.\n## Postconditions\nThe result is available.\n"
                  "## Business rules\nRN-01: The request must be valid.\n"
                  "## Acceptance criteria\nCA-01: Given valid input, when submitted, then return a result.\n"
                  "## Alternate flows\n| ID | Name | Condition | Behavior |\n"
                  "|---|---|---|---|\n| FA-01 | Unavailable | At step 2 input is unavailable. | %s |\n")
        for action in ("The System displays a warning.", "The System sends a warning.",
                       "The System suspends evaluation."):
            result = self.cli(SPEC, source % action)
            self.assertIn("FA-01 has no declared outcome", result.stdout)
        for action in ("The System ends the use case.", "The System returns to step 2.",
                       "The System displays a warning and ends the use case."):
            result = self.cli(SPEC, source % action)
            self.assertNotIn("FA-01 has no declared outcome", result.stdout)

    def test_markdown_identifier_headings_define_flows_without_defining_substeps(self):
        source = ("# CU-01 Complete goal\nPrimary actor: User\nTrigger: Submit.\n"
                  "Preconditions: Ready.\n## Basic flow\n1. The User submits input.\n"
                  "2. The System returns a result; invalid input follows FA-01.\n"
                  "## Alternate flows\n### FA-01 Invalid input\n"
                  "FA-01.1 The System returns a validation error and ends the use case.\n"
                  "## Postconditions\nA result is returned.\n## Acceptance criteria\n"
                  "Given valid input, when submitted, then return a result.\n")
        result = self.cli(SPEC, source)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FA:1", result.stdout)
        duplicate = self.cli(SPEC, source + "\n### FA-01 Repeated definition\n")
        self.assertEqual(duplicate.returncode, 1, duplicate.stdout + duplicate.stderr)
        self.assertIn("defined 2 times", duplicate.stdout)

    def test_chinese_structural_fields_do_not_require_changing_output_language(self):
        source = ("# CU-01 处理请求\n主参与者：用户\n触发：用户提交请求。\n前置条件：输入已提供。\n"
                  "## 基本流程\n1. 用户提交输入。\n2. 系统返回结果；输入无效时转 FA-01。\n"
                  "## 替代流程\n### FA-01 输入无效\nFA-01.1 系统返回错误并结束本次处理。\n"
                  "## 后置条件\n用户收到结果。\n## 验收标准\n有效输入返回结果，无效输入返回错误。\n")
        result = self.cli(SPEC, source)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Basic-flow steps: 2", result.stdout)
        self.assertIn("FA:1", result.stdout)
        self.assertNotIn("no declared outcome", result.stdout)
        self.assertIn("writing-risk hints cover English/Spanish", result.stdout)
        missing = self.cli(SPEC, source.replace("前置条件：输入已提供。\n", ""))
        self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
        self.assertIn("missing minimum specification field: preconditions", missing.stdout)


if __name__ == "__main__":
    unittest.main()
