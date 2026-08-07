---
name: audio-runtime
description: Build, revise, synchronize, quality-check, and release LMS narration/audio through a deterministic code-driven pipeline. Use for TTS, voiceover, narration, pronunciation, SSML, audio-video sync, subtitles, audio mixing, batch regeneration, or audio QC under Mindway.
version: 1.0.0
status: REVIEW_READY
---

# Mindway Audio Runtime v1

## Purpose

Audio Runtime treats narration as a compiled artifact rather than a one-off recording or an opaque AI generation.

Core principles:

- Deterministic where technically possible.
- Code-driven and source-controlled.
- Evidence-first.
- Strict QC before release.
- Incremental and cache-aware.
- Reversible and traceable.
- Engine-agnostic.
- Human review by exception, not by default.
- Compatible with Graphic Runtime and a future shared Mindway Content Runtime.

Default mental model:

`Verified knowledge/script source -> Speech IR -> phonetic/prosody compiler -> TTS routing -> audio processing -> QC -> timeline alignment -> mix -> signed build artifact`

Generated WAV/MP3 files are build artifacts, not source of truth.

## When to use

Use this skill whenever work includes one or more of the following:

- LMS narration or voiceover.
- TTS generation or regeneration.
- Thai/English mixed narration.
- Dental or clinical pronunciation.
- SSML or prosody control.
- Audio/video synchronization.
- Subtitle timing generated from narration.
- Batch generation of many lessons or scenes.
- Audio loudness, clipping, silence, intelligibility, or quality checks.
- Background music/SFX mixing.
- Voice consistency or engine comparison.
- Updating one sentence without rebuilding unrelated audio.
- Releasing, rolling back, or tracing an audio artifact.

Do not use this skill to invent clinical/business facts. The narration source must come from a verified source or clearly marked draft.

## Output status

Use only these task statuses:

- `DONE`
- `REVIEW_READY`
- `NEED_CONFIRM`
- `BLOCKED`

Audio production should normally stop at `REVIEW_READY` until required human/business/clinical approval is satisfied.

# 1. Source of Truth

## 1.1 Never make MP3/WAV the SSOT

The persistent source should be structured text and configuration.

Preferred hierarchy:

1. Knowledge/fact source.
2. Stable semantic line/scene IDs.
3. Narration text.
4. Spoken normalization.
5. Pronunciation/prosody metadata.
6. Timeline constraints.
7. Mix/output profile.

Recommended source file:

`lesson.audio.json`

Example:

```json
{
  "lesson_id": "M14-S03",
  "language": "th-TH",
  "voice_profile": "lms_th_clear_v1",
  "segments": [
    {
      "id": "M14.S03.SC04.L002",
      "source_text": "ตรวจสอบ Radiograph ก่อนเริ่มการรักษา",
      "spoken_text": "ตรวจสอบ เรดิ โอ กราฟ ก่อนเริ่มการรักษา",
      "intent": "instruction",
      "timing": {
        "preferred_sec": 4.2,
        "min_sec": 3.8,
        "max_sec": 4.8
      }
    }
  ]
}
```

Stable IDs must survive wording edits whenever the semantic unit remains the same.

# 2. Speech Intermediate Representation (Speech IR)

Do not bind the master source directly to one TTS vendor's SSML dialect.

Compile natural narration into a vendor-neutral Speech IR first.

Example:

```json
{
  "id": "M14.S03.SC04.L002",
  "tokens": [
    {"type": "speech", "text": "ตรวจสอบ"},
    {
      "type": "term",
      "term_id": "DENT_RADIOGRAPH",
      "surface": "Radiograph",
      "pronunciation": "เร-ดิ-โอ-กราฟ"
    },
    {"type": "pause", "ms": 150},
    {"type": "speech", "text": "ก่อนเริ่มการรักษา"}
  ],
  "intent": "instruction",
  "pace": 0.94,
  "emphasis": []
}
```

Then compile Speech IR to the chosen engine format:

`Speech IR -> Azure SSML`

`Speech IR -> Edge-TTS input`

`Speech IR -> ElevenLabs configuration`

`Speech IR -> local phoneme/model input`

This protects Mindway from vendor lock-in.

# 3. Phonetic Compiler

## 3.1 Dental Pronunciation Lexicon

Maintain a versioned pronunciation registry for terminology, abbreviations, names, numbers, and mixed-language phrases.

Example:

```yaml
DENT_ENDODONTICS:
  written: Endodontics
  spoken_th: เอน-โด-ดอน-ติกส์
  status: locked

DENT_RADIOGRAPH:
  written: Radiograph
  spoken_th: เร-ดิ-โอ-กราฟ
  status: locked

ABBR_CSSD:
  written: CSSD
  spoken_th: ซี-เอส-เอส-ดี
  status: locked
```

A human-approved pronunciation should become `locked` and must not silently change because an AI or engine has a different preference.

## 3.2 Semantic normalization

Normalize ambiguous tokens before synthesis.

Examples:

- `40%` -> `สี่สิบเปอร์เซ็นต์`
- `M18` -> the approved spoken form.
- `DF` -> approved abbreviation pronunciation.
- Dates, branch codes, dental numbers, units, prices, and ranges -> approved spoken form.

Do not assume that visible text and spoken text must be identical.

## 3.3 Context-aware pronunciation

Pronunciation may depend on context.

The lexicon may contain profiles such as:

- Thai-accent clinical English.
- Native-English phrase.
- Letter-by-letter abbreviation.
- Dental noun usage.
- Brand/product-specific approved pronunciation.

# 4. Prosody as Code

Prosody must be represented as reusable semantics, not repeated prompt prose.

Suggested semantic tokens:

- `NORMAL`
- `INSTRUCTION`
- `CAUTION`
- `CLINICAL_CAUTION`
- `TRANSITION`
- `KEY_TERM`
- `SUMMARY`
- `QUESTION`

Example policy:

```yaml
CLINICAL_CAUTION:
  rate: 0.90
  pause_before_ms: 180
  pause_after_ms: 300
  emphasis: medium
  music_duck_db: -4
```

Graphic Runtime, Audio Runtime, subtitles, and motion may consume the same semantic event.

# 5. TTS Engine Routing

Do not hard-code the runtime to a single engine.

## 5.1 Routing layers

Preferred routing model:

1. Local/private-capable engine when quality and language support are sufficient.
2. Approved cloud neural voice when higher naturalness is needed.
3. Alternative engine for difficult segments.
4. Human-recorded or approved golden phrase for critical wording when appropriate.

Possible engines include Edge-TTS, Azure Neural Voice, ElevenLabs, Piper, Kokoro, or other local/cloud engines that satisfy the current task.

Engine availability changes over time; verify the actual environment before claiming an engine is usable.

## 5.2 Privacy-aware routing

Before sending content to a cloud engine, classify whether the segment contains sensitive, private, personal, patient, employee, credential, or company-confidential information.

Sensitive material must not be sent to an external service without explicit permission and an allowed data-processing path.

## 5.3 N-version synthesis for risky segments

For difficult/high-risk sentences, synthesize candidates with more than one approved engine and compare them through QC.

Do not spend this cost on every ordinary sentence.

Typical trigger:

- Many specialist terms.
- Mixed Thai/English.
- Names or brands.
- Prior pronunciation failures.
- High-importance safety wording.

# 6. Deterministic Build and Audio Lockfile

Record every material build dependency.

Recommended `audio.lock`:

```yaml
build_id: M14-S03-audio-v18
script_hash: sha256:...
lexicon_hash: sha256:...
speech_ir_hash: sha256:...
engine: azure
voice: th-TH-PremwadeeNeural
engine_config_hash: sha256:...
processor: ffmpeg
processor_version: recorded-at-build
sample_rate: 48000
channels: 1
delivery_lufs: -16
true_peak_ceiling_dbtp: -1.0
```

Important: identical source does not guarantee bit-identical audio from every cloud TTS engine because providers may update models. Therefore record the environment and run regression checks rather than falsely claiming perfect bit-level determinism.

# 7. Content-Addressed Incremental Build

Hash each semantic segment and its material dependencies.

Segment cache key should include at minimum:

- spoken text.
- pronunciation entries used.
- prosody.
- voice/engine configuration.
- processing profile.

If the key is unchanged, reuse the approved cached segment.

Example:

```text
43 segments
41 cache hits
2 regenerated
```

Changing one sentence should not force unrelated narration to regenerate.

# 8. Timeline Compiler

Audio and graphics should ideally consume one shared scene timeline instead of forcing one medium to fit the other after production.

Preferred model:

```text
Content / Scene IR
        |
Timeline Constraint Solver
   |              |
Graphic Runtime   Audio Runtime
```

Each scene can define:

- minimum duration.
- preferred duration.
- maximum duration.
- semantic transition rules.

## 8.1 Constraint order

When generated speech does not match the preferred scene duration, prefer this order:

1. Use available scene elasticity.
2. Adjust natural punctuation/pause placement.
3. Regenerate with a slightly different approved pace.
4. Apply pitch-preserved time stretching within a safe budget.
5. Mark warning/review if the constraint cannot be satisfied naturally.

Do not automatically distort narration just to preserve an arbitrary visual duration.

Suggested stretch policy:

- up to +/-3%: may auto-process if QC passes.
- 3-6%: warning and quality check.
- above 6%: prefer regenerate or change timeline; do not silently accept.

The thresholds are Mindway operating defaults, not universal psychoacoustic standards, and may be tuned from evidence.

# 9. Audio Processing

Use deterministic command-line or code-driven processing where practical.

Typical tools:

- FFmpeg for format conversion, loudness analysis/normalization, mixing, silence detection, clipping/peak checks, muxing.
- Rubber Band, SoundTouch, SoX, or equivalent for time/pitch operations when required.

Record tool versions in the build manifest when reproducibility matters.

# 10. Loudness and Acoustic Policy

Do not incorrectly state that EBU R128 equals `-16 LUFS`.

Use EBU R128 / ITU-R BS.1770 compatible measurement where available.

Mindway may define a delivery profile such as:

```text
Measurement framework: R128 / BS.1770-compatible
LMS delivery target: -16 LUFS integrated
True peak ceiling: -1 dBTP
```

Treat these as Mindway delivery targets unless a destination platform specifies otherwise.

# 11. QC Gate

Never equate one metric with overall correctness.

Audio QC must evaluate at least three independent dimensions:

1. Content correctness.
2. Pronunciation correctness.
3. Acoustic/listening quality.

Add timing and release integrity as separate gates when producing synchronized media.

## 11.1 Content QC

Use ASR readback as supporting evidence, not as proof that pronunciation is correct.

Normalize ASR and source text before comparison where appropriate.

Do not use a fixed `98%` threshold blindly across all models/languages. Thresholds must be calibrated from actual error behavior.

## 11.2 Pronunciation QC

Use one or more of:

- approved lexicon checks.
- phoneme/phone alignment.
- forced alignment.
- pronunciation unit tests.
- human review for uncertain terms.

A transcript may be correct while pronunciation is still wrong.

## 11.3 Acoustic QC

Check as relevant:

- integrated loudness.
- true peak.
- clipping.
- unexpected silence.
- excessive background noise.
- duration.
- channel/sample-rate consistency.
- abrupt edits/clicks.
- speech/background intelligibility.

## 11.4 Timing QC

Check:

- actual duration against scene constraints.
- segment start/end alignment.
- subtitle timing.
- no blank/late narration state.
- A/V synchronization.

# 12. Pronunciation Unit Tests

Maintain regression tests for approved specialist terms.

Example:

```text
TEST-DENT-001
Input: Endodontics
Expected pronunciation: เอน-โด-ดอน-ติกส์

TEST-DENT-002
Input: CSSD
Expected pronunciation: ซี-เอส-เอส-ดี
```

When a real failure is corrected, consider adding it as a permanent regression test.

Goal: the system should learn from failures instead of merely reporting them repeatedly.

# 13. Audio Invariants / Property Tests

Define conditions that must never silently pass.

Example invariants:

- no unresolved English/technical token that requires lexicon handling.
- no unexpected raw numeric token when spoken normalization is required.
- no clipping above the configured ceiling.
- no unexplained silence above the configured limit.
- no unauthorized engine fallback.
- no unknown voice profile.
- no missing stable segment ID.
- no release artifact without manifest/hash.

# 14. Voice Consistency and Drift

Where technically feasible, monitor voice consistency across batches or long-form narration.

Possible evidence:

- speaker embedding similarity.
- pitch/rate distribution.
- spectral characteristics.
- regression against approved canary phrases.

Do not call voice identity drift proven from one weak metric. Use it as a warning signal for review.

# 15. Voice Canary Suite

Before adopting a new model/voice/version, synthesize a stable reference suite containing:

- Thai conversational sentences.
- dental terminology.
- abbreviations.
- mixed Thai/English.
- numbers and units.
- caution wording.
- long and short sentences.

Compare against the approved baseline before promoting the new voice to production.

# 16. Golden Phrase Library

Critical or frequently reused phrases may be stored as approved reusable audio components.

Prefer semantic phrases rather than isolated syllables to preserve natural coarticulation/prosody.

Each golden phrase must include:

- stable phrase ID.
- approved text.
- pronunciation/profile.
- voice identity.
- source/build metadata.
- approval status.

Do not silently splice a golden phrase into a voice/profile that sounds materially inconsistent.

# 17. Subtitle Runtime

Subtitle text must be anchored to the verified textual source, not authored from ASR output.

Preferred flow:

`Verified text -> alignment against audio -> timestamps -> SRT/VTT`

ASR may help alignment/QC but must not silently rewrite the official subtitle wording.

# 18. Programmatic Mixing

Use a deterministic mixing graph where practical.

Logical tracks:

1. Narration.
2. Background music.
3. Sound effects/semantic cues.

Music ducking should react to narration and intelligibility requirements rather than relying only on one fixed gain value.

For LMS/mobile use, prioritize speech intelligibility over cinematic impact.

# 19. Responsive Audio Profiles

When useful, compile multiple delivery profiles from the same source:

- Standard.
- Clear learning / slower.
- Focus / no music.
- Review / faster.
- Mobile-speaker optimized.
- Low-bandwidth mono.

These are derived artifacts. Do not fork the knowledge source merely to make another listening profile.

# 20. Process Drift Monitoring

For large-scale production, track process metrics across builds, not just per-file pass/fail.

Possible metrics:

- speaking rate.
- average/variance of pause duration.
- loudness.
- pitch distribution.
- ASR content score.
- pronunciation failure count.
- voice similarity.
- regeneration rate.
- cache hit rate.

If the process starts drifting while individual clips still appear to pass, flag a warning before widespread degradation occurs.

# 21. Artifact Manifest / Audio BOM

Every release candidate should be traceable to its ingredients.

Recommended `audio-manifest.json`:

```json
{
  "artifact": "M14-S03.mp3",
  "build_id": "M14-S03-audio-v18",
  "script_hash": "...",
  "speech_ir_hash": "...",
  "lexicon_hash": "...",
  "engine": "...",
  "voice": "...",
  "music_assets": [],
  "sfx_assets": [],
  "processor": "ffmpeg",
  "qc_report": "qc.json",
  "artifact_sha256": "..."
}
```

Never release an artifact that cannot be mapped back to the build/source used to create it.

# 22. Release and Rollback

Separate build from release.

Preferred states:

```text
SOURCE
-> BUILD
-> QC
-> REVIEW_READY
-> APPROVED RELEASE
```

Keep the previous approved artifact available for rollback when feasible.

Do not overwrite the only known-good release with an unreviewed build.

# 23. Exception-Only Human Review

Human attention should focus on uncertain or risky segments.

Example:

```text
200 clips
191 automatic PASS
6 WARNING
3 FAIL
-> human reviews 9 clips
```

Escalate segments based on evidence such as:

- pronunciation uncertainty.
- engine disagreement.
- previous failure history.
- abnormal process metrics.
- sensitive/clinical wording.
- excessive timing correction.

# 24. Failure Memory

A corrected production failure should produce one or more durable improvements when justified:

- lexicon update.
- pronunciation test.
- invariant.
- canary sentence.
- routing rule.
- timeline rule.
- QC threshold recalibration.

Avoid storing duplicate noise. Capture only learning that prevents recurrence or improves future builds.

# 25. Integration with Graphic Runtime

Audio Runtime and Graphic Runtime should not independently invent their own scene timing or semantic structure.

Preferred shared source direction:

```text
Mindway Content Runtime
        |
Knowledge / Semantic Scene IR
        |
   +----+----+---------+------+
   |         |         |      |
Graphic    Audio    Subtitle  Quiz
Runtime    Runtime   Runtime  Runtime
   |         |         |      |
   +---------+---------+------+
        Runtime QC
        |
   Release Manifest
```

When a source fact changes, downstream outputs should be marked stale or rebuilt according to dependencies.

# 26. Default Build Workflow

For non-trivial LMS audio work:

1. Identify verified source and stable lesson/scene/line IDs.
2. Separate factual/knowledge content from spoken wording.
3. Normalize numbers, abbreviations, mixed-language terms, and terminology.
4. Resolve pronunciation through the versioned lexicon.
5. Compile to Speech IR.
6. Resolve semantic prosody/timing rules.
7. Calculate a pre-synthesis speech/time budget.
8. Select engine based on language, quality, privacy, cost, and risk.
9. Reuse valid cached segments.
10. Synthesize only changed/missing segments.
11. Run acoustic processing.
12. Run content, pronunciation, acoustic, and timing QC.
13. Align official subtitle text to the actual narration.
14. Mix narration/music/SFX if required.
15. Generate waveform/spectrogram or other diagnostics only when they help QC.
16. Write `audio.lock`, QC report, and artifact manifest.
17. Return exceptions and status.
18. Release only after the required approval gate.

# 27. Build Report Format

Preferred concise report:

```text
AUDIO BUILD: M14-S03

Source integrity      PASS
Speech normalization PASS
Lexicon               PASS
Pronunciation         PASS / WARNING / FAIL
Content readback      PASS / WARNING / FAIL
Acoustic QC           PASS / WARNING / FAIL
Timing                PASS / WARNING / FAIL
Subtitle alignment    PASS / WARNING / FAIL
Artifact integrity    PASS / WARNING / FAIL

Segments: 43
Cache hits: 41
Regenerated: 2
Warnings: 0
Failures: 0

Build ID: M14-S03-audio-v18
Status: REVIEW_READY
```

Do not invent test results that were not actually measured.

# 28. Evidence Rules

- Never claim an audio file was listened to, measured, aligned, synthesized, or QC-checked unless that action actually occurred.
- Never claim a voice/model/API is currently available without verifying when availability matters.
- Never claim `100% pronunciation accuracy` merely because a lexicon exists.
- Never claim deterministic bit-identical output from a nondeterministic/cloud model without evidence.
- Distinguish configured target from measured result.
- Preserve build logs and hashes when traceability matters.

# 29. Tool Selection Rules

Choose the simplest deterministic toolchain capable of the job.

Typical preference:

- Structured source: JSON/YAML/SSML/Speech IR.
- TTS: approved local or cloud engine selected at runtime.
- Audio processing/mixing: FFmpeg first unless another tool provides a material quality advantage.
- Time stretch: pitch-preserving tool when required.
- ASR: local Whisper or suitable alternative for readback evidence where available.
- Forced alignment/phoneme analysis: appropriate local or approved tool when pronunciation risk justifies it.
- Hashing/manifest: standard cryptographic hash (e.g. SHA-256).

Do not add a dependency merely because it is sophisticated. Every dependency must reduce risk, work, cost, or error.

# 30. Improvement Rule

Audio Runtime v1 is not immutable.

When a new technique is found, compare it against current behavior on:

- accuracy.
- intelligibility.
- repeatability.
- speed.
- cost.
- privacy.
- debuggability.
- reproducibility.
- rollback capability.

Propose changes separately before replacing the current production method.

Do not silently rewrite the runtime during an active production build.

# 31. Definition of Done

An Audio Runtime task is complete only when the requested scope has appropriate evidence for:

- source linkage.
- correct build target.
- pronunciation handling.
- audio generation/processing as requested.
- required QC.
- timing/subtitle alignment if relevant.
- manifest/traceability for release-grade artifacts.
- unresolved warnings clearly stated.

For production-grade LMS narration, a generated MP3 alone is not Definition of Done.

# 32. Handoff

End substantial Audio Runtime work with:

- What was built/changed.
- Source/build IDs.
- QC evidence available.
- Warnings/failures.
- What was cached/rebuilt.
- Release status.
- Next action.
