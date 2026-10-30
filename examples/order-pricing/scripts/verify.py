"""Verify the published order-pricing example from any working directory."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

DEMO = Path(__file__).resolve().parents[1]


def text_sha256(path):
    """Keep reviewed text hashes stable across Git LF/CRLF checkouts."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=DEMO.parents[1],
                        help="MKL UML repository root; inferred from this checkout by default")
    parser.add_argument("--render", action="store_true",
                        help="Also check PlantUML syntax and regenerate SVG/PNG with local PlantUML")
    args = parser.parse_args()
    source = args.skill_root.resolve()
    logs = DEMO / "validation" / "latest"
    logs.mkdir(parents=True, exist_ok=True)
    results = []
    # A failed/interrupted rerun must not leave a previous PASS looking current.
    (logs / "result.json").write_text(json.dumps({
        "checked_at": datetime.now(timezone.utc).isoformat(), "passed": False,
        "status": "RUNNING", "human_approval": False,
        "formal_gate_disposition": "NOT FULLY VERIFIED"
    }, indent=2) + "\n", encoding="utf-8")

    def run(name, command, cwd=DEMO, extra_env=None):
        command = list(map(str, command))
        environment = dict(os.environ, PYTHONUTF8="1")
        environment.update(extra_env or {})
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                                encoding="utf-8", timeout=120, env=environment)
        content = "COMMAND: " + json.dumps(command) + "\nEXIT: " + str(result.returncode)
        if extra_env:
            content += "\nENVIRONMENT OVERRIDES: " + json.dumps(extra_env)
        content += "\nSTDOUT:\n" + result.stdout + "\nSTDERR:\n" + result.stderr
        (logs / (name + ".log")).write_text(content, encoding="utf-8")
        record = {"name": name, "exit_code": result.returncode,
                  "passed": result.returncode == 0,
                  "log": "validation/latest/" + name + ".log"}
        results.append(record)
        print(("PASS" if record["passed"] else "FAIL") + " " + name, flush=True)
        return result

    def cli(name, skill, filename, flags):
        return run(name, [sys.executable, "-B", source / "skills" / skill / "scripts" / filename, *flags])

    source_record = json.loads((DEMO / "SKILL_SOURCE.json").read_text(encoding="utf-8"))
    for path, expected in source_record["runtime_sha256"].items():
        actual = text_sha256(source / path)
        if actual != expected:
            raise ValueError("Skill runtime differs from the reviewed baseline: " + path)
    for stage in ("analysis", "design"):
        record = json.loads((DEMO / "handoffs" / (stage + ".json")).read_text(encoding="utf-8"))
        for path, expected in record["inputs_sha256"].items():
            actual = text_sha256(DEMO / path)
            if actual != expected:
                raise ValueError(stage + " review is stale after artifact change: " + path)
        if record["human_approval"] is not False:
            raise ValueError("This teaching example does not claim formal human approval")

    domain = DEMO / "01-domain/domain.puml"
    use_cases = DEMO / "02-use-cases/use-cases.puml"
    spec = DEMO / "03-spec/CU01-quote-cart.md"
    robustness = DEMO / "04-robustness/robustness.puml"
    sequences = sorted((DEMO / "06-interactions").glob("*.puml"))
    classes = DEMO / "07-class-model/classes.puml"
    if not sequences:
        raise ValueError("No reviewed sequence diagrams")
    scope_record = json.loads((DEMO / "06-interactions/sequence-scope.json").read_text(encoding="utf-8"))
    if scope_record.get("schema_version") != 1:
        raise ValueError("Unsupported sequence scope manifest")
    scopes = scope_record["sequences"]
    if set(scopes) != {path.name for path in sequences}:
        raise ValueError("Every sequence must have an explicit, reviewed scope")
    if not any(item.get("scope") == "use-case" and "CU-01" in item.get("use_cases", [])
               for item in scopes.values()):
        raise ValueError("A complete CU-01 sequence is required")
    sequence_flags = [item for path in sequences for item in ("--secuencia", path)]
    cli("01-domain", "mkl-uml-domain-modeler", "validate_domain_puml.py", [domain])
    cli("02-use-cases", "mkl-uml-use-case-diagram", "validate_use_case_puml.py", [use_cases])
    cli("03-specification", "mkl-use-case-specifier", "validate_use_case_spec.py", [spec])
    cli("04-robustness", "mkl-uml-robustness-diagram", "validate_robustness_puml.py",
        [robustness, "--domain", domain])
    cli("05-pdr", "mkl-pdr-review", "validate_pdr.py",
        ["--robustez", robustness, "--spec", spec, "--dominio", domain, "--casos-uso", use_cases])
    for index, sequence in enumerate(sequences, start=1):
        scope = scopes[sequence.name]
        support = ["--dominio", domain]
        if scope.get("scope") == "use-case":
            support += ["--spec", spec, "--robustez", robustness]
        elif scope.get("scope") != "technical-probe" or not scope.get("requirements") or not scope.get("reason"):
            raise ValueError("Unsupported or unjustified sequence scope: " + sequence.name)
        cli("06-sequence-" + str(index), "mkl-uml-sequence-diagram", "validate_sequence_puml.py",
            ["--secuencia", sequence, *support])
    cli("07-classes", "mkl-uml-design-class-model", "validate_design_class_puml.py",
        ["--clases", classes, *sequence_flags, "--spec", spec, "--dominio", domain])
    cli("08-cdr", "mkl-cdr-review", "validate_cdr.py",
        ["--clases", classes, *sequence_flags, "--spec", spec, "--dominio", domain,
         "--robustez", robustness, "--requisitos", DEMO / "00-input/requirements.md",
         "--pruebas", DEMO / "06-interactions/test-plan.md"])
    header_result = cli("08-headers", "mkl-cdr-review", "generate_code_headers.py",
                        ["--clases", "07-class-model/classes.puml", "--id", "CDR-01",
                         "--salida", logs / "headers.generated.java"])
    if header_result.returncode == 0:
        fresh = (logs / "headers.generated.java").read_text(encoding="utf-8")
        if fresh != (DEMO / "08-cdr/headers.java").read_text(encoding="utf-8"):
            raise ValueError("Reviewed headers differ from fresh generation; reinspection is required")
    test_result = run("09-reference-tests", [sys.executable, "-B", "-m", "unittest",
                      "discover", "-s", "tests", "-v"], DEMO / "09-reference-implementation")
    run("09-visible-examples", [sys.executable, "-B", "run_example.py"],
        DEMO / "09-reference-implementation")
    run("09-extension", [sys.executable, "-B", "extension_demo.py"],
        DEMO / "09-reference-implementation")
    test_count = re.search(r"Ran (\d+) tests?", test_result.stderr)
    # Review snapshots are evidence, not maintained current diagrams.
    rendered = [domain, use_cases, robustness, *sequences, classes]
    if args.render:
        plantuml = shutil.which("plantuml")
        if plantuml is None:
            raise ValueError("--render requires PlantUML on PATH; omit it to run validators and tests")
        run("10-plantuml-syntax", [plantuml, "--check-syntax", *rendered])
        run("10-plantuml-svg", [plantuml, "-tsvg", "-failfast2", *rendered])
        run("10-plantuml-png", [plantuml, "-tpng", "-failfast2", *rendered],
            extra_env={"PLANTUML_LIMIT_SIZE": "16384"})
        for path in rendered:
            for suffix in (".svg", ".png"):
                if not path.with_suffix(suffix).is_file():
                    raise ValueError("Missing rendered " + suffix + ": " + str(path))
    passed = all(item["passed"] for item in results)
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "passed": passed,
              "status": "PASS" if passed else "FAIL",
              "source_skill_version": source_record["version"], "checks": results,
              "reference_unittest_methods": int(test_count.group(1)) if test_count else None,
              "oracle_defined_cases": len(json.loads((DEMO / "00-input/acceptance-oracle.json")
                                           .read_text(encoding="utf-8"))["cases"]),
              "diagrams": len(rendered), "review_baselines_match": True,
              "rendering_requested": args.render,
              "reviewed_headers_match": header_result.returncode == 0,
              "formal_gate_disposition": "NOT FULLY VERIFIED", "human_approval": False,
              "interpretation": "Mechanical results and scoped demo review do not create formal business approval."}
    (logs / "result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Result:", "PASS" if passed else "FAIL")
    print("Formal gate: NOT FULLY VERIFIED; no human approval is claimed.")
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, AssertionError, subprocess.TimeoutExpired) as error:
        destination = DEMO / "validation/latest"
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "result.json").write_text(json.dumps({
            "checked_at": datetime.now(timezone.utc).isoformat(), "passed": False,
            "status": "BLOCKED", "reason": str(error), "human_approval": False,
            "formal_gate_disposition": "NOT FULLY VERIFIED"
        }, indent=2) + "\n", encoding="utf-8")
        print("Verification blocked:", error, file=sys.stderr)
        raise SystemExit(2)
