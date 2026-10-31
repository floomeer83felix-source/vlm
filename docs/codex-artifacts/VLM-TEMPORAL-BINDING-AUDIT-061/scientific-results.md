# 061 cached response and transfer audit

2026-10-31 Asia/Shanghai. **COMPLETE_CACHED_RESPONSE_AUDIT / CAUSAL_BOTTLENECK_UNRESOLVED / NO_NEW_METHOD_CLAIM.** This is a read-only diagnostic of060's fixed outputs and features; no new answer, training or method result. The060 A-pool gate failure and057/059 closed recipes remain unchanged.

## Response decomposition

For the already-used source holdout, every row has N50 four-cell instances (200 answers). B0 is one NA-seed condition, never duplicated by seed.

| Method | Seed | Constant | Video only | Question only | Checkerboard correct / inverted | Mixed | Q-invariant | V-invariant |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A25 | 19 | 20 | 20 | 3 | 3 / 0 | 4 | 80% | 46% |
| A25 | 73 | 10 | 27 | 2 | 2 / 1 | 8 | 74% | 24% |
| P1_25 | 19 | 3 | 31 | 2 | 1 / 0 | 13 | 68% | 10% |
| P1_25 | 73 | 5 | 28 | 1 | 4 / 3 | 9 | 66% | 12% |
| A68 | 19 | 14 | 25 | 2 | 3 / 0 | 6 | 78% | 32% |
| A68 | 73 | 13 | 33 | 1 | 0 / 2 | 1 | 92% | 28% |
| P1_68 | 19 | 6 | 24 | 1 | 5 / 3 | 11 | 60% | 14% |
| P1_68 | 73 | 5 | 26 | 0 | 4 / 4 | 11 | 62% | 10% |
| B0 | NA | 11 | 0 | 12 | 7 / 0 | 20 | 22% | 46% |


The eight small-head configurations predominantly fail to change with the complementary question: Q-invariance is60–92%, compared with V-invariance10–46%. VIDEO_ONLY is the largest or tied-largest individual class for all eight heads; CONSTANT also contributes to both invariance measures. A25→A68 Q-invariance changes80→78% for seed19 and74→92% for seed73. This is a behavior-level question-axis response shortfall, not proof that the q feature, a connector, event recognition or a specific layer caused it.

Both-axis checkerboards remain uncommon for the heads (1–8 of50). Among P1_68's eight checkerboards per seed,3 and4 are fully inverted; A68 seed73 has two checkerboards and both inverted. Checkerboard behavior alone is not answer correctness. No test-label flips, complementary repairs, projections or oracle correction scores were computed.

B0 differs:46% V-invariant,22% Q-invariant and40% MIXED; its seven checkerboards are all correct. Thus the heads' dominant pattern is not automatically the same as B0's, and neither axis summary identifies a causal mechanism. CONSTANT belongs to both invariance sets; these rates are not disjoint probabilities.

All6056 CLOSED strictly binary predictions and1514 four-way instances were retained. The33 condition rows reproduce060's original N/cell/complete/valid/unknown, item, video-pair, question-pair and four-way correct counts. K0–K4, all five types, correct/inverted checkerboards and both edge counts satisfy the frozen identities. These are algebraic descriptions of the same patterns, not multiple independent discoveries. Full33-condition counts, including all68/11/54 split configurations, are in the CSV/JSON; no favorable seed or response subset was selected.

## Fixed descriptive cluster intervals

| Difference | Seed | Q-invariance difference, pp [95% interval] | V-invariance difference, pp [95% interval] |
|---|---:|---:|---:|
| A68 − A25 | 19 | -2 [-14, +10] | -14 [-34, +6] |
| P1_68 − P1_25 | 19 | -8 [-28, +10] | +4 [-10, +18] |
| A68 − A25 | 73 | +18 [+6, +28] | +4 [-14, +22] |
| P1_68 − P1_25 | 73 | -4 [-22, +14] | -2 [-8, +4] |


Positive differences mean more invariance, not improved accuracy. A68 seed73's+18pp Q-invariance interval excludes0 in this descriptive calculation; it indicates less question change in that seed, not a new benefit. P1's Q-invariance decreases have intervals containing0. No new pass/fail or significance gate is introduced.

All18 marginal and8 paired intervals are in the JSON, in proportion units. Exactly one Random55061 stream produced10000 common choices(range25,k25) draws for all26 statistics; two members per sampled file family retained, actual sampled N, linear2.5/97.5% quantiles. Paired differences use the same clusters jointly. The225 public source rows contain only the five label-blind type counts, with a consistent anonymous F01–F25 mapping, and independently reproduce all26 intervals. File families, four cells and two seeds do not create independent original sources or verified participant/kitchen identities.

## Exact collisions and cached geometry

| Split | N | q distance median | Ordered V distance median | Best720-permutation distance median | Temporal variation median | Exact-collision union | Necessary head upper bound | Unique V / slots |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| train_pool68 | 68 | 0.047230 | 0.134372 | 0.080474 | 0.027849 | 0 | 68 | 136 / 136 |
| validation11 | 11 | 0.044507 | 0.136746 | 0.078629 | 0.026657 | 0 | 11 | 22 / 22 |
| development54 | 54 | 0.046074 | 0.137026 | 0.086431 | 0.027507 | 0 | 54 | 108 / 108 |
| source_holdout50 | 50 | 0.043680 | 0.128846 | 0.084233 | 0.025289 | 0 | 50 | 100 / 100 |


Within every complementary instance, q0/q1 and ordered V0/V1 are never exactly equal. No q relative distance is≤1e−4. The exact-collision union is0 in each split, leaving only the trivial necessary deterministic-head upper bounds68/11/54/50; no low ceiling from this test explains the observed failures. This does not show that the features preserve the needed semantic/time information or that an effective readout is learnable. The bound concerns a deterministic current-V/q head, not B0's RGB/original-question input or other representations.

All numerical geometry is float64 with denominator epsilon1e−12. The ordered Frobenius distance and minimum over all720 six-row assignments use the fixed formula; the minimum is computed from the6×6 squared row-cost matrix without approximating the permutation search. Time variation is the per-video centered energy ratio across six units; the table reports medians and the JSON all five fixed quantiles (0,.25,.5,.75,1). The2N video slots and their unique counts are not independent samples. Segment swapping is not framewise video reversal, and matching time rows is not action localization. Relative distances, including q distances, do not diagnose semantic absence or cross-modal alignment.

## Training-string coverage

| Split | N | Pair seen | Both events seen, pair new | One event seen | No event seen | q slots / unique strings |
|---|---:|---:|---:|---:|---:|---:|
| train_pool68 | 68 | 68 | 0 | 0 | 0 | 136 / 84 |
| validation11 | 11 | 8 | 2 | 1 | 0 | 22 / 18 |
| development54 | 54 | 28 | 19 | 7 | 0 | 108 / 74 |
| source_holdout50 | 50 | 0 | 0 | 0 | 50 | 100 / 88 |


Both normalized event strings in every source-holdout pair are absent fromtrain68:50/50 NO_EVENT_SEEN. This is a complete literal-string coverage gap for this split, not merely unseen event-pair combinations. It constrains interpretation of transfer, but does not establish that lexical coverage caused the failure, that action semantics were unseen, or that Qwen pretraining did not expose them. No accuracy-by-coverage strata or label-based vocabulary selection was computed.

Only frozen question strings were parsed; normalization is underscore→space, whitespace collapse and casefold, with no synonym/stem/LLM rewrite. Unordered pairs remain length2 tuples retaining both event positions. Normalized equal-event instances are0 in every split and no instance was removed. Train68 is the only coverage reference. All original/de-duplicated question counts are retained; global366 question slots use220 distinct cached strings.

The audit identifies a dominant question-response pattern for these heads plus a source literal-vocabulary gap; it does not separate feature content, alignment, optimization, source coverage or publisher-label quality causally. No new mechanism, tuning, architecture/loss search, GPU experiment or automatic062 follows. TimeBlind NOT_RUN.
