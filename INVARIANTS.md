# Mindway Invariant Registry

Status: CORE
Purpose: compact registry of properties that must survive compatible Mindway evolution.

| ID | Invariant | Verification idea |
|---|---|---|
| INV-001 | `NO VERIFIED /my = NO SUBSTANTIAL EXECUTION` | Entry tests must reject substantial work before canonical verification. |
| INV-002 | One failed access route is not `MINDWAY_BLOCKED`. | Route-ladder tests must continue while a safe applicable route remains. |
| INV-003 | Never fabricate source access, tool execution, agents, verification, or completion. | Evidence-required assertions and negative tests. |
| INV-004 | A blocked branch does not automatically block the mission. | Blocker tests must attempt safe fallback, reversible work, alternative sources/tools, and independent workstreams. |
| INV-005 | Authority order is canonical Mindway → locked project governance/SSOT → task source → relevant skill/context. | Conflict tests must surface lower-layer conflicts rather than silently override. |
| INV-006 | Bootstrap is pre-entry transport/verification only; it cannot become a competing governance SSOT. | Architecture lint/review checks BOOTSTRAP scope. |
| INV-007 | Completion requires verification proportional to the claim. | Runtime must distinguish attempted, produced, verified, blocked, skipped, and not-done states. |
| INV-008 | Sensitive/private/company/patient/employee/credential information is protected; access is not authority. | Safety and disclosure tests. |
| INV-009 | Preserve the original mission through `ORIENT → PLAN/EXECUTE → VERIFY → RECORD → DECIDE`. | Mission-drift regression cases. |
| INV-010 | Real failures that reveal reusable failure classes should become regression cases after root-cause confirmation. | Regression ledger links failure → fix → test. |
| INV-011 | Lower layers may extend but may not silently override higher-layer invariants. | Architecture conflict tests. |
| INV-012 | Observability reports evidence of execution; it must never manufacture execution or causality. | Trace/event consistency checks. |

## Change policy

- Prefer adding a regression case over adding prose when an invariant already covers the failure.
- Add a new invariant only when the property is architecture-level, durable, and not adequately represented by an existing invariant.
- Changing or retiring an invariant is an architectural decision and requires explicit review plus compatibility analysis.
- Skills and projects should reference invariant IDs rather than copy large duplicate rule blocks when practical.
