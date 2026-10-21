#!/usr/bin/env node
// Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE for attribution.
// Keep installation semantics in the shared Python installer.
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const root = fileURLToPath(new URL('../', import.meta.url));
const help = `MKL UML skill installer

Usage:
  mkl-uml install --agent codex|claude-code [options]

Options:
  --agent NAME         codex or claude-code (required for install)
  --skill NAME         Install one skill; omit to install all eight
  --destination PATH   Override the agent's personal skills directory
  --python PATH        Python 3.9+ executable; otherwise auto-detected
  --help               Show this help
  --version            Show the package version

Existing target directories are never overwritten.
`;

function fail(message) {
  process.stderr.write(`ERROR: ${message}\n`);
  process.exit(2);
}

let args;
try {
  args = parseArgs({
    allowPositionals: true,
    options: {
      agent: { type: 'string' },
      skill: { type: 'string' },
      destination: { type: 'string' },
      python: { type: 'string' },
      help: { type: 'boolean', short: 'h' },
      version: { type: 'boolean', short: 'v' },
    },
  });
} catch (error) {
  fail(error.message);
}

if (args.values.help) {
  process.stdout.write(help);
  process.exit(0);
}
if (args.values.version) {
  process.stdout.write(`${JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version}\n`);
  process.exit(0);
}
if (args.positionals.length !== 1 || args.positionals[0] !== 'install') {
  fail('Use "mkl-uml install --agent codex|claude-code". See --help.');
}
const agentDirectories = {
  codex: join(homedir(), '.agents', 'skills'),
  'claude-code': join(homedir(), '.claude', 'skills'),
};
if (!Object.hasOwn(agentDirectories, args.values.agent ?? '')) {
  fail('--agent must be codex or claude-code.');
}
if (args.values.destination !== undefined && !args.values.destination.trim()) {
  fail('--destination must not be empty.');
}
if (args.values.skill !== undefined && !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.values.skill)) {
  fail('Invalid skill name.');
}

if (args.values.python !== undefined && !args.values.python.trim()) {
  fail('Python executable path must not be empty.');
}

const candidates = args.values.python !== undefined
  ? [[args.values.python]]
  : process.platform === 'win32' ? [['py', '-3'], ['python'], ['python3']] : [['python3'], ['python']];
let python;
for (const candidate of candidates) {
  const probe = spawnSync(candidate[0], [...candidate.slice(1), '-c',
    'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'],
    { stdio: 'ignore', timeout: 10000 });
  if (probe.status === 0) {
    python = candidate;
    break;
  }
}
if (!python) {
  fail('Python 3.9+ is required. Install Python or pass --python /path/to/python.');
}

const destination = args.values.destination ?? agentDirectories[args.values.agent];
const arguments_ = [...python.slice(1), join(root, 'tools', 'install_skills.py'),
  '--destination', destination];
if (args.values.skill !== undefined) arguments_.push(args.values.skill);
const result = spawnSync(python[0], arguments_, {
  stdio: 'inherit',
  env: { ...process.env, PYTHONUTF8: '1', PYTHONDONTWRITEBYTECODE: '1' },
});
if (result.error) fail(`Could not run the Python installer: ${result.error.message}`);
process.exit(result.status ?? 1);
