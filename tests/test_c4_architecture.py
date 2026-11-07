"""Domain-neutral C4 CLI contracts; no application business requirements."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/mkl-uml-c4-architecture/scripts/validate_c4.py'
SOURCES = {
 'context': '@startuml\n!include <C4/C4_Context>\ntitle Context\nPerson(user, "User")\nSystem(target, "Target")\nRel(user, target, "Uses")\n@enduml\n',
 'container': '@startuml\n!include <C4/C4_Container>\ntitle Containers\nSystem_Boundary(target, "Target") {\nContainer(app, "Application", "Runtime", "Handles input")\nContainerDb(store, "Data", "Storage", "Stores data")\n}\nRel(app, store, "Reads", "Protocol")\n@enduml\n',
 'component': '@startuml\n!include <C4/C4_Component>\ntitle Components\nContainer_Boundary(app, "Application") {\nComponent(entry, "Entry", "Module", "Accepts input")\nComponent(core, "Core", "Module", "Owns behavior")\n}\nRel(entry, core, "Invokes")\n@enduml\n',
 'deployment': '@startuml\n!include <C4/C4_Deployment>\ntitle Deployment\nDeployment_Node(host, "Host", "Environment") {\nContainer(app, "Application", "Runtime", "Handles input")\n}\n@enduml\n'}


class C4Contracts(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for level, source in SOURCES.items():
            (self.root / (level + '.puml')).write_text(source, encoding='utf-8')
        self.record = {
            'schema_version': 1,
            'scope': 'Neutral system design',
            'required_levels': ['context', 'container'],
            'sources': [{'id': 'S1', 'reference': 'Supplied conversation and external evidence'}],
            'requirements': [
                {'id': 'F1', 'kind': 'functional', 'text': 'Preserve the declared input contract', 'source_ids': ['S1'], 'status': 'confirmed'},
                {'id': 'Q1', 'kind': 'quality', 'text': 'Meet the agreed response budget', 'source_ids': ['S1'], 'status': 'confirmed'}],
            'quality_scenarios': [{'id': 'QS1', 'requirement_ids': ['Q1'], 'context': 'Agreed test workload',
                'stimulus': 'Input arrives', 'response': 'Result returned', 'measure': 'Agreed response budget', 'verification': 'Timed boundary test'}],
            'decisions': [{'id': 'D1', 'requirement_ids': ['F1', 'Q1'], 'view_ids': ['V0', 'V1'], 'decision': 'Keep behavior behind the declared interface',
                'rationale': 'Localizes the responsibility', 'tradeoffs': 'A separate seam to maintain', 'status': 'settled'}],
            'views': [{'id': 'V'+str(i), 'level': level, 'status': 'ready', 'artifact': level+'.puml',
                'scope': scope, 'reason': 'Selected to answer the current design question'}
                for i, (level, scope) in enumerate([('context', 'target'), ('container', 'target'), ('component', 'app'), ('deployment', 'host')])],
            'handoff': {'status': 'ready', 'consumer': 'Detailed design', 'notes': 'Use the current views, requirements and decisions'}}

    def invoke(self, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), *map(str, args)], capture_output=True, text=True)

    def record_check(self, strict=True):
        path = self.root / 'architecture.json'
        path.write_text(json.dumps(self.record), encoding='utf-8')
        result = self.invoke('--record', path, *(['--require-ready'] if strict else []))
        self.assertNotIn('Traceback', result.stderr)
        return result

    def test_four_standalone_literal_views(self):
        for level in SOURCES:
            with self.subTest(level=level):
                result = self.invoke(self.root/(level+'.puml'), '--level', level)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                self.assertEqual(json.loads(result.stdout)['coverage']['profile'], 'checked')

    def test_complete_record_ready_without_requiring_prd(self):
        result = self.record_check()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertTrue(json.loads(result.stdout)['ready'])

    def test_selected_unconfirmed_requirement_blocks_until_corrected(self):
        for state in ('open', 'proposed'):
            self.record['requirements'][0]['status'] = state
            self.assertEqual(self.record_check().returncode, 1)
        self.record['requirements'][0]['status'] = 'confirmed'
        self.assertEqual(self.record_check().returncode, 0)

    def test_quality_requirement_needs_scenario_and_verification(self):
        original = copy.deepcopy(self.record)
        for missing in ('scenario', 'measure', 'verification'):
            self.record = copy.deepcopy(original)
            if missing == 'scenario': self.record['quality_scenarios'] = []
            else: self.record['quality_scenarios'][0][missing] = ''
            self.assertEqual(self.record_check().returncode, 1)

    def test_scenario_metadata_is_retained_and_unsettled_status_blocks(self):
        scenario = self.record['quality_scenarios'][0]
        scenario.update(source_ids=['S1'], priority='P1', status='confirmed')
        self.record['requirements'][1]['priority'] = 'P1'
        result = self.record_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for field, value in (('source_ids', ['MISSING']), ('priority', ''), ('status', 'open')):
            old = copy.deepcopy(scenario[field]); scenario[field] = value
            self.assertEqual(self.record_check().returncode, 1)
            scenario[field] = old
        self.assertEqual(self.record_check().returncode, 0)

    def test_requirements_need_decisions_and_settled_choices(self):
        for mutation in ('coverage', 'state'):
            old = copy.deepcopy(self.record)
            if mutation == 'coverage': self.record['decisions'][0]['requirement_ids'] = ['F1']
            else: self.record['decisions'][0]['status'] = 'proposed'
            self.assertEqual(self.record_check().returncode, 1)
            self.record = old

    def test_decision_needs_actual_applicable_view_links(self):
        for links in ([], ['MISSING'], ['VD']):
            self.record['views'].append({'id': 'VD', 'level': 'deployment',
                'status': 'not_applicable', 'scope': 'target', 'reason': 'Excluded scope'})
            self.record['decisions'][0]['view_ids'] = links
            result = self.record_check()
            self.assertEqual(result.returncode, 1)
            self.record['views'].pop()
        self.record['decisions'][0]['view_ids'] = ['V1']
        self.assertEqual(self.record_check().returncode, 0)

    def test_cross_view_label_or_technology_drift_is_rejected(self):
        path = self.root/'deployment.puml'
        for replacement in ('Changed application', 'Other runtime'):
            source = SOURCES['deployment'].replace('Application', replacement) if replacement.startswith('Changed') else SOURCES['deployment'].replace('Runtime', replacement)
            path.write_text(source)
            self.assertEqual(self.record_check().returncode, 1)

    def test_unknown_reference_duplicate_id_and_unknown_field_rejected(self):
        original = copy.deepcopy(self.record)
        for mutation in ('unknown_ref', 'duplicate_id', 'unknown_field'):
            self.record = copy.deepcopy(original)
            if mutation == 'unknown_ref': self.record['requirements'][0]['source_ids'] = ['MISSING']
            elif mutation == 'duplicate_id': self.record['views'][0]['id'] = 'F1'
            else: self.record['extra'] = True
            self.assertEqual(self.record_check().returncode, 1)

    def test_draft_and_nonapplicability_have_distinct_meanings(self):
        self.record['views'][3] = {'id':'VD', 'level':'deployment', 'status':'not_applicable', 'scope':'target', 'reason':'No deployment decision in this scope'}
        self.assertEqual(self.record_check().returncode, 0)
        self.record['views'][3]['reason'] = ''
        self.assertEqual(self.record_check().returncode, 1)
        self.record['views'][3]['reason'] = 'No deployment decision in this scope'
        self.record['views'][0]['status'] = 'draft'
        result = self.record_check(False)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['ready'])
        self.assertEqual(self.record_check().returncode, 1)

    def test_missing_required_view_or_scope_fails(self):
        self.record['views'] = self.record['views'][1:]
        self.assertEqual(self.record_check().returncode, 1)
        self.record['required_levels'] = ['container']
        self.record['views'][0]['scope'] = 'missing'
        self.assertEqual(self.record_check().returncode, 1)

    def test_local_paths_cannot_escape_or_follow_outside_symlinks(self):
        for path in ('../escape.puml', str(self.root/'context.puml')):
            self.record['views'][0]['artifact'] = path
            result = self.record_check()
            self.assertEqual(result.returncode, 1)
            self.assertIn('ARTIFACT_OUTSIDE_ROOT', result.stdout)
        with tempfile.TemporaryDirectory() as outside:
            source = Path(outside)/'outside.puml'
            source.write_text(SOURCES['context'])
            try:
                (self.root/'link.puml').symlink_to(source)
            except (OSError, NotImplementedError):
                return  # Some Windows hosts lack symlink privileges.
            self.record['views'][0]['artifact'] = 'link.puml'
            result = self.record_check()
            self.assertEqual(result.returncode, 1)
            self.assertIn('ARTIFACT_OUTSIDE_ROOT', result.stdout)

    def test_comments_notes_and_legends_cannot_supply_elements(self):
        source = '@startuml\n!include <C4/C4_Context>\ntitle Context\n\' System(fake, "Fake")\nnote "System(fake, x)"\nnote as N\nSystem(other, "Other")\nend note\nlegend\nSystem(also, "Also")\nendlegend\nRel(fake, other, "Calls")\n@enduml\n'
        p = self.root/'notes.puml';p.write_text(source)
        result = self.invoke(p, '--level', 'context')
        self.assertEqual(result.returncode, 1)
        self.assertIn('UNKNOWN_ENDPOINT', result.stdout)

    def test_unknown_syntax_is_partial_and_blocks_strict(self):
        p=self.root/'context.puml'
        p.write_text(SOURCES['context'].replace('@enduml', 'CustomMacro(target)\n@enduml'))
        result=self.invoke(p,'--level','context')
        self.assertEqual(result.returncode,0)
        self.assertEqual(json.loads(result.stdout)['coverage']['profile'],'partial')
        self.assertEqual(self.record_check().returncode,1)

    def test_nonliteral_arguments_and_unknown_display_macros_stay_partial(self):
        path = self.root/'context.puml'
        for declaration in ('System(other, "Other" + suffix + "Name")',
                            'System(other, "Other", $description)',
                            'LAYOUT_UNDEFINED()', 'System_Boundary_Ext(other, "Other")'):
            path.write_text(SOURCES['context'].replace('@enduml', declaration+'\n@enduml'))
            result = self.invoke(path, '--level', 'context', '--require-ready')
            self.assertEqual(result.returncode, 1, declaration)
            self.assertFalse(json.loads(result.stdout)['ready'])

    def test_mixed_levels_duplicate_alias_and_unknown_endpoint_fail(self):
        p=self.root/'context.puml'
        for addition in ('Container(app, "App", "Runtime")', 'System(target, "Again")', 'Rel(target, missing, "Calls")'):
            p.write_text(SOURCES['context'].replace('@enduml',addition+'\n@enduml'))
            self.assertEqual(self.invoke(p,'--level','context').returncode,1)

    def test_multiline_calls_quoted_commas_and_forward_relations(self):
        p=self.root/'context.puml'
        p.write_text('@startuml\n!include <C4/C4_Context>\ntitle Multiline\nRel(user, target, "Calls, safely")\nPerson(\nuser, "User, role"\n)\nSystem(target, "Target")\n@enduml\n')
        self.assertEqual(self.invoke(p,'--level','context').returncode,0)

    def test_remote_include_and_macro_code_are_not_executed(self):
        p=self.root/'context.puml'
        p.write_text(SOURCES['context'].replace('!include <C4/C4_Context>','!includeurl https://example.invalid/remote.puml'))
        self.assertEqual(self.invoke(p,'--level','context').returncode,1)

    def test_malformed_json_shapes_and_duplicate_keys_have_structured_errors(self):
        for value in (None, [], {}, {'schema_version':1, 'views':False}):
            p=self.root/'bad.json';p.write_text(json.dumps(value))
            result=self.invoke('--record',p,'--require-ready')
            self.assertEqual(result.returncode,1,result.stderr)
            self.assertIsInstance(json.loads(result.stdout),dict)
        p.write_text('{"schema_version":1,"schema_version":1}')
        result=self.invoke('--record',p)
        self.assertEqual(result.returncode,2)
        self.assertIn('input_error',json.loads(result.stderr))

    def test_bad_utf8_and_missing_input_report_exit_two(self):
        p=self.root/'bad.puml';p.write_bytes(b'\xff')
        for path in (p,self.root/'missing.puml'):
            result=self.invoke(path,'--level','context')
            self.assertEqual(result.returncode,2)
            self.assertNotIn('Traceback',result.stderr)

    def test_external_containers_and_nested_groups_keep_correct_ownership(self):
        p=self.root/'container.puml'
        source=SOURCES['container'].replace('Container(app,', 'Boundary(group, "Group") {\nContainer(app,').replace('ContainerDb(store,', '}\nContainerDb(store,')
        source=source.replace('@enduml','Container_Ext(peer, "Peer", "Runtime")\nRel(app, peer, "Calls")\n@enduml')
        p.write_text(source)
        self.assertEqual(self.record_check().returncode,0)

    def test_nearest_typed_owner_cannot_be_bypassed_by_outer_scope(self):
        for level, owner, first, second in (
                ('container', 'System_Boundary', 'Container(app,', 'ContainerDb(store,'),
                ('component', 'Container_Boundary', 'Component(entry,', 'Component(core,')):
            for wrapper, expected in ((owner, 1), ('Boundary', 0)):
                with self.subTest(level=level, wrapper=wrapper):
                    source = SOURCES[level].replace(first, wrapper + '(other, "Group") {\n' + first)
                    source = source.replace(second, '}\n' + second)
                    (self.root / (level + '.puml')).write_text(source, encoding='utf-8')
                    result = self.record_check()
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    if expected:
                        self.assertIn('OWNERSHIP_MISMATCH', result.stdout)
                        self.assertFalse(json.loads(result.stdout)['ready'])
            (self.root / (level + '.puml')).write_text(SOURCES[level], encoding='utf-8')

    def test_empty_technology_and_outside_declarations_fail(self):
        p=self.root/'container.puml'
        for source in (SOURCES['container'].replace('"Runtime"','""'), SOURCES['container']+'Container(late, "Late", "Runtime")\n'):
            p.write_text(source)
            self.assertEqual(self.invoke(p,'--level','container').returncode,1)


if __name__ == '__main__':
    unittest.main()
