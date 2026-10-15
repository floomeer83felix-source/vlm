# VLM-HOURVIDEO-WHOLEVIDEO-QA-013 — provisional paired whole-video MCQ

Date: **2026-10-15 (Asia/Shanghai)**. Contract main `bdb6da3`. Clean independent docs checkout safely synced; latest AGENTS/task board/results/overview and013 protocol read; unique READY/no prior parent result verified. User explicitly authorized≤86 local Qwen generate attempts/GPU≤30 minutes. Actual frozen workload:74 attempts,37 questions per arm.

**Status: MATCHED_UID_WHOLE_VIDEO_QA_PROVISIONAL.** Clock/evidence label throughout: **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**, nominal sampling model **MEDIA_PTS_DIRECT_WHOLE_VIDEO**. Scores below are **provisional within the same-user-matched demo, assumed whole-video clock**. Formal HourVideo DEV/leaderboard accuracy = **NOT_ESTABLISHED**. The012 release/crop/time-origin uncertainty is preserved; it was not retroactively declared PASS.

## Pre-GPU eligibility, immutable denominator and isolation

The exact authorized media entry and current local model roots from011 were reused; no example-path substitution, directory enumeration or full107,941-frame decode replay. Necessary config/weight-size/local processor checks passed. The original annotation SHA matched the privately retained012 evidence. Current video size/mtime were frozen and checked again at scoring; this is scoped continuity evidence, not a new official remote byte-hash certificate.

The scheme was implemented and frozen **before model inference and before gold scoring**:

| Nongold eligibility result | Count |
|---|---:|
|Original same-UID five-option/gold-qualified records|43|
|Explicit image-task suffix requiring extra asset|5|
|Explicit external-asset reference in question/option/MCQ schema|1|
|Uncertain auxiliary-asset exclusions|0|
|Other nontext-schema exclusions|0|
|**Frozen eligible N per arm**|**37**|

Classifier rules used task schema, explicit image/URL/file references and explicit deictic auxiliary references, not gold values, question difficulty or model replies. Ordinary standalone word `image` did not imply an external resource. All remaining video/text-only questions entered in original stable order. No task/QID/text/option/answer or exclusion-specific identifying content is published.

A separate CPU freeze process copied only ordinal, question text and five original option strings into the inference input. It did not copy gold, canary or relevant_timestamps. The inference worker **never opened the annotation/gold file**. Annotation-time windows were neither consulted nor mapped for frame selection. Gold existed/was encoding-qualified in012 and current annotation identity was verified by SHA; no gold value entered selection or prompts.

**14/14 offline synthetic protocol tests PASS**,0 failures/errors. They covered strict prediction parsing/reference-label encoding, correct invalid/not-run accounting, paired queue/four-cell aggregation, nongold/timestamp independence, ordinary-image-word acceptance and explicit/uncertain auxiliary exclusion. Synthetic fixtures were protocol tests only, not video/model results.

The fixed model queue alternated AB/BA by eligible question order, **2×37=74** maximum attempts, below86. Each actual attempt was fsynced before generate; none was repeated or replaced. Private frozen-input/annotation hashes were rechecked by the post-run scorer. No seed, question set, prompt, parser or budget changed after outputs were observed.

## Whole-source PTS and real selection

CPU candidate extraction sought only within the already verified media's own measured first/last PTS. It decoded **5,098 frames across seeks**, retained exactly**48 real RGB candidates**, and took**7.656 s**. Candidate actual PTS were finite/nonnegative/strictly increasing, spanning**3597.900000 s**. This was not a new full decode. No audio transcription or manual frame inspection occurred.

Uniform12 used fixed equally spaced indices in the same48. Query-aware12 used real SigLIP normalized image/text cosine scores, deterministic stable top12 and restored chronological PTS order. **SigLIP query text was the question alone**, excluding options/gold/external fields. Shared visual embeddings were computed once.

| Selection aggregate over37 questions | Actual result |
|---|---:|
|Frames fed to Qwen per arm/question|12|
|Uniform selected span|3597.900000 s|
|Query-selected span min/mean/max|1990.333333 /3082.723423 /3597.900000 s|
|Query-selected spans below1200 s|0|
|Mean intersection with uniform12|3.378378 frames|
|Mean Jaccard|0.167011|

These are source-video coverage metrics, not annotation evidence localization or proof of better grounding. No relevant_timestamps determined any candidate or selected window. Timing metadata used source nominal-fps indices derived from observed PTS; it does not certify annotation zero or release identity.

## Hardware gate, fixed model settings and cost

Owned cooperative/task mutexes passed and were released normally. Two target RTX3090 observations separated≥2.1 s: free**22,978/22,974 MiB**, utilization**7%/8%**, satisfying≥8 GiB/≤30%. No positively confirmed conflicting heavy training job was found in the scoped checks; mixed C+G nonemptiness did not independently block execution. Snapshots/cooperative locks are not a guarantee of physical exclusivity.

Both models loaded only from the previously user-authorized actual roots, with local_files_only=True, offline mode, trust_remote_code=False and safetensors. Existing environment retained. Qwen3-VL-4B-Instruct BF16/SigLIP F32, SDPA, eval/inference_mode; no quantization/offload adaptation, warmup generate, training or gradient updates. The process-local allocator fraction limited reservations conservatively to20 GiB; no global cache purge occurred.

The system prompt was exactly the contract's instruction to choose A–E and output only one letter. Each question used the original question and all five options, identically in A/B. Both received12 video frames, same processor/visual budget and grid**[6,12,18]**, representing12 source frames with temporal patch2 and192×288 processed resolution. Input limit8,192 tokens, do_sample=False and max_new_tokens64 were fixed. No arm identity, gold or canary was fed to Qwen.

| Execution/cost metric | Actual result |
|---|---:|
|Qwen generate attempts/returned successfully|**74/74**|
|Attempts/returns per arm|**37/37**|
|SigLIP image forwards|6 batches×8 candidates,48 total|
|SigLIP text forwards|5 batches,37 question-only queries|
|SigLIP model load|0.453 s|
|SigLIP shared image/text feature + preprocessing stage|0.953 s|
|Qwen model load|3.953 s|
|Combined GPU-stage wall, including loading/selection/preprocessing/generation|**31.906 s**|
|Torch peak allocated|**8848.588867 MiB (~8.64 GiB)**|
|Torch peak reserved|9042.000000 MiB|
|Entire actual worker|69.094 s|
|Independent supervisor|69.859 s, normal exit|

SigLIP loading/shared retrieval cost is charged to B and reported separately, not omitted or described as uniform cost. Candidate pool extraction is common to both. GPU-stage wall conservatively includes CPU preparation occurring while GPU models are resident; it is not measured pure CUDA kernel time. Framework allocator figures exclude driver/context overhead. CPU process-RAM peak was not independently measured.

| Returned-output metric | Uniform | SigLIP query-aware |
|---|---:|---:|
|Generate wall summed over37 calls|9.847 s|8.514 s|
|CPU processor wall summed|3.278 s|3.252 s|
|New tokens total|103|90|
|New-token min/max|2 /15|2 /10|
|Natural EOS endings|37|37|
|64-token cap without EOS|0|0|

EOS was checked from actual final generated token IDs against the model's EOS set. Token counts include terminal tokens. No length-truncated response was observed. Successful model execution still permits invalid answer format; it is not the count of correct answers. No output was repaired or regenerated.

## Isolated post-generation scoring — provisional assumed-clock result

Only after the owned inference child exited and a generation-phase termination marker was persisted did a **separate scorer process** open gold. It verified frozen files/annotation identity, reparsed private answers using the same pretested parser and compared once. Valid output requires strip() then exactly uppercase A–E with an optional final period; longer free text, lowercase/multiple choices or explanations are INVALID. Invalid/failed/not-run remain in the frozen denominator37.

**Every score in this section is provisional within the same-user-matched demo, assumed whole-video clock — CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; not official HourVideo accuracy.**

| Fixed-denominator outcome (provisional assumed-clock) | Uniform | SigLIP query-aware |
|---|---:|---:|
|Correct/N|**6/37 (16.22%, provisional)**|**12/37 (32.43%, provisional)**|
|Valid but wrong|27|22|
|INVALID|4|3|
|NOT_RUN|0|0|
|Total denominator|37|37|
|Nominal item-level Wilson95% interval (provisional)|7.65–31.14%|19.63–48.54%|

Provisional assumed-clock paired correctness table: **both_right4, A_only2, B_only8, both_wrong23**. Here both_wrong means neither arm correct, including any INVALID, so the four cells sum to37 and do not silently remove formatting failures. Provisional assumed-clock B−A difference is**6/37 =16.22 percentage points**. Descriptive exact two-sided McNemar on10 discordant questions gives**p=0.109375**. This does not establish statistical superiority.

The nominal intervals/tests treat question items as independent for a simple descriptive reference. All questions come from one video, may share evidence, and were filtered for available assets. Those calculations do not certify population uncertainty, multi-video transfer, official benchmark coverage or a causal sampling advantage. The unknown release/crop/time-origin correspondence remains an additional interpretation limit. No accuracy interval is represented as official benchmark evidence; no reference-answer content or per-item prediction is public.

## Safety, preservation and stop

AST and actual disposable-owned-child monotonic timeout tests passed before the real worker. Independent watchdog caps were CPU600 s/GPU1800 s and conservative worker-parent2400 s, below the50-minute parent allowance. Actual work ended normally well within these guards; no real worker/external/user process was killed or other lock removed. No UTC/date-string timing conversion was used.

Input source continuity was checked after generation; no annotation/video/model was modified. No research HTTP/GET/HEAD/Range/AWS/cloud API, model/video download, install, environment/driver/PATH change, full012 decode replay or old-experiment/ledger change occurred. Git coordination network is separate. Only the allowed new anonymous Markdown receipt and one appended parent result are submitted; all IDs, gold, QA, canary, timestamps sequences, outputs, model files, private code/paths/hashes/ledgers remain local.

Normal main push then STOP; no unused attempts/GPU allowance carried forward. **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**, **NOVELTY=RETAIN0** and Charades **FINAL_MEDIA_STOP** remain. The result is a same-video provisional whole-video MCQ exploration, not official HourVideo leaderboard accuracy, certified release/PTS alignment, Qwen training, independent-video generalization or publication-level novelty.
