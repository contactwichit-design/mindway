---
name: media-production
version: 0.1.0
status: EXPERIMENTAL
description: Experimental Mindway T15 runtime extension for deterministic video probe, project planning, local render, technical verification, Thai-capable caption rendering, and visual inspection. It does not replace T15 or canonical Graphic/Visual delivery gates.
---

# Mindway Media Production Runtime — Experimental v0.1

## Mission

Extend existing Template System `T15 — Media Production` with an executable, local-first and verifiable video path without changing canonical `/my` or declaring the capability ACTIVE before real tests pass.

Core route:

`SOURCE → PROBE → PROJECT MANIFEST → PLAN → RENDER → TECHNICAL QC → VISUAL INSPECTION → STORY-MEDIA QC → REVIEW_READY`

`TECH_VALID != REVIEW_READY`.

## Authority and boundaries

- Existing T15 remains the workflow owner.
- Canonical `/my`, Public Standard, project-specific owner locks and approval gates remain stronger than this skill.
- The runtime is execution infrastructure. It does not choose the story, decide which cut is good, invent facts, or approve final visual taste.
- Never overwrite the source.
- A plan fingerprints its source and rendering must refuse stale plans when the input changed.
- Visual/story inspection remains mandatory when the picture changes.
- Thai/Unicode content must be visually inspected; successful encoding is not proof of correct shaping/readability.

## v0.1 scope

Implemented:

1. Capability doctor for FFmpeg/ffprobe/basic caption capability.
2. Probe-first normalized metadata: duration, dimensions, fps, VFR suspicion, codec, pixel format, HDR signal, rotation, audio.
3. `video.project.json` manifest.
4. Source SHA-256 fingerprint in `video.plan.json`.
5. Deterministic fit by explicit width/height using pad or crop.
6. ASS/libass caption burn-in suitable for Thai-capable fonts.
7. H.264/AAC MP4 reference render.
8. Technical QC for duration, dimensions, fps, file integrity and required audio presence.
9. First/middle/last inspection frames for independent visual review.
10. Synthetic self-test fixture.

Not yet production-active:

- Automatic editorial decisions.
- Highlight selection.
- Subject-aware smart reframe.
- Automatic silence removal.
- Beat editing.
- HDR-to-SDR policy.
- Brand profile registry.
- Platform delivery profiles.
- Audio loudness target enforcement.
- Multi-source timeline / B-roll / transitions.
- Automatic story-media semantic approval.

These remain `STOCK/QUEUE` until separately tested.

## Runtime commands

```bash
python runtime/video_runtime.py doctor
python runtime/video_runtime.py probe INPUT.mp4
python runtime/video_runtime.py plan video.project.json --out video.plan.json
python runtime/video_runtime.py render video.plan.json
python runtime/video_runtime.py verify OUTPUT.mp4 --plan video.plan.json
python runtime/video_runtime.py look OUTPUT.mp4 --out-dir inspection
python runtime/video_runtime.py self-test --workdir /tmp/mindway-video-test
```

All commands return JSON.

## Project manifest

Source of truth for one render is structured configuration rather than the final MP4.

Minimum:

```json
{
  "schema_version": "0.1",
  "project_id": "M14-S03-VIDEO",
  "story_spine": ["..."],
  "source": {"path": "input.mp4"},
  "captions": [{"start": 0.5, "end": 3.5, "text": "..."}],
  "delivery": {"width": 1920, "height": 1080, "fps": 30, "fit": "pad"},
  "output": {"path": "output.mp4", "overwrite": false}
}
```

## Promotion criteria

Remain `EXPERIMENTAL` until tests cover at minimum:

1. Synthetic local fixture PASS.
2. Thai caption visual inspection PASS.
3. Source overwrite protection PASS.
4. Stale-plan refusal PASS.
5. Real LMS 1080p/30 source PASS.
6. Real phone/iPhone source PASS, including HDR/VFR handling decision.
7. Representative story-media review PASS under Public Standard.

Only after evidence should this move `EXPERIMENTAL → TESTED → ACTIVE`.

## Provenance

Design patterns adapted from external `kajisho5/ffmpeg-skill` study: probe-first execution, dry/explicit plans, input fingerprinting, no-source-overwrite, machine-readable results, capability checks, technical verification and visual inspection. This implementation is a Mindway-specific experimental reference runtime rather than a copy or replacement of that external skill.
