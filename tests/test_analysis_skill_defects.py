# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Single-artifact parser regressions exercised through dependency-free CLIs."""
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOMAIN = ROOT / "skills/mkl-uml-domain-modeler/scripts/validate_domain_puml.py"
USECASE = ROOT / "skills/mkl-uml-use-case-diagram/scripts/validate_use_case_puml.py"
SPEC = ROOT / "skills/mkl-use-case-specifier/scripts/validate_use_case_spec.py"
DOMAIN_STYLE = "skinparam linetype ortho\nskinparam classAttributeIconSize 0\nhide methods\nhide empty members\n"
USECASE_STYLE = ("left to right direction\nskinparam linetype ortho\n"
                 "skinparam packageStyle rectangle\nskinparam shadowing false\n")
SPEC_BASE = ("# CU-01 Evaluate request\nPrimary actor: Caller\nTrigger: Submit.\n"
             "Preconditions: Input is available.\n## Basic flow\n"
             "1. The Caller submits input.\n2. The System evaluates input.\n"
             "## Postconditions\nThe result is available.\n## Acceptance criteria\n"
             "Given valid input, when submitted, then a result is returned.\n")


class AnalysisSkillDefects(unittest.TestCase):
    def cli(self, script, text, *flags):
        with tempfile.TemporaryDirectory(prefix="analysis skill ") as directory:
            target = Path(directory) / ("artifact.md" if script == SPEC else "artifact.puml")
            target.write_text(text, encoding="utf-8")
            result = subprocess.run([sys.executable, "-I", "-B", str(script), str(target), *flags],
                                    cwd=directory, capture_output=True, text=True,
                                    encoding="utf-8", timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def assert_exit(self, result, code):
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)

    def domain(self, declaration, member, *flags):
        return self.cli(DOMAIN, "@startuml\n" + DOMAIN_STYLE + declaration + " {\n" + member
                        + "\n}\nclass Kind\nRecord -- Kind : belongs to\n@enduml\n", *flags)

    def test_decorated_domain_classes_cannot_hide_operations(self):
        for declaration in ("class Record #LightBlue", "class Record <<entity>> #LightBlue",
                            'class "Recorded Item" as Record #LightBlue <<entity>>'):
            for flags in ((), ("--profile", "enriched")):
                with self.subTest(declaration=declaration, flags=flags):
                    result = self.domain(declaration, "+evaluate() : String", *flags)
                    self.assert_exit(result, 1)
                    self.assertIn("Operation-like member", result.stdout)

    def test_colored_domain_values_stay_usable(self):
        result = self.domain('class "Recorded Item" as Record #LightBlue', "label")
        self.assert_exit(result, 0)
        self.assertNotIn("no detected relationship", result.stdout)

    def test_strict_domain_types_do_not_depend_on_the_alphabet(self):
        for member in ("name : String", "名称 : 文本", "état : État", "имя : Строка"):
            with self.subTest(member=member):
                strict = self.domain("class Record #LightBlue", member)
                self.assert_exit(strict, 1)
                self.assertIn("Type annotation detected", strict.stdout)
                self.assert_exit(self.domain("class Record #LightBlue", member, "--profile", "enriched"), 0)

    def test_enriched_domain_allows_attributes_and_cardinalities_not_operations(self):
        source = ("@startuml\n" + DOMAIN_STYLE + "class Record {\n+label : String\n}\n"
                  'class Kind\nRecord "0..*" -- "1" Kind : belongs to\n@enduml\n')
        strict = self.cli(DOMAIN, source)
        self.assert_exit(strict, 1)
        self.assertIn("Multiplicity/cardinality", strict.stdout)
        enriched = self.cli(DOMAIN, source, "--profile", "enriched")
        self.assert_exit(enriched, 0)
        self.assertNotIn("no detected relationship", enriched.stdout)

    def usecase(self, declaration, name="Evaluate request", actor_inside=False):
        return self.cli(USECASE, "@startuml\n" + USECASE_STYLE
                        + ("" if actor_inside else "actor Caller\n") + declaration + " {\n"
                        + ("actor Caller\n" if actor_inside else "")
                        + f'usecase "{name}" as CU_Evaluate\n}}\nCaller -- CU_Evaluate\n@enduml\n')

    def test_subject_alias_preserves_scope_validation(self):
        for declaration in ('rectangle "Subject"', 'rectangle "Subject" as Subject'):
            with self.subTest(declaration=declaration):
                self.assert_exit(self.usecase(declaration), 0)
                invalid = self.usecase(declaration, actor_inside=True)
                self.assert_exit(invalid, 1)
                self.assertIn("actor declaration detected inside", invalid.stdout)

    def test_unspaced_cjk_goal_is_not_a_one_word_goal(self):
        for name in ("处理请求", "要求を評価", "요청평가"):
            with self.subTest(name=name):
                result = self.usecase('rectangle "Subject" as Subject', name)
                self.assert_exit(result, 0)
                self.assertNotIn("may be too vague", result.stdout)
        self.assertIn("may be too vague", self.usecase('rectangle "Subject"', "Process").stdout)

    def test_actor_alias_resolution_is_shared_by_participation_checks(self):
        for actor in ('actor "Caller" as ACT_Caller', "actor Caller as ACT_Caller",
                      "actor 参与者 as ACT_Caller"):
            with self.subTest(actor=actor):
                body = ('@startuml\n' + USECASE_STYLE + actor + '\nrectangle "Subject" as Subject {\n'
                        'usecase "Evaluate request" as CU_Evaluate\n}\nACT_Caller -- CU_Evaluate\n@enduml\n')
                result = self.cli(USECASE, body, "--dominant", "Evaluate request")
                self.assert_exit(result, 0)
                self.assertNotIn("no actors declared", result.stdout)
                self.assertNotIn("not directly associated", result.stdout)
                inside = body.replace(actor + "\n", "").replace('as Subject {\n', 'as Subject {\n' + actor + '\n')
                self.assert_exit(self.cli(USECASE, inside), 1)

    def test_empty_specification_fields_and_zero_flow_are_errors(self):
        empty = ("# CU-01 Evaluate request\nPrimary actor:\nTrigger:\nPreconditions:\n"
                 "## Basic flow\n## Postconditions\n## Acceptance criteria\n")
        result = self.cli(SPEC, empty)
        self.assert_exit(result, 1)
        self.assertIn("empty minimum specification field: basic flow", result.stdout)
        self.assertIn("empty minimum specification field: primary actor", result.stdout)
        for body in ("", "1.\n2.\n", "1)\n2)\n", "| Step | Action |\n|---|---|\n", "[TBD]\n",
                     "The following section describes evaluation.\n", "| Step | Action |\n|---|---|\n| 1 | |\n"):
            with self.subTest(body=body):
                source = SPEC_BASE.replace("1. The Caller submits input.\n2. The System evaluates input.\n", body)
                self.assert_exit(self.cli(SPEC, source), 1)

    def test_lean_label_and_table_values_remain_valid(self):
        self.assert_exit(self.cli(SPEC, SPEC_BASE), 0)
        source = ("# CU-01 Evaluate request\n| Field | Value |\n|---|---|\n"
                  "| Primary actor | Caller |\n| Trigger | Submit |\n| Preconditions | Ready |\n"
                  "| Basic flow | 1. Caller submits input. 2. System returns result. |\n"
                  "| Success postcondition | Result available |\n| Acceptance criteria | Valid input returns result |\n")
        self.assert_exit(self.cli(SPEC, source), 0)
        self.assertIn("Basic-flow steps: 2", self.cli(SPEC, source).stdout)
        table = SPEC_BASE.replace("1. The Caller submits input.\n2. The System evaluates input.\n",
                                  "| Step | Action |\n|---|---|\n| 1 | Caller submits input. |\n| 2 | System returns a result. |\n")
        self.assertIn("Basic-flow steps: 2", self.cli(SPEC, table).stdout)

    def test_numbered_multiline_flow_owns_its_chinese_outcome(self):
        source = SPEC_BASE + ("## Alternate flows\n### 1. FA-01 输入无效 ###\n"
                              "1. 系统说明拒绝原因。\n2. 结束本次处理。\n"
                              "### 2. FA-02 未提供输入\n1. 系统显示提示。\n")
        result = self.cli(SPEC, source)
        self.assert_exit(result, 0)
        self.assertNotIn("FA-01 has no declared outcome", result.stdout)
        self.assertIn("FA-02 has no declared outcome", result.stdout)
        self.assertIn("FA:2", result.stdout)

    def test_english_multiline_flow_exit_is_checked_without_id_repetition(self):
        source = SPEC_BASE + ("## Alternate flows\n### FA-01 Invalid input\n"
                              "The System explains the refusal.\nThe use case terminates.\n")
        result = self.cli(SPEC, source)
        self.assert_exit(result, 0)
        self.assertNotIn("has no declared outcome", result.stdout)
        missing = self.cli(SPEC, source.replace("The use case terminates.", "The System displays a warning."))
        self.assertIn("FA-01 has no declared outcome", missing.stdout)

    def test_a_reference_in_another_flow_cannot_supply_an_exit(self):
        source = SPEC_BASE.replace("2. The System evaluates input.",
                                   "2. The System returns a result, or follows FA-01 if invalid.")
        source += "## Alternate flows\n### FA-01 Invalid input\nThe System displays a warning.\n"
        result = self.cli(SPEC, source)
        self.assert_exit(result, 0)
        self.assertIn("FA-01 has no declared outcome", result.stdout)

    def test_a_heading_mention_is_not_a_flow_definition(self):
        source = SPEC_BASE + ("## Alternate flows\n### 1. FA-01 Invalid input\n"
                              "The System displays a warning.\n"
                              "### Notes referring to FA-01\nThe System returns to the Caller.\n")
        result = self.cli(SPEC, source)
        self.assert_exit(result, 0)
        self.assertIn("FA-01 has no declared outcome", result.stdout)

    def test_template_actor_and_steps_are_not_completed_field_values(self):
        for marker in ("[Actor]", "[Primary Actor]", "[Actor Primario]", "[Nombre del actor]"):
            with self.subTest(marker=marker):
                result = self.cli(SPEC, SPEC_BASE.replace("Primary actor: Caller", "Primary actor: " + marker))
                self.assert_exit(result, 1)
                self.assertIn("empty minimum specification field: primary actor", result.stdout)
                self.assertIn("unfilled template markers remain", result.stdout)
        source = SPEC_BASE.replace("1. The Caller submits input.\n2. The System evaluates input.\n",
                                   "1. [Step 1]\n2. [Step 2]\n")
        result = self.cli(SPEC, source)
        self.assert_exit(result, 1)
        self.assertIn("Basic-flow steps: 0", result.stdout)

    def test_role_links_and_business_guards_are_not_template_markers(self):
        for actor in ("[Actor](https://example.invalid/roles/caller)", "[Actor][role]"):
            source = SPEC_BASE.replace("Primary actor: Caller", "Primary actor: " + actor)
            source += "\n[role]: https://example.invalid/roles/caller\n"
            source = source.replace("1. The Caller submits input.", "1. [allowed] The Caller submits input.")
            result = self.cli(SPEC, source)
            self.assert_exit(result, 0)
            self.assertNotIn("unfilled template", result.stdout)

    def test_fenced_examples_cannot_supply_a_specification(self):
        for opener, closer in (("```markdown", "```"), ("  ~~~~text", " ~~~~~"),
                               ("````markdown", "````")):
            with self.subTest(opener=opener):
                result = self.cli(SPEC, opener + "\n" + SPEC_BASE + closer + "\n")
                self.assert_exit(result, 1)
                self.assertIn("missing minimum specification field", result.stdout)
                self.assertIn("Basic-flow steps: 0", result.stdout)
                self.assertNotIn("Defined identifiers:", result.stdout)

    def test_hidden_examples_do_not_supply_ids_steps_or_writing_risks(self):
        hidden = ("# CU-01 Example\nRN-99: database SQL\nFA-99: returns\n"
                  "Primary actor: [Actor]\n1. [Step 1]\n")
        for wrapped in ("```\n" + hidden + "```\n", "<!--\n" + hidden + "-->\n"):
            with self.subTest(wrapped=wrapped[:10]):
                result = self.cli(SPEC, SPEC_BASE + wrapped)
                self.assert_exit(result, 0)
                self.assertIn("Basic-flow steps: 2", result.stdout)
                self.assertNotIn("RN:1", result.stdout)
                self.assertNotIn("defined 2 times", result.stdout)
                self.assertNotIn("implementation detail", result.stdout)
                self.assertNotIn("unfilled template", result.stdout)

    def test_fence_character_length_and_unclosed_fence_follow_commonmark(self):
        hidden = "Primary actor: [Actor]\n1. [Step 1]\n"
        for inner in ("```", "~~~", "```` extra"):
            with self.subTest(inner=inner):
                source = "````markdown\n" + inner + "\n" + hidden + "````\n" + SPEC_BASE
                result = self.cli(SPEC, source)
                self.assert_exit(result, 0)
                self.assertNotIn("unfilled template", result.stdout)
        self.assert_exit(self.cli(SPEC, "~~~\n" + SPEC_BASE), 1)
        # A comment delimiter within a fence is just an example, not a comment
        # that can swallow the real specification after that fence.
        self.assert_exit(self.cli(SPEC, "```\n<!--\n```\n" + SPEC_BASE), 0)

    def test_only_eligible_same_flow_text_supplies_its_outcome(self):
        branch = "## Alternate flows\n### 1. FA-01 Invalid input\nThe System displays a warning.\n"
        for hidden in ("```\nThe use case terminates.\n```\n", "<!-- The use case terminates. -->\n"):
            with self.subTest(hidden=hidden[:10]):
                missing = self.cli(SPEC, SPEC_BASE + branch + hidden)
                self.assert_exit(missing, 0)
                self.assertIn("FA-01 has no declared outcome", missing.stdout)
                found = self.cli(SPEC, SPEC_BASE + branch + hidden + "The use case terminates.\n")
                self.assertNotIn("FA-01 has no declared outcome", found.stdout)

    def test_identifier_definitions_keep_ordinary_sentence_punctuation(self):
        source = SPEC_BASE.replace("2. The System evaluates input.", "2. The System applies RN-01; invalid input follows FA-01.")
        source += ("## Business rules\nRN-01. Input must be valid.\n"
                   "## Alternate flows\nFA-01. The System rejects invalid input.\nThe use case terminates.\n")
        result = self.cli(SPEC, source)
        self.assert_exit(result, 0)
        self.assertIn("RN:1", result.stdout)
        self.assertNotIn("not defined", result.stdout)
        self.assertNotIn("has no declared outcome", result.stdout)

    def test_code_steps_cannot_complete_an_otherwise_empty_basic_flow(self):
        source = SPEC_BASE.replace("1. The Caller submits input.\n2. The System evaluates input.\n",
                                   "```\n1. The Caller submits input.\n```\n")
        result = self.cli(SPEC, source)
        self.assert_exit(result, 1)
        self.assertIn("Basic-flow steps: 0", result.stdout)

    def test_missing_template_resource_is_a_disclosed_partial_check(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "scripts" / SPEC.name
            script.parent.mkdir()
            shutil.copyfile(SPEC, script)
            target = root / "spec.md"
            target.write_text(SPEC_BASE, encoding="utf-8")
            result = subprocess.run([sys.executable, "-I", "-B", str(script), str(target)],
                                    cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=20)
            self.assert_exit(result, 0)
            self.assertIn("template vocabulary unavailable", result.stdout)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
