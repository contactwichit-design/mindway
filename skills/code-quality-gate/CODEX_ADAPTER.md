# Codex Adapter — Mindway Code Quality Gate

Status: CANDIDATE
Policy source: `skills/code-quality-gate/SKILL.md`

## Purpose
Give Codex a concrete execution contract without making Codex-specific behavior the canonical quality policy.

## Entry
Before using this adapter, load canonical `/my` and the Code Quality Gate skill. Project-local `AGENTS.md`, `SECURITY.md`, tests, type/lint rules, locked architecture decisions, and repository invariants remain authoritative within their scope.

## Codex workflow

1. Resolve the comparison baseline, normally the target branch such as `main`.
2. Read the diff first; do not scan unrelated repository areas unless evidence requires it.
3. Run the repository's existing lint, typecheck, tests, and security checks when available.
4. Run the deterministic reference scanner where useful:

```bash
python runtime/code_quality_gate.py --pretty <changed-paths...>
```

5. Review the diff contextually against all eight quality families in `SKILL.md`.
6. Produce findings using the evidence contract:

```text
OBSERVATION
EVIDENCE: path:line + relevant diff/context
RULE: CQG-...
DEFECT
SEVERITY: LOW | MEDIUM | HIGH | BLOCKER
REPAIR
CONFIDENCE: 0..1
```

7. Before changing code, classify each candidate as:
   - `SAFE_MECHANICAL`
   - `CONTEXT_DEPENDENT`
   - `PROTECTED_BY_INVARIANT`
   - `LIKELY_FALSE_POSITIVE`
8. Repair only evidenced defects. Prefer the smallest behavior-preserving diff.
9. Re-run impacted tests/static checks and the quality scan.
10. Report the final gate verdict. Never claim `REVIEW_READY` solely because this adapter returns `PASS`.

## Default Codex review prompt

```text
Use Mindway Code Quality Gate on this diff.

Priorities:
- Preserve behavior and repository invariants.
- Compare against the target branch rather than reviewing files in isolation.
- Detect unnecessary comments, unjustified type escapes, defensive overgrowth, deep nesting, needless abstractions, naming/style drift, duplication/complexity, and test slop.
- Do not remove security/privacy/data-integrity/compatibility checks merely to simplify code.
- Every finding must include path/line evidence, rule ID, severity, minimal repair, and confidence.
- Treat deterministic scanner output as hints, not truth.
- Apply minimal repairs for high-confidence defects, then re-run relevant tests/checks.
- A quality PASS is not REVIEW_READY; independent review and stronger project gates still apply.
```

## Stop conditions
Stop automatic repair and return `BLOCKED_BY_INVARIANT` when cleanup would conflict with an explicit security, privacy, business, financial, clinical, compatibility, migration, or data-integrity requirement.

Stop and request owner/project-gate review when a repair materially changes architecture, public API, persisted data, authorization behavior, destructive behavior, or other high-impact semantics.

## Expected handoff

```text
Target:
Baseline:
Changed paths:
Checks run:
Findings fixed:
Accepted debt:
Invariant conflicts:
Gate verdict:
Independent review still required: yes/no + reason
Evidence paths:
```
