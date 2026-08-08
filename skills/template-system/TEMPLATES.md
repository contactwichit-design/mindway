# Mindway Fillable Templates T01–T18

Status: REVIEW_READY  
Version: 0.2.0

Use only selected sections. Remove empty optional fields instead of filling with noise.

## T01 — Mission / Task
```yaml
mission: 
scope_in: []
scope_out: []
owner: 
priority: 
inputs: []
constraints: []
definition_of_done: []
expected_output: 
next_action: 
status: IN_PROGRESS
```

## T02 — Research / Discovery
```yaml
question: 
source_priority: []
search_boundary: 
internal_sources: []
external_references: []
findings: []
inferences: []
source_gaps: []
verification: []
next_action: 
```

## T03 — Plan / Execution
```yaml
outcome: 
work_units: []
dependencies: []
owners: []
priority: 
evidence_per_unit: []
blockers: []
stop_gates: []
ready_queue: []
next_action: 
```

## T04 — Decision
```yaml
decision_question: 
options: []
criteria: []
evidence: []
tradeoffs: []
reversibility: 
unknowns: []
recommendation: 
approval_required: 
```

## T05 — Status / Compact HUD
```yaml
status: 
mission_primary: 
delta: 
evidence: []
blocked_not_done: []
blocker_validity: HARD|SOFT|INVALID|NONE
safe_continuation: []
next_action: 
risk_gate: 
resource_values: MEASURED_ONLY
```

## T06 — HOFF / Continuity
```yaml
mission: 
owner_system: 
source_ids: []
completed_verified: []
current_state: 
decisions_locks: []
open_loops: []
blockers: []
artifacts: []
exact_next_action: 
status: 
```

## T07 — QA / Review
```yaml
artifact: 
source_baseline: []
checks: []
results: []
pass_fail: 
debt: []
regression: []
readback: 
approval_gate: 
recommended_status: 
```

## T08 — Data / Analysis
```yaml
question: 
schema: 
sources: []
transformations: []
validation: []
metrics: []
exceptions: []
insights: []
actions: []
reproducibility_note: 
```

## T09 — Communication
```yaml
audience: 
objective: 
context: 
verified_facts: []
tone: 
message: 
call_to_action: 
attachments_links: []
approval_before_send: 
```

## T10 — Document
```yaml
audience: 
reading_goal: 
source_boundary: []
sections: []
evidence: []
version_status: 
renderer: 
export_format: 
qa: []
```

## T11 — Visual / Graphic
```yaml
message: 
audience: 
verified_content: []
design_profile: 
canvas_viewport: 
visual_hierarchy: []
assets: []
renderer: HTML_CSS_JS_SVG_OR_EQUIVALENT
accessibility: []
render_qc: []
```

## T12 — Presentation
```yaml
audience: 
objective: 
narrative_arc: []
slide_roles: []
evidence: []
speaker_intent: 
design_profile: 
export: 
qa: []
```

## T13 — Web / UI
```yaml
user_job: 
information_architecture: []
components: []
states: [default,loading,empty,error,success]
actions: []
data_contract: []
responsive_rules: []
accessibility: []
tests: []
deployment_gate: 
```

## T14 — Learning / LMS
```yaml
learner: 
learning_objectives: []
prerequisites: []
source_boundary: []
lesson_architecture: []
reinforcement: []
assessment: []
assignment: 
media_units: []
qa: []
owner_registration: 
```

## T15 — Media Production
```yaml
source_script: 
scene_timeline: []
narration_source: 
audio_artifact: 
subtitle_timing_source: 
visual_units: []
render_target: 
technical_qc: []
render_evidence: []
```

## T16 — Automation / Agent
```yaml
mission: 
trigger_cadence: 
inputs: []
state: 
actions: []
tools_permissions: []
idempotency: 
retry_policy: 
verification: []
notification_policy: 
blocker_behavior: 
stop_condition: 
```

## T17 — Blocker / Recovery
```yaml
blocked_action: 
reason: 
evidence: []
validity: HARD|SOFT|INVALID
safe_fallback: []
independent_work_continued: []
unblock_condition: 
next_action: 
```

## T18 — Evolution / Maintenance
```yaml
candidate: 
existing_coverage: []
proven_gap: 
measurable_value: []
evidence: []
comparison: 
decision: UPDATE_EXISTING|CREATE_NEW|DEPRECATE|NO_CHANGE|NEED_CONFIRM
benchmark_impact: 
regression_impact: 
dependency_impact: 
rollback: 
next_action: 
```

## Composition example
An LMS video does not create a new bespoke template. Compose:
`T01 + T14 + T15 + T11 + T07 + T06`
Then select renderer/design profile separately.

## Rule
A template is a starting contract, not permission to invent missing facts. Unknown required truth remains unknown and routes through T17 or the owner system.