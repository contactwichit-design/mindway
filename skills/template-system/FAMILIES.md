# Template Family Contracts

Status: REVIEW_READY  
Version: 0.2.0

Each family below is a reusable behavioral contract, not a file-format template. Load only selected families.

## T01 — Mission / Task
Use when defining work.
- Required: objective, scope, owner, priority, source/inputs, constraints, Definition of Done, expected artifact, next action.
- Fail if: mission is vague enough to change output materially.
- Typical output: task brief / execution contract.

## T02 — Research / Discovery
Use for search, learning, evidence gathering, source comparison.
- Required: question, source priority, search boundary, findings, evidence, source gaps, internal/external/inference separation.
- QA: freshness, authority, provenance, unsupported claims.
- Typical output: research note / source map / comparison.

## T03 — Plan / Execution
Use when work must be sequenced.
- Required: outcome, phases, work units, dependencies, owner, priority, evidence per unit, blocker route, stop gates.
- QA: executable order, dependency correctness, no cosmetic tasks.
- Typical output: roadmap / run board / production plan.

## T04 — Decision
Use when choosing among alternatives.
- Required: decision question, options, criteria, evidence, trade-offs, reversibility, recommendation, approval boundary.
- QA: criteria consistency, unknowns visible, no invented certainty.
- Typical output: decision memo / recommendation.

## T05 — Status / Compact HUD
Use for routine or progress reporting.
- Required: STATUS, mission/primary, Δ change, evidence, blocked/not-done + reason + validity, safe continuation, next, risk/gate.
- Do not repeat unchanged background.
- Token/quota only if measured; otherwise UNAVAILABLE.

## T06 — HOFF / Continuity
Use when another AI/person/session must resume.
- Required: mission, owner system, exact sources/IDs, verified completed work, current state, decisions/locks, blocker, next action, artifact paths, status.
- QA: resume without reconstructing the whole conversation.

## T07 — QA / Review
Use to verify an artifact or process.
- Required: source baseline, checks, expected result, actual result, PASS/FAIL per gate, debt, regression, acceptance boundary.
- Maker output cannot self-promote beyond required owner/gatekeeper approval.

## T08 — Data / Analysis
Use for tables, spreadsheets, metrics, quantitative/structured analysis.
- Required: schema, source, transformation, validation, metrics, exceptions, interpretation, action.
- QA: row/column identity, formulas, missingness, reconciliation, reproducibility.

## T09 — Communication
Use for email, LINE, memo copy, announcement, outreach.
- Required: audience, objective, context, facts, tone, CTA/next step, attachments/links if relevant.
- QA: recipient/action clarity, no unsupported claims, privacy/approval boundary.

## T10 — Document
Use for SOP, report, proposal, memo, policy draft, formal reading artifacts.
- Required: audience, reading goal, hierarchy, content sections, evidence, version/status, renderer/export rules.
- QA: completeness, headings, typography/glyphs, pagination/export when rendered.

## T11 — Visual / Graphic
Use for graphics, infographics, diagrams, posters, visual docs.
- Required: message, audience, source facts, visual hierarchy, design profile, canvas/viewport, assets, accessibility, deterministic renderer.
- Runtime: structured content → HTML/CSS/JS/SVG or equivalent → render → QC.
- QA: fonts/glyphs, clipping, facts, dimensions, asset load, visual hierarchy.

## T12 — Presentation
Use for decks/training/pitches.
- Required: audience, objective, narrative arc, slide roles, evidence, speaker intent, visual profile, export.
- QA: one job per slide, narrative continuity, source accuracy, readability.

## T13 — Web / UI
Use for websites, dashboards, applications and interactive surfaces.
- Required: user/job, information architecture, states, actions, data/source contract, components, responsive behavior, accessibility, error/loading/empty states, deployment gate.
- QA: functional paths, state coverage, responsiveness, accessibility, smoke tests.

## T14 — Learning / LMS
Use for lessons, modules, training and assessment.
- Required: learner, objectives, prerequisite, content/source boundary, lesson architecture, reinforcement, assessment, assignment if applicable, QA, registration.
- If media exists compose T15/T11.
- Never invent clinical/policy/business truth.

## T15 — Media Production
Use for video, audio, narration, subtitles and motion.
- Required: source/script, timeline/scene architecture, narration, audio identity, subtitle/timing, visuals, render target, technical QA.
- Audio/subtitles must derive from verified media timing where required.
- QA: duration, blank frames, sync, first/last frames, captions, codec/output evidence.

## T16 — Automation / Agent
Use for scheduled/triggered/repeated work.
- Required: trigger/cadence, inputs, state, actions, tools, permissions, idempotency, retry, verification, blocker behavior, notification policy, stop condition.
- QA: no duplicate runs/writes, safe failure, observable evidence.

## T17 — Blocker / Recovery
Use whenever progress is blocked or skipped.
- Required: exact action, reason, evidence, HARD/SOFT/INVALID, safe fallback, independent work, unblock condition.
- Before stopping test: read-only discovery, alternate source/tool, reversible setup, smaller subtask, independent unit.
- A final-approval gate blocks finalization, not necessarily production preparation.

## T18 — Evolution / Maintenance
Use to improve reusable systems/skills/templates.
- Required: candidate, existing coverage, failure/gap, measurable value, evidence, comparison, UPDATE_EXISTING/CREATE_NEW/DEPRECATE/NO_CHANGE/NEED_CONFIRM, regression/dependency impact, rollback.
- Architecture growth requires evidence and applicable owner approval.

## Shared completion rule
Every family inherits the universal primitives and owner-system truth. Completion is determined by the strongest applicable task-specific gate, not filenames or optimistic labels.