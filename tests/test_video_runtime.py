import json
from pathlib import Path
import tempfile
import unittest
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("video_runtime", ROOT / "runtime" / "video_runtime.py")
vr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vr)


class VideoRuntimeTests(unittest.TestCase):
    def test_source_overwrite_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td)
            src=d/"x.mp4"; src.write_bytes(b"fake")
            m={
                "schema_version":"0.1","project_id":"T",
                "source":{"path":"x.mp4"},
                "delivery":{"width":1920,"height":1080,"fps":30},
                "output":{"path":"x.mp4"}
            }
            with self.assertRaises(vr.VideoRuntimeError) as cm:
                vr.validate_manifest(m,d)
            self.assertEqual(cm.exception.kind,"input")

    def test_ass_time(self):
        self.assertEqual(vr.ass_time(65.25),"0:01:05.25")

    def test_self_test_when_ffmpeg_available(self):
        if not vr.doctor().get("usable"):
            self.skipTest("ffmpeg/ffprobe unavailable")
        with tempfile.TemporaryDirectory() as td:
            result=vr.self_test(Path(td))
            self.assertEqual(result["status"],"PASS")
            self.assertTrue(Path(result["output"]).exists())
            self.assertEqual(len(result["inspection"]["frames"]),3)

    def test_stale_plan_refused(self):
        if not vr.doctor().get("usable"):
            self.skipTest("ffmpeg/ffprobe unavailable")
        with tempfile.TemporaryDirectory() as td:
            d=Path(td)
            src=vr.make_fixture(d)
            manifest=d/"video.project.json"
            manifest.write_text(json.dumps({
                "schema_version":"0.1",
                "project_id":"STALE",
                "source":{"path":src.name},
                "delivery":{"width":1280,"height":720,"fps":30,"fit":"pad"},
                "output":{"path":"out.mp4","overwrite":True}
            }),encoding="utf-8")
            plan=vr.build_plan(manifest)
            plan_path=d/"video.plan.json"
            plan_path.write_text(json.dumps(plan),encoding="utf-8")
            src.write_bytes(src.read_bytes()+b"changed")
            with self.assertRaises(vr.VideoRuntimeError) as cm:
                vr.render(plan_path)
            self.assertEqual(cm.exception.kind,"stale_plan")


if __name__=="__main__":
    unittest.main()
