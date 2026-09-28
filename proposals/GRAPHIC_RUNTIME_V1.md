# Proposal: Mindway Graphic Runtime v1

Status: REVIEW_READY
Date: 2026-08-07

## Decision proposed

Adopt `skills/graphic-runtime/SKILL.md` as Mindway's primary production skill for graphics, document-like visuals/PDF exports, motion graphics, and programmatic video until a faster method can match or exceed its accuracy and reliability gates.

## Why

The production source becomes inspectable code instead of a flattened generated image. This improves control over exact text, typography, dimensions, spacing, brand tokens, data values, animation timing, and repeatability.

## Default stack

- HTML/CSS/JS as the lightest common visual source of truth.
- SVG/Canvas/WebGL only where useful inside the composition.
- Playwright/Chromium for deterministic preview, screenshot, and PDF export.
- GSAP/CSS/Web Animations for simple motion.
- Headless Chromium + FFmpeg / an HTML-first renderer such as Hyperframes or html-video for MP4.
- Remotion as escalation for complex frame/timeline logic, not the default.

## Important refinement to the original idea

Do not make ordinary screen recording the default way to create video. It is simple, but it can introduce dropped frames, timing variance, browser/UI artifacts, and inconsistent capture.

Prefer deterministic frame/time rendering from the HTML animation, then encode to MP4. Use screen recording only for real interactive demos or when frame rendering is unavailable.

## Accuracy gates

1. wait for fonts and assets before capture
2. verify intended font resolution and multilingual glyph coverage
3. fixed viewport/artboard dimensions
4. detect overflow/clipping/scrollbars
5. compare critical rendered text/data against the approved source
6. verify image dimensions/aspect ratios
7. for video, verify first/last frames, scene timing, readable dwell time, audio sync, duration, and blank-frame flashes

## Trade-offs

### Advantages

- much stronger text and number accuracy than direct image generation
- fast edits because content and styling stay editable
- one source can export PNG, PDF, and motion/video variants
- reusable templates and brand primitives reduce repeated work
- easier automated QC
- version-control friendly

### Costs

- more engineering setup for highly artistic/photo-realistic scenes
- HTML/browser rendering can differ if font/assets are not locked
- complex video may need a frame-native engine such as Remotion
- third-party rendering projects must be license-checked before production adoption

## Compatibility

This proposal does not replace Mindway's public core protocol. It is a task-specific production skill and follows `/my`, minimum-context loading, evidence-first decisions, reversible changes, and approval boundaries.

## External patterns reviewed

- Microsoft Playwright CLI / Playwright screenshot, PDF, and recording workflows
- Vercel agent-browser browser automation patterns
- `nexu-io/html-video` and Hyperframes-style HTML/CSS/GSAP -> Chromium -> FFmpeg rendering
- Remotion for programmatic frame-based video
- agent frontend design-principle skills for typography/layout/token discipline

These are references only. Mindway should keep its own workflow abstraction so the underlying renderer can be replaced without changing the user-facing process.

## Upgrade path

Keep a renderer adapter boundary:

`brief -> content model -> visual composition -> renderer adapter -> QC -> deliverable`

This prevents lock-in. If a future renderer is faster or more accurate, replace the adapter rather than redesigning the whole workflow.
