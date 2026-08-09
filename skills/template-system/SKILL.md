---
name: template-system
description: Route recurring Mindway work into reusable intent-based template families, machine-readable primitives, design profiles, renderers, QA and blocker recovery so AI can execute faster with less guesswork and duplication.
version: 1.0.0
status: CORE_ACTIVE
owner_approval: 2026-08-09
---

# Mindway Universal Template System

## Purpose
Reduce AI guesswork, repeated setup, inconsistent outputs, missing QA/gates and unnecessary template duplication.

## Core principle
Do not begin from file type. Begin from intent and compose reusable behavioral families.

`REQUEST → ROUTE → COMPOSE → SOURCE → EXECUTE → VERIFY → OUTPUT → HANDOFF`

Prefer UPDATE_EXISTING over CREATE_NEW. Reuse structured content across renderers whenever possible.

## Core `/my` behavior
For substantial work, `/my` uses this skill as its default reusable-work router when a template composition materially helps.

1. Infer intent from the user's natural request; do not require the user to name a template.
2. Read the compact registry/router first.
3. Select the minimum sufficient families only.
4. Load task/project owner-system truth and locked templates above generic family defaults.
5. Keep semantic content separate from renderer/design profile.
6. Execute and verify under the normal `/my` safety, approval and source rules.
7. Simple self-contained work may bypass Template System when loading it would add overhead without value.

## System components
- `QUICKSTART.md` — shortest human/AI entry and common recipes.
- `REGISTRY.md` — compact T01–T18 index and fast-load order.
- `SYSTEM.json` — machine-readable families, primitives, recipes and rules.
- `ROUTER.md` — AI routing contract.
- `FAMILIES.md` — full behavioral contracts for all 18 families.
- `TEMPLATES.md` — fillable T01–T18 YAML skeletons.
- `DESIGN_PROFILE_ZAFT_PERSONAL.md` — personal design override layer.
- `TESTS.md` — routing/regression/production-benchmark protocol.
- `BENCHMARK.md` — structural benchmark and unproven empirical claims.
- `BENCHMARK_1000_SIMULATION.md` — owner-defined 1000-case simulation and promotion evidence.
- `INTEGRATION_PROPOSAL.md` — integration history/decision record.
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
- classify by behavior, not extension;
- search existing capability before creating a new template;
- compose the minimum sufficient family set;
- resolve owner-system truth before substantive production;
- use deterministic code-first rendering for visual/media work under `/my`;
- verify before completion;
- route around soft blockers and stop only the affected action on a real hard gate;
- capture durable learning only when it changes future execution.

## Content / renderer separation
The semantic content object is the source of truth. Renderer profiles transform it into chat, Markdown, HTML, PDF, DOCX, slides, image, video or connected-system output. File type is an output decision, not the primary work definition.

## Design profiles
Design is an override layer, not a fork of the workflow. A project/owner-system locked brand overrides a generic or personal profile for its scope.

## Blocker integrity
Every BLOCKED / STOPPED / SKIPPED / NOT_DONE state must include exact blocked action, reason/evidence, HARD/SOFT/INVALID classification, safe fallback, independent work that can continue and exact unblock condition. Before stopping, test read-only discovery, alternative source/artifact, reversible setup, smaller safe subtask and independent supporting work.

## Completion contract
Completion is determined by the strongest applicable task-specific/owner-system gate, not a filename or optimistic label. Draft, candidate, folder-only, part-only, script-ready and local-only states must not be promoted when stronger evidence is required.

## Promotion evidence
The owner-directed 1000-case structural simulation covered broad domains, renderers, risk/complexity, source conditions and blocker states. Mean simulated productivity ratio was 3.59× baseline; the top-10 recipe average was 3.64×; all 1000 modeled cases exceeded the owner threshold of 2.0×. These are simulation/proxy results, not empirical time/token claims. See `BENCHMARK_1000_SIMULATION.md`.

Owner instruction explicitly approved immediate core promotion when that threshold passed. Core hook remains reversible and live production measurement continues.

## Evolution gate
Update this system only when evidence shows reduced cycle time/manual steps, reduced error/rework, improved consistency/quality, closed safety/capability/regression gap, or proven scale/maintenance need. Avoid family proliferation.

Current status: `CORE_ACTIVE`.