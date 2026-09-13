# JOE × Hermes × Mindway — Working Plan

Date: 2026-09-09
Last 360 closeout: 2026-09-14
Status: REVIEW_READY / ACTIVE_DIRECTION
Owner: ZAFT

> Decision/data log only. This file does not modify canonical `/my`.

## Mission
Build **JOE** as ZAFT's persistent AI front door: conversational, visual, capable of real work, able to grow through memory/skills, and able to use multiple models/tools without locking JOE's identity to one provider.

## Architecture decision

### Front agent
- **Hermes is the primary front agent/runtime candidate.**
- ZAFT talks to JOE; Hermes supplies agent runtime, persistent memory, skills/growth, execution, delegation, and model/tool routing.
- JOE is the persistent identity/persona experienced by ZAFT.

### Mindway
- `/my` remains **Mindway DNA / governance**, not a replacement for Hermes.
- Keep only durable owner rules where they add value: mission preservation, SSOT, permission/safety boundaries, verification, learning governance, record/handoff discipline.
- Avoid duplicating Hermes-native planning, memory, skills, browser/tool execution, or agent capabilities unnecessarily.
- Canonical `/my` must not be modified as part of this implementation without separate review.

### Models/tools
Hermes/JOE may select appropriate specialists, including:
- OpenAI / Codex
- Gemini
- Claude
- Nous / Hermes models
- local models where useful
- GitHub
- Google Workspace
- browser/web/computer tools

Models are replaceable specialist brains; they are not JOE's permanent identity.

## Cost-routing rule
Exploit already-included/available entitlements before unnecessary API spend where safe and technically supported.

Initial routing preference:
- **Code, repository work, tests, refactors, build/deploy scripts → Codex first** when the available ChatGPT/Codex allowance can be used.
- General reasoning/consulting → best-fit model based on quality/cost.
- Large reading/context workloads → choose cost-effective long-context model.
- Simple repetitive tasks → cheapest adequate model or deterministic tooling.
- High-risk/final verification → strongest approved model + verification gate.
- Fallback to paid API only when subscription path/quota/tool support is insufficient.

Do not assume exact remaining quota; inspect the provider's usage/status when available.

## Conversation surfaces
Preferred progression:
1. ChatGPT as an early familiar conversation surface if a secure bridge to JOE/Hermes is available.
2. **JOE Web** as the long-term primary surface.
3. Optional LINE/voice/other channels later.
4. Telegram is not preferred as the primary user surface.

All surfaces should converge on the same JOE runtime/memory subject to security/profile separation.

## JOE Web product direction
JOE Web is a **conversational thinking workspace**, not just chat.

Core modes:
- Chat
- Mindmap
- Canvas / free drawing / flows
- Work / project status
- Files/media
- Memory/knowledge when appropriate

### Shared visual-thinking state
Chat, Mindmap, and Canvas should share the same project state:
- Chat instruction can modify a mindmap.
- Moving/editing a node becomes conversation context.
- Drawings/arrows/selected objects/images can be referenced directly.
- Switching modes must not force ZAFT to restate context.

### Media/output support
- Images/galleries
- Video preview/streaming
- PDF/docs
- Tables/charts/dashboards
- Code/structured output
- Before/after comparison
- Progress/status and approval actions

## Performance locks
Performance is first-class.

1. Typing, dragging, drawing, panning and selection happen locally and feel immediate.
2. UI never waits for Hermes/LLM completion before responding.
3. AI responses and progress stream incrementally.
4. Long-running jobs do not block the UI.
5. Load on demand; never preload all chats, memories, files, media and logs.
6. Images use thumbnails/previews first.
7. Video streams instead of preloading full files.
8. Web UI and Hermes runtime are separate processes/services.
9. Hermes restart/failure must not make the workspace entirely unusable.
10. Prioritize native-app-like feel on iPhone/mobile.

## Security / company-data direction
- Do not create one unrestricted Personal + Company memory/permission pool.
- Separate JOE Personal and JOE Company profiles/zones where needed.
- Use least privilege: only approved folders, repos, mail/calendar scopes, sheets, or systems.
- Secrets/API keys/OAuth tokens never live in `/my`, Git history, prompts, or general memory.
- Maintain an audit trail of significant reads/writes/actions/model destinations.
- Classify data before model routing. Sensitive company/patient/employee/credential data must not be sent to unapproved providers.
- Start company integrations read-only and narrow; expand permissions only after verification/approval.

## Deployment direction
- Hermes should run on an always-available host (initial candidate: VPS/cloud VM; free/low-cost options should be evaluated first).
- Private management/access plane preferred; do not expose a privileged Hermes control API directly to the public Internet.
- JOE Web is a separate front-end service communicating with Hermes through a controlled API/event channel.

## Candidate implementation history
The local `joe-candidate` evolved through multiple verified checkpoints:
- Early runnable demo: commit `2803da3` on `candidate/joe-workspace`.
- Follow-up integration/UI checkpoint: `950006d`.
- Local performance/memory work: code `fc6f21c`, handoff `889d13a`.
- Owner-gate preparation: `1a85d5f`, checkpoint `89e1b42`.
- Windows Hermes bootstrap repair: commit `2f16ca4`, checkpoint `2697d40`.

Reported verification improved from 20 → 23 → 32 → 42 tests, with lint/typecheck/build passing and dependency audit reporting 0 vulnerabilities at the latest bootstrap checkpoint.

## Current Candidate behavior
JOE Candidate currently targets:
- Chat streaming
- Projects
- Mindmap
- Canvas
- Media Library
- Personal/Company boundary awareness
- local-first project/memory persistence
- bounded context to Hermes
- Codex-first coding route
- same-origin Node policy boundary
- isolated Hermes profile

The Candidate architecture intentionally keeps company sources disabled and keeps personal Hermes isolated from company mounts/connectors/credentials.

## Runtime / authentication progress
### Completed
- Git for Windows installed successfully after bootstrap found `git` missing.
- Windows bootstrap was repaired so owner should not manually build a Python venv.
- Bootstrap now detects Python, creates/repairs isolated venv, installs pinned dependencies, handles Windows long-path behavior, and is intended to be idempotent.
- Hermes runtime/gateway was observed running after bootstrap.
- Codex device authentication setting in ChatGPT Security was enabled.
- **OpenAI Codex OAuth succeeded**; terminal confirmed credential added as `openai-codex-oauth-1`.

### Still requiring acceptance verification
Do not mark `LIVE_CANDIDATE` until all are actually proven:
- `provider-check` resolves Codex successfully.
- real Hermes general request succeeds.
- real Codex coding request succeeds and actual provider is verified.
- second-turn/session continuity works.
- project memory survives expected reload/restart behavior.
- reconnect/error path works.
- any prior `HERMES_EMPTY_RESPONSE` condition is either gone or root-caused/fixed.
- pending media QA is closed: video, PDF, download, cancel/reselect, large-file behavior.
- GitHub remote/private repo push and PR evidence are completed if still pending.
- full regression remains green.

## Owner-action policy
For Candidate work, Codex was authorized to continue through safe/reversible work without asking repeatedly. Owner actions should be batched and requested only where interactive login/account confirmation is genuinely required.

Allowed Candidate scope included:
- isolated personal Hermes setup
- Codex personal OAuth
- candidate code/refactors/tests
- browser/mobile QA
- Docker/local deployment/config scripts
- JOE identity/memory/skills structure
- GitHub private Candidate repo work without secrets

Still blocked without separate approval:
- Production deployment
- public sharing
- new billing/cost commitments
- company-wide Google Workspace access
- company credentials
- patient/employee/payroll/HR-confidential data
- destructive operations
- canonical `/my` modifications

## Initial build sequence
1. Preserve this decision log.
2. Create JOE continuity package: persona/SOUL, durable user context, project boundaries, Mindway Core rules.
3. Stand up Hermes Candidate runtime (no production/company-wide privileges).
4. Connect Codex first for code-heavy workloads; add provider fallbacks deliberately.
5. Validate memory + skill growth + restart persistence.
6. Build minimal JOE Web shell with Chat + streaming + project list.
7. Add Mindmap with shared conversation state.
8. Add Canvas/object-referenced conversation.
9. Add media/file/work views.
10. Add security profiles, company connector scopes, audit logs, and approval gates.
11. Performance QA on iPhone/mobile and slow-network scenarios.
12. Only after candidate gates pass, consider broader company use.

## Non-goals / anti-patterns
- Do not rebuild Hermes inside Mindway.
- Do not make `/my` duplicate every Hermes feature.
- Do not bind JOE identity permanently to ChatGPT, Gemini, Claude, or Nous.
- Do not create an all-powerful company agent on day one.
- Do not preload the entire knowledge/memory store into every request.
- Do not expose secrets or privileged agent APIs publicly.

## Current decision
**Hermes = primary agent/runtime candidate.**
**JOE = persistent identity/front experience.**
**Mindway = durable DNA/governance.**
**Codex = preferred first coding worker when plan allowance is available.**
**JOE Web = target primary visual workspace.**

## 360 closeout — 2026-09-14
Preserve these points for the next session:
1. Do not restart architecture discussion from zero; Hermes-at-front + JOE identity + Mindway DNA is the accepted direction.
2. Do not add unrelated product features before closing `LIVE_CANDIDATE` acceptance.
3. Next execution order: provider-check → live Hermes request → live Codex route → continuity/memory → media QA → GitHub remote evidence → full regression.
4. Keep Personal and Company security zones separated; no company-sensitive data in personal memory/runtime.
5. Keep Codex-first routing for code to use existing allowance before unnecessary API spend.
6. JOE Web remains visual-first: Chat + Mindmap + Canvas + media/work views, with local-first performance and streaming AI.
7. Canonical `/my` remains unchanged by this project unless separately reviewed.

Next milestone: **close `LIVE_CANDIDATE` evidence gate, then move to Growth Memory/Skills quality and broader JOE Web hardening.**