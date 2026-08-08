---
name: template-system
description: Route recurring Mindway work into reusable intent-based template families, machine-readable primitives, design profiles, renderers, QA and blocker recovery so AI can execute faster with less guesswork and duplication.
version: 0.2.0
status: REVIEW_READY
---

# Mindway Universal Template System

## Purpose
Reduce AI guesswork, repeated setup, inconsistent outputs, missing QA/gates and unnecessary template duplication.

## Core principle
Do not begin from file type. Begin from intent and compose reusable behavioral families.

`REQUEST → ROUTE → COMPOSE → SOURCE → EXECUTE → VERIFY → OUTPUT → HANDOFF`

Prefer UPDATE_EXISTING over CREATE_NEW. Reuse structured content across renderers whenever possible.

## System components
- `REGISTRY.md` — compact T01–T18 index.
- `SYSTEM.json` — machine-readable families, primitives, recipes and rules.
- `ROUTER.md` — AI routing contract.
- `FAMILIES.md` — full behavioral contracts for all 18 families.
- `DESIGN_PROFILE_ZAFT_PERSONAL.md` — personal design override layer.
- `TESTS.md` — routing/regression/benchmark protocol.
- `runtime/template_router.py` — deterministic behavior-tag/recipe router and self-tests.

## Universal primitives
1. MISSION — objective, scope, owner, priority, Definition of Done.
2. INPUT — supplied material, required fields, assumptions.
3. SOURCE — owner system, provenance, current/locked/candidate/archive state.
4. CONSTRAINT — safety, approval, brand, format, time, cost.
5. PROCESS — ordered execution units and dependencies.
6. OUTPUT — required artifact and renderer/profile.
7. EVIDENCE — paths, IDs, citations, measurable delta.
8. QA — checks, regression, readback, acceptance criteria.
9. BLOCKER — exact blocked action, evidence, validity, fallback, unblock condition.
10. NEXT — one highest-value continuation action.
11. STATUS — task state supported by current governance/owner system.

## Template families
T01 Mission / Task  
T02 Research / Discovery  
T03 Plan / Execution  
T04 Decision  
T05 Status / Compact HUD  
T06 HOFF / Continuity  
T07 QA / Review  
T08 Data / Analysis  
T09 Communication  
T10 Document  
T11 Visual / Graphic  
T12 Presentation  
T13 Web / UI  
T14 Learning / LMS  
T15 Media Production  
T16 Automation / Agent  
T17 Blocker / Recovery  
T18 Evolution / Maintenance

## Router behavior
1. Classify by behavior, not extension.
2. Search existing capability before creating a new template.
3. Compose the minimum sufficient family set.
4. Resolve owner-system truth before substantive production.
5. Keep semantic content separate from renderer/design profile.
6. Use deterministic code-first rendering for visual/media work under `/my`.
7. Verify before completion.
8. Route around soft blockers; stop only the affected action on a real hard gate.
9. Record durable learning only when it changes future execution.

Do not ask the user to choose a template when intent is inferable.

## Content / renderer separation
The semantic content object is the source of truth. Renderer profiles transform it into chat, Markdown, HTML, PDF, DOCX, slides, image, video or connected-system output. File type is an output decision, not the primary work definition.

## Design profiles
Design is an override layer, not a fork of the workflow. A project/owner-system locked brand overrides a generic or personal profile for its scope.

## Blocker integrity
Every BLOCKED / STOPPED / SKIPPED / NOT_DONE state must include:
- exact blocked action;
- reason and evidence;
- HARD / SOFT / INVALID;
- safe fallback;
- independent work that can continue;
- exact unblock condition.

Before stopping, test read-only discovery, alternative source/artifact, reversible setup, smaller safe subtask and independent supporting work.

## Completion contract
Completion is determined by the strongest applicable task-specific/owner-system gate, not a filename or optimistic label. Draft, candidate, folder-only, part-only, script-ready and local-only states must not be promoted when stronger evidence is required.

## Evolution gate
Update this system only when evidence shows reduced cycle time/manual steps, reduced error/rework, improved consistency/quality, closed safety/capability/regression gap, or proven scale/maintenance need. Avoid family proliferation.

## Verification status
- 18 family contracts defined.
- machine-readable registry created.
- deterministic router created and read back.
- 5 deterministic routing self-tests pass in equivalent runtime validation.
- 15 representative routing cases + 7 regression cases documented.
- core canonical `/my` not modified automatically.

Current status: REVIEW_READY. Promotion to APPROVED/LOCKED remains an owner/governance decision.