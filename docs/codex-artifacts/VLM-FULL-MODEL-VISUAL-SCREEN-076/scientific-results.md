# 076 complete Qwen visual evidence screen

2026-11-02 Asia/Shanghai. **NO_SATISFYING_FULL_MODEL_VISUAL_SCREEN / STOP_NEW_ADAPTER_TRAINING_ON_THIS_ENTRY.** All432planned logical answers are CLOSED/finite with no unknowns. REAL32has no all-correct observational quartet, ties both controls at0/55and answers fewer native questions correctly than TEXT_ONLY. The frozen investment gate fails. No new adapter training, rerun, prompt change or new mechanism claim follows.

## Fixed constrained-choice results

Same24stored videos/144questions; one frozen Qwen3-VL-4B-Instruct checkpoint,32real224RGBframes or RGBblack with identical true clock/nonpixel input,or current text alone. Default chat template,assistant first-continuation position; literalYes/Noare distinct single tokens. Prediction compares their two logits,margin>0Yes/tieNo. No generation, sampling, extra prompt, threshold choice or confidence-based selection.

| Condition | Item correct | Six-question all-correct | Opposite-label quartet correct | Reverse pairs complementary | Coherent videos /24 | Constant-answer videos /24 |
|---|---:|---:|---:|---:|---:|---:|
| REAL32 | 76/144 (52.7778%) | 1/24 (4.1667%) | 0/55 | 10/72 | 1 | 17 |
| CLOCK_BLACK32 | 72/144 (50.0000%) | 0/24 (0.0000%) | 0/55 | 0/72 | 0 | 24 |
| TEXT_ONLY | 97/144 (67.3611%) | 6/24 (25.0000%) | 0/55 | 49/72 | 8 | 0 |

REAL32versus CLOCK_BLACK32:7native items independently corrected and3harmed,net+4/144(+2.7778pp); six-question net+1/24(+4.1667pp); quartetnet0/55. REAL32versus TEXT_ONLY:26items independently corrected and47harmed,net−21/144(−14.5833pp); six-question net−5/24(−20.8333pp); quartetnet0/55. All margins,indices and statuses were sealed before truth parsing. Full counts are in[3conditions](./condition-summary.csv)and[2paired rows](./paired-summary.csv).

The small item gain over matched-clock black is preserved. It does not satisfy the required strict quartet advantage over both controls,and the native-item requirement against text also fails. The result is this fixed screen's failure; it does not prove that all temporal relationships or all video use are impossible for this backbone. Black inputs shift distribution;32uniformsamples/224resolution may miss relevant evidence; labels and source provenance retain their limits.

## Why the55quartets matter

A question/tau pair is canonicalized by smaller UTF8text,without looking at predictions. Among14canonical questions,7have both publisher labels across the24videos. For each question,all positive-video×negative-video pairs are retained in the fixed order,producing55observational quartets(two videos×sameq/tau). No confidence/correctness filtering or sample replacement. They share videos/questions and are not55independent samples or same-video causal counterfactuals; backgrounds and unasked events are uncontrolled.

TEXT_ONLYgives exactly the same answer to the same input in each video context. Its quartetcorrect count0is a mandatory software/binding guard and passed. Its97/144item and6/24six-way scores can reflect question/semantic priors and this batch's distribution; they provide no visual evidence. Neither native six-way coherence nor item accuracy alone replaces the opposite-label quartet test. No bootstrap,p-value,subgroup,seed search or new comparison gate was added.

## Full inputs and inference, not separated features

32distinctreal nearest-PTS midpoints per video,CFR-index tolerance as in074/068.24clips yielded19,110traversed frames. Nativeprocessor[16,14,14]grid/[3136,1536]pixels and784visualtokens verified with one CPU syntheticfixture,then all actualinputs. Every REAL/BLACKpair has identicalinput_ids,mask,grid and all other nonpixel tensors; black uses that video's originalfps/duration/frameindices/encodedtimestampsequence. Pixelstorage shares24realblobs and one actual-byte-identical blackblob. TEXT_ONLYhas no video placeholder/clock.

One frozenbf16/SDPAload,316actual complete root forwards:144REAL,144BLACK,28TEXT,with116textaliases covering432logicalanswers. Each call runs the native visual/language path as applicable and lm_headat the lastvalid position; logits_to_keep1avoids unnecessary sequence-wide vocabulary output without bypassing the backbone. OnlyYes/Notwo logits,margin,prediction savedprivately. Measuredhooks:root316,visual288,decoder316,decoderlayers11376,lm_head316; these are measured entries,not a census of every submodule/kernel. No old12frameQA/smallhead/featureforward,retry,generation or training.

## Independent verification and evidence boundaries

Pre-weight-load independentinputgate2458checks and finalindependentreview3438checks passed. All code was sealed before firstresearchpayload,unchanged after32frameDECODE/ROOTSTARTED. The input gate independently tokenized the defaultprompt,checked lastposition/singleYes-Noidentity,32indices/realRGB/grids,and all144matchednonpixelpairs. Final review rechecked persistedtensors,seals,316uniqueinputs/432bindings/aliases,alltwo-logit rules/ledger/hookcounts,oldlabelbinding,55quartets/3conditions/2pairs/guardandgate. No producer-scorer import,decoder/visual/root replay,secondmedia decode or post-output supplementcode.

GPUJobexit0/actualactive0before scoring,all six Jobs finallyactive0/exit0/no kill. GPU129.469s/600,allocatedpeak9,687,196,160B/16GiB. Data-plane prepared/RGBlogicalreads963,465,370B/1GiBbefore report metadata reads,sharedbufferscounted per actor. Host/physicalIO/periodicdiskmonitor coverage is limited. Torch/BLASwere configured4threads,but PyAVcodec thread policy inherited defaults and was not independently capped/measured; full codec≤4thread compliance is not certified. This limitation remains in the receipt/summary rather than being presented as full resource certification.

This is an already-used batch and publisher-exact-order-derived labels,not a new blind benchmark or authenticated physical-event ordering. Strict completion/nonoverlap/uniqueoccurrence,recording/participant/old-source/pretraining exposure are unknown. Full32framemultimodalroot and earlier12frameseparated-featureheads differ in interface/budget; no fair newmethod victory or connector localization follows. D/070/current smallheadtuning stays stopped,069paused,controlled reorderingHOLD. No automatic077 or paper work.
