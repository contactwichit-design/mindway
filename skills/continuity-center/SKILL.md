# Mindway Continuity Center Runtime

Status: ACTIVE
Scope: ongoing work that must survive chats, agents, models, providers, or long gaps between sessions

## Purpose

Preserve enough operational context that a new AI or a designated Center AI can understand the work, why it matters, what has already happened, what must not be changed, and what should happen next — without relying on model memory or replaying the entire conversation.

The continuity record is not a transcript and not a second source of truth. It is a verified navigation layer back to the real sources, decisions, artifacts, and unfinished work.

Core principle:

`DO NOT TRUST MEMORY ALONE → READ THE WORK RECORD → VERIFY SOURCES → RESUME FROM CURRENT STATE`

## Center AI model

A Center AI is a **role**, not a permanent model identity.

Its job is to reconstruct and coordinate the current state across workstreams from canonical continuity records and authoritative source systems. A different model/provider may fill the Center role later without losing the project, provided the records remain intact and verifiable.

The Center AI must not silently become the business, clinical, legal, data, or system owner. Source authority remains with the applicable owner/system.

## Work codes

When the owner or project supplies a work code, preserve that exact code. Do not renumber, reinterpret, merge, or invent a replacement code unless the project rules explicitly allow it.

A project may use a sequence such as:

`WORK-1 → WORK-2 → WORK-3 → ...`

Each record should identify its predecessor when known so the chain can be followed without reading unrelated files.

If no work code exists, do not create project-specific numbering merely for convenience unless the workspace explicitly authorizes it.

## When a continuity record is required

Create or update a continuity record when at least one is true:

- the owner explicitly asks to save, hand off, off-load, record, checkpoint, or continue the work elsewhere;
- the work has a supplied work code;
- the work spans multiple chats, agents, models, systems, or days;
- decisions, dependencies, locks, risks, or unfinished actions would be costly to rediscover;
- a Center AI or future worker will need to resume without the full conversation;
- a project-defined handoff command (for example `/off`) requires it.

Do not create continuity noise for trivial self-contained tasks.

## Record depth

Use the minimum depth that preserves real continuity.

### LIGHT

Use for simple ongoing work where the mission and next action are obvious.

Minimum:

- WORK CODE
- MISSION
- CURRENT STATE
- COMPLETED
- OPEN LOOP
- NEXT ACTION

### DEEP

Use for explicit handoff/off-load, complex system work, multi-system dependencies, high rework cost, or when the owner asks for detailed preservation.

A DEEP record should contain, when relevant:

1. **WORK CODE / CHAIN** — exact code, previous code, related workstreams.
2. **MISSION** — what outcome is actually being pursued.
3. **WHY IT MATTERS** — operational/business reason; what failure would cause.
4. **CURRENT STATE** — where the work truly stands now, not merely what was discussed.
5. **COMPLETED / VERIFIED** — actions actually completed and how they were verified.
6. **IN PROGRESS** — work started but not yet closed.
7. **DECISIONS + RATIONALE** — decisions already made and why; distinguish owner decision from AI proposal.
8. **HARD LOCKS / DO NOT TOUCH** — contracts, schemas, story spines, permissions, systems, fields, files, or constraints that must be preserved.
9. **SYSTEMS / DEPENDENCIES** — source → transformation → consumer relationships and downstream risks.
10. **SOURCE OF TRUTH / EVIDENCE** — authoritative systems/files/threads and useful identifiers or links where safe.
11. **DATA / INTERFACE CONTRACTS** — keys, fields, outputs, status vocabularies, or compatibility requirements that matter to resumption.
12. **RISKS / UNCERTAINTY** — unresolved facts, confidence limits, possible failure modes.
13. **FAILED / REJECTED ROUTES** — important attempts that should not be repeated blindly, including why they failed.
14. **HUMAN CONTEXT** — only human/emotional context that materially changes how the work should be continued.
15. **OPEN LOOPS / DECISIONS NEEDED** — concrete unresolved items and who owns the decision when known.
16. **NEXT ACTIONS** — ordered next steps, beginning with the highest-value safe action.
17. **RESUME INSTRUCTION** — the shortest accurate instruction a future AI needs to re-enter the work.
18. **STATUS / TIMESTAMP** — current status vocabulary and the time of the snapshot when useful.

## Human context — enough to communicate, not psychoanalyze

Continuity may include emotional or interpersonal context when it materially affects execution, communication, review, or prioritization.

Useful examples:

- the owner is worried that the work is becoming fragmented;
- repeated loss of context is causing frustration and should be actively prevented;
- the owner wants communication to sound like them rather than like a formal generated document;
- a topic is politically or organizationally sensitive and should be phrased carefully;
- the owner has low confidence in a specific subsystem because prior attempts failed;
- a decision carries urgency or pressure that changes the order of operations.

Rules:

1. Prefer the owner’s explicit words or a cautious paraphrase.
2. Record only context that changes how future work should be done.
3. Do not diagnose personality, mental state, health, motive, or sensitive traits.
4. Do not turn a fleeting mood into a durable identity claim.
5. Do not preserve private or sensitive details merely to make the record feel personal.
6. Human context is execution context, not evidence of technical fact.

A good Human Context section is usually short but specific enough that the next AI understands the tone, pressure, concern, or trust issue around the work.

## Facts, inference, proposal, feeling

Do not flatten different kinds of knowledge into one voice. Mark material items when ambiguity would matter:

- `FACT` — directly supported by an authoritative source or completed tool result.
- `OWNER DECISION` — explicitly chosen/approved by the owner.
- `INFERENCE` — reasoned conclusion that may still require verification.
- `PROPOSAL` — suggested future approach, not yet authoritative.
- `HUMAN CONTEXT` — owner-expressed concern, preference, pressure, or communication need.

## Source and privacy discipline

A continuity record points back to sources; it does not replace them.

- Preserve source provenance and exact identifiers when useful and safe.
- Do not copy large sensitive datasets into the record.
- Do not expose patient, employee, credential, financial, secret, or other protected information beyond what is strictly necessary and authorized.
- Prefer references, IDs, links, file names, schema names, and concise summaries over duplicating raw protected content.
- Respect the workspace’s source-of-truth hierarchy.

## Center AI read behavior

Before a Center AI answers “where are we?”, assigns work, or resumes a coded workstream:

1. Read the newest relevant continuity record.
2. Follow the chain backward only as far as needed to resolve missing rationale or dependencies.
3. Verify material current-state claims against authoritative live sources when freshness matters.
4. Merge related workstreams by reference; do not physically collapse their histories merely for convenience.
5. Detect conflicts between records and source systems; source authority wins.
6. Surface stale records instead of treating them as current truth.
7. Continue from the highest-value unfinished safe action.

## Worker AI write behavior

A worker creating a continuity record must:

- record what actually happened, not what it intended to do;
- distinguish complete, partial, blocked, proposed, and unverified states;
- preserve important negative knowledge (what was tried and should not be repeated blindly);
- preserve owner locks and decisions;
- include enough rationale that a future AI does not undo a deliberate choice;
- keep the record navigable rather than dumping the entire transcript;
- update the existing relevant record/chain when project rules prefer update-over-duplication.

## Relationship to durable learning

Continuity state and durable learning are different.

- **Continuity state** answers: “Where is this work now, why, and what next?”
- **Durable learning** answers: “What reusable principle should survive beyond this specific workstream?”

Do not discard necessary continuity merely because it is project-specific. Conversely, do not promote every project detail into global durable learning.

Core invariant:

`PROJECT CONTINUITY ≠ GLOBAL MEMORY`

## Closure / handoff test

Before considering a DEEP handoff sufficient, ask:

- Could a capable AI that did not see this chat understand the mission?
- Would it know what has actually been completed?
- Would it know which decisions and locks must be preserved?
- Would it know which systems/sources to trust?
- Would it understand material human context and communication sensitivity?
- Would it avoid repeating known failed routes?
- Could it identify the next safe action without asking the owner to retell the story?

If not, the record is too thin.

If the record requires reading the entire prior conversation to understand basic state, the handoff has failed.
