import tempfile
import unittest
from pathlib import Path

from loop_runtime import RunLedger, EventLog, save_checkpoint, load_checkpoint

class LoopRuntimeTests(unittest.TestCase):
    def test_happy_path(self):
        r = RunLedger("test", requested_cycles=3, topology="SEQUENTIAL")
        e = EventLog(r.run_id)
        e.emit("run.created")
        for state in ["ORIENTING","PLANNED","RUNNING","VERIFYING","COMPLETE"]:
            r.transition(state)
        self.assertEqual(r.state, "COMPLETE")
        self.assertEqual(e.events[0]["sequence"], 0)

    def test_invalid_transition_fails(self):
        r = RunLedger("test")
        with self.assertRaises(ValueError):
            r.transition("COMPLETE")

    def test_terminal_cannot_restart(self):
        r = RunLedger("test")
        for state in ["ORIENTING","PLANNED","RUNNING","VERIFYING","COMPLETE"]:
            r.transition(state)
        with self.assertRaises(ValueError):
            r.transition("RUNNING")

    def test_fix_loop(self):
        r = RunLedger("test")
        for state in ["ORIENTING","PLANNED","RUNNING","VERIFYING","FIXING","VERIFYING","COMPLETE"]:
            r.transition(state)
        self.assertEqual(r.state, "COMPLETE")

    def test_checkpoint_roundtrip(self):
        r = RunLedger("test")
        e = EventLog(r.run_id)
        e.emit("run.created")
        with tempfile.TemporaryDirectory() as td:
            cp = save_checkpoint(r, e, Path(td))
            loaded = load_checkpoint(Path(cp["uri"]))
            self.assertEqual(loaded["checksum"], cp["checksum"])
            self.assertEqual(loaded["data"]["ledger"]["run_id"], r.run_id)

    def test_blocked_branch_does_not_force_whole_run_block(self):
        r = RunLedger("test")
        r.add_blocked_branch("external publish", "approval unavailable", "continue local verification")
        self.assertEqual(r.state, "NEW")
        self.assertEqual(len(r.blocked_branches), 1)

if __name__ == "__main__":
    unittest.main()
