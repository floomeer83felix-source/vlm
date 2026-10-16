# R1 — supplemental CPU-only pre-acceptance

Published **2026-10-16 (Asia/Shanghai)** at the user's explicit request. Documentation baseline: `4d41736cb49d9c866f2dc4ae336a3c9050f730d7`.

**R1_BOUNDED_CPU_PREACCEPTANCE_PASS / ELIGIBLE_QA_39 / FORMAL_017_NOT_STARTED.** This publishes the preceding user-authorized private CPU-only inspection. The user initially requested a private response, then expressly requested upload of its acceptance results. This publication is a supplemental evidence record, not execution, completion or consumption of the formal 017 parent. No new media inspection, label reading or experiment was performed for this upload.

## Input and bounded media evidence

The exact local MP4 was resolved from the frozen R1 identity and the user's actual official single-identity CLI command/output directory. It was a regular file; the inspected path and its ancestors had no reparse flags. No download-directory scan, old partial-file substitution or inspection of 013/014 media occurred. The user reported completion of an official `v1/full_scale` download; the existing CLI's version 1.7.3 and supported command options had previously been checked locally.

| Observed item | Result |
|---|---:|
| Actual local bytes | 606,852,958 |
| Actual local MiB | 578.740080 |
| Container / video codec | MP4 / VP9 |
| Video resolution / pixel format | 1440 × 1080 / yuv444p |
| Declared video rate | 30 frames/s |
| ffprobe stream/container duration | 2783.466667 s |
| Declared video frames | 83,504 |
| Nonempty video packets demuxed to EOF | 83,504 |
| Missing packet PTS / DTS | 0 / 0 |
| Non-increasing packet PTS / DTS | 0 / 0 |
| Packets with corruption flag | 0 |
| First / last observed video packet PTS | 0 / 2783.433333 s |
| CPU pixel-decode checks, start / middle / tail | 24 / 40 / 154 frames |
| Total actually decoded frames | 218 |
| Sampled frame PTS | Present and strictly increasing within each window |
| Sampled decode errors / corrupt-frame findings | 0 / 0 |
| Tail decode | Reached EOF; final decoded frame PTS matched final packet PTS |
| File size/mtime continuity during inspection | Unchanged |

The existing isolated ffprobe 9.0.2 was used with local-file protocol restriction. PyAV used CPU decoding with bounded windows and an owned-child timeout; no model or hardware decoder was requested. The checks establish readable container structure, packet traversal to EOF with the declared frame count, and successful bounded pixel decoding including the tail. **They are not a complete pixel decode of all 83,504 frames or an official remote byte-hash/content authenticity certificate.** No claim that every frame is semantically valid or independently corruption-free is made.

## R1 metadata and question qualification

- The exact R1 identity matched the authorized HourVideo dev record and the local release-1 canonical manifest. The newly downloaded manifest's R1 row equaled the corresponding row used in 016. Explicit `release_1=True` and `canonical_is_validated=True` flags were present, with an official-shaped canonical source reference and nonempty recorded source/origin identifiers.
- Annotation duration and canonical-MP4 manifest duration both declared **2783.47 s**, approximately **3.33 ms** above the measured stream duration. The general manifest duration field separately declared about **2783.48 s**; it was not silently substituted for the canonical-MP4 field. These are compatible rounded metadata observations, not an independent time-mapping certificate.
- R1 was neither of the two previously observed sample identities and did not match their recorded `(video_source, origin_video_id)` groups. This is recorded-source exclusion evidence, not proof of strict independent physical capture or absence of unrecorded overlapping events.
- An isolated CPU qualification checker inspected **only R1's** question/option text and label values as needed for the documented 013/014 eligibility contract. All **39 original questions** matched R1, had five nonempty options, a nonempty question and a valid single-letter A–E reference-label encoding. **Explicit image-task exclusions: 0; explicit external-asset reference exclusions: 0; other schema/uncertainty exclusions: 0.** No URL/external image-file marker, deictic auxiliary-image marker or ordinary image-word occurrence was found in the inspected question/MCQ/option fields.
- **Eligible question count under this CPU pre-acceptance screen: 39.** This verifies qualification and label encoding, not semantic correctness of every reference answer. No answer, question, option, per-item decision or identifying text is published. No reference label entered an observation-selection or inference process; neither process was started. No accuracy or paired-model result exists from this check.

## Separate evidence decisions

| Evidence claim | Status and limit |
|---|---|
| Local file readable and bounded engineering integrity checks satisfied | **PASS**, scoped to the checks above |
| R1 UID / recorded source / release-1 metadata association | **PASS**, based on existing local metadata and user-reported official acquisition |
| Declared duration correspondence and minimum 20-minute media span | **PASS** |
| Local stream origin and canonical-manifest stream origin both zero | **PASS** as a stream-level observation |
| Independent immutable release/canonical byte-identity certificate | **UNKNOWN** |
| Original physical-capture crop start / exact release-edit correspondence | **UNKNOWN** |
| Independent annotation-time-zero to media-PTS mapping | **UNKNOWN** |
| Strict physical source independence | **UNKNOWN** |
| Official remote byte-hash agreement | **UNKNOWN / NOT CHECKED** |

Retain **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**. A zero stream timestamp does not certify the original crop start or annotation zero. Any future permitted whole-video experiment would still need its prospectively stated `MEDIA_PTS_DIRECT_WHOLE_VIDEO` assumption and could not claim official HourVideo leaderboard certification from this pre-acceptance alone.

## Authority and preservation

The preceding check performed **0 GPU operations, Qwen/SigLIP forwards, model loads, training, network downloads or environment modifications**. It did not re-run 013/014 or modify video/annotation/manifest inputs. This upload performed documentation synchronization and publication only; it did not repeat the media or gold checks. No raw labels, QA text, identities, paths, object keys, private hashes, frames or source reidentification map are included.

Formal 017 remains **NOT_STARTED**, with **no GPU authorization** and no `### VLM-HOURVIDEO-NEW-SOURCES-017` execution result added. R2/R3 acquisition and any new experiment remain user decisions. No ChatGPT-owned planning file or historical result was edited. Publish this supplemental report and one clearly separate append-only pre-acceptance record, then stop. **PAUSE_FURTHER_GPU / NOVELTY=RETAIN0 / Charades FINAL_MEDIA_STOP** remain.
