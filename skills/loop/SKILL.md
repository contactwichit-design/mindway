---
name: loop
description: Unified Mindway execution command combining planning, bounded continuation, recursive improvement, repair propagation, verification, checkpoint/resume, and optional parallel topology.
version: 0.2.0
status: EXPERIMENTAL
---

# /loop — Unified Mindway Execution Runtime v0.2

## Purpose
`/loop` is Mindway's bounded execution controller. It is a durable execution protocol, not a promise of background work.

## Invocation
- `/loop` — infer the minimum useful cycle budget and execute immediately.
- `/loop N` — execute up to N useful cycles, N=1..99.
- `/loop plan` — planning only.
- `/loop resume <run_id>` — resume a persisted compatible checkpoint when accessible.
- `/fy` -> `/loop plan`; `/myN` -> `/loop N` during compatibility migration.

## Runtime graph
`MISSION -> ORIENT -> PLAN -> EXECUTE -> VERIFY -> [FIX/RIL -> VERIFY]* -> RECORD -> DECIDE -> COMPLETE|CHECKPOINT|STOP`

A cycle is meaningful progress, not a tool call or chat message. Preserve the original mission and hard constraints across every cycle.

## Planner and topology
Choose the minimum useful topology: `SEQUENTIAL`, `PARALLEL` when real concurrency exists, or `HYBRID`. Never claim parallel workers ran unless they actually ran.

## State machine
Run states: `NEW -> ORIENTING -> PLANNED -> RUNNING -> VERIFYING -> FIXING -> CHECKPOINTED -> RUNNING -> COMPLETE`.
Exceptional states: `NEED_USER | BLOCKED | PLATFORM_LIMIT | CYCLE_LIMIT | FAILED`.

## Durable run ledger
Use `runtime/schemas/mindway_run.schema.json` where supported. Preserve stable run_id/mission, cycle budget/progress, current state, exact next action, completed outputs with evidence, risks/approval gates, source/version references, checkpoint pointer when persisted, explicit stop reason, and consequential open failure debt. Never claim persistence unless actually written.

## Retry, repair, and Recursive Improvement Loop
Retry only when plausibly transient or repairable. Prefer targeted repair over restart, preserve successful independent work, use bounded retries, and change strategy when repeated failure evidence demands it.

When a failure is reusable or indicates a systemic defect, invoke the Trajectory & Decision Runtime Recursive Improvement Loop (RIL):

`DETECT -> DIAGNOSE -> PATCH -> VERIFY_ORIGINAL -> GENERALIZE -> FIND_ANALOGS -> PROPAGATE_PREVENTION -> IMPACT_CHECK -> REGRESSION -> SYSTEM_RECHECK -> CLOSE|REOPEN`

Rules:
1. `RECORD != RESOLVE`; documentation alone cannot close a failure.
2. Repair the immediate result when useful, but patch the reusable producing mechanism when safely possible.
3. Generalize the failure principle, not a domain-specific patch blindly.
4. Search reasonable analogous surfaces and propagate prevention within evidence-supported scope.
5. Analyze fix radius, risk radius, and test radius.
6. A consequential side effect becomes a child failure and re-enters RIL.
7. Keep unrelated safe work moving; a scoped repair branch does not automatically block the mission.
8. Do not let system-improvement work displace a still-feasible requested deliverable.
9. Keep unresolved reusable failures visible as failure debt with reason/scope/next action.
10. Stop recursion when bounded closure is satisfied and no meaningful evidence-supported improvement remains.

Truthful failure states include `DETECTED`, `DIAGNOSED`, `PATCHED_NOT_VERIFIED`, `TESTED`, `VERIFIED`, `CLOSED`, `DEFERRED`, `BLOCKED`, and `REOPENED`. Never call an instance repair a system fix without system evidence.

## Idempotency
Before repeating an external side effect, determine whether it already succeeded. Use stable operation IDs/checksums where supported. Never duplicate publish/send/create/write actions merely because a response was lost.

## Checkpoint/resume
Checkpoint when platform boundary, cycle limit, or external dependency interrupts unfinished work. A checkpoint must let a compatible Mindway runtime continue without reconstructing the conversation. Resume by re-entering canonical `/my`, validating compatibility/integrity, then continuing from the highest-value unfinished safe action.

## Approval interrupts
For publish/delete/rights transfer/data exposure/high-impact decisions, enter `NEED_USER` only for the gated action. Continue unrelated safe work when possible. Restore prior task context after approval interruption.

## Hard-blocker test
Before stopping as `BLOCKED`, test safe fallback, reversible/read-only continuation, alternative source/tool, and independent workstreams. If any useful safe route remains, do not stop the whole mission.

## Verification
Maker output is not automatically verified. Verify against source, constraints, tests, expected output, mission-level quality, and compatibility. A repairable verification failure returns to `FIXING/RIL` rather than being reported complete.

A narrow technical pass cannot override mission failure. Verification should check the actual objective, not merely easy-to-measure proxies.

## Recursive completion
A run is `COMPLETE` only when the requested outcome is verified complete or no further meaningful work is required. A consequential unresolved child failure relevant to the requested outcome prevents false parent completion unless explicitly and validly deferred.

For a reusable failure, closure requires: root cause repaired/contained; original case verified; reasonable analogous scope checked; regression/prevention added where feasible; no known consequential patch side effect unresolved; original mission still passes; and further recursion has no meaningful evidence-supported value.

Future evidence may reopen a closed failure.

## Observability
Emit minimal redacted events for task/routing/work/tool/QC/fix/RIL propagation/impact/regression/checkpoint/resume/improvement/completion when the runtime supports events. Observatory views must not invent causality.

## Completion report
Report completed work plus any `BLOCKED`, `STOPPED`, `SKIPPED`, `NOT_DONE`, `DEFERRED_FAILURE_DEBT`, or `PATCHED_NOT_VERIFIED` branch with evidence and exact next action. Never hide unresolved work to make a run appear complete.