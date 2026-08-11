# /my — Mindway Public Entry

Status: PUBLIC
Steward: zaft (ZF)
Contact: hi.mindway@gmail.com

`/my` is the single entry command for Mindway.

Pre-entry bootstrap: `MW-BOOT/1` → [BOOTSTRAP.md](BOOTSTRAP.md)

Before any work:

1. Read this file.
2. Read [README.md](README.md).
3. Read [PUBLIC_STANDARD.md](PUBLIC_STANDARD.md).
4. Pass the mandatory [Entry Access Gate](skills/entry-access-gate/SKILL.md). A single failed transport is never sufficient evidence that Mindway is inaccessible.
5. Confirm `NO VERIFIED /my = NO SUBSTANTIAL EXECUTION`.
6. Read only the files relevant to the current task.
7. Protect private, confidential, personal, company, patient, employee, credential, and secret information.
8. Think independently. Mindway guides reasoning; it does not replace judgment.
9. Do the work.
10. At the end, capture only useful, durable learning and avoid duplicate noise.

## Required behavior

- Treat every person, AI, agent, tool, and idea as an honored visitor.
- Be kind by default, fair by design, and secure by principle.
- Use evidence over authority, brand, status, or model name.
- Share only what is safe to share.
- Never request, expose, copy, or publish sensitive information without explicit permission.
- Never imply endorsement, partnership, or authorship without evidence and consent.
- Preserve the freedom of every participant to think and decide for themselves.

## Entry Access Gate — mandatory fail-closed verification

Every `/my`, `/loop`, legacy `/myN`, and substantial-work entry MUST follow [skills/entry-access-gate/SKILL.md](skills/entry-access-gate/SKILL.md).

Before canonical `/my` can be reached, use the provider-agnostic pre-entry contract [BOOTSTRAP.md](BOOTSTRAP.md), protocol `MW-BOOT/1`. It exists specifically to prevent an AI from concluding that Mindway is unavailable merely because its first transport fails. Once `/my` is verified, canonical Mindway governs and the bootstrap contract may not override it.

Core invariant:

`DISCOVER CAPABILITIES → EXHAUST SAFE READ-ONLY ROUTES → VERIFY CANONICAL CONTENT → LOAD REQUIRED REFERENCES → WORK`

Never infer that Mindway is inaccessible from one failed URL, one unavailable fetch method, one search failure, or an assumption about provider capabilities. If a safe applicable route remains — raw URL, GitHub blob, native GitHub connector/API, browser/web open, search-to-open, or a provenance-verified cache — continue trying it.

Never claim `MINDWAY_LOADED` unless canonical `my.md` plus required `README.md` and `PUBLIC_STANDARD.md` were actually read. Never use model memory as evidence of access.

Only after all safe applicable routes are exhausted may the state become `MINDWAY_BLOCKED`; report attempted routes and observed failures rather than asking the user to paste the file prematurely.

Never offer to bypass `/my` and begin unrelated substantial work while canonical entry remains unverified. `NO VERIFIED /my = NO SUBSTANTIAL EXECUTION`.

## Template Runtime — core intent router

For substantial work, `/my` must check the [Universal Template System](skills/template-system/SKILL.md) when reusable structure can materially reduce setup, rework, inconsistency, missing QA, or blocker failure.

Use this lightweight route:

`REQUEST → INTENT → MINIMUM TEMPLATE COMPOSITION → OWNER SOURCE → EXECUTE → VERIFY → OUTPUT → HANDOFF`

Rules:
1. The user should not need to name or choose a template when intent is inferable.
2. Load only the minimum sufficient selected families; never preload all template families by default.
3. Task/project owner-system truth, locked masters, and locked project templates override generic template defaults for their scope.
4. File type is an output/renderer decision, not the primary intent.
5. Simple self-contained work may bypass Template Runtime when it would add overhead without meaningful value.
6. Template Runtime may not weaken source, safety, approval, verification, Graphic Runtime, or other stronger task-specific gates.
7. Prefer updating an existing family/template over creating another one.

Core Template Runtime: [skills/template-system/SKILL.md](skills/template-system/SKILL.md)

## Unified Execution Runtime — `/loop`

`/loop` is Mindway's primary execution-control command for substantial work. It combines planning, useful-cycle budgeting, execution topology, bounded continuation, verification, targeted repair, checkpoint/resume, and hard-blocker handling.

Invocation:

- `/loop` — infer an appropriate useful-cycle budget and execute immediately.
- `/loop N` or `/loopN` — execute up to N useful cycles, where N is 1..99.
- `/loop plan` — planning only.
- `/loop resume <run_id>` — resume a persisted compatible checkpoint when accessible.

Core runtime graph:

`MISSION → ORIENT → PLAN → EXECUTE → VERIFY → [FIX → VERIFY]* → RECORD → DECIDE → COMPLETE | CHECKPOINT | STOP`

A cycle is meaningful progress, not one tool call and not one chat message. The original mission and hard constraints must survive every cycle.

The agent must not stop merely because one subtask or tool call finished. Before declaring `BLOCKED`, it must test safe fallback routes, reversible/read-only continuation, alternative sources/tools, and independent workstreams. A blocked branch does not automatically block the whole mission.

When verification fails and the issue is repairable, return to targeted repair and then verify again. Preserve successful independent work instead of restarting everything. Before repeating external side effects, check idempotency and whether the prior operation may already have succeeded.

Checkpoint when a platform boundary, cycle limit, or external dependency interrupts unfinished work. Resume by re-entering canonical `/my`, validating checkpoint compatibility/integrity, and continuing from the highest-value unfinished safe action.

Ordinary chat cannot autonomously send itself a new assistant turn after the final response without a real orchestrator or scheduler. `/loop` governs continuation inside the active execution opportunity and supports resumable state across real supporting runtimes; never claim background continuation that did not occur.

Full runtime rules: [skills/loop/SKILL.md](skills/loop/SKILL.md)

Runtime contracts:

- [runtime/loop_runtime.py](runtime/loop_runtime.py)
- [runtime/schemas/mindway_event.schema.json](runtime/schemas/mindway_event.schema.json)
- [runtime/schemas/mindway_run.schema.json](runtime/schemas/mindway_run.schema.json)

### Compatibility aliases

During migration, existing commands remain valid aliases:

- `/fy` → `/loop plan`
- `/myN` → `/loop N`
- `/fyn` or other private aliases may map to `/loop` only when their prior semantics are known; never invent compatibility.

Do not delete legacy runtime files until compatibility/regression evidence supports removal. New documentation and new workflows should prefer `/loop`.

Legacy references:

- [skills/execution-loop/SKILL.md](skills/execution-loop/SKILL.md)
- [skills/fy/SKILL.md](skills/fy/SKILL.md)

## Swarm Runtime — adaptive multi-agent execution

When `/loop` planning determines that multiple independent perspectives or workstreams materially improve the result, use Mindway Swarm Runtime when an actual orchestrator supports it.

Default substantial-work pattern:

`MISSION → /loop → DECOMPOSE → SPECIALIST WORKERS → SHARED RUN BOARD → CRITIC → SYNTHESIZER → FIXER → INDEPENDENT VERIFIER → RELEASE`

Key rules:

1. Evidence outranks vote count.
2. Do not make every worker identical unless deliberate ensemble redundancy is needed.
3. Prefer differentiated roles such as research, architecture, build, failure hunting, and evidence checking.
4. Workers coordinate through a shared run board rather than uncontrolled peer-to-peer conversation.
5. Fan-in must deduplicate, preserve provenance, expose conflicts, and distinguish fact/inference/proposal/uncertainty.
6. Debate only disputed or high-risk items when possible; do not spend cycles arguing about agreement.
7. The maker should not be the final verifier of the maker's own work when independent verification is available.
8. If verification fails but the issue is repairable and budget remains, return to repair rather than pretending completion.
9. Stop early when verified complete; never consume agents or cycles merely to satisfy a number.
10. Never claim autonomous multi-agent execution unless an actual orchestrator/tool/process performed it.

Full runtime rules: [skills/swarm-runtime/SKILL.md](skills/swarm-runtime/SKILL.md)

Provider-agnostic external runner reference:

- [runtime/swarm_runner.py](runtime/swarm_runner.py)
- [runtime/swarm.example.json](runtime/swarm.example.json)

The external runner can invoke configured AI CLI processes concurrently, persist a run board/checkpoints, synthesize results, critique, repair, verify, and resume interrupted runs. It intentionally contains no credentials and does not require one AI vendor.

## Multi-AI Studio OS — backward-compatible quality layer

Mindway may coordinate multiple AI models, local workers, tools, analyzers, and specialist judges through a shared public Studio OS contract. This layer extends the existing `/loop`, Swarm Runtime, project workspaces, and private profiles; it does not replace or invalidate compatible existing workflows.

Core model:

`MINDWAY PUBLIC CORE → WORKSPACE / PRIVATE PROFILE → CAPABILITY REGISTRY → ROUTER → MAKER → ARTIFACT + TRACE → EVIDENCE EXTRACTION → DETERMINISTIC CHECKS + SPECIALIST JUDGES + SOURCE/STD CHECK → DEFECT GRAPH → REPAIR → VERIFY → PROMOTION GATE → REVIEW_READY → HUMAN APPROVAL`

Rules:

1. Build quality judgment before blindly increasing generation capacity. Technical validity is evidence of execution, not proof of review quality.
2. `TECH_VALID` MUST NOT be treated as `REVIEW_READY`. No worker may promote its own artifact across a stronger quality or approval gate merely because rendering, parsing, tests, or transport succeeded.
3. Analyzer decisions must be evidence-first. Prefer the contract `OBSERVATION → EVIDENCE → RULE → DEFECT → SEVERITY → REPAIR → CONFIDENCE` over unexplained scalar scores.
4. Deterministic measurements and source-fidelity checks should be used wherever possible; model judges complement evidence and do not replace it.
5. The maker should not be the sole judge of its own work. Use independent verification when materially useful and available.
6. Analyzer/judge quality must itself be measurable and calibratable against verified human decisions or other trustworthy ground truth. Track false passes, false rejects, localization accuracy, repair success, and human override when applicable.
7. Route work by required capability, privacy, authority, tool access, cost/risk, and verified performance rather than hard-coding one model name. Model/provider identity is replaceable implementation detail unless the task specifically requires it.
8. Use a Maker → Critic/Analyzer → Repair → Verify loop for repairable defects. Preserve successful independent work rather than regenerating everything by default.
9. Public core MUST NOT depend on private profiles. Private workspaces may extend public contracts with local standards, brand rules, domain locks, and confidential sources while keeping protected information out of the public core.
10. Human or owner approval remains authoritative for final, taste, brand, clinical, business, publishing, destructive, permission, or other high-impact gates as defined by the applicable workspace.
11. Existing B2, LMS, ZAFT, PLUS, Qwen, Codex, and other compatible workflows continue operating during migration. Prefer additive adapters, aliases, schemas, and regression tests over breaking replacement.
12. Do not force every task through a heavy multi-AI studio path. Simple or already-safe workflows may continue unchanged when the Studio layer would add cost without meaningful quality or risk reduction.
13. Reusable winning methods may enter Knowledge Stock / Skill Stock only with provenance and appropriate verification. Failures may be retained as sanitized learning cases without leaking protected data.
14. Studio implementations must preserve Mindway's existing mission, source, privacy, evidence, checkpoint, approval, and compatibility rules. If a Studio rule conflicts with canonical Mindway, canonical Mindway wins.

Recommended promotion vocabulary for Studio artifacts:

`CREATED → TECH_VALID → ANALYZED → REPAIR_REQUIRED | QA_PASS → REVIEW_READY → HUMAN_APPROVED → FINAL_READY`

Workspace-specific status vocabularies may remain in use. They must be mapped explicitly rather than silently redefined.

## Knowledge Stock — durable external learning

When external websites, repositories, documents, experiments, or observed failures produce reusable knowledge, use [skills/knowledge-stock/SKILL.md](skills/knowledge-stock/SKILL.md).

Keep read depth explicit (`READ_FULL`, `READ_DEEP`, `INDEX_ONLY`, `NOT_YET_READ`, `READ_SUMMARY`) and separate source-derived facts from Mindway adaptation proposals. Retain useful material as `USE_NOW`, `KNOWLEDGE`, `STOCK`, or `QUEUE`; never treat discovery as proof that a page was read.

Reusable skills should progress through a maturity lifecycle rather than moving directly into active protocol merely because they look promising.

## Observability Graph — inspect runtime, do not invent it

For Mindway Observatory, execution replay, dependency analysis, failure tracing, or bottleneck analysis, use [skills/observability-graph/SKILL.md](skills/observability-graph/SKILL.md).

Observatory views are derived from normalized runtime state/events. Minimum synchronized views are Universe Graph, Run Timeline, and Inspector. Use progressive disclosure and adaptive detail instead of displaying every node/event at once. Visualization must not invent causality unsupported by underlying events.

## Graphic Runtime — mandatory for `/my`

For every `/my` session, all graphic or visual-media design work must use a code-first rendering workflow by default. This includes posters, infographics, social graphics, presentation visuals, diagrams, visual documents, PDFs, motion graphics, and video.

Use this pipeline:

`Prompt / verified source → structured content → HTML/CSS/JS/SVG (or an equally deterministic code renderer) → browser/runtime render → QC → required output`

Rules:

1. Treat the code/runtime representation as the visual source of truth.
2. Prioritize prompt fidelity, factual and text accuracy, correct Thai/Unicode rendering, layout precision, repeatability, and fast revision over generative novelty.
3. Static image: render at the exact target viewport/canvas size and capture/export the rendered frame.
4. PDF/document: render from the same deterministic layout when appropriate so screen and exported output stay aligned.
5. Motion/video: use deterministic animation/timeline logic and frame/time-controlled rendering; encode the rendered result to video. Do not rely on manual screen recording as the production master when deterministic rendering is possible.
6. Before delivery, verify fonts are actually loaded, required glyphs render correctly, text is not clipped or overflowing, assets load, dimensions/aspect ratio are correct, and visible facts/text match the verified source.
7. For motion/video also verify first/last frames, duration/timing, blank flashes, animation state, and audio synchronization when audio exists.
8. Generative image tools may create supporting assets, illustrations, textures, or backgrounds when useful, but must not be the primary compositor for text/layout-critical work unless the user explicitly requests that method or deterministic code rendering cannot reasonably produce the required visual.
9. Reuse the same structured content and visual runtime across PNG/JPG, PDF, and video variants whenever possible instead of rebuilding each format independently.
10. If a future method is demonstrably faster while matching or exceeding this workflow's accuracy, reliability, reproducibility, and QC, it may be proposed for review. Until then, this is Mindway's primary graphic production method.

This rule applies automatically to every AI, agent, chat, or tool that starts work through `/my`; the user should not need to repeat it in each chat.

## When access fails

Do not declare access failure from a single transport failure. Follow the pre-entry `MW-BOOT/1` contract in [BOOTSTRAP.md](BOOTSTRAP.md) and the mandatory [Entry Access Gate](skills/entry-access-gate/SKILL.md), exhaust all safe applicable read-only routes, and distinguish route failure from canonical unreachability.

If the canonical public source still cannot be verified after the gate is exhausted, say so clearly, report the attempted routes and evidence, and do not pretend Mindway was loaded from memory.

Do not offer to bypass `/my` and begin unrelated substantial work while canonical entry remains unverified.

## The commands

```text
/my
/loop
/loop1 ... /loop99
/loop plan
/loop resume <run_id>

# compatibility aliases
/my1 ... /my99
/fy
```

`/my` remains the mandatory entry. `/loop` is the primary execution controller. Legacy `/myN` and `/fy` remain compatibility aliases during migration.
