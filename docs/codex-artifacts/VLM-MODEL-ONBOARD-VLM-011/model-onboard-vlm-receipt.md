# VLM-MODEL-ONBOARD-VLM-011 — actual Qwen/SigLIP long-video 2×2 inference

Date: 2026-10-14 (Asia/Shanghai). Contract main `53f36d7`. Clean independent docs checkout safely synchronized; latest AGENTS, task board, results, overview and011 contract read. Unique READY/no prior result confirmed. The current user supplied two exact model roots and explicit≤4 local Qwen generations/GPU≤40-minute authority. Only those roots and the earlier exact authorized movie entry were accessed.

**Outcome: REAL_QWEN_SIGLIP_LONGVIDEO_TECH_AB_COMPLETE — 4 attempted/4 successfully returned bounded generations.** Both models really ran on RTX3090. No model training, external model/video request, installation or official QA evaluation occurred.

## Asset onboarding and in-round user corrections

The Qwen model passed static qwen3_vl/Qwen3VLForConditionalGeneration identity, two-shard index membership/header-tensor-set consistency, file lengths and safetensors shape/dtype/contiguous-offset/end-of-file checks. Two weight files total **8,875,719,344 bytes**,713 tensors and4,437,815,808 tensor elements. Required config, generation config, tokenizer, chat-template, image and video processor files were present. Offline Qwen3VLProcessor/Qwen2TokenizerFast loading and sample text encoding passed.

Initial SigLIP inspection found its contract-required vocabulary absent. A812,762,989-byte PyTorch.bin existed, but safetensors did not. That archive's410 entries passed CRC without executing pickle. The existing transformers safety check refused PyTorch.bin loading under torch2.5.1 and required≥2.6; no weight load, GPU attempt or dependency upgrade was made at that point.

During this still-active parent task, the user explicitly reported supplementing the vocabulary and then safetensors. These were user changes, not executor downloads or repair. Only the same fixed entries were rechecked following the new evidence. The798,330-byte vocabulary allowed SiglipProcessor/SiglipTokenizer CPU loading and encoding. The new **812,672,320-byte safetensors**,408 tensors/203,155,970 elements passed shape/dtype/contiguous-data-offset/file-end checks; both text and vision weights were present. Safetensors was explicitly selected for actual loading; the incompatible.bin path was not used. No unchanged failed GPU/model load was retried.

Architecture imports passed in the preserved environment: torch2.5.1, transformers4.57.6, safetensors0.5.2, PyAV15.1.0, NumPy1.26.4; sentencepiece, torchvision and PIL modules present. All from_pretrained calls were offline/local_files_only, trust_remote_code=False. Static header/index checks do not substitute for official remote whole-weight hashes; source legitimacy uses the user's official-download attestation. Actual successful loading and inference subsequently confirmed operational compatibility for the tested configuration.

## Real local video and fixed candidate pool

The first previously authorized local movie entry was used; no alternate search, directory enumeration or old-part access. It was a regular no-reparse entry with the expected local file size;009's full container/decode evidence was reused, not its training replayed. No full movie decode was repeated.

This round CPU PyAV sought uniformly across the verified duration and selected **48 real RGB candidate frames**, all observed PTS finite/nonnegative/strictly increasing, spanning **1464.630 s**. Candidate retrieval decoded5,244 frames across seeks and took **1.766 s**. Frame arrays stayed private/RAM. Uniform12 used fixed equally spaced candidate indices. SigLIP cosine top12 used stable tie ordering and restored PTS order, with no QA answers/manual image inspection or motion fallback.

The two prompts were exactly the contract's P1 chronological visual summary and P2 beginning/middle/end change instructions. One common system instruction, same Qwen weights/processor/resolution and deterministic decoding were used; no arm label was given to the model. Qwen received12 chronological video frames with timing metadata, do_sample_frames=False and CPU video size constraints shortest_edge4096/longest_edge786432 aggregate pixels. Actual video grid **[6,12,18]** represents12 source frames with temporal patch2 and192×288 processed resolution. Timing metadata used observed PTS mapped to the source nominal frame-rate indices; selected-span metrics below use actual observed PTS, not a new protected-dataset clock bridge.

| Query selection metric | P1 | P2 |
|---|---:|---:|
| Uniform frames |12|12|
| Uniform actual PTS span |1464.630 s|1464.630 s|
| SigLIP selected frames |12|12|
| SigLIP actual PTS span |1402.301 s|1184.150 s|
| Intersection with uniform12 |3 frames|3 frames|
| Frame-set Jaccard |0.1429|0.1429|

P2 query-selected coverage is below20 minutes even though the common candidate pool spans>20 minutes. No gate or sample was changed to make it look broader. Frame coverage reduction/low overlap is a descriptive selection result, not an accuracy or grounding result.

## GPU gate, loading and SigLIP cost

Owned cooperative/task mutexes passed nonblocking acquisition and were released normally. Two target RTX3090 observations separated≥2.1 s: free **22,623/22,626 MiB**, utilization **10%/12%**, both meeting≥8 GiB/≤30%. No positively confirmed conflicting heavy task appeared in the scoped gate. Mixed C+G context nonemptiness was not a rejection rule; this does not guarantee physical exclusivity.

Attention: SDPA. Qwen: BF16, eval/inference_mode; SigLIP: F32, eval/inference_mode. Both actual loaders forced safetensors and local-only, with no quantization/offload/version fallback. A task-local allocator fraction conservatively limited reserved allocations to20 GiB; no global cache clearing/driver reset occurred.

- SigLIP load: **0.516 s**.
- Image feature forward attempts/completions: **6/6**,8 candidate frames per batch,48 total.
- Text feature forward attempts/completions: **1/1 batched forward for both frozen prompts**.
- Shared candidate image/text encoding and CPU preprocessing cost: **0.891 s**; each query's deterministic48-score sort was below recorded clock resolution.
- SigLIP loading plus shared retrieval cost is charged to query-aware selection, **not omitted or folded into uniform generation**. It is a once-per-task shared cost, not a per-query independent measurement.
- Qwen load: **4.000 s**.

SigLIP weights were released after retrieval before Qwen loading; no cache purge was invoked. No optimization/backward/adapter update occurred.

## Actual four bounded Qwen generations

Order frozen before execution: P1 A/B, P2 B/A. max_new_tokens192, do_sample=False, warmup0. Each attempt was fsynced before generate and success persisted afterward. Same-question prompt/system/template, frame count, processing settings, weight/dtype and decoder settings were common; chosen frame contents/timestamps varied by arm.

| Actual order | Arm | Input tokens | Returned new tokens | CPU processor | Generate time |
|---|---|---:|---:|---:|---:|
|P1-1|Uniform12|433|192|0.031 s|8.766 s|
|P1-2|SigLIP12|434|192|0.015 s|8.187 s|
|P2-1|SigLIP12|430|192|0.031 s|8.141 s|
|P2-2|Uniform12|430|192|0.015 s|8.062 s|

**4/4 actual generate attempts returned successfully**, no failed GPU retry. Input-token variation comes from selected timestamp text and question text, not arm labels. Output token counts include any terminal token; all four hit the configured192-token count. Natural-EOS/finish reasons were not separately retained, so replies may be length-truncated: successful bounded execution does not mean a complete semantic answer. Full outputs remain private and were neither uploaded nor used to self-score.

Combined GPU-stage elapsed, including both loaders, retrieval, preprocessing, generations and explicit synchronization: **38.906 s**, below2,400 s. Framework peak allocated **8,716.771 MiB (~8.51 GiB)**, reserved **8,778.000 MiB**, below20 GiB. These are framework allocator metrics, not full driver/device peaks. Whole worker **49.609 s**. CPU process-RAM peak was not independently instrumented.

## Supervision, preservation and scientific boundary

AST check and actual disposable no-network owned-child timeout selftest passed before the real worker. Independent monotonic supervision enforced CPU480 s, GPU2,400 s and conservative worker-parent2,700 s (below55-minute allowance). Only the precisely owned child handle could be terminated; the real worker finished normally and no external/user process or lock was altered. Preparatory CPU audits preceded that worker and completed promptly; no exact combined whole-round timer was persisted. No UTC string/timezone conversion was used in timeout decisions.

Old experiments, environments, drivers, protected QA and original research assets remained unchanged. Model/media research GET/HEAD/Range/AWS/cloud/model APIs/installations **0**; Git coordination is separate. Only user-supplemented files changed in the two authorized model roots; the executor did not modify them. No checkpoint, weights, frame, full answer, private path/hash/ledger/code or raw log is uploaded. Only this anonymous receipt and one appended parent result are submitted, then normal push/STOP.

This establishes real long-span movie input, paired SigLIP selection and Qwen generation feasibility/cost. The two generic prompts have **no reference answers**: correctness, method superiority, significance, grounding, cross-film generalization and HourVideo/Ego4D QA are **NOT_EVALUATED**. The previous45% temporal-head numbers have a different task/denominator and are not compared to these outputs. **NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP** and HourVideo/Ego4D release/PTS bridge **UNKNOWN** remain.
