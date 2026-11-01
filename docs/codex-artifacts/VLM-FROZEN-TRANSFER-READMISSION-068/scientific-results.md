# 068 fixed frozen item-transfer results

2026-11-01 Asia/Shanghai. **COMPLETE_FROZEN_ITEM_TRANSFER / POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE.** All 2,400 new single-cell predictions are CLOSED and valid. On the fixed 50 VIDHALLUC two-video instances, the six frozen D heads improve four-cell all-correct accuracy over the matching C heads by a mean **11.00 percentage points**. Mean C accuracy is **1.33%**, mean D **12.33%**. Absolute accuracy remains low; this is no mechanism PASS, independent-source confirmation or revision of the original 063 20% target failure.

| Frozen seed | C four-cell correct /50 | D four-cell correct /50 | D−C instances | D−C pp |
|---|---:|---:|---:|---:|
| 137 | 1 | 8 | +7 | +14 |
| 263 | 0 | 7 | +7 | +14 |
| 419 | 0 | 6 | +6 | +12 |
| 557 | 0 | 2 | +2 | +4 |
| 733 | 1 | 7 | +6 | +12 |
| 911 | 2 | 7 | +5 | +10 |

All six differences are positive, with no new seed/checkpoint selection. The six-seed repeated comparison totals are 36 D-only correct, three C-only correct, one both correct and 260 both wrong. These 300 comparisons reuse the same 50 instances and are not 300 independent sources. The 600 method/seed four-cell evaluations are also repeated runs, not new instances.

Mean single-cell accuracy is C 49.33%, D 53.58% (+4.25 pp). Seed557 is retained despite its single-cell deterioration from 99/200 to 98/200; its D four-cell accuracy is only 2/50. Seed911 single-cell accuracy is unchanged at 100/200 despite a four-cell increase. No negative or zero cell-level result was removed.

Question-invariant responses fall from mean C 71% to D 30%, a D−C change of **−41 pp** (negative means less question invariance). Per-seed invariant count differences are −22/−21/−16/−23/−20/−21 out of 50. This response change cannot substitute for answer accuracy. Single-cell, video-pair, question-pair, K0…K4 and all five response-pattern counts remain in the [12-condition table](./condition-summary.csv); corrections and harms remain in the [six-pair table](./paired-summary.csv).

| Metric, D−C | Fixed-six-head paired-unit axis, 95% interval (pp) | Fixed-50-item seed axis, 95% interval (pp) |
|---|---:|---:|
| Four-cell all-correct; point +11 | [5.00, 17.67] | [8.00, 13.33] |
| Question invariance; point −41 | [−50.00, −32.00] | [−44.00, −37.00] |

Exactly the original two 13-bin seed-sum histograms and four intervals were computed: Random55066 for 10,000 paired-unit draws from canonical separate marginal expansions; Random55067 for 10,000 whole-seed draws; linear quantiles at position=(10000−1)p. Histograms each sum to 50; weighted sums are +33 answer instances and −123 invariant instances across the six paired comparisons. Marginal canonical expansions do not preserve actual cross-metric member alignment, so these are not a joint bootstrap or interaction analysis. There are no per-seed intervals, p-values, additional axes or revised decision threshold. Exact unrounded values are in [mean intervals](./mean-intervals.csv) and the [26-bin frequency table](./difference-histogram.csv).

The original 066 membership, tau strings, 12 old final states, original head architecture/356,673 parameters, strict logit>0, and frozen train84 mu/scalar RMS were unchanged. C uses h(q); D uses [h(q)−h(tau(q))]/2, followed by original float64 normalization and float32 head input. No training, head warmup, loss, optimizer, refitting, new B0 or sampling change occurred. The observation, GPU/prediction and scoring roles were separated; publisher answers were parsed only after all output sealing and prediction Job actual active zero. Inference never consulted another cell's output.

The revised resource gate passed before new outputs: all 100 directory records were saved first, with total compressed 404,959,596 B and uncompressed 407,278,699 B. One member exceeds the old 32 MiB compression threshold and none the old 64 MiB uncompressed threshold. This is a new 068 same-version directory measurement; 067's missing values and NA result remain unchanged. See [media admission](./media-admission-summary.json).

The scientific scope remains **publisher-QA-level item transfer**. Strict event non-overlap/chronology, original recording independence and pretraining independence are not certified. Exact old media/RGB/logical-input collisions were not found; old pixel/token summaries are absent and those levels remain UNKNOWN, without rerunning old inputs. Public publisher answers were previously visible; this is not a new blind test. A positive conditional mean does not establish a core innovation or repair 063's failed absolute target. No tuning or pool expansion follows this result.

Separately sealed independent verification completed **5,359 checks**, rebuilt all four table families from the publisher labels and sealed new outputs, and checked states/transforms/identities/journals/input facts and operational bounds without importing the scorer, forwarding a model or decoding again. The pre-decode static/integer checks and one synthetic CPU processor fixture are software evidence only. Read accounting and verification limits are in the [execution receipt](./execution-receipt.md). This parent ends with its single safe delivery; no automatic 069.
