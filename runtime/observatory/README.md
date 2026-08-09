# Mindway Observatory MVP
Code-first, local-first view derived from runtime evidence.

Views: `Universe Graph ↔ Run Timeline ↔ Inspector`.

`index.html` contains a deterministic demo and exposes `window.loadMindwayRun(run)` for normalized view data:

```json
{"nodes":[{"id":"task","type":"task","label":"Task","status":"running"}],"edges":[["task","worker"]],"events":[["work.started","Task"]]}
```

Production adapters should transform `mindway_event.schema.json` JSONL plus the run ledger into this view model. The renderer must not infer unsupported causality. Sensitive event payloads must be redacted before rendering or export.

MVP verification checklist:
- no random layout or fabricated events;
- node/event selection updates Inspector;
- timeline preserves event order;
- failed/fixed/complete states are distinguishable without relying on text alone in future accessibility pass;
- large runs should add clustering/LOD before rendering every node.
