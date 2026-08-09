---
name: mindway-mcp
description: Expose canonical Mindway protocol, loop runtime contracts, skill stock, run ledger, schemas and safe examples to MCP-compatible local AI and specialist workers without exposing secrets or private operational payloads.
version: 0.1.0
status: REVIEW_READY
---
# Mindway MCP
## Purpose
Provide a small, local-first grounding surface for AI workers.
## Resource contract
Expose read-only resources first:
- `mindway://canonical/my`
- `mindway://runtime/loop`
- `mindway://schemas/event`
- `mindway://schemas/run`
- `mindway://skills/index`
- `mindway://skills/{skill_id}`
- `mindway://runs/{run_id}` only after redaction/authorization.
## Tool contract
Optional tools may include `search_skills`, `get_skill`, `validate_event`, `validate_run`, `checkpoint_run`, and `query_run_graph`.
Writes to canonical protocol, permissions, external publication, destructive operations, credentials, or sensitive data are never implicit MCP authority.
## Grounding rules
1. Canonical `/my` outranks cached skill content.
2. Return provenance, maturity and last-verified metadata with reusable skills.
3. Never represent `INDEX_ONLY` or `NOT_YET_READ` source material as learned content.
4. Prefer local files/SSOT and minimal payloads.
5. Redact private/company/patient/employee/credential content before exposing run data.
6. MCP availability does not equal permission to mutate owner systems.
## Local AI readiness
A worker should be able to discover a skill, inspect dependencies/examples/tests, run its own compatibility check, then use it without loading the whole Mindway corpus.
