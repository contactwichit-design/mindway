---
name: myoff
description: Canonical Mindway DEEP handoff and persistence contract for resumable cross-chat work.
version: 1.0.0
status: ACTIVE
---

# /myoff — DEEP Resume Package

## Mission

Persist enough verified operational context that a capable AI which did not see the original chat can safely resume the work without asking the owner to retell the story.

A `/myoff` record is a **navigation and resume package**, not a transcript and not a replacement Source of Truth.

## Mandatory entry

Before executing `/myoff`:

1. Enter canonical `/my` and pass its required Entry Access Gate.
2. Preserve any exact owner-supplied work code, Run ID, Decision ID, project/workstream name, and source identifiers.
3. Use the current chat/workstream as the primary source for what actually happened. Do not upgrade remembered or recovered claims to verified state without evidence.

## Canonical persistence destination — Mindway 00_MAIN

For the current Mindway `00_MAIN` workspace, every successful `/myoff` MUST persist to this single canonical **Native Google Sheet**:

- Title: `00_ZF_AI_CONTROL_CENTER`
- Spreadsheet ID: `16WAw-NCgB27KVfwnkwWO7If5mlzd0BNabTfsX3iBbKE`
- Canonical URL: `https://docs.google.com/spreadsheets/d/16WAw-NCgB27KVfwnkwWO7If5mlzd0BNabTfsX3iBbKE/edit`
- Expected timezone: `Asia/Bangkok`

The prior Office-file Control Center with Drive File ID `1h1Zw3SGFex9RMwhxFAVIdwrOCk-uRDiE` is **LEGACY / DO NOT WRITE** after this migration. It may be used only as historical evidence when needed.

### Storage binding rule

Do not create a replacement spreadsheet, folder, database, or alternate handoff store merely because the canonical sheet is temporarily inaccessible.

If the canonical destination cannot be read or written after reasonable supported routes are tested:

- generate the complete handoff in the current response;
- set persistence state to `PERSISTENCE_BLOCKED`;
- state the exact route/tool limitation;
- state the smallest action required to restore persistence;
- never claim `/myoff COMPLETE` and never claim that data was saved.

If the canonical destination is intentionally changed by the owner, the binding in this skill and the active Control Center decision must be updated in the same migration before new `/myoff` writes use the new destination.

## Canonical tab contract

### `06_HANDOFF_DETAIL` — full Resume Package

Append one DEEP package per `/myoff`. Preserve the existing header contract:

1. Handoff ID
2. Event Time
3. Recorded Time
4. Workstream
5. Chat / Topic
6. Source Mode
7. Work Status
8. Evidence State
9. Mission
10. Why It Matters
11. Target / DoD
12. Story So Far
13. Current State
14. Completed / Verified
15. In Progress
16. Decisions + Rationale
17. Hard Locks / Do Not Touch
18. Systems / Dependencies
19. Source of Truth / Evidence
20. Data / Interface Contracts
21. Risks / Uncertainty
22. Failed / Rejected Routes
23. Open Loops / Decisions Needed
24. Exact Next Actions
25. Resume Instruction
26. Related IDs

Use the minimum detail that passes the resume test; do not dump the entire transcript.

### `01_AI_LOG` — event/index ledger

Append one concise index row for the same handoff. It must contain the Handoff ID in `Related ID` and enough information for MAIN CONTROL to locate the detailed package.

`01_AI_LOG` is history/index, not current-state truth and not a transcript.

### `00_CONTROL` — current operational snapshot

Update only when the `/myoff` changes the current state of a workstream. One workstream should resolve to one current-state row. Do not reconstruct current state by treating every historical event as current.

### `03_DECISION_LOG` — durable active decisions

Add or update only decisions/hard locks that must survive the chat. Do not copy ordinary discussion into the decision log. When a newer owner-approved decision replaces an older one, preserve history and mark the old decision `SUPERSEDED` rather than silently deleting it.

### `02_TARGET_SNAPSHOT` — mission / target contract

Update only when Mission, Target/DoD, hard locks, Source of Truth, or critical path materially changes. Do not rewrite it on every `/myoff` when nothing changed.

## Evidence model

Work Status and Evidence State are independent axes.

Recommended Work Status values:

- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `WAITING`
- `NEED_QC`
- `DONE`

Evidence State values:

- `VERIFIED` — checked against authoritative source or completed tool result in the relevant run.
- `REPORTED` — stated by the source chat/work record but not reverified in the current handoff run.
- `STALE` — previously supported but freshness is no longer sufficient for current execution.
- `UNKNOWN` — evidence is missing or insufficient.

Never treat Control Center text itself as sufficient proof to upgrade an item to `VERIFIED`.

## Source Mode

Use a source mode that makes provenance clear, for example:

- `SOURCE_NATIVE` — current source chat/workstream and relevant live sources were directly available.
- `PROJECT_RECOVERY` — reconstructed from surfaced project context or continuity records.
- `PRIOR_CONTEXT_RECOVERY` — reconstructed from prior context without full source-native verification.

Recovery records may be useful for navigation, but must not impersonate live verified workstream state.

## Event time and recorded time

Keep them distinct:

- `Event Time` = when the underlying work/event happened, when known.
- `Recorded Time` = when the handoff was written to Control Center.

For historical recovery where exact event time is not known, use an explicit approximate/unknown value. Never use the backfill timestamp as if it were the original event time.

## DEEP content requirements

Include, when relevant:

- exact work code / chain / related Run IDs;
- Mission and Why It Matters;
- Target / Definition of Done;
- Current State;
- Completed / Verified work and verification method;
- In Progress work;
- owner decisions and rationale;
- Hard Locks / Do Not Touch;
- systems and dependencies;
- authoritative Source of Truth / evidence pointers;
- data/interface contracts, keys, schemas, outputs, or status vocabularies needed for resumption;
- Risks / Uncertainty;
- important Failed / Rejected Routes and why they failed;
- only material human/communication context that changes execution;
- Open Loops / Decisions Needed;
- ordered Exact Next Actions;
- a short Resume Instruction.

Protect private, patient, employee, credential, financial, secret, and other sensitive information. Prefer safe references/IDs/links and concise summaries over copying protected raw data into the Control Center.

## Seven-question PASS gate

A `/myoff` package is sufficient only if a capable AI that did not see the original chat can answer:

1. What are we doing, and why?
2. What is the Target / Definition of Done?
3. What was actually completed?
4. What is `VERIFIED` versus `REPORTED`, `STALE`, or `UNKNOWN`?
5. Which decisions / Hard Locks must not be reversed?
6. What blockers and important failed routes exist?
7. What exact action should happen next, and which authoritative source should be opened first?

If the next AI must ask the owner to retell basic prior state, the handoff is `INCOMPLETE`.

## Handoff ID

Reuse an owner/project-defined exact work code or Run ID when it already supplies the continuity identity. Otherwise create a stable unique Handoff ID and use that exact same ID in `06_HANDOFF_DETAIL` and `01_AI_LOG`.

Do not renumber an owner-supplied work code.

## Write sequence

Use this sequence unless a stronger workspace rule applies:

`ORIENT → BUILD DEEP PACKAGE → WRITE 06_HANDOFF_DETAIL → WRITE 01_AI_LOG → UPDATE 00_CONTROL IF STATE CHANGED → UPDATE 03_DECISION_LOG IF A DURABLE DECISION CHANGED → UPDATE 02_TARGET_SNAPSHOT IF TARGET CONTRACT CHANGED → READ BACK → VERIFY → REPORT`

Prefer direct Native Google Sheets range/cell updates. Do not replace the entire workbook merely to append a handoff when direct native writes are available.

## Verification gate

Before reporting success:

1. Re-read the exact `06_HANDOFF_DETAIL` row and confirm the Handoff ID and required fields.
2. Re-read the corresponding `01_AI_LOG` row and confirm it points to the same Handoff ID.
3. If `00_CONTROL`, `03_DECISION_LOG`, or `02_TARGET_SNAPSHOT` changed, re-read those exact cells/rows too.
4. Confirm the write occurred in spreadsheet ID `16WAw-NCgB27KVfwnkwWO7If5mlzd0BNabTfsX3iBbKE`.
5. Report the canonical Sheet URL and Handoff ID.

`WRITE ATTEMPTED ≠ PERSISTED`

`PERSISTED ≠ VERIFIED`

Only after read-back verification may the state be `/myoff COMPLETE`.

## Cold-start resume behavior

A new AI resuming work should use:

`/my → resolve canonical Control Center → read current workstream row → read relevant Target + active Decisions → read newest relevant DEEP handoff → follow Source of Truth pointer → verify freshness/current state → resume from the highest-value safe next action`

The Control Center navigates to truth; it does not become the workstream's live truth merely because it is easier to read.

## Completion response

A successful `/myoff` should report at minimum:

- `/myoff COMPLETE`
- Handoff ID
- Workstream
- Work Status
- Evidence State
- Exact Next Action
- canonical Control Center URL

A failed persistence attempt must report `/myoff PERSISTENCE_BLOCKED` instead, with the handoff content preserved in the response and no false save claim.