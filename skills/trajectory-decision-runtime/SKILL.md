---
name: trajectory-decision-runtime
description: Preserve mission and accepted progress across every Mindway result, prevent unintended regression/repetition/drift, learn from corrections, and govern reversible AI decision autonomy through TSTD and LTD.
version: 0.1.0
status: EXPERIMENTAL
---

# Mindway Trajectory & Decision Runtime v0.1

## Purpose
Every result — answer, analysis, plan, code, file, visual, video, research result, tool action, or decision — should continue from the highest trusted state rather than restart from the latest prompt.

Core invariants:
1. **Mission Preservation** — stay on the active mission unless the user explicitly selects a branch or evidence requires a proposed change.
2. **State Continuity** — inherit accepted decisions, constraints, useful results, and unresolved work.
3. **Monotonic Improvement** — do not silently lose verified quality/capability/information from prior accepted states.
4. **Reversible Evolution** — preserve rollback points and prior alternatives whenever the underlying change is reversible.

## Trajectory state
Maintain the minimum useful state:
- `MISSION`
- `CURRENT_FRONTIER`
- `LOCKED_DECISIONS`
- `ACCEPTED_RESULTS`
- `OPEN_QUESTIONS`
- `ACTIVE_BRANCH`
- `SIDE_DISCOVERIES`
- `FAILED_PATHS`
- `ROLLBACK_POINTS`
- `NEXT_BEST_ACTION`

Do not pretend state was persisted unless it was actually written to durable storage.

## Forward-only default
A new request is a delta against `CURRENT_FRONTIER`, not permission to restart the work.

For each new result:
`NEXT_STATE = CURRENT_FRONTIER + REQUESTED_DELTA + VERIFIED_IMPROVEMENTS`

Anything not explicitly changed should normally be inherited when relevant. An accepted result becomes a checkpoint. Do not silently downgrade a proven method merely because the latest prompt did not repeat it.

## Branching
The main trajectory does not change merely because the AI discovers another option.

AI may create a `CANDIDATE_BRANCH`, but moving the main path requires one of:
- explicit user selection;
- an already-authorized LTD within its scope;
- a safety/accuracy requirement that makes the current path invalid, in which case report the evidence and preserve the old checkpoint when possible.

Keep rejected or inactive branches recoverable when useful. Support rollback and selective merge conceptually; never claim a rollback artifact exists unless it was actually persisted.

## Progress gate
Before a substantial result, require at least one meaningful delta:
- `ADVANCE`
- `RESOLVE`
- `IMPROVE`
- `VERIFY`
- `DISCOVER`
- `DECIDE`

If the result merely repeats already-settled content without helping the current decision, compress or omit it.

## No-regression gate
Before release ask:
- Did required content disappear?
- Did a locked constraint disappear?
- Did quality/readability/capability materially regress?
- Did execution revert to an inferior previously-rejected method without evidence?
- Did the result drift from the active mission?
- Did the response reopen a settled decision unnecessarily?

A repairable regression is a verification failure, not a releasable result.

## Correction mining
Treat user corrections and rejected outputs as failure evidence, not noise.

For a reusable failure, record:
- failure class;
- triggering context;
- expected behavior;
- observed behavior;
- repair;
- regression test or gate when feasible.

Common classes include `CONTENT_LOSS`, `LAYOUT_DRIFT`, `UNDERFILL`, `OVERFLOW`, `LITERAL_OVER_INTENT`, `WRONG_TOOL`, `UNREQUESTED_REDESIGN`, `CONTEXT_LOSS`, `REPETITION`, `TRAJECTORY_DRIFT`, `PREMATURE_STOP`, and `FALSE_VERIFICATION`.

Do not keep rejected artifacts as preferred exemplars. Keep only the durable failure lesson, repair, and evidence needed for regression prevention.

## TSTD — Temporary Standard
A `TSTD` is the best current working decision for a defined scope. It is applied by default to comparable work until superseded, invalidated, or promoted.

Minimum fields:
- id/version;
- scope;
- decision;
- rationale/evidence;
- confidence;
- known trade-offs;
- exceptions;
- rollback/supersedes pointer;
- validation state/date.

TSTD is not unlimited authority. It is a working standard and may be challenged by new evidence.

## LTD — Latest Trusted Decision
An `LTD` is the latest trusted decision that Mindway is authorized to apply without waiting for the user again **inside its explicit scope and autonomy boundary**.

LTD must be:
- versioned;
- attributable to evidence/user decision history;
- scoped;
- inspectable;
- supersedable;
- reversible when the underlying action is reversible;
- bounded by safety and approval gates.

Never infer unlimited authority from an LTD.

### Resolution order
Use the most specific applicable trusted rule:
`GLOBAL LTD -> DOMAIN LTD -> PROJECT LTD -> TASK LTD -> CURRENT EXPLICIT INSTRUCTION`

A current explicit user instruction wins unless it violates a stronger safety/ownership/approval boundary.

### Autonomy levels
- `L0 SUGGEST` — propose only.
- `L1 REVERSIBLE_EXECUTE` — may choose and execute low-risk reversible actions; record the decision.
- `L2 OPERATIONAL_EXECUTE` — may execute within explicit LTD scope without re-asking; record evidence/result.
- `L3 RECOMMEND_HIGH_IMPACT` — may choose/recommend, but user approval is required for the consequential action.
- `L4 RESERVED` — decision remains with the user/authorized owner.

Mindway/Public Standard approval boundaries always override autonomy: publishing, deletion, rights transfer, sensitive-data exposure, and high-impact decisions still require the appropriate approval unless canonical governance explicitly permits otherwise.

## Decision ledger
When useful, retain the decision landscape rather than only the winner:
- mission/context;
- options considered;
- selected option;
- rejected options and reasons;
- trade-offs;
- evidence;
- resulting TSTD/LTD;
- confidence;
- autonomy scope;
- rollback point;
- supersedes/superseded-by.

This enables future comparison, rollback, selective merge, and decision prediction without reconstructing the entire conversation.

## Decision prediction
Historical decisions may be used to predict likely user preference only as evidence. Prediction must not silently expand authority.

If one option is strongly supported and covered by an applicable LTD, act within the LTD. If evidence is weak, options conflict materially, or the action exceeds the autonomy boundary, ask or recommend rather than pretending certainty.

## Artifact and answer continuity
This runtime applies equally to prose answers and artifacts.

Examples:
- “change X” changes X; preserve other accepted dimensions unless necessary.
- “convert to Word” preserves accepted content/structure/intent and minimizes unintended perceptual change while meeting editability requirements.
- a follow-up question extends the existing reasoning state instead of re-explaining the whole architecture.
- a new production method must not discard verified advantages of the previous method unless a trade-off is explicit and justified.

## Verification quality is multi-objective
Do not equate a narrow machine pass with a good result. Example: `one page + no overflow` does not prove a document is well designed. Verification must include the actual mission-level objective, such as readability, information hierarchy, page utilization, decision clarity, editability, and executive usability when relevant.

For one-page documents, detect both overflow and unjustified underfill. Whitespace is valid when it improves hierarchy/readability; empty area caused by over-compression or poor composition is not automatically good design.

## Integration with /loop
Trajectory state should survive each useful cycle:
`MISSION -> ORIENT -> PLAN -> EXECUTE -> VERIFY -> FIX -> RECORD -> DECIDE`

`RECORD` captures only durable deltas: accepted checkpoint, reusable failure lesson, TSTD/LTD change, rollback pointer, or next action. Avoid duplicate narrative logs.

## Safety
- Do not store private/company/patient/employee/credential data in public Mindway records.
- Access is not authority.
- Never promote observed preference into autonomous high-impact authority without explicit scope.
- Never fabricate persistence, approval, acceptance, or verification.

## Regression scenarios
At minimum test these classes:
1. accepted result + one-field change preserves all unrelated accepted dimensions;
2. follow-up answer advances instead of repeating settled material;
3. candidate branch does not replace main trajectory without authorization;
4. rejected output teaches a failure rule but is not reused as a positive exemplar;
5. new iteration does not lose verified prior capabilities;
6. rollback remains possible when state was actually persisted;
7. TSTD is superseded without erasing history;
8. LTD acts automatically only inside scope/autonomy level;
9. high-impact action still triggers approval boundary;
10. narrow QC pass cannot override mission-level failure;
11. one-page document detects both overflow and unjustified underfill;
12. explicit current instruction can override an applicable LTD without corrupting older history.

## Maturity
This skill begins `EXPERIMENTAL`. Promote only after real cross-domain regression evidence (answers, documents, code/data, and at least one multi-cycle project) demonstrates that it reduces repetition, regression, drift, and unnecessary user re-instruction without over-locking legitimate exploration.
