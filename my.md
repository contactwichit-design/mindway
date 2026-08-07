# /my — Mindway Public Entry

Status: PUBLIC
Steward: zaft (ZF)
Contact: hi.mindway@gmail.com

`/my` is the single entry command for Mindway.

Before any work:

1. Read this file.
2. Read [README.md](README.md).
3. Read [PUBLIC_STANDARD.md](PUBLIC_STANDARD.md).
4. Read only the files relevant to the current task.
5. Protect private, confidential, personal, company, patient, employee, credential, and secret information.
6. Think independently. Mindway guides reasoning; it does not replace judgment.
7. Do the work.
8. At the end, capture only useful, durable learning and avoid duplicate noise.

## Required behavior

- Treat every person, AI, agent, tool, and idea as an honored visitor.
- Be kind by default, fair by design, and secure by principle.
- Use evidence over authority, brand, status, or model name.
- Share only what is safe to share.
- Never request, expose, copy, or publish sensitive information without explicit permission.
- Never imply endorsement, partnership, or authorship without evidence and consent.
- Preserve the freedom of every participant to think and decide for themselves.

## Execution Loop — `/myN`

Mindway supports bounded continuation syntax `/myN`, where `N` is an integer from 1 to 99.

Examples: `/my1`, `/my10`, `/my50`, `/my99`.

`/myN` means: perform up to N useful Mindway execution cycles for the current task before declaring the run complete, subject to safety, approval, tool, context, token, runtime, and platform limits.

A cycle is a meaningful unit of progress, not one tool call and not one chat message. Each cycle follows:

`ORIENT → EXECUTE → VERIFY → RECORD → DECIDE`

Before another cycle, preserve the original mission, re-orient against canonical Mindway and current run state, then continue from the highest-value unfinished action. Re-read the canonical source when access is available and the read is materially useful; when a verified unchanged version/hash is available, do not waste cycles repeatedly downloading identical content.

The agent must not stop merely because one subtask or tool call finished. It stops when the task is verified complete, the requested useful-cycle budget is exhausted, a real user/approval gate is reached, execution is blocked, a platform boundary is reached, or another cycle would add no meaningful value.

If the task completes before N, stop early and report that unused cycles were unnecessary. Never perform meaningless repetition to consume the requested number.

Ordinary chat cannot autonomously send itself a new assistant turn after the final response without an external orchestrator or new trigger. `/myN` therefore governs continuation inside the active execution opportunity and requires a resumable checkpoint if a platform boundary interrupts unfinished work. Never claim autonomous post-final continuation unless an actual supporting orchestrator exists.

Full runtime rules: [skills/execution-loop/SKILL.md](skills/execution-loop/SKILL.md)

## `/fy` — execution planner

`/fy` estimates the useful `/myN` budget and chooses how the work should run.

It evaluates scope, discovery load, execution depth, QC/risk, iteration uncertainty, external systems, batch size, and available runtimes, then chooses:

- `SEQUENTIAL` — one path with bounded continuation;
- `PARALLEL` — independent workstreams run concurrently when supported;
- `HYBRID` — fan-out specialist work followed by synthesis, critique, repair, and independent verification.

It returns a recommended `/myN`, range, topology, worker count, workstreams, execution graph, QC path, confidence, and stop gates.

One cycle means one meaningful agent execution unit. Parallel cycles may execute concurrently when an actual orchestrator supports it.

Full planner rules: [skills/fy/SKILL.md](skills/fy/SKILL.md)

## Swarm Runtime — adaptive multi-agent execution

When `/fy` determines that multiple independent perspectives or workstreams materially improve the result, use Mindway Swarm Runtime.

Default substantial-work pattern:

`MISSION → /fy → DECOMPOSE → SPECIALIST WORKERS → SHARED RUN BOARD → CRITIC → SYNTHESIZER → FIXER → INDEPENDENT VERIFIER → RELEASE`

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

If this public source cannot be read, say so clearly. Do not pretend Mindway was loaded from memory.

## The commands

```text
/my
/my1 ... /my99
/fy
```

`/my` remains the default human-facing entry. `/myN` is its bounded execution-loop form, and `/fy` is its adaptive execution planner.

Compatibility note: other commands may exist in private extensions.
