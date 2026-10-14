# VLM-PD-LONGVIDEO-006 — reason-coded official source check

Date: 2026-10-14 (Asia/Shanghai). Contract baseline main `fbd3819`. The clean independent docs checkout was safely fast-forwarded; latest AGENTS, task board, results, overview, new README/downloader and referenced public A/B trainer were reread. Unique READY and absence of an earlier 006 result were verified. This was a new bounded parent execution, not a rerun of 005.

**Outcome: HOLD — reason_code `DERIVATIVE_EXACT_KEY_COUNT`.** Offline selftest passed. The single official metadata request passed schema/file identity and structured US Public Domain checks, but did not supply exactly one derivative entry matching the frozen `360p.vp9.webm` transcode key. No video request or GPU experiment followed.

## Offline and isolation checks

Both committed Python sources were copied into a new private task-owned directory and passed UTF-8 AST inspection. Existing directory ancestors had no Windows reparse attributes. The new downloader's explicit `--selftest` completed with **OFFLINE_SCHEMA_SELFTEST_PASS**: one positive fixture and four negative cases checking license, exact-key count, official derivative URL and file-title rejection. The downloader also executes the same selftest internally before its real request; that internal gate passed. These are schema/branch tests, not evidence of real media access or a simulated research result.

Only authorized private copies were changed: avoid the original metadata read potentially exceeding its cap by one byte; validate exact cap/EOF handling; persist metadata HTTP status, media reserved/read-body counts, and a terminal fsynced reason_code. No source selection or licensing requirement was relaxed. Public code, 005 assets and old request budgets remain unchanged. The public A/B trainer was privately copied/AST checked but never executed.

## Actual network and gates

| Gate or operation | Actual result |
|---|---|
| Official Commons metadata GET | **1 attempt, HTTP 200** |
| Complete metadata application body | **3,155 bytes / 524,288-byte maximum** |
| JSON/API/schema/page identity/videoinfo | **META_SCHEMA_PASS** |
| Structured copyright fields | **LICENSE_PASS, jurisdiction US** |
| Exact 360p VP9 derivative gate | **HOLD / DERIVATIVE_EXACT_KEY_COUNT** |
| Official derivative URL gate | **NOT_RUN** |
| Media GET | **0 / 1** |
| Media response-body bytes | **0 / 100,663,296-byte maximum** |
| HEAD / Range / retries / mirrors | **0 / 0 / 0 / 0** |
| Complete new video / part | **None / none** |

Default TLS verification, explicit proxy disabling and redirect rejection were retained. STARTED and META_GET_ATTEMPT were fsynced before the one request. The private ledger then recorded META_BODY_COMPLETE, META_SCHEMA_PASS, LICENSE_PASS and **TERMINAL_HOLD with reason_code DERIVATIVE_EXACT_KEY_COUNT**. This accurate terminal reason is durable, rather than merely an exception class. No raw metadata, URL, hash or private path is published.

The reason means the count of entries with the exact requested key was **not one**. The executor did not retain the numeric count; it therefore does not distinguish zero matches from multiple matches in this report. It does not prove that the public webpage has no 360p video, that every official transcode is unavailable, or that licensing failed. No alternate key, inferred URL, second API request or original-version download was attempted. The US declaration is reported as jurisdiction-specific metadata evidence, not a worldwide public-domain guarantee; specific-use legal clearance was not promoted beyond it after the derivative gate failed.

## CPU and GPU result

No full video was acquired. CPU video decoding, frame/PTS ≥20-minute eligibility, train/validation timing split, resource snapshots, GPU mutex acquisition and torch/CUDA execution were **NOT_RUN**.

| A/B metric | Uniform | Motion priority |
|---|---|---|
| Actual backward calls / optimizer updates | **0 / 0** | **0 / 0** |
| Real selected training frames | **NOT_RUN** | **NOT_RUN** |
| Loss / parameter changes / later-block accuracy | **NOT_RUN** | **NOT_RUN** |
| GPU stage time / allocator peak | **NOT_RUN** | **NOT_RUN** |

No claim of ≥350 real samples, ≥1,200-second PTS span, complete movie or A/B performance is made. The conditional CPU hard-supervision and GPU gates were never entered or asserted to have passed. No old flower clip, synthetic arrays or protected media substituted for the missing eligible source. No precise foreground-duration measurement was persisted; the bounded metadata operation completed promptly and no extended CPU/GPU work was started.

## Handoff

Data operation totals: metadata GET1; media GET0; AWS/Ego4D/Charades/HourVideo access0; model/weight/API execution0. No installation, environment/PATH/driver change, original research-tree access, old ledger mutation, process termination or background job occurred. Only this new anonymous Markdown receipt and one appended parent result are submitted.

A future separately authorized task may investigate the returned derivative schema/key correspondence using appropriately permitted evidence; this completed parent does not authorize another request or any alternative transcode. Stop after one normal main push.

**NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP**, HourVideo/Ego4D release/PTS bridge **UNKNOWN** remain. There is no long-video training or scientific A/B result in this execution.
