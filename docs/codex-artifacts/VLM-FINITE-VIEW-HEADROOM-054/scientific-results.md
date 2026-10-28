# 054 finite-view headroom and ranking

2026-10-28 (Asia/Shanghai). **SIMPLE_CONFIDENCE_USES_MOST_HEADROOM.** Within the fixed053 fill128 table, O15 covers13/24 versus F9/24: four recoverable F errors across three sources. Nongold E15 recovers3 of those4, misses1, and harms2 F-correct questions, yielding10/24. The frozen ranking-gap criterion requires at least2 missed recoverable errors; it is not met. This does not validate E15 as a deployable method, reverse053's stop decision or establish innovation.

## Three questions answered

**Finite correct output exists for how many questions?** O15=13/24. F is one of the15 allowed nonempty states, so H=13−9=4. Source gains are1,0,1,2, covering3/4 sources. Eleven questions have no correct top1 in these15 states. That absence does not prove missing natural evidence, model impossibility or a bound on future observations/methods.

**How much does fixed confidence use?** E15 is the highest measured top1-margin state among all15, with exact larger-cardinality/smaller-mask/earlier-letter ties, frozen before labels. It uses no second-fill gate and is an explicitly post-hoc control, not an improvement to the same053 gated method. It recovers3 errors and harms2 successes: net+1. The O15−E15 difference of3 is **one missed recovery plus two harms**, not three missed recoverable F errors.

**How do I/A estimates correspond to their selected state's response?** I's candidate disagrees with that state's measured top1 once; it agrees but is wrong15 times and agrees/correct8 times. A has the corresponding2/14/8 split. These are candidate categories, not final-answer errors or a causal decomposition. Old final I8/A10 and changed counts3/5 remain separate and unchanged.

## Fixed24-question/source results

All cells are correct/N. No unknown scores, missing joins or old-correctness discrepancies occurred. Old six-method outputs were checked individually against the same original24 labels, with zero mismatches; the labels did not enter E15 selection.

| Source | F | M | A | I | C | R | E15* | B0** | O15 / O1 / O2 / O3*** |
|---|---|---|---|---|---|---|---|---|---|
| S01 | 2/6 | 2/6 | 3/6 | 2/6 | 2/6 | 2/6 | 2/6 | 2/6 | each3/6 |
| S02 | 2/6 | 1/6 | 2/6 | 2/6 | 2/6 | 2/6 | 2/6 | 1/6 | each2/6 |
| S03 | 3/6 | 3/6 | 2/6 | 2/6 | 3/6 | 4/6 | 3/6 | 1/6 | each4/6 |
| S04 | 2/6 | 1/6 | 3/6 | 2/6 | 3/6 | 3/6 | 3/6 | 1/6 | each4/6 |
| **ALL** | **9/24** | **7/24** | **10/24** | **8/24** | **10/24** | **11/24** | **10/24** | **5/24** | **each13/24** |

*E15: POSTHOC_UNGATED_CONFIDENCE_CONTROL. **B0: MASKED_CONTROL, all128 RGB fill with48 slots/1296 visual tokens and the same positional carrier; it is not a no-video/text-only input. ***O15/O1/O2/O3: FINITE_GOLD_ORACLE_NOT_DEPLOYABLE; no answer-aware choice is a usable policy. Cardinality-specific oracles need not be monotonic; their equal coverage here is an observation, not an assumption or independent replication. Full60 condition rows and kinds/unknown counts are in [finite-view-summary.csv](./finite-view-summary.csv).

## Recovery, harm and minimum successful cardinality

| Source | N | F | O15 | E15 | H | Recovered | Harm | Missed | K1 | K2 | K3 | K4 | NONE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S01 | 6 | 2 | 3 | 2 | 1 | 1 | 1 | 0 | 3 | 0 | 0 | 0 | 3 |
| S02 | 6 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 4 |
| S03 | 6 | 3 | 4 | 3 | 1 | 1 | 1 | 0 | 4 | 0 | 0 | 0 | 2 |
| S04 | 6 | 2 | 4 | 3 | 2 | 1 | 0 | 1 | 4 | 0 | 0 | 0 | 2 |
| **ALL** | **24** | **9** | **13** | **10** | **4** | **3** | **2** | **1** | **13** | **0** | **0** | **0** | **11** |

H=O15−F≥0; missed=H−recovered≥0; E15−F=recovered−harm hold both overall and per source. ALL is the source sum, while the count of sources with H>0 is separately3. The [five-row headroom/ranking table](./headroom-and-ranking.csv) also includes every I/A category and final-result count.

Every question with any successful nonempty state also has at least one successful single-retained-block state. Hence minimum successful K is1 for13 questions and NONE for11. This is a finite masked-response property: each such input still has48 positions, including gray-filled blocks. K is not MRFS, a necessary-evidence annotation, a universal minimum frame count or proof that the retained pixels caused correctness. O1/O2/O3 do not create separate samples or get summed into a new question denominator.

## I/A candidate correspondence versus final output

Each triple below is (candidate differs from selected state's measured top1, top1 agrees but answer wrong, top1 agrees and answer correct). Triples partition all questions. Final correct/change counts refer to frozen053 outputs after its original gate.

| Source | I category triple | I final correct/N | I changed | A category triple | A final correct/N | A changed |
|---|---|---|---:|---|---|---:|
| S01 | (0,4,2) | 2/6 | 2 | (0,3,3) | 3/6 | 1 |
| S02 | (1,3,2) | 2/6 | 0 | (0,5,1) | 2/6 | 1 |
| S03 | (0,4,2) | 2/6 | 1 | (1,3,2) | 2/6 | 1 |
| S04 | (0,4,2) | 2/6 | 0 | (1,3,2) | 3/6 | 2 |
| **ALL** | **(1,15,8)** | **8/24** | **3** | **(2,14,8)** | **10/24** | **5** |

Agreement between an estimated candidate and an actual state response is not agreement with truth. Conversely candidate mismatch is not automatically the final policy's error: the old policy may fall back to F. These descriptions do not license counterfactual changes to old selections or an attribution of failure to visual evidence, interference or fusion.

## Target-score rank and margin descriptions

Ranks sort raw five-option log scores descending, breaking exact ties A–E. Target margin is the gold option's score minus its strongest rival; no new normalization, threshold or selection rule is learned. Quantiles are frozen linear type7. The following pool score vectors; **the statistical question unit remains24**, not360/384.

| States | Vectors | Target-rank counts1/2/3/4/5 | Margin min | Q25 | Median | Q75 | Max |
|---|---:|---|---:|---:|---:|---:|---:|
| All16, including gray control | 384 | 134/81/53/79/37 | −10.500000 | −4.375000 | −1.500000 | 0.875000 | 5.375000 |
| Nonempty only | 360 | 129/79/46/73/33 | −8.750000 | −4.375000 | −1.437500 | 1.000000 | 5.375000 |
| Empty gray control | 24 | 5/2/7/6/4 | −10.500000 | −5.937500 | −2.875000 | −0.437500 | 1.750000 |
| One retained block | 96 | 29/25/13/20/9 | −8.750000 | −4.500000 | −1.625000 | 0.625000 | 4.875000 |
| Two retained blocks | 144 | 53/29/20/30/12 | −7.500000 | −4.250000 | −1.375000 | 0.875000 | 5.000000 |
| Three retained blocks | 96 | 38/19/11/19/9 | −7.500000 | −4.187500 | −1.187500 | 1.125000 | 5.375000 |
| Full | 24 | 9/6/2/4/3 | −6.750000 | −3.968750 | −1.000000 | 1.218750 | 4.750000 |

All35 source/cardinality rank-margin profiles, including their question denominators and vector counts, are provided in JSON. No per-question ranks, target labels, scores or mask-to-answer mapping is public. These state-wise descriptions are neither calibration claims nor evidence for a newly tuned rank selector.

## Frozen decision and stop

The finite-space opportunity threshold is met exactly: H=4 and three positive-headroom sources. The next frozen condition, missed≥2, fails because missed=1. Therefore the prescribed result is **SIMPLE_CONFIDENCE_USES_MOST_HEADROOM**. That name concerns recovery coverage: the two harms remain material, and net gain is only1. It is not a deployment GO or a claim that confidence solves the task.

This is a post-hoc analysis of already paid, already exposed model states, with one unchanged original-label read and zero new model/processor/GPU/visual-array operations. It neither restores I nor promotes E15/R into a novel candidate. The same fixed24 questions, four nominal recordings, sparse low-resolution cache, ordinal clock and one known time-scope caveat remain. No cleaned23-question primary result, statistical significance, independent-source validation or future-method upper bound is claimed. All outputs end in STOP; no automatic055, model, new observation, threshold, training or data acquisition.
