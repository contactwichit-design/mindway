import random,tempfile,unittest
from pathlib import Path
from loop_runtime import RunLedger,EventLog,save_checkpoint,resume_checkpoint
class RuntimeV2(unittest.TestCase):
 def ready(self):
  l=RunLedger("LMS production verification",topology="HYBRID"); [l.transition(s) for s in ("ORIENTING","PLANNED","RUNNING","VERIFYING")]; return l
 def test_completion_gate(self):
  l=self.ready(); l.add_failure("CONTENT_LOSS","LMS_VIDEO")
  with self.assertRaises(ValueError): l.transition("COMPLETE")
 def test_fake_closed_is_rejected(self):
  l=self.ready(); f=l.add_failure("FALSE_VERIFICATION","LMS_VIDEO"); f["state"]="CLOSED"; self.assertFalse(l.can_complete())
 def test_approval_gate(self):
  l=self.ready(); l.approval_gates=["publish"]
  with self.assertRaises(ValueError): l.transition("COMPLETE")
  l.validated_approvals=["publish"]; l.transition("COMPLETE")
 def test_real_redaction(self):
  e=EventLog("r"); x=e.emit("tool.called",payload={"patient":{"name":"SECRET"},"safe":"ok"},redacted_fields=["patient.name"]); self.assertEqual(x["payload"]["patient"]["name"],"[REDACTED]"); self.assertNotIn("SECRET",str(x))
 def test_parallel_causality_explicit(self):
  e=EventLog("r"); a=e.emit("work.started",branch_id="A"); b=e.emit("work.started",branch_id="B"); self.assertIsNone(b["parent_span_id"]); self.assertNotEqual(a["span_id"],b["span_id"])
 def test_checkpoint_semantic_guard(self):
  l=RunLedger("LMS"); l.semantic_snapshot={"my_sha":"abc","lms_ssot":"v1"}; e=EventLog(l.run_id)
  with tempfile.TemporaryDirectory() as d:
   cp=save_checkpoint(l,e,Path(d)); resume_checkpoint(Path(cp["uri"]),cp["checksum"],l.semantic_snapshot)
   with self.assertRaises(ValueError): resume_checkpoint(Path(cp["uri"]),cp["checksum"],{"my_sha":"def","lms_ssot":"v1"})
 def test_1000_lms_adversarial(self):
  classes=["CONTENT_LOSS","LAYOUT_DRIFT","AUDIO_DESYNC","SOURCE_DRIFT","FALSE_VERIFICATION","PREMATURE_COMPLETION","UNICODE_FAILURE"]
  for seed in range(1000):
   r=random.Random(seed); l=self.ready(); relevant=r.random()<.9; f=l.add_failure(r.choice(classes),"LMS_VIDEO",r.choice(["S1","S2","S3"]),relevant)
   if relevant:
    self.assertFalse(l.can_complete()); l.close_failure(f["id"],"verified-root",["original-pass","regression-pass"],["original","neighbor","export"],["M00","M01","M03"]); self.assertTrue(l.can_complete())
   else: self.assertTrue(l.can_complete())
if __name__=="__main__": unittest.main()
