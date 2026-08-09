# Mindway Architecture Constitution

Status: CORE ARCHITECTURE
Purpose: preserve system shape while Mindway evolves.

## Layer model

`AI / HUMAN → MW-BOOT/1 → /my → GOVERNANCE → /loop → SKILLS + RUNTIME → PROJECT/TASK → VERIFY → RECORD`

### Responsibilities

- `BOOTSTRAP.md` — pre-entry transport discovery and canonical verification only.
- `my.md` — canonical operating entry and governance router.
- `PUBLIC_STANDARD.md` — public foundation and safety/behavior standard.
- `/loop` — execution control: plan, execute, verify, repair, checkpoint, decide.
- `skills/` — specialized reusable capabilities. Skills may extend execution but may not redefine higher-layer governance.
- `runtime/` — deterministic machinery, schemas, runners, and tests.
- project/task layer — scoped rules and source-of-truth for a mission; may extend but not override canonical governance.
- observability/record — evidence of what actually happened; never a source for invented execution.

## Dependency direction

Preferred direction:

`BOOTSTRAP → /my → GOVERNANCE → RUNTIME/SKILLS → PROJECT/TASK`

Lower layers may reference higher-layer contracts for compliance, but must not silently override them. Avoid circular authority. If a project rule conflicts with canonical Mindway, canonical Mindway wins and the conflict must be surfaced.

## Architectural invariants

The authoritative invariant list is [INVARIANTS.md](INVARIANTS.md). Architecture changes must preserve active invariants or explicitly propose an invariant revision for review.

## Evolution rule

Prefer extension over replacement, compatibility over breakage, and evidence-driven changes over speculative complexity. New layers require a distinct responsibility that cannot be safely expressed by an existing layer.

`BOOTSTRAP.md` must remain small. It must not accumulate project rules, business logic, execution planning, or domain knowledge.

## Change gate

Before a structural change is considered complete:

1. identify affected layers;
2. check invariant impact;
3. run regression/self-test where available;
4. preserve compatibility or document migration;
5. verify canonical entry still works;
6. record unresolved risk honestly.
