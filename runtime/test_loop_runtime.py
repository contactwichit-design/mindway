import random
import tempfile
import unittest
from pathlib import Path

from loop_runtime import EventLog, RunLedger, load_checkpoint, resume_checkpoint, save_checkpoint


class LoopRuntimeTests(unittest.TestCase):
    def test_happy_path(self):
        r = RunLedger("test", requested_cycles=3, topology="SEQUENTIAL")
        e = EventLog(r.run_id)
        e.emit("run.created")
        for state in ["ORIENTING", "PLANNED", "RUNNING", "VERIFYING", "COMPLETE"]:
            r.transition(state)
        self.assertEqual(r.state, "COMPLETE")
        self.assertEqual(e.events[0]["sequence"], 0)

    def test_invalid_transition_fails(self):
        r = RunLedger("test")
        with self.assertRaises(ValueError):
            r.transition("COMPLETE")

    def test_terminal_cannot_restart(self):
        r = RunLedger("test")
        for state in ["ORIENTING", "PLANNED", "RUNNING", "VERIFYING", "COMPLETE"]:
            r.transition(state)
        with self.assertRaises(ValueError):
            r.transition("RUNNING")

    def test_fix_loop(self):
        r = RunLedger("test")
        for state in ["ORIENTING", "PLANNED", "RUNNING", "VERIFYING", "FIXING", "VERIFYING", "COMPLETE"]:
            r.transition(state)
        self.assertEqual(r.state, "COMPLETE")

    def test_checkpoint_roundtrip_and_integrity(self):
        r = RunLedger("test")
        e = EventLog(r.run_id)
        e.emit("run.created")
        with tempfile.TemporaryDirectory() as td:
            cp = save_checkpoint(r, e, Path(td))
            loaded = load_checkpoint(Path(cp["uri"]), cp["checksum"])
            self.assertEqual(loaded["data"]["ledger"]["run_id"], r.run_id)
            rr, ee = resume_checkpoint(Path(cp["uri"]), cp["checksum"])
            self.assertEqual(rr.run_id, r.run_id)
            self.assertEqual(len(ee.events), 1)
            p = Path(cp["uri"])
            p.write_bytes(p.read_bytes() + b"tamper")
            with self.assertRaises(ValueError):
                load_checkpoint(p, cp["checksum"])

    def test_blocked_branch_does_not_force_whole_run_block(self):
        r = RunLedger("test")
        r.add_blocked_branch("external publish", "approval unavailable", "continue local verification")
        self.assertEqual(r.state, "NEW")
        self.assertEqual(len(r.blocked_branches), 1)

    def test_schema_aligned_input_validation(self):
        for bad in [0, 100, -1, True]:
            with self.assertRaises(ValueError):
                RunLedger("test", requested_cycles=bad)
        with self.assertRaises(ValueError):
            RunLedger("test", topology="RANDOM")
        e = EventLog("run_test")
        with self.assertRaises(ValueError):
            e.emit("not.a.real.event")
        with self.assertRaises(ValueError):
            e.emit("work.started", cycle=-1)

    def test_stress_1000_deterministic_runs(self):
        for i in range(1000):
            rng = random.Random(i)
            r = RunLedger(
                f"stress-{i}",
                requested_cycles=rng.randint(1, 99),
                topology=rng.choice(["SEQUENTIAL", "PARALLEL", "HYBRID"]),
            )
            e = EventLog(r.run_id)
            e.emit("run.created", status=r.state)
            r.transition("ORIENTING"); e.emit("orient.started", status=r.state)
            r.transition("PLANNED"); e.emit("plan.created", status=r.state)
            r.transition("RUNNING"); e.emit("work.started", cycle=1, status=r.state)
            if rng.random() < 0.35:
                r.transition("CHECKPOINTED"); e.emit("checkpoint.saved", status=r.state)
                r.transition("RUNNING"); e.emit("run.resumed", status=r.state)
            r.transition("VERIFYING"); e.emit("verify.started", status=r.state)
            for _ in range(rng.randint(0, 3)):
                r.transition("FIXING"); e.emit("fix.started", status=r.state)
                r.transition("VERIFYING"); e.emit("fix.completed", status=r.state)
            r.transition("COMPLETE")
            e.emit("verify.pass", status=r.state)
            e.emit("run.completed", status=r.state)
            self.assertEqual(r.state, "COMPLETE")
            self.assertTrue(all(ev["sequence"] == n for n, ev in enumerate(e.events)))


if __name__ == "__main__":
    unittest.main()
