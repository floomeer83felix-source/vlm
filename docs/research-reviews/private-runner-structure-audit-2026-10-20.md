# Existing runner and structural-record audit — 2026-10-20

This continues the user's delegated progress review and diagnosis. The user
provided the two exact private 017/018 runtime directories in response to a
request explicitly limited to source code and structural metadata. No old
experimental parent was reopened. Public baseline: `0e08265`.

**Outcome: exact input references recovered; coarse sampling and the recorded
input/selection structures verified; actual semantic failure layer UNKNOWN.**
This is not a model evaluation, a source-eligibility PASS or new GPU permission.

## Authorized inspection and preserved boundaries

Both supplied roots and their ancestor chains were checked as non-reparse
directories. Inventory was confined to the two exact roots. A bounded probe of
one observed source subdirectory stopped at its 48-entry cap; further inspection
used exact artifact names learned from the authorized source code, not a broader
directory search. No directory outside the supplied roots was enumerated.

Read-only AST inspection covered 15 distinct scripts, including the six actual
per-source runners. The scripts were parsed as text, never imported or executed.
Twenty-four distinct structural artifacts were inspected: one frozen manifest,
one packet-PTS summary, one execution summary and one selection audit for each
of six sources. No frozen question file, prediction/answer file, source movie,
external annotation/manifest, model asset or credential was opened. No private
file was written. JSON metadata values were used only for shapes, counts, time
intervals and selector-identity checks; no gold or outcome-based tuning occurred.

An initial metadata-shape check assumed 017 had the 018 cosine field and stopped
with KeyError. The actual writer schemas were then inspected and the audit
adapted to their documented difference. The complete six-source structural
pass succeeded. These were inspection-tool adjustments, not failed model-call
retries or historical experiment reruns. All stdlib-child checks found
torch/numpy/transformers/av absent from loaded modules.

A suspected regex-escaping issue was explicitly falsified: the actual pattern
strings extracted by AST were checked against nine invented dependency/plain
text examples, and all nine matched their expected semantics. The concern came
from escaped source display, not a demonstrated bug in the actual patterns.
No old protocol module/function was imported or run and no old regex was fixed.
These synthetic source-semantics checks used no private question or answer.

## 1. The lost handoff entries have been recovered

| Entry role | Evidence now available | Boundary |
|---|---|---|
| Main dev annotation input | Exact path literal recovered consistently from qualification/scoring sources | Target not opened or statted; current presence, contents and permission not newly certified. |
| Official release-1 source manifest | Exact path literal recovered from the qualifier | Target not opened or statted; physical provenance and current access remain unverified. |
| Actual private inference components | Six exact per-source scripts present and parsed under the supplied roots | Runtime health and current GPU resources were not tested. |
| Selection and execution metadata | Exact saved artifacts present and structurally checked | Semantic correctness is not encoded by these structural checks. |

Exact private paths remain in the private conversation/source records only.
The former entry blocker was a handoff loss, not evidence that data or code had
disappeared. Recovering a reference does not authorize opening every referenced
input or certify the new sources required by 024. The old 024 HOLD stays closed.

## 2. Actual recorded candidate spacing is coarse

The source code targets 48 evenly spaced packet-PTS positions, with a 0.10-second
tail margin. For each target it seeks backward and takes the first decoded
frame at or after the target, checking finite strictly increasing PTS.
Only the saved numeric PTS records were read in this review; no decode occurred.

| Anonymous source | Frozen N | Candidate gap min / mean / max, seconds | Recorded frames / visual tokens | Recorded returns / attempts |
|---|---:|---|---|---|
| R1 | 39 | 59.200 / 59.220 / 59.233 | 12 / 324 | 78 / 78 |
| R2 | 39 | 93.533 / 93.547 / 93.567 | 12 / 324 | 78 / 78 |
| R3 | 37 | 63.867 / 63.885 / 63.900 | 12 / 324 | 74 / 74 |
| R4 | 36 | 79.133 / 79.155 / 79.167 | 12 / 324 | 108 / 108 |
| R5 | 35 | 76.267 / 76.282 / 76.300 | 12 / 324 | 105 / 105 |
| R6 | 34 | 74.600 / 74.621 / 74.633 | 12 / 324 | 102 / 102 |

Thus the candidate gap concern is now backed by saved run metadata, not just
an hour-long arithmetic example. A short action could fall between candidates,
but no event-instance annotation or pixel evidence was inspected, so actual
event-miss frequency and its contribution to errors remain UNKNOWN.

## 3. No input-size mismatch was found in the inspected structures

The six actual input-construction function ASTs are identical. Every run summary
records grid [6,12,18], 12 source frames and 324 visual tokens. The input code
checks frame count, grid and visual-token consistency. This supports the claimed
input-budget control in the inspected implementation and saved summaries; it
does not independently reprocess tensors or certify semantic evidence quality.

All saved selections contain 12 unique increasing candidate indices within
0..47. For all 105 questions in 018, the saved finite 48-score rows reproduce
the saved Global Top12 exactly using descending cosine/earliest-index ties.
The saved 12bin selections likewise reproduce the same-score maximum in each
four-candidate bin. This audit used no question text, reference answer or model
response. It found no mismatch in these numeric selection rules.

## 4. The saved records cannot answer the semantic question by themselves

017 selection audits persist PTS, selected indices and RGB digests, but no
cosine matrix. 018 also persists its question-by-48 cosine matrix. Neither
inspected runner persists the normalized image embeddings or frame RGB arrays
used during inference; the source retains those in memory and writes digests/
selection records instead. No general assertion that the whole machine lacks
other caches is made; no other directory was searched.

The saved question cosine matrix is not enough to obtain new event-A/event-B
similarities. A hash cannot establish that an action is visible in a candidate,
and a retrieval score cannot independently certify its own event identity.
Existing files therefore permit numerical/structural auditing without proving
candidate evidence recall, selected evidence recall or correct order use.

All six runners embed question text only for retrieval and enable tokenizer
truncation. No per-question retrieval-text truncation/length audit appears in
the inspected run summaries. Truncation is a possible unmeasured confound;
this review did not read questions or tokenize them, so no actual affected count
or causal explanation is claimed.

## 5. Old components cannot be copied into the stricter gold contract unchanged

Source inspection shows the old 018 qualifier loads annotations and calls the
canonical gold-label validator before inference. Both old scoring scripts
decode the complete annotation JSON, then select the relevant questions.
This observation concerns source code only; none of those reads was executed
in this review. It is not an allegation that the old authorized contracts were
violated or that answer values entered the old inference pipeline.

024, however, permits its gold read only after all generation children exit,
and restricts it to the current batch. Direct reuse would not implement that
new boundary. A future run needs an answer-skipping nongold projection and a
separate, batch-scoped final scorer. Existing source paths alone do not make
that integration complete. The inspected source-group function uses the pair
(video_source, origin_video_id); it does not independently authenticate physical
recording/shot/edit separation. That limitation is unchanged.

## 6. Next evidence and disposition

The next useful CPU evidence is the availability of permitted source fields and
the number of genuinely two-explicit-event questions under a frozen nongold
rule. The exact two metadata references are now known. Reading their nongold
question text exceeds the user-confirmed source/structure-only inspection, so
a bounded request has been presented in the private chat: at most 120 seconds,
source/task/question fields only, skipping gold/options/reference-time/canary
values, with no media, network, model, file modification or environment change.
Until explicitly approved, those targets are not accessed. Any future private
registry write likewise needs its own scope; none was created in this review.

Even an approved text/metadata audit cannot decide whether real frames contain
the required event. Semantic grounding evidence would need separate authorized
labels or visual inspection and a properly controlled diagnostic. No old answer
or model-output text may be opened or used to choose thresholds in this phase.

This review updates planning only; it creates no READY experimental task and
does not revive 024 or any old quota. The earlier
[mathematical diagnosis](./oep-diagnosis-2026-10-20.md) remains valid. Matching
anchor quotas and defining real rank/fallback semantics are still required
before a new OEP comparison. Current-round model/GPU calls, media reads/decodes,
gold reads, prediction-body reads, research downloads, training, environment
changes and private writes are all zero. Historic scripts, results, protocols
and READMEs remain unchanged. **REAL_QA_EFFECT_UNKNOWN; NOVELTY=RETAIN0;
CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; Charades FINAL_MEDIA_STOP.**
