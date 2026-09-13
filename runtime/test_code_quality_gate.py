import tempfile
import unittest
from pathlib import Path

import code_quality_gate as cqg


class CodeQualityGateTests(unittest.TestCase):
    def _scan(self, suffix: str, source: str):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f"sample{suffix}"
            path.write_text(source, encoding="utf-8")
            return cqg.scan_file(path)

    def test_clean_python_has_no_deterministic_findings(self):
        findings = self._scan(".py", "def add(a: int, b: int) -> int:\n    return a + b\n")
        self.assertEqual(findings, [])

    def test_broad_exception_is_detected(self):
        findings = self._scan(
            ".py",
            "def run():\n    try:\n        work()\n    except Exception:\n        recover()\n",
        )
        self.assertIn("CQG-DEF-001", {item.rule_id for item in findings})

    def test_swallowed_exception_is_high_severity(self):
        findings = self._scan(
            ".py",
            "def run():\n    try:\n        work()\n    except Exception:\n        pass\n",
        )
        swallowed = [item for item in findings if item.rule_id == "CQG-DEF-002"]
        self.assertEqual(len(swallowed), 1)
        self.assertEqual(swallowed[0].severity, "HIGH")
        self.assertEqual(cqg.verdict_for(findings), "REPAIR_REQUIRED")

    def test_typescript_as_any_is_detected(self):
        findings = self._scan(".ts", "const user = payload as any;\n")
        self.assertIn("CQG-TYPE-001", {item.rule_id for item in findings})

    def test_deep_nesting_is_detected(self):
        findings = self._scan(
            ".py",
            "def run(a, b, c, d):\n"
            "    if a:\n"
            "        if b:\n"
            "            if c:\n"
            "                if d:\n"
            "                    return 1\n"
            "    return 0\n",
        )
        self.assertIn("CQG-NEST-001", {item.rule_id for item in findings})

    def test_pass_does_not_imply_review_ready(self):
        report = cqg.build_report([])
        self.assertEqual(report["verdict"], "PASS")
        self.assertIn("A PASS is not REVIEW_READY.", report["limitations"])


if __name__ == "__main__":
    unittest.main()
