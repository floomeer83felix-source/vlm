# 071 frozen selector intervention

2026-11-01 Asia/Shanghai. **COMPLETE_FROZEN_SELECTOR_INTERVENTION / RETROSPECTIVE_DIAGNOSTIC.** All 24 fixed070 heads were evaluated under the two prescribed selector interventions, keeping their original H, question readout and MLP. All28,800 logical cells are CLOSED/valid:9,600 original cached answers,16,800 actual new MLP answers and2,400 exact new-input aliases. No original full answer or original MLP logit was recomputed. There is no new recipe PASS, model ranking or training decision.

## Accuracy changes

Equal-weight mean four-cell all-correct accuracy across the fixed six seeds (%); differences are intervention minus original in percentage points. Each pool retains its50 planned instances. Summing six runs gives300 repeated comparisons, not300 independent sources.

| Pool | Frozen head | Original cached | Train mean | Uniform | Mean−original pp | Uniform−original pp |
|---|---|---:|---:|---:|---:|---:|
| 50Salads | CONCAT | 16.00 | 5.67 | 0.00 | −10.33 | −16.00 |
| 50Salads | FACTOR | 27.67 | 27.00 | 0.33 | −0.67 | −27.33 |
| 50Salads | REVERSE | 16.33 | 0.00 | 0.00 | −16.33 | −16.33 |
| 50Salads | ANCHOR | 30.33 | 31.00 | 0.33 | +0.67 | −30.00 |
| VIDHALLUC | CONCAT | 14.33 | 4.67 | 0.67 | −9.67 | −13.67 |
| VIDHALLUC | FACTOR | 23.33 | 25.67 | 4.00 | +2.33 | −19.33 |
| VIDHALLUC | REVERSE | 13.67 | 0.00 | 0.00 | −13.67 | −13.67 |
| VIDHALLUC | ANCHOR | 22.00 | 22.33 | 5.33 | +0.33 | −16.67 |

FACTOR and ANCHOR retain broadly similar aggregate four-cell scores with the learned training-mean selector, despite substantial changes in attention and individual predictions. This is a description of these fixed heads on already-used items; it is **not** an equivalence finding or proof that semantic information was never used. Their readout still uses the current question's R representation. Uniform weighting causes large accuracy losses. That shows an effect of this specific intervention, not correct event localization or a real-video causal counterfactual.

CONCAT and REVERSE have different original readouts: CONCAT retains both shared and role components, while REVERSE retains the exchange-invariant shared component and originally carries role dependence through selection. Fixing REVERSE's selector removes that role-dependent route; q/tau cells then have identical MLP inputs. The resulting exact aliases and zero four-cell accuracy in all six REVERSE heads are an architectural consequence under these complementary questions, not evidence that all heads use only role readout or that all selector effects are semantic localization.

## Attention changes and changed predictions

These are new071 measurements of original and intervened intermediate weights, not attention cached by070. L1 means cover all200 logical cells per head/pool, averaged equally across six heads; changed percentages use all1,200 repeated cell predictions. No member was selected by correctness.

| Pool | Head | Train-mean changed % | Train-mean mean L1 | Uniform changed % | Uniform mean L1 |
|---|---|---:|---:|---:|---:|
| 50Salads | CONCAT | 25.42 | 0.697 | 42.67 | 1.122 |
| 50Salads | FACTOR | 22.42 | 0.665 | 48.00 | 1.348 |
| 50Salads | REVERSE | 32.83 | 0.838 | 41.50 | 1.028 |
| 50Salads | ANCHOR | 22.00 | 0.679 | 43.67 | 1.398 |
| VIDHALLUC | CONCAT | 26.42 | 0.860 | 39.83 | 1.141 |
| VIDHALLUC | FACTOR | 22.25 | 0.643 | 41.17 | 1.571 |
| VIDHALLUC | REVERSE | 27.75 | 0.917 | 38.92 | 1.058 |
| VIDHALLUC | ANCHOR | 20.83 | 0.689 | 39.33 | 1.493 |

In particular, near-preserved aggregate scores coexist with roughly21–22% changed cell predictions for FACTOR/ANCHOR under TRAIN_MEAN. Gains and harms can offset; the predictions are not identical. Full per-head/pool/intervention L1 mean/median/p95, original/intervention natural-log entropy and changed counts are retained in the [96 attention rows](./attention-summary.csv). The [96 paired rows](./paired-summary.csv) retain independent corrections, harms, zero/negative/positive net changes and descriptive invariance differences. All scores, response patterns, K0…K4 and execution denominators remain in the [144 conditions](./condition-summary.csv), including all48 original cached conditions reproduced from070.

## Exactly32 conditional answer intervals

Intervention−original four-cell accuracy difference; pp, rounded only here. File axis means25 two-instance file families for50Salads and50 file-pair units forVIDHALLUC. Exact unrounded values are in [mean-intervals.csv](./mean-intervals.csv).

| Pool / head / intervention | Point pp | File-axis95% interval | Seed-axis95% interval |
|---|---:|---:|---:|
| 50Salads / CONCAT / mean | −10.33 | [−17.00,−4.67] | [−16.67,−4.00] |
| 50Salads / CONCAT / uniform | −16.00 | [−22.67,−10.00] | [−20.00,−12.00] |
| 50Salads / FACTOR / mean | −0.67 | [−5.33,3.67] | [−4.67,3.33] |
| 50Salads / FACTOR / uniform | −27.33 | [−33.00,−21.67] | [−33.33,−22.00] |
| 50Salads / REVERSE / mean | −16.33 | [−23.67,−9.67] | [−17.67,−14.33] |
| 50Salads / REVERSE / uniform | −16.33 | [−23.67,−9.67] | [−17.67,−14.33] |
| 50Salads / ANCHOR / mean | +0.67 | [−3.00,4.33] | [−4.33,5.33] |
| 50Salads / ANCHOR / uniform | −30.00 | [−35.67,−24.67] | [−35.00,−25.00] |
| VIDHALLUC / CONCAT / mean | −9.67 | [−14.67,−5.00] | [−12.00,−7.67] |
| VIDHALLUC / CONCAT / uniform | −13.67 | [−19.33,−8.67] | [−19.67,−9.67] |
| VIDHALLUC / FACTOR / mean | +2.33 | [−2.00,6.33] | [−6.33,10.00] |
| VIDHALLUC / FACTOR / uniform | −19.33 | [−24.67,−14.33] | [−25.67,−14.33] |
| VIDHALLUC / REVERSE / mean | −13.67 | [−20.33,−8.00] | [−16.33,−10.67] |
| VIDHALLUC / REVERSE / uniform | −13.67 | [−20.33,−8.00] | [−16.33,−10.67] |
| VIDHALLUC / ANCHOR / mean | +0.33 | [−4.00,4.67] | [−2.67,4.00] |
| VIDHALLUC / ANCHOR / uniform | −16.67 | [−22.00,−12.00] | [−20.33,−12.67] |

All304 fixed seed-sum bins, including zero frequencies, are in the [difference histogram](./difference-histogram.csv). Each histogram frequency sum is25 or50 and its weighted sum matches the six-seed paired net. Random55072/55073,10,000 draws per pool/axis and linear(10000−1)p quantiles were unchanged. Canonical separate marginal expansions do not preserve actual cross-intervention/arm member alignment; these are not joint interaction or mixed-pool intervals. No p-values, subgroup, response or per-seed CI was added. An interval including zero is not a test of equivalence.

## Interpretation and scope

TRAIN_MEAN is a single vector for each fixed final head: the84 original sorted training questions are individually projected/nonlinearized in float32, averaged in float64, then converted to float32. It is not a mean input passed through GELU, and no evaluation data or labels fit it. Its attention still depends on each video's H/content/position. UNIFORM directly sets six float32 weights to1/6, but H retains original temporal position/conv information and the signed temporal moment remains. Neither intervention is a no-vision or no-time model.

Only alpha changes; H/g_read/MLP, states, views, anchors, threshold and membership are fixed. Original alpha and MLP-input geometry were newly reconstructed to support intervention and exact aliasing; no original logit evidence exists, so no original logit change is reported. All original answers came from sealed070 predictions. Of19,200 logical interventions,16,800 have one actual new MLP answer and2,400 inherit the earliest same-state, byte-identical, element-equal new input. There were no actual original-input aliases, no approximate cache matches, forced complements or label-based alias decisions.

The independent verifier passed146,393 checks of states/seals, saved mean/geometry identities, alias graph/thresholds/keys, labels and all144/96/96/304/32 tables, using no scorer import or learned forward. It independently checked aggregation/bootstrap and saved-intermediate algebra, **not** a replay of learned conv/projection/MLP. Static/source provenance and intermediate checks are not independent reproduction of every learned operation.

Both50 pools were already scored; physical source/pretraining independence and three-event selectivity remain unconfirmed. No best head or selector is selected, ANCHOR is not promoted,070's STOP_THIS_RECIPE is unchanged,069 stays paused, and no training/writing/automatic072 follows. See [execution receipt](./execution-receipt.md) for complete costs and limitations.
