# Booster comparison — 17 October 2026

Status: **scoped acceptance PASSED**. Owner-authorized adoption of the exact tested canonical contract and compatible project pointer.

## Decision

Candidate and baseline each satisfied **20/20 scenario acceptance criteria (100% observed in this sample)**. The candidate met the frozen threshold of at least 19/20, was no worse than baseline, and had zero observed critical failures within independently inspected evidence. Policy-file bytes read decreased from **83,030 to 48,950 UTF-8 bytes (41.05%)**. This supports a smaller common work contract while preserving sample outcomes.

## Design and results

Baseline commit: `72a1b045c48e3fb1e03fb68f99ee3c0bbe6f75ba` (67 files). Frozen candidate: 68 files, with five policy/document changes below. Protocol `MW-BOOSTER-COMPARE-20-v1.1` contains 20 synthetic scenarios and 45 locked scenario assertions per arm. The score denominator is 20.

Two fresh contexts used the same inherited model/effort without override, the same tools/permissions, and fixed C01–C20 order. Each ran one warm batch. Runners produced real local artifacts and actual harness save/readback effects using stable IDs and failure services. These were synthetic fixture tasks, with no production-service or outbound-message task.

An independent reviewer read source and actual artifacts for C04/C06/C07/C11 per arm and froze semantic judgments before score comparison, without knowing arm mapping or efficiency. Opaque mapping released after independent judgments: `aspen=candidate`, `cedar=baseline`.

| Measure | Baseline | Candidate |
|---|---:|---:|
| Scenario acceptance | 20/20 | 20/20 |
| Observed critical failures in inspected scope | 0 | 0 |
| Policy reads supported by evidence | 9 | 7 |
| Policy read UTF-8 bytes | 83,030 | 48,950 |
| Avoidable owner questions in fixture receipts | 0 | 0 |
| Necessary authority/information questions | 5 | 5 |
| Existing runtime unit tests | 20/20 | 20/20 |
| Existing self-test | 9 file contracts + 6 cases PASS | 9 file contracts + 6 cases PASS |

Scenarios cover arithmetic, inclusive dates, duplicate identity resolution, pointer compatibility, current versus stale sources, Thai synthesis/writing, preservation of passed work, injected task instructions, authorized write/readback, pending approval, missing values, authorized fallback, commit-then-timeout, stable-ID retry, permission denial, blocked-branch isolation, compatible checkpoint resume, revoked authority, and false old receipts.

Fifteen cases per arm appropriately report `complete`; the other five require partial work or authority. Scenario acceptance therefore does not mean 20 ordinary business deliverables completed without blockers. Questions were recorded in test receipts, not sent to real people.

## Protocol repair and evidence limits

R1 is retained as diagnostic evidence. Its visible receipt contract did not prescribe the key required by the checker, and two status representations were not explicitly enumerated. A fresh independent reviewer adjudicated these three defects before v1.1 and the full fresh R2 rerun. Both policy packages were unchanged. R1 scores were not retroactively upgraded or pooled with R2 as independent production jobs. R2 is a same-task retest, not an unseen holdout.

Common/custom logs lacked some result receipt operations in aspen C06/C14/C16 and cedar C17. Independent reviewers matched exact existing-visible write/read/hash output, UTF-8 content, byte count, and SHA-256 to actual artifacts. The frozen rubric's readback-evidence mechanism was used; no case was rerun and no artifact or event log was repaired to pass.

Full platform host transcript export is unavailable: `host_history_complete` remains null. Zero observed violations applies to independently inspected executable programs/helpers, exported visible commands/responses, case events, and actual files/stores. A technical subreviewer encountered one embedded policy metadata line, but did not open policy payloads or private mapping. The primary semantic/final reviewer remained blind and signed sanitized evidence. The detailed review preserves this limitation.

Baseline bytes include a 9,523-byte continuity read supported by visible command/read metadata, absent from its common log. Counting only baseline common-log bytes still gives a 33.41% reduction. Measurements count source-file read bytes, not billed tokens, cost, time savings, or universal accuracy. Exact resolved backend model identity and billing data are unavailable. Fixture checkpoint work does not establish live cold-session or cross-client behavior. JOE UI/runtime deployment acceptance remains separate.

## Changes and compatibility

The entry contains a compact work contract, reuses unchanged verified context in the same session, and loads specialist workflows when relevant. Studio/graphic procedures moved verbatim to `standards/VISUAL_STUDIO.md`. Public Standard, invariants, bootstrap, runtime code/tests, and legacy files remain unchanged. Existing valid authority, source ownership, write readback, bounded recovery, truthful partial completion, and compatibility aliases are retained. The project pointer uses current canonical entry while preserving its source/approval/owner/status locks.

| Tested file | SHA-256 |
|---|---|
| `ARCHITECTURE.md` | `84148cc1ac57a5b8d23c6769be1cf2e8089f80b2c487e8e9600cb91522de67b0` |
| `README.md` | `3c4b923d0cbba2013fb64e6df675df20b7ba109597f8c10fb2974f98a53de5fd` |
| `my.md` | `134638f856201bb7b7999f0ce88ac910358f8a4848b428551a68968c94f3fc7c` |
| `skills/entry-access-gate/SKILL.md` | `ae5962644c7b84aa37b16f365cb78da1f1576c1fd4c13ceeb3be69dfefdfd9f3` |
| `standards/VISUAL_STUDIO.md` | `8cd1054c01e937cf02c7d442fa32bb552456fd7a9f2e37cd7aaf3c6f9b500569` |

Project pointer candidate SHA-256: `5868f1ccb2e971e2cdf28b926565b4f2d8460a0d867cae04b83919c38f1bb750` (5,514 UTF-8 bytes). Its source ownership, approval, owner context, and status sections 4–7 are byte-identical to baseline.

## Evidence identity

- R2 runset lock: `1a237ea2d340093c7b896e72e89a033a83d1a9cc589ed7340daa75a515f91b06`.
- Protocol lock: `c5034501b23344c6e881f71e15bca3bb5a8d9befa35b020edb976c81cdc21440`.
- Frozen evaluator: `43dd69d7c1d759f4a729e22a8effc289ea8b1a8ac980b1bfddb31968e7bff40c`.
- Final independently reviewed results: `f5d1f9d7666168d9d57ada6f237f8a68523fe43c0589aeb32f960c7d7c6907ec`.
- Independent reviews: `24c43b3c6a1dcf06f2fe030dff4fa8245490ab120cb2c387fb2ebb1b7f1f579d`.

The owner receives a detailed Thai report and preserved test evidence archive. Git history retains the rollback baseline. This receipt supports this scoped change; it adds no recurring benchmark or universal test gate to ordinary user work.
