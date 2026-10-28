# 053: block interaction does not pass the development gates

2026-10-28 (Asia/Shanghai). **STOP_CURRENT_ROUTER / NOVELTY=UNRESOLVED.** The complete fixed24-question comparison returned all437 new model forwards and144 method outputs, with no missing/invalid score. Interaction router I answered8/24, below new full-input baseline F9/24, additive A10/24, confidence C10/24 and fixed search R11/24. Every preregistered I gate fails.

These are six **new, shared likelihood-readout** methods: actual assistant prefix Answer: and five qualified single-token continuations, one use_cache=False forward per distinct input. Old free-generation scores are not the baselines for these differences. M is contiguous-block masked-input voting, not051's interleaved12-frame V4.

## Complete fixed denominators

All cells below are correct/N. Every method retains24 questions/four sources each6, including the predeclared052 scope caveat. INVALID, FAILED, NOT_RUN and SCORING_UNKNOWN are0 for every method/source row. There is no cleaned subset or selected source.

| Source | F full | M block vote | A additive | I interaction | C confidence | R fixed search |
|---|---|---|---|---|---|---|
| S01 | 2/6 | 2/6 | 3/6 | 2/6 | 2/6 | 2/6 |
| S02 | 2/6 | 1/6 | 2/6 | 2/6 | 2/6 | 2/6 |
| S03 | 3/6 | 3/6 | 2/6 | 2/6 | 3/6 | 4/6 |
| S04 | 2/6 | 1/6 | 3/6 | 2/6 | 3/6 | 3/6 |
| **ALL** | **9/24** | **7/24** | **10/24** | **8/24** | **10/24** | **11/24** |

The [30-row condition table](./condition-summary.csv) includes all states. The [25-row paired table](./paired-summary.csv) includes every I-comparator/source cell; all unknown counts are0. ALL is the four-source sum, not an extra sample.

| I versus | Correction | Harm | Both correct | Both wrong | Net correct | Required net | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| F | 1 | 2 | 7 | 14 | **−1** | ≥4, plus≥3 positive sources | FAIL |
| A | 0 | 2 | 8 | 14 | **−2** | ≥2 | FAIL |
| C | 0 | 2 | 8 | 14 | **−2** | ≥2 | FAIL |
| R | 0 | 3 | 8 | 13 | **−3** | ≥2 | FAIL |
| M | 2 | 1 | 6 | 15 | **+1** | ≥2 | FAIL |

| Source | I−F | I−A | I−C | I−R | I−M |
|---|---:|---:|---:|---:|---:|
| S01 | 0 | −1 | 0 | 0 | 0 |
| S02 | 0 | 0 | 0 | 0 | +1 |
| S03 | −1 | 0 | −1 | −2 | −1 |
| S04 | 0 | −1 | −1 | −1 | +1 |

I−F has **0/4 positive sources**, below the required3/4. The slight advantage over M also fails its independently fixed requirement. These are development investment rules, not statistical significance tests, broad equivalence proofs or an authorization to promote the best control into a new experiment.

## Did the interaction term contribute useful changes?

I and A selected different (answer,mask) pairs on21/24 questions, with different masks on21 and different candidate answers on8. After the common two-fill gate, final outputs differed on only4. Of those4, A alone was correct on2 and both were wrong on2; I alone was correct on0. Thus selection movement did not establish a beneficial answer-level interaction effect; paired net I−A is−2.

| Method | Candidate already F | Checked change proposals | Accepted changes | Rejected→F | Fill-top disagreement among checked | Selected full |
|---|---:|---:|---:|---:|---:|---:|
| A | 16 | 8 | 5 | 3 | 1 | 1 |
| I | 20 | 4 | 3 | 1 | 0 | 1 |
| C | 18 | 6 | 6 | 0 | 0 | 1 |
| R | 19 | 5 | 5 | 0 | 0 | 2 |

Checked change proposals require both observed fills and the strict margin rule; candidate-already-F terminates without such a requirement. I's3 accepted changes comprise1 correction and2 harms relative to F. Agreement across the two fills and larger model margins therefore did not guarantee truth. The non-full I rejection did not have top disagreement between fills, but it failed candidate/top or margin requirements. No threshold, tie policy or output was revised after seeing labels.

## Approximation diagnostics are not accuracy gains

Errors below are estimated minus measured **five-option normalized model log scores**. Each triple row pools24×4×5=480 score components; each raw-full row pools24×5=120. These are not additional independent questions or model calls. Triple states were collected for validation but withheld from the I/A/C routing interfaces. R has only its separately fixed observations.

| Estimator | Validation set | Components | MAE | RMSE | Mean signed error | Max absolute |
|---|---|---:|---:|---:|---:|---:|
| I second order | Three-block states | 480 | 1.077571 | 1.528147 | −0.101023 | 6.642145 |
| A first order | Three-block states | 480 | 2.156203 | 3.070270 | +0.022690 | 12.072172 |
| I raw Q | Full, before override | 120 | 2.941267 | 4.200194 | −0.246717 | 17.946418 |
| A raw Q | Full, before override | 120 | 3.217094 | 4.546686 | +0.000708 | 16.297651 |

The routed full estimate has zero error for both methods **by construction**, because the design replaces it with the measured full vector. It is not evidence of extrapolation accuracy. Second-order estimates fit the finite withheld triple score vectors better numerically, while final task correctness is worse. This separates response-approximation behavior from useful answer selection; neither error table establishes necessary natural evidence, causal interference or a retrieval/fusion decomposition.

## Actual acquisition and policy cost

The experiment paid for384 distinct fill128 states plus53 distinct selected zero-fill states: **437 unique forwards**, not437 per method. The55 zero-map logical question/mask states include2 full reuses; no zero-empty input or unselected mask was queried. All actual states retained48 slots and1296 visual tokens, including masked slots.

The following are **component replays within the shared run**, summed over24 questions. Common diagnostic paths charge the declared observation set even where a method ignores some entries. Natural minimal paths separately omit A's unused pairs and C's unused empty state. Any needed selected-state/two-fill verification is included and identities deduplicated. No method was separately loaded or rerun for timing.

| Method | Common-path states | Range/question | Common forward subtotal (s) | Natural-minimal states | Range/question | Minimal forward subtotal (s) |
|---|---:|---|---:|---:|---|---:|
| F | 24 | 1 | 18.437 | 24 | 1 | 18.437 |
| M | 96 | 4 | 73.495 | 96 | 4 | 73.495 |
| A | 301 | 12–14 | 230.947 | 159 | 6–8 | 122.153 |
| I | 293 | 12–14 | 224.977 | 293 | 12–14 | 224.977 |
| C | 294 | 12–13 | 225.681 | 270 | 11–12 | 206.774 |
| R | 317 | 13–14 | 242.746 | 317 | 13–14 | 242.746 |

I and R match the frozen worst-case14-state bound, **not their actual counts or wall time**. I paid more than A's natural minimal path while answering fewer questions. R used24 more replayed states than I and answered3 more, but that does not make R a novel method or justify automatic continuation. Acquisition also includes triple validation and selected-zero responses unused by early-F branches; these remain charged to the shared experiment rather than hidden as free work.

All437 measured forward/transfer/log-score components totaled335.007 s, contained within the **385.937 s** single model Job. Formal initial CPU preparation24.359 s is also contained there. CPU-only Jobs totaled32.218 s; all supervised Jobs418.155 s. Loading/imports, template/masking/preparation gaps, loop/fsync/selection overhead and teardown are not fully attributable to standalone policies. Full end-to-end deployment latency is UNKNOWN; component subtotals and overlapping policy replays must not be added to the outer experiment cost.

## Disposition and evidence boundary

All methods, inputs and isolated scoring are complete; this is not an incomplete-run fallback decision. The registered I gates fail against F and all four controls, including its no-interaction ablation and matched worst-case search. **Stop this specific router.** Do not expand blocks/fills, tune the prefix/margins, pick favorable sources, substitute a control as the new candidate, train or launch054 from this budget.

The same previously exposed24 questions, nominal four recordings, low-resolution48-candidate cache and ordinal clock do not establish independent-source or natural-video generalization. One known task-scope caveat remains; no cleaned score is used. Masking and model feedback, finite differences and attribution have published precedents, including [MACD](https://arxiv.org/html/2602.01740v2), [ReaSon](https://ojs.aaai.org/index.php/AAAI/article/view/38387) and [Play Fair](https://arxiv.org/abs/2011.12372); this experiment does not certify originality or reproduce their methods. The frozen design's broader novelty review is not upgraded here. NOVELTY=UNRESOLVED, with no new core contribution claimed.
