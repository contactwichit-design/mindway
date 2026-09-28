---
name: motion-runtime
description: Deterministic code-first production runtime for animated graphics and video under Mindway, using structured timelines, HTML/CSS/JS or Remotion-style frame logic, browser/frame rendering, FFmpeg encoding, audio synchronization, and strict visual/audio QC.
version: 1.0.0-proposal
status: PROPOSAL
---

# Mindway Motion Runtime v1 — Proposal

## Purpose

Make motion and video production reproducible, editable, batchable, and synchronized by treating a video as code + timeline + assets rather than as an opaque generation.

Default model:

`verified content -> scene/timeline IR -> deterministic visual runtime -> exact frames -> encode -> audio/subtitle sync -> QC -> release`

Video files are build artifacts. The source of truth is structured content, timeline data, code, and approved assets.

## 1. Runtime hierarchy

Preferred routes:

1. HTML/CSS/JS/SVG with deterministic time/frame control for simple-to-medium motion graphics.
2. A programmatic video framework such as Remotion when component reuse, scene sequencing, parameterized renders, audio, captions, or large batch production materially improve the workflow.
3. Direct frame generation with Canvas/SVG/other code renderers when faster or more stable.
4. FFmpeg for image-sequence/video encoding, compositing, muxing, resizing, frame-rate conversion, loudness processing, and final packaging.
5. Generative video models may create supporting shots/assets when required, but must not replace deterministic composition when text, timing, branding, data, or repeatability are critical.

## 2. No manual screen recording as production master

Do not use manual screen recording as the authoritative source when deterministic frame capture is possible.

Instead define time explicitly:

- composition width/height;
- frames per second;
- exact duration;
- scene start/end;
- animation curves;
- asset timing;
- narration timing;
- caption timing.

Render frame `n` from deterministic state `t = n / fps`.

## 3. Timeline IR

Use a vendor-neutral scene/timeline representation where practical.

```json
{
  "video_id": "M14-S03",
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "duration_sec": 42,
  "scenes": [
    {
      "id": "SC01",
      "start": 0,
      "end": 6.5,
      "template": "title-card",
      "content_ref": "M14.S03.SC01",
      "audio_ref": "M14.S03.SC01.VO",
      "transition_out": "fade-8f"
    }
  ]
}
```

Stable scene IDs should survive revisions when the semantic scene remains the same.

## 4. Motion design as reusable components

Build reusable components rather than one-off timelines:

- TitleCard
- LowerThird
- StepCard
- Comparison
- Timeline
- Checklist
- Quote
- MetricCounter
- DiagramReveal
- ImagePanZoom
- DeviceFrame
- SubtitleTrack
- CTA
- Outro

Expose parameters such as text, images, colors, duration, emphasis, and timing. Reuse across modules and formats.

## 5. Deterministic animation rules

Prefer functions of frame/time rather than stateful animation that depends on real-time playback.

Examples:

- opacity = f(frame)
- translateY = f(frame)
- scale = f(frame)
- progress = clamp((frame-start)/(end-start))

Avoid sources of non-determinism:

- `Date.now()`;
- unseeded randomness;
- network assets during final render;
- animations that depend on wall-clock scheduling;
- asynchronous data without explicit render blocking;
- font loading after capture begins.

If randomness is visually useful, seed it and record the seed.

## 6. Video candidate search

Do not full-render hundreds of long videos to find a style.

Use a funnel:

`many timeline/style specs -> storyboard contact sheets -> short representative previews -> top candidates -> full render`

For example:

`200 motion specs -> 20 storyboard sheets -> 6 x 5-second previews -> 2 full renders -> 1 selected`

Use Production Runtime scoring, with extra motion checks:

- timing clarity;
- visual continuity;
- pacing;
- narration synchronization;
- readability per frame;
- transition restraint;
- first/last frame quality.

## 7. Audio integration

Use Mindway Audio Runtime as the narration authority.

Recommended coupling:

`content semantic IDs -> Speech IR -> approved audio segments -> measured durations -> timeline -> render`

The motion timeline should consume measured audio duration rather than guessing when narration determines pacing.

Prefer sentence/segment-level audio assets with stable IDs for incremental rebuilds.

## 8. Captions and subtitles

Generate captions from the same approved narration source whenever possible.

Do not independently rewrite subtitles from memory.

Caption QC:

- wording matches approved narration unless an intentional subtitle-shortening rule exists;
- time ranges do not overlap incorrectly;
- safe-area placement;
- adequate contrast;
- maximum readable line length;
- Thai segmentation reviewed where automatic wrapping is poor.

## 9. FFmpeg finalization

Use FFmpeg or an equivalent reproducible encoder for final packaging when available.

Typical responsibilities:

- image sequence -> H.264/H.265/VP9/AV1 video as required;
- mux narration/music/SFX;
- scale/pad/crop;
- frame-rate control;
- audio loudness normalization;
- trim/concat;
- metadata inspection;
- thumbnail/contact-sheet extraction.

Pin encoding settings in build config. Do not rely on undocumented GUI defaults.

## 10. Video QC gate

Before release verify at minimum:

### Structure
- expected width/height;
- expected frame rate;
- expected duration tolerance;
- expected codec/container;
- audio stream exists when required.

### Visual
- frame 0;
- first meaningful frame;
- scene boundaries;
- transition midpoints;
- final meaningful frame;
- final frame;
- no blank/black/white flashes unless intentional;
- no stale placeholders;
- no clipped text;
- correct Thai/Unicode;
- assets present.

### Timing
- narration starts/ends correctly;
- captions align;
- important text remains on screen long enough;
- no transition cuts off speech;
- no unintended dead air.

### Audio
- no clipping;
- target loudness profile met when specified;
- music ducking does not obscure speech;
- stereo/mono behavior intentional;
- sample rate/channel layout acceptable.

## 11. Regression and repair

For reusable video templates, maintain:

- storyboard/contact-sheet baselines;
- selected frame snapshots;
- metadata expectations;
- audio-duration expectations;
- build hashes/manifests.

A revision should rebuild only affected scenes/assets where feasible.

## 12. Video types supported by this runtime

This runtime is appropriate for any video whose critical composition can be represented by deterministic assets and timelines, including:

- LMS lessons;
- animated explainers;
- social reels;
- kinetic typography;
- infographic videos;
- product/service explainers;
- dashboard/data animations;
- training videos;
- slideshow/document motion;
- subtitles/lower-thirds;
- branded intros/outros;
- process/flow animations;
- video assembled from generated or filmed shots.

It does not claim that code alone can synthesize every photorealistic scene. For footage that must be generated, filmed, simulated, or rendered in 3D, use the best source-generation method and then bring the resulting assets into the deterministic composition/timeline.

## 13. Five-minute rule

For ordinary requests, target a useful result or verified preview within five minutes when feasible.

If a final full-resolution encode is expected to exceed five minutes:

1. produce storyboard or low-resolution proof first;
2. estimate the longer render based on actual measured performance when possible;
3. ask before committing to the expensive render if user approval is required by the current workflow.

Never lower factual, text, or synchronization QC just to meet the timebox.