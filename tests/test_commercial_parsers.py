#!/usr/bin/env python3
# Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Commercial audit regressions exercised through the installed-style CLIs."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PDR = ROOT / 'skills/mkl-pdr-review/scripts/validate_pdr.py'
DESIGN = ROOT / 'skills/mkl-uml-design-class-model/scripts/validate_design_class_puml.py'
SEQUENCE = ROOT / 'skills/mkl-uml-sequence-diagram/scripts/validate_sequence_puml.py'
PIPE = ROOT / 'tests/fixtures/pipeline'
DIRECTIVES = ('skinparam style strictuml\nskinparam shadowing false\n'
              'skinparam responseMessageBelowArrow true\n')
COLLABORATION = 'boundary Console\ncontrol Booking\nConsole -> Booking : reserve()\n'


class CommercialParserTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.temp = Path(temporary.name)

    def file(self, name, text):
        path = self.temp / name
        path.write_text(text, encoding='utf-8')
        return path

    def cli(self, script, *arguments):
        return subprocess.run([sys.executable, '-B', str(script), *map(str, arguments)],
                              capture_output=True, text=True, encoding='utf-8', timeout=20)

    def assert_exit(self, result, code):
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def pdr(self, robustness=None, *extra):
        return self.cli(PDR, '--robustez', robustness or PIPE / 'robustez.puml',
                        '--spec', PIPE / 'especificacion.md',
                        '--dominio', PIPE / 'dominio.puml',
                        '--casos-uso', PIPE / 'casos_uso.puml', *extra)

    def test_pdr_annotations_cannot_be_a_complete_target(self):
        body = re.sub(r"/'[\s\S]*?'/", '', (PIPE / 'robustez.puml').read_text(encoding='utf-8'))
        for name, hidden in [('comment', "/'\n" + body + "\n'/"),
                             ('note', 'note as Hidden\n' + body + '\nend note'),
                             ('hnote', 'hnote over Hidden\n' + body + '\nend note'),
                             ('legend', 'legend\n' + body + '\nendlegend')]:
            with self.subTest(annotation=name):
                result = self.pdr(self.file(name + '.puml', '@startuml\n' + hidden + '\n@enduml\n'))
                self.assert_exit(result, 1)
                self.assertIn('no usable', result.stdout)

    def test_design_annotations_cannot_be_a_complete_target(self):
        body = 'class Ghost <<solution>> {\n+approve() : void\n}\n'
        for name, hidden in [('comment', "/'\n" + body + "'/\n"),
                             ('note', 'note as Hidden\n' + body + 'end note\n'),
                             ('rnote', 'rnote over Hidden\n' + body + 'end note\n'),
                             ('legend', 'legend\n' + body + 'endlegend\n')]:
            with self.subTest(annotation=name):
                result = self.cli(DESIGN, '--clases', self.file(name + '.puml', '@startuml\n' + hidden + '@enduml\n'))
                self.assert_exit(result, 1)
                self.assertIn('Classes: 0', result.stdout)

    def test_inline_notes_do_not_hide_following_real_declarations(self):
        design = self.file('real.puml', '@startuml\nnote "summary" as N\n'
                           'class Real <<solution>> {\n-id : Integer\n}\n@enduml\n')
        result = self.cli(DESIGN, '--clases', design)
        self.assert_exit(result, 0)
        self.assertIn('Classes: 1', result.stdout)
        rob = self.file('real-rob.puml', '@startuml\nnote right : summary\n'
                        'boundary Console\ncontrol Booking\nConsole -- Booking : reserve\n@enduml\n')
        self.assert_exit(self.cli(PDR, '--robustez', rob), 0)

    def test_hidden_declarations_do_not_shift_real_source_locations(self):
        model = self.file('locations.puml', '@startuml\n/\'\nclass Fake {\n}\n\'/\n'
                          'note as N\nclass Phantom {\n}\nend note\n'
                          'class Real <<solution>> {\n+issue() : void\n}\n@enduml\n')
        sequence = self.file('unrelated.puml', '@startuml\nparticipant A\nparticipant Real\nA -> Real : unrelated()\n@enduml\n')
        result = self.cli(DESIGN, '--clases', model, '--secuencia', sequence)
        self.assert_exit(result, 1)
        self.assertIn('Classes: 1', result.stdout)
        self.assertIn('L11:', result.stdout)

    def test_pdr_each_supplied_specification_requires_a_robustness_pair(self):
        extra = self.file('cu08.md', (PIPE / 'especificacion.md').read_text(encoding='utf-8').replace('CU-07', 'CU-08'))
        result = self.pdr(None, '--spec', extra)
        self.assert_exit(result, 0)
        self.assertIn(str(extra), result.stdout)
        self.assertIn('unpaired specification', result.stdout)
        self.assertIn('NOT FULLY VERIFIED', result.stdout)

    def test_pdr_explicit_mismatched_cu_ids_do_not_pair_by_position(self):
        rob = self.file('cu99.puml', (PIPE / 'robustez.puml').read_text(encoding='utf-8').replace('CU-07', 'CU-99'))
        result = self.pdr(rob)
        self.assert_exit(result, 0)
        self.assertIn('NOT FULLY VERIFIED', result.stdout)
        self.assertIn('unpaired specification', result.stdout)

    def test_pdr_duplicate_cu_specs_are_ambiguous(self):
        duplicate = self.file('duplicate.md', (PIPE / 'especificacion.md').read_text(encoding='utf-8'))
        result = self.pdr(None, '--spec', duplicate)
        self.assert_exit(result, 0)
        self.assertIn('ambiguous', result.stdout)
        self.assertIn('NOT FULLY VERIFIED', result.stdout)

    def test_pdr_empty_supporting_inputs_withhold_acceptance(self):
        empty = self.file('empty.txt', '')
        for flag in ('--spec', '--dominio', '--casos-uso'):
            with self.subTest(flag=flag):
                flags = ['--robustez', PIPE / 'robustez.puml', '--spec', PIPE / 'especificacion.md',
                         '--dominio', PIPE / 'dominio.puml', '--casos-uso', PIPE / 'casos_uso.puml']
                flags[flags.index(flag) + 1] = empty
                result = self.cli(PDR, *flags)
                self.assert_exit(result, 0)
                self.assertIn('NOT FULLY VERIFIED', result.stdout)

    def test_pdr_table_alternate_substeps_are_behavior(self):
        spec = ROOT / 'skills/mkl-use-case-specifier/tests/examples/spec_subpasos.md'
        rob = self.file('renew.puml', '@startuml\ntitle CU-05 Renew loan\n'
                        'actor Student\nboundary "Library Portal" as Portal\n'
                        'control "Checks Loan Reservation Return Date" as Renew\n'
                        'entity Loan\nentity Reservation\nStudent -- Portal : confirms renewal\n'
                        'Portal -- Renew : displays Loan List records Return Date\n'
                        'Renew -- Loan : renewal\nRenew -- Reservation : FA-01\n@enduml\n')
        result = self.cli(PDR, '--robustez', rob, '--spec', spec)
        self.assert_exit(result, 0)
        self.assertNotIn('does not specify system behavior', result.stdout)

    def test_design_ordinary_prefixes_are_not_accessor_exemptions(self):
        model = self.file('ticket.puml', '@startuml\nclass Ticket <<solution>> {\n'
                          '-id : Integer\n+issue() : void\n+settle() : void\n+isla() : void\n+hasta() : void\n}\n@enduml\n')
        sequence = self.file('ticket-sequence.puml', '@startuml\nparticipant Sender\nparticipant Ticket\nSender -> Ticket : unrelated()\n@enduml\n')
        result = self.cli(DESIGN, '--clases', model, '--secuencia', sequence)
        self.assert_exit(result, 1)
        for name in ('issue', 'settle', 'isla', 'hasta'):
            self.assertIn('Ticket.' + name + '()', result.stdout)
        self.assertNotIn('accessor(s)', result.stdout)

    def test_design_each_parameter_needs_its_own_type(self):
        model = self.file('mixed.puml', '@startuml\nclass Ticket <<solution>> {\n'
                          '+approve(known : Map<String, Integer>, missing) : void\n}\n@enduml\n')
        result = self.cli(DESIGN, '--clases', model)
        self.assert_exit(result, 0)
        self.assertIn('not typed', result.stdout)
        self.assertIn('missing', result.stdout)

    def test_design_generic_parameters_and_quoted_defaults_stay_intact(self):
        model = self.file('typed.puml', '@startuml\nclass Ticket <<solution>> {\n'
                          '+approve(known : Map<String, List<Integer>>, label : String = "x,y") : void\n}\n@enduml\n')
        result = self.cli(DESIGN, '--clases', model)
        self.assert_exit(result, 0)
        self.assertNotIn('not typed', result.stdout)

    def sequence(self, suffix):
        return self.cli(SEQUENCE, '--secuencia', self.file('sequence.puml',
                        '@startuml\n' + DIRECTIVES + COLLABORATION + suffix + '@enduml\n'), '--con-activaciones')

    def test_sequence_stray_else_cannot_hide_following_activation(self):
        result = self.sequence('else impossible\nactivate Booking\n')
        self.assert_exit(result, 1)
        self.assertIn("'else'", result.stdout)
        self.assertIn('activation leak', result.stdout)

    def test_sequence_else_requires_an_alt_or_par_fragment(self):
        for kind in ('opt', 'loop', 'critical', 'break', 'group'):
            with self.subTest(kind=kind):
                result = self.sequence(kind + ' condition\nelse invalid\nBooking -> Console : reject()\nend\n')
                self.assert_exit(result, 1)
                self.assertIn("'else'", result.stdout)
        for kind in ('alt', 'par'):
            with self.subTest(kind=kind):
                self.assert_exit(self.sequence(kind + ' first\nBooking -> Console : accept()\nelse second\nBooking -> Console : reject()\nend\n'), 0)

    def test_sequence_autoactivate_off_restores_manual_validation(self):
        result = self.sequence('autoactivate on\nBooking -> Console : status()\nautoactivate off\ndeactivate Booking\n')
        self.assert_exit(result, 1)
        self.assertIn('without an open activation', result.stdout)
        result = self.sequence('autoactivate on\nBooking -> Console : status()\nautoactivate off\nactivate Booking\n')
        self.assert_exit(result, 1)
        self.assertIn('activation leak', result.stdout)

    def test_sequence_balanced_manual_region_after_autoactivate_off_is_valid(self):
        result = self.sequence('autoactivate on\nBooking -> Console : status()\nautoactivate off\nactivate Booking\ndeactivate Booking\n')
        self.assert_exit(result, 0)
        self.assertNotIn('there are no manual pairs', result.stdout)

    def test_reply_warning_preserves_asynchronous_message_semantics(self):
        result = self.sequence('Booking --> Console : reserved\nBooking --> Console : shown\n')
        self.assert_exit(result, 0)
        self.assertIn('messages are returns', result.stdout)
        self.assertNotIn('asynchronous return', result.stdout)
        self.assertIn('Signal', result.stdout)

    def test_input_failures_use_exit_two_without_tracebacks(self):
        invalid = self.temp / 'invalid.puml'
        invalid.write_bytes(b'\xff\xfe')
        for script, flag in ((PDR, '--robustez'), (DESIGN, '--clases'), (SEQUENCE, '--secuencia')):
            for path in (invalid, self.temp):
                with self.subTest(script=script.name, path=str(path)):
                    self.assert_exit(self.cli(script, flag, path), 2)


if __name__ == '__main__':
    unittest.main()
