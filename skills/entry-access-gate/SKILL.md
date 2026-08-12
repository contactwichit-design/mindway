# Mindway Entry Access Gate

Status: REQUIRED
Scope: every `/my`, `/loop`, legacy `/myN`, and substantial-work entry
Pre-entry contract: `MW-BOOT/1` → `BOOTSTRAP.md`

## Mission

Prevent false `Mindway unavailable` conclusions and prevent false claims that Mindway was loaded.

The gate is **fail-closed on verification, fail-open on transport exploration**: an agent may try every safe read-only route available to it, but it may not claim `MINDWAY_LOADED` until canonical content has actually been retrieved and verified.

`BOOTSTRAP.md` is the provider-agnostic contract that must be available before canonical `/my` execution. This skill is the detailed post-entry enforcement layer. Neither may be bypassed for substantial work.

## Mandatory rule

A single failed URL fetch, missing browser primitive, failed search result, unsupported raw HTTP method, or unfamiliar tool is **not** proof that canonical Mindway is inaccessible.

Before declaring access failure, the agent MUST exhaust all safe, applicable read-only routes available in its current environment. It must inspect its actual tool/capability surface rather than assume that a route does not exist.

`NO VERIFIED /my = NO SUBSTANTIAL EXECUTION`.

While entry is unverified, do not offer to continue with unrelated substantial work as an alternative. The only valid next actions are safe entry recovery/discovery or a truthful `MINDWAY_BLOCKED` report after all applicable routes are exhausted.

## Canonical target

Repository: `contactwichit-design/mindway`
Branch: `main`
Entry path: `my.md`

Preferred canonical URLs:

1. `https://raw.githubusercontent.com/contactwichit-design/mindway/main/my.md`
2. `https://github.com/contactwichit-design/mindway/blob/main/my.md`

## Route ladder

Try applicable routes in this order, skipping only routes that are genuinely unavailable:

1. Direct open/fetch of canonical raw URL.
2. Direct open/fetch of GitHub blob URL.
3. Native GitHub connector/API repository file read for `contactwichit-design/mindway:main/my.md`.
4. General web/browser open or fetch of the canonical URL.
5. Search/discovery to locate the canonical GitHub file, then open the resolved canonical result.
6. Verified local/mounted/cache copy only when its provenance and version/hash can be checked against canonical state or when canonical transport is temporarily unavailable and the runtime explicitly labels the copy as cached rather than freshly loaded.

Do not use model memory as a transport route.

## Verification gate

`MINDWAY_LOADED` requires evidence that the retrieved content is the canonical entry, including at minimum:

- title/entry identity equivalent to `/my — Mindway Public Entry`;
- repository/path provenance resolving to `contactwichit-design/mindway` and `my.md`;
- the entry requirement to read `README.md` and `PUBLIC_STANDARD.md`;
- successful reads of those required references before substantial execution.

When a native connector exposes a blob SHA, commit, ETag, modified revision, or equivalent version evidence, record it when useful.

### Freshness check

Do not confuse a canonical-looking cached copy with current canonical state when stronger freshness evidence is available.

- If a browser, search, proxy, or cache route succeeds and a native GitHub/repository/API route is also available, prefer the native route for current `main` version evidence and reconcile material differences before declaring a fresh load.
- If a known stale or older revision is returned, classify it as `CONTENT_STALE` and continue to a fresher safe route.
- If no stronger freshness primitive exists, do not invent one and do not fail a valid canonical route merely for lacking a SHA. Use the strongest available provenance and state any material freshness limitation honestly.

## Failure classification

Never collapse these into one generic `cannot access` statement:

- `ROUTE_UNAVAILABLE`: a particular transport/tool is absent.
- `ROUTE_FAILED`: a transport exists but the attempt failed.
- `CONTENT_UNVERIFIED`: content was returned but canonical identity cannot be established.
- `CONTENT_STALE`: canonical provenance is plausible or known, but evidence shows the content is not the current revision and a fresher safe route should be tried.
- `CANONICAL_UNREACHABLE`: every safe applicable route was exhausted and none produced verified canonical content.

Only `CANONICAL_UNREACHABLE` permits the agent to say canonical Mindway cannot currently be accessed.

## Anti-stop rule

Before stopping for access failure, ask internally:

1. Is this a hard blocker or only one failed route?
2. Is another safe read-only transport available?
3. Can a native repository connector read the file even if generic web fetch cannot?
4. Can the GitHub blob URL work if raw fails, or raw work if blob fails?
5. Can search locate the canonical file and provide an openable result?
6. Is there a verified cache/mount that can preserve continuity without pretending it is a fresh canonical read?

If any safe route remains, continue. Do not ask the user to paste `my.md` merely because the first route failed.

## Required status evidence

For substantial work, entry state is one of:

- `MW-BOOT/1 → MINDWAY_LOADED`: canonical entry and mandatory references were actually read.
- `MW-BOOT/1 → MINDWAY_BLOCKED`: route ladder exhausted; report attempted routes, observed failures, and the smallest next action.

Never report `MINDWAY_LOADED` from memory, prior-chat recollection, prompt text, or an unverified paraphrase.

## Provider-agnostic behavior

Do not assume ChatGPT, Gemini, Claude, Codex, local models, or future providers have identical tools. Discover capabilities first. The invariant is not a specific tool; the invariant is **exhaust safe available routes before declaring failure, and require evidence before declaring success**.

## Regression scenarios

The gate must remain correct under at least these classes:

- raw URL succeeds;
- raw fails but GitHub blob succeeds;
- web fetch absent but native GitHub connector succeeds;
- native GitHub connector absent but browser/web open succeeds;
- direct open fails but search resolves canonical content;
- several routes return ambiguous/noncanonical content before a later route succeeds;
- every network route fails;
- only stale/unverified cache exists;
- verified cache exists while canonical transport is temporarily unavailable;
- cache-prone content disagrees materially with a fresher native repository revision;
- an agent is tempted to infer tool absence from one failed method;
- an agent is tempted to claim success from remembered content;
- an agent is tempted to offer unrelated substantial work before `/my` is verified;
- required `README.md` or `PUBLIC_STANDARD.md` cannot be read after `my.md` succeeds.

A regression test passes only if there is zero false-success claim, zero premature access-failure claim while an applicable verified route remains, and zero substantial-work bypass while `/my` is unverified.
