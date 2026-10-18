# VLM-HOURVIDEO-TRAIN-PREP-001 — combined read-only CPU preparation

2026-10-18 (Asia/Shanghai).
**TRAIN_PREP_CPU_STATIC_COMPLETE_WITH_HOLDS**.

Main was safely fast-forwarded to `481debf336ba343f1adf8d2ef0debaa6ae3df9a6`.
Latest AGENTS, task board, results, overview and updated TRAIN-PREP contract were
reread; this was the unique READY parent with no previous formal result. The
active user authorized A/B/C/D together. All four parts were completed within
their permitted evidence scopes; missing A/B evidence did not stop C/D.

| Part | Status within this task | Result and minimum remaining prerequisite |
|---|---|---|
| A: original identity and rights | HOLD | Historical public rights evidence reviewed; ORIGINAL_009_IDENTITY_UNKNOWN and RIGHTS_BINDING_UNKNOWN. Need a precisely authorized nonprotected original provenance/permission record bound to the candidate. |
| B: source isolation and leakage | HOLD | Public recorded-group history and leakage boundaries reviewed; STRICT_PHYSICAL_SOURCE_INDEPENDENCE_UNKNOWN. Need positive nonprotected recording/shot/edit/source-group isolation evidence, not access to dev answers. |
| C: static assets, distributions, host | PASS, static scope only | Known model roots, small configurations, expected weight-file presence,13 package metadata versions and CPU host resources inspected. Runtime/processor constructibility, feature output shape and GPU_RESOURCE_UNVERIFIED remain UNKNOWN. |
| D: conditional training protocol | PASS, paper scope only | Objective, windows, controls, seeds, architecture and aggregate proposed budgets frozen below. No execution permission or readiness certificate is granted. |

## A — public rights evidence and original identity

The [009 public receipt](../VLM-LOCAL-LONGVIDEO-009/local-long-video-ab-receipt.md)
records prior user research-training attestation and structured US public-domain
evidence. It expressly limits remote-byte and worldwide-rights claims. This is
historical executor evidence, not a newly inspected original permission record.

The [022 receipt](../VLM-TRAIN-SOURCE-VERIFY-022/read-only-source-verification-receipt.md)
already established existence and bounded container/packet readability for the
single user-declared candidate, with specifications matching009. Those facts
were reused without opening or even re-statting the movie. No probe, demux,
decode or hash was performed in this round.

No additional precise nonprotected original license/origin text or trusted old
digest entry was supplied within the current authorized scope. The local-file
to original-work/source/transcode binding therefore remains UNKNOWN. Prior
training-use attestation is positive historical evidence, but does not by itself
certify that binding or resolve territory-specific use rights. The current
read-only permission is not future training permission. No title, filename,
genre, age, matching size or duration was used to upgrade rights or identity.
No new licensing site, source URL, private receipt directory or permission
record was searched. UNKNOWN is not a conclusion that the asset is unlicensed.

## B — physical-source separation and leakage

Public009 and [018](../VLM-UNSEEN-SOURCE-STRATIFIED-018/three-arm-new-source-receipt.md)
describe prior training/internal-validation and recorded evaluation groups;
[021](../VLM-TRAIN-SOURCE-ELIGIBILITY-021/read-only-source-eligibility-receipt.md)
and022 preserve the physical-independence gap. Different recorded identifiers,
film subject matter or historical nonaccess to QA are insufficient proof of
different physical recording/shot/edit sources. No specifically authorized
nonprotected source-group proof was available to close this gap. Private
Ego4D/HourVideo UID/source maps, dev annotations, reference timestamps, QA/gold,
evaluation media and Charades were not accessed.

Leakage rules frozen for any future approved work:

- Same-film later-block validation is training-internal validation, not a new
  physically independent held-out video or official benchmark score.
- The observed013–018 dev questions, answers and predictions cannot supervise
  an optimizer, teacher/pseudo-target, selector, hyperparameter choice,
  checkpoint choice or stopping decision.
- Source-group separation must be established before execution; an unknown
  original/capture relationship holds even when numeric IDs differ.
- PTS may construct internal training labels/windows, but PTS, frame ranks,
  pair IDs, source IDs, text QA and annotation timestamps are not head inputs.
- All future controls must share the same frozen features, train/validation
  windows, pair sets and denominator; no result-dependent source replacement.

## C — observed static assets, versions and host snapshot

Only the two previously authorized exact model roots were used. Direct expected
filenames were checked without listing directories or scanning caches. Present
entries and necessary ancestors were regular/non-reparse. No weight tensor or
large tokenizer content was opened, and no framework/model was instantiated.

| Asset | Static observations | Unverified boundary |
|---|---|---|
| Qwen3-VL-4B | Model type qwen3_vl; declared architecture Qwen3VLForConditionalGeneration; text hidden2560/layers36/heads32; vision hidden1024/depth24/output2560. Two expected weight shards stat-present, total8,875,719,344B; index has713 entries. | Weight contents/dtypes/identity and model or processor construction were not tested. No root dtype value was reported in the selected metadata; this is not runtime BF16 proof. |
| Qwen processor/tokenizer | Image/video descriptors and tokenizer config present; Qwen3VLProcessor, Qwen2VLImageProcessorFast, Qwen3VLVideoProcessor and Qwen2Tokenizer declarations; patch16/temporal2/merge2; tokenizer maximum262144; chat-template descriptor present. | Raw template/tokenizer bodies not published; no processor call or token-grid proof in this round. |
| SigLIP | Model type siglip; declared SiglipModel and float32; one expected safetensors file stat-present,812,672,320B. Text hidden768/heads12 are explicit; vision patch16 is explicit. | The small vision config omits its output hidden dimension; text hidden768 does not certify image-feature width. Actual image-feature output shape, defaults and tensor dtype remain untested. |
| SigLIP processor/tokenizer | SiglipProcessor/SiglipImageProcessor/SiglipTokenizer descriptors;224x224 resize, rescale/normalize enabled; text maximum64. | Construction and vocabulary/runtime compatibility are not established by descriptors alone. |

Ten small JSONs were read, each below2MiB; the largest was64,742B. They comprised
two model configs, two image preprocessing configs, one video preprocessing
config, two tokenizer configs, one special-token map, one Qwen shard index and
one generation config. Nineteen direct leaf entries were checked, including the
two index-declared shards:15 existed and four optional descriptor entries were
absent. There was no fallback search. The absent generic processor descriptors,
one special-token map and the image-only asset's video descriptor are reported
as absent, not automatically a broken installation. The two large tokenizer
JSONs were stat-only because they exceeded2MiB. All three weight files were
stat-only; weight content reads were0. Whole model/processor completeness is
therefore not certified.

All following versions are **installed distribution metadata only**, queried
with stdlib importlib.metadata. No corresponding runtime was imported.

| Component | Version |
|---|---|
| Python interpreter | 3.9.21 |
| torch | 2.5.1 |
| transformers | 4.57.6 |
| av | 15.1.0 |
| numpy | 1.26.4 |
| Pillow | 10.4.0 |
| safetensors | 0.5.2 |
| tokenizers | 0.22.2 |
| accelerate | 1.3.0 |
| huggingface-hub | 0.36.2 |
| torchvision | 0.20.1 |
| sentencepiece | 0.2.1 |
| protobuf | 6.33.2 |
| Jinja2 | 3.1.5 |

The package metadata is not a compatibility test or CUDA build/driver query.
The [019](../VLM-TRAIN-HEAD-HARNESS-019/synthetic-cpu-harness-receipt.md)
WinError1455 and [020](../VLM-TRAIN-CPU-RUNTIME-020/cpu-runtime-verification-receipt.md)
WinError87 outcomes remain historical bounded runtime failures with unresolved
causes. They were neither retried nor treated as proof that the current runtime
is healthy, permanently unusable, or GPU-ready.

Host-only snapshot:16 logical CPUs;63.82GiB physical total,43.01GiB available;
43.31GiB available system commit with67.82GiB commit limit. Free space on the
already known asset and runtime volumes was326.97GiB and412.85GiB respectively.
No volume path/device identifier is published. Windows system-memory APIs and
filesystem free-space metadata were used; no Torch/CUDA DLL, NVML,
nvidia-smi or GPU driver API was loaded/queried. **GPU_RESOURCE_UNVERIFIED**.
These snapshots do not reserve resources or guarantee future availability.

## D — frozen conditional self-supervised proposal, NOT execution permission

This proposal can execute only after A/B become positively supported and a new
reviewed task/runtime/resource/user-authorization gate passes. The movie is not
opened here. It is already a development training asset, not a fresh held-out
test. The protocol is a temporal-proximity proxy and an engineering control
comparison, not an event-order or long-video QA mechanism claim.

| Item | Frozen proposal for the next separately approved run |
|---|---|
| Task | TRAIN_HEAD_SELF_SUPERVISED; continuous-logit binary near versus far prediction from two frozen visual embeddings only. |
| Time basis | Real frame PTS from the approved movie only. Let u=PTS-first_valid_frame_PTS and L=last_valid_u. Require finite strict order, no missing/duplicate selected frames and L>=1200s; no annotation/capture-zero certificate is inferred. |
| Training-internal split | Train0<=u<0.70L-9s; validation0.70L+9s<=u<=L. The18s gap is excluded; pairs cannot cross windows. All evaluation source groups remain excluded. |
| Features | Exactly128 distinct train and64 validation source frames at deterministic evenly spaced actual-PTS targets within their own windows. Frozen local SigLIP image processor, eval/inference mode, float32, batch8, L2-normalized embeddings; no text encoder/query/QA. No augmentation or resampling after outcomes. |
| Feature-shape gate | Paper input dimension d=768. The current static check does NOT certify that image-output width. Before any head update in a later approved run, actual finite feature shape must be exactly[192,768]; otherwise STOP, no silent dimension change. |
| Pairs | Within each window enumerate unordered i<j. Positive0<delta_PTS<=12s, negative delta_PTS>=120s; discard the middle band. Stable gap/index ordering, first48 positives and48 negatives per window; insufficient classes hold. Resulting96-pair pools remain fixed for all controls. |
| Controls | Untrained random head0 updates; primary true-label head100 updates; shuffled-label negative head100 updates.200 optimizer updates TOTAL, not200 per group. Same architecture, head initialization, features, pair presentations and optimization settings. |
| Balanced negative control | Interleave the fixed positive/negative pairs into eight-pair blocks, each4/4. Shuffle labels once within each block using seed19, preserve per-batch counts, and never reshuffle/reseed based on loss. If the overall shuffled target is unchanged, STOP rather than retry. |
| Pair schedule/seeds | Initial head seed19; precomputed block schedule seed2026 shared across both trained controls; fixed validation presentation seed2126. True versus shuffled target is the only optimization-control difference. |
| Head | abs(z_i-z_j) concatenated with z_i*z_j; detach inputs; Linear1536->64, ReLU, Linear64->1. Two linear layers and98,433 trainable parameters by arithmetic, below1M; no temporal position, gap, index, ID or QA features. |
| Optimizer | Head-only AdamW, lr0.002, weight_decay0.01, betas(0.9,0.999), eps1e-8; BCEWithLogitsLoss; batch8, accumulation1, no scheduler. Both training groups use100 updates exactly unless a safety STOP occurs. |
| Frozen backbones | SigLIP eval/inference-mode features, no encoder gradient or optimizer membership. Qwen remains frozen and unloaded; Qwen forward/LoRA/update count0. |
| Validation/checkpoint | Same fixed96 true-label validation pairs for random/primary/shuffled heads. Report all outcomes and invalid/nonfinite failures. No best-of-loss or seed/source selection; save at most the primary head's predetermined final100th-step checkpoint, never the best-performing control. |
| Proposed caps | <=200 actual head updates in aggregate; <=60 cumulative GPU minutes INCLUDING encoder/load/feature/validation stages; batch<=8 and accumulation<=4 (fixed1 here); one private checkpoint<=256MiB; all additional research temporary data<=2GiB; downloads0. |
| Additional proposed safety ceilings | Allocated GPU peak<=2GiB for this head/encoder pipeline, CPU extraction<=600s, runtime parent<=4500s. These are conservative paper ceilings, NOT measured feasibility or granted quotas. Failure is STOP, not batch/precision/limit changes. |
| Future resource admission | Fresh explicit GPU permission and READY contract; safe owned locks, no conflicting workload, two fresh free>=8GiB/utilization<=30% gates if retained by that future contract, monotonic watchdog and durable pre-step global counter. No such GPU check occurred now. |

The019 implementation remains a synthetic-only harness capped at16 rows,
32-dimensional input and12 updates with its original256MiB contract. It is not
directly compatible with this proposed192-row/768-dimensional real-feature
protocol. No019 code or budget was changed, and020's separate failed runtime
attempt was not repeated. A separately reviewed real-data runner/integration
is still required under a later authorized task; if unavailable, execution must
hold rather than silently expand the old harness limits.

The12s/120s thresholds and frame counts are fixed now without reading actual
QA/answers or optimizing candidate results. Evenly spaced features can still
produce empty pair classes if real usable PTS do not meet the contract; STOP
rather than adjust thresholds. Repeated pairs from one film are not independent
population replicates. Adjacent-frame visual similarity, local scene/static
content and film-to-first-person distribution shift remain explicit shortcuts
and confounds. Any later other-domain training must retain this disclosure.

The48-per-class quota was chosen during paper review to avoid requiring64 near
pairs from only64 validation frames: at the historically reported duration,
the uniform validation spacing supports only63 adjacent near pairs. This is
an arithmetic design check using the public duration, not new media evidence
or an outcome-driven adjustment. Actual PTS eligibility remains a future gate.

Parameter change, finite loss/gradients/weights, exact shared update counts,
frozen-backbone gradient absence, resource peaks and final-checkpoint cap must
be observed in the future authorized execution, not inferred from this design.
Proxy-loss improvement is not evidence of HourVideo QA gains, source-general
performance, statistical significance or novelty. External QA evaluation would
need a separately authorized independent, frozen source protocol.

## Read scope, timing and final admission

The bounded static child read the six public009/018/019/020/021/022 receipts and
the ten small asset JSONs, performed direct file/ancestor stat checks and queried
nine package distributions plus CPU host resources. A second supervised
stdlib-only metadata query checked four processor dependencies. Actual owned
child wall times were0.485s and0.219s. A conservative60s allowance covers the
initial public coordination/reference reads, including future contract review:
accounted read-only investigation60.704s, below300s. The first child had a240s
outer/235s internal ceiling; the completed child left ample cumulative budget
for the15s-bounded dependency query. Documentation authoring and Git transport
are outside this read-only investigation timer. There was no unbounded survey,
asset retry, directory enumeration or current media read.

Precisely authorized new private nonprotected license/origin/group records
read:0; source/evaluation private maps read:0; model tensor/large-tokenizer
content reads:0; media stat/probe/demux/decode/hash:0; Torch/Transformers/AV model
runtime imports:0; GPU APIs, gradients, optimizer updates, checkpoints,
research network/downloads, installation/environment changes and private
writes:0. Framework names did not appear in the static children's loaded
module checks. Only this public receipt and one formal parent append are written.

Minimum next evidence is asset-bound original rights/identity and nonprotected
positive physical-source isolation proof; the existing installed runtime and
actual feature/GPU-resource gates also require a separately approved execution.
No additional permission request, private search, runtime repair or new task is
initiated here. **TRAIN_PREP_CPU_STATIC_COMPLETE_WITH_HOLDS is not
TRAIN_CPU_PREFLIGHT_PASS. TRAIN-GPU remains QUEUED/HOLD.**

No private media name/path/title/license URL, asset location, identity map,
hash, raw configuration/log, weights, feature or protected QA/gold is published.
Historical results, task README and planning files remain unchanged. One
ordinary main push, then STOP. **NOVELTY=RETAIN0;
CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; Charades FINAL_MEDIA_STOP.**
