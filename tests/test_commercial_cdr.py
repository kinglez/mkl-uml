# Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Commercial-readiness regressions through the CDR and header CLIs."""
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CDR = ROOT / "skills/mkl-cdr-review/scripts/validate_cdr.py"
HEADERS = ROOT / "skills/mkl-cdr-review/scripts/generate_code_headers.py"
PIPELINE = ROOT / "tests/fixtures/pipeline"


class CommercialCDRTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.temp = Path(directory.name)

    def write(self, name, text):
        path = self.temp / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, script, *arguments):
        result = subprocess.run([sys.executable, "-B", str(script), *map(str, arguments)],
                                capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertNotIn("Traceback", result.stderr, result.stdout + result.stderr)
        return result

    def cdr(self, **overrides):
        inputs = {"clases": [PIPELINE / "modelo_clases_diseno.puml"],
                  "secuencia": [PIPELINE / "secuencia.puml"],
                  "spec": [PIPELINE / "especificacion.md"],
                  "robustez": [PIPELINE / "robustez.puml"],
                  "dominio": [PIPELINE / "dominio.puml"],
                  "requisitos": [PIPELINE / "requisitos.md"],
                  "pruebas": [PIPELINE / "plan_pruebas.md"]}
        inputs.update(overrides)
        args = [value for key, paths in inputs.items() for path in paths
                for value in ("--" + key, path)]
        return self.run_cli(CDR, *args)

    def headers(self, model):
        return self.run_cli(HEADERS, "--clases", self.write("classes.puml", model))

    def assert_unverified(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PROPOSED VERDICT: NOT FULLY VERIFIED", result.stdout)
        self.assertNotIn("PROPOSED VERDICT: ACCEPTED", result.stdout)

    def test_empty_and_unrecognized_supplied_support_do_not_count_as_checked(self):
        for flag, unrecognized in (("spec", "# Unrelated prose\nNo specified use case.\n"),
                                   ("dominio", "@startuml\n@enduml\n"),
                                   ("requisitos", "# Requirements\nNo identified requirements.\n"),
                                   ("pruebas", "# Plan\nNo identified test cases.\n"),
                                   ("robustez", "@startuml\n@enduml\n")):
            for text in ("", unrecognized):
                with self.subTest(flag=flag, text=text):
                    self.assert_unverified(self.cdr(**{flag: [self.write(flag + ".txt", text)]}))

    def test_each_supplied_spec_and_robustness_must_be_usable(self):
        empty = self.write("empty.txt", "")
        for flag, good in (("spec", "especificacion.md"), ("robustez", "robustez.puml")):
            with self.subTest(flag=flag):
                self.assert_unverified(self.cdr(**{flag: [PIPELINE / good, empty]}))

    def test_html_comments_cannot_supply_requirements_or_test_evidence(self):
        for flag, fixture in (("requisitos", "requisitos.md"), ("pruebas", "plan_pruebas.md"),
                              ("spec", "especificacion.md")):
            text = (PIPELINE / fixture).read_text(encoding="utf-8")
            # Remove the fixture's own attribution comment before wrapping it.
            text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
            for closing in ("\n-->", ""):
                with self.subTest(flag=flag, closed=bool(closing)):
                    path = self.write(flag + ".md", "<!--\n" + text + closing)
                    self.assert_unverified(self.cdr(**{flag: [path]}))

    def test_commented_test_details_cannot_cover_real_controllers_or_flows(self):
        plan = self.write("partial-plan.md", "CP-99: unrelated manual smoke case.\n<!--\n"
                          "Verify Requester Authorization; Resolve Agreement; Calculate Due Date; "
                          "Register Incident; FA-01; FA-02\n-->\n")
        result = self.cdr(pruebas=[plan])
        self.assertIn("Controller 'Verify Requester Authorization' does not appear", result.stdout)
        self.assertIn("Flow FA-01 has no associated test case", result.stdout)

    def test_commented_spec_flows_do_not_create_requirements(self):
        spec = (PIPELINE / "especificacion.md").read_text(encoding="utf-8")
        spec += "\n<!-- FA-99: omitted scratch design -->\n"
        result = self.cdr(spec=[self.write("comments.md", spec)])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("FA-99", result.stdout)

    def test_missing_robustness_withholds_test_coverage_acceptance(self):
        result = self.cdr(robustez=[])
        self.assert_unverified(result)
        self.assertRegex(result.stdout, r"rule 1 \(test plan\): .*robustness")

    def test_scoped_independent_checks_still_report_defects(self):
        model = self.write("scoped.puml", "@startuml\nclass Receiver <<solution>> {\n"
                           "+approve() : void\n}\n@enduml\n")
        seq = self.write("scoped-seq.puml", "@startuml\nparticipant Sender\n"
                         "participant Receiver\nSender -> Receiver : reject()\n@enduml\n")
        result = self.cdr(clases=[model], secuencia=[seq], spec=[], robustez=[],
                          dominio=[], requisitos=[], pruebas=[])
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("approve", result.stdout)
        self.assertIn("rule 3 (types and signatures): executed", result.stdout)

    def test_note_and_comment_classes_are_not_review_targets(self):
        body = "class Ghost <<solution>> {\n+approve() : void\n}\n"
        for hidden in ("note as Summary\n" + body + "end note\n",
                       "hnote over Ghost\n" + body + "end note\n",
                       "rnote as Summary\n" + body + "end note\n",
                       "legend left\n" + body + "endlegend\n",
                       "/'\n" + body + "'/\n", "' class Ghost\n"):
            with self.subTest(hidden=hidden):
                model = self.write("hidden.puml", "@startuml\n" + hidden + "@enduml\n")
                result = self.cdr(clases=[model])
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Classes: 0", result.stdout)
                generated = self.run_cli(HEADERS, "--clases", model)
                self.assertEqual(generated.returncode, 2, generated.stdout)
                self.assertNotIn("public class Ghost", generated.stdout)

    def test_note_declarations_do_not_supply_domain_or_controller_evidence(self):
        for flag, text in (("dominio", "class Incident {\n-id : String\n}\n"),
                           ("robustez", 'control "Register Incident" as C\n')):
            with self.subTest(flag=flag):
                path = self.write(flag + ".puml", "@startuml\nnote as Summary\n" + text
                                  + "end note\n@enduml\n")
                self.assert_unverified(self.cdr(**{flag: [path]}))

    def test_local_flow_ids_cannot_cover_a_different_use_case(self):
        spec = (PIPELINE / "especificacion.md").read_text(encoding="utf-8")
        seq = (PIPELINE / "secuencia.puml").read_text(encoding="utf-8")
        spec08 = self.write("CU08.md", spec.replace("CU-07", "CU-08"))
        # Retain the basic messages, remove all executable branch evidence in CU-08.
        seq08 = "\n".join(line for line in seq.replace("CU-07", "CU-08").splitlines()
                            if not re.match(r"\s*(?:alt|else|end)\b", line)) + "\n"
        result = self.cdr(spec=[PIPELINE / "especificacion.md", spec08],
                          secuencia=[PIPELINE / "secuencia.puml", self.write("CU08.puml", seq08)])
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertRegex(result.stdout, r"RULE #9:.*CU-08.*FA-01")
        self.assertRegex(result.stdout, r"RULE #9:.*CU-08.*FA-02")

    def test_note_title_and_comment_flow_mentions_do_not_prove_design(self):
        seq = (PIPELINE / "secuencia.puml").read_text(encoding="utf-8")
        basic = "\n".join(line for line in seq.splitlines()
                          if not re.match(r"\s*(?:alt|else|end)\b", line))
        for fake in ("note over B_Form\nFA-01 and FA-02 are not yet designed.\nend note\n",
                     "title CU-07 FA-01 FA-02 are not yet designed\n",
                     "' FA-01 FA-02 are not yet designed\n"):
            with self.subTest(fake=fake):
                result = self.cdr(secuencia=[self.write("fake.puml", basic.replace(
                    "@enduml", fake + "@enduml"))])
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("RULE #9:", result.stdout)
                self.assertIn("FA-01", result.stdout)

    def test_else_branch_flow_labels_are_executable_evidence(self):
        seq = (PIPELINE / "secuencia.puml").read_text(encoding="utf-8")
        seq = seq.replace("alt FA-02 category does not exist", "alt category exists")
        seq = seq.replace("else valid category", "else FA-02 unknown category")
        result = self.cdr(secuencia=[self.write("else.puml", seq)])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("RULE #9:", result.stdout)

    def test_ambiguous_duplicate_spec_identity_cannot_be_silently_paired(self):
        copy = self.write("duplicate.md", (PIPELINE / "especificacion.md").read_text(encoding="utf-8"))
        result = self.cdr(spec=[PIPELINE / "especificacion.md", copy])
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertRegex(result.stdout, r"RULE #9:.*CU-07.*(?:ambiguous|multiple)")

    def test_distinct_use_cases_may_reuse_local_flow_ids(self):
        spec08 = self.write("CU08.md", (PIPELINE / "especificacion.md").read_text(
            encoding="utf-8").replace("CU-07", "CU-08"))
        seq08 = self.write("CU08.puml", (PIPELINE / "secuencia.puml").read_text(
            encoding="utf-8").replace("CU-07", "CU-08"))
        result = self.cdr(spec=[PIPELINE / "especificacion.md", spec08],
                          secuencia=[PIPELINE / "secuencia.puml", seq08])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("RULE #9:", result.stdout)

    def test_release_scope_declaration_still_requires_all_sequence_diagrams(self):
        spec = (PIPELINE / "especificacion.md").read_text(encoding="utf-8")
        spec += "\n*This release also includes CU-08 (escalate incident).*\n"
        result = self.cdr(spec=[self.write("release.md", spec)])
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("ENTRY CRITERIA: CU-08", result.stdout)

    def test_nested_cu_heading_identifies_specification_scope(self):
        spec = (PIPELINE / "especificacion.md").read_text(encoding="utf-8")
        spec = spec.replace("# CU-07", "## CU-07")
        result = self.cdr(spec=[self.write("nested.md", spec)])
        self.assertIn("rule 9 (alternative courses): executed", result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_header_destination_cannot_alias_source_file(self):
        original = "@startuml\nclass Order {\n-id : String\n}\n@enduml\n"
        source = self.write("source.puml", original)
        for kind in ("same", "normalized", "symlink", "hardlink"):
            with self.subTest(kind=kind):
                source.write_text(original, encoding="utf-8")
                if kind == "same":
                    dest = source
                elif kind == "normalized":
                    dest = self.temp / "sub" / ".." / source.name
                    (self.temp / "sub").mkdir(exist_ok=True)
                else:
                    dest = self.temp / (kind + ".txt")
                    if kind == "symlink":
                        dest.symlink_to(source)
                    else:
                        os.link(source, dest)
                result = self.run_cli(HEADERS, "--clases", source, "--salida", dest)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_destination_multiplicity_controls_reference_collection_and_optionality(self):
        for relation, expected in (
            ('Order "1" --> "0..*" Item : items', "private List<Item> itemsItem;"),
            ('Order "0..*" <-- "1" Item : orders', "private List<Order> ordersOrder;"),
            ('Order "1" --> "0..1" Item : item', "private Optional<Item> itemItem;"),
            ('Order "1" --> "2..5" Item : items', "private List<Item> itemsItem;"),
            ('Order "1" --> "1" Item : item', "private Item itemItem;")):
            with self.subTest(relation=relation):
                result = self.headers("@startuml\nclass Order\nclass Item\n" + relation + "\n@enduml\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertIn("multiplicity", result.stdout)
                self.assertNotIn("???", result.stdout.split("public class", 1)[1])

    def test_missing_destination_multiplicity_is_exposed(self):
        result = self.headers('@startuml\nclass Order\nclass Item\nOrder "1" --> Item : item\n@enduml\n')
        self.assertIn("Item??? itemItem;", result.stdout)
        self.assertIn("relationship without multiplicity", result.stdout)
        self.assertNotIn("No typing gaps found", result.stdout)

    def test_source_multiplicity_is_preserved_and_validated(self):
        for source, expected in (("2..5", "source multiplicity 2..5"),
                                 ("", "source multiplicity missing"),
                                 ("several", "unsupported source multiplicity 'several'")):
            with self.subTest(source=source):
                marker = '"' + source + '" ' if source else ""
                result = self.headers('@startuml\nclass Order\nclass Item\nOrder ' + marker
                                      + '--> "1" Item : item\n@enduml\n')
                self.assertIn("private Item itemItem;", result.stdout)
                self.assertIn(expected, result.stdout)
                if source in ("", "several"):
                    self.assertNotIn("No typing gaps found", result.stdout)

    def test_generation_writes_a_distinct_destination_without_changing_source(self):
        original = "@startuml\nclass Order {\n-id : String\n}\n@enduml\n"
        source = self.write("source.puml", original)
        dest = self.write("headers.txt", "old output")
        result = self.run_cli(HEADERS, "--clases", source, "--salida", dest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("private String id;", dest.read_text(encoding="utf-8"))
        self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_derived_attribute_keeps_its_type_name_and_meaning(self):
        result = self.headers("@startuml\nclass Cart {\n+/total : Money\n}\n@enduml\n")
        self.assertIn("Money total", result.stdout)
        self.assertIn("derived", result.stdout)

    def test_signal_reception_is_preserved_as_a_classified_review_annotation(self):
        result = self.headers("@startuml\nclass PaymentWebhook <<solution>> {\n"
                              "+<<signal>> paymentCompleted(reservationId : String, outcome : PaymentOutcome)\n"
                              "}\n@enduml\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Signal reception (not an Operation)", result.stdout)
        self.assertIn("+<<signal>> paymentCompleted(reservationId : String, outcome : PaymentOutcome)",
                      result.stdout)
        self.assertIn("language-specific mapping", result.stdout)
        self.assertNotIn("public void paymentCompleted", result.stdout)
        self.assertNotIn("No typing gaps found", result.stdout)

    def test_property_multiplicity_preserves_optionality_collections_and_bounds(self):
        for multiplicity, expected_type in (("0..1", "Optional<String>"),
                                            ("0..*", "List<String>"),
                                            ("2..5", "List<String>"), ("1", "String")):
            with self.subTest(multiplicity=multiplicity):
                result = self.headers("@startuml\nclass Booking {\n"
                                      "-lastCallbackId : String [" + multiplicity + "]\n}\n@enduml\n")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("private " + expected_type + " lastCallbackId;", result.stdout)
                self.assertIn("multiplicity " + multiplicity, result.stdout)

    def test_unsupported_property_multiplicity_cannot_generate_a_clean_report(self):
        result = self.headers("@startuml\nclass Booking {\n"
                              "-lastCallbackId : String [several]\n}\n@enduml\n")
        self.assertIn("lastCallbackId", result.stdout)
        self.assertIn("unsupported property multiplicity 'several'", result.stdout)
        self.assertNotIn("No typing gaps found", result.stdout)

    def test_array_attribute_type_is_not_mistaken_for_property_multiplicity(self):
        result = self.headers("@startuml\nclass Booking {\n-ids : String[]\n}\n@enduml\n")
        self.assertIn("private String[] ids;", result.stdout)
        self.assertIn("No typing gaps found", result.stdout)

    def test_unparsed_modeled_members_are_exposed_in_header_report(self):
        result = self.headers("@startuml\nclass Cart {\n+unsupported -> broken\n}\n@enduml\n")
        self.assertIn("unsupported -> broken", result.stdout)
        self.assertNotIn("No typing gaps found", result.stdout)

    def test_aliases_preserve_associations_and_inheritance(self):
        result = self.headers('@startuml\nclass "Order" as O\nclass "Item" as I\n'
                              'class "Base" as B\nO --|> B\nO "1" --> "0..*" I : items\n@enduml\n')
        self.assertIn("class Order extends Base", result.stdout)
        self.assertIn("private List<Item> itemsItem;", result.stdout)

    def test_alias_inheritance_preserves_cdr_operation_provenance(self):
        model = self.write("inheritance.puml", '@startuml\nclass "Base" as B <<solution>> {\n'
                           '+approve() : void\n}\nclass "Child" as C <<solution>> {\n'
                           '+approve() : void\n}\nC --|> B\n@enduml\n')
        seq = self.write("inheritance-seq.puml", "@startuml\nparticipant Sender\nparticipant Base\n"
                         "Sender -> Base : approve()\n@enduml\n")
        result = self.cdr(clases=[model], secuencia=[seq], spec=[], robustez=[],
                          dominio=[], requisitos=[], pruebas=[])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("wrong class", result.stdout)
        self.assertNotIn("does not come from", result.stdout)

    def test_nested_generic_parameters_and_quoted_defaults_are_not_split(self):
        result = self.headers('@startuml\nclass Loader {\n'
                              '+load(values : Map<String, List<Integer>>, label : String = "a,b") : void\n'
                              '}\n@enduml\n')
        self.assertIn('load(Map<String, List<Integer>> values, String label = "a,b")', result.stdout)
        self.assertNotIn("untyped parameters", result.stdout)

    def test_each_parameter_must_have_a_type(self):
        model = self.write("partial.puml", "@startuml\nclass Receiver <<solution>> {\n"
                           "+approve(known : String, missing) : void\n}\n@enduml\n")
        seq = self.write("partial-seq.puml", "@startuml\nparticipant Sender\nparticipant Receiver\n"
                         "Sender -> Receiver : approve()\n@enduml\n")
        result = self.cdr(clases=[model], secuencia=[seq], spec=[], robustez=[],
                          dominio=[], requisitos=[], pruebas=[])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertRegex(result.stdout, r"RULE #3.*approve.*not typed")

    def test_large_clean_design_is_not_rejected_by_a_findings_quota(self):
        model = (PIPELINE / "modelo_clases_diseno.puml").read_text(encoding="utf-8")
        model = model.replace("@enduml", "skinparam shadowing false\n" * 400 + "@enduml")
        result = self.cdr(clases=[self.write("large.puml", model)])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("REVIEW SELF-TEST", result.stdout)
        self.assertNotIn("superficial", result.stdout)
        self.assertIn("WARNINGS: none", result.stdout)
        self.assertIn("PROPOSED VERDICT: ACCEPTED (subject", result.stdout)


if __name__ == "__main__":
    unittest.main()
