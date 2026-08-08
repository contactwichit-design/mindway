# Template Registry

Status: REVIEW_READY  
Version: 0.2.0

| ID | Family | Primary behavior | Typical outputs |
|---|---|---|---|
| T01 | Mission / Task | define work and completion | task brief, execution contract |
| T02 | Research / Discovery | discover and ground | research note, source map |
| T03 | Plan / Execution | sequence work | plan, roadmap, run board |
| T04 | Decision | choose with evidence | decision memo, recommendation |
| T05 | Status / Compact HUD | expose delta and next state | routine/status report |
| T06 | HOFF / Continuity | resume without rediscovery | handoff/checkpoint |
| T07 | QA / Review | verify quality/completion | QC report, acceptance gate |
| T08 | Data / Analysis | structure and interpret data | analysis, KPI, dashboard data |
| T09 | Communication | move a recipient to action | email, LINE, memo copy |
| T10 | Document | produce structured reading artifact | report, SOP, proposal, PDF/DOCX |
| T11 | Visual / Graphic | communicate visually | graphic, infographic, diagram |
| T12 | Presentation | narrative across frames/slides | deck, training presentation |
| T13 | Web / UI | interactive information/action surface | site, dashboard, app UI |
| T14 | Learning / LMS | teach and assess | module, lesson, quiz |
| T15 | Media Production | timed audiovisual communication | video, audio, motion |
| T16 | Automation / Agent | repeat/trigger work reliably | routine, workflow, agent |
| T17 | Blocker / Recovery | recover safe progress | blocker packet, fallback plan |
| T18 | Evolution / Maintenance | improve reusable capability | update proposal, regression note |

## Fast-load order
For token economy, read in this order:
1. `REGISTRY.md` — identify possible family.
2. `ROUTER.md` or `SYSTEM.json` — compose minimum set.
3. `FAMILIES.md` — read only selected family contracts.
4. relevant design/renderer profile only when needed.
5. `TESTS.md` only for maintenance/regression/promotion.

## Composition policy
Templates are composable. A task may use multiple families but should load only the minimum sufficient set. File format is a renderer/output choice, not a family.

## Override policy
Locked project or owner-system templates and source truth override generic family defaults for their scope. Design profiles may change expression but not facts, evidence, workflow semantics or approval gates.

## Lifecycle
`CANDIDATE → REVIEW_READY → APPROVED/LOCKED → DEPRECATED`

Current system: REVIEW_READY. Approval/locking remains an owner/governance decision.