# VLM-UNSEEN-SOURCE-STRATIFIED-018 — three new recorded sources, three fixed 12-frame baselines

2026-10-16 (Asia/Shanghai). **THREE_SOURCE_THREE_ARM_EXPLORATION_COMPLETE / CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**. Main safely synchronized to `83947f8ef9728a6bef3343995c1137837167fc12`; unique READY and no prior formal018 result. The current user explicitly authorized at most 315 local Qwen generates, 2400 cumulative GPU-stage seconds, 20GiB peak PyTorch allocated and 5400 parent seconds, conditional on CPU qualification. No 017 budget was reused.

## CPU qualification and frozen denominators

All three exact, previously supplied official-CLI destinations were ordinary non-reparse files. Every source was rechecked in this round; full local SHA continuity matched the earlier private CPU acceptance, and size/mtime remained unchanged. UID, annotated source, recorded origin group, release-1 flag, canonical validation and official v1/full_scale location matched the existing authorized metadata and each newly obtained local manifest. The three recorded groups differ from one another and from the five already observed sources. No directory search or remote request was used.

| Source | Bytes | Video / container seconds | Video packets to EOF / declared frames | Bounded decoded start+middle+tail | Final N / exclusions |
|---|---|---|---|---|---|
| R4 | 8150914484 | 3720.433 / 3720.433 | 111613 / 111613 | 24+83+178 | 36 / 0 |
| R5 | 1760903980 | 3585.400 / 3585.432 | 107562 / 107562 | 24+59+120 | 35 / 0 |
| R6 | 12220330569 | 3507.300 / 3507.300 | 105219 / 105219 | 24+124+181 | 34 / 0 |

All video streams are VP9/yuv420p at 30fps; R4/R5 are 1920×1440 and R6 is 2560×1920. Every demux reached EOF; missing/non-increasing PTS/DTS and corrupt-packet flags were 0. Bounded pixel decode reached the actual final packet PTS in each tail window without errors. This is not a decode of every frame or official remote byte certification. R5 video3585.400s versus container3585.432s is already represented in canonical video/MP4 metadata; no offset was invented.

The exact 013/014/017 nongold exclusion and gold-encoding functions were reused byte-for-byte. All 36/35/34 source questions have five nonempty options and valid canonical A–E encodings; image-task, external-asset, auxiliary-image, schema and gold-encoding exclusions were 0. The CPU qualification process validated label forms and then exited. Before any GPU operation, nongold inference inputs, source PTS bounds, final N, and the full ordinal-based queue were frozen. Only ordinal/question/five options enter inference; no answer labels, canary or annotation timestamps enter selection or prompts.

Release-1/UID/canonical-duration metadata match: **PASS**. Independent immutable release-byte identity, original crop origin, exact annotation-zero-to-media-PTS bridge and strict physical-capture independence: **UNKNOWN**. Canonical PTS field agreement is not an independently certified annotation clock. All scores remain **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED** and are not official HourVideo leaderboard results.

## Frozen controls and execution

A=original Uniform12; B=original question-only SigLIP global top12; C=the same 48 chronologically ordered real-PTS candidates split into 12 consecutive disjoint four-index bins, highest identical question-only cosine per bin, ties to lower original index. All selected IDs are unique and chronologically ordered. Original 48-candidate PTS sampling and original A/B selection were retained. B/C share one image-feature and question-text pass. No option text, label, relevant timestamp or old outcome is used for retrieval.

Same existing Qwen3-VL-4B BF16, SigLIP F32, local processors, SDPA, original five-option/system prompt, seed19, `do_sample=False`, `max_new_tokens=64`, source metadata and no extra frame sampling. Model input construction was AST-identical to 017. Ordinal%3 rotates ABC/BCA/CAB before generation. Every one of 315 calls realized 12 actual source frames, grid[6,12,18] and 324 visual tokens; selected timestamp tokens may differ. The original 14 protocol tests plus 7 new C/tie/queue/denominator tests passed; the owned-child timeout guard passed.

All model loads were offline/local safetensors with trust_remote_code=False. Inference audit hooks denied networking and opens of original gold annotation entries. The project global OS file lock was held through all generation; cooperative RTX3090 and 018 mutexes were held by each source worker. Two fresh telemetry gates per source required free≥8192MiB and utilization≤30%. Durable fsync ledgers reserved each call before generate. Per-process allocator fraction capped 20GiB; guards and the owned-child supervisor enforced cumulative GPU and parent deadlines. No other process or lockfile was killed/deleted.

After all generation children exited and a durable all-terminated marker was written, one separate CPU scorer opened gold and verified input/media hashes, original questions/options, frozen queue, raw-reply strict parsing, ledger order, all selections/ties, token/grid equality and exact count arithmetic. No model output was retried, repaired, selectively removed or regenerated.

## Provisional nominal-clock accuracy

| Source | Arm | Correct/N | Accuracy | Valid wrong | INVALID | NOT_RUN | Returned |
|---|---|---|---|---|---|---|---|
| R4 | A | 13/36 | 36.11% | 18 | 5 | 0 | 36/36 |
| R4 | B | 15/36 | 41.67% | 20 | 1 | 0 | 36/36 |
| R4 | C | 10/36 | 27.78% | 21 | 5 | 0 | 36/36 |
| R5 | A | 11/35 | 31.43% | 20 | 4 | 0 | 35/35 |
| R5 | B | 12/35 | 34.29% | 16 | 7 | 0 | 35/35 |
| R5 | C | 11/35 | 31.43% | 17 | 7 | 0 | 35/35 |
| R6 | A | 8/34 | 23.53% | 23 | 3 | 0 | 34/34 |
| R6 | B | 9/34 | 26.47% | 22 | 3 | 0 | 34/34 |
| R6 | C | 11/34 | 32.35% | 19 | 4 | 0 | 34/34 |

Paired cells below are ordered **both correct / first-only correct / second-only correct / neither correct**. Invalid and missing outputs remain in their full frozen denominators and count as not correct.

| Source | A/B paired | B/C paired | A/C paired | B−A pp | C−B pp | C−A pp |
|---|---|---|---|---|---|---|
| R4 | 10 / 3 / 5 / 18 | 9 / 6 / 1 / 20 | 7 / 6 / 3 / 20 | +5.56 | -13.89 | -8.33 |
| R5 | 6 / 5 / 6 / 18 | 8 / 4 / 3 / 20 | 9 / 2 / 2 / 22 | +2.86 | -2.86 | +0.00 |
| R6 | 7 / 1 / 2 / 24 | 9 / 0 / 2 / 23 | 7 / 1 / 4 / 22 | +2.94 | +5.88 | +8.82 |

Equal-recorded-source descriptive means: A 30.36%, B 34.14%, C 30.52%. B minus A +3.78pp (exact fractional accuracy difference 608/16065); C minus B -3.62pp (exact fractional accuracy difference -2327/64260); C minus A +0.16pp (exact fractional accuracy difference 1/612). No question-pooled old/new score, p-value, significance or population-generalization claim.

In these three new recorded groups B−A was positive in 3/3, whereas C−B was negative in 2/3 and positive in 1/3. C increased measured temporal-bin coverage but did not produce a consistent accuracy improvement over B; its equal-source accuracy was near A. This is a descriptive outcome of this fixed three-source experiment, not proof that coverage causes errors or that any method has a stable population advantage.

## Time coverage and selected-frame overlap

| Source | Arm | PTS span min / mean / max (s) | Occupied index-bins min / mean / max (of12) | Occupied normalized-time bins min / mean / max (of12) |
|---|---|---|---|---|
| R4 | A | 3720.300 / 3720.300 / 3720.300 | 12 / 12.000 / 12 | 12 / 12.000 / 12 |
| R4 | B | 2216.367 / 3109.059 / 3641.167 | 5 / 7.722 / 10 | 5 / 7.722 / 10 |
| R4 | C | 3324.533 / 3500.434 / 3720.300 | 12 / 12.000 / 12 | 12 / 12.000 / 12 |
| R5 | A | 3585.267 / 3585.267 / 3585.267 | 12 / 12.000 / 12 | 12 / 12.000 / 12 |
| R5 | B | 1449.367 / 3003.351 / 3585.267 | 4 / 7.343 / 10 | 4 / 7.343 / 10 |
| R5 | C | 3280.167 / 3454.504 / 3585.267 | 12 / 12.000 / 12 | 12 / 12.000 / 12 |
| R6 | A | 3507.167 / 3507.167 / 3507.167 | 12 / 12.000 / 12 | 12 / 12.000 / 12 |
| R6 | B | 1417.800 / 2864.112 / 3357.933 | 5 / 7.382 / 9 | 5 / 7.382 / 9 |
| R6 | C | 3059.467 / 3241.607 / 3357.933 | 12 / 12.000 / 12 | 12 / 12.000 / 12 |

| Source | Pair | Shared frames min / mean / max (of12) | Mean Jaccard |
|---|---|---|---|
| R4 | A_B | 1 / 2.806 / 6 | 0.137 |
| R4 | B_C | 5 / 7.722 / 10 | 0.482 |
| R4 | A_C | 0 / 2.667 / 7 | 0.134 |
| R5 | A_B | 1 / 3.029 / 4 | 0.147 |
| R5 | B_C | 4 / 7.343 / 10 | 0.451 |
| R5 | A_C | 1 / 2.400 / 4 | 0.114 |
| R6 | A_B | 1 / 2.882 / 5 | 0.139 |
| R6 | B_C | 5 / 7.382 / 9 | 0.449 |
| R6 | A_C | 0 / 2.676 / 6 | 0.131 |

Index-bin coverage is enforced by C by construction. Normalized-time coverage uses 12 equal-width bins over the actual candidate PTS span; it is measured separately. Any coverage improvement is an input-policy property; these aggregate accuracy differences do not establish a causal error mechanism.

## Measured cost and resource accounting

| Source | 48-candidate CPU decode s / actual decoded frames | SigLIP load / shared features s | Cosine / B selection / C selection s | Qwen load s | GPU stage s | Peak allocated / reserved MiB |
|---|---|---|---|---|---|---|
| R4 | 21.578 / 3084 | 0.578 / 1.375 | 0.000 / 0.000 / 0.000 | 4.610 | 53.328 | 8864.785 / 9328.000 |
| R5 | 7.969 / 2867 | 0.532 / 1.312 | 0.000 / 0.000 / 0.000 | 4.328 | 52.203 | 8883.848 / 9216.000 |
| R6 | 32.484 / 2652 | 0.531 / 1.750 | 0.000 / 0.000 / 0.000 | 4.313 | 61.813 | 8968.505 / 9212.000 |

| Source | Arm | Processor total s | Generate total s | Generated tokens min / max | Input tokens min / max | Natural EOS / returns |
|---|---|---|---|---|---|---|
| R4 | A | 5.876 | 9.793 | 2 / 11 | 459 / 638 | 36 / 36 |
| R4 | B | 5.718 | 8.094 | 2 / 11 | 460 / 639 | 36 / 36 |
| R4 | C | 5.765 | 8.840 | 2 / 9 | 459 / 638 | 36 / 36 |
| R5 | A | 5.532 | 9.048 | 2 / 10 | 462 / 659 | 35 / 35 |
| R5 | B | 5.534 | 9.438 | 2 / 10 | 462 / 658 | 35 / 35 |
| R5 | C | 5.452 | 9.283 | 2 / 10 | 462 / 659 | 35 / 35 |
| R6 | A | 8.735 | 9.122 | 2 / 12 | 459 / 760 | 34 / 34 |
| R6 | B | 8.751 | 8.625 | 2 / 12 | 460 / 761 | 34 / 34 |
| R6 | C | 8.707 | 8.763 | 2 / 12 | 459 / 760 | 34 / 34 |

| Source | Resource gate free MiB (two snapshots) | Utilization % (two snapshots) | SigLIP image / text batches | Worker wall s |
|---|---|---|---|---|
| R4 | 22957 / 22957 | 12 / 12 | 6 / 5 | 107.672 |
| R5 | 22956 / 22956 | 11 / 12 | 6 / 5 | 93.687 |
| R6 | 22955 / 22955 | 11 / 13 | 6 / 5 | 104.453 |

**Shared deployment accounting:** candidate extraction and Qwen loading are common execution costs; SigLIP loading, 48-image features, all question-text embeddings and cosine scores are incurred once jointly for B/C. B adds global sorting and C adds per-bin selection, followed by their separate Qwen/processor costs. **Independent single-strategy accounting:** either B alone or C alone must pay the full SigLIP load+image/text-feature+cosine cost, its own selector and its own Qwen/processor costs; neither gets retrieval for free. Do not double-charge shared forwards in this experiment or omit them in standalone deployment comparisons.

Very short cosine/selector intervals logged as 0.000s are below the worker clock/timing resolution, not proof of zero cost. Stage times are wall-clock measurements with CUDA synchronization where applicable, not exclusive kernel utilization. GPU-stage totals conservatively include loads, retrieval, processor/logging and generation while that phase is active. Peak allocated/reserved are source-process peaks, not arm-attributable incremental measurements.

Total **315 attempts /315 returns**; natural EOS 315/315, cap-without-EOS 0. Worker GPU-stage sum **167.344s**; supervisor charged **167.344s** ≤2400s. Maximum allocated **8968.505MiB (8.758GiB)** ≤20GiB. Conservative parent elapsed at verification **856.77s** ≤5400s, including an initial300s sync allowance. No actual OOM, timeout, failed generate or worker kill occurred.

## Scientific interpretation and publication boundary

These are three newly evaluated recorded source groups under a frozen comparison of existing baselines. C was designed after observing earlier sources and tested only on the unseen R4–R6 roster; that design history is retained. Results do not certify physical capture independence, release/crop/annotation clock equivalence, gold semantic correctness, stable superiority, official leaderboard performance or new algorithmic novelty. **NOVELTY=RETAIN0; CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; Charades FINAL_MEDIA_STOP.**

Research downloads/network, dependency/environment changes, training/gradient updates and old013–017 inference reruns: **0**. Public changes are only this anonymous receipt plus one formal018 result append. No private UID/source map/path, QA, gold, prediction text, raw source PTS, hash, image/video or model file is published. One ordinary main push, then STOP; unused budget grants no further work.
