# Visual and Studio Workflows

Load for graphic/media work or multi-model artifact quality review. The canonical [work contract](../my.md) and [Public Standard](../PUBLIC_STANDARD.md) govern authority, scope, and completion. These procedures are conditional; they do not add a mandatory Studio path to ordinary work.

## Contents

- Multi-AI Studio OS
- Graphic Runtime

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

## Graphic Runtime — required for visual work

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

