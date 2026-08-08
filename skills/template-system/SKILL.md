# Mindway Universal Template System

Status: CANDIDATE
Purpose: reduce AI guesswork, repeated setup, inconsistent outputs, and unnecessary template duplication.

## Principle
Do not begin from file type. Begin from intent and compose reusable primitives.

`REQUEST → ROUTE → COMPOSE → SOURCE → EXECUTE → VERIFY → OUTPUT → HANDOFF`

Prefer UPDATE_EXISTING over CREATE_NEW. Reuse structured content across renderers where possible.

## Universal primitives
Every production template may draw from these primitives:

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
11. STATUS — DONE / REVIEW_READY / NEED_CONFIRM / BLOCKED or task-specific equivalent.

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

## Router
Classify the request by behavior, not file extension. Select the smallest sufficient set of families and primitives. Do not ask the user to choose a template when intent is inferable.

Examples:
- approval memo → T01 + T09 + T10 + T07
- LMS clip → T01 + T14 + T15 + T11 + T07 + T06
- sales dashboard → T01 + T08 + T04 + T13 + T07
- recurring routine → T01 + T16 + T05 + T17 + T07

## Routing rules
1. Load only task-relevant sources.
2. Search existing capability by behavior before creating a new template.
3. Compose the minimum sufficient family set.
4. Preserve source truth and provenance.
5. Keep content/schema separate from renderer when practical.
6. Use deterministic code-first rendering for visual/media work under `/my`.
7. Verify before counting an artifact as complete.
8. Route around soft blockers; stop only on a proven hard gate.
9. Record durable learning only when it changes future execution.

## Content / Renderer separation
A content object is the semantic source of truth. Renderer profiles transform it into outputs such as chat HUD, HTML, PDF, document, slides, image, video, or connected-system records. Do not rewrite the same semantic content independently for each output unless the medium requires a real semantic change.

## Design profiles
Design is an override layer, not a fork of the workflow template.

Profiles may include:
- ZAFT PERSONAL DNA
- PLUS CORPORATE DNA
- task/project-specific locked brand systems

A profile controls typography, spacing, surfaces, palette, iconography, motion, density, and output-specific layout without changing source truth.

## Completion contract
A template-produced artifact is complete only when its task-specific Definition of Done is satisfied and evidence exists. Draft, candidate, folder-only, part-only, script-ready, or local-only states must not be promoted to completed when the owner system requires stronger evidence.

## Blocker integrity
Every BLOCKED / STOPPED / SKIPPED / NOT_DONE state must state:
- exact blocked action;
- reason and evidence;
- validity: HARD / SOFT / INVALID;
- safe fallback;
- independent work that can continue;
- exact unblock condition.

Before stopping, test read-only discovery, alternative source/artifact, reversible setup, smaller safe subtask, and independent supporting work.

## Evolution gate
Update this system only when evidence shows at least one of:
- reduced cycle time or manual steps;
- reduced error or rework;
- improved output quality or consistency;
- closed safety/capability gap;
- closed benchmark/regression gap;
- proven scale or maintenance need.

Avoid family proliferation. New families require behavior that cannot be represented cleanly by existing composition.
