# VLM-HOURVIDEO-NEW-SOURCES-017 — three-source paired exploration

**2026-10-16 (Asia/Shanghai)**. Documentation baseline `421193ba9da92da044d197be8fc0105ad52c8b02`; clean independent checkout safely synchronized, unique READY and no previous formal 017 result verified. The user explicitly authorized this round: at most **232 Qwen generate attempts, 2,400 GPU-stage seconds, 20 GiB peak PyTorch allocated memory and 5,400 seconds for the parent task**, conditional on CPU gates. The earlier R1 supplemental pre-acceptance was not a previous formal 017 execution.

**THREE_RECORDED_NEW_SOURCE_PAIRED_EXPLORATION_COMPLETE.** All three frozen sources passed qualification; final denominators **39 / 39 / 37** were fixed before GPU execution. **230 attempts / 230 successful returns**, no model-output retry, no training. All scores below are **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**, provisional under the prospectively specified `MEDIA_PTS_DIRECT_WHOLE_VIDEO` assumption. **Formal HourVideo leaderboard accuracy, population superiority and publication-level novelty remain NOT_ESTABLISHED.**

## CPU media, source and eligibility gates

Only the three exact authorized MP4 entries and the known dev/release-1 metadata entries were used; no directory scan, new download, old partial-file recovery or replacement candidate was used. Existing official CLI acquisition took place in earlier user-authorized download steps, not in this 017 execution.

R1 reused the [published bounded pre-acceptance](./r1-cpu-preacceptance.md): 83,504 packets to EOF and 218 sampled decoded frames. The same exact entry and expected size were checked; current size/mtime and a new private SHA256 snapshot were frozen and verified again after generation. No new full R1 decode was performed. There was no historical R1 byte-hash certificate to promote into independent release certification. The dev annotation SHA matched the original 013 frozen annotation SHA, supporting reuse of R1's 39-question qualification. The original R1 gold values were not reopened by the new pre-inference eligibility parser.

| Media engineering evidence | R1 | R2 | R3 |
|---|---:|---:|---:|
| Actual local bytes | 606,852,958 | 458,336,512 | 1,162,312,033 |
| Video stream duration, seconds | 2783.466667 | 4396.833333 | 3002.733333 |
| Container duration, seconds | 2783.466667 | 4396.854362 | 3003.262000 |
| Canonical manifest video duration, seconds | 2783.47 | 4396.83 | 3002.73 |
| Annotation/canonical-MP4 duration, seconds | 2783.47 | 4396.83 | 3003.26 |
| Video packet count / declared frames | 83,504 / 83,504, reused | 131,905 / 131,905 | 90,082 / 90,082 |
| Missing or non-increasing packet PTS/DTS | 0, prior evidence | 0 | 0 |
| Corrupt packet flags | 0, prior evidence | 0 | 0 |
| Pre-acceptance pixel-decode frames | 218, prior evidence | 314 | 269 |
| Start/middle/tail decode and tail EOF | Prior PASS reused | PASS | PASS |

R2/R3 packet traversal reached EOF and bounded CPU decode windows succeeded. The measured video duration matched each manifest's **video** duration within about 3.33 ms. R3's approximately 0.53-second container/video difference also exists in the manifest's separate canonical-MP4/video duration fields; no artificial clock offset, crop or extra frame was introduced to erase it. Checks were bounded, not complete pixel decoding or official remote byte-hash verification.

Each current manifest row matched the corresponding 016 release-1 record. Explicit release-1/canonical-validation flags, UID correspondence, declared durations and recorded origin/source groups passed the local checks. R1/R2/R3 have three distinct recorded groups and no recorded match to the two old sample groups. **Strict physical-capture independence, immutable release/crop correspondence and annotation-time-zero to media-PTS certification remain UNKNOWN.** Canonical stream-start correspondence is not an annotation-zero certificate.

The user supplied the exact original 013/014 private implementation directories. Their `protocol.py` files were byte-identical. The original `exclusion`, `canonical_gold`, alternating paired queue and prediction parser were copied without modification; all **14 original protocol tests PASS**, with an additional disposable-owned-child timeout test PASS. R2/R3 label encoding checks occurred only in an isolated CPU qualifier. Only ordinal, question text and five original option strings were copied into the inference inputs: no gold, canary, reference timestamp or source identity field.

| Nongold qualification before inference | R1 | R2 | R3 |
|---|---:|---:|---:|
| Original questions | 39 | 39 | 41 |
| Explicit image-task exclusions | 0 | 0 | 3 |
| Explicit external-resource exclusions | 0 | 0 | 1 |
| Other exclusions | 0 | 0 | 0 |
| **Frozen eligible N per arm** | **39** | **39** | **37** |
| Planned Qwen calls | 78 | 78 | 74 |

The extra external-resource exclusion in R3 explains why its final N is 37 rather than 016's structural upper bound of 38. This decision preceded all model outputs and did not depend on labels or difficulty. No source was held, replaced, reordered or selected by an observed score. Reference-label encoding qualification does not independently establish the semantic correctness of every reference answer.

## Frozen execution and isolation

The original 014 runner's selection, prompt construction, model settings, processor arguments and generation loop were retained. Changes were restricted to 017 identity, each source's frozen N and PTS/frame-count record, the cumulative remaining GPU allowance, instrumentation-only grid/token/selection checks, and an owned parent supervisor. Old 013/014 scripts, logs and ledgers were read-only; no old QA was replayed.

- Same local Qwen3-VL-4B-Instruct BF16 and SigLIP base F32 asset entries and existing shard-size/configuration gates; safetensors, local-only/offline loading, `trust_remote_code=False`, SDPA, eval/inference mode. No installation, quantization change, fine-tuning, gradients or optimizer steps.
- Each source used **48 actual RGB candidates** from its own observed video PTS bounds, retaining the original 0.10-second tail margin. A selected uniform12; B used normalized SigLIP image/question-only text cosine, stable top12 and chronological order. No options, gold or annotation `relevant_timestamps` entered retrieval. Real selected-frame indices/PTS/RGB hashes were retained privately for verification, not published.
- Identical A/B question/options and system instruction: `Choose exactly one answer from A, B, C, D, E. Output only the single letter.` Original processor size arguments, source-video metadata and no extra frame sampling were retained. All calls realized **12 source frames, video grid [6,12,18], 324 video tokens**; runtime grid/token checks passed throughout. Source-derived timestamp tokens can vary with the selected frames; the prompt construction rule was unchanged.
- `do_sample=False`, `max_new_tokens=64`, original seed 19, zero warm-up generates, and original question-order AB/BA alternation. Valid prediction means strip then exactly uppercase A–E with an optional final period; no free-text answer extraction, repair or regeneration.
- The parent held the original workspace global GPU file's nonblocking OS byte lock through all generation, without deleting or resetting it. Each source also held the original cooperative RTX3090 mutex and a 017 task mutex. Two fresh snapshots per source satisfied free VRAM at least 8 GiB and utilization at most 30%; no positively identified conflicting training job was found. Mixed desktop contexts were not mistaken for an empty GPU guarantee.
- Before every generate, the private attempt reservation was appended and fsynced. Single-start markers prevented parent/source replay; ledger tuples matched the exact paired-queue prefix. One supervisor imposed the total 232-attempt/2,400-second budget and a monotonic parent deadline calibrated once from the round start. It could terminate only its own child. No real worker timed out, was killed, failed or retried.
- The inference audit hook rejected network operations and opening either original annotation file. Only after **all three generation children exited** was the termination marker created and the separate scoring process started. It rechecked frozen questions, annotation identity, video size/mtime and full private media SHA256, reparsed the saved replies once, and applied the unchanged aggregation logic. No scorer label was sent back to a model or selector.

## Provisional assumed-clock scores, source by source

**Every score in this section is CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**, under nominal whole-video correspondence; no official HourVideo score is claimed. Invalids and all planned questions remain in each arm's denominator.

| Source | Uniform correct/N | SigLIP correct/N | B−A, percentage points | INVALID A / B | NOT_RUN A / B |
|---|---:|---:|---:|---:|---:|
| R1 | **10/39 (25.64%)** | **14/39 (35.90%)** | **+10.26** | 2 / 3 | 0 / 0 |
| R2 | **5/39 (12.82%)** | **8/39 (20.51%)** | **+7.69** | 5 / 3 | 0 / 0 |
| R3 | **14/37 (37.84%)** | **12/37 (32.43%)** | **−5.41** | 4 / 5 | 0 / 0 |

| Provisional paired correctness cell | R1 | R2 | R3 |
|---|---:|---:|---:|
| Both correct | 9 | 5 | 9 |
| Uniform only correct | 1 | 0 | 5 |
| SigLIP only correct | 5 | 3 | 3 |
| Neither correct, including INVALID | 24 | 31 | 20 |
| Sum / frozen N | 39 | 39 | 37 |

Valid-but-wrong counts A/B were respectively **27/22, 29/28 and 19/20**. All **230/230** returned generations ended naturally with EOS; token-cap-without-EOS, generation failures and NOT_RUN were all zero. Natural EOS did not turn invalid formatting into a correct or valid answer. The invalids above were retained without any output retry.

Under the same **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED** limitation, the prespecified source-equal-weight descriptive means are **Uniform 25.43%, SigLIP 29.61%**, with **B−A = +4.18pp** (exact mean difference 181/4329). There are **two positive source differences and one negative**. These are three recorded source groups, not 115 independent video replicates; exact physical independence remains unverified. No question-pooled overall accuracy, confidence interval, significance claim or combination with old 013/014 scores is reported.

## Actual cost, coverage and resource reconciliation

| Execution/resource metric | R1 | R2 | R3 |
|---|---:|---:|---:|
| Qwen attempts / successful returns | 78 / 78 | 78 / 78 | 74 / 74 |
| GPU-stage wall, seconds | **33.141** | **35.218** | **31.625** |
| Peak allocated, MiB | **9099.487305** | **9043.666992** | **9134.436035** |
| Peak reserved, MiB | 9614 | 9498 | 9508 |
| Entire source worker, seconds | 68.031 | 48.343 | 47.656 |
| Candidate extraction, seconds | 4.032 | 3.188 | 6.109 |
| Actual seek-decoded candidate frames | 2923 | 3107 | 3643 |
| SigLIP load / features, seconds | 0.469 / 0.984 | 0.453 / 0.875 | 0.469 / 0.891 |
| Qwen load, seconds | 3.969 | 3.922 | 3.968 |
| Generate wall sum A / B, seconds | 9.308 / 9.232 | 11.173 / 10.455 | 9.347 / 9.235 |
| Processor wall sum A / B, seconds | 3.438 / 3.424 | 3.281 / 3.248 | 2.936 / 2.954 |
| Common candidate/uniform span, seconds | 2783.333333 | 4396.700000 | 3002.600000 |
| Query span minimum / mean / maximum, seconds | 1184.4 / 2013.466667 / 2664.9 | 2899.933333 / 3969.735043 / 4303.133333 | 1213.833333 / 2362.023423 / 3002.6 |
| Query spans below 1200 seconds | 1 | 0 | 0 |
| Mean uniform/query intersection, frames | 3.128205 | 2.871795 | 3.702703 |
| Mean Jaccard | 0.153458 | 0.138010 | 0.189380 |

The cumulative GPU-stage wall was **99.984 seconds / 2,400-second allowance**. Maximum allocated was **9134.436035 MiB, about 8.92 GiB / 20 GiB allowance**. Actual Qwen calls were **230 / 232**; the unused two calls are not a continuation authorization. SigLIP performed **18 image batches and 15 text batches** over the three sources. Retrieval load/features are charged to B separately; common candidate extraction and model loads are not hidden. GPU-stage wall includes resident CPU preprocessing, not just CUDA kernel time. Allocator peaks are not total physical VRAM measurements.

The one R1 query span below 20 minutes is a retained descriptive outcome of the original selector, not a failed source-duration gate or a reason to change the selection. Coverage, overlap and different errors do not independently identify evidence grounding or explain the score differences causally.

## Verification, interpretation and stop

Post-run independent checks passed for frozen-before-GPU timestamps, unchanged inputs, queue/attempt/completion reconciliation, four-cell totals, wrong/invalid/NOT_RUN denominators, EOS counts, 48 unique ordered candidate times, unique chronological 12-frame selections, original protocol identity, runtime visual grid/token equality and all resource caps. Exact rational arithmetic independently reproduced the per-source differences and source-equal-weight macro. Verification was completed about **965.68 seconds into the 5,400-second parent allowance**, before documentation publication; no further model call was made.

This round establishes successful execution of the frozen paired baseline on three additional recorded sources, with a **positive descriptive macro and heterogeneous per-source directions**. It does not establish stable SigLIP superiority, a new acquisition mechanism, statistical significance, independent population generalization, pure visual grounding or a causal reason for any difference. The unknown immutable release/crop/annotation-zero bridge remains; these are assumption-limited exploratory scores. **NOVELTY=RETAIN0** and Charades **FINAL_MEDIA_STOP** remain.

There were **0 research-network requests, downloads, dependency/environment changes, training updates, old-task reruns or historical experiment/result modifications** in this 017 round. Git documentation coordination is separate. Only this anonymous receipt and one appended formal 017 result are submitted. No identity, private path, question/option, gold, reply body, media/frame, model, private hash or reidentification map is uploaded. After one ordinary main push, **STOP**; no R4–R6 substitution, follow-on experiment or residual-budget use.
