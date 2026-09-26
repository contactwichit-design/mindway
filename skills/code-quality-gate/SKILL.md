---
name: code-quality-gate
description: Evidence-first anti-slop and maintainability gate for AI-assisted code changes before REVIEW_READY promotion.
version: 0.1.0
status: CANDIDATE
owner_approval: pending
---

# Mindway Code Quality Gate

## Mission
Prevent technically valid AI-generated code from being promoted merely because it runs, parses, lints, or passes tests. Detect maintainability defects, unnecessary complexity, unsafe type escapes, defensive overgrowth, weak tests, and other forms of code slop while preserving required behavior and project invariants.

This skill is additive. It does not modify canonical `/my`, replace project-specific standards, or grant final approval authority.

## Core invariant

`TECH_VALID != REVIEW_READY`

Recommended route:

`AI WRITE -> LINT/TYPECHECK -> TEST -> SECURITY CHECK -> CODE_QUALITY_GATE -> REPAIR -> RE-TEST -> RESCAN -> INDEPENDENT REVIEW -> REVIEW_READY`

A passing anti-slop scan is supporting evidence only. It MUST NOT override security requirements, business rules, compatibility locks, project invariants, or human approval gates.

## When to use
Use this gate when one or more of these are true:

- AI or agent generated or heavily modified code;
- a substantial diff is being prepared for review;
- tests pass but maintainability is uncertain;
- refactoring may accidentally change behavior;
- generated code contains broad exception handling, `any`/type escapes, deep nesting, duplicated logic, unnecessary abstractions, noisy comments, weak naming, or brittle tests;
- the project requires a stronger promotion check between `TECH_VALID` and `REVIEW_READY`.

Skip or reduce this gate for tiny, obvious, low-risk changes when it would add no meaningful signal.

## Evidence contract
Every reported defect should follow:

`OBSERVATION -> EVIDENCE -> RULE -> DEFECT -> SEVERITY -> REPAIR -> CONFIDENCE`

Do not return unexplained scalar quality scores as the sole basis for a decision.

## Verdicts

- `PASS` — no material code-quality defects found under the active rules.
- `PASS_WITH_DEBT` — code may proceed to independent review, but explicit low-risk debt remains.
- `REPAIR_REQUIRED` — material maintainability or test-quality defects should be repaired before promotion.
- `BLOCKED_BY_INVARIANT` — a proposed cleanup conflicts with a required project/security/compatibility invariant; do not auto-remove the protected behavior.

## Required checks
At minimum inspect these eight families when applicable:

1. `COMMENTS` — redundant narration, stale commentary, generated filler, comments that repeat syntax instead of explaining intent.
2. `TYPE_ESCAPES` — unjustified `any`, broad casts, ignored type errors, or equivalent escape hatches.
3. `DEFENSIVE_OVERGROWTH` — speculative guards, broad `try/except` or `try/catch`, swallowed errors, impossible-state handling without evidence.
4. `NESTING_CONTROL_FLOW` — deep nesting, avoidable `else`, missing early returns, condition pyramids.
5. `ABSTRACTION` — helper/class/factory/wrapper layers that do not reduce real complexity or duplication.
6. `NAMING_STYLE` — generic AI-style names, inconsistent domain vocabulary, misleading names, style drift from the local codebase.
7. `DUPLICATION_COMPLEXITY` — repeated logic, copy-paste branches, unnecessary branching, dead code, avoidable indirection.
8. `TEST_SLOP` — tests that only mirror implementation, over-mock internals, assert weakly, hide failures, or fail to prove important behavior.

## Safety rules

1. Preserve observable behavior unless the task explicitly authorizes behavior change.
2. Prefer the smallest repair that closes the evidenced defect.
3. Never remove a defensive check only because it looks redundant when it protects a documented security, privacy, financial, clinical, data-integrity, compatibility, or operational invariant.
4. Never replace tests with weaker assertions to make a cleanup pass.
5. Run relevant tests after every material repair.
6. Compare against the project baseline/main branch when available; inspect the diff, not just isolated files.
7. The maker should not be the sole final verifier when independent review is available.
8. Vendor-specific tools are adapters, not the policy source of truth.

## Scan -> plan -> execute -> rescan

### 1. Scan
Collect candidate findings with file/line evidence, rule IDs, and confidence.

### 2. Plan
Group findings into:
- safe mechanical repair;
- context-dependent repair;
- protected by invariant;
- likely false positive.

### 3. Execute
Apply the smallest behavior-preserving changes first. Avoid broad rewrites unless the evidence supports them.

### 4. Rescan
Re-run deterministic checks, tests, and relevant static analysis. Confirm that repairs did not introduce new defects.

## Promotion rule
A code change may move from `TECH_VALID` toward `REVIEW_READY` only when:

- required tests/type/lint/security checks pass or their exceptions are explicitly documented;
- material `REPAIR_REQUIRED` findings are closed or explicitly accepted by the owner/project gate;
- protected invariants remain intact;
- the final quality decision contains evidence, not only a score;
- independent review occurs when materially useful and available.

## Machine-readable contracts

- Rules: `RULES.json`
- Report schema: `../../runtime/schemas/code_quality_report.schema.json`
- Reference runtime: `../../runtime/code_quality_gate.py`
- Codex adapter: `CODEX_ADAPTER.md`
- Regression tests: `../../runtime/test_code_quality_gate.py`

## Status
`CANDIDATE` until reviewed against real repositories and false-positive/false-negative evidence is collected. Do not silently promote this skill into canonical `/my` during implementation.