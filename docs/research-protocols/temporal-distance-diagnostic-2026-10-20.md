# Question-constrained temporal-distance diagnostic — 2026-10-20

**Status: design frozen for public code task 025 only. Real-data execution,
media access/download, GPU and gold scoring are NOT READY and not authorized.**
This is a new exploratory diagnostic, not a revision or resumption of 023/024.
The user delegated research planning and writing the next task to this repo.
Historical protocols, implementations and parent results remain unchanged.

## 1. Research decision and hypothesis

The [nongold audit](../research-reviews/nongold-feasibility-audit-2026-10-20.md)
finds 28 explicit two-event time-gap forms across 28 videos, not twelve usable
questions in two videos. A supplied event order is a retrieval constraint; it
is not an unknown AB/BA answer to predict. The first focused question is:

> With the same 48 candidate PTS, twelve presented frames, two distinct event
> anchors and event-query scores, does imposing the question's given order
> change evidence selection and descriptive QA performance relative to an
> otherwise matched unordered pair?

This tests a constraint on a simple ranking heuristic. It does not claim a new
algorithm, calibrated event detection, independent event grounding or Qwen's
temporal reasoning. The [rank/anchor diagnosis](../research-reviews/oep-diagnosis-2026-10-20.md)
and [runner audit](../research-reviews/private-runner-structure-audit-2026-10-20.md)
motivate the controls. No training is justified by the available evidence.

## 2. Nongold admission: a narrow, deterministic interface

025 uses invented fixtures only. Implement the following grammar before any
future application to real data; do not tune it to reproduce the observed 28.

- Admit only exact task `perception/information_retrieval/temporal_distance`
  and a complete, case-insensitive question of the form
  `How long after <event A> <aux> <event B>?`.
- Normalize whitespace. The boundary is a standalone word in
  `{did, does, do, was, were, is, are}`. Enumerate possible boundary tokens in
  the remainder: accept only one with nonempty event clauses. An optional
  comma immediately before that boundary may be removed. Keep clause wording;
  no LLM, semantic completion or answer-assisted rewriting.
- Reject multiple possible boundaries, nested temporal markers
  `before/after/then/earlier/later` inside either clause, missing clauses,
  unsupported forms and question strings longer than 4,096 characters.
  Report explicit unsupported/ambiguous reasons, not event absence.
- Event A is the given earlier event; B the given later event. Do not infer
  the unknown gap, occurrence identity, or which repeated instance is intended.
  Unknown-middle-event and one-anchor questions are outside this version.
- Parsing takes only task and question. Options, answers, reference times,
  old outputs and source performance cannot influence admission or event text.

A strict parser may admit fewer than the 28 audited forms. Report that fact;
do not relax the grammar, substitute questions or meet a quota by changing it.

## 3. Answer-skipping projections and immutable planning

The future input schema has top-level video keys, nested `video_metadata`, and
a `benchmark_dataset` question list. Implement bounded streaming JSON projection,
not whole-file `json.load(s)`. Skip values of unknown/protected fields lexically
without decoding or materializing them. JSON syntax and string escaping still
need validation; protected values must not appear in errors or debug output.
Reject duplicate object keys, malformed input, excessive nesting (>64), input
larger than 64 MiB, or an admitted string larger than 64 KiB. These are parser
limits, not permission to open a real file of that size.

Two explicit nongold views are needed:

1. **Screen view:** requested batch/source membership, task, question, UID
   consistency, admitted source/version/duration fields only. Skip all options,
   gold, reference-time and canary values. Never expose a real identity in public
   logs; fixtures use invented keys. Source/version matches remain observations,
   not rights or physical-independence certificates.
2. **Inference view:** only after a future authorization includes model-input
   options, retain exactly five nonempty string fields `answer_1`…`answer_5`
   for the prompt, plus the same question. Gold/reference-time/canary remain
   skipped. Event extraction and scoring vectors receive the question only,
   never these options. 025 tests this view only with invented options.

Allowlist nested field names explicitly from the documented schema; do not
automatically retain every field in `video_metadata` or a question object.
Use an exact batch key list; do not decode unrelated question values. Neither
view reads/validates the correct-answer value before generation. This is a
deliberate new boundary, distinct from the authorized historical 017/018
qualification. Test that changing protected fixture values cannot change
nongold projections, decomposition, selected frames or the generation plan.

Freeze planned question keys, original question indices, source grouping,
qualifications/exclusions, four-arm queue and N before model execution. Sorting
must use the frozen private source order and original question index, not scores
or outcomes. Never serialize actual identities or prompts into public outputs.

## 4. Four arms with a matched causal comparison

Inputs are 48 finite strictly increasing PTS and finite raw cosine vectors
`q[i]`, `a[i]`, `b[i]` in [-1,1], i=0…47. No percentile threshold, learned
calibration, minimum gap, adaptive candidate expansion or hyperparameter sweep.
Invalid inputs HOLD; do not repair, impute, clip or drop frames.

| Arm | Exact selection |
|---|---|
| A — Uniform12 | Indices `round(47*k/11)` for k=0…11, in time order. |
| B — GlobalTop12 | Top twelve by `(-q[i], PTS[i], i)`, then time order. |
| C — UnorderedPair12 | Choose the distinct event-labelled pair `(i,j)`, i≠j, maximizing `a[i]+b[j]`; sum ties use smallest `(i,j)`. Keep exactly these two unique anchors; fill ten by B's ranking, excluding anchors. |
| D — OrderedPair12 | Same as C, restricted to i<j because the question supplies A before B. Same two-anchor quota and identical question-score filling. |

All four outputs contain twelve unique indices sorted by PTS. C and D use
exactly the same two event embeddings, raw scores, pair objective, tie rule,
fill rule and final chronological presentation. Their only difference is the
admissible pair order. They may intentionally return identical selections;
record that rate, rather than discard such questions. Identical/tightly
clustered/negative cosine inputs still produce a pair, flagged
`EVIDENCE_PRESENCE_UNVERIFIED`; they cannot produce semantic PRESENT/ABSENT
or calibrated SUPPORT. This selector has no semantic-absence fallback.

For unsupported text forms, the library may expose B as an explicit diagnostic
fallback, but such questions are not added to this two-event cohort. A future
denominator cannot silently mix fallbacks with qualified pairs. Old 023
bidirectional-four-anchor and 018 twelve-bin arms are not rerun here.

The public adapter builds a plan only; it has no live-model execution switch.
The future wrapper must reuse the already frozen Qwen/processor/prompt/decoder
contract, subject to an independently authorized exact runner entry. All arms
have the same actual frames/token budget, model prompt, deterministic decoding
and source candidate pool. Rotate queue order ABCD/BCDA/CDAB/DABC by the frozen
global question index modulo four. Count all four planned attempts even if
two selected frame sets coincide; no output reuse, retries or best-of selection.

Future receipts must separately charge shared candidate image encoding, q/a/b
text embedding, arm selection and Qwen work. Sharing the exact same a/b scores
between C and D prevents an event-query-cost confound. Record text token lengths
and truncation, actual visual token/grid counts and all resource peaks. 025
cannot measure any of these model quantities.

## 5. Isolated, one-shot final scorer and denominator honesty

The public scorer accepts a stream-opening callback, immutable planned batch,
terminal ledger and child-exit receipt. It validates the logical gate **before**
calling the opener, consumes its one-shot guard before attempting the read, and
does not retry malformed input or reopen after failure. Its separate module
does not run on import. In 025 every opener returns invented in-memory JSON.

The gate requires every planned arm to be terminal (returned, invalid, failed
or NOT_RUN), a frozen ledger, and all model children exited. A test receipt
does not prove real OS process isolation. Before any future real gold access,
an authorized supervisor must actually observe child exits, close the queue,
deny gold to generation children and launch a separate CPU scorer. A user-
supplied boolean or an `--allow-gold` flag alone is not sufficient evidence.

The scorer streams the annotation container once and decodes only
`correct_answer_label` for the exact frozen batch keys. Other gold/options/
reference/canary values remain unmaterialized. Container traversal does not
mean only batch bytes were read. No gold is returned to selectors or the model
plan. Canonical labels in this new contract are strings that strip/uppercase
to exactly one of A–E; no numeric guessing or answer-text matching. A prediction
must strip to exactly one uppercase A–E; other output is INVALID, without retry.

Keep `N_planned` unchanged. With valid gold, failed/INVALID/NOT_RUN attempts
remain in that planned denominator as incorrect, with separate reason counts;
publish pair cells only with explicit arm-state accounting. If a planned gold
is missing, duplicated or invalid, report `GOLD_SCHEMA_HOLD`, `N_valid_gold`,
`N_bad_gold` and known correct counts, with full-denominator accuracy and paired
tables **UNKNOWN**, not a silently smaller scored N. Do not read gold early to
make the denominator convenient, repair annotations, or rerun the batch.

## 6. Required CPU falsification and integration checks

025 must test the entire invented annotation → nongold views → decomposition →
frozen queue → four selections → stub terminal ledger → final scorer chain.
Tests establish code/interface behavior, never real retrieval/QA accuracy.
Required assertions include:

- Correct nested metadata projection; skipped protected and unrelated values
  are never decoded (instrument value decoding, not just final output).
- Escaped quotes/braces/Unicode in skipped values, nested canaries, duplicate
  keys, truncation, depth/size limits, and safe errors without fixture secrets.
- Protected-value mutations leave screen/plan/selection unchanged; options
  appear only in the inference view, never event clauses or score inputs.
- A supported invented time-gap form, multiple auxiliary-boundary ambiguity,
  nested-marker rejection, and mislabelled non-time-gap forms.
- Reverse unordered maxima cause C/D to differ while both retain exactly two
  distinct anchors; already-ordered maxima give identical C/D frames.
- Fully tied/negative scores are unverified heuristics, not absence/support;
  exact ties, no anchor duplication, twelve chronological frames and bad PTS/
  NaN/out-of-range scores rejected without silent repair.
- Both event vectors swapping changes the permitted-order problem; no old
  AB/BA-union invariance is falsely presented as selecting a true relation.
- Four-arm rotation, full planned queue, terminal NOT_RUN/INVALID preservation,
  premature/live-child scoring denied without opening the stream, one successful
  open, and second/failed read attempts denied.
- Out-of-batch gold not decoded, bad/missing gold produces UNKNOWN accuracy,
  and a complete invented batch produces the expected paired cells by hand.

No test imports or reruns historical task modules, private runners or models.

## 7. Subsequent real study: conditions, limits and stop decision

The intended first real run is an **exploratory engineering diagnostic**, up to
four eligible new videos with one qualified time-gap question per video; the
exact N is not known. At that cap, four arms mean at most sixteen Qwen attempts.
This is a design ceiling, not GPU permission, a download request, or an assertion
that four legal independent sources exist. Do not require twelve questions from
two videos. A larger source-level study must be designed separately.

Do not make a real-run task READY until concrete evidence and a new user scope
exist together: exact private inputs/maps, deterministic nongold inclusion and
old-source exclusion (013/014/R1–R6 plus known derivatives), current rights,
version, actual media paths or costed official single-source acquisition, and
explicit source/participant grouping. No current count proves four available
qualified sources or current acquisition rights.

The proposed new real study is a **recorded-group-separated diagnostic**, not
the strict physical-independence test required by closed 024. Its operational
screen would exclude matching recorded origin groups and known participant
groups against old sources and one another, and every officially linked known
derivative; missing grouping evidence must be disclosed before any task is
made READY. The user must separately accept this narrower exploratory scope
and its residual dependence risk as part of a new real contract. It is not
already authorized by asking to write tasks. Keep
`RECORDED_GROUP_SEPARATION_ONLY / PHYSICAL_RECORDING_INDEPENDENCE_UNKNOWN`
unless stronger evidence actually exists. The 50/50 join and 35 participants
cannot authenticate capture/shot/edit independence. Strict independent-source
generalization remains HOLD. This explicit change of study target does not
weaken or reopen 024, and avoids creating another parent that demands an
independence certificate the available manifest does not contain.

The user has seen dataset structure and some nongold forms during this audit;
this is an exploratory dev design, not a preregistration before all dataset
inspection. No new model outcomes or old gold informed its grammar/parameters.
Prospective cohort sorting must be fixed before new outcomes; unknown eligible
counts or acquisition costs need not generate another empty HOLD parent.
Use the already recovered exact entries when seeking a new bounded data scope,
not another directory scan or a repeated request for the same paths.

A future real contract must freeze its actual CPU/GPU/generate/memory/wall/
download/disk caps from that cohort and obtain explicit user approval. No 017,
018 or 024 remainder is reusable. Gold access and input-option access likewise
need the new scope; writing 025 creates neither.

Report future per-source correct/N, INVALID/NOT_RUN, six pair tables, C=D rate,
anchor PTS, span/bin coverage proxies and full costs. A 48-frame pool with
observed historical gaps of about 59–94 seconds cannot certify short-event
recall or fine time localization. Absolute localization needs a certified time
bridge. A constant clock-zero offset cancels in a time difference, but matching
release/crop/rate and event instances is still unverified; all scored claims
therefore retain the required `CLOCK_ZERO_ASSUMED_NOT_CERTIFIED` qualifier.
Similarity and span proxies cannot certify event identity or distinguish
candidate-missing, selection-missing and reasoning failure. That requires
independent event-instance/time evidence under a separate permitted protocol;
none is presently established. No new manual labels are authorized.

**GO for 025 interface implementation only. NO-GO for a paper mechanism claim,
training or unapproved real execution.** Stop this branch rather than multiply
toy tasks if a real diagnostic remains infeasible after these identified
interface repairs; consider a separately licensed temporal-grounding benchmark
with existing instance labels only through a new research decision.
`NOVELTY=RETAIN0`; Charades `FINAL_MEDIA_STOP` remains in force.
