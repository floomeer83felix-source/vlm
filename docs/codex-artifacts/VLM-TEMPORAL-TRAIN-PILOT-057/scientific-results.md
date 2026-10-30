# 057 scientific results

**COMPLETE_REAL_TRAINING_PILOT / NO_PILOT_SUPPORT_FOR_THIS_RECIPE.**
Stop this specific joint-supervision recipe; no retuning, extra steps, new seed,
expanded subset or automatic058. Novelty remains UNRESOLVED. This result does
not establish that temporal learning or every joint loss is generally ineffective.

Actual fixed-feature training completed:8 configurations×250 real CPU updates,
2000 total. Qwen was frozen, loaded once and not trained. This is a small new
25-train/2-validation/24-test pilot from the same05651 pairs. Original055/056
minimum-size gate did not pass and is unchanged. Validation was evaluated only
after training; no checkpoint/seed/hyperparameter selection.

Test full-denominator four-way all-correct results:

| Method | seed19 | seed73 |
|---|---:|---:|
| A ordinary adapter |5/24 (20.83%)|7/24 (29.17%)|
| V video-pair supervision |2/24 (8.33%)|4/24 (16.67%)|
| S shuffled joint groups |4/24 (16.67%)|5/24 (20.83%)|
| I true joint groups |3/24 (12.50%)|4/24 (16.67%)|
| B0 frozen Qwen |1/24 (4.17%), evaluated once|same single B0 set|

I−A is−2/24 (−8.33pp) and−3/24 (−12.50pp), failing the required positive≥2
instances/≥5pp for both seeds. I−V is+1/24 and0; the second strict-positive
condition fails. I−S is−1/24 for both. I−B0 is+2/24 and+3/24, average+10.42pp,
but improvement over B0 does not satisfy the same-capacity A control.
Therefore the preregistered pilot gate FAILS.

I versus A paired corrections/harms are2/4 (seed19;1 both-correct,17 both-wrong)
and0/3 (seed73;4 both-correct,17 both-wrong). Group-paired10000-bootstrap95%
intervals for I−A are[−28.57,+12.00]pp and[−25.93,0.00]pp. Intervals are small-
sample uncertainty summaries, not independent confirmation or equivalence tests.
All8 comparisons and anonymous source-stratified differences are in the CSV/JSON.

Single-cell test accuracy: B0 56/96; seed19 A55/V48/S50/I53 of96;
seed73 A66/V56/S53/I52 of96. Video-pair and question-pair counts, all train/
validation metrics and failures remain in the25-row condition CSV. All1728
planned head+B0 evaluation cells are terminal valid, no failures/invalid/not-run
or unknown scoring cells, and no denominator cleaning. Main unit remains24
four-cell instances and15 participant groups, not96 independent cells or48
independent seed-replicated instances.

Every head has356673 actually instantiated parameters at measured Dv=Dq=2560,
using6 visual time units from the12 real frames. Per-seed initialization and
sampling exposure are shared,8000 training-cell exposures per configuration.
Loss decreases and positive parameter changes are reported as training execution
evidence only. They do not replace the failed answer-gain gate.

Source evidence is official-annotation join plus published segment-swap construction;
cross-kitchen/physical independence is not certified. No external evaluation was
planned or performed. Four-way success alone would not prove question-specific
temporal localization or improvements inside the frozen LLM. The initial admission
supervisor repair is disclosed in the receipt; no model input/weight load was retried.
