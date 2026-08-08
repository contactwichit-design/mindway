---
name: production-runtime
description: Primary Mindway runtime for high-fidelity production across images, PDFs, documents, batch graphics, text variants, and code-generated artifacts. Uses intent-aware dual-track interpretation, deterministic code-first rendering, candidate search, strict QC, and a five-minute default timebox.
version: 1.0.0-proposal
status: PROPOSAL
---

# Mindway Production Runtime v1 — Proposal

## Purpose

Make production faster, more accurate, more repeatable, and more aligned with the user's actual goal rather than blindly obeying a locally worded instruction that conflicts with established context.

Default model:

`MISSION -> INTENT MODEL -> STRUCTURED SOURCE -> CANDIDATE SEARCH -> CHEAP FILTER -> DETERMINISTIC RENDER -> QC -> RANK -> RELEASE`

This runtime extends Graphic Runtime. It does not weaken source, safety, approval, or factual constraints.

## 1. Outcome fidelity outranks literal obedience

Use this precedence when interpreting a production request:

1. Safety, privacy, law, platform limits, and approval gates.
2. Verified source of truth and explicit hard locks.
3. The user's stable mission and established preferences relevant to the current task.
4. The user's current explicit instruction.
5. Inferred intent from the conversation and prior accepted outputs.
6. Tool defaults and model habits.

A current instruction is not automatically a hard lock. When it appears to conflict with the user's demonstrated goal, do not silently ship a worse result merely because it is literal.

### 1.1 Dual-track interpretation rule

When the explicit instruction and inferred desired outcome materially conflict:

- `TRACK A — Literal`: produce the best safe version that follows the instruction as written, only when preserving this version is useful for compatibility, comparison, or user intent.
- `TRACK B — Intent`: produce the version that best matches the user's likely desired outcome based on mission, context, prior preferences, and accepted patterns.

If Track A would clearly add no value and there is no hard requirement to preserve it, it may be omitted. Never conceal the interpretation conflict.

For high-impact business, legal, clinical, destructive, publishing, or irreversible decisions, do not substitute inferred intent for required approval.

## 2. Five-minute default production budget

Default wall-clock target for ordinary production work: `<= 5 minutes` when the active environment and tools make that feasible.

Rules:

- Prefer the fastest route that meets or exceeds required fidelity and QC.
- Do not perform expensive brute-force rendering merely because a large candidate count was requested.
- If a materially better method is expected to exceed five minutes, tell the user before starting the expensive phase and offer the faster alternative.
- Tool or platform latency outside the agent's control must be reported honestly; never claim a runtime that was not observed.

## 3. Gen1000 is a search strategy, not a requirement to full-render 1000 files

The default `GEN1000` pattern means exploring a large candidate space cheaply and rendering only promising candidates at full fidelity.

Recommended funnel:

`1000 candidate specs -> static validation -> score -> top 50 -> low-cost preview -> top 12-24 -> full render -> visual QC -> top 3 -> final selection`

Candidate specs may vary:

- layout system;
- hierarchy;
- spacing;
- typography scale;
- composition;
- copy treatment;
- crop;
- image placement;
- diagram topology;
- motion timing;
- narration pacing;
- output dimensions.

Do not generate meaningless random variations. Candidate generation must explore plausible design hypotheses derived from the mission and context.

### 3.1 Selection score

Default weighted score, adjustable per task:

- Goal / concept fidelity: 35
- Factual and text correctness: 25
- Context / user-fit: 15
- Information hierarchy and usability: 10
- Rendering robustness / reproducibility: 10
- Novelty / aesthetic interest: 5

Any candidate with a hard-lock violation, missing required content, broken Thai/Unicode, clipping, incorrect fact, wrong dimensions, or missing asset is rejected regardless of total score.

## 4. Code-first production hierarchy

Default deterministic tool order:

1. HTML/CSS/JS/SVG for layout-heavy visual work.
2. Playwright/Chromium for browser rendering, screenshot capture, and visual regression.
3. SVG + a deterministic renderer such as resvg for suitable static vector work.
4. Canvas or other deterministic code renderer when it materially improves speed or fidelity.
5. Native document/spreadsheet tools when the requested editable format requires them and they outperform the code route.
6. Generative visual models as supporting-asset generators, not the primary compositor for text/layout-critical work unless explicitly requested or deterministic rendering is unsuitable.

The structured source, not the PNG/PDF/video, is the persistent source of truth whenever practical.

## 5. Static production pipeline

For posters, social graphics, carousels, diagrams, dashboards, profile cards, infographics, certificates, reports, memos, and visual PDFs:

`verified content -> content.json -> template -> exact viewport render -> screenshot/export -> visual QC -> output`

Required QC:

- fonts loaded before capture;
- Thai/Unicode glyph coverage;
- no clipping or overflow;
- all required content present;
- source facts unchanged;
- correct logo/assets;
- correct canvas dimensions and safe margins;
- first render repeatable in the same pinned environment;
- final image visually inspected, not only syntax-checked.

For stable templates, maintain golden screenshots and use visual-diff regression where possible.

## 6. Multi-output reuse

Prefer one structured content model across outputs.

Example:

`content.json -> 1080x1080 PNG`
`content.json -> 1080x1350 PNG`
`content.json -> A4 PDF`
`content.json -> 1920x1080 video scene`

Do not rewrite the same facts independently for each output unless necessary.

## 7. Text and non-visual productivity generation

The candidate-search principle also applies to writing and structured artifacts when doing so is faster and improves quality.

Examples:

- message polishing;
- memo wording;
- interview question banks;
- SOP wording;
- naming;
- summaries;
- spreadsheet formulas;
- template generation;
- JSON/YAML/CSV handoffs;
- HTML guides;
- code scaffolds.

Use cheap internal variants, evaluate against one shared rubric, and return only the strongest result unless comparison materially helps the user.

Do not produce hundreds of visible variants. Search broadly internally; surface narrowly.

## 8. Failure prevention

### 8.1 Content-loss gate

Never shorten required content only to force a page, image, slide, or viewport constraint unless the user explicitly prefers omission over expansion.

When content does not fit:

1. improve layout;
2. reduce unnecessary decoration;
3. adjust spacing/type within readability bounds;
4. change component arrangement;
5. expand to another page/frame;
6. only then propose content reduction.

### 8.2 Renderer fallback ladder

If the primary browser route fails:

1. retry with a clean deterministic local server and pinned browser;
2. capture screenshot instead of browser PDF when screenshot is more stable;
3. convert verified screenshot(s) to PDF when raster PDF is acceptable;
4. use resvg for compatible static SVG;
5. use another deterministic code renderer;
6. only use a lower-fidelity path if the user accepts the trade-off.

Do not silently fall back to a method known to lose content or break typography.

### 8.3 Asset readiness gate

Before render, confirm required local assets exist and are readable. For remote assets, cache them locally when licensing and permissions allow.

### 8.4 Environment pinning

For production templates, record:

- browser/runtime version;
- viewport;
- device scale factor;
- fonts and versions when distributable/licensed;
- locale;
- timezone if visible dates are rendered;
- rendering dependencies.

Visual regression should run in the same environment as the baseline because browser screenshots may differ across operating systems and browser versions.

## 9. Candidate manifest

For nontrivial or batch work, maintain a compact manifest:

```json
{
  "mission": "...",
  "hard_locks": [],
  "intent_notes": [],
  "candidate_count": 1000,
  "rendered_preview_count": 24,
  "finalist_count": 3,
  "selected_id": "C0714",
  "score": {
    "goal": 35,
    "facts": 25,
    "context": 14,
    "usability": 10,
    "robustness": 10,
    "novelty": 4
  },
  "qc": {
    "fonts": "pass",
    "overflow": "pass",
    "facts": "pass",
    "dimensions": "pass"
  }
}
```

Do not fabricate candidate counts or QC results. Record only what was actually executed.

## 10. Relationship to other Mindway runtimes

- Graphic Runtime defines the mandatory deterministic visual-production baseline.
- Production Runtime adds interpretation, candidate search, ranking, timeboxing, and cross-output reuse.
- Motion Runtime handles deterministic video and animated-media production.
- Audio Runtime handles narration, pronunciation, prosody, TTS routing, audio QC, and mix.
- Execution Loop controls continuation.
- `/fy` chooses topology and useful cycle budget.

## 11. Release rule

A result may be released only when:

- the requested mission is preserved;
- no known hard-lock violation remains;
- visible text/facts match verified source;
- output has passed format-specific QC;
- the selected candidate is not merely the most literal candidate when a clearly better intent-aligned candidate exists;
- the runtime did not knowingly use an inferior method when a faster, more accurate, and available method was already established.

If a new method demonstrably exceeds the current runtime in speed, accuracy, reproducibility, and intent fidelity, record it as a proposal and compare before replacing the default.