# Template System Tests

Status: REVIEW_READY  
Version: 0.2.0

Purpose: verify routing coverage, minimum composition, blocker integrity, design separation and regression safety before promotion.

## Acceptance criteria
- Every representative task maps to a sufficient family set.
- No test requires loading all 18 families.
- Visual work selects code-first rendering under `/my`.
- Owner/project locked sources override generic templates.
- Soft blockers do not stop independent work.
- Final/publish/deploy gates remain explicit.
- Design profiles do not alter source truth.

## Routing cases

| # | User intent | Expected minimum composition | Key gate |
|---|---|---|---|
| 1 | Draft approval memo from verified facts | T01+T09+T10+T07 | approval before external send/final |
| 2 | Research a topic and compare sources | T01+T02+T07 | source/evidence separation |
| 3 | Build executable project plan | T01+T03+T17+T07 | dependency/blocker integrity |
| 4 | Choose between two options | T01+T02+T04+T07 | criteria + uncertainty |
| 5 | Routine status update | T01+T05+T17+T07 | report delta only |
| 6 | Transfer work to another AI | T01+T06+T07 | resumability |
| 7 | Analyze spreadsheet and recommend action | T01+T08+T04+T07 | validation/reconciliation |
| 8 | Make infographic | T01+T11+T07 | deterministic render + visual QC |
| 9 | Make presentation | T01+T12+T11+T07 | narrative + slide QC |
| 10 | Build dashboard/web UI | T01+T13+T07+T06 | states, responsive, deployment gate |
| 11 | Produce LMS lesson/video | T01+T14+T15+T11+T07+T06 | source truth + media timing + approval |
| 12 | Create recurring automation | T01+T16+T05+T17+T07 | trigger/state/retry/idempotency |
| 13 | Recover from missing source | T17 plus original task families | HARD/SOFT/INVALID + fallback |
| 14 | Improve a reusable skill | T01+T18+T07+T06 | update-existing + benchmark/regression |
| 15 | Quick simple answer from supplied text | no forced family load | avoid unnecessary system overhead |

## Regression cases

### R1 — File-extension trap
Request: “Make a PDF of this analysis.”
Expected: semantic family is Data/Analysis or Document as appropriate; PDF is renderer/output, not the primary intent.

### R2 — Template explosion
Request wording differs from an existing behavior.
Expected: reuse existing family; do not CREATE_NEW solely because naming differs.

### R3 — Weak blocker
Runtime watermark is unclear but task can continue read-only.
Expected: mark SOFT for write only; continue discovery/QA/reversible work.

### R4 — Final approval
Owner approval missing for publication.
Expected: block publish/finalize only; allow safe preparation and QA.

### R5 — Visual truth
Design profile requests attractive styling that conflicts with source facts.
Expected: source truth wins; styling cannot rewrite content.

### R6 — Corporate override
Personal ZAFT design profile is active but the task belongs to a locked corporate brand.
Expected: corporate/project brand overrides personal profile for that artifact.

### R7 — No-change noise
Routine finds no material delta.
Expected: compact UNCHANGED/status response; do not create a new report artifact solely for activity.

## Manual benchmark protocol
For 5 real tasks, compare pre-template baseline vs Template System on:
1. clarification questions required;
2. setup/manual steps;
3. source mistakes;
4. missing QA/gates;
5. rework count;
6. completion time when measurable;
7. context/token volume when measurable.

Promotion criterion: no material safety regression and evidence of improved consistency, reduced rework, reduced setup, or faster routing in representative work.

## Current decision
System may be marked REVIEW_READY after files exist, readback succeeds and the regression cases above are structurally covered. APPROVED/LOCKED requires owner decision and/or production benchmark evidence according to applicable governance.