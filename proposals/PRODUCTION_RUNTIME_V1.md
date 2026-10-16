# Proposal — Production Runtime v1

Status: PROPOSAL / NOT ACTIVE CANONICAL POLICY

## Mission

Promote the user's established code-first production method into a stable primary Mindway production system for images, visual documents, PDF, motion/video, narration/audio, and other repeatable productivity artifacts.

## Why this proposal exists

Graphic Runtime already makes deterministic code-first visual production mandatory under `/my`, but several operational gaps remain:

1. Literal prompt following can still defeat the user's understood goal.
2. There is no explicit candidate-search / rank / select runtime.
3. There is no explicit five-minute production budget.
4. Large-batch generation can be wasteful if every candidate is fully rendered.
5. Motion/video needs its own frame/timeline/QC rules.
6. Static-browser rendering needs a regression and fallback policy.
7. Audio Runtime is strong, but needs to be explicitly coupled to Motion Runtime and Production Runtime.
8. There is no single release rule preventing an agent from knowingly using an inferior established method.

## Proposed architecture

```text
                         MINDWAY /my
                              |
                        Production Runtime
                              |
             +----------------+----------------+
             |                |                |
        Static/Graphic      Motion/Video      Text/Artifacts
             |                |                |
 HTML/CSS/JS/SVG         Timeline IR       Structured source
 Playwright/resvg        Remotion-style     candidate search
 screenshot/PDF          frame renderer     native/code output
             |                |
             +------- Audio Runtime ---------+
                         Speech IR / TTS
                              |
                            FFmpeg
                              |
                         QC / Release
```

## Core policy changes proposed for later review

### A. Intent-aware production

When a literal instruction materially conflicts with the user's established desired outcome, use a dual-track rule:

- Track A: best literal interpretation, only when useful.
- Track B: best intent-aligned interpretation based on mission and context.

Do not ship a worse result merely because it follows wording more literally.

Hard locks, verified source, safety, privacy, approval gates, and high-impact decisions still outrank inferred intent.

### B. GEN1000 search funnel

`GEN1000` should mean broad candidate-space search, not automatically 1000 full-resolution renders.

Recommended default:

`1000 candidate specs -> top 50 -> 12-24 rendered previews -> top 3 -> final`

This keeps selection breadth while protecting the five-minute budget.

### C. Five-minute default timebox

Ordinary production should target a useful verified result within five minutes when the environment permits.

If a materially better phase is expected to exceed five minutes, report that before the expensive phase and offer a faster path.

### D. Deterministic static route

`verified source -> structured content -> HTML/CSS/JS/SVG -> pinned browser/runtime -> screenshot/export -> visual QC -> output`

Use screenshot-to-PDF when browser screenshot is stable and direct browser PDF is not, provided raster PDF is acceptable.

Maintain visual regression baselines for stable templates.

### E. Deterministic motion route

`verified source -> timeline IR -> deterministic frame state -> exact frames -> FFmpeg encode -> audio/caption sync -> QC`

Do not use manual screen recording as the production master when frame-controlled rendering is available.

### F. Audio control boundary

The pipeline, pronunciation rules, prosody parameters, routing, processing, mixing, timing, and QC can be code-controlled. Do not claim that every neural TTS engine can produce acoustically bit-identical or perfectly controllable output: cloud/model updates and model behavior can introduce variation. Use lockfiles, canary suites, candidate synthesis, and regression QC.

### G. Better-method exception

The runtime is primary until another method is demonstrated to be faster while matching or exceeding:

- intent fidelity;
- factual/text accuracy;
- reproducibility;
- editability;
- batchability;
- QC strength;
- total production time.

A replacement should be compared before promotion, not adopted because it is newer.

## Existing Mindway assets reused

- `/myN` Execution Loop for bounded continuation.
- `/fy` for topology and cycle planning.
- Swarm Runtime for differentiated research/build/critic/verifier roles where supported.
- Graphic Runtime as current mandatory code-first baseline.
- Audio Runtime for Speech IR, pronunciation, TTS routing, lockfiles, incremental builds, and audio QC.

## New proposed skills

- `skills/production-runtime/SKILL.md`
- `skills/motion-runtime/SKILL.md`

## Promotion patch proposed for canonical `/my`

After review, canonical `/my` could add a short section similar to:

```text
## Production Runtime — mandatory for /my production work

For production work, use skills/production-runtime/SKILL.md in addition to the relevant task runtime.

Outcome fidelity: do not knowingly ship a worse result merely because it follows a local instruction literally when the user's established mission clearly indicates a better interpretation. Preserve hard locks, verified sources, safety, privacy, and approval gates. When material ambiguity remains, use literal and intent-aligned tracks as defined by Production Runtime.

Use broad candidate search with cheap filtering before expensive full rendering. Default ordinary production target is <=5 minutes when feasible; ask before an expected longer expensive phase.

Static visual production uses Graphic Runtime. Motion/video uses Motion Runtime. Narration/audio uses Audio Runtime. Reuse one structured content source across outputs whenever practical.
```

## Trade-offs

### Benefits

- fewer context-understanding failures;
- fewer content-loss failures;
- larger design search space without brute-force cost;
- repeatable batch production;
- stronger Thai/text accuracy;
- one source across image/PDF/video;
- easier regression testing and repair;
- less vendor lock-in.

### Costs / risks

- more runtime code/templates to maintain;
- visual golden tests require pinned environments;
- scoring remains partly judgment-based;
- 1000-spec search can still be wasteful if candidate dimensions are poorly designed;
- Remotion may have licensing implications depending on team/company usage;
- browser rendering is not pixel-identical across environments unless pinned;
- TTS acoustic output is not universally deterministic;
- raster screenshot PDFs are less semantically accessible/editable than native vector/text PDFs.

## Promotion gate

Do not merge merely because the proposal exists. Before canonical promotion:

1. test one memo/PDF;
2. test one 20+ image batch;
3. test one carousel/social-size batch;
4. test one 15-60 second motion graphic;
5. test one narrated video with Thai/English mixed terms;
6. measure wall-clock time and failures;
7. verify fallback behavior;
8. compare output against the current Graphic Runtime baseline;
9. promote only if the new runtime is at least as accurate and more useful.
