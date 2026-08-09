# /loop Migration Status — 2026-08-09

Mission: unify `/fy`, `/myN`, continuation, verification/repair, observability, knowledge ingestion and local-AI skill access under `/loop` without breaking compatibility.

## Implemented
- `skills/loop/SKILL.md` unified command contract.
- `runtime/schemas/mindway_event.schema.json` event contract.
- `runtime/schemas/mindway_run.schema.json` durable run-ledger contract.
- `runtime/loop_runtime.py` state/event/checkpoint backbone.
- `runtime/test_loop_runtime.py` core regression tests.
- `runtime/observatory/index.html` code-first Observatory MVP.
- `runtime/knowledge_ingest.py` provenance/read-status ingestion primitives.
- `runtime/schemas/mindway_skill.schema.json` executable skill lifecycle schema.
- `skills/mindway-mcp/SKILL.md` local-first MCP contract.
- `runtime/mindway_mcp_server.py` minimal dependency-free MCP stdio server.
- `runtime/test_knowledge_mcp.py` ingestion/MCP regression tests.
- `.github/workflows/runtime-tests.yml` CI regression definition.

## Verification state
`NOT_DONE`: repository regression suite has not produced an executed PASS result.

Observed blockers:
1. Local execution environment cannot resolve `github.com`, so it cannot clone the canonical repository for an exact test run.
2. GitHub repository Actions query returned zero workflow runs after workflow commits; therefore no CI PASS evidence exists in the available environment.

These are hard blockers only for the canonical-promotion gate, not for reversible implementation work.

## Canonical gate
`my.md` remains unchanged with `/myN` and `/fy` as public commands. Do NOT promote `/loop` to canonical primary command until the exact repository test suite runs and passes.

After PASS:
1. re-read canonical `/my` and required references;
2. update `my.md` to make `/loop` primary execution command;
3. map `/fy -> /loop plan` and `/myN -> /loop N` as compatibility aliases;
4. retain legacy skill files during deprecation window;
5. run regression again against the canonical migration;
6. mark `/loop` TESTED/ACTIVE only after that second pass.

No destructive migration, permission change, secret exposure, or legacy deletion has been performed.
