# Code Quality Gate — Promotion Proposal

Date: 2026-08-26
Status: PROPOSAL / CANDIDATE
Scope: public Mindway code-quality capability

## Problem
AI-assisted code can be technically valid while still increasing maintenance cost. Tests, linting, type checks, and security scans do not by themselves detect all forms of unnecessary complexity, weak abstractions, generated commentary, defensive overgrowth, type escapes, deep nesting, or test slop.

Mindway already states that `TECH_VALID` is not `REVIEW_READY` and prefers evidence-first Maker -> Critic/Analyzer -> Repair -> Verify loops. This proposal adds a focused code-maintainability gate without changing those core rules.

## Proposed capability
Add a vendor-neutral `Code Quality Gate` between technical validation and independent review:

`WRITE -> LINT/TYPE/TEST/SECURITY -> CODE_QUALITY_GATE -> REPAIR -> REVERIFY -> INDEPENDENT REVIEW -> REVIEW_READY`

The gate uses four verdicts:

- `PASS`
- `PASS_WITH_DEBT`
- `REPAIR_REQUIRED`
- `BLOCKED_BY_INVARIANT`

It requires evidence-first findings rather than unexplained scalar scores.

## Included candidate artifacts

- `skills/code-quality-gate/SKILL.md` — policy and workflow contract.
- `skills/code-quality-gate/RULES.json` — vendor-neutral rule registry.
- `skills/code-quality-gate/CODEX_ADAPTER.md` — Codex-specific execution adapter.
- `runtime/code_quality_gate.py` — deterministic hint scanner for selected high-confidence patterns.
- `runtime/test_code_quality_gate.py` — regression tests for the reference scanner.
- `runtime/schemas/code_quality_report.schema.json` — normalized report contract for richer analyzers/adapters.

## Deliberate design choices

### Vendor-neutral core
Third-party anti-slop tools may be useful adapters or evidence sources, but their rule sets, repositories, availability, and security posture can change. Mindway should own the capability contract while external tools remain replaceable implementations.

### No score-only promotion
A numeric quality score can be gamed and may reward deletion of legitimate defensive behavior. Promotion therefore depends on evidenced findings, project checks, and invariants rather than a single score.

### Invariant protection
A cleanup suggestion must not override security, privacy, financial, clinical, data-integrity, compatibility, migration, or other explicit project requirements. Conflicting cleanup is classified as `BLOCKED_BY_INVARIANT` rather than auto-applied.

### Minimal repair
Prefer the smallest change that resolves an evidenced defect. Avoid broad rewrites that create additional review surface without necessity.

## Benefits

- closes part of the gap between `TECH_VALID` and maintainable code;
- provides a common review vocabulary across Codex/Cursor/other agents;
- reduces dependence on model-specific prompt quality;
- makes anti-slop findings inspectable and auditable;
- preserves stronger project/security/human gates.

## Costs and risks

- false positives, especially for contextual rules such as abstractions, naming, and comments;
- additional review/runtime cost on large diffs;
- deterministic heuristics can overflag generated or domain-specific patterns;
- teams may incorrectly treat `PASS` as final approval unless the promotion boundary stays explicit;
- adding too many rules could become another source of procedural slop.

## Promotion evidence required
Do not promote directly into canonical `/my` only because the candidate implementation exists.

Run at least one controlled repository trial and record:

1. baseline branch and target diff;
2. existing lint/type/test/security status;
3. gate findings and repairs;
4. false-positive count;
5. missed defects found by independent human/agent review;
6. behavior/regression result after repair;
7. diff-size impact;
8. human override decisions;
9. whether maintainability meaningfully improved without invariant loss.

Recommended initial success criteria:

- zero behavior regression caused by automatic repair;
- zero removal of protected invariants;
- all HIGH/BLOCKER findings include reproducible evidence;
- false positives are low enough that reviewers do not routinely ignore the gate;
- at least one independently verified maintainability defect is caught beyond baseline lint/type/test/security tooling.

## Promotion decision

Current recommendation: keep as `CANDIDATE` on a review branch. If controlled trial evidence passes, promote the skill as an optional code-work capability and add a lightweight canonical route/reference. If evidence is weak, repair the candidate or keep it as adapter stock without changing the public core.
