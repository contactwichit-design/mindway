---
name: observability-graph
description: Turn Mindway runtime state and events into an observable graph/timeline system with progressive disclosure, synchronized views, evidence annotations, and graph analytics. Use for Mindway Observatory, run replay, dependency analysis, failure tracing, bottleneck detection, or Local AI inspection interfaces.
version: 0.1.0
status: REVIEW_READY
---

# Mindway Observability Graph v0.1

## Purpose

Make Mindway execution inspectable without changing the execution core. Visualization is a derived view of verified runtime/event state, not a hand-drawn story.

## Core model

`Mindway Runtime -> Event/Graph Schema -> Observatory Views -> Human/AI Inspection`

Minimum synchronized views:

1. **Universe Graph** — tasks, agents, skills, tools, sources, artifacts, dependencies.
2. **Run Timeline** — temporal replay of orient/execute/verify/fix/improvement/return events.
3. **Inspector** — selected node/event details, evidence, status, source, annotations and next action.

Selections and filters should remain synchronized across views.

## Graph contract

Normalize before render. Recommended node types:

- task
- project/workstream
- agent/worker
- skill
- tool
- source
- artifact
- verifier/fixer
- improvement

Recommended edge types:

- routed_to
- depends_on
- used_skill
- called_tool
- produced
- verified_by
- failed_at
- fixed_by
- returned_to
- derived_from

Runtime event types should include at least:

`task.created`, `route.selected`, `work.started`, `tool.called`, `tool.succeeded`, `tool.failed`, `verify.pass`, `verify.fail`, `fix.started`, `fix.completed`, `improvement.proposed`, `checkpoint.saved`, `run.resumed`, `run.completed`.

## Progressive disclosure

Do not display every event/node at once.

Use hierarchy and clustering:

- project/workstream/skill-family/agent-swarm may collapse into a group/constellation;
- allow drill-down into the underlying graph;
- preserve context while expanding;
- foreground important signals and de-emphasize background noise.

## Layout selection

Layout is chosen by question:

- overview / structural discovery -> organic or structural;
- `/my`-centric dependency view -> radial;
- execution path / task flow -> sequential;
- focus/debug -> lens/focus layout;
- large disconnected components -> component packing/cluster view.

Do not lock Mindway Universe to one galaxy layout.

## Adaptive level of detail

As density/zoom changes:

- far: show constellations, density, aggregate status;
- medium: show tasks/workstreams/major dependencies;
- near: show event/tool/QC/fix detail.

Use aggregation, filtering, bundling, opacity and sizing to protect signal-to-noise.

## Evidence annotations

Failures, fixes, decisions and improvements should carry explainable annotations when available:

- reason
- evidence/source
- verifier result
- proposal
- uncertainty
- owner/approval gate when safe to expose

Visualization must not imply causality that the underlying events do not support.

## Graph analytics

When enough graph data exists, compute or expose:

- traversal/dependency path
- centrality/hubs
- shortest/critical paths when meaningful
- bottleneck/failure concentration
- orphan/unowned nodes
- repeated fix loops
- high-use/high-failure skills/tools

Analytics are decision support, not automatic truth.

## Local-first preference

Observability logs may contain sensitive operational context. Prefer local/self-hosted processing, redaction, minimal retained payloads, and disconnected operation where practical.

## Relationship to Graphic Runtime

Observatory visuals follow Mindway Graphic Runtime: code-first representation, deterministic rendering, exact text/data fidelity, and render/QC before export. Motion/replay should be driven by event time/state rather than random animation.

## External patterns learned

This skill was informed by publicly documented patterns from Cambridge Intelligence products and developer materials: coordinated graph/timeline/geospatial views, layouts, combos/progressive disclosure, annotations, graph analysis, event-driven component architecture, normalized data contracts, adaptive rendering, self-hosting and MCP-based developer grounding. These are patterns adapted for Mindway; this file does not imply partnership or SDK usage.
