# Template System Benchmark

Status: REVIEW_READY  
Version: 0.2.0

## Scope
This benchmark measures structural routing efficiency and safety coverage. It does not claim unmeasured wall-clock or token savings.

## Baseline
Naive universal-template loading would expose all 18 families to every substantial task.

## Router result
Across the 14 default recipes in `SYSTEM.json`:
- minimum selected families: 3;
- maximum selected families: 6;
- average selected families: 4.14;
- average family-load reduction vs loading all 18: approximately 76.98%.

This is a structural context-load reduction, not a claim that total model token usage falls by the same percentage.

## Representative cases

| Scenario | Families selected | Count | Avoided vs 18 | Key safety retained |
|---|---|---:|---:|---|
| Approval memo | T01,T07,T09,T10 | 4 | 77.8% | source/QA/send approval |
| Routine status | T01,T05,T07,T17 | 4 | 77.8% | blocker integrity/no-change noise |
| Data dashboard | T01,T04,T07,T08,T13 | 5 | 72.2% | validation/decision/UI QA |
| LMS lesson/video | T01,T06,T07,T11,T14,T15 | 6 | 66.7% | source/media/render/QA/handoff |
| Automation | T01,T05,T07,T16,T17 | 5 | 72.2% | trigger/state/retry/blocker QA |

## Deterministic router validation
`runtime/template_router.py` self-test logic was validated against five routing assertions:
1. approval memo recipe;
2. LMS lesson recipe;
3. automation recipe;
4. data + recommend + dashboard + QA tags;
5. blocked + research tags.

Result: 5/5 PASS in equivalent runtime validation.

## Regression coverage
`TESTS.md` contains 15 representative routing cases and 7 explicit regression cases covering:
- file-extension trap;
- template proliferation;
- weak blocker handling;
- final approval boundaries;
- visual/source truth conflict;
- corporate/project design override;
- no-change noise.

## What is proven
- The router can represent a broad task set with 3–6 families instead of loading all 18.
- The system preserves QA and blocker contracts in representative compositions.
- Reusable behavior families reduce the need for one-off template proliferation structurally.

## What remains unproven
- exact wall-clock reduction;
- exact token reduction;
- rework reduction across repeated live production;
- user satisfaction improvement over several production cycles.

These require production observation rather than synthetic claims.

## Decision
The system has sufficient structural evidence for `REVIEW_READY`, but not enough live-run evidence for `APPROVED/LOCKED` without owner decision.