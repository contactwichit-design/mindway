# Template System Integration Proposal

Status: PROPOSE_TO_SAF  
Version: 0.2.0

## Proposal
After production benchmark evidence is sufficient, allow canonical `/my` to reference `skills/template-system/SKILL.md` as the default optional router for recurring substantial work where a reusable template materially reduces setup, rework or inconsistency.

## Why this is not auto-applied
Canonical `/my` is governance/core behavior. The current Template System is REVIEW_READY but not yet APPROVED/LOCKED. Core integration must not be self-approved by the implementing AI.

## Current evidence
- 18 reusable behavior families exist.
- fillable T01–T18 templates exist.
- machine-readable `SYSTEM.json` exists.
- deterministic router exists with 5 passing self-tests in equivalent runtime validation.
- 15 representative routing cases and 7 regression cases are defined.
- blocker-integrity and owner-source rules are preserved.
- visual/media routing preserves the mandatory code-first Graphic Runtime.

## Proposed canonical behavior
A future approved `/my` integration would add only this lightweight behavior:

1. For substantial work, check whether the request matches an existing Template System family/recipe.
2. Load only the minimum sufficient selected families.
3. Keep task/project owner-system templates higher priority than generic templates.
4. Do not force template loading for simple self-contained work.

No new command is proposed. No new routine round is proposed. No competing Mindway/master/registry is proposed.

## Benchmark before approval
Apply to at least 5 representative real tasks and compare against prior baseline:
- clarification/setup steps;
- source mistakes;
- missing QA/gates;
- rework count;
- time when measurable;
- token/context volume when measurable.

## Rollback
Because the system is an optional skill and `/my` is unchanged, rollback is simply to stop routing through the skill or mark it DEPRECATED. No source data migration is required.

## Decision requested later
`APPROVE_INTEGRATION | KEEP_OPTIONAL | REVISE | DEPRECATE`

Until then, the Template System remains usable as an optional REVIEW_READY skill without changing canonical governance.