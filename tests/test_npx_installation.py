# Copyright 2026 kingle.zhuang. Organization: mkl.
"""Exercise the Node entrypoint and the actual npm-packed installation payload."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

from tools.skill_payload import build_payload, skill_names

ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which('node')
NPM = shutil.which('npm')
CLI = ROOT / 'bin/mkl-uml.mjs'


@unittest.skipUnless(NODE, 'Node.js is required for npx installer tests')
class NpxInstallation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='mkl node test ')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.destination = self.directory / 'installed skills'

    def run_cli(self, *args, cli=CLI):
        return subprocess.run([NODE, str(cli), *map(str, args)],
                              cwd=self.directory, capture_output=True, text=True,
                              encoding='utf-8', timeout=30)

    def test_help_does_not_require_installing_anything(self):
        result = self.run_cli('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--agent', result.stdout)
        self.assertIn('--destination', result.stdout)
        self.assertFalse(self.destination.exists())

    def test_installs_all_eight_using_existing_payload_contract(self):
        result = self.run_cli('install', '--agent', 'codex', '--destination', self.destination,
                              '--python', sys.executable)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(sorted(p.name for p in self.destination.iterdir()), skill_names())
        for name in skill_names():
            actual = {p.relative_to(self.destination/name).as_posix(): p.read_bytes()
                      for p in (self.destination/name).rglob('*') if p.is_file()}
            self.assertEqual(actual, build_payload(name))

    def test_installs_only_requested_skill_for_claude_code(self):
        name = 'mkl-uml-domain-modeler'
        result = self.run_cli('install', '--agent', 'claude-code', '--destination', self.destination,
                              '--skill', name, '--python', sys.executable)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual([p.name for p in self.destination.iterdir()], [name])
        self.assertEqual((self.destination/name/'NOTICE').read_bytes(), (ROOT/'NOTICE').read_bytes())

    def test_existing_targets_are_preserved_without_partial_install(self):
        occupied = self.destination/'mkl-uml-sequence-diagram'
        occupied.mkdir(parents=True)
        sentinel = occupied/'keep.txt'
        sentinel.write_text('existing work')
        result = self.run_cli('install', '--agent', 'codex', '--destination', self.destination,
                              '--python', sys.executable)
        self.assertEqual(result.returncode, 2, result.stdout+result.stderr)
        self.assertIn('already exists', result.stderr)
        self.assertEqual(sentinel.read_text(), 'existing work')
        self.assertEqual([p.name for p in self.destination.iterdir()], [occupied.name])

    def test_invalid_options_and_skills_do_not_write(self):
        for flags in [[], ['--agent','unknown'], ['--agent','codex','--unknown'],
                      ['--agent','codex','--skill','../README.md']]:
            with self.subTest(flags=flags):
                result = self.run_cli('install', '--destination', self.destination, *flags)
                self.assertEqual(result.returncode, 2, result.stdout+result.stderr)
                self.assertFalse(self.destination.exists())

    def test_missing_python_has_an_actionable_error(self):
        for executable in [self.directory/'missing-python', '']:
            with self.subTest(executable=str(executable)):
                result = self.run_cli('install', '--agent', 'codex', '--destination', self.destination,
                                      '--python', executable)
                self.assertEqual(result.returncode, 2, result.stdout+result.stderr)
                self.assertIn('Python', result.stderr)
                self.assertFalse(self.destination.exists())

    @unittest.skipUnless(NPM, 'npm is required to verify the packed package')
    def test_packed_package_installs_without_the_source_checkout(self):
        npm = Path(NPM)
        if sys.platform == 'win32':
            npm_command = [NODE, str(npm.parent/'node_modules/npm/bin/npm-cli.js')]
        else:
            npm_command = [str(npm)]
        result = subprocess.run([*npm_command, 'pack', '--ignore-scripts', '--json',
                                 '--cache', str(self.directory/'npm-cache'),
                                 '--pack-destination', str(self.directory)], cwd=ROOT,
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        report = json.loads(result.stdout)
        packed = report[0] if isinstance(report, list) else next(iter(report.values()))
        archive = self.directory/packed['filename']
        extracted = self.directory/'unpacked'
        with tarfile.open(archive) as package:
            members = package.getnames()
            self.assertIn('package/bin/mkl-uml.mjs', members)
            self.assertIn('package/tools/install_skills.py', members)
            self.assertIn('package/LICENSE', members)
            self.assertIn('package/NOTICE', members)
            self.assertFalse(any('__pycache__' in n or '.DS_Store' in n or n.endswith('.pyc') for n in members))
            self.assertFalse(any(n.startswith('package/dist/') for n in members))
            package.extractall(extracted, filter='data')
        result = self.run_cli('install', '--agent', 'codex', '--destination', self.destination,
                              '--python', sys.executable, cli=extracted/'package/bin/mkl-uml.mjs')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(len(list(self.destination.iterdir())), 8)
        for name in skill_names():
            actual = {p.relative_to(self.destination/name).as_posix(): p.read_bytes()
                      for p in (self.destination/name).rglob('*') if p.is_file()}
            self.assertEqual(actual, build_payload(name))
        npx_target = self.directory/'npm exec installed'
        result = subprocess.run([*npm_command, 'exec', '--offline', '--yes', '--cache',
                                 str(self.directory/'npm-cache'), '--package', str(archive), '--',
                                 'mkl-uml', 'install', '--agent', 'codex', '--destination', str(npx_target),
                                 '--python', sys.executable], cwd=self.directory,
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(sorted(p.name for p in npx_target.iterdir()), skill_names())


if __name__ == '__main__':
    unittest.main()
