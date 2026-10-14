# VLM-LOCAL-LONGVIDEO-009 — actual local long-video temporal A/B

Date: 2026-10-14 (Asia/Shanghai). Contract main `374d3a1`. The independent clean docs checkout was safely fast-forwarded; latest AGENTS, task board, results, overview,009 contract and frozen public trainer were reread. Unique READY/no prior parent result was confirmed.

**Outcome: LOCAL_LONG_VIDEO_TEMPORAL_AB_EXPLORATORY.** One explicitly authorized local complete long video was actually decoded and used for two RTX3090 temporal-order heads, **100 backward/optimizer updates per arm**. Both arms scored **0.4500** on the same later-block validation pairs: no observed motion-priority advantage in this run.

## Local input, source and read-only checks

Only the user's first exact authorized entry was checked and found; the alternative entry was not inspected. No directory enumeration or search occurred. It was a regular file, not a symlink/reparse entry, and its ancestors passed the reparse check. Private byte size was103,909,467 (99.096 MiB); source size is reported here as the nonidentifying99.096 MiB aggregate. Input EBML signature passed.

Research training use was explicitly authorized by the user for the manually obtained official public-domain film. Source qualification combines this current user attestation with the already documented official structured US Public Domain evidence; no new licensing/network request was made. This is not cryptographic certification that the local file equals an official remote object, or a worldwide legal guarantee. No conflicting license evidence was encountered in the scoped checks. The authorized film input is separate from protected first-person QA assets; no HourVideo/Ego4D media/QA/source map was read, and no formal heldout QA result is claimed. Same-film validation is only internal exploratory validation, not an independent research test set.

Exactly one existing CPU ffprobe invocation returned success without error output: WebM, one VP9 video stream,480p, container duration **1465.597 seconds**. A full PyAV video-stream decode then reached EOF successfully without a caught decode error, with **43,924 actual decoded frames**. This provides local container/decode completeness evidence, not remote whole-object checksum provenance. Private source SHA before/after all operations matched; the digest itself is not published. No media copying, repair, remuxing, rename or modification occurred.

## Real CPU sampling and fixed comparison

CPU decode duration **14.875 s**. Every decoded frame's PTS was present, finite, nonnegative and strictly increasing. The frozen approximately3-second sampling procedure retained **489 real RGB frame features**; sampled span **1465.464 s**, exceeding1,200 s and350 retained samples.

Features: CPU8×8×3 RGB values. Frozen split: first70% timeline for training, final30% for later-block validation, excluding samples within9 seconds on either side of the boundary. Each arm selected128 training frames; common validation selected70 frames and generated exactly the same160 pair presentations with validation generator seed2126. Uniform training span **1015.014 s**; motion-priority training span **1012.011 s**; common validation span **429.429 s**.

Uniform selects evenly spread training candidates. Motion priority ranks adjacent low-resolution RGB absolute change, takes the128 largest with deterministic stable ordering, then restores chronological order. No QA/query relevance, manual label, optical-flow model or selected best seed was introduced. The gap and sampled-pair task remain defined by rank differences, so selected physical-time gaps/visual difficulty can differ between arms even with equal frame/update budgets.

## Hardware/resource gate and true updates

Both the known cooperative and task mutexes were absent and acquired nonblockingly; only owned handles were released. Two RTX3090 observations were separated by≥2.1 seconds:

| Observation | Free memory | GPU utilization |
|---|---:|---:|
| 1 |22,500 MiB|12%|
| 2 |22,501 MiB|12%|

Both passed free≥8 GiB/utilization≤30%. No positively confirmed conflicting heavy training task was found in these scoped checks. Mixed Windows C+G nonemptiness did not block execution. Cooperative locks/snapshots are not a physical exclusivity guarantee.

Existing pytorch/CUDA and real cuda:0 were used. Both arms: same model initialization seed19, training pair generator2026, validation generator2126,384→64→1 head with24,705 trainable parameters, AdamW lr0.002, BCE-with-logits, batch16. Initialization and validation equality follow the frozen code resetting the same seeds and reusing identical validation features; no second model run or new seed selection occurred.

| Actual metric | Uniform128 | Motion128 |
|---|---:|---:|
| Real backward/optimizer updates |**100/100**|**100/100**|
| First sampled-batch loss |0.689918|0.691118|
| Last sampled-batch loss |0.779309|0.732843|
| Parameter absolute-change sum |231.676|200.402|
| Same-film later-block pair accuracy |**0.4500**|**0.4500**|
| Timed arm optimization/evaluation subsection |0.422 s|0.250 s|

All loss and gradient checks passed; both parameter changes were finite/nonzero. Combined actual GPU stage, including initialization/optimization/evaluation: **1.938 s**, well below12 minutes. Torch combined peak allocated **18.025 MiB**, reserved **22.000 MiB**, below512 MiB allocated cap; per-arm peak was not separately instrumented. Framework memory figures exclude driver/context overhead. CPU process-RAM peak was not independently measured; retained small features and transient frame arrays were bounded.

The final batch losses are higher than the first for both arms, and batches differ. This is not evidence of convergence. Accuracy difference is **0 percentage points**; this run does not show an advantage for motion priority. Arm subsection runtimes omit some initialization and are too small to support a speed claim. Repeated pairs from one film are not independent experimental replicates; no significance or cross-film generalization is asserted.

## Private input adaptation and independent time supervision

The frozen public trainer remained unchanged. Its legacy96 MiB guard belonged to an old network acquisition contract, while009 and the user explicitly authorized this local480p file without that download cap. Only the private copy replaced that guard with equality to the one prechecked file's actual size; no other media was admitted. Sampling, seeds, architecture, loss, optimizer, validation pairs and100-step-per-arm budget were unchanged.

Other private-only instrumentation: monotonic per-frame deadline, strict PTS verification across every decoded frame, two CPU decoder/torch threads, aggregate decode/per-arm/reserved-memory metrics and private progress/completed-arm records. CPU frames were decoded once; the original run function reused those same verified RAM arrays rather than decoding a second time. No frame/feature/checkpoint was uploaded.

A separate owned-process supervisor enforced CPU≤600 s, GPU≤720 s and parent≤1,800 s using monotonic clocks and phase markers. Before the real worker, an offline no-network sleeping test child was really stopped by the same guard mechanism and passed. No real experiment worker, external/user process or other lock was terminated/changed. Actual worker duration **24.203 s**; supervisor confirmed normal completion. ffprobe also had a30-second scoped own-helper timeout and exited normally. No UTC/string conversion was used for durations.

## Asset boundaries and handoff

Qwen/SigLIP exact authorized asset entries remain **ASSET_ENTRY_UNKNOWN**; no scan or weight/processor read was made, and no model forward/LoRA occurred. Media/network GET/HEAD/Range/AWS/model APIs/installation: **0**; Git coordination transport is separate. Old budgets/parts/ledgers, original research workspace, protected QA and environment/PATH/drivers remained untouched. Only the two specified anonymous Markdown paths are submitted; all media, hashes, private code and logs remain local.

After one normal main push, STOP. This is a single-film long-span low-dimensional temporal-head exploration, not long-video VLM question answering, independent heldout performance or a publication result. **NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP** and HourVideo/Ego4D release/PTS bridge **UNKNOWN** remain.
