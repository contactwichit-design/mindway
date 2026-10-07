# Video Runtime v0.1 — Experimental Test Report

Date: 2026-10-07
Branch: `exp/video-runtime-v0.1`
Status: `EXPERIMENTAL`
Promotion: **NOT ACTIVE**

## Mission

Test the smallest reusable T15 Media Production execution path:

`PROBE → PROJECT MANIFEST → PLAN → RENDER → TECHNICAL QC → VISUAL INSPECTION`

without changing canonical `/my` or replacing Template System T15.

## Environment

- FFmpeg: 7.1.5
- ffprobe: 7.1.5
- Python: 3.13.5
- Required filters detected: `ass`, `subtitles`, `drawtext`
- Encoders detected: H.264 + AAC
- Thai fonts available
- Test path: local/synthetic; no company, employee, patient, or private source media used

## Automated regression results

Result: **4 / 4 PASS**

1. `test_ass_time` — PASS
2. `test_self_test_when_ffmpeg_available` — PASS
3. `test_source_overwrite_rejected` — PASS
4. `test_stale_plan_refused` — PASS

The branch version itself was read back, reconstructed, compiled, and rerun. Runtime blob SHA matched GitHub read-back evidence.

## Synthetic fixture result

Input:

- 4.00 s
- 1280 × 720
- 30 fps CFR
- H.264 / yuv420p
- AAC mono / 48 kHz

Output:

- 4.01 s
- 1920 × 1080
- 30 fps
- H.264 / yuv420p
- AAC mono / 48 kHz
- output non-empty
- source audio preserved
- technical QC: PASS

## Thai / visual inspection

Caption test:

`ทดสอบ Video Runtime • Probe → Plan → Render → QC`

Inspection frames:

- 0.15 s: caption correctly absent; no blank frame
- 2.005 s: Thai/English caption visible, readable, no tofu, no broken Thai shaping observed
- 3.86 s: caption correctly absent; no blank frame

Visual QC result for this fixture: **PASS**

Story-media QC remains a calling-agent/human gate by design. The deterministic runtime does not self-promote a technically valid file to `REVIEW_READY`.

## Implemented in v0.1

- probe-first media metadata
- structured `video.project.json`
- source SHA-256 fingerprinted `video.plan.json`
- stale-plan refusal
- source overwrite protection
- deterministic pad/crop fit
- ASS/libass captions
- Thai-capable rendering path
- H.264/AAC reference render
- technical verification
- first/middle/last inspection frames
- machine-readable JSON results
- synthetic self-test

## Not yet proven

These are not ACTIVE and are not blockers for the current experimental fixture:

- real LMS 1080p/30 input
- real phone/iPhone VFR
- HDR / Dolby Vision handling
- delivery/platform profiles
- loudness enforcement
- brand profile registry
- multi-source timeline/B-roll
- smart reframe
- automatic editorial decisions
- automatic story-media semantic approval

## Promotion gate

Keep status `EXPERIMENTAL` until at minimum:

1. Synthetic fixture — **PASS**
2. Thai caption visual inspection — **PASS**
3. Source overwrite protection — **PASS**
4. Stale-plan refusal — **PASS**
5. Real LMS 1080p/30 source — PENDING
6. Real phone/iPhone source, including HDR/VFR decision — PENDING
7. Representative Public Standard story-media review — PENDING

Current decision: **continue testing; do not merge/promote to ACTIVE yet.**
