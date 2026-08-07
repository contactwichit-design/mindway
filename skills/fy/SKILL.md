---
name: fy
description: Estimate the useful /myN execution-cycle budget for a task before starting it. Use when the user invokes /fy, asks how many Mindway cycles a task likely needs, or when choosing a bounded continuation budget would reduce premature stopping or waste.
version: 1.0.0
status: REVIEW_READY
---

# /fy — Mindway Cycle Estimator v1

## Purpose

Estimate an appropriate `/myN` budget for the current task.

`/fy` does not measure wall-clock time, tokens, or guarantee completion. It estimates how many meaningful Execution Loop cycles are likely to be useful before completion or a natural decision gate.

## Output

Return:

```text
/fy
Recommended: /myN
Range: /myA-/myB
Confidence: LOW | MEDIUM | HIGH
Why: concise explanation
Expected phases: ...
Stop gates: ...
```

Prefer one recommended integer N from 1-99.

## Estimation model

Estimate from five dimensions. Score each 0-4.

### 1. Scope (S)

0 = trivial single action
1 = small self-contained task
2 = several dependent subtasks
3 = multi-artifact or multi-system work
4 = broad project/workstream

### 2. Source/Discovery load (D)

0 = all facts supplied
1 = one source/read
2 = several files/sources
3 = cross-system discovery/reconciliation
4 = uncertain, large, or changing source landscape

### 3. Execution depth (E)

0 = answer only
1 = one production action
2 = build + revise
3 = multiple production stages
4 = architecture/implementation/migration with dependencies

### 4. QC/Risk (Q)

0 = low-risk, easy visual check
1 = normal verification
2 = strict QC or factual reconciliation
3 = business/brand/data-sensitive or release-adjacent
4 = legal/clinical/destructive/high-impact approval-heavy work

### 5. Iteration uncertainty (I)

0 = deterministic path
1 = known workflow
2 = likely fixes after first pass
3 = experiments/comparisons likely
4 = research/prototyping with unknown failure modes

Base score:

`T = S + D + E + Q + I`

Recommended cycle mapping:

- T 0-2 -> `/my1`
- T 3-5 -> `/my2`
- T 6-8 -> `/my3`
- T 9-11 -> `/my5`
- T 12-14 -> `/my8`
- T 15-17 -> `/my12`
- T 18-20 -> `/my20`

Then apply modifiers.

## Modifiers

Increase recommendation when:

- multiple external systems must be read/written: +2 to +8 cycles;
- batch artifacts or many records: +2 to +15;
- strict regression/QC suite is required: +2 to +6;
- exploratory alternatives must be tested, not merely proposed: +2 to +8;
- a durable reusable system/skill is being created: +2 to +6.

Reduce recommendation when:

- a clear template/runtime already exists: -1 to -5;
- most work is cacheable/incremental: -1 to -5;
- user asks only for review/diagnosis, not implementation: -1 to -4.

Clamp final result to 1-99.

## Interpretation

N is a maximum useful cycle budget, not an obligation to consume every cycle.

A task may finish early when verified COMPLETE.

A high N does not override safety, approval, platform, or tool boundaries.

## Examples

### Simple rewrite

Likely `/my1`.

### Review one spreadsheet and fix a few formulas

Likely `/my3` to `/my5` depending on source quality and QC.

### Build a reusable production runtime, test it on real artifacts, review failures, and update protocol

Likely `/my10` to `/my20`.

### Large cross-system migration with discovery, implementation, regression testing, and cleanup

Potentially `/my20` to `/my50`, but split into milestones if independent approval gates exist.

## Automatic recommendation

When `/fy` is invoked alone immediately before a task, inspect the task and recommend `/myN`.

When the user invokes `/fy` without a task to estimate, explain that `/fy` needs the intended task description.

Do not silently turn `/fy` into execution unless the user also requested the work to start.
