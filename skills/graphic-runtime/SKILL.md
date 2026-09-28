---
name: graphic-runtime
description: Mindway primary code-first graphic/media production skill. Use for static graphics, posters, one-page visuals, presentation-like layouts, documents/PDFs, motion graphics, animated explainers, and videos when the output can be rendered deterministically from HTML/CSS/JS or an equivalent code renderer. Prioritize prompt fidelity, factual/text accuracy, typography correctness, reproducibility, speed, and visual QC.
status: proposal
version: 0.1.0
---

# Mindway Graphic Runtime

## Purpose

Create visual media from code as the source of truth instead of treating a generated bitmap as the master artifact.

Default principle:

`prompt/content -> structured scene/layout -> HTML/CSS/JS -> browser render -> QC -> PNG/PDF/MP4`

The goal is to make text, numbers, spacing, brand rules, fonts, and timing inspectable and repeatable.

## Default Scope

Use this skill for:

- posters, infographics, social graphics, banners, cards, dashboards, diagrams, visual summaries
- document-like pages and PDFs where exact layout matters
- animated slides, kinetic typography, motion graphics, explainers
- short-form and long-form programmatic videos
- reusable visual templates and batch-produced media

Do not use a generative image as the final compositor for text-heavy or layout-critical work unless the user explicitly asks for that style or the code-first route cannot achieve the intended visual. Generated imagery may still be used as an asset inside the coded composition.

## Runtime Hierarchy

### 1. Static master: HTML/CSS/JS + Chromium

Preferred for still graphics and document-like visuals.

- fixed artboard size and aspect ratio
- semantic HTML for text and data
- CSS variables/tokens for typography, spacing, palette, radii, shadows, grids
- SVG for icons, diagrams, logos, charts, and vector shapes where possible
- raster images only as placed assets, not as the layout master
- browser-rendered output via Playwright/Chromium

### 2. Static export

Preferred outputs:

- PNG/JPEG: browser screenshot at the exact viewport/artboard size
- PDF: browser PDF export from the same HTML layout when print fidelity is appropriate
- SVG: direct export when the composition is fundamentally vector and supported cleanly

### 3. Motion master: HTML/CSS/JS + deterministic time

Preferred for motion graphics and videos that can be represented in HTML.

- CSS animations, Web Animations API, GSAP, Canvas, SVG, or WebGL as needed
- animation timing must be driven by deterministic time/frame state
- do not depend on uncontrolled real-time randomness
- seed any randomness
- expose scene duration and key timestamps in code

### 4. Video render

Preferred order:

1. HTML-first engine using headless Chromium + frame/time capture + FFmpeg encoding
2. Hyperframes/html-video style pipeline when available for multi-scene HTML/CSS/GSAP production
3. Remotion only when React/frame logic offers a clear advantage for complex timelines, data-driven sequences, reusable compositions, or advanced video orchestration
4. FFmpeg for final encode, concat, audio mix, format conversion, and delivery packaging

The user's requested medium does not change the design source of truth: the coded composition remains master whenever practical.

## Required Production Flow

### Step 1 — Lock the brief

Capture only what is needed:

- output type
- target size/aspect ratio
- exact text/content/source
- visual hierarchy
- brand/design constraints
- required assets
- motion duration/FPS if applicable

Never invent critical names, numbers, policy, clinical claims, pricing, dates, or source facts.

### Step 2 — Build a structured content model

Separate content from visual code when the artifact is non-trivial.

Recommended structure:

- `content.json` or compact JS object for copy/data
- `tokens.css` or CSS variables for design system
- `index.html` / component files for composition
- `render.*` for export automation

This makes corrections fast and prevents text edits from breaking layout logic.

### Step 3 — Build deterministic layout

Use explicit dimensions and constraints.

Required rules:

- set exact viewport/artboard dimensions
- avoid responsive ambiguity for final exports unless multiple sizes are requested
- use grid/flex intentionally
- prevent accidental scrollbars
- check text overflow and clipping
- use safe-area margins
- avoid browser-dependent default margins/styles
- normalize box sizing

### Step 4 — Font gate

Font correctness is a hard gate.

Before capture:

- declare an explicit font stack
- load the intended font from an approved/local/web-safe source
- wait for `document.fonts.ready`
- verify the expected font actually resolved
- fail or flag QC if fallback font is used unexpectedly
- do not export while fonts are still loading

For Thai or multilingual work, verify glyph coverage for every required script.

### Step 5 — Asset gate

Before render:

- verify all local/remote assets loaded successfully
- check intrinsic image dimensions and cropping
- preserve logo aspect ratio
- prevent stretched images
- prefer SVG for logos/icons when available
- do not hotlink fragile assets in final production when a stable local copy is permitted

### Step 6 — Render

For stills:

- launch Chromium/Playwright
- set exact viewport
- wait for network idle or explicit readiness signal
- wait for fonts and images
- capture the exact artboard/element
- use high-resolution/device-scale capture when useful

For PDFs:

- use the same coded layout
- define print page size and margins explicitly
- verify pagination if multi-page

For video:

- define width, height, FPS, total duration
- render frames or deterministic browser capture
- encode with FFmpeg/H.264 unless another format is explicitly required
- capture audio separately or mix at encode stage when practical

### Step 7 — Visual QC gate

Do not deliver immediately after first render.

At minimum verify:

- all requested text is present and spelled correctly
- no unsupported/fallback glyphs
- no clipping, overflow, hidden text, or accidental scrollbars
- correct aspect ratio and pixel dimensions
- visual hierarchy matches the brief
- logo/brand constraints are respected when supplied
- images are not distorted
- key numbers and dates match the source
- contrast/readability is acceptable
- no debug UI, cursor, browser chrome, or accidental artifacts

For video also verify:

- first frame and last frame are intentional
- no blank flashes between scenes
- animation begins/ends at intended timestamps
- text stays on screen long enough to read
- transitions do not cover required information
- audio sync and duration match the timeline when audio exists

### Step 8 — Content QC gate

For source-backed work, compare the rendered artifact against the source content, not just the HTML source.

Use machine checks where practical:

- count/compare required text strings
- assert key data values
- check DOM bounding boxes for overflow
- detect missing images/fonts through browser console/network failures
- validate dimensions and duration

### Step 9 — Delivery package

Keep the editable coded master whenever useful.

Recommended outputs:

- source HTML/CSS/JS
- source content/data file
- final PNG/PDF/MP4
- optional preview image
- compact QC report only when the task is substantial or risk-sensitive

## Playwright Capture Pattern

Playwright/Chromium is the default capture layer because it can render the same HTML used for preview and export screenshots/PDFs at controlled dimensions.

Typical still workflow:

```text
open local HTML -> set viewport -> await readiness -> await document.fonts.ready -> screenshot
```

Typical document workflow:

```text
open local HTML -> set print CSS/page size -> await readiness -> PDF export
```

Typical motion workflow:

```text
open animated HTML -> drive deterministic timeline/frame -> capture frames or browser video -> FFmpeg encode
```

## Readiness Contract

Every non-trivial composition should expose a readiness signal so capture does not guess timing.

Example contract:

```js
window.__MINDWAY_READY__ = false;
Promise.all([
  document.fonts.ready,
  ...Array.from(document.images).map((img) => img.complete
    ? Promise.resolve()
    : new Promise((resolve, reject) => {
        img.addEventListener('load', resolve, { once: true });
        img.addEventListener('error', reject, { once: true });
      }))
]).then(() => {
  window.__MINDWAY_READY__ = true;
});
```

Capture automation should wait for `window.__MINDWAY_READY__ === true` before export.

## Deterministic Motion Contract

For reliable video, animations should be controllable by an explicit time value.

Recommended pattern:

```js
window.renderAt = (timeSeconds) => {
  // derive all animation state from timeSeconds
};
```

A renderer can then call `renderAt(frame / fps)` and capture exactly one frame at a time. This is more reliable than hoping a screen recorder samples a real-time animation perfectly.

If using a runtime that already provides frame-based rendering, use its native frame clock.

## Fast Path

For simple static graphics:

1. one self-contained HTML file
2. embedded CSS + SVG
3. Playwright screenshot
4. visual QC

For simple animated graphics/video:

1. one HTML file
2. GSAP/CSS/Web Animations
3. fixed duration
4. headless Chromium render
5. FFmpeg MP4 encode
6. video QC

Avoid introducing React, a bundler, or a heavy framework unless complexity justifies it.

## Complex Path

Escalate to Remotion or another frame-native renderer only when one or more apply:

- many scenes and reusable compositions
- data-driven repeated video production
- complex audio/timeline synchronization
- frame-perfect timeline logic is easier in a video framework
- large reusable animation component library

Even then, maintain the same Mindway guarantees: explicit content source, deterministic render, font/asset gates, and output QC.

## Reuse System

Prefer reusable primitives over one-off code:

- typography tokens
- spacing/grid tokens
- brand palette tokens
- logo/header/footer components
- chart/diagram primitives
- card/layout primitives
- caption/lower-third templates
- scene transition primitives
- safe-area guides
- render presets for common output sizes

Common presets may include:

- square social
- portrait social
- landscape presentation
- A4 portrait/landscape
- Full HD 16:9
- vertical 9:16 video

Do not hard-lock these if the task specifies another size.

## Failure Prevention

### Fonts

Never assume a font rendered because CSS named it. Verify load and glyph coverage.

### Thai text

Avoid canvas/text-render paths that silently substitute fonts unless verified. Browser DOM/SVG text is preferred for layout-heavy Thai work.

### Screenshots

Never capture before readiness. Crop to the intended artboard rather than leaving browser whitespace.

### PDF

Do not use PDF as the design source when the same content can originate from HTML. Treat PDF as an export format.

### Video

Do not rely on manual screen recording as the preferred production method when deterministic frame capture is available. Screen recording is a fallback for interactive/live UI demonstrations, not the default motion renderer.

### Generative visuals

Use generative images for illustrations/background/photographic assets when useful, but composite final text/layout in code for accuracy.

## Evidence-Informed References

The architecture is informed by open-source patterns including:

- Microsoft Playwright CLI: browser automation, screenshots, PDF export, video recording
- Vercel agent-browser / browser automation patterns
- html-video / Hyperframes: HTML/CSS/GSAP rendered through headless Chromium and FFmpeg to MP4
- Remotion: frame/programmatic React video rendering for complex cases
- frontend design-principle skills: intentional typography, layout, spacing, and token systems

These projects are references, not endorsements or required dependencies. Check current licenses and versions before embedding third-party code or using a dependency in production.

## Mindway Decision Rule

For any requested graphic/media artifact, choose the fastest method that preserves or improves:

1. factual/text accuracy
2. prompt fidelity
3. deterministic reproducibility
4. typography/layout correctness
5. visual quality
6. edit speed
7. export reliability

The code-first runtime is the default until another method demonstrably beats it on the same quality gates.

## Status

This file is a proposal skill. It should remain reversible and should not silently alter Mindway's public core protocol. Promote it only through the normal review/approval path.
