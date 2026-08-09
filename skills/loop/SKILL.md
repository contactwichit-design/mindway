---
name: loop
description: Unified Mindway execution command combining planning, bounded continuation, repair, verification, checkpoint/resume, and optional parallel topology. Use when the user invokes /loop, /fy, /myN, or asks Mindway to continue substantial work until verified completion within platform limits.
version: 0.1.0
status: EXPERIMENTAL
---

# /loop — Unified Mindway Execution Runtime v0.1

## Purpose

`/loop` unifies the intent previously split across `/fy`, `/myN`, and private continuation variants while preserving backward compatibility.

It is a durable execution protocol, not a promise of background work. Ordinary chat cannot create a new post-final turn without a real orchestrator.

## Invocation

- `/loop` — plan an appropriate useful-cycle budget and execute immediately.
- `/loop N` — execute up to N useful cycles, N=1..99.
- `/loop plan` — planning only; compatibility behavior for `/fy`.
- `/loop resume <run_id>` — resume a persisted checkpoint when the runtime can access it.

Compatibility:

- `/fy` -> `/loop plan`
- `/myN` -> `/loop N`
- legacy/private continuation aliases may map to `/loop` only when their semantics are known; never invent compatibility.

## Runtime graph

`MISSION -> ORIENT -> PLAN -> EXECUTE -> VERIFY -> [FIX -> VERIFY]* -> RECORD -> DECIDE -> COMPLETE|CHECKPOINT|STOP`

A cycle is meaningful progress, not a tool call or message.

## Planner

When N is absent, score Scope, Discovery, Execution depth, QC/Risk, and Iteration uncertainty using the existing `/fy` rubric. Choose the minimum useful topology:

- SEQUENTIAL
- PARALLEL when actual concurrent workers are supported
- HYBRID for fan-out plus synthesis/critique/repair/independent verification

Never claim parallel workers ran unless they actually ran.

## State machine

Run states:

`NEW -> ORIENTING -> PLANNED -> RUNNING -> VERIFYING -> FIXING -> CHECKPOINTED -> RUNNING -> COMPLETE`

Terminal exceptional states:

`NEED_USER | BLOCKED | PLATFORM_LIMIT | CYCLE_LIMIT | FAILED`

Every transition emits an event conforming to `runtime/schemas/mindway_event.schema.json`.

## Durable run ledger

Use `runtime/schemas/mindway_run.schema.json`. Minimum invariants:

- stable run_id and mission;
- requested/estimated cycle budget;
- completed useful cycles;
- current state and exact next action;
- completed outputs with evidence;
- risks and approval gates;
- source/version references when useful;
- checkpoint pointer when persisted;
- explicit stop reason.

Do not claim persistence unless storage was actually written.

## Retry and repair

Retry only when the failure is plausibly transient or repairable.

- Prefer targeted repair over restarting the whole run.
- Preserve successful independent work.
- Use bounded retry counts.
- Change strategy when the same failure repeats.
- Record failure class, attempt, evidence, repair and verification result.

## Idempotency

Before repeating a side effect, determine whether it already succeeded. Use stable operation IDs/checksums where supported. Never duplicate publish/send/create/write actions merely because a response was lost.

## Checkpoint/resume

Checkpoint when a platform boundary, cycle limit, or external dependency interrupts unfinished work. A checkpoint must contain enough state for another compatible Mindway agent/runtime to continue without reconstructing the whole conversation.

Resume must re-orient against canonical `/my`, verify the checkpoint is compatible/current, then continue from the highest-value unfinished safe action.

## Approval interrupts

For publish/delete/rights transfer/data exposure/high-impact decisions, enter `NEED_USER` only for the gated action. Continue unrelated safe work when possible. On return, restore the prior task context and least-destructive default.

## Hard-blocker test

Before stopping as BLOCKED, test whether the blocker is real:

1. Can a safe fallback solve it?
2. Can reversible/read-only work continue?
3. Is an alternative source/tool available?
4. Can independent workstreams continue?

If yes, do not stop the whole mission. Record the blocked branch and continue safe work.

## Verification

Maker output is not automatically verified. Prefer independent verification when available. Verify against source, constraints, tests, expected output and compatibility. A repairable verification failure returns to FIXING rather than being reported as complete.

## Observability

Emit events for task creation/routing/work/tool/QC/fix/checkpoint/resume/improvement/completion. Keep payloads minimal and redact sensitive data. Observatory views are derived from these events and must not invent causality.

## Completion

A run is COMPLETE only when the requested outcome is verified complete or no further meaningful work is required. Report BLOCKED/STOPPED/SKIPPED/NOT_DONE branches explicitly with evidence and next action.
