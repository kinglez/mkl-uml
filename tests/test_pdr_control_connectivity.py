# Copyright 2026 kingle.zhuang. Organization: mkl. See NOTICE.
"""PDR connectivity distinguishes topology warnings from located behavior claims."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PDR = ROOT / "skills/mkl-pdr-review/scripts/validate_pdr.py"
MODEL = '''@startuml
actor "Caller" as ACT_Caller
boundary "Input channel" as B_Input
control "Process request" as C_Main
control "核对约束" as C_Required
entity "Record" as E_Record
ACT_Caller -- B_Input
B_Input -- C_Main
C_Main -- E_Record
'''


class PDRControlConnectivity(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="pdr behavior ")
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        self.target = self.work / "diagram.puml"
        self.source = self.work / "behavior.md"
        self.source.write_text("# Behavior\n3. 系统核对约束后处理输入。\n", encoding="utf-8")
        self.record = self.work / "behavior-map.json"

    def mapping(self, **changes):
        entry = {"diagram": "diagram.puml", "entry": "B_Input", "control": "C_Required",
                 "source": "behavior.md", "line": 2, "quote": "3. 系统核对约束后处理输入。", "step": "3"}
        entry.update(changes)
        return {"schema_version": 1, "required_controls": [entry]}

    def run_pdr(self, extra="", mapping=None, model=MODEL):
        self.target.write_text(model + extra + "@enduml\n", encoding="utf-8")
        command = [sys.executable, "-I", "-B", str(PDR), "--robustez", str(self.target)]
        if mapping is not None:
            self.record.write_text(json.dumps(mapping, ensure_ascii=False), encoding="utf-8")
            command += ["--behavior-map", str(self.record)]
        result = subprocess.run(command, cwd=self.work, capture_output=True, text=True,
                                encoding="utf-8", timeout=20)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def assert_exit(self, result, expected):
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_isolated_control_is_a_located_warning_without_a_map(self):
        result = self.run_pdr()
        self.assert_exit(result, 0)
        self.assertIn("ERRORS: none", result.stdout)
        self.assertRegex(result.stdout, r"L5: isolated control 'C_Required'")
        self.assertIn("核对约束", result.stdout)
        self.assertIn("NOT FULLY VERIFIED", result.stdout)

    def test_connected_control_has_no_isolation_warning(self):
        result = self.run_pdr("C_Main -- C_Required\n")
        self.assert_exit(result, 0)
        self.assertNotIn("isolated control", result.stdout)

    def test_located_requirement_makes_disconnected_control_an_error(self):
        result = self.run_pdr(mapping=self.mapping())
        self.assert_exit(result, 1)
        self.assertIn("not reachable through boundary/control coordination", result.stdout)
        self.assertIn("behavior.md:2 (step 3)", result.stdout)
        self.assertIn("C_Required", result.stdout)

    def test_declared_control_accepts_direct_or_coordinated_entry(self):
        for link in ("B_Input -- C_Required\n", "C_Main -- C_Required\n"):
            with self.subTest(link=link):
                result = self.run_pdr(link, self.mapping())
                self.assert_exit(result, 0)
                self.assertIn("structural connectivity checked", result.stdout)
                self.assertNotIn("isolated control", result.stdout)

    def test_shared_entity_does_not_connect_required_behavior(self):
        result = self.run_pdr("C_Required -- E_Record\n", self.mapping())
        self.assert_exit(result, 1)
        self.assertNotIn("isolated control", result.stdout)
        self.assertIn("not reachable", result.stdout)

    def test_another_boundary_and_shared_actor_do_not_bridge_entry(self):
        extra = ('boundary "Other channel" as B_Other\nACT_Caller -- B_Other\n'
                 'B_Other -- C_Required\n')
        result = self.run_pdr(extra, self.mapping())
        self.assert_exit(result, 1)
        self.assertIn("not reachable", result.stdout)

    def test_layout_and_note_edges_do_not_hide_isolation(self):
        for extra in ("C_Main -[hidden]- C_Required\n",
                      'note "Description" as Note\nC_Required .. Note\n'):
            with self.subTest(extra=extra):
                result = self.run_pdr(extra, self.mapping())
                self.assert_exit(result, 1)
                self.assertIn("isolated control", result.stdout)
                self.assertIn("not reachable", result.stdout)

    def test_unknown_syntax_or_endpoints_keep_connectivity_partial(self):
        for extra in ("C_Main -- E_Unknown\n", "!include external.puml\n",
                      "C_Main *-- C_Required\n"):
            with self.subTest(extra=extra):
                result = self.run_pdr(extra, self.mapping())
                self.assert_exit(result, 0)
                self.assertIn("connectivity unverified because BCE coverage is partial", result.stdout)
                self.assertNotIn("isolated control", result.stdout)
                self.assertNotIn("not reachable", result.stdout)

    def test_missing_required_alias_is_a_diagram_finding_when_complete(self):
        result = self.run_pdr(mapping=self.mapping(control="C_Missing"))
        self.assert_exit(result, 1)
        self.assertIn("mapped alias 'C_Missing' is absent", result.stdout)

    def test_stale_source_wrong_types_and_unknown_fields_are_input_errors(self):
        for mapping in (self.mapping(quote="Different source text"), self.mapping(line=999),
                        self.mapping(line=True), self.mapping(entry="E_Record"),
                        self.mapping(control="E_Record"), self.mapping(unknown=True)):
            with self.subTest(mapping=mapping):
                result = self.run_pdr("C_Main -- C_Required\n", mapping)
                self.assert_exit(result, 2)
                self.assertIn("invalid behavior map", result.stderr)

    def test_record_requires_actual_target_and_contained_local_sources(self):
        (self.work / "other.puml").write_text(MODEL + "@enduml\n", encoding="utf-8")
        for mapping in (self.mapping(diagram="other.puml"), self.mapping(source="../outside.md"),
                        self.mapping(source=str(self.source)), self.mapping(source="missing.md")):
            with self.subTest(mapping=mapping):
                self.assert_exit(self.run_pdr(mapping=mapping), 2)
        self.assert_exit(self.run_pdr(mapping=self.mapping(source="bad\x00name.md")), 2)

    def test_symbolic_source_escape_and_duplicate_json_keys_are_input_errors(self):
        with self.subTest(case="symbolic source escape"):
            with tempfile.TemporaryDirectory() as outside:
                external = Path(outside) / "source.md"
                external.write_text(self.source.read_text(encoding="utf-8"), encoding="utf-8")
                try:
                    (self.work / "escape.md").symlink_to(external)
                except (OSError, NotImplementedError) as exc:
                    self.skipTest(f"symbolic links unavailable: {exc}")
                self.assert_exit(self.run_pdr(mapping=self.mapping(source="escape.md")), 2)
        self.target.write_text(MODEL + "@enduml\n", encoding="utf-8")
        self.record.write_text('{"schema_version": 1, "schema_version": 1, "required_controls": []}', encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", "-B", str(PDR), "--robustez", str(self.target),
                                 "--behavior-map", str(self.record)], cwd=self.work,
                                capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assert_exit(result, 2)
        self.assertIn("duplicate JSON key", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_or_empty_mappings_are_rejected(self):
        mapping = self.mapping()
        mapping["required_controls"] *= 2
        self.assert_exit(self.run_pdr(mapping=mapping), 2)
        self.assert_exit(self.run_pdr(mapping={"schema_version": 1, "required_controls": []}), 2)


if __name__ == "__main__":
    unittest.main()
