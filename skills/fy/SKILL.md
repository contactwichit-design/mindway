---
name: fy
description: Backward-compatible planning alias for canonical /loop plan. Use when the user invokes /fy or when an older Mindway workflow still references /fy during migration.
version: 3.0.0
status: COMPATIBILITY
---

# /fy — compatibility alias for `/loop plan`

## Purpose

`/fy` remains valid for backward compatibility, but it no longer maintains an independent execution-planning protocol.

Canonical semantics:

`/fy` → `/loop plan`

The source of truth for planning, cycle budgeting, topology, checkpoint behavior, repair, and verification is:

- `my.md` — canonical command mapping;
- `skills/loop/SKILL.md` — current execution runtime.

## Invocation behavior

- `/fy <task>` means `/loop plan <task>` and is planning-only.
- `/fy` without an explicit task may use the current mission when it is already clear; otherwise request only the minimum missing task context.
- `/fy` must not silently execute work. Execution requires `/loop`, `/loop N`, a compatible legacy execution alias, or an explicit user instruction to start execution.
- Entry still requires verified canonical `/my` according to `MW-BOOT/1` and the Entry Access Gate before substantial work.

## Compatibility rules

1. Do not maintain a second scoring system that can drift from `/loop`.
2. Do not present legacy `/myN` recommendations as the canonical planner output. If a legacy surface requires them, map them explicitly to `/loop N` and label them compatibility output.
3. Do not reinterpret `/fy` as a separate runtime, autonomous worker launcher, or background process.
4. Preserve old user habits while routing behavior to the current canonical planner.
5. If `my.md` and this file ever disagree, `my.md` is authoritative and the mismatch is a regression defect.

## Legacy note

Historical `/fy` versions contained their own complexity rubric, worker-count logic, and `/myN` recommendation format. Those semantics are retained in Git history for provenance but are deprecated for active execution because maintaining two planners creates command drift.
