#!/usr/bin/env python3
# English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution.
"""Run each skill validator against its example fixtures as a CI smoke check.

This checks execution, not the semantic accuracy of reported findings. Both
exit 0 (no findings) and exit 1 (findings reported) are valid for these fixtures,
which deliberately include invalid models. A traceback or an unexpected exit
status fails the check. Review expected findings separately when changing rules.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

# Validators accepting one positional input path.
POSITIONAL = {
    "mkl-uml-domain-modeler": ("scripts/validate_domain_puml.py", "tests/examples/*.puml"),
    "mkl-uml-use-case-diagram": ("scripts/validate_use_case_puml.py", "tests/examples/*.puml"),
    "mkl-use-case-specifier": ("scripts/validate_use_case_spec.py", "tests/examples/*.md"),
    "mkl-uml-robustness-diagram": ("scripts/validate_robustness_puml.py", "tests/examples/*.puml"),
}

# Validators accepting several artifacts via CLI flags, one set per scenario
# under tests/examples/<scenario>/. Legacy flags and fixture names are retained
# for compatibility with each validator.
MULTI_INPUT = {
    "mkl-pdr-review": ("scripts/validate_pdr.py", {
        "--dominio": "dominio.puml",
        "--casos-uso": "casos_uso.puml",
        "--robustez": "robustez.puml",
        "--spec": "especificacion.md",
    }),
    "mkl-uml-sequence-diagram": ("scripts/validate_sequence_puml.py", {
        "--secuencia": "secuencia.puml",
        "--robustez": "robustez.puml",
        "--spec": "especificacion.md",
        "--dominio": "dominio.puml",
    }),
    "mkl-uml-design-class-model": ("scripts/validate_design_class_puml.py", {
        "--clases": "modelo_clases_diseno.puml",
        "--dominio": "dominio.puml",
        "--secuencia": "secuencia.puml",
        "--spec": "especificacion.md",
    }),
    "mkl-cdr-review": ("scripts/validate_cdr.py", {
        "--clases": "modelo_clases_diseno.puml",
        "--secuencia": "secuencia.puml",
        "--spec": "especificacion.md",
        "--robustez": "robustez.puml",
        "--dominio": "dominio.puml",
        "--requisitos": "requisitos.md",
        "--pruebas": "plan_pruebas.md",
    }),
}

# Required flags for each multi-input validator.
REQUIRED_FLAGS = {
    "mkl-pdr-review": {"--robustez"},
    "mkl-uml-sequence-diagram": {"--secuencia"},
    "mkl-uml-design-class-model": {"--clases"},
    "mkl-cdr-review": {"--clases", "--secuencia"},
}

ALL_SKILLS = sorted(set(POSITIONAL) | set(MULTI_INPUT))


def run(cmd, cwd):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    crashed = "Traceback (most recent call last)" in proc.stderr
    return proc.returncode, crashed, proc.stderr


def report(skill, label, code, crashed, err):
    if crashed:
        print(f"[{skill}] CRASH in {label}\n{err}")
        return False
    if code not in (0, 1):
        print(f"[{skill}] unexpected exit code ({code}) in {label}\n{err}")
        return False
    print(f"[{skill}] OK {label} (exit {code})")
    return True


def check_positional(skill, script_rel, glob_pat):
    skill_dir = SKILLS / skill
    script = skill_dir / script_rel
    fixtures = sorted(skill_dir.glob(glob_pat))
    if not fixtures:
        print(f"[{skill}] WARNING: no fixtures found ({glob_pat})")
        return True
    ok = True
    for fixture in fixtures:
        code, crashed, err = run([sys.executable, str(script), str(fixture)], skill_dir)
        ok &= report(skill, fixture.name, code, crashed, err)
    return ok


def check_multi_input(skill, script_rel, flag_map):
    skill_dir = SKILLS / skill
    script = skill_dir / script_rel
    examples_dir = skill_dir / "tests" / "examples"
    scenarios = sorted(p for p in examples_dir.iterdir() if p.is_dir()) if examples_dir.is_dir() else []
    if not scenarios:
        print(f"[{skill}] WARNING: no test scenarios found")
        return True
    required = REQUIRED_FLAGS.get(skill, set())
    ok = True
    for scenario in scenarios:
        cmd = [sys.executable, str(script)]
        missing_required = False
        for flag, filename in flag_map.items():
            fixture = scenario / filename
            if fixture.exists():
                cmd += [flag, str(fixture)]
            elif flag in required:
                missing_required = True
                print(f"[{skill}] {scenario.name}: missing {filename}, required by {flag}")
        if missing_required:
            ok = False
            continue
        code, crashed, err = run(cmd, skill_dir)
        ok &= report(skill, scenario.name, code, crashed, err)
    return ok


def check_structure():
    ok = True
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        readme = skill_dir / "README.md"
        if not skill_md.exists():
            ok = False
            print(f"[{skill_dir.name}] missing SKILL.md")
        if not readme.exists():
            ok = False
            print(f"[{skill_dir.name}] missing README.md")
        if skill_dir.name not in ALL_SKILLS:
            print(f"[{skill_dir.name}] WARNING: directory not recognized by run_all_validators.py")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skill", choices=ALL_SKILLS, help="run the validator for one skill")
    ap.add_argument("--check-structure", action="store_true",
                     help="check that each directory under skills/ contains SKILL.md and README.md")
    args = ap.parse_args()

    if args.check_structure:
        sys.exit(0 if check_structure() else 1)

    targets = [args.skill] if args.skill else ALL_SKILLS
    ok = True
    for skill in targets:
        if skill in POSITIONAL:
            script_rel, glob_pat = POSITIONAL[skill]
            ok &= check_positional(skill, script_rel, glob_pat)
        else:
            script_rel, flag_map = MULTI_INPUT[skill]
            ok &= check_multi_input(skill, script_rel, flag_map)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
