# VLM-HOURVIDEO-MATCHED-QA-012 — matched gold present, release/PTS evidence hold

Date: **2026-10-15 (Asia/Shanghai)**. Contract baseline main `52b3d44`. The independent docs checkout was clean and synchronized; latest AGENTS, task board, results, overview and012 README were read. Unique READY/no previous parent result confirmed. The user explicitly authorized local qualification, conditional≤4 Qwen generations/GPU≤40 minutes and post-generation isolated scoring.

**Outcome: RELEASE_PTS_BRIDGE_HOLD.** The authorized official-demo entry exists, its private UID exactly matches the authorized annotation entry,43 questions have five options and syntactically valid gold, and full real-video decoding/PTS checks pass. Independent evidence establishing the exact release/crop/annotation-zero-to-media-PTS mapping was not supplied. This gate was not inferred from identity/duration proximity; no GPU generation or scoring was run.

## Exact-entry access and privacy

The user clarified the private media stem in the active conversation. The extensionless exact entry was absent; only the same stem with the official MP4 extension was checked and found. This was the same user-specified object with a hidden-extension interpretation, not directory enumeration or a search over UID candidates. No other download entry was inspected.

The media is a regular file with no reparse ancestry, size **889.396 MiB**. The previously authorized annotation file was read-only, regular and no-reparse. Its current SHA was measured and retained privately; no hash, UID, filename, source mapping, question, option text or answer value is published. No old media part or private research tree was accessed.

Source/use basis is the user's attestation that the file was manually obtained from the official HourVideo demo release and the current research-evaluation authorization. No network verification, gated-access bypass, credential request or copyright/permission expansion occurred. This user/source evidence is not a remote publisher byte-hash or exact immutable-release mapping certificate.

## Identity and gold qualification

| CPU qualification | Observed result |
|---|---|
| Exact annotation UID match |**PASS**|
| Questions in matched record |**43**|
| Same-record question UID agreement |**PASS for43 eligible records**|
| Nonempty question plus five nonempty options |**43 eligible**|
| Explicit valid reference-answer label fields |**43 eligible**|
| Required at least two eligible questions |**PASS**|

Gold qualification checked field presence/type and admissible label encoding, not correctness against viewed images or model outputs. No gold value was exported to a selection policy/prompt. The CPU qualification process handled the protected record locally; no inference policy or scorer consumed it. Only eligibility counts were retained in anonymous output.

The planned first-two-question rule was not executed or frozen as an actual scoring set because release/PTS qualification failed first. The pre-registered possible denominator remains2 per arm if a future independently authorized qualified run is performed; this batch has **0 evaluated questions**, not a0% QA score or43 evaluated questions.

## Complete container and actual PTS

Exactly one existing CPU ffprobe call returned success without error output, in **0.094 s**. MP4 contains one VP9 video stream and an AAC audio stream; no audio transcription/analysis occurred. Container start is0 and duration **3598.054362 s**; video-stream duration **3598.033333 s**. The annotation video metadata duration is **3598.030000 s**, a video-stream-duration difference of **0.003333 s**. These are observed numeric comparisons, not an alignment tolerance selected to declare PASS.

One complete CPU PyAV video-stream decode reached EOF successfully:

- **107,941 actual decoded frames**.
- Every frame had actual PTS/time base; values finite, nonnegative and strictly increasing.
- First video-frame PTS **0.021029 s**; last **3598.021029 s**.
- Actual full decoded PTS span **3598.000000 s**, exceeding1,200 s.
- Last-frame PTS minus annotation duration **−0.008971 s**.
- CPU qualification worker elapsed **330.375 s**, below600 s.

No frame was displayed, manually interpreted, exported publicly or used for model input. Full RGB candidate extraction was not performed: eligibility used actual decoded-frame timing, not synthetic samples or inferred end timestamps. No input repair, remuxing, frame shifting, scaling, timestamp truncation or file mutation occurred.

## Exact remaining scientific gate

**reason_code: RELEASE_PTS_BRIDGE_HOLD**. Evidence-entry classification: **NO_EXACT_INDEPENDENT_MAPPING_ENTRY_SUPPLIED**.

Official-demo provenance attestation, UID equality and closely matching duration/PTS endpoints are useful supporting evidence. They do not independently identify an immutable release, prove absence of a same-duration crop/time shift, or specify whether annotation zero maps to container zero, first video PTS or another original-source origin. The provided annotation metadata has duration/source/scenario/device fields; no separately supplied exact release/crop/zero-origin mapping entry was available for this execution.

No alignment function or tolerance was invented from the observed residuals. No claim is made that the demo is mismatched, corrupted or impossible to align; the required bridge remains **UNVERIFIED**, rather than disproven. A future decision needs a precise authorized evidence entry documenting the same release and the reversible annotation-time/media-PTS mapping, or an explicitly reviewed revised qualification protocol. This completed parent does not authorize additional source searches, network requests or automatic GPU continuation.

## Conditional inference and scoring

| Planned operation/metric | Actual result |
|---|---|
| Qwen generate attempts/successes |**0/0**|
| SigLIP image/text forwards |**0/0**|
| GPU execution time |**0 s**|
| Current model loading/resource snapshots/mutex gate |**NOT_RUN**|
|48 candidate/12 selected-frame comparison |**NOT_RUN**|
| EOS/length truncation/token counts/selection overlap |**NOT_RUN**|
| Task model memory peak |**NOT_RUN**|
| Independent scoring calls/questions |**0/0**|
| Accuracy/paired four-cell table |**NOT_EVALUATED**|

The upstream011 model readiness is historical evidence only; this CPU gate failure did not trigger another model load or replay of its successful generations. No movie substitution, gold-assisted selection, answer exposure to a model, self-scoring or unpaired inference occurred. There is no formal pilot score to merge with earlier movie/no-QA experiments.

## Execution controls and stop

The private qualifier passed AST inspection and denied socket connect/DNS operations. It checked monotonic time during frame iteration with a590-second internal guard, plus an independent supervisor bound to the owned worker at600 seconds; the worker exited normally, with no forced termination. No UTC/date-string conversion was used. Current inputs were opened read-only; only new private audit files were written. No installation, environment/model/driver/PATH change, protected-asset scan, external process/lock change, historical replay or old ledger modification occurred.

Research media/model/AWS/HTTP/cloud API requests **0**; Git coordination transport is separate. Only this anonymous Markdown receipt and one append-only parent result are submitted; all IDs, QA/gold, raw timing records, source paths/hashes and scripts remain private. Normal main push then STOP.

**NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP** and the relevant HourVideo/Ego4D release/PTS bridge **UNKNOWN** remain. Real matched media/gold and full PTS were established, but this batch produced no Qwen QA result or scientific sampling advantage.
