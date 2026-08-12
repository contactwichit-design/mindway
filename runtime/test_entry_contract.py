import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class EntryContractTests(unittest.TestCase):
    def test_required_entry_files_exist(self):
        for path in (
            "my.md",
            "BOOTSTRAP.md",
            "README.md",
            "PUBLIC_STANDARD.md",
            "skills/entry-access-gate/SKILL.md",
            "skills/loop/SKILL.md",
            "skills/fy/SKILL.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_canonical_my_entry_invariants(self):
        text = read("my.md")
        self.assertIn("`/my` is the single entry command for Mindway.", text)
        self.assertIn("MW-BOOT/1", text)
        self.assertIn("README.md", text)
        self.assertIn("PUBLIC_STANDARD.md", text)
        self.assertIn("NO VERIFIED /my = NO SUBSTANTIAL EXECUTION", text)
        self.assertIn("/fy", text)
        self.assertIn("/loop plan", text)
        self.assertIn("/myN", text)
        self.assertIn("/loop N", text)

    def test_bootstrap_anti_bypass_invariants(self):
        text = read("BOOTSTRAP.md")
        for required in (
            "Protocol: `MW-BOOT/1`",
            "One failed access method",
            "Exhaust all safe applicable read-only routes",
            "Never use memory",
            "NO VERIFIED /my = NO SUBSTANTIAL EXECUTION",
            "MINDWAY_LOADED",
            "MINDWAY_BLOCKED",
            "contactwichit-design/mindway",
            "main",
            "my.md",
        ):
            self.assertIn(required, text)

    def test_readme_embeds_bootstrap_contract(self):
        text = read("README.md")
        self.assertIn("MW-BOOT/1", text)
        self.assertIn("https://raw.githubusercontent.com/contactwichit-design/mindway/main/my.md", text)
        self.assertIn("NO VERIFIED /my = NO SUBSTANTIAL EXECUTION", text)

    def test_entry_gate_targets_current_canonical_path(self):
        text = read("skills/entry-access-gate/SKILL.md")
        self.assertIn("Repository: `contactwichit-design/mindway`", text)
        self.assertIn("Branch: `main`", text)
        self.assertIn("Entry path: `my.md`", text)
        self.assertIn("raw fails but GitHub blob succeeds", text)
        self.assertIn("required `README.md` or `PUBLIC_STANDARD.md` cannot be read", text)

    def test_fy_is_only_a_loop_plan_compatibility_alias(self):
        my_text = read("my.md")
        loop_text = read("skills/loop/SKILL.md")
        fy_text = read("skills/fy/SKILL.md")
        for text in (my_text, loop_text, fy_text):
            self.assertIn("/fy", text)
            self.assertIn("/loop plan", text)
        self.assertIn("compatibility alias", fy_text.lower())
        self.assertNotIn("Base cycle mapping", fy_text)
        self.assertNotIn("recommended `/myN` cycle budget", fy_text)

    def test_bootstrap_and_gate_cover_cache_freshness(self):
        bootstrap = read("BOOTSTRAP.md")
        gate = read("skills/entry-access-gate/SKILL.md")
        self.assertIn("cache-prone", bootstrap.lower())
        self.assertIn("freshness", gate.lower())


if __name__ == "__main__":
    unittest.main()
