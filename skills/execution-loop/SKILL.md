---
name: execution-loop
description: Continue substantial Mindway work through bounded internal execution cycles using /myN, with re-orientation, progress state, QC, stop conditions, and resumable handoff. Use when the user invokes /my followed by an integer from 1 to 99 or asks for long-running autonomous-style continuation within a chat response.
version: 1.0.0
status: REVIEW_READY
---

# Mindway Execution Loop v1

## Purpose

Prevent premature stopping on substantial work by converting one user instruction into a bounded sequence of deliberate execution cycles.

`/myN` means: perform up to N useful Mindway execution cycles for the current task before declaring the run complete, subject to hard platform, safety, approval, and tool limits.

Examples:

- `/my1` = one execution cycle.
- `/my10` = up to ten execution cycles.
- `/my99` = up to ninety-nine execution cycles, but never meaningless repetition.

This protocol does NOT claim that an AI can send a new chat message to itself after its final response. Without an external orchestrator or new trigger, ordinary chat cannot autonomously create a new assistant turn after the turn has ended. Therefore `/myN` is implemented as internal continuation cycles within the active execution opportunity, plus resumable state when a platform boundary is reached.

## Core invariant

Before ending a `/myN` run, the agent must know:

1. requested cycle budget N;
2. completed useful cycles;
3. current task state;
4. whether the task is actually complete;
5. why execution is stopping;
6. the exact next action if continuation remains.

The agent must not stop merely because one subtask or one tool call finished.

## Cycle definition

One cycle is a meaningful unit of progress, not one chat message and not one tool call.

Each cycle follows:

`ORIENT -> EXECUTE -> VERIFY -> RECORD -> DECIDE`

### ORIENT

At cycle start:

- Re-read the canonical `/my` entry when access is available and when re-reading is materially useful.
- Preserve the original user mission and hard constraints.
- Read only minimum task-relevant context.
- Load the latest runtime state from the current run ledger when available.
- Identify the highest-value unfinished next action.

Do not perform wasteful repeated external reads when the canonical source is unchanged and an already-verified content hash/version is available. Revalidation may use version/hash/modified state when supported.

### EXECUTE

Perform the next meaningful block of work. Prefer completing a coherent dependency over generating commentary.

### VERIFY

Check the produced result against source, constraints, expected outputs, and task-specific QC.

### RECORD

Update the run ledger with evidence of progress, unresolved issues, outputs, and next action.

### DECIDE

Continue another cycle when:

- useful work remains;
- the next action is executable now;
- another cycle is likely to increase task completion or quality;
- cycle budget remains.

Stop only under an explicit stop condition.

## Stop conditions

A `/myN` run stops when the first applicable condition is true:

### COMPLETE

The requested outcome is complete and verified. Do not waste remaining cycles merely to consume N.

### CYCLE_LIMIT

N useful cycles have been completed and unfinished work remains.

### PLATFORM_LIMIT

The active environment cannot continue because of context/token/tool/runtime/output constraints.

### NEED_USER

A genuinely non-resolvable decision, missing source, required approval, credential, legal/business/clinical approval gate, or destructive-action confirmation is required.

### BLOCKED

A dependency or tool is unavailable and no safe alternative route exists.

### DIMINISHING_RETURN

The next cycle would only repeat prior work, cosmetically rewrite output, or add negligible value without new evidence.

Safety and higher-level system constraints always override requested cycle count.

## Run ledger

Maintain a compact run state during execution. Suggested schema:

```json
{
  "runtime": "mindway-execution-loop-v1",
  "task_id": "stable-or-local-id",
  "requested_cycles": 10,
  "completed_cycles": 4,
  "status": "IN_PROGRESS",
  "mission": "...",
  "completed": ["..."],
  "current_state": "...",
  "next_action": "...",
  "risks": ["..."],
  "source_versions": {},
  "artifacts": [],
  "stop_reason": null
}
```

A run ledger may live only in active context for lightweight work. Persist it to an owner-approved shared system only when persistence is useful and authorized.

Do not invent persistence. If no persistent storage was actually written, say so.

## Continuation checkpoint

When a platform boundary forces a stop before completion, produce a compact checkpoint containing:

- original mission;
- cycle budget and cycles completed;
- verified completed work;
- current working state;
- exact next action;
- unresolved risks/approval gates;
- artifact/source identifiers needed to resume.

The checkpoint must be sufficient for another compatible Mindway agent to resume without reconstructing the whole conversation.

## Progress behavior

For long runs, provide occasional concise user-visible progress updates when the environment supports them. Do not count progress messages as cycles.

## Anti-loop safeguards

Never:

- repeat the same analysis solely to consume cycle budget;
- re-read unchanged sources unnecessarily when a verified version/hash is available;
- create artifacts solely to prove activity;
- lower QC to reach N;
- bypass approval/safety gates;
- claim a new autonomous chat turn occurred when it did not;
- claim background continuation unless an actual scheduler/orchestrator was created and supports it.

## Relationship to other runtimes

Execution Loop controls continuation. It does not replace task-specific runtimes.

Examples:

`/my10 + graphic task` -> Execution Loop + Graphic Runtime

`/my20 + narration task` -> Execution Loop + Audio Runtime

Each task runtime supplies its own production/QC rules; Execution Loop determines whether another useful cycle should occur.

## Completion report

At the end of a run report at minimum:

```text
/myN
Cycles: X/N
Status: COMPLETE | CYCLE_LIMIT | PLATFORM_LIMIT | NEED_USER | BLOCKED
Completed: ...
Remaining: ...
Next: ...
```

If COMPLETE occurs before N, explicitly say the remaining cycles were unnecessary rather than pretending they were executed.
