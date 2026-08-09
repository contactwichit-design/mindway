# Template System Integration Decision

Status: ACCEPTED_AND_INTEGRATED  
Version: 1.0.0  
Decision date: 2026-08-09

## Decision
The Template System is integrated into canonical `/my` as the core lightweight intent router for substantial reusable work.

## Owner authorization
The owner explicitly instructed a 1000-case simulation across broad work/product dimensions and set this acceptance rule: if the selected top-10 candidate patterns produced simulated productivity greater than 2.0× the prior ad-hoc baseline, promote the system into the core immediately.

Result: PASS. See `BENCHMARK_1000_SIMULATION.md`.

- overall simulated mean: 3.59× baseline;
- top-10 recipe mean: 3.64× baseline;
- minimum simulated case: 2.18×;
- 1000/1000 simulated cases exceeded 2.0×.

These are structural simulation/proxy results, not empirical wall-clock or token claims.

## Integrated canonical behavior
Canonical `/my` now:
1. checks Template Runtime for substantial work when reusable structure materially helps;
2. infers intent without making the user choose a template;
3. loads only the minimum sufficient template families;
4. keeps owner-system/locked project truth above generic templates;
5. treats file type as renderer/output rather than primary intent;
6. bypasses Template Runtime for simple self-contained work when it adds no value;
7. preserves all stronger source, safety, approval, verification and Graphic Runtime gates.

## Why the hook is lightweight
No T01–T18 family is preloaded globally. `/my` contains only the routing rule and link to `SKILL.md`; the selected family contracts are loaded on demand.

## Rollback
Remove the Template Runtime section from `/my` and mark `skills/template-system/SKILL.md` non-core. No source-data migration is required.

## Ongoing evidence
Continue measuring live work for wall-clock time, actual token/context usage, source errors, missed QA/gates and rework. Live evidence may refine the router but does not undo the explicit owner integration decision unless the owner changes it or a material safety/regression issue requires containment.