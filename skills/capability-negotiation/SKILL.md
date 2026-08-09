# Mindway Capability Negotiation

Status: REQUIRED WHEN TOOL/TRANSPORT CAPABILITY AFFECTS EXECUTION

## Mission

Choose execution routes from capabilities that actually exist in the current runtime instead of assuming provider behavior from model or vendor name.

## Contract

Before a task depends on an external capability, determine the smallest relevant capability surface:

`NEED → DISCOVER AVAILABLE CAPABILITIES → CLASSIFY READ/WRITE/SIDE-EFFECT → SELECT SAFEST SUFFICIENT ROUTE → EXECUTE → VERIFY`

Do not perform exhaustive capability discovery when the task does not need it. Discover only what materially affects the mission.

## Capability record

For relevant capabilities classify each as one of:

- `AVAILABLE_VERIFIED` — capability was exposed and successfully exercised or otherwise reliably evidenced.
- `AVAILABLE_UNTESTED` — capability is exposed but has not yet been exercised.
- `UNAVAILABLE_VERIFIED` — runtime/tool surface demonstrates it is absent or unsupported.
- `FAILED_TRANSIENT` — route/tool exists but the attempt failed; this is not proof of absence.
- `UNKNOWN` — insufficient evidence.

Never turn `FAILED_TRANSIENT` or `UNKNOWN` into `UNAVAILABLE_VERIFIED` without evidence.

## Route selection

Prefer, in order:

1. read-only over write when read is sufficient;
2. native structured connector/API over brittle indirect routes when both provide equivalent authoritative access;
3. reversible over irreversible actions;
4. owner/SSOT sources over secondary copies;
5. verified capability over assumed provider behavior.

## Provider rule

Do not reason `ChatGPT can`, `Gemini cannot`, `Claude has`, or `local AI lacks` unless the current runtime actually provides evidence. Provider/model identity is not a capability manifest.

## Entry integration

For `/my` access, this skill supports `MW-BOOT/1` and `skills/entry-access-gate/SKILL.md`. If the first transport fails, classify it as a route failure and discover other relevant read capabilities before considering `MINDWAY_BLOCKED`.

## Side effects

Capability discovery never grants authority. Before writes, publishing, deletion, permission changes, transfers, or other high-impact side effects, apply the relevant approval and safety gates.
