---
name: knowledge-stock
description: Ingest external knowledge into Mindway without losing provenance, classify read depth and integration readiness, retain reusable skills for future Local AI/worker use, and prevent premature promotion of untested ideas into active protocol.
version: 0.1.0
status: REVIEW_READY
---

# Mindway Knowledge Stock v0.1

## Purpose

Turn external websites, repositories, documents, experiments, and observed failures into a durable knowledge/skill inventory while keeping canonical Mindway stable.

## Read-status contract

Every source page/item must be marked as exactly one of:

- `READ_FULL` — full primary page read and summarized.
- `READ_DEEP` — main content/techniques studied deeply; peripheral content may remain.
- `INDEX_ONLY` — page/index discovered and catalogued; child content not fully read.
- `NOT_YET_READ` — known target queued for future ingestion.
- `READ_SUMMARY` — only a reliable secondary/indexed summary was available; do not treat as a full primary-source read.

Never upgrade a status without evidence from an actual read.

## Retention rule

Do not discard useful external knowledge merely because it is not needed now. Classify instead:

- `USE_NOW` — low-risk/high-value pattern that improves current Mindway work.
- `KNOWLEDGE` — durable mental model or architecture principle worth retaining.
- `STOCK` — reusable skill/function reserved for future Local AI, specialist workers, or projects.
- `QUEUE` — known source/skill awaiting deeper reading, testing, or integration.

## Skill lifecycle

Reusable skills should progress through:

`DISCOVERED -> STOCK -> EXPERIMENTAL -> TESTED -> ACTIVE -> LOCKED`

Alternate terminal states:

`DEPRECATED` or `REPLACED`.

Presence in the stock does not mean a skill is safe for production.

## Minimum skill record

```json
{
  "skill_id": "stable-id",
  "name": "...",
  "source_urls": ["..."],
  "provenance": "primary|secondary|experiment",
  "read_status": "READ_DEEP",
  "maturity": "STOCK",
  "target_runtime": ["..."],
  "capabilities": ["..."],
  "dependencies": [],
  "examples": [],
  "fixtures": [],
  "expected_outputs": [],
  "tests": [],
  "risks": [],
  "last_verified": "YYYY-MM-DD"
}
```

## Executable-skill preference

For important reusable skills, prefer an executable skill pack over a prose-only note:

- `SKILL.md`
- runnable example(s)
- fixture/input sample
- expected output
- regression/QC test
- provenance/source metadata
- compatibility/version notes

This makes future Local AI workers able to load, test, and use a skill rather than merely read about it.

## Source ingestion loop

`DISCOVER -> INVENTORY -> READ -> EXTRACT -> CLASSIFY -> DEDUPE -> TEST -> INTEGRATE or STOCK -> VERIFY -> RECORD`

Keep source-derived facts separate from Mindway adaptation proposals.

## Privacy and provenance

- Do not place private/company/patient/employee/credential data into public skill stock.
- Store source URLs and verification dates.
- Preserve uncertainty and conflicting evidence.
- External brand/vendor claims are evidence inputs, not authority.

## Integration gate

Promote a pattern to `ACTIVE` only when:

1. it solves a real Mindway need;
2. dependencies and trade-offs are understood;
3. a test or concrete successful use exists when feasible;
4. it does not conflict with canonical Mindway;
5. rollback/compatibility is understood.

Otherwise keep it in `KNOWLEDGE`, `STOCK`, or `QUEUE`.

## Tool-use learning capture — required at every /my

At every verified canonical `/my` entry, treat this Knowledge Stock capture rule as active. During execution, when a non-obvious, reusable, evidence-backed tool workaround or effective interaction pattern is discovered, capture it before closure in an authorized persistent location, then read back to verify. This is an execution rule, not an assumption that every discovery is already saved.

- Distinguish `DISCOVERED`, `TESTED`, and `VERIFIED`; never call an untested trick active.
- Record tool/runtime, task and failure signature, exact reproducible remedy, scope and safety caveats, independent observed result, source/provenance, and regression check.
- Prefer updating an existing skill/record rather than creating duplicates. Respect project SSOT for private details; generalize public lessons without identifiers, credentials, session details, or private data.
- If persistence is inaccessible, report `PERSISTENCE_BLOCKED` and provide an exact proposed record; do not claim it was saved.
- On later related tasks, consult relevant verified tool lessons before retrying known failed routes, while re-verifying current compatibility.

### Verified reference case — editable browser fields via Windows accessibility

- **Environment:** Authorized Windows desktop; Remote Desktop Commander + locally installed `pywinauto` UIA backend; authenticated browser in a separately opened window.
- **Observed failure:** A rich `contenteditable` field accepted typing, but normal Ctrl+A replacement did not select the entire editor; appended input corrupted the prompt. Generic browser automation could not target the rich field.
- **Verified remedy:** Locate the exact authorized browser window, inspect its UIA tree, target the intended Edit control (not a neighboring field), focus it, invoke `edit.iface_text.DocumentRange.Select()`, then send Backspace and type the replacement via the UIA-supported keyboard path. Read back the full content, reload the page, reopen the step and read it again to prove persistence.
- **Test result:** Corrected Thai-language draft prompt persisted after reload, required-field validation cleared, and an isolated manual text-only test returned the expected structured text with successful execution status.
- **Safety:** Do not seize unrelated windows or live user sessions. Disable external source access when not needed, use synthetic data, avoid send/publish/mutation steps, and obtain approval for higher-impact actions. UIA coordinates/control trees may vary across apps and versions; inspect before acting.
- **Regression check:** Verify the exact editor is targeted; inserted content has no prefix/suffix from old prompt; no validation error; reload preserves text; test run is isolated and has no external side effects.
- **Status:** `TESTED` for this environment and field class, not universally `ACTIVE` on all websites.
