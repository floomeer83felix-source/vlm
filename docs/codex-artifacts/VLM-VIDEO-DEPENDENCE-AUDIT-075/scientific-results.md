# 075 video-reference and structural calibration audit

2026-11-02 Asia/Shanghai. **COMPLETE_CPU_VIDEO_REFERENCE_AND_STRUCTURAL_AUDIT.** Every planned learned-head item and all720integer text orders were evaluated. Removing the current video's individual feature changes many predictions, while its aggregate answer advantage over a shared reference is not established by these observed results. This is a posthoc audit of already-used074items; no new mechanism, selected model or renewed training route.

## Six-question accuracy and changed predictions

Equal-weight six-seed means (%). Each seed keeps24published videos/144questions. GLOBAL_MEAN_V is one shared6x2560reference from this unlabeled24video batch, summed in fixed index order in float64, divided24then castfloat32; it preserves six positions. ZERO_V is a shared all-zero float32input. Normalizers,42training anchors,all36states and logit>0threshold remain unchanged.

| Frozen method | Original cached six-way % | Shared mean V % | Zero V % | Mean V changed answers % | Zero V changed answers % |
|---|---:|---:|---:|---:|---:|
| C_NATIVE | 0.6944 | 0.0000 | 0.0000 | 38.6574 | 44.5602 |
| D_NATIVE | 2.0833 | 4.1667 | 1.3889 | 39.3519 | 49.8843 |
| CONCAT | 3.4722 | 2.0833 | 0.0000 | 38.8889 | 47.9167 |
| FACTOR | 11.1111 | 17.3611 | 10.4167 | 37.6157 | 45.4861 |
| REVERSE | 2.7778 | 0.6944 | 0.0000 | 38.0787 | 44.2130 |
| ANCHOR | 13.1944 | 13.8889 | 1.3889 | 33.7963 | 52.0833 |

FACTOR retains10.4167%six-way accuracy with zeroV versus11.1111%original, a−0.6944ppmean change, but393/864answers change(45.4861%). Its shared-mean reference rises to17.3611%(+6.25pp)while325/864answers change(37.6157%). ANCHORsharedmean13.8889%versus13.1944%original(+0.6944pp)also changes292/864answers(33.7963%); zeroV falls to1.3889%(−11.8056pp),changing450/864(52.0833%). These are preserved answer and response facts, not equivalence findings or proof of correct temporal localization.

All72control/method/seed comparisons change at least one answer; identical-complete-prediction seed counts are0throughout. The fixed sharedV removes sample-specific video input from each prediction; its batch-mean content remains transductive overall information. The zero reference can shift input distribution, and old biases/position encoding/convolution and question/anchor priors remain. Drops under this intervention cannot identify which temporal evidence the original head used correctly. Aggregate gains under a shared reference do not make it a proposed algorithm or justify choosing a new champion.

## All conditions and relation consistency

[108conditions](./condition-summary.csv),[72paired rows](./paired-summary.csv)and[12method-control summaries](./method-control-summary.csv)retain all six seeds and full24/144/72denominators. Each pair reports independent corrections/harms/both/unknown,net,changed items and changed six-answer groups. Original36answer/response metric rows reproduce074exactly; original coherence counts are new075posthoc calculations, not measurements retroactively attributed to074.

A six-answer vector is coherent only when it equals one of the six complete orders of its three original event texts. Complementary but cyclic answers remain incoherent; no predictions are repaired. Conditions partition24groups into coherent-and-correct/coherent-but-wrong/incoherent, with the first exactly equal to six-way all-correct. For example, over the144repeated seed/video groups, originalFACTOR partitions16/76/52; meanV25/70/49; zeroV15/59/70. OriginalANCHOR19/75/50; meanV20/60/64; zeroV2/37/105. These sums do not create144independent recordings.

## Exhaustive text-only ordering calibration

Only the current question's two original text strings determine its prediction under a fixed global rank. All6!720UTF8-canonical text orders were enumerated equally; none was fitted, selected or promoted as a method. There are6texts,12unordered triples and28exactquestions;20,160unique integer predictions map to103,680logical answers,with83,520shared-text aliases. This is pure integer work, not model calls.

Every video is six-way correct under exactly120orders. Across17,280permutation/video groups,2,880are correct; across103,680items,51,840are correct. Equal-weight mean six-way16.6667%,item50%,reverse complement100%,constant-video0,coherent groups17,280. [Summary](./structural-baseline-summary.json)and[25bins](./structural-baseline-histogram.csv)retain all0..24correct-group counts; frequencies sum720and their weighted sum2880. No vocabulary, permutations or per-member predictions are public.

The1/64independent-six-bit,1/8independent-complementary-pair-bit and1/6complete-order expectations refer to different mathematical output constraints. The exact720-order mean is not a single model's measured performance, a p-value or an independent-sampling significance claim. The720orders share the same six texts. No bootstrap/interval,extra comparison gate,seed selection,subgroup or difference-in-differences was added.

## Verification and limits

All science,independent state/final oracles,budget/Job/ledger and matrix code were sealed before the first074payload read and remained unchanged. An independent pre-call state gate passed468checks; final independent input/reference/anchor/alias/metric/baseline recomputation passed81,971checks. It imported neither producer predictor nor scorer and performed no learned replay. The mean's ordered float64formula,zero input,full state/required-view bytes,all15552keys,exact aliases/ledgers,seals,old cache and handed scoring-label binding were checked independently. Labels were first parsed by the scorer after new learned and integer predictions had closed and bothJobswereactualactive0/exit0.

Exactly2016newCPUheadcalls produce10368interventionlogicalitems via8352aliases;5184originalitems onlycache. No oldhead/encoder/featuregeneration,torchbackward/optimizer,GPU/nvidia-smi,media/ZIP/rawmetadata,Qwenprocessor/modelconfig/largeweightaccess,download,newtraining,newlabels,environmentchange or paper work. Small-head weights were read directly from074without copying a weight package.

The source retains publisher-order-derived labels,uncertified strict completion/nonoverlap/unique occurrence,unknown physical recording/participant and pretraining/old-source exposure. Highest identified source unit remains24published videoIDs. Sharedmean is a transductive reference and zero may be out-of-distribution. CurrentDmulti-event transfer and070remain closed;069writing remains paused; real controlled video reordering remains HOLD. The audit does not establish core innovation or authorize a follow-on task.
