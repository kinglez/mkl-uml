# Copyright 2026 kingle.zhuang. Organization: mkl.
"""A review cannot approve checks whose indispensable evidence is absent."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/mkl-pdr-review/scripts/validate_pdr.py'


class ReviewCoverage(unittest.TestCase):
    def run_pdr(self, robustness):
        return subprocess.run([sys.executable, str(SCRIPT), '--robustez', str(robustness)],
                              capture_output=True, text=True, timeout=20)

    def test_missing_sources_withhold_acceptance(self):
        result = self.run_pdr(ROOT/'tests/fixtures/pipeline/robustez.puml')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('\n  NOT FULLY VERIFIED\n', result.stdout)
        self.assertNotIn('\n  ACCEPTED WITH REWORK VERIFICATION\n', result.stdout)
        self.assertIn('NOT EXECUTED - domain model missing', result.stdout)
        self.assertIn('NOT EXECUTED - textual specification missing', result.stdout)

    def test_missing_sources_do_not_hide_detected_blocking_defects(self):
        result = self.run_pdr(ROOT/'skills/mkl-pdr-review/tests/examples/sintaxis_mala/robustez.puml')
        self.assertEqual(result.returncode, 1, result.stdout+result.stderr)
        self.assertIn('\n  REINSPECTION REQUIRED\n', result.stdout)


if __name__ == '__main__':
    unittest.main()
