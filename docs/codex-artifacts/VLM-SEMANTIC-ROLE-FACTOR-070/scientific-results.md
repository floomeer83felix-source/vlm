# 070 semantic/role routing pilot

2026-11-01 Asia/Shanghai. **COMPLETE_CPU_MECHANISM_PILOT / NO_SUPPORT_FOR_THIS_FACTORED_ROUTING / STOP_THIS_RECIPE.** All 24 configurations completed their fixed 250 CPU updates, all 22,368 new predictions were sealed, and all 11,184 cached C/D predictions were reproduced. The candidate fails the preregistered all-controls gate. No tuning, extra seed, new data or continuation follows this result; 069 remains paused.

FACTOR improves mean four-cell accuracy over old D, CONCAT and REVERSE in both already-used 50-item pools. Those gains are retained. However, its advantage over a **different-event-pair training anchor** is not stable, and it fails the required positive-seed count against D in the 50Salads pool. Higher mean accuracy or passing the new absolute floor cannot rescue these failed controls.

## Complete descriptive results

Mean four-cell all-correct accuracy (%), equal weight across the fixed six seeds:

| Split | C cached | D cached | CONCAT | FACTOR | REVERSE | ANCHOR |
|---|---:|---:|---:|---:|---:|---:|
| train68 | 97.79 | 98.77 | 99.26 | 96.81 | 99.75 | 98.53 |
| validation11 | 42.42 | 40.91 | 37.88 | 46.97 | 40.91 | 33.33 |
| development54 | 18.83 | 24.07 | 25.62 | 31.79 | 26.23 | 37.96 |
| source_holdout50 / 50Salads | 5.00 | 17.67 | 16.00 | 27.67 | 16.33 | 30.33 |
| item_transfer50 / VIDHALLUC | 1.33 | 12.33 | 14.33 | 23.33 | 13.67 | 22.00 |

All train/validation/development conditions are reported, without subgroup selection. These secondary summaries did not select a checkpoint or modify the gates. The full [180-condition table](./condition-summary.csv) retains every seed, all planned/new/cached/status denominators, single-cell/video-pair/question-pair/four-cell accuracy, question invariance, K0…K4 and five response patterns. The [60 paired rows](./paired-summary.csv) retain corrections, harms, zero/negative differences and descriptive question-invariance differences, including C context comparisons.

The per-seed primary-pool four-cell counts, in fixed order 137/263/419/557/733/911, are:

| Pool | C cached | D cached | CONCAT | FACTOR | REVERSE | ANCHOR |
|---|---|---|---|---|---|---|
| 50Salads, each /50 | 3/6/1/1/2/2 | 10/10/10/6/8/9 | 7/9/4/7/9/12 | 16/10/15/20/13/9 | 9/9/9/8/6/8 | 11/13/17/17/13/20 |
| VIDHALLUC, each /50 | 1/0/0/0/1/2 | 8/7/6/2/7/7 | 7/5/5/6/4/16 | 9/21/12/8/10/10 | 6/6/9/4/8/8 | 9/12/12/11/13/9 |

## Fixed gate: both pools fail

Totals below sum six matched-seed net instance differences. They are repeated comparisons, not independent sources. D/CONCAT require at least five positive seeds and total net≥18; REVERSE/ANCHOR require at least four and total net≥9. Each pool also requires FACTOR total correct≥60 across six runs. All comparisons use integers before percentage display.

| Pool | FACTOR versus | Positive seeds /6 | Total net | Mean difference pp | Gate |
|---|---|---:|---:|---:|---|
| 50Salads | D cached | 4 | +30 | +10.00 | **FAIL: positive seeds** |
| 50Salads | CONCAT | 5 | +35 | +11.67 | PASS |
| 50Salads | REVERSE | 6 | +34 | +11.33 | PASS |
| 50Salads | ANCHOR | 2 | −8 | −2.67 | **FAIL: both requirements** |
| VIDHALLUC | D cached | 6 | +33 | +11.00 | PASS |
| VIDHALLUC | CONCAT | 5 | +27 | +9.00 | PASS |
| VIDHALLUC | REVERSE | 6 | +29 | +9.67 | PASS |
| VIDHALLUC | ANCHOR | 2 | +4 | +1.33 | **FAIL: both requirements** |

FACTOR absolute totals are 83/300 (27.67%) and 70/300 (23.33%), both meeting this new pilot's floor. Source D comparisons include two ties, not six improvements. The item CONCAT comparison includes a negative seed911 difference; the source ANCHOR comparison includes a −11-instance seed911 difference. All remain in the tables. The current new candidate's absolute results do not retrospectively revise 063's failed old-D 20% target.

## Exactly sixteen fixed intervals

FACTOR−control mean four-cell difference, percentage points; rounded here only. Each cell shows [2.5%,97.5%]. Exact values, including fractional interpolation endpoints, are in [mean-intervals.csv](./mean-intervals.csv).

| Pool / control | Point pp | File-family or file-pair axis | Whole-seed axis |
|---|---:|---:|---:|
| 50Salads / D cached | +10.00 | [3.33,17.00] | [3.33,17.67] |
| 50Salads / CONCAT | +11.67 | [5.67,17.67] | [2.33,20.67] |
| 50Salads / REVERSE | +11.33 | [4.67,18.00] | [5.67,17.00] |
| 50Salads / ANCHOR | −2.67 | [−8.33,3.67] | [−11.33,4.67] |
| VIDHALLUC / D cached | +11.00 | [4.00,17.34] | [5.33,18.33] |
| VIDHALLUC / CONCAT | +9.00 | [3.33,14.33] | [−1.33,19.67] |
| VIDHALLUC / REVERSE | +9.67 | [3.00,15.67] | [4.67,18.00] |
| VIDHALLUC / ANCHOR | +1.33 | [−5.67,8.00] | [−4.00,8.33] |

Exactly 152 public frequency bins support these intervals: four controls ×25 bins for 25 original two-instance 50Salads file families, plus four ×13 bins for 50 VIDHALLUC file-pair units. Every zero-frequency bin is retained. Each histogram's weighted sum matches its six-seed net total. Per pool, Random55070 generated 10,000 shared canonical-index draws; Random55071 generated 10,000 shared whole-seed draws, with the fixed denominator300 and linear quantile position=(10000−1)p. Canonical histogram expansions describe separate marginals and do not preserve actual cross-control member alignment. No joint bootstrap, response/C/per-seed interval, p-value or new subgroup test was added.

## What was tested and what stops

All four new heads have 356,673 parameters and original056 keys/shapes, video/position/LN/conv/MLP. Two 32-row slices of the existing question projection provide the shared-component and role projections. FACTOR uses the repeated shared component for temporal weighting and repeated role component for readout. REVERSE exchanges duties; ANCHOR replaces the selector's shared component with a fixed different-event-pair training anchor. CONCAT is **parameter-matched 32+32 block projection concatenation**, not an unrestricted 5120→64 projection. This architectural limitation is essential when interpreting its contrast.

The shared component is an exchange-invariant average, not proven pure semantics. R uses the exact frozen old D normalizer; its centered values and the output are not forced to be antisymmetric. Only the new shared-component mean/scalar RMS was fit, on the original 84 training questions. Anchors come from the original 42 training canonical pairs, selected without labels/scores; they may share an event with the current pair and are not certified completely unrelated semantics. No unused parameters, forced complementary answers, cross-cell output repair or event-boundary input was introduced.

The failed anchor controls do not support the claimed specific value of using the current event pair's shared component for selection in this recipe. They do not prove all possible semantic/role decompositions impossible, nor identify a causal explanation. Observed accuracy gains and a positive interval against a weaker control are insufficient to retain this mechanism under the fixed all-controls gate.

Both primary pools were already scored before 070; this is development screening, not blind confirmation. File families/pairs do not certify original-recording or participant independence. Two-event complementary questions and six tubelets do not establish three-event selectivity, event localization, causal mechanism or algorithmic originality. Full scientific disposition is **STOP_THIS_RECIPE**; no favorable seed/control is renamed a contribution. No paper work, further head, extra training or automatic071 follows.

Independent verification completed **48,566 checks**, rebuilding all 180/60/152/16 tables and gates from sealed outputs and labels, without importing the scorer or rerunning a forward/optimizer. See [execution receipt](./execution-receipt.md) for identities, provenance fallback, role isolation and resource-accounting limits.
