# VLM-PD-LONGVIDEO-005 — bounded metadata stop receipt

Date: 2026-10-14 (Asia/Shanghai). Contract baseline: main `9d3e926`. The independent documentation checkout was clean and safely fast-forwarded. Latest AGENTS, task board, results, overview, parent README and both supplied scripts were read; the task was the unique READY parent without an existing result.

**Outcome: METADATA_VALIDATION_HOLD / VIDEO_GET_0 / GPU_UPDATES_0.** The one allowed Commons metadata request returned HTTP 200 and a complete 3,155-byte application response. The supplied fetcher's subsequent metadata validation raised ValueError before the source-license PASS marker and before any media request. The parent was stopped; no second metadata attempt, alternate movie or GPU experiment was performed.

## Actual request and asset state

| Item | Observed result |
|---|---|
| Fixed official metadata API GET attempts | **1 / 1** |
| Metadata response | **HTTP 200; 3,155 application bytes** |
| Media GET attempts | **0 / 1** |
| Video response-body bytes | **0** |
| HEAD / Range / retries / mirrors | **0 / 0 / 0 / 0** |
| Complete new video / new media part | **Absent / absent** |
| GPU training executions | **0** |
| Uniform / motion backward and optimizer updates | **0 / 0** |

The private STARTED/request ledger was fsynced before the request. Its terminal observed stage was META_BODY_COMPLETE; no SOURCE_LICENSE_PASS, MEDIA_GET_ATTEMPT or MEDIA_RESPONSE_ACCEPTED entry exists. The acquisition report records HOLD / ValueError, without an HTTP error status. The sole network attempt was consumed and was not reset, refunded or repeated. The ledger is retained privately.

This demonstrates successful metadata HTTP transport, not successful source qualification. Application bytes are not a measurement of TLS/wire traffic. Git transport is separate from these bounded data requests.

## What the failure does and does not establish

The failure occurred after metadata body acquisition and before source/license validation was recorded as passed. The committed script catches exceptions and emits only their class; the private copy retained that behavior for ValueError. It did not persist the offending field, the precise validation branch or the full metadata response. Thus the exact cause is **UNKNOWN**: possible branch classes include file/page identity, videoinfo structure, public-domain evidence or derivative qualification. No branch is asserted as the actual cause.

The official-film Public Domain marker, exact official 360p.vp9.webm derivative uniqueness/URL and admissible video Content-Length are **NOT_VERIFIED this round**. A 200 response alone does not prove those gates. This is not evidence that the film is non-public-domain, that the derivative does not exist, that the server rejected access, or that RTX3090 is unavailable. No supplementary page/API request was made to recover the lost diagnostic fields, and no failed acquisition was rerun.

## Long-video and A/B metrics

Complete media, duration ≥20 minutes, real frame samples ≥350, sampled PTS span ≥1,200 seconds, train/validation separation and actual decoder output: **NOT_RUN / UNKNOWN**. No ffprobe or real video decode was invoked.

Uniform arm: 0 selected real training samples, 0 updates; loss, parameter movement, validation accuracy and GPU time/memory **NOT_RUN**. Motion arm: the same. Zero selected samples means no selection execution, not a dataset cardinality finding. No resource snapshots, GPU mutex acquisition, torch CUDA operation, synthetic fallback, old short-video replay or partial Ego4D decoding was performed.

## Execution integrity and private preparations

A new task-owned private directory was created and its existing ancestors checked for Windows reparse attributes. Only the current public task sources were copied there. Offline UTF-8 AST checks passed before the sole fetch invocation. Public Python sources were not modified.

Private preparation tightened metadata reads to the exact 512 KiB cap rather than the original potential extra byte; added content-encoding/declared-length checks and persistent metadata/body/request stages. It also prepared monotonic CPU iteration checks and aggregate decode/per-arm timing metrics in the private trainer, but **the trainer was never executed**. These unexecuted preparations do not prove a CPU hard-supervision or training safety gate passed. No source-level repair was followed by another network attempt.

The bounded foreground request completed well within the 10-minute acquisition and 25-minute task limits; precise total foreground timing was not independently persisted, so no exact duration is claimed. No protected media, AWS/profile, Ego4D, Charades, HourVideo annotations, model weights, credentials or original research workspace was accessed. No dependencies/environment/drivers/PATH or old assets/ledgers were changed. No background experiment or process termination occurred.

## Decision and handoff

Only this anonymous receipt and one append-only parent result are submitted. A future separately authorized task could first improve validation-branch diagnostics offline and resolve the fixed official source qualification; this receipt does not authorize any further request or experiment. Ordinary main push is followed by STOP.

**NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP**, and release/PTS bridge **UNKNOWN** remain. No long-video, sampling advantage, Qwen QA or cross-video generalization result exists for this batch.
