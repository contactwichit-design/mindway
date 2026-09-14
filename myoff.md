# /myoff — Mindway Deep Handoff Entry

Status: ACTIVE
Scope: Mindway continuity handoff / off-load / resume packaging

`/myoff` is the canonical command for closing or handing off an active chat/workstream so another capable AI can resume without the owner retelling the story.

## Entry contract

1. Enter canonical `/my` first and pass its required access gate.
2. Read [skills/myoff/SKILL.md](skills/myoff/SKILL.md).
3. Create a DEEP Resume Package from what actually happened in the current chat/workstream.
4. Persist it to the canonical Control Center destination defined by the `/myoff` skill.
5. Read back the exact written records and verify persistence before reporting `/myoff COMPLETE`.

`/myoff` is **not** a chat summary and is **not** permission to invent missing state.

Core invariants:

`CURRENT STATE ≠ HISTORY`

`CONTROL CENTER ≠ SOURCE OF TRUTH`

`CONTROL CENTER = CONTROL PLANE / NAVIGATION LAYER`

`/myoff = RESUME PACKAGE, NOT CHAT SUMMARY`

`01_AI_LOG = EVENT INDEX, NOT TRANSCRIPT`

If the canonical persistence destination cannot be accessed or written, do not silently create a new spreadsheet, folder, database, or alternate log. Produce the handoff in the current response, mark persistence as `PERSISTENCE_BLOCKED`, state the attempted route and smallest action needed, and never claim the record was saved.

The canonical execution/storage contract is in [skills/myoff/SKILL.md](skills/myoff/SKILL.md).