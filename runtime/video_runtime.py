#!/usr/bin/env python3
"""Mindway experimental video runtime v0.1.

Deterministic, local-first reference runtime for T15 Media Production.
Commands:
  doctor
  probe INPUT
  plan MANIFEST [--out PLAN]
  render PLAN
  verify OUTPUT --plan PLAN
  look OUTPUT [--out-dir DIR]
  self-test [--workdir DIR]

Standard-library only. Requires ffmpeg + ffprobe for media operations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

VERSION = "0.1.0-experimental"


class VideoRuntimeError(RuntimeError):
    def __init__(self, kind: str, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.kind = kind
        self.details = details or {}


def emit(payload: dict[str, Any], code: int = 0) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code


def run(cmd: list[str], *, timeout: int = 120, check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise VideoRuntimeError("timeout", f"Command timed out after {timeout}s", {"cmd": cmd}) from e
    if check and p.returncode != 0:
        raise VideoRuntimeError(
            "command_failed",
            (p.stderr or p.stdout or "command failed").strip(),
            {"cmd": cmd, "returncode": p.returncode},
        )
    return p


def which(name: str) -> str | None:
    return shutil.which(name)


def parse_ratio(value: str | None) -> float | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    if "/" in value:
        a, b = value.split("/", 1)
        try:
            den = float(b)
            return float(a) / den if den else None
        except ValueError:
            return None
    try:
        return float(value)
    except ValueError:
        return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise VideoRuntimeError("input", f"Input does not exist: {path}")
    if not which("ffprobe"):
        raise VideoRuntimeError("missing_tool", "ffprobe is not available")
    p = run([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)
    ])
    raw = json.loads(p.stdout)
    streams = raw.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fmt = raw.get("format", {})
    duration = None
    for candidate in [fmt.get("duration"), video and video.get("duration"), audio and audio.get("duration")]:
        if candidate not in (None, "N/A"):
            try:
                duration = float(candidate)
                break
            except (TypeError, ValueError):
                pass

    vobj = None
    if video:
        avg = parse_ratio(video.get("avg_frame_rate"))
        rfr = parse_ratio(video.get("r_frame_rate"))
        transfer = video.get("color_transfer")
        primaries = video.get("color_primaries")
        hdr = transfer in {"smpte2084", "arib-std-b67"}
        rotation = 0
        tags = video.get("tags") or {}
        if "rotate" in tags:
            try:
                rotation = int(float(tags["rotate"]))
            except (ValueError, TypeError):
                rotation = 0
        for side in video.get("side_data_list") or []:
            if "rotation" in side:
                try:
                    rotation = int(float(side["rotation"]))
                except (ValueError, TypeError):
                    pass
        vfr = bool(avg and rfr and abs(avg - rfr) > 0.01)
        vobj = {
            "codec": video.get("codec_name"),
            "width": video.get("width"),
            "height": video.get("height"),
            "fps": avg or rfr,
            "avg_frame_rate": video.get("avg_frame_rate"),
            "r_frame_rate": video.get("r_frame_rate"),
            "pixel_format": video.get("pix_fmt"),
            "color_space": video.get("color_space"),
            "color_transfer": transfer,
            "color_primaries": primaries,
            "hdr": hdr,
            "bt2020_or_hdr": hdr or primaries == "bt2020",
            "rotation": rotation,
            "variable_frame_rate_suspected": vfr,
        }

    aobj = None
    if audio:
        aobj = {
            "codec": audio.get("codec_name"),
            "channels": audio.get("channels"),
            "channel_layout": audio.get("channel_layout"),
            "sample_rate": int(audio["sample_rate"]) if str(audio.get("sample_rate", "")).isdigit() else audio.get("sample_rate"),
        }

    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "duration_s": duration,
        "video": vobj,
        "audio": aobj,
    }


def doctor() -> dict[str, Any]:
    result: dict[str, Any] = {
        "runtime_version": VERSION,
        "ffmpeg": {"path": which("ffmpeg"), "available": bool(which("ffmpeg"))},
        "ffprobe": {"path": which("ffprobe"), "available": bool(which("ffprobe"))},
        "capabilities": {},
        "fonts": {},
    }
    if result["ffmpeg"]["available"]:
        filters_proc = run(["ffmpeg", "-hide_banner", "-filters"], check=False)
        vf = filters_proc.stdout + filters_proc.stderr
        enc_proc = run(["ffmpeg", "-hide_banner", "-encoders"], check=False)
        enc = enc_proc.stdout + enc_proc.stderr
        result["capabilities"] = {
            "ass": " ass " in vf or " ass" in vf,
            "subtitles": " subtitles " in vf or " subtitles" in vf,
            "drawtext": " drawtext " in vf or " drawtext" in vf,
            "h264": "libx264" in enc or " h264_" in enc,
            "aac": " aac " in enc or " aac" in enc,
        }
    if which("fc-match"):
        p = run(["fc-match", "-f", "%{family}|%{file}\n", ":lang=th"], check=False)
        line = (p.stdout or "").splitlines()[0] if (p.stdout or "").splitlines() else ""
        fam, _, fpath = line.partition("|")
        result["fonts"] = {"thai_available": bool(line), "family": fam or None, "file": fpath or None}
    else:
        result["fonts"] = {"thai_available": None, "reason": "fc-match unavailable"}
    result["usable"] = bool(result["ffmpeg"]["available"] and result["ffprobe"]["available"])
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise VideoRuntimeError("input", f"JSON file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise VideoRuntimeError("input", f"Invalid JSON in {path}: {e}") from e


def validate_manifest(m: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    if str(m.get("schema_version")) != "0.1":
        errors.append("schema_version must be '0.1'")
    if not m.get("project_id"):
        errors.append("project_id is required")
    src = m.get("source") or {}
    if not src.get("path"):
        errors.append("source.path is required")
    delivery = m.get("delivery") or {}
    for k in ["width", "height", "fps"]:
        if not delivery.get(k):
            errors.append(f"delivery.{k} is required")
    output = m.get("output") or {}
    if not output.get("path"):
        errors.append("output.path is required")
    if errors:
        raise VideoRuntimeError("input", "Manifest validation failed", {"errors": errors})

    source_path = (base_dir / src["path"]).resolve() if not Path(src["path"]).is_absolute() else Path(src["path"]).resolve()
    output_path = (base_dir / output["path"]).resolve() if not Path(output["path"]).is_absolute() else Path(output["path"]).resolve()
    if source_path == output_path:
        raise VideoRuntimeError("input", "Output path must not overwrite the source")
    if not source_path.exists():
        raise VideoRuntimeError("input", f"Source not found: {source_path}")
    if output_path.exists() and not output.get("overwrite", False):
        raise VideoRuntimeError("input", f"Output exists and overwrite=false: {output_path}")

    normalized = json.loads(json.dumps(m))
    normalized["source"]["path"] = str(source_path)
    normalized["output"]["path"] = str(output_path)
    return normalized


def build_plan(manifest_path: Path) -> dict[str, Any]:
    m = validate_manifest(load_json(manifest_path), manifest_path.parent)
    src = Path(m["source"]["path"])
    pr = probe(src)
    delivery = m["delivery"]
    captions = m.get("captions") or []
    operations = [
        {"op": "probe", "input": str(src)},
        {
            "op": "fit",
            "mode": delivery.get("fit", "pad"),
            "width": int(delivery["width"]),
            "height": int(delivery["height"]),
            "fps": float(delivery["fps"]),
        },
    ]
    if captions:
        operations.append({"op": "captions", "mode": "ass", "count": len(captions)})
    operations += [
        {"op": "encode", "video_codec": delivery.get("video_codec", "h264"), "audio_codec": delivery.get("audio_codec", "aac")},
        {"op": "verify"},
        {"op": "look", "frames": 3},
    ]
    return {
        "plan_version": "0.1",
        "runtime_version": VERSION,
        "manifest_path": str(manifest_path.resolve()),
        "project_id": m["project_id"],
        "story_spine": m.get("story_spine", []),
        "source": {
            "path": str(src),
            "sha256": sha256_file(src),
            "probe": pr,
        },
        "delivery": delivery,
        "captions": captions,
        "output": m["output"],
        "operations": operations,
        "quality_gates": {
            "technical_qc": "required",
            "visual_qc": "required_if_picture_changed",
            "story_media_qc": "calling_agent_or_human_required",
            "thai_unicode_qc": "required_when_non_latin_text_present",
        },
    }


def ass_time(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def write_ass(captions: list[dict[str, Any]], path: Path, width: int, height: int, font: str) -> None:
    font_size = max(24, int(height * 0.045))
    margin_v = max(28, int(height * 0.06))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,{font},{font_size},&H00FFFFFF,&H000000FF,&H00101010,&H80000000,0,0,0,0,100,100,0,0,1,3,1,2,80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    rows=[]
    for c in captions:
        start=float(c["start"]); end=float(c["end"])
        if end <= start:
            raise VideoRuntimeError("input", f"Caption end must be after start: {c}")
        rows.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{ass_escape(str(c['text']))}")
    path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")


def escape_filter_path(path: Path) -> str:
    s = str(path.resolve()).replace("\\", "/")
    return s.replace(":", r"\:").replace("'", r"\'")


def render(plan_path: Path) -> dict[str, Any]:
    if not which("ffmpeg"):
        raise VideoRuntimeError("missing_tool", "ffmpeg is not available")
    plan = load_json(plan_path)
    src = Path(plan["source"]["path"])
    if not src.exists():
        raise VideoRuntimeError("input", f"Source not found: {src}")
    current_hash = sha256_file(src)
    if current_hash != plan["source"].get("sha256"):
        raise VideoRuntimeError("stale_plan", "Source changed after plan creation", {"planned": plan["source"].get("sha256"), "current": current_hash})
    out = Path(plan["output"]["path"])
    if out == src:
        raise VideoRuntimeError("input", "Refusing to overwrite source")
    if out.exists() and not plan["output"].get("overwrite", False):
        raise VideoRuntimeError("input", f"Output exists and overwrite=false: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d=plan["delivery"]
    w,h,fps=int(d["width"]),int(d["height"]),float(d["fps"])
    fit=d.get("fit","pad")
    if fit == "pad":
        vf=f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps:g}"
    elif fit == "crop":
        vf=f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps:g}"
    else:
        raise VideoRuntimeError("input", f"Unsupported fit mode in v0.1: {fit}")

    tmp_ass=None
    captions=plan.get("captions") or []
    if captions:
        font=d.get("caption_font","Noto Sans Thai")
        fd, tempname=tempfile.mkstemp(prefix="mindway-video-", suffix=".ass")
        os.close(fd)
        tmp_ass=Path(tempname)
        write_ass(captions,tmp_ass,w,h,font)
        vf += f",ass='{escape_filter_path(tmp_ass)}'"

    cmd=["ffmpeg","-hide_banner","-y" if plan["output"].get("overwrite",False) else "-n","-i",str(src),"-vf",vf,"-c:v","libx264","-crf",str(d.get("crf",18)),"-pix_fmt","yuv420p","-movflags","+faststart"]
    if plan["source"]["probe"].get("audio"):
        cmd += ["-c:a","aac","-b:a",str(d.get("audio_bitrate","192k"))]
    else:
        cmd += ["-an"]
    cmd += [str(out)]
    try:
        p=run(cmd,timeout=int(d.get("timeout_sec",300)))
    finally:
        if tmp_ass and tmp_ass.exists():
            tmp_ass.unlink()
    pr=probe(out)
    return {"status":"rendered","output":str(out),"probe":pr,"commands":[cmd],"stderr_tail":"\n".join((p.stderr or "").splitlines()[-8:])}


def verify(output: Path, plan_path: Path) -> dict[str, Any]:
    plan=load_json(plan_path)
    pr=probe(output)
    expected=plan["delivery"]
    src_pr=plan["source"]["probe"]
    checks=[]
    def ck(name: str, passed: bool, observed: Any, wanted: Any, severity: str="P0"):
        checks.append({"check":name,"pass":bool(passed),"observed":observed,"expected":wanted,"severity":severity})
    v=pr.get("video") or {}
    ck("width",v.get("width")==int(expected["width"]),v.get("width"),int(expected["width"]))
    ck("height",v.get("height")==int(expected["height"]),v.get("height"),int(expected["height"]))
    efps=float(expected["fps"]); ofps=float(v.get("fps") or 0)
    ck("fps",abs(ofps-efps)<=0.05,ofps,efps)
    source_duration=src_pr.get("duration_s")
    out_duration=pr.get("duration_s")
    if source_duration is not None and out_duration is not None:
        ck("duration",abs(out_duration-source_duration)<=0.20,out_duration,source_duration)
    ck("nonempty",output.exists() and output.stat().st_size>1024, output.stat().st_size if output.exists() else 0, ">1024 bytes")
    if src_pr.get("audio"):
        ck("audio_present",pr.get("audio") is not None,bool(pr.get("audio")),True)
    p0=[c for c in checks if c["severity"]=="P0" and not c["pass"]]
    return {
        "status":"PASS" if not p0 else "FAIL",
        "technical_qc":checks,
        "probe":pr,
        "visual_qc":"REQUIRED",
        "story_media_qc":"REQUIRES_CALLING_AGENT_OR_HUMAN",
        "thai_unicode_qc":"REQUIRES_VISUAL_INSPECTION" if any(any(ord(ch)>127 for ch in str(c.get("text",""))) for c in plan.get("captions") or []) else "NOT_APPLICABLE",
    }


def look(output: Path, out_dir: Path) -> dict[str, Any]:
    pr=probe(output)
    dur=float(pr.get("duration_s") or 0)
    if dur <= 0:
        raise VideoRuntimeError("output", "Cannot inspect frames: output duration is not positive")
    out_dir.mkdir(parents=True,exist_ok=True)
    times=[min(0.15,dur*0.1),dur*0.5,max(0.0,dur-0.15)]
    paths=[]
    for idx,t in enumerate(times,1):
        pth=out_dir/f"frame_{idx}_{t:.2f}s.png"
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.3f}","-i",str(output),"-frames:v","1",str(pth)],timeout=60)
        if not pth.exists() or pth.stat().st_size==0:
            raise VideoRuntimeError("output",f"Failed to create inspection frame: {pth}")
        paths.append(str(pth))
    return {"status":"frames_created","times_s":times,"frames":paths}


def make_fixture(workdir: Path) -> Path:
    workdir.mkdir(parents=True,exist_ok=True)
    src=workdir/"fixture_source.mp4"
    run([
        "ffmpeg","-hide_banner","-loglevel","error","-y",
        "-f","lavfi","-i","testsrc2=size=1280x720:rate=30:duration=4",
        "-f","lavfi","-i","sine=frequency=440:sample_rate=48000:duration=4",
        "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(src)
    ],timeout=120)
    return src


def self_test(workdir: Path) -> dict[str, Any]:
    doc=doctor()
    if not doc.get("usable"):
        raise VideoRuntimeError("missing_tool","Runtime is not usable",doc)
    src=make_fixture(workdir)
    manifest=workdir/"video.project.json"
    out=workdir/"fixture_output.mp4"
    plan_path=workdir/"video.plan.json"
    manifest_data={
        "schema_version":"0.1",
        "project_id":"MW-VIDEO-SELFTEST-001",
        "story_spine":["source fixture","Thai caption appears","technical output preserved"],
        "source":{"path":src.name},
        "captions":[{"start":0.5,"end":3.5,"text":"ทดสอบ Video Runtime • Probe → Plan → Render → QC"}],
        "delivery":{"width":1920,"height":1080,"fps":30,"fit":"pad","caption_font":"Noto Sans Thai","crf":18},
        "output":{"path":out.name,"overwrite":True}
    }
    manifest.write_text(json.dumps(manifest_data,ensure_ascii=False,indent=2),encoding="utf-8")
    plan=build_plan(manifest)
    plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")
    rendered=render(plan_path)
    verified=verify(out,plan_path)
    frames=look(out,workdir/"inspection")
    return {
        "status":"PASS" if verified["status"]=="PASS" else "FAIL",
        "doctor":doc,
        "source_probe":plan["source"]["probe"],
        "plan_path":str(plan_path),
        "output":rendered["output"],
        "verification":verified,
        "inspection":frames,
        "next_gate":"Visual/story inspection by calling agent before REVIEW_READY"
    }


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description="Mindway experimental video runtime")
    sub=parser.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor")
    p=sub.add_parser("probe"); p.add_argument("input")
    p=sub.add_parser("plan"); p.add_argument("manifest"); p.add_argument("--out")
    p=sub.add_parser("render"); p.add_argument("plan")
    p=sub.add_parser("verify"); p.add_argument("output"); p.add_argument("--plan",required=True)
    p=sub.add_parser("look"); p.add_argument("output"); p.add_argument("--out-dir",default="inspection")
    p=sub.add_parser("self-test"); p.add_argument("--workdir")
    args=parser.parse_args(argv)
    try:
        if args.cmd=="doctor": return emit(doctor())
        if args.cmd=="probe": return emit(probe(Path(args.input).resolve()))
        if args.cmd=="plan":
            mp=Path(args.manifest).resolve(); plan=build_plan(mp)
            if args.out:
                op=Path(args.out).resolve(); op.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8"); plan["written_plan"]=str(op)
            return emit(plan)
        if args.cmd=="render": return emit(render(Path(args.plan).resolve()))
        if args.cmd=="verify": return emit(verify(Path(args.output).resolve(),Path(args.plan).resolve()))
        if args.cmd=="look": return emit(look(Path(args.output).resolve(),Path(args.out_dir).resolve()))
        if args.cmd=="self-test":
            wd=Path(args.workdir).resolve() if args.workdir else Path(tempfile.mkdtemp(prefix="mindway-video-selftest-"))
            return emit(self_test(wd))
    except VideoRuntimeError as e:
        return emit({"status":"ERROR","kind":e.kind,"message":str(e),"details":e.details},2)


if __name__=="__main__":
    raise SystemExit(main())
