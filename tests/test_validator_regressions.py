#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
# Modification notice: adds executable MKL validator regression coverage.
"""Exercise validator contracts through their real, dependency-free CLIs."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEQUENCE = ROOT / "skills/mkl-uml-sequence-diagram/scripts/validate_sequence_puml.py"
DESIGN = ROOT / "skills/mkl-uml-design-class-model/scripts/validate_design_class_puml.py"
CDR = ROOT / "skills/mkl-cdr-review/scripts/validate_cdr.py"
DESIGN_GOOD = ROOT / "skills/mkl-uml-design-class-model/tests/examples/bueno"
DIRECTIVES = """skinparam style strictuml
skinparam shadowing false
skinparam responseMessageBelowArrow true
"""
COLLABORATION = "boundary Console\ncontrol Booking\nConsole -> Booking : reserve()\n"


class ValidatorRegressionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.temp = Path(self.directory.name)

    def run_cli(self, script, *arguments):
        return subprocess.run(
            [sys.executable, str(script), *map(str, arguments)],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )

    def sequence(self, text, *flags):
        path = self.temp / "sequence.puml"
        path.write_text(text, encoding="utf-8")
        return self.run_cli(SEQUENCE, "--secuencia", path, *flags)

    def assert_exit(self, result, code):
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def branched_sequence(self, count, prefix="", suffix=""):
        # Each binary alternative doubles paths: 7/8/9 give 128/256/512.
        fragment = """alt accepted
Booking -> Console : accept()
else rejected
Booking -> Console : reject()
end
"""
        return ("@startuml\n" + DIRECTIVES + COLLABORATION + prefix
                + fragment * count + suffix + "@enduml\n")

    def test_balanced_activation_closes_after_seven_eight_and_nine_alternatives(self):
        for count in (7, 8, 9):
            with self.subTest(alternatives=count):
                result = self.sequence(self.branched_sequence(
                    count, "activate Booking\n", "deactivate Booking\n"),
                    "--con-activaciones")
                self.assert_exit(result, 0)
                self.assertNotIn("activation leak", result.stdout)
                if count == 9:
                    self.assertIn("sample, not exhaustively", result.stdout)
                else:
                    self.assertNotIn("sample, not exhaustively", result.stdout)

    def test_activation_leak_in_suffix_after_path_cap_is_detected(self):
        for count in (7, 8, 9):
            with self.subTest(alternatives=count):
                result = self.sequence(self.branched_sequence(
                    count, suffix="activate Booking\n"), "--con-activaciones")
                self.assert_exit(result, 1)
                self.assertIn("activation leak", result.stdout)

    def test_invalid_deactivation_in_suffix_after_path_cap_is_detected(self):
        result = self.sequence(self.branched_sequence(
            9, suffix="deactivate Booking\n"), "--con-activaciones")
        self.assert_exit(result, 1)
        self.assertIn("without an open activation", result.stdout)

    def test_self_call_warning_in_suffix_after_path_cap_is_detected(self):
        result = self.sequence(self.branched_sequence(
            9, suffix="Booking -> Booking : check()\n" * 3))
        self.assert_exit(result, 0)
        self.assertIn("consecutive self-calls", result.stdout)
        self.assertIn("sample, not exhaustively", result.stdout)

    def test_empty_or_malformed_sequence_is_model_error(self):
        cases = {
            "empty file": "",
            "empty diagram": "@startuml\n@enduml\n",
            "missing both markers": DIRECTIVES + COLLABORATION,
            "missing start": COLLABORATION + "@enduml\n",
            "missing end": "@startuml\n" + COLLABORATION,
            "reversed markers": "@enduml\n" + COLLABORATION + "@startuml\n",
            "multiple diagrams": ("@startuml\n" + COLLABORATION + "@enduml\n") * 2,
            "no declarations": "@startuml\nConsole -> Booking : reserve()\n@enduml\n",
            "no messages": "@startuml\nboundary Console\ncontrol Booking\n@enduml\n",
        }
        for label, text in cases.items():
            with self.subTest(label=label):
                self.assert_exit(self.sequence(text), 1)

    def test_comments_and_notes_cannot_supply_a_diagram(self):
        for text in (
            "/'\n@startuml\n" + COLLABORATION + "@enduml\n'/\n",
            "note over Console\n@startuml\n" + COLLABORATION + "@enduml\nend note\n",
            "' @startuml\n' boundary Console\n' control Booking\n' Console -> Booking : reserve()\n' @enduml\n",
        ):
            with self.subTest(text=text):
                self.assert_exit(self.sequence(text), 1)

    def test_comments_and_notes_cannot_supply_a_message(self):
        for hidden in (
            "/'\nConsole -> Booking : reserve()\n'/\n",
            "note over Console\nConsole -> Booking : reserve()\nend note\n",
            "hnote over Console\nConsole -> Booking : reserve()\nend note\n",
            "' Console -> Booking : reserve()\n",
        ):
            with self.subTest(hidden=hidden):
                self.assert_exit(self.sequence("@startuml\nboundary Console\n"
                                               "control Booking\n" + hidden + "@enduml\n"), 1)

    def test_fake_participants_in_comments_or_notes_do_not_satisfy_declarations(self):
        for hidden in (
            "/'\nboundary Console\ncontrol Booking\n'/\n",
            "note over Console\nboundary Console\ncontrol Booking\nend note\n",
        ):
            with self.subTest(hidden=hidden):
                self.assert_exit(self.sequence("@startuml\n" + hidden
                                               + "Console -> Booking : reserve()\n@enduml\n"), 1)

    def test_comment_or_note_content_does_not_create_orphan_or_fragment_errors(self):
        hidden = "/'\nboundary Ghost\nalt phantom\n'/\n"
        hidden += "note over Console\ncontrol Phantom\nalt phantom\nend note\n"
        result = self.sequence("@startuml named_diagram\n" + DIRECTIVES
                               + COLLABORATION + hidden + "@enduml\n")
        self.assert_exit(result, 0)
        self.assertIn("Participants: 2 | Messages: 1", result.stdout)

    def test_usage_errors_keep_exit_two_and_legacy_flags(self):
        self.assert_exit(self.run_cli(SEQUENCE), 2)
        self.assert_exit(self.run_cli(SEQUENCE, "--secuencia", self.temp / "absent.puml"), 2)
        self.assert_exit(self.sequence("@startuml\n" + COLLABORATION + "@enduml\n",
                                       "--con-activaciones"), 0)

    def test_comment_delimiter_inside_a_message_does_not_hide_following_events(self):
        result = self.sequence("@startuml\n" + DIRECTIVES + COLLABORATION
                               + "Booking -> Console : current /' from 2024\n"
                               + "activate Booking\n@enduml\n")
        self.assert_exit(result, 1)
        self.assertIn("activation leak", result.stdout)

    def operation_provenance(self, script, event):
        model = self.temp / "operations.puml"
        model.write_text("@startuml\nclass Receiver <<solution>> {\n"
                         "-id : Integer\n+approve() : void\n}\n@enduml\n", encoding="utf-8")
        sequence = self.temp / "events.puml"
        sequence.write_text("@startuml\nparticipant Sender\nparticipant Receiver\n"
                            + event + "\n@enduml\n", encoding="utf-8")
        return self.run_cli(script, "--clases", model, "--secuencia", sequence)

    def test_only_operation_calls_provide_operation_provenance(self):
        for script in (DESIGN, CDR):
            for event in (
                "Sender -> Receiver : approve()",
                "Receiver <- Sender : approve()",
                "Sender -> Receiver : approve",
                "Sender -> Receiver : <<synchCall>> approve()",
                "Sender ->> Receiver : <<asynchCall>> approve()",
                "Receiver <<- Sender : <<asynchCall>> approve()",
            ):
                with self.subTest(script=script.name, event=event):
                    self.assert_exit(self.operation_provenance(script, event), 0)

    def test_replies_signals_and_lifecycle_events_do_not_supply_operations(self):
        for script in (DESIGN, CDR):
            for event in (
                "Sender --> Receiver : approve()",
                "Receiver <-- Sender : approve()",
                "Sender -> Receiver : <<reply>> approve()",
                "Sender ->> Receiver : <<asynchSignal>> approve()",
                "Sender -> Receiver : approve() <<asynchSignal>>",
                "Sender -> Receiver : <<createMessage>> approve()",
                "Sender -> Receiver : <<deleteMessage>> approve()",
                "Sender -> Receiver ** : approve()",
                "Sender -> Receiver !! : approve()",
                "create Receiver\nSender -> Receiver : approve()",
                "Sender ->x Receiver : approve()",
                "destroy Receiver",
            ):
                with self.subTest(script=script.name, event=event):
                    result = self.operation_provenance(script, event)
                    self.assert_exit(result, 1)
                    if "->x" not in event and not event.startswith("destroy"):
                        self.assertIn("approve", result.stdout)

    def test_ambiguous_async_message_requires_declared_intent(self):
        for script in (DESIGN, CDR):
            with self.subTest(script=script.name):
                result = self.operation_provenance(script, "Sender ->> Receiver : approve()")
                self.assert_exit(result, 1)
                self.assertIn("unresolved asynchronous", result.stdout)

    def test_hidden_messages_cannot_establish_operation_provenance(self):
        for script in (DESIGN, CDR):
            for hidden in (
                "/'\nSender -> Receiver : approve()\n'/",
                "note over Receiver\nSender -> Receiver : approve()\nend note",
            ):
                with self.subTest(script=script.name, hidden=hidden):
                    self.assert_exit(self.operation_provenance(script, hidden), 1)

    def test_create_entity_declaration_counts_the_created_lifeline(self):
        result = self.sequence("@startuml\n" + DIRECTIVES + COLLABORATION
                               + 'create entity "Ticket" as E_Ticket\n'
                               + "Booking -> E_Ticket : <<createMessage>> new Ticket(id)\n@enduml\n")
        self.assert_exit(result, 0)
        self.assertIn("Participants: 3 | Messages: 2", result.stdout)

    def test_create_declaration_does_not_supply_operation_provenance(self):
        for script in (DESIGN, CDR):
            with self.subTest(script=script.name):
                result = self.operation_provenance(
                    script, 'create entity "Receiver" as Created\nSender -> Created : approve()')
                self.assert_exit(result, 1)
                self.assertIn("approve", result.stdout)

    def test_signal_reception_is_parsed_separately_from_operations(self):
        model = self.temp / "receptions.puml"
        model.write_text("@startuml\nclass Webhook <<solution>> {\n"
                         "-- receptions --\n"
                         "+ <<signal>> PaymentResult(purchaseId : String, approved : Boolean, "
                         "reason : String [0..1])\n}\n@enduml\n", encoding="utf-8")
        sequence = self.temp / "signals.puml"
        sequence.write_text("@startuml\nparticipant Sender\nparticipant Webhook\n"
                            "Sender ->> Webhook : <<asynchSignal>> PaymentResult(id, true, reason)\n"
                            "@enduml\n", encoding="utf-8")
        for script in (DESIGN, CDR):
            with self.subTest(script=script.name):
                result = self.run_cli(script, "--clases", model, "--secuencia", sequence)
                self.assert_exit(result, 0)
                self.assertIn("Operations: 0", result.stdout)
                self.assertIn("Receptions: 1", result.stdout)
                self.assertNotIn("could not be parsed", result.stdout)
                self.assertNotIn("CANNOT CERTIFY", result.stdout)

    def test_unknown_member_stereotypes_still_report_unparsed_members(self):
        model = self.temp / "unsupported.puml"
        model.write_text("@startuml\nclass Webhook <<solution>> {\n"
                         "+ <<unknown>> PaymentResult(id : String)\n}\n@enduml\n",
                         encoding="utf-8")
        sequence = self.temp / "signal.puml"
        sequence.write_text("@startuml\nparticipant Sender\nparticipant Webhook\n"
                            "Sender ->> Webhook : <<asynchSignal>> PaymentResult(id)\n@enduml\n",
                            encoding="utf-8")
        for script in (DESIGN, CDR):
            with self.subTest(script=script.name):
                result = self.run_cli(script, "--clases", model, "--secuencia", sequence)
                self.assertIn("PaymentResult", result.stdout)
                self.assertNotIn("Receptions: 1", result.stdout)

    def design(self, text):
        path = self.temp / "alias.puml"
        path.write_text(text, encoding="utf-8")
        return self.run_cli(DESIGN, "--clases", path,
                            "--dominio", DESIGN_GOOD / "dominio.puml",
                            "--secuencia", DESIGN_GOOD / "secuencia.puml",
                            "--spec", DESIGN_GOOD / "especificacion.md")

    def test_class_aliases_preserve_ready_model_and_inheritance_provenance(self):
        original = (DESIGN_GOOD / "modelo_clases_diseno.puml").read_text(encoding="utf-8")
        for declaration in ('class "BookLoan" as BL', "class BookLoan as BL"):
            for inheritance in ("Loan <|-- BL", "BL --|> Loan"):
                with self.subTest(declaration=declaration, inheritance=inheritance):
                    text = original.replace("class BookLoan {", declaration + " {")
                    text = text.replace("Loan <|-- BookLoan", inheritance)
                    result = self.design(text)
                    self.assert_exit(result, 0)
                    self.assertIn("STATUS: READY FOR CDR", result.stdout)
                    self.assertNotIn("another class", result.stdout)

    def test_alias_relationship_endpoints_resolve_to_visible_domain_names(self):
        original = (DESIGN_GOOD / "modelo_clases_diseno.puml").read_text(encoding="utf-8")
        baseline = self.design(original)
        self.assert_exit(baseline, 0)
        aliased = original.replace("class Member {", 'class "Member" as M {')
        aliased = aliased.replace('Member "1" --', 'M "1" --')
        result = self.design(aliased)
        self.assert_exit(result, 0)
        # Alias spelling must not introduce false relationship-provenance warnings.
        self.assertEqual(result.stdout.split("WARNINGS:", 1)[1].split("INFORMATION", 1)[0],
                         baseline.stdout.split("WARNINGS:", 1)[1].split("INFORMATION", 1)[0])


if __name__ == "__main__":
    unittest.main()
