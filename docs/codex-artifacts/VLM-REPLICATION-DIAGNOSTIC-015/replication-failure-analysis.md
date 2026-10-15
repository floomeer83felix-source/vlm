# VLM-REPLICATION-DIAGNOSTIC-015 — CPU-only replication audit

2026-10-15 (Asia/Shanghai). Reviewed documentation main: `8a2ebce8fe80a8f2c85b7bec65e0c3e9fc5b0e00`. User explicitly authorized A/C only; B has no newly authorized exact private entries and is **PRIVATE_ARTIFACTS_NOT_AUTHORIZED / SKIPPED**. No private-result search or access occurred.

**A COMPLETE / C COMPLETE; RESULT_DIRECTION_FLIP; QUERY_SAMPLING_SUPERIORITY_NOT_ESTABLISHED; NOVELTY=RETAIN0.** The initial positive within-video difference did not reproduce on the one additional video. This does not establish that SigLIP is generally ineffective or that uniform sampling is generally superior. Both score sets remain **CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**, exploratory nominal whole-video results, not official HourVideo leaderboard scores.

## Scope and evidence

The separate clean documentation checkout was fetched and safely fast-forwarded. AGENTS, latest task board/results/overview and the [015 contract](./README.md) were reread. The current task-board status column contains exactly one READY parent, 015; no prior 015 result or report existed. The latest dated decision and 015 row supersede historical READY statements and stale overview/header summaries; planning documents were not edited. Another documentation checkout with pre-existing uncommitted changes was left untouched, as was the experimental workspace.

Inputs are the public [013 receipt](../VLM-HOURVIDEO-WHOLEVIDEO-QA-013/whole-video-provisional-qa-receipt.md) delivered in [bf5e36a](https://github.com/floomeer83felix-source/vlm/commit/bf5e36ad216c33e6cb04d2493c9e5fce050f7713), [014 receipt](../VLM-HOURVIDEO-CROSSVIDEO-014/crossvideo-heldout-receipt.md) delivered in [e7f654a](https://github.com/floomeer83felix-source/vlm/commit/e7f654a2acb93fed196da0ea4d361cb14bc1725f), and the historical [novelty screen](../../route2-novelty-screen.md) and [mechanism reset](../../mechanism-reset-2026-10-09.md). No external literature request or new paper/full-text verification occurred. This is an independent arithmetic/document audit, not independent verification of private pixels, tensor identity, gold, predictions or execution ledgers.

## A1. Deterministic reconciliation

All scores in this table have the provisional assumed-clock limitation above. A = uniform12; B = frozen question-only SigLIP query12.

| Measure | 013: original demo | 014: one additional sample video |
|---|---:|---:|
| Original records / nongold exclusions / fixed N per arm | 43 / 6 / 37 | 29 / 0 / 29 |
| Both correct / A-only / B-only / neither correct | 4 / 2 / 8 / 23 | 7 / 4 / 2 / 16 |
| A correct / valid wrong / INVALID / NOT_RUN | 6 / 27 / 4 / 0 | 11 / 15 / 3 / 0 |
| B correct / valid wrong / INVALID / NOT_RUN | 12 / 22 / 3 / 0 | 9 / 16 / 4 / 0 |
| A correct/N | 6/37 = 16.216216% | 11/29 = 37.931034% |
| B correct/N | 12/37 = 32.432432% | 9/29 = 31.034483% |
| B minus A | +6/37 = +16.216216pp | −2/29 = −6.896552pp |
| Discordant items | 10 | 6 |
| Descriptive exact two-sided McNemar p | 7/64 = 0.109375 | 11/16 = 0.6875 |
| Qwen attempts / returns / natural EOS | 74 / 74 / 74 | 58 / 58 / 58 |
| Token-cap-without-EOS / retries / training updates | 0 / 0 / 0 | 0 / 0 / 0 |
| User-authorized attempt cap for that execution | 86 | 58 |
| GPU-stage wall / historical 1,800 s cap | 31.906 s | 25.344 s |
| Allocator peak / historical 20 GiB allocation limit | 8,848.588867 MiB | 8,884.593750 MiB |

Stdlib Python (`Fraction`, `math.comb`) independently checked: four cells sum to N; correct counts equal both + corresponding only cell; correct + valid wrong + invalid = N in each arm; attempts = 2N and do not exceed the actual user cap; GPU-stage and allocation summaries are below reported limits. NOT_RUN and failed generations are zero in both receipts. Neither-correct includes INVALID; invalids were not removed from denominators. For discordant counts b=A-only and c=B-only, the audited p is `min(1, 2 * sum(comb(b+c,k) for k=0..min(b,c)) / 2**(b+c))`. Reported rounded percentages and p values reconcile without a material discrepancy. The wider 014 planning ceiling is not the actual 58-attempt authorization and cannot provide unused permissions.

At a descriptive item level both p values exceed 0.05. Questions within a video can share evidence; the binomial independence assumption underlying these reference p values is unverified. They establish neither superiority, equivalence, absence of effect nor a significant between-video interaction. No new pooled test, confidence interval, macro accuracy or overall benchmark accuracy was calculated. **N_video=2 potential source groups; N_new=1**. Distinct canonical identities were reported, but strict physical-capture independence is not independently certified. The question counts do not create 66 independent source replicates.

## A2. Controls and observable differences

Receipt-level controls match: same local Qwen3-VL-4B-Instruct BF16 and SigLIP F32 assets; 48 candidates from each video's own PTS; A uniform12 and B question-only cosine top12 in chronological order; no options/gold in retrieval; same MCQ prompt, processor, video grid `[6,12,18]`, deterministic decode and 64-new-token cap; alternating AB/BA; unchanged exclusion and parser rules. Both report 14/14 protocol tests, isolated post-inference scoring and no output repair/retry. These are documented controls, not newly remeasured raw execution guarantees. Matching grid/frame count supports comparable visual input budgets, not a new independent token/tensor audit.

| Observable | 013 | 014 | Interpretation limit |
|---|---:|---:|---|
| Candidate PTS span | 3,597.9 s | 4,226.7 s | Different durations; absolute seconds alone cannot explain the flip |
| Mean query-selected span | 3,082.723423 s | 3,677.821839 s | Span between extremes is not evidence coverage |
| Mean query span / candidate span | 85.681187% | 87.014026% | Normalized from public means and fixed span; no semantic localization inference |
| Mean intersection with uniform12 | 3.378378 frames | 3.068966 frames | Selection differs from uniform, with relevance unverified |
| Mean intersection / 12 | 28.153150% | 25.574717% | Retained-frame overlap, not Jaccard |
| Reported mean per-question Jaccard | 0.167011 | 0.148722 | Cannot reconstruct this mean by transforming the mean intersection |
| INVALID A / B | 10.810811% / 8.108108% | 10.344828% / 13.793103% | EOS completion does not guarantee valid A–E format |
| New-token totals A / B | 103 / 90 | 73 / 84 | Includes EOS; all calls naturally ended |
| New-token ranges A / B | 2–15 / 2–10 | 2–13 / 2–13 | No observed cap truncation in either run |
| Qwen generation wall sums A / B | 9.847 / 8.514 s | 7.097 / 7.343 s | Different N, prompts and lengths; no matched deployment speedup inference |
| Processor wall sums A / B | 3.278 / 3.252 s | 2.280 / 2.299 s | Common pipeline; totals do not measure equal per-question work |
| B SigLIP load + feature stage | 0.453 + 0.953 s | 0.454 + 0.859 s | Retrieval is charged to B; generation-only timing omits it |
| GPU-stage wall / worker wall | 31.906 / 69.094 s | 25.344 / 60.156 s | GPU-stage includes resident CPU work, not pure CUDA kernel time |

Candidate construction is common to both arms in each run; the reports separately record extraction at 7.656 s versus 4.031 s. Different seek-decode workloads and source durations prohibit a simple between-run cost attribution. Allocator peaks exclude driver/context overhead; these public summaries do not establish physical residency or deployment savings.

Candidate explanations remain **unidentified**, with the following observable boundaries:

- **Population/task composition:** 013 used a dev-annotation matched demo with six explicit auxiliary-asset exclusions; 014 used a different public-sample source with none. Subject matter, evidence distribution, task mix and annotation quality may differ. Aggregate receipts supply no authorized category or per-item evidence to quantify those explanations. Selection rules are reported unchanged; there is no evidence of output-based cherry-picking in these runs.
- **Temporal selection geometry:** normalized mean spans are close, despite different durations and modestly different overlap. End-to-end span does not reveal missing interior events, redundancy, evidence precision or relevance. Neither a larger span nor lower overlap diagnoses SigLIP misretrieval. A temporal-distribution explanation requires independent evidence under a new authorized design.
- **Formatting:** invalid rates vary and all remain incorrect in the primary endpoint. A mechanical sensitivity bound, allowing only existing INVALID calls to hypothetically become correct while fixing all valid outputs, places B−A in `[+2/37,+9/37]` for 013 and `[−5/29,+2/29]` for 014. Thus formatting alone cannot erase 013's positive sign under this artificial bound, while 014's sign is sensitive. These are identification bounds, not observed corrected scores, instructions to repair outputs or evidence that formatting caused the flip. No invalid-overlap or semantic-error subtype was invented.
- **Model/prompt interactions and chance:** fixed settings remove configuration changes as a documented explanation, but different content/options may interact with the same model and sparse frames. Both non-significant item-level results and the tiny number of source groups permit sampling variability. Neither chance nor a content-specific mechanism is established as the cause.
- **Source/clock and disclosure:** both use `MEDIA_PTS_DIRECT_WHOLE_VIDEO` with `CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`; immutable release/crop/annotation-zero and capture independence remain unverified. Full 013 decode and 014 packet preflight are different historical audit types. These uncertainties limit score interpretation, but do not show that actual mismatching media caused the flip. The previously observed demo and publicly available sample gold are not blind confirmatory data.

## A3. Existing-method risk; no new literature review

Only the two linked historical project reviews were inspected. Their source characterizations remain attributed historical screening evidence; no current availability, publication detail or full-text claim was independently revalidated here.

| Historical screening entry | Repetition risk for the present proposal |
|---|---|
| Q-Frame | Query-aware similarity selection and fixed visual budgets already have direct precedent |
| Self-Adaptive Sampling | Question-aware versus question-agnostic sampling comparisons already exist |
| DIG2026 | Query-type-dependent global/local sampling and stratification are prior risks, not a new finding from these aggregates |
| CVPR2026 RL Selector | Single-frame relevance versus set utility is an existing concern; a negative similarity result is not a new operator |
| VideoSEAL | Evidence/answer authority separation and grounding checks are prior risks; correct MCQ predictions alone do not prove grounded reasoning |

A better score on one video is a performance observation. A paper-level mechanism needs a distinct state/update/action rule, a falsifiable behavior unavailable to the closest matched baseline, and source-independent evidence with full cost controls. No such mechanism is established here. Historical M1/M2/M3 closures are not reopened. **QUERY_SAMPLING_SUPERIORITY_NOT_ESTABLISHED; NOVELTY=RETAIN0.** Stop using these two observed sources to tune prompts, seeds, retrieval thresholds or frame budgets for confirmatory claims.

## B. Private diagnostic gate

**PRIVATE_ARTIFACTS_NOT_AUTHORIZED / SKIPPED.** The current authorization provides no two exact private result entries and explicitly directs skipping B in that case. No result-directory enumeration, private prediction/gold access, per-question reconstruction or category inference was performed. A and C are complete without B; no additional private credentials or paths are required for this delivery.

## C. Recommended scientific decision and future admission gates

**NO_GO_SIGLIP_STABLE_ADVANTAGE:** reject the current claim of stable SigLIP superiority and reject further tuning or training on the two observed sources. This is a claim/evidence NO-GO, not a universal algorithm impossibility result. The technical inference chain has worked; additional compatibility smoke tests or reruns of 013/014 do not address the scientific gap.

**GO_REPLICATION_ONLY_IF_NEW_DATA:** a future falsifiable question is whether the unchanged B policy improves fixed-denominator paired correctness over unchanged A on a source roster frozen independently of outcomes, at explicitly measured total cost. Necessary gates before any new execution are:

1. **New lawful data and source separation:** at least 2–3 additional genuinely new physical source groups, excluding the old demo/sample and their alternate encodings/crops. Establish lawful evaluation use, exact media/gold correspondence, fixed mother population and nongold eligibility, historical overlap exclusion and defensible release/PTS/time-origin evidence. Another approved multi-video long-video benchmark is possible only after equivalent rights, gold, duration and clock gates pass. Existing user access is not a new download authorization. Public/disclosed gold remains explicitly exploratory, not blind.
2. **Freeze the estimand and roster before observing results:** keep all eligible questions for each source and A uniform12/B original frozen query12; same Qwen assets, prompt, parser, 48-candidate construction, 12-frame preprocessing budget, deterministic settings and paired order. Freeze invalid/failed/NOT_RUN handling, fixed denominators, a scientifically meaningful positive margin and the analysis/stop rule before execution. Do not invent a margin from these outcomes. Report every admitted source and every failure regardless of sign; no replacing losing videos or increasing N until a favorable result appears.
3. **Source-level evidence:** publish per-source paired tables/differences and cost/coverage summaries. Source groups, rather than individual questions, are the replication/statistical clustering units. Two or three new groups permit limited descriptive replication; they do not by themselves guarantee adequate power or a reliable population confidence interval. Any confirmatory sample-size/power and clustered uncertainty plan must be justified and frozen prospectively using enough independently supported groups. No inference from the present two groups is substituted for that plan.
4. **Controls and possible C:** distinguish realized visual tokens/grids, temporal distribution, overlap, invalid formatting, candidate extraction, retrieval, processor, model load and generation cost. Do not omit B's retrieval overhead. Only after literature and independent-data gates pass may a new parent specify C, such as a fixed time-stratified/semantic-diversity strong existing baseline, with its own fair compute accounting and new explicit GPU budget. C is not authorized by 015 or the spent 014 allowance. A/B success alone cannot establish novelty against those stronger precedents.
5. **Novelty and training:** prospective positive evidence must still survive closest-method review and a distinct-mechanism test. A negative or heterogeneous replication closes the stable-advantage claim for the frozen domain rather than triggering same-source hyperparameter searches. Neither result authorizes selector training, Qwen fine-tuning, distillation or LoRA. Training additionally requires a lawful genuinely separate training set, frozen independent evaluation, leakage controls, a new READY parent and specific user resources.

**Present action: PAUSE_FURTHER_GPU.** The necessary newly verified sources, protocol and new execution budget are not supplied in this CPU-only round. These recommendations are an audit deliverable for ChatGPT review, not a change to ChatGPT-owned planning files or an activation of queued tasks. All future positive and negative source results must be retained. `NOVELTY=RETAIN0`, `CLOCK_ZERO_ASSUMED_NOT_CERTIFIED` and Charades `FINAL_MEDIA_STOP` persist.

## Delivery and safety

Only installed Python stdlib arithmetic and public documentation were used. This round performed **0 GPU operations, 0 model inference/generation, 0 video decode, 0 research HTTP/AWS or media/model downloads, 0 training, 0 environment changes and 0 historical experiment/result/ledger changes**. Git documentation coordination is the only network exception. No private identities, QA/options/gold, replies, frames, paths, hashes or reidentification maps are included.

Deliverables are this single anonymous report and exactly one appended 015 parent result. After the one ordinary main push, stop; no background continuation, new source acquisition or leftover-budget use.
