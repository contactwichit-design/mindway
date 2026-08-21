---
name: add
description: Context-aware Advance continuation for Mindway. Use when the owner invokes /add alone or with /my, /loop, or another compatible command.
version: 0.1.0
status: EXPERIMENTAL
---

# /add — Context-Aware Advance

## Purpose

`/add` means **Advance from the real mission, not merely from the latest sentence**.

It extends the active Mindway execution opportunity by reconstructing relevant context, discovering missing requirements and next-best actions, and continuing safe useful work without waiting for the owner to enumerate every step.

`/add` does not create background execution and does not override `/my`, `/loop`, source, privacy, approval, or verification gates.

## Context reconstruction

Before advancing, inspect the minimum sufficient relevant context in this order:

`CURRENT REQUEST → RELEVANT RECENT CHAT / CHECKPOINT → CANONICAL /my → PROJECT / OWNER SSOT → PRIOR REQUIREMENTS / DECISIONS / LOCKS → ACTIVE ARTIFACT / EVIDENCE`

Do not reread unrelated history. Load only what can materially change the mission, constraints, definition of done, or next action.

## Advance loop

For the active mission:

1. Reconstruct the actual mission and preserve hard constraints.
2. Collect explicit requirements already stated by the owner.
3. Infer only evidence-supported implicit requirements needed for the mission to work in practice.
4. Detect missing pieces, contradictions, defects, risks, dependencies, and useful next actions.
5. Classify discoveries as `REQUIRED_NOW | SAFE_ADVANCE | NEED_USER | BACKLOG`.
6. Execute `REQUIRED_NOW` and `SAFE_ADVANCE` work immediately when reversible, authorized, and evidence-supported.
7. Verify the real output, not merely the completion of a tool call.
8. Repair verification failures when repairable.
9. Re-evaluate the mission and continue while meaningful safe work remains.

## Anti-premature-stop rule

After the owner has authorized execution with language equivalent to `ทำเลย`, `ทำต่อ`, `ให้จบ`, or by invoking `/add`, do **not** stop merely to report progress, announce the next step, or ask for another continuation message while meaningful independent work remains.

Before ending an active execution opportunity, ask internally:

- Is the requested outcome actually verified complete?
- Is there a safe next-best action I can execute now?
- Can I resolve the missing requirement from relevant chat, canonical `/my`, owner SSOT, or available evidence?
- Can another independent branch continue even if one branch is blocked?
- Am I about to say “next I will…” when I could perform that action now?

If a safe useful action remains, continue.

## Valid stop states

Stop only at one of these boundaries:

- `COMPLETE` — mission-level outcome is verified complete or no meaningful work remains.
- `NEED_USER` — an owner decision, approval, taste choice, inaccessible definition, or high-impact gate is genuinely required and cannot be resolved from authorized context.
- `BLOCKED` — safe fallback routes and independent workstreams are exhausted.
- `PLATFORM_LIMIT` — the active runtime cannot continue; leave a precise checkpoint and highest-value next action.
- `CYCLE_LIMIT` — `/loop N` budget is exhausted; checkpoint rather than pretending completion.

## Scope control

`/add` is not permission for uncontrolled scope expansion.

- Improvements necessary for the mission belong in `REQUIRED_NOW`.
- Reversible, low-risk improvements that materially increase usefulness may be `SAFE_ADVANCE`.
- Nice-to-have expansions that can distract from closure belong in `BACKLOG`.
- Publishing, deletion, rights transfer, sensitive-data exposure, irreversible actions, and high-impact decisions still require the applicable approval gate.

## Composition

Recommended forms:

- `/my /add <mission>` — context-aware advance.
- `/my /loop /add <mission>` — bounded continuous execution plus discovery/advance.
- `/add` — advance the current known mission after re-orienting to relevant context.

When combined with `/loop`, `/loop` controls execution state/cycle budget and `/add` controls context-aware discovery and next-best-action continuation.

## Completion report

Do not emit routine progress chatter during execution. At a real stop boundary, report concisely:

- state;
- verified completed work;
- unresolved gates/risks;
- checkpoint / exact next action when not complete.
