# Mindway Template Router

Status: REVIEW_READY  
Version: 0.2.0

## Goal
Turn a natural-language request into the smallest sufficient template composition without asking the user to choose a template when intent is clear.

## Route

`REQUEST → INTENT TAGS → FAMILY COMPOSITION → OWNER SOURCE → EXECUTION → QA → RENDERER → HANDOFF`

## Step 1 — classify behavior
Identify only behavior that materially changes execution:

- define / assign / scope → T01
- search / learn / compare / verify sources → T02
- plan / sequence / decompose → T03
- choose / approve / recommend → T04
- report state / routine / dashboard status → T05
- resume / transfer / checkpoint → T06
- inspect / test / QC / regression → T07
- calculate / analyze / KPI / structured data → T08
- email / LINE / memo / announcement / CTA → T09
- report / SOP / policy draft / proposal / reading artifact → T10
- visual / infographic / diagram / poster → T11
- presentation / slides / narrative deck → T12
- website / dashboard / interactive UI / app → T13
- lesson / LMS / curriculum / quiz / assessment → T14
- video / audio / narration / subtitle / motion → T15
- recurring / trigger / workflow / agent → T16
- blocked / failed / missing dependency / fallback → T17
- skill / reusable improvement / benchmark / maintenance → T18

## Step 2 — compose minimally
Use the fewest families that cover the behavior. T01 and T07 are common but are not mandatory for trivial work. Do not load all 18 families.

## Step 3 — resolve source ownership
Before drafting substantive facts, identify the owner system and current/locked/candidate/archive state. Project-specific locked templates override generic templates for their scope.

## Step 4 — select renderer separately
The semantic content object is primary. Renderer is selected after content:

- chat_compact — quick user answer / Mindway Compact Report
- markdown — durable text / GitHub / HOFF
- html — visual, UI, deterministic document surface
- pdf / docx — formal reading artifact
- slides — presentation
- image — static rendered frame
- video — timed rendered sequence
- connected_system — Sheet/Asana/Drive/etc. write when authorized

Visual work under `/my` uses the Graphic Runtime and deterministic code-first composition by default.

## Step 5 — apply design profile
Design profile is an override layer. It changes visual expression, not facts, workflow, source ownership, evidence, QA, or approval.

## Step 6 — blocker integrity
A blocker never means “stop everything” automatically.

For every blocked/stopped/skipped/not-done action, resolve:
1. exact blocked action;
2. reason;
3. evidence;
4. HARD / SOFT / INVALID;
5. safe fallback;
6. independent work still executable;
7. exact unblock condition.

Before stopping, test read-only discovery, alternative source/artifact, reversible setup, smaller safe subtask, and independent work.

## Step 7 — completion
Do not promote draft/candidate/folder-only/part-only/script-ready/local-only states when stronger evidence is required. Final/publish/deploy/high-impact actions remain subject to owner approval.

## Default compositions

| Request pattern | Composition |
|---|---|
| Approval memo | T01 + T09 + T10 + T07 |
| Research report | T01 + T02 + T10 + T07 |
| Project execution plan | T01 + T03 + T17 + T07 |
| Decision comparison | T01 + T02 + T04 + T07 |
| Routine status | T01 + T05 + T17 + T07 |
| Handoff | T01 + T06 + T07 |
| Sales/data dashboard | T01 + T08 + T04 + T13 + T07 |
| Graphic/infographic | T01 + T11 + T07 |
| Presentation | T01 + T12 + T11 + T07 |
| Website/app | T01 + T13 + T07 + T06 |
| LMS lesson/clip | T01 + T14 + T15 + T11 + T07 + T06 |
| Video/audio | T01 + T15 + T11 + T07 |
| Automation/routine | T01 + T16 + T05 + T17 + T07 |
| Skill/system evolution | T01 + T18 + T07 + T06 |

## Ambiguity rule
If multiple compositions are plausible but produce materially different risk or outputs, choose the safest reversible path or ask one targeted question. Do not ask questions only to make the user choose an internal template name.

## Token/performance rule
Prefer registry metadata and this router before opening full template detail. Load detailed family guidance only for selected families.