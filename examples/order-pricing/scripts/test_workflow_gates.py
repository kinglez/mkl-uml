"""Acceptance of this worked example's blocking/revalidation behavior only."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

DEMO = Path(__file__).resolve().parents[1]
SKILL_ROOT = Path(os.environ.get("MKL_SKILL_ROOT", str(DEMO.parents[1])))
CHECKER = SKILL_ROOT / 'skills/mkl-uml-c4-architecture/scripts/validate_c4.py'


class WorkflowGates(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        shutil.copytree(DEMO/'architecture', self.root/'architecture',
                        ignore=shutil.ignore_patterns('*.png', '*.svg', '__pycache__'))
        self.path = self.root/'architecture/architecture.json'
        self.record = json.loads(self.path.read_text(encoding='utf-8'))

    def run_gate(self, expected):
        self.path.write_text(json.dumps(self.record), encoding='utf-8')
        proc = subprocess.run([sys.executable, '-B', str(CHECKER), '--record', str(self.path),
                               '--project-root', str(self.root), '--require-ready'], capture_output=True, text=True)
        self.assertEqual(proc.returncode, expected, proc.stdout+proc.stderr)
        self.assertNotIn('Traceback', proc.stderr)
        return json.loads(proc.stdout)

    def test_current_architecture_passes(self):
        self.assertTrue(self.run_gate(0)['ready'])

    def test_unsettled_quality_blocks_then_recovers(self):
        target = next(r for r in self.record['requirements'] if r['id']=='RNF-02')
        target['status']='open'; result=self.run_gate(1)
        self.assertIn('REQUIREMENT_UNSETTLED',str(result['blockers']))
        target['status']='confirmed'; self.run_gate(0)

    def test_missing_required_source_blocks_then_recovers(self):
        p=self.root/'architecture/container.puml'; original=p.read_bytes();p.unlink()
        self.assertIn('ARTIFACT_MISSING',str(self.run_gate(1)['errors']))
        p.write_bytes(original);self.run_gate(0)

    def test_cross_view_drift_blocks_then_recovers(self):
        p=self.root/'architecture/component.puml';original=p.read_text(encoding='utf-8')
        p.write_text(original.replace('Local quoting program','Different program'),encoding='utf-8')
        self.assertIn('CROSS_VIEW_DRIFT',str(self.run_gate(1)['errors']))
        p.write_text(original,encoding='utf-8');self.run_gate(0)

    def test_missing_decision_view_link_blocks_then_recovers(self):
        original=copy.deepcopy(self.record['decisions'][0]['view_ids'])
        self.record['decisions'][0]['view_ids']=[]
        self.assertIn('DECISION_VIEW_REQUIRED',str(self.run_gate(1)['blockers']))
        self.record['decisions'][0]['view_ids']=original;self.run_gate(0)

    def test_shared_helper_consumers_match_actual_code(self):
        data=json.loads((self.root/'architecture/component-code-map.json').read_text(encoding='utf-8'))
        paths={'07-class-model/classes.puml'}
        paths.update(member['path'] for c in data['components'] for member in c['members'])
        for name in paths:
            target=self.root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(DEMO/name,target)
        spec=importlib.util.spec_from_file_location('allocation',DEMO/'scripts/check_architecture.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.assess(self.root,SKILL_ROOT)
        data['shared_helpers'][0]['used_by'].remove('catalog_snapshot')
        (self.root/'architecture/component-code-map.json').write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Shared helper consumers'):
            module.assess(self.root,SKILL_ROOT)

    def reviewed_copy(self):
        record=json.loads((DEMO/'handoffs/architecture.json').read_text(encoding='utf-8'))
        for name in record['inputs_sha256']:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(DEMO/name,p)
        target=self.root/'handoffs/architecture.json';target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(record),encoding='utf-8')
        spec=importlib.util.spec_from_file_location('example_verify',DEMO/'scripts/verify.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module,record,target

    def test_upstream_edit_invalidates_review_then_restoration_recovers(self):
        module,_,_=self.reviewed_copy()
        module.verify_review_baselines(self.root, ('architecture',))
        p=self.root/'architecture/component.puml';original=p.read_bytes();p.write_bytes(original+b'\n')
        with self.assertRaisesRegex(ValueError,'stale'):
            module.verify_review_baselines(self.root, ('architecture',))
        p.write_bytes(original);module.verify_review_baselines(self.root, ('architecture',))

    def test_missing_analysis_edge_cannot_bypass_handoff(self):
        module,record,target=self.reviewed_copy()
        del record['inputs_sha256']['handoffs/analysis.json']
        target.write_text(json.dumps(record),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'handoff input'):
            module.verify_review_baselines(self.root, ('architecture',))


if __name__=='__main__':
    unittest.main()
