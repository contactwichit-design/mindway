---
name: review-360
description: Evidence-first 360-degree review with iterative diagnosis, scoped repair, and re-verification for past work, current artifacts, and future plans.
version: 1.0.0
status: ACTIVE
owner_approval: 2026-10-09
---

# /360 — Mindway Review → Repair → Re-review

## Entry and purpose
Always enter canonical `/my` and required references before substantial review. `/360` is an owner-facing command for structured, evidence-first multi-dimensional review. It never means merely praising, rating, or listing suggestions. The invariant is:

`BASELINE → FIND DEFECT → REPAIR (when authorized and feasible) → VERIFY → RE-REVIEW → DECIDE`

When the user asks for a retrospective and future-plan review together, default to 10 iterative rounds for EACH group (20 total), unless the owner specifies a different cycle budget. For an unspecified ordinary `/360`, infer a bounded number of useful rounds based on scope; avoid arbitrary 20-round overhead. Follow `/loop` for bounded continuation and checkpointing.

## Minimum review dimensions
Use relevant dimensions, not a ceremonial fixed score: mission/Definition of Done, functional correctness, data integrity/authority, upstream/downstream dependencies, privacy/security/permissions, practical executability/tool capabilities, human workflow/UX, cost/resource constraints, failure handling/reversibility, test coverage/read-back, maintainability/operations, release/approval, and continuity/evidence.

## Cycle contract
Each distinct round must record:
1. Scope and current baseline (with source/evidence state).
2. New defect or highest-priority unresolved risk.
3. Exact corrective change. Execute an authorized safe repair where tools allow; otherwise revise the specific implementation plan, contract, artifact or test and mark it `PLAN_ONLY`.
4. Re-review against the stated acceptance check; classify `PASS_VERIFIED`, `PLAN_REVIEW_PASS`, `FAIL`, `BLOCKED`, or `NOT_TESTED`. A logical plan check never equals live-system verification.
5. Residual issue, next action, and whether the prior cycle's fix introduced regressions.

Make cycles cumulative: round N+1 uses the corrected result of N. Do not produce 10 copies of the same checklist or invent tool runs. When no additional material defect is found, record that finding and close early only if the owner did not explicitly require a fixed number of rounds.

## Severity and operating rules
- P0 = blocks correctness, privacy, source authority, core functionality or release gate; must be resolved before production.
- P1 = materially impairs usability, observability, supportability or acceptance quality.
- P2 = non-blocking optimization/expansion; defer when mission DoD is already met.
- Preserve original mission, current source-of-truth hierarchy, existing locks, approvals, and previous proven checkpoints.
- Never count a rewritten plan as a repaired deployment; never count untested code as a passed integration.
- If blocked, explore bounded safe substitutes and continue independent branches. Keep owner interruption minimal and specific.
- Never create new master trackers or rewrite protected source data simply to store a review.
- Never spend additional money or invoke metered tools contrary to owner cost constraints.
- High-impact writes, public release, sensitive-data access and destructive actions obey canonical approval gates.

## Required output
Provide a compact cycle ledger with round, dimension, defect, change executed/proposed, verification status, and residual risk; plus cumulative final corrected plan, P0 blockers, test matrix, explicit evidence/links, release decision, and exact next action. Keep past-work audit distinct from future-plan audit. For long work, a full ledger may live in the designated canonical Control Center while chat shows key findings.

## Persistence /save
When owner asks to record, persist the durable command contract and/or review checkpoint to the verified canonical destination and read back. Repository canonical changes must be read back from the exact branch and linked; PR-only state is PROPOSED, not ACTIVE. Do not claim successful deployment merely because this skill document exists.

## Invocation examples
- `/my /360` — review current work and iterate fixes.
- `/my /360 5` — five bounded review cycles.
- `/my /360 past 10 + future 10` — twenty cycles with separate retrospective/prospective ledgers.
- `/my /360 /save` — persist verified durable findings in the existing control plane.
