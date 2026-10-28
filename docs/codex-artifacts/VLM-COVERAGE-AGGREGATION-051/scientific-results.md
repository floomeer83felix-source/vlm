# 051 coverage and aggregation results

2026-10-28 (Asia/Shanghai). **NO_MATERIAL_DEPLOYABLE_GAIN under both preregistered development gates.** F48 tied SO at 9/24. Fixed four-view voting reached 10/24, one net correction above SO, with positive gains in only two of four sources. NOVELTY remains RETAIN0.

## Full fixed cohort

Each cell below is correct/N; sources are anonymous aliases. All new model answers were valid; INVALID, FAILED, NOT_RUN and SCORING_UNKNOWN were 0 throughout. V4 uses the fixed highest-vote rule with earliest P0→P3 tie break; it required no extra model call. Old natural outputs were read-only and strictly rescored against the same 24 original labels; all 96 per-question correctness flags agreed with 049, no historical result changed.

| Source | SO | UO=UR | SR | F48 | P0 | P1 | P2 | P3 | V4 | O4* | O5* |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 | 2/6 | 1/6 | 2/6 | 3/6 | 1/6 | 1/6 | 2/6 | 1/6 | 2/6 | 2/6 | 3/6 |
| S02 | 1/6 | 1/6 | 1/6 | 2/6 | 2/6 | 0/6 | 2/6 | 2/6 | 2/6 | 2/6 | 2/6 |
| S03 | 3/6 | 3/6 | 4/6 | 3/6 | 2/6 | 3/6 | 2/6 | 3/6 | 2/6 | 3/6 | 3/6 |
| S04 | 3/6 | 3/6 | 2/6 | 1/6 | 3/6 | 4/6 | 2/6 | 2/6 | 4/6 | 4/6 | 4/6 |
| Total | **9/24** | 8/24 | 9/24 | **9/24** | 8/24 | 8/24 | 8/24 | 8/24 | **10/24** | 11/24 | 12/24 |

*O4/O5 are gold-selected finite-program diagnostics, **not deployable methods**, evidence labels or upper bounds on future methods. Their correctness here was computed only after the real model worker exited. The [48-row CSV](./condition-summary.csv) includes all source×condition states, old-baseline markings and nondeployable oracle markings.

## Prespecified opportunity decisions and paired effects

| Gate | Source-equal net vs SO | Per-source net | Positive sources | Required | Decision |
|---|---:|---|---:|---|---|
| H_F, F48 | **0** | +1/6, +1/6, 0, −1/3 | 2/4 | ≥1/6 and ≥3/4 positive | FAIL |
| H_V, V4 | **1/24 (+4.17 pp)** | 0, +1/6, −1/6, +1/6 | 2/4 | ≥1/6 and ≥3/4 positive | FAIL |

With equal six-question source sizes, the net-gain requirement corresponds to four extra correct answers, rather than the observed zero or one. These gates govern development investment; they are not significance tests or confirmation-set certification. Both are reported against the fixed SO baseline, without selecting a weaker comparator.

In the table below, correction means the first program is correct and the second wrong; harm is the reverse. Each row has the full stated denominator and unknown=0.

| Comparison | Source | Correction | Harm | Both correct | Both wrong |
|---|---|---:|---:|---:|---:|
| F48 vs SO | S01 | 1 | 0 | 2 | 3 |
| | S02 | 1 | 0 | 1 | 4 |
| | S03 | 1 | 1 | 2 | 2 |
| | S04 | 0 | 2 | 1 | 3 |
| | **Total N24** | **3** | **3** | **6** | **12** |
| V4 vs SO | S01 | 1 | 1 | 1 | 3 |
| | S02 | 1 | 0 | 1 | 4 |
| | S03 | 0 | 1 | 2 | 3 |
| | S04 | 1 | 0 | 3 | 2 |
| | **Total N24** | **3** | **2** | **7** | **12** |
| V4 vs F48 | S01 | 0 | 1 | 2 | 3 |
| | S02 | 0 | 0 | 2 | 4 |
| | S03 | 0 | 1 | 2 | 3 |
| | S04 | 3 | 0 | 1 | 2 |
| | **Total N24** | **3** | **2** | **7** | **12** |

All 24 votes had four valid constituents; seven votes were tied at the highest count and resolved by the frozen earliest-view rule. Zero all-invalid votes occurred. No confidence weighting, gold-dependent view selection, judge model or revised tie break was used.

## Finite-program diagnostics

| Source | Full-only | Split-only | Split-only recovered by V4 | Vote-missed | All-five-wrong |
|---|---:|---:|---:|---:|---:|
| S01 | 1 | 0 | 0 | 0 | 3 |
| S02 | 0 | 0 | 0 | 0 | 4 |
| S03 | 0 | 0 | 0 | 1 | 3 |
| S04 | 0 | 3 | 3 | 0 | 2 |
| **Total** | **1** | **3** | **3** | **1** | **12** |

O4=11/24≥V4=10/24 and O5=12/24≥max(F48,V4), also checked per question. Four-view diversity was useful on three S04 questions while voting missed one S03 opportunity. One full-only case does not prove joint reasoning necessary; 12 all-five failures do not prove the 48 candidates lack evidence. These outcomes cannot be converted into selector-training labels or an oracle method score.

## Measured cost and interpretation

These totals cover the fixed 24-question program. Native ordinal timecodes, actual BF16 input tensors and grids were checked before weights; the same model/prompt/generation identity was used throughout.

| Program | Calls | Visual tokens | Full input tokens | Nonvisual input tokens | Generated tokens | CPU processor wall (s) | Generate wall (s) | Prefill / decode within generate (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| F48 | 24 | 31,104 | 39,742 | 8,638 | 48 | 1.016 | 19.999 | 18.267 / 1.403 |
| P0 | 24 | 7,776 | 12,622 | 4,846 | 48 | 0.205 | 5.952 | 4.454 / 1.404 |
| P1 | 24 | 7,776 | 12,622 | 4,846 | 48 | 0.184 | 6.079 | 4.502 / 1.467 |
| P2 | 24 | 7,776 | 12,622 | 4,846 | 48 | 0.219 | 5.988 | 4.455 / 1.441 |
| P3 | 24 | 7,776 | 12,622 | 4,846 | 48 | 0.266 | 5.968 | 4.436 / 1.440 |
| **Four-P/V4** | **96** | **31,104** | **50,488** | **19,384** | **192** | **0.874** | **23.987** | **17.847 / 5.752** |

Nonvisual token counts include wrappers/timecodes and are not solely question-text tokens. V4's generate wall was about 1.20× F48's in this shared run, with four times as many generated tokens/calls. Total measured processor+generate components were 21.015 vs 24.861 seconds. Vote-only overhead, shared loading/transfer/startup/teardown attribution and full standalone deployment wall remain UNKNOWN; neither program was rerun to estimate them. Substage times are contained diagnostics and are not added to the 61.531-second model Job envelope or the 95.764-second total supervised experiment cost.

Thus identical RGB union and total visual tokens do not make equal-cost or equal-organization interventions. Tubelet pairing, native timecodes, sequence length and repeated language prefixes differ. This experiment does not isolate a unique neural fusion cause. The 049 historical baseline already paid for its execution, separately reported there; its cost is neither newly incurred nor assumed free for a deployable system.

## Research disposition

The preregistered result supports stopping further investment in **these fixed all-frame/voting programs as material-gain candidates on this development cohort**. No automatic extension, threshold/prompt/view change, second model, training or additional QA is justified by this parent. This does not establish that better coverage or aggregation can never work. Any future work requires owner review and a separately approved design, rather than relabeling these observations as a positive mechanism.

The same 24 questions and four previously exposed recording aliases are not an independent confirmation sample; physical source independence is uncertified. Resolution is 192×288 and time is an ordinal carrier, not a certified physical-seconds bridge. Scores are development diagnostics, not official HourVideo leaderboard scores. No statistical superiority, natural-long-video generalization, novel selector or core paper mechanism is claimed.049's stopped coordinate hypothesis remains stopped; NOVELTY=RETAIN0.
