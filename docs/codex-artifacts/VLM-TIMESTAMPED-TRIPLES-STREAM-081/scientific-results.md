# 081 scientific results

**NO_SATISFYING_JOINT_SUPERVISION_SIGNAL / STOP_THIS_RECIPE**. Execution and independent review are complete; this is a valid negative for the fixed recipe, not an incomplete run and not evidence against all question-conditioned temporal learning.

The primary endpoint is each source's **36/36 correct** over six real video permutations and six directed questions. All six seeds for all three heads scored **0/8** on test, with **144/288 (50%)** single-item accuracy. I−A and I−S are **0 percentage points**, corrected/harmed/net all zero for source completion. The frozen Qwen B0 REAL scored **176/288 (61.1111%)**, two complete native variants out of 48, zero complete sources out of eight. Thus I is **11.1111 percentage points below B0** in item accuracy and has no relative source-completion gain.

## Full test comparison

| Method | Seed | Items /288 | Native /48 | Source 36-all /8 | Quartet /144 | FLIP /48 | HOLD /96 |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0 REAL | - | 176 | 2 | 0 | 24 | 1 | 23 |
| B0 BLACK | - | 144 | 0 | 0 | 0 | 0 | 0 |
| B0 TEXT | - | 144 | 0 | 0 | 10 | 0 | 10 |
| A | 19 | 144 | 0 | 0 | 6 | 0 | 6 |
| A | 73 | 144 | 0 | 0 | 2 | 0 | 2 |
| A | 101 | 144 | 0 | 0 | 0 | 0 | 0 |
| A | 137 | 144 | 0 | 0 | 2 | 0 | 2 |
| A | 181 | 144 | 0 | 0 | 10 | 0 | 10 |
| A | 229 | 144 | 0 | 0 | 2 | 0 | 2 |
| I | 19 | 144 | 0 | 0 | 6 | 0 | 6 |
| I | 73 | 144 | 0 | 0 | 2 | 0 | 2 |
| I | 101 | 144 | 0 | 0 | 0 | 0 | 0 |
| I | 137 | 144 | 0 | 0 | 2 | 0 | 2 |
| I | 181 | 144 | 0 | 0 | 10 | 0 | 10 |
| I | 229 | 144 | 0 | 0 | 2 | 0 | 2 |
| S | 19 | 144 | 0 | 0 | 6 | 0 | 6 |
| S | 73 | 144 | 0 | 0 | 2 | 0 | 2 |
| S | 101 | 144 | 0 | 0 | 0 | 0 | 0 |
| S | 137 | 144 | 0 | 0 | 2 | 0 | 2 |
| S | 181 | 144 | 0 | 0 | 10 | 0 | 10 |
| S | 229 | 144 | 0 | 0 | 2 | 0 | 2 |

The three heads have identical aggregate test metrics within each seed; this does not assert identical weights or logits. All BLACK/TRAIN_MEAN head controls and B0 BLACK/TEXT score exactly 50% items and zero whole sources as required by the balanced question-only software guard. Their incidental HOLD quartet successes do not imply visual order sensitivity. [Baseline](./baseline-summary.csv), [head](./head-summary.csv), and [paired](./paired-summary.csv) tables also retain all train/development results and all controls. No failing cells were removed.

## Fixed gate, unchanged

```json
{
  "I_item_at_least50pct": true,
  "I_test_source_sum": 0,
  "above_own_fixed_controls": false,
  "complete": true,
  "item_flip_hold_not_lower": true,
  "net_source_sums": {
    "A": 0,
    "S": 0
  },
  "not_lower_B0_items": false,
  "passes": false,
  "seeds_strictly_above_both": 0,
  "software_guards": "PASS",
  "strictly_above_B0_sources": false
}
```

Only **0/6** seeds strictly beat both controls on source completion (required ≥5); I source sum **0/48** (required ≥12); net sums versus A/S **0/0** (required ≥6 each). I equals A/S in aggregated item/FLIP/HOLD metrics, but fails non-inferiority to B0 items, strict superiority to B0 source completion and strict superiority to its own fixed-video source controls. The ≥50% item floor alone passes. The full conjunction fails: **stop this recipe**, without tuning, extra seeds, changed losses, extra samples or a second scoring pass after modification.

## Pairing and uncertainty

The test has **eight independent analysis source groups**, not 48 independent observations from six seeds. Each source's six-seed mean completion difference is zero for I−A and I−S. The presealed source-paired exact sign-flip calculation enumerates 256 sign patterns; both descriptive two-sided tail fractions are **256/256 = 1**. All source completion differences are zero; the study supplies no positive source-level evidence. This is a descriptive null reference, not a confirmatory significance claim; physical recording/participant independence remains UNKNOWN. In paired mean CSV rows, counts sum six seeds while percentage differences divide by six times the source denominator; `independent_source_groups` remains eight.

## Scope and limits

Inputs use actual sampled RGB event clips, not latent-only permutations. Frozen Qwen features feed external binary heads; the experiment neither trains the backbone nor establishes a changed internal LLM reasoning mechanism. Loss decrease or changed parameters is not evidence of useful temporal binding. Software fixtures, the 50% fixed-input guard and formal gate arithmetic only establish their specified checks.

The 32 sources are a fixed self-defined 20/4/8 split within Perception Test official train, not a new external/official zero-shot or blind benchmark. Cross-recording/participant independence, pretrained overlap, event visibility, atomic completion and unique occurrence are UNKNOWN; the original strict-source constraints were not relaxed. Data are attributed to Google DeepMind Perception Test (CC-BY-4.0); sampling/permutation/supervision are local modifications. All negative results are preserved. No core innovation claim, paper or automatic 082 execution follows.
