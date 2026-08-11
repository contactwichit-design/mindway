import random
import unittest
from recursive_improvement import FailureGraph, FailureNode

class RecursiveImprovementTests(unittest.TestCase):
    def test_false_completion_blocked(self):
        g=FailureGraph(); g.add(FailureNode("FALSE_VERIFICATION","LMS_VIDEO"))
        self.assertFalse(g.can_complete())

    def test_record_does_not_resolve(self):
        g=FailureGraph(); f=FailureNode("CONTENT_LOSS","DOCUMENT",evidence=["lesson recorded"]); g.add(f)
        self.assertFalse(g.can_complete())
        with self.assertRaises(ValueError): f.transition("CLOSED")

    def test_verified_closure(self):
        g=FailureGraph(); f=FailureNode("UNDERFILL","DOCUMENT"); g.add(f)
        f.root_cause="QC checked overflow only"; f.test_radius=["original","analog"]
        f.evidence=["original-pass","analog-pass"]; f.state="VERIFIED"; f.transition("CLOSED")
        self.assertTrue(g.can_complete())

    def test_unrelated_failure_does_not_block(self):
        g=FailureGraph(); g.add(FailureNode("COSMETIC","OTHER",severity="S4",mission_relevant=False))
        self.assertTrue(g.can_complete())

    def test_child_failure_blocks_parent_completion(self):
        g=FailureGraph(); p=FailureNode("LAYOUT_DRIFT","LMS_VIDEO"); pid=g.add(p)
        p.root_cause="renderer"; p.test_radius=["original"]; p.evidence=["pass"]; p.state="VERIFIED"; p.transition("CLOSED")
        g.add(FailureNode("AUDIO_DESYNC","LMS_VIDEO"),parent_id=pid)
        self.assertFalse(g.can_complete())

    def test_1000_lms_weighted_scenarios(self):
        classes=["CONTENT_LOSS","LAYOUT_DRIFT","OVERFLOW","AUDIO_DESYNC","FALSE_VERIFICATION","CONTEXT_LOSS","PREMATURE_COMPLETION"]
        for i in range(1000):
            rng=random.Random(i); g=FailureGraph()
            f=FailureNode(rng.choice(classes),"LMS_VIDEO",severity=rng.choice(["S1","S2","S3"])); g.add(f)
            self.assertFalse(g.can_complete())
            # instance repair alone must remain open
            f.evidence=["instance repaired"]
            self.assertFalse(g.can_complete())
            # reusable closure requires diagnosis + test radius + verification evidence
            f.root_cause="fixture-root"; f.test_radius=["original","neighboring-scene","export"]
            f.analogs_checked=["M00","M01","M03"]; f.evidence.append("regression-pass"); f.state="VERIFIED"; f.transition("CLOSED")
            self.assertTrue(g.can_complete())

if __name__=="__main__": unittest.main()
