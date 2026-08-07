---
name: fy
description: Estimate the useful /myN execution budget and choose the best Mindway execution topology before starting a task. Use when the user invokes /fy, asks how many cycles/agents a task needs, or when choosing sequential vs parallel vs hybrid execution would reduce premature stopping, blind spots, or waste.
version: 2.0.0
status: REVIEW_READY
---

# /fy — Mindway Execution Planner v2

## Purpose

`/fy` plans how Mindway should execute a task, not merely how long one agent should keep trying.

It returns:

- recommended `/myN` cycle budget;
- topology: `SEQUENTIAL`, `PARALLEL`, or `HYBRID`;
- minimum useful worker count;
- workstream decomposition;
- review/synthesis/verification stages;
- likely stop/approval gates;
- confidence and rationale.

One cycle means one meaningful agent execution unit. When an external orchestrator supports concurrency, several cycles may execute in parallel.

## Output

```text
/fy
Recommended: /myN
Range: /myA-/myB
Topology: SEQUENTIAL | PARALLEL | HYBRID
Workers: N
Graph: ...
Confidence: LOW | MEDIUM | HIGH
Why: ...
Workstreams: ...
QC path: ...
Stop gates: ...
```

## Step 1 — score complexity

Score each dimension 0-4.

### Scope (S)
0 trivial; 1 small; 2 several subtasks; 3 multi-artifact/system; 4 broad project/workstream.

### Discovery (D)
0 supplied; 1 one source; 2 several sources; 3 cross-system reconciliation; 4 uncertain/large/changing landscape.

### Execution depth (E)
0 answer; 1 one production action; 2 build+revise; 3 multiple stages; 4 architecture/implementation/migration.

### QC/Risk (Q)
0 low; 1 normal check; 2 strict QC; 3 business/brand/data/release-sensitive; 4 legal/clinical/destructive/high-impact.

### Iteration uncertainty (I)
0 deterministic; 1 known flow; 2 likely fixes; 3 experiments/comparisons; 4 research/prototyping with unknown failure modes.

`T = S + D + E + Q + I`

Base cycle mapping:

- 0-2 -> `/my1`
- 3-5 -> `/my2`
- 6-8 -> `/my3`
- 9-11 -> `/my5`
- 12-14 -> `/my8`
- 15-17 -> `/my12`
- 18-20 -> `/my20`

Modifiers:

- multiple external systems: +2 to +8;
- batch artifacts: +2 to +15;
- strict regression/QC: +2 to +6;
- tested alternatives: +2 to +8;
- reusable runtime/skill: +2 to +6;
- existing runtime/template: -1 to -5;
- cacheable/incremental work: -1 to -5;
- review-only scope: -1 to -4.

Clamp 1-99.

## Step 2 — choose topology

Choose `SEQUENTIAL` when:

- dependencies are strongly serial;
- source mutations must happen in order;
- task is small;
- concurrency creates write conflicts;
- one specialist can complete safely with independent verification.

Choose `PARALLEL` when:

- 3+ workstreams are independent;
- discovery can happen concurrently;
- deliberate ensemble comparison is useful;
- batch units are isolated and safe to run concurrently.

Choose `HYBRID` when:

- independent discovery/build streams can fan out but final integration/QC is serial;
- maker/critic/fixer/verifier separation is useful;
- the task combines research, architecture, implementation, and risk analysis.

Default substantial-system topology:

`specialist workers -> critic -> synthesizer -> fixer -> independent verifier`

Use the minimum useful number of workers. More agents are not automatically better.

## Step 3 — decompose work

Give each workstream:

- stable ID;
- role;
- goal;
- expected output;
- dependencies;
- relevant sources/context;
- whether concurrent execution is safe.

Prefer differentiated roles over identical workers unless ensemble redundancy is intentionally requested.

Useful roles include:

- researcher;
- architect;
- builder;
- failure_hunter;
- evidence_checker;
- critic;
- synthesizer;
- fixer;
- verifier.

## Step 4 — plan integration

Fan-in must not concatenate outputs blindly.

Plan for:

1. unique finding extraction;
2. semantic deduplication;
3. conflict detection;
4. evidence ranking;
5. fact/inference/proposal separation;
6. synthesis;
7. targeted critique;
8. repair;
9. independent verification.

For large fan-in, prefer tree reduction over one giant synthesis context.

## Step 5 — evidence policy

Never use simple majority vote as the final correctness rule.

Use:

`Evidence quality > reproducibility > source freshness/authority-for-task > vote count`

Preserve a minority finding when it is better-supported than the majority.

## Step 6 — cycle accounting

Example:

```text
5 workers in parallel = 5 cycles
2 critics = 2 cycles
1 synthesis = 1 cycle
1 repair = 1 cycle
1 verification = 1 cycle
Total = /my10
```

Parallel execution reduces wall-clock time when the orchestrator supports it, but does not erase execution-cycle accounting.

N remains a maximum useful budget, not an obligation to waste cycles.

## External orchestration

When topology requires actual simultaneous agents across turns/processes, use Mindway Swarm Runtime if available:

- `skills/swarm-runtime/SKILL.md`
- `runtime/swarm_runner.py`

Normal chat alone cannot guarantee spawning autonomous post-final turns. Be explicit about that boundary.

## Examples

### Small rewrite
`/my1`, `SEQUENTIAL`, 1 maker; no swarm.

### Spreadsheet reconciliation
Likely `/my5-/my10`, `HYBRID`: source checker + formula checker + risk/QC, then synthesis and verification.

### Reusable LMS runtime
Likely `/my10-/my20`, `HYBRID`: research + architecture + implementation + failure hunter + evidence check, then critic/synthesis/repair/verify.

### Large migration
Potentially `/my20-/my50`, usually staged HYBRID graphs with explicit approval milestones.

## Invocation behavior

When `/fy` is invoked with a task, return the plan. Do not silently execute unless the user also asked to start.

When `/fy` is invoked without a task, ask for or infer only when the intended task is already clear from the current conversation.
