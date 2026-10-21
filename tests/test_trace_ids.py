# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Observable identifier lifecycle, independent of diagram display order."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'trace_ids.py'
SPEC = importlib.util.spec_from_file_location('trace_ids', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TraceIdentifiers(unittest.TestCase):
    def fresh(self):
        return {'version': 1, 'namespaces': {}}

    def group(self, registry, namespace='project', prefix='CU'):
        return registry['namespaces'][namespace][prefix]

    def test_reorder_subset_and_new_goal_preserve_existing_ids(self):
        first = MODULE.reconcile(self.fresh(), 'CU', ['reserve-room', 'cancel-reservation'])
        before = copy.deepcopy(first)
        second = MODULE.reconcile(first, 'CU', ['cancel-reservation', 'reserve-room', 'amend-reservation'])
        entries = self.group(second)['assignments']
        self.assertEqual(entries['reserve-room']['id'], 'CU-01')
        self.assertEqual(entries['cancel-reservation']['id'], 'CU-02')
        self.assertEqual(entries['amend-reservation']['id'], 'CU-03')
        self.assertEqual(first, before, 'must not mutate supplied registry')
        partial = MODULE.reconcile(second, 'CU', ['reserve-room'])
        self.assertEqual(second, partial, 'omission from partial work is not retirement')

    def test_retirement_never_frees_an_identifier(self):
        first = MODULE.reconcile(self.fresh(), 'CU', ['old-goal'])
        second = MODULE.reconcile(first, 'CU', ['new-goal'], retire=['old-goal'])
        self.assertEqual(self.group(second)['assignments']['old-goal']['state'], 'retired')
        self.assertEqual(self.group(second)['assignments']['new-goal']['id'], 'CU-02')
        with self.assertRaises(ValueError):
            MODULE.reconcile(second, 'CU', ['old-goal'])

    def test_imported_high_water_is_respected(self):
        first = MODULE.reconcile(self.fresh(), 'CU', ['known-goal'])
        self.group(first)['high_water'] = 20
        second = MODULE.reconcile(first, 'CU', ['new-goal'])
        self.assertEqual(self.group(second)['assignments']['new-goal']['id'], 'CU-21')

    def test_local_flow_namespaces_do_not_collide(self):
        first = MODULE.reconcile(self.fresh(), 'FA', ['payment-refused'], namespace='CU-07')
        second = MODULE.reconcile(first, 'FA', ['no-stock'], namespace='CU-08')
        self.assertEqual(self.group(second, 'CU-07', 'FA')['assignments']['payment-refused']['id'], 'FA-01')
        self.assertEqual(self.group(second, 'CU-08', 'FA')['assignments']['no-stock']['id'], 'FA-01')

    def test_bad_registry_collision_or_counter_is_rejected(self):
        first = MODULE.reconcile(self.fresh(), 'CU', ['a', 'b'])
        bad = copy.deepcopy(first)
        self.group(bad)['assignments']['b']['id'] = 'CU-01'
        with self.assertRaises(ValueError):
            MODULE.reconcile(bad, 'CU', ['c'])
        self.group(first)['high_water'] = 0
        with self.assertRaises(ValueError):
            MODULE.reconcile(first, 'CU', ['c'])

    def test_cli_emits_registry_and_rejects_missing_existing_file(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--prefix', 'CU', '--key', 'reserve-room'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.group(json.loads(result.stdout))['assignments']['reserve-room']['id'], 'CU-01')
        failure = subprocess.run([sys.executable, str(SCRIPT), '--registry', str(ROOT/'absent-registry.json'), '--prefix', 'CU'], capture_output=True, text=True)
        self.assertEqual(failure.returncode, 2)


if __name__ == '__main__':
    unittest.main()
