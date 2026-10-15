# VLM-HOURVIDEO-CROSSVIDEO-014 — one additional public-sample video

2026-10-15 (Asia/Shanghai). Documentation main: `23fa708`; unique READY parent, no previous 014 result. The user supplied the official sample annotations and manually obtained the selected official video, then explicitly authorized this one video, at most **58 Qwen generate attempts**, and at most **30 GPU minutes**. This receipt closes that execution; it does not authorize another video or replay.

**SINGLE_ADDITIONAL_VIDEO_EXPLORATORY_REPLICATION / CROSS_VIDEO_PUBLIC_SAMPLE_REPLICATION.** Both arms completed on anonymous **video-1**. Uniform12 scored **11/29 (37.93%)**, question-only SigLIP12 scored **9/29 (31.03%)**; B−A = **−2/29 = −6.90 percentage points**. This additional video's direction is opposite to 013's observed direction. A reliable advantage of query-aware selection is **not established**. Only one additional video was run, so no cross-video macro accuracy or pooled accuracy is reported.

## Eligibility and evidence limits

- The two exact user-authorized sample metadata files parsed successfully and had equal two-UID sets. Selection was fixed by excluding the previously evaluated demo, leaving exactly one other canonical UID; no prediction or correctness-based video selection occurred.
- Video-1 has **29 original records**, all with five nonempty text options and structurally valid explicit gold labels. The unchanged 013 nongold exclusion rules excluded **0**; all 29 entered both arms in original stable order. Gold structure validation is not semantic verification of every reference answer. The public sample is not a blind held-out test set.
- User-attested official single-UID CLI acquisition requested `v1/full_scale`. The locally matched canonical UID differs from 013's demo. Different canonical UID and matching metadata support correspondence, but no independent physical-capture manifest or immutable release/time-origin bridge was supplied; strict capture independence and exact release alignment remain uncertified. No original video, sample rows, identity mapping, answer, or credential is attached.
- Read-only CPU container/packet preflight: **763.32 MiB**, MP4/VP9, container duration **4,226.854362 s**, video stream **4,226.833333 s**, annotation-declared duration **4,226.83 s**. Demux reached EOF over **126,805** nonempty video packets; packet PTS span **4,226.8 s**, missing PTS/DTS **0/0**, PTS/DTS reversals **0/0**. This packet audit is not a complete pixel decode or semantic content certification.
- **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED** remains. Sampling used only this video's own PTS, never annotation `relevant_timestamps`. This is provisional whole-video QA, **not official HourVideo leaderboard accuracy**.

## Frozen execution and isolation

The 013 protocol module was copied byte-for-byte, including exclusion, A–E output parsing and AB/BA paired order. Its **14/14** synthetic tests passed, as did an owned-child timeout guard. The new private runner changed only task identity, the tighter 58-attempt allowance, source-specific PTS/frame metadata and annotation-open blocking. The inference child could not open the original annotation files. Model fields were whitelisted into a separate frozen nongold input; gold was read by a separate scorer only after the supervised inference child exited. This does not imply the earlier annotation eligibility process never accessed gold fields for validation.

- Same local Qwen3-VL-4B-Instruct BF16 and SigLIP base F32 assets/processors as 013; local-only loading, unchanged model/shard identity and size gates, no model/environment installation or change.
- **48** whole-video candidates, **4,226.7 s** PTS span; bounded seek decode visited **3,071** frames in **4.031 s**. No full historical decode or old QA forward was replayed.
- A: unchanged uniform12. B: unchanged question-text-only cosine top12 from the same 48 candidates, then chronological order. Options/gold were not supplied to the retrieval query.
- Identical Qwen MCQ prompt and preprocessing across arms; video grid **[6, 12, 18]**, deterministic `do_sample=False`, `max_new_tokens=64`, no warm-up generation or retry, no training. New frame-count metadata came from this video's packet audit, rather than retaining the old demo's frame count.
- Query-selected temporal span min/mean/max: **2,338.166667 / 3,677.821839 / 4,226.7 s**; none below 1,200 s. Mean uniform/query intersection **3.068966/12**, mean Jaccard **0.148722**. These describe selections, not verified evidence grounding.

## Anonymous paired results — video-1 only

All fractions use the frozen **N=29**, including invalid outputs. Natural EOS does not imply a valid A–E answer.

| Measure | A: uniform12 | B: SigLIP query12 |
|---|---:|---:|
| Correct / N | **11/29** | **9/29** |
| Accuracy, provisional | **37.93%** | **31.03%** |
| Valid wrong | 15 | 16 |
| INVALID | 3 | 4 |
| NOT_RUN | 0 | 0 |
| Returned generations | 29 | 29 |
| Natural EOS | 29 | 29 |
| Token cap without EOS | 0 | 0 |
| Generated tokens, total | 73 | 84 |
| Generated tokens, min–max | 2–13 | 2–13 |
| Qwen generation seconds, sum | 7.097 | 7.343 |
| Input processor seconds, sum | 2.280 | 2.299 |

| Paired correctness cell | Count |
|---|---:|
| Both correct | 7 |
| A only correct | 4 |
| B only correct | 2 |
| Neither correct, including INVALID | 16 |
| Total | 29 |

Descriptive two-sided exact McNemar **p=0.6875**. Questions share one video and are not independent video replicates; this item-level calculation does not certify significance or generalization. No cross-video pooling with the previously observed 013 development video, no configuration reselection, and no additional video search were performed.

## Resource and safety reconciliation

- Global RTX3090 mutex and task-owned mutex passed. Two snapshots more than two seconds apart: free **22,820 / 22,819 MiB**, utilization **16% / 15%**. No conflicting training job was confirmed; desktop mixed contexts were not treated as automatic blockers. No other process was terminated.
- **58 attempts / 58 successful returns**, one per frozen question/arm; persistent reservation/completion ledger reconciled exactly with the fixed AB/BA order. No extra Qwen generation, output repair or retry.
- SigLIP: **6 image batches / 4 question-text batches**; load **0.454 s**, features **0.859 s**, charged to B. Qwen load **3.906 s**.
- GPU phase including loading/retrieval/generation: **25.344 s / 1,800 s cap**. Torch allocator peak **8,884.593750 MiB**, reserved peak **9,138 MiB**, under the **20 GiB allocated** limit. Worker wall **60.156 s**, supervised child wall **60.922 s**; normal exit, no timeout/kill. Independent CPU/GPU and remaining parent-wall supervision remained active.
- Frozen inputs and original media size/mtime were unchanged after execution; protocol identity, ledger, score denominators, EOS counts and resource caps reconciled. Historical experiments, model assets and original research environment were not modified.
- **0** research-network requests, new media/model downloads, dependency installs, gradient updates or optimizer steps during this execution. Git synchronization/publication is separate from research data access. Private questions, answers, predictions, source identities, media paths, hashes and logs remain local.

Execution is complete; scientific review remains with ChatGPT. **One new video is insufficient to claim cross-video validation complete**, and this run establishes neither a new mechanism nor model superiority. `NOVELTY=RETAIN0`, Charades `FINAL_MEDIA_STOP` and the uncertified release/clock boundary remain. Only this anonymous receipt and one appended Codex result are submitted; normal main push then STOP.
