# 082 scientific diagnosis

**CACHE_INTEGRITY_PASS / CAUSE_UNRESOLVED** for the checked cache links and statistics. The original 081 recipe remains closed. No binding defect or contradictory exact current feature input was found; this does not certify all implementation paths or identify the causal reason for failed fitting.

## Responses to real video permutations

| Split | B0 sensitive / views | Head sensitive views (18 configurations) | Head correct items |
|---|---:|---|---:|
| train | 44/120 | 15 configs × 0, 3 configs × 1 | 358–360/720 |
| development | 14/24 | 18 configs × 0 | 72–72/144 |
| test | 22/48 | 18 configs × 0 | 144–144/288 |

In every invariant source/question view the fixed answer is exactly **3/6 correct**, independently verified. All test and development head decisions are invariant across six real video permutations. Training has 15 fully invariant configurations and three with one sensitive view each; these are binary decisions, not statements that logits never change or video features are wholly unused. REAL differs from BLACK/TRAIN_MEAN on many items; this alone demonstrates neither successful temporal binding nor its cause. The [57-row table](./cache-diagnostics.csv) preserves every source/item/view denominator, FLIP/HOLD result, invariant/sensitive correctness and control agreement.

Same-seed test and development REAL predictions are identical across A/I/S, but training seed73 differs: I−A **1/720**, I−S **3/720**, A−S **2/720** disagreement. Other same-seed/split comparisons are zero. Thus equal aggregate accuracy was not sufficient to claim identical predictions everywhere. All 18 final states differ from their initial state and from their same-seed arm counterparts.

## Binding and exact feature information

Captured main-merger V, literal-q/TEXT token-key q, prediction V/Q and train V/Q/Y are bit-exactly linked. Ordered V has **192 distinct** tensors (six per source), q has **138 distinct** feature tensors for 138 literal questions, with no different-literal collision. Across 96 q/tau pairs there are **0 exact collisions**; cosine spans **0.954828–0.998203**, relative L2 **0.060261–0.299229**. High cosine is not evidence that the language model cannot distinguish roles. Development has 12/24 and test16/48 unique literal questions seen in training; this is coverage, not evidence of generalization.

After inverse permutation of three known six-unit blocks, **160/160** noncanonical V comparisons equal canonical V byte-for-byte, max absolute difference and relative L2 zero. This is actual block equivariance of these cached features. The temporal mean reference is only approximately equal in float32 reduction: exact equality **0/160**, max absolute difference **1.19e-7–4.77e-7**, relative L2 **6.37e-8–9.83e-8**. Those rounding-scale mean differences are not counted as exact collisions or evidence of usable ordering.

All **1,152** exact `(ordered V bytes, q bytes)` classes are distinct, with **0** opposing-label classes. Deterministic item upper bounds are train720/720, dev144/144, test288/288; within-source completion upper bounds20/20,4/4,8/8. These upper bounds only say this exact-contradiction test does not rule out correct decisions. They neither establish learnability of this architecture nor prove that training succeeded; source bounds do not solve all cross-source compatibility constraints.

## Position and loss evidence

All 18 states contain **341,633** parameters; every scalar differs from initialization, including all1,152 position entries. Position initial is zero, final is finite. No final state's18 rows are all identical; **0/18** final states satisfy exact repetition of the three six-row blocks. Block-pair L2 differences span **0.00147472–0.01469776**. Same-seed final arm-pair state differences have L2 **0.000230879–0.00537854**; no final arm pair is tensor-equal. Parameter-family delta norms/counts and per-configuration position checks are in the [summary](./diagnostic-summary.json), without tensor values.

In ideal real arithmetic, if P repeats across the three block positions and V only block-permutes, query-attention pooling is permutation invariant: projected per-token terms and scores permute, and the weighted sum is unchanged. V satisfies the exact premise here, but final P does not. Therefore **the joint strict symmetry condition is not met**. Approximate blocks, float effects and invariant binary answers do not prove strict function symmetry or a sufficient causal explanation. This condition is specific to the stated pool, not all temporal adapters.

The original4,500 STARTED/CLOSED updates remain complete. First10 mean BCE spans **0.705525–0.709662**, last10 **0.69314749–0.69314837**; final BCE **0.69314736–0.69314796**, near ln2. Final relation loss is **0.3333333433** in all18 configurations. The fixed step1/10/50/100/250 values, first/last10 means and finite checks are preserved per configuration. Loss reduction and parameter change coexist with near-chance train answers; neither establishes useful fitting. Gradients and head continuous margins were not stored: gradient effectiveness/zero gradients, convergence and precise margin dynamics are **UNKNOWN**, without new forward/backward evidence.

## Clock finding and stopping boundary

The original idle exclusion is **UNVERIFIED**: registered records contain no preexisting explicit user pause authorization tied to that interval. Arithmetic and train-to-predict sequence agree; active0 is insufficient authorization. Final private closure raw081 **30,785.853 s** and raw four-parent **34,799.670 s** exceed12,000/14,400 s. Charged4,731.450/8,745.267 s are reported separately without certifying that subtraction. These later closure values differ from the earlier public report snapshot because reporting/push continued. No old record is altered and no scientific outputs are discarded or rerun.

The independent oracle passed1,495 assertions without production-helper/scorer calls or predictor replay; binding/statistic checks total116,053. Scope remains a posthoc cache diagnosis of the fixed official-train development split. The actual cause of near-chance fitting remains unresolved. No new mechanism, optimizer choice, learning-rate fix, threshold, head, training proposal, paper or 083 execution is justified or performed by this package.
