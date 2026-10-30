# Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Flow behavior is evidence in supported prose/table forms, not marker presence."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/mkl-pdr-review/scripts/validate_pdr.py"
MODULE_NAME = "mkl_pdr_table_behavior"
loader = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT)
PDR = importlib.util.module_from_spec(loader)
sys.modules[MODULE_NAME] = PDR
loader.loader.exec_module(PDR)


def specification(flows, cu="CU-07"):
    return (f"# {cu} Quote cart\n\n## Basic flow\n"
            "1. The Shopper submits the Cart through the Quote port.\n"
            "2. The System checks the Cart and returns a PriceQuote.\n\n" + flows)


class PdrTableBehaviorTests(unittest.TestCase):
    def errors(self, flows):
        parsed = PDR.parse_spec("spec.md", specification(flows))
        errors = []
        count = PDR.check_alternos_sin_comportamiento(parsed, errors)
        return parsed, count, errors

    def assert_behavior(self, flows, ids):
        parsed, count, errors = self.errors(flows)
        self.assertEqual(set(ids), set(parsed.flujos))
        self.assertEqual(0, count, errors)
        self.assertEqual([], errors)

    def assert_no_behavior(self, flows):
        parsed, count, errors = self.errors(flows)
        self.assertEqual({"FA-01"}, set(parsed.flujos))
        self.assertEqual(1, count, errors)
        self.assertIn("does not specify system behavior", errors[0])

    def test_real_compact_example_and_numbered_edition_are_equivalent(self):
        example = ROOT / "examples/order-pricing"
        for relative in ("review-history/pdr-initial-specification.md",
                         "03-spec/CU01-quote-cart.md"):
            with self.subTest(edition=relative):
                parsed = PDR.parse_spec(relative, (example / relative).read_text(encoding="utf-8"))
                self.assertEqual(10, len(parsed.flujos))
                errors = []
                self.assertEqual(0, PDR.check_alternos_sin_comportamiento(parsed, errors), errors)

    def test_compact_action_column_establishes_system_subject(self):
        self.assert_behavior("""## Alternative flows
| ID | Condition | System behavior | Outcome |
|---|---|---|---|
| FA-01 | At step 2 the Cart is empty | Reports the empty-Cart reason. | Terminates without a quote. |
| FE-02 | At step 2 the Product is absent | Returns the unknown-Product refusal. | Terminates. |
""", {"FA-01", "FE-02"})

    def test_combined_condition_and_behavior_cell_with_explicit_system(self):
        self.assert_behavior("""## Alternate flows
| ID | Trigger and anchored behavior | Outcome | Source |
|---|---|---|---|
| **FA_1** | At step 2, the System rejects an empty Cart and reports a reason. | Terminates. | RF-01 |
""", {"FA-01"})

    def test_separate_responsible_party_and_action(self):
        self.assert_behavior("""## Exception flows
| ID | Condition | Responsible party | Action | Outcome |
|---|---|---|---|---|
| FE-01 | At step 2 the Cart is empty | System | Reports the empty-Cart reason. | Terminates. |
""", {"FE-01"})

    def test_plural_headers_and_code_formatted_flow_id(self):
        self.assert_behavior("""## Alternative flows
| ID | Conditions | System actions | Outcomes |
|---|---|---|---|
| `FA-01` | At step 2 the Cart is empty | Returns the refusal reason. | Terminates. |
""", {"FA-01"})

    def test_spanish_compact_columns_remain_supported(self):
        self.assert_behavior("""## Flujos alternativos
| ID | Condición | Comportamiento del sistema | Resultado |
|---|---|---|---|
| FA 1 | En paso 2 el carrito está vacío | Devuelve el motivo del rechazo. | Termina el caso de uso. |
""", {"FA-01"})

    def test_outcome_column_can_contain_explicit_system_behavior(self):
        self.assert_behavior("""## Alternative flows
| ID | Name | Condition | Outcome |
|---|---|---|---|
| FA-01 | Empty Cart | At step 2 the Cart is empty | The System rejects the request and ends the use case. |
""", {"FA-01"})

    def test_markdown_code_and_escaped_pipes_preserve_column_positions(self):
        self.assert_behavior("""## Alternative flows
| ID | Condition | Responsible party | Action | Outcome |
|---|---|---|---|---|
| FA-01 | At step 2, compare `a | b` | System | Returns `EMPTY\\|CART` and preserves input. | Terminates. |
""", {"FA-01"})

    def test_empty_or_placeholder_action_is_not_behavior(self):
        for action in ("", "—", "TBD", "System", "The system", "System TBD", "To be specified"):
            with self.subTest(action=action):
                self.assert_no_behavior("## Alternative flows\n"
                    "| ID | Condition | System behavior | Outcome |\n|---|---|---|---|\n"
                    f"| FA-01 | At step 2 the System is unavailable | {action} | Ends. |\n")

    def test_system_token_in_source_column_does_not_supply_action(self):
        self.assert_no_behavior("""## Alternative flows
| ID | Condition | Action | Outcome | Source |
|---|---|---|---|---|
| FA-01 | At step 2 the Cart is empty | TBD | Pending | System returns a refusal in DS-01. |
""")

    def test_source_of_behavior_column_is_still_only_a_reference(self):
        self.assert_no_behavior("""## Alternative flows
| ID | Condition | Source of system behavior | Outcome |
|---|---|---|---|
| FA-01 | At step 2 the Cart is empty | The System rejects requests in DS-01. | Pending |
""")

    def test_test_identifier_alone_is_not_an_action(self):
        self.assert_no_behavior("""## Alternative flows
| ID | Condition | System behavior | Outcome |
|---|---|---|---|
| FA-01 | At step 2 the Cart is empty | CP-01 | Terminates. |
""")

    def test_reference_only_and_annotated_placeholder_cells_are_not_actions(self):
        for action in ("See DS-07", "See DS-07 section 2", "`See DS-07`",
                       "TBD (see CP-01)", "TBD; refer to DS-07", "System TBD (see CP-01)",
                       "TBD - see CP-01", "TBD: see CP-01", "TBD, see CP-01"):
            with self.subTest(action=action):
                self.assert_no_behavior("## Alternative flows\n"
                    "| ID | Condition | System behavior | Outcome |\n|---|---|---|---|\n"
                    f"| FA-01 | At step 2 the Cart is empty | {action} | Terminates. |\n")

    def test_real_action_can_retain_a_reference_annotation(self):
        self.assert_behavior("""## Alternative flows
| ID | Condition | System behavior | Outcome |
|---|---|---|---|
| FA-01 | At step 2 the Cart is empty | Returns a refusal (see CP-01). | Terminates. |
""", {"FA-01"})

    def test_outcome_does_not_fill_a_placeholder_action_column(self):
        self.assert_no_behavior("""## Alternative flows
| ID | Condition | Responsible party | Action | Outcome |
|---|---|---|---|---|
| FA-01 | At step 2 the Cart is empty | System | TBD | The System terminates. |
""")

    def test_traceability_table_is_not_a_flow_definition(self):
        self.assert_no_behavior("""## Traceability
| Flow | System behavior | Test |
|---|---|---|
| FA-01 | The System rejects the request. | CP-01 |
""")

    def test_flow_section_does_not_make_a_test_mapping_action_evidence(self):
        self.assert_no_behavior("""## Alternative flows
| Flow | System behavior | Test |
|---|---|---|
| FA-01 | The System rejects the request. | CP-01 |
""")

    def test_long_traceability_row_does_not_replace_a_numbered_definition(self):
        self.assert_behavior("## Alternative flows\n### FA-01 Empty Cart\n"
            "1. The System rejects the Cart.\n\n## Traceability\n"
            "| Flow | Reference |\n|---|---|\n| FA-01 | "
            + "Source requirement and test links without executable behavior. " * 6
            + " |\n", {"FA-01"})

    def test_flow_subheading_does_not_escape_reference_ancestor(self):
        for body in ("| Step | System behavior | Outcome |\n|---|---|---|\n"
                     "| 1 | The System rejects the request. | Terminates. |\n",
                     "1. The System rejects the request and terminates.\n"):
            with self.subTest(body=body):
                self.assert_no_behavior("## Traceability\n### FA-01 Empty Cart\n" + body)

    def test_nested_reference_definition_cannot_replace_numbered_behavior(self):
        self.assert_behavior("## Alternative flows\n### FA-01 Empty Cart\n"
            "1. The System rejects the Cart.\n\n## Traceability\n"
            "### FA-01 Empty Cart references\n"
            + "Source requirements and test links. " * 12
            + "\n| Step | System behavior | Outcome |\n|---|---|---|\n"
            "| 1 | TBD | Pending |\n", {"FA-01"})

    def test_flow_title_domain_word_is_not_a_reference_section(self):
        self.assert_behavior("""## Alternative flows
### FA-01 Insufficient coverage
1. The System refuses the request and returns the reason.
""", {"FA-01"})

    def test_use_case_goal_word_is_not_a_reference_section(self):
        source = specification("## Alternative flows\n### FA-01 Refused request\n"
                               "1. The System returns the refusal reason.\n")
        source = source.replace("CU-07 Quote cart", "CU-07 Confirm acceptance")
        parsed = PDR.parse_spec("spec.md", source)
        errors = []
        self.assertEqual(0, PDR.check_alternos_sin_comportamiento(parsed, errors), errors)

    def test_heading_and_system_named_only_in_note_are_not_behavior(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
Note: The System will be involved in this scenario.
""")

    def test_html_comment_cannot_supply_missing_behavior(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
<!--
1. The System rejects the Cart and reports a reason.
-->
""")

    def test_quoted_table_is_not_executable_specification_evidence(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
> | ID | System behavior | Outcome |
> |---|---|---|
> | FA-01 | The System rejects the request. | Terminates. |
""")

    def test_fenced_example_cannot_supply_missing_behavior(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
```markdown
1. The System rejects the Cart and reports a reason.
```
""")

    def test_indented_code_cannot_supply_missing_behavior(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
    1. The System rejects the Cart and reports a reason.
""")

    def test_numbered_table_requires_nonplaceholder_action(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
| Step | Responsible party | Action |
|---|---|---|
| FA-01.1 | System | TBD |
""")

    def test_numbered_list_requires_more_than_system_role(self):
        self.assert_no_behavior("""## Alternative flows
### FA-01 Empty Cart
1. The System.
""")

    def test_existing_numbered_english_and_spanish_actions_are_preserved(self):
        self.assert_behavior("""## Alternative flows
**FA-01** Empty Cart; terminates without a quote.
1. The System reports the empty-Cart reason.
### FE-02 Unknown Product
1. El sistema informa al comprador del rechazo.
""", {"FA-01", "FE-02"})

    def test_flow_action_does_not_leak_across_use_cases(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            paths = []
            for cu, action in (("CU-07", "Returns a refusal and preserves the Cart."),
                               ("CU-08", "TBD")):
                rob = folder / (cu + ".puml")
                rob.write_text("@startuml\ntitle " + cu + " Quote cart\n"
                    'actor Shopper\nboundary "Quote port" as Port\ncontrol "Checks Cart" as Check\n'
                    "Shopper -- Port : submits Cart\nPort -- Check : FA-01 returns PriceQuote\n@enduml\n",
                    encoding="utf-8")
                spec = folder / (cu + ".md")
                spec.write_text(specification("## Alternative flows\n"
                    "| ID | Condition | System behavior | Outcome |\n|---|---|---|---|\n"
                    f"| FA-01 | At step 2 the Cart is empty | {action} | Terminates. |\n", cu),
                    encoding="utf-8")
                paths.extend(("--robustez", str(rob), "--spec", str(spec)))
            result = subprocess.run([sys.executable, "-B", str(SCRIPT), *paths],
                capture_output=True, text=True, encoding="utf-8", timeout=20)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            errors = [line for line in result.stdout.splitlines() if "does not specify system behavior" in line]
            self.assertEqual(1, len(errors), result.stdout)
            self.assertIn("CU-08.md", errors[0])
            self.assertNotIn("CU-07.md", errors[0])


if __name__ == "__main__":
    unittest.main()
