# Mindway LMS Evaluation Profile v0.1
Status: EXPERIMENTAL

Purpose: use LMS production as the high-value proving ground for Mindway runtime improvements while preventing benchmark overfitting.

## Test surfaces
1. Source fidelity — no unsupported facts, omissions, or terminology drift.
2. Instructional objective — learner can identify the intended action/knowledge after the asset.
3. Content completeness — required module/scene/checklist/quiz elements survive transformation.
4. Visual hierarchy — key point is perceptually dominant; whitespace is intentional; no overflow/underfill proxy abuse.
5. Thai/Unicode — glyphs, line breaks, numerals, abbreviations, and pronunciation source are correct.
6. Motion — deterministic first/last frame, duration, transitions, no blank flashes/jitter.
7. Audio — narration completeness, pronunciation, loudness consistency, timing and A/V sync.
8. Dental visual correctness — tooth/anatomy/icon registry matches the intended treatment/context.
9. Export integrity — expected dimensions, fps, duration, codec/container and file readability.
10. Accessibility/learning usability — readable text duration, contrast, captions/transcript where required.
11. No-regression — accepted qualities from prior best-known artifact remain unless an explicit trade-off is approved.
12. Decision usefulness — reviewer can rapidly understand what changed, why, evidence, and next action.

## Candidate protocol
For a production task, generate the minimum useful candidate breadth rather than a fixed huge count. Score deterministic gates first, then rubric graders, then pairwise compare top candidates. Preserve only candidates that beat the current accepted frontier without losing locked qualities.

A 1000-run test means 1000 scenario executions of the evaluation/runtime logic unless 1000 actual media renders are explicitly executed. Never claim simulated scenarios are 1000 produced videos.

## Anti-overfit split
- 60% development fixtures
- 20% hidden-like perturbation fixtures
- 20% holdout fixtures not used to tune thresholds

Perturbations should include long Thai text, short sparse scenes, missing assets, wrong tooth/icon, timing extremes, narration mismatch, stale source, contradictory instructions, renderer failure, export failure, and tool interruption.

## Release gate
Release only when hard factual/source/export gates pass, mission-level rubric passes, no consequential open failure remains for the artifact, and the candidate is not worse than the accepted frontier on locked dimensions.

## Learning telemetry opportunity
When LMS instrumentation is added, prefer xAPI-compatible event semantics for learner activity/performance so learning analytics are portable. Keep learner identity/private data out of public Mindway test fixtures.
