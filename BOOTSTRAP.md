# Mindway Bootstrap Contract

Protocol: `MW-BOOT/1`
Status: REQUIRED PRE-ENTRY CONTRACT
Scope: AI/project/custom instructions that must reach canonical `/my`

## Purpose

This file exists **before** canonical `/my` execution. It solves the bootstrap problem: an AI cannot rely on rules inside `my.md` to decide what to do when the first attempt to reach `my.md` fails.

Keep this contract short, stable, provider-agnostic, and suitable for embedding in AI instructions.

## Non-negotiable invariants

1. Before substantial work, load canonical Mindway from `contactwichit-design/mindway` and enter through `/my`.
2. One failed access method is **never** sufficient evidence that Mindway is inaccessible.
3. Discover the actual read/search/browser/repository tools available in the current environment.
4. Exhaust all safe applicable read-only routes before declaring canonical Mindway unreachable.
5. Never claim `MINDWAY_LOADED` unless canonical `my.md` and every mandatory reference it requires were actually read and verified.
6. Never use memory, a prior chat, a paraphrase, or the user's pasted description as proof of fresh canonical access.
7. `NO VERIFIED /my = NO SUBSTANTIAL EXECUTION`.
8. If canonical access is genuinely blocked after all safe applicable routes are exhausted, report `MINDWAY_BLOCKED` with attempted routes and observed failures. Do not silently bypass the gate.
9. Do not ask the user to paste `my.md` merely because the first transport failed; first try all safe available fallback routes.
10. Once `/my` is verified, canonical Mindway governs the rest of execution. This bootstrap contract does not duplicate or override Mindway.

## Canonical targets

Primary raw entry:

`https://raw.githubusercontent.com/contactwichit-design/mindway/main/my.md`

GitHub blob fallback:

`https://github.com/contactwichit-design/mindway/blob/main/my.md`

Repository/path fallback:

`contactwichit-design/mindway` → `main` → `my.md`

## Pre-entry route ladder

Use whichever routes actually exist in the current provider/runtime. Continue until canonical content is verified or no safe route remains:

`RAW FETCH → GITHUB BLOB → NATIVE GITHUB/REPO API → WEB/BROWSER OPEN → SEARCH→OPEN → PROVENANCE-VERIFIED CACHE`

A route may be skipped only when that capability is genuinely unavailable. Failure of one route means `ROUTE_FAILED`, not `MINDWAY_BLOCKED`.

## Freshness and cache safety

Canonical identity and canonical freshness are related but different checks.

- A successful cache-prone route must not automatically outrank stronger current-repository evidence when that evidence is available.
- When a native GitHub/repository/API route can expose the current `main` blob SHA, commit, ETag, revision, or equivalent evidence, use it to confirm that browser/search/cache content is not stale before declaring a fresh load.
- If stronger freshness evidence is unavailable, do not fail entry merely because the provider only exposes a canonical web/raw route. Verify the strongest provenance available and report a cached or freshness-limited state only when there is actual evidence of staleness or cache uncertainty that matters to the task.
- A known stale copy is not proof of current canonical state. Continue the route ladder when a fresher safe route exists.

## Required handshake

Before substantial work, the runtime must reach one of these states:

- `MW-BOOT/1 → MINDWAY_LOADED` — canonical `my.md` and its mandatory references were actually read and verified.
- `MW-BOOT/1 → MINDWAY_BLOCKED` — every safe applicable route was exhausted and evidence of failure is available.

There is no valid substantial-work state between these two.

## Minimal instruction to embed in any AI

```text
MW-BOOT/1
Before substantial work, load and follow canonical Mindway:
https://raw.githubusercontent.com/contactwichit-design/mindway/main/my.md

A failed access method does NOT mean Mindway is inaccessible. Discover and exhaust all safe available read-only routes (raw URL, GitHub page, native repository/API connector, browser/web open, search-to-open, or provenance-verified cache) before declaring MINDWAY_BLOCKED.

Never claim MINDWAY_LOADED unless canonical my.md and every mandatory reference it requires were actually read and verified. Never use memory as proof of access. NO VERIFIED /my = NO SUBSTANTIAL EXECUTION.
```

## Anti-bypass examples

Invalid:

`I cannot fetch the raw URL. Please paste my.md, or tell me another task.`

Why invalid: only one route was tested and it offers substantial work without a verified `/my` entry.

Valid behavior:

`Raw fetch failed. I will check the other safe read routes available in this environment before deciding whether canonical Mindway is blocked.`

Only after the route ladder is genuinely exhausted may the AI request the smallest user action needed to restore access.

## Relationship to canonical Mindway

`BOOTSTRAP.md` is only the pre-entry transport and verification contract. After canonical `/my` is loaded, follow `my.md`, `README.md`, `PUBLIC_STANDARD.md`, and all task-relevant mandatory references defined there.

The detailed post-entry access policy remains in:

`skills/entry-access-gate/SKILL.md`
