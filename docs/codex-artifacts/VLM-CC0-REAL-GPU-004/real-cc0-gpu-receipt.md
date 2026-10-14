# VLM-CC0-REAL-GPU-004 — real public-video CUDA training receipt

Date: 2026-10-14 (Asia/Shanghai). Safely fast-forwarded the independent public docs checkout to main `77b206c`; confirmed the unique READY task and absence of an earlier parent result. Exactly one media acquisition and one training execution were performed.

**Result: REAL_CC0_VIDEO_GPU_TECH_SMOKE.** A complete MDN flower video was decoded on CPU, its real-frame features were used in 80 actual RTX3090 backward/optimizer updates, and parameters changed. No infrastructure-only CUDA retest was run.

## Source and acquisition

Source classification: **SOURCE_MDN_CC0 / LICENSE_PASS** for this bounded local engineering use. The [official MDN shared-assets README](https://github.com/mdn/shared-assets/blob/main/README.md) specifies its hosting domain and CC0/permissively licensed asset policy. The [MDN video example](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video) names flower.mp4; [official historical MDN discussion](https://github.com/mdn/interactive-examples/issues/1674) documents the migration into the cc0-videos directory, also corroborated by [issue 1749](https://github.com/mdn/interactive-examples/issues/1749). The [general license page](https://github.com/mdn/shared-assets/blob/main/LICENSE.md) was inspected but is not treated as a standalone asset-specific CC0 grant. This conclusion uses the combined official asset context, not merely public HTTP availability; it does not claim provenance verification of a different protected dataset.

No existing input was present in the newly created task-owned private directory. The provided fetcher was copied privately and passed UTF-8 AST inspection before execution. Exactly **1 ordinary GET**, **0 HEAD**, **0 Range**, **0 retries**, to the contract's fixed MDN HTTPS video URL returned a complete 200 response. Proxy inheritance and redirect following were disabled, with default HTTPS certificate verification retained.

Actual application response body: **1,128,375 bytes**, below 8,388,608 bytes. The downloader checked response encoding, declared length, actual length and MP4 header, flushed the private part and atomically committed the complete media. Private size/SHA matched the acquisition receipt afterward, and the part file was absent. The private SHA and video are not published. Application-body accounting is not a measurement of physical TLS/network traffic. Public license-page/Git traffic is separate from the one media GET.

## Real frames and split

PyAV performed real CPU decoding; OpenCV reduced selected RGB frames to 8×8×3 features. The runner retained **75 real-frame samples**, selecting every second decoded frame; this count is the feature-bearing frame count, not the total decoder output count or a claim of 96 frames.

Actual sampled PTS were finite, nonnegative and strictly increasing; sampled span **4.938 seconds**, exceeding the 1-second requirement. At least 32 real frames and the nonconstant-feature check passed. The first **56 frames** formed training; the final **19 frames** formed a disjoint, later contiguous validation block. No QA text, answers, source UID or protected dataset was used.

Validation is within this one short time-lapse clip, with 96 sampled pair presentations that may repeat underlying frame pairs. It is not an independent-video test or a long-video benchmark.

## Resource gate and actual training

Known cooperative and task-owned mutexes were absent and then acquired nonblockingly. Only this run's owned handles were released. Two target RTX3090 observations were separated by ≥2.1 seconds:

| Observation | Free GPU memory | GPU utilization |
|---|---:|---:|
| 1 | 22,907 MiB | 3% |
| 2 | 22,905 MiB | 3% |

Both passed free ≥8 GiB / utilization ≤30%. No positively confirmed conflicting training job was found in the scoped checks. Windows C+G list nonemptiness was not used as a rejection rule; this cooperative gate and snapshots are not a guarantee of physical-device exclusivity.

The supplied trainer used the existing pytorch environment and actual cuda:0, fixed model seed 19, training-pair seed 2026 and validation-pair seed 3037. Model: 384→64→1 temporal-order head, **24,705 trainable parameters**, AdamW lr 0.002, BCE-with-logits, batch 16. Training inputs came exclusively from the downloaded video's real frame features.

| Actual metric | Result |
|---|---:|
| Backward / optimizer updates | **80 / 80** |
| First training batch loss | 0.697165 |
| Last training batch loss | 0.661437 |
| Parameter absolute-change sum | 147.391893 |
| Same-clip later-block pair accuracy | 0.5417 |
| Torch peak allocated | 17.92 MiB |
| Torch peak reserved | 22.00 MiB |
| Runner timed GPU stage | 1.625 s |
| Entire training executor, including CPU/import/gate/validation | 7.031 s |

All training losses and gradients were finite; actual parameter movement was nonzero. First/last losses are from different sampled batches and do not establish monotonic convergence or scientific efficacy. The runner's GPU-stage timer ends before validation; the 7.031-second total executor bounds the complete training/validation execution and is still far below 10 GPU minutes. Allocator figures exclude driver/context overhead. CPU RAM peak was not independently instrumented; temporary frame/feature arrays were bounded by the provided small-media/96-feature-frame design. No checkpoint or feature output was published.

## Private-copy safeguards and limits

Public fetch/training source files remain unmodified. Only authorized private execution copies were adjusted: clamp steps/time to 80/10, check finite gradients, persist anonymous update progress, record reserved allocator memory, use two CPU threads; downloader uses remaining-budget reads without the original possible one-byte cap overread, checks monotonic acquisition duration, and fsyncs cumulative body-read entries. A private wrapper enforces task/media identity, no-replay marker, nonblocking mutexes, resource snapshots and network denial during training. Both provided scripts and the wrapper passed offline AST parsing; no separate synthetic experiment or CUDA infrastructure test was run. The trainer's run function was invoked once with steps=80 and gpu_minutes=10 under that wrapper.

No AWS/Ego4D/Charades/HourVideo access, model/API calls, weight downloads, dependency installs, environment/PATH/driver changes, process killing, old ledger edits or historical experiment replay occurred. The original research workspace was not accessed. All media, execution copies, raw receipts and acquisition ledger remain private. Exactly the authorized new Markdown receipt and one append-only parent result are submitted.

**Scientific interpretation:** this verifies the short real-video → CPU frames/PTS/features → RTX3090 temporal-head gradient chain. It does not demonstrate Qwen/SigLIP training, long-video reasoning, cross-video generalization or a research improvement. **NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP**, independent legal long-video training assets and the HourVideo release/PTS bridge remain unresolved. Stop after ordinary main push; no queued experiment is launched.
