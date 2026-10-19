# OEP diagnosis and next research decision — 2026-10-20

User-directed Codex review and planning, continuing the user's request to review
progress and determine the next direction. This is a public-source diagnosis,
not a new experimental parent or a renewal of 024 data/GPU authorization.
Reviewed main: `6bee319d9b96e5b496fee922af48710f34fdbb56`.

**Decision: do not retry 024 unchanged or start training.** Correct the stale
planning state, resolve the input handoff once, and specify a real diagnostic
that can distinguish candidate acquisition, selection and downstream use.
Actual dominant failure on real video remains UNKNOWN.

## 1. What the existing experiments establish

From the public [017 receipt](../codex-artifacts/VLM-HOURVIDEO-NEW-SOURCES-017/new-sources-paired-receipt.md):
source-equal Uniform=25.433125%, Top12=29.614230%, difference=4.181104pp.
From [018](../codex-artifacts/VLM-UNSEEN-SOURCE-STRATIFIED-018/three-arm-new-source-receipt.md):
Uniform=30.356365%, Top12=34.140990%, 12bin=30.519763%, Top12 minus
Uniform=3.784625pp. These values were independently recomputed with rational
arithmetic from the published correct/N cells, not by reopening any old QA.
They remain CLOCK_ZERO_ASSUMED_NOT_CERTIFIED and descriptive recorded-source
results. They do not identify the causal reason for any improvement.

The [024 receipt](../codex-artifacts/VLM-HOURVIDEO-OEP-REAL-024/real-oep-pilot-receipt.md)
already closes that parent at the eligibility gate: no question queue was
frozen and no actual QA generation occurred. A board entry saying it is still
READY/unexecuted is stale. The old execution contract and results are retained.

## 2. Proven protocol problem: ranks do not implement an absence gate

The [024 protocol](../research-protocols/real-oep-pilot-2026-10-19.md) proposes
stable rank percentiles before applying the 023 pair mechanism, but supplies no
exact percentile/tie formula or independent semantic-evidence acceptance rule.
The following theorem is conditional on ordinary ordinal percentiles, not a
claim that an unimplemented 024 runner already uses a particular formula.

Let ranks run from 0 to 47, and p=r/47. Threshold p>=0.70 keeps ranks
33 through 47: exactly 15 frames per event, irrespective of absolute score.
For event sets A and B of size 15, choose any a in A and a distinct b in B.
Either a<b, which is an AB candidate, or b<a, which is a BA candidate.
Therefore at least one direction always exists. For decomposable inputs,
the no-supported-direction fallback is unreachable under this mapping.

Concrete arithmetic witness: both raw score vectors are
`s[i] = -0.9 + i * 0.000001`, i=0..47. All raw values are negative and tightly
clustered, but ordinal conversion still produces 15 qualified frames for each
event and 105 pairs in EACH direction. Low raw cosine is not itself a ground
truth event-absence label; this witness proves the loss of an absolute evidence
gate, not a statement about an actual video's content.

Average-rank ties could change the all-tied case, but an arbitrarily small
strictly ordered perturbation restores the same rank-based support. A ranking
heuristic may still improve QA; it must be evaluated as ranking, without
claiming that its threshold authenticates event presence or reliable fallback.
Do not silently edit the closed synthetic 023 contract to hide this distinction.

## 3. Proven comparison confound: unequal anchor quotas

The [023 implementation](../../prototypes/ordered_evidence_selector_023.py)
can retain four ordered anchors while its unordered ablation retains at most
two. A concrete witness, with all other scores zero, is:

| Event score | Nonzero entries |
|---|---|
| A | index 2: 1; index 10: 0.875 |
| B | index 5: 0.875; index 20: 1 |

Best AB=(2,20); best BA=(5,10). OEP retains {2,5,10,20}, while unordered
retains {2,20}; both then fill to 12 with sQ. A resulting QA difference would
combine order constraints with the number of event anchors replacing sQ frames.
This is valid code under the old contract, but insufficient isolation of an
ordering mechanism. A future diagnostic needs a deterministic unordered control
with matched per-question unique anchor count and the same event-query costs.

There is a further exact symmetry: exchanging sA and sB exchanges the AB and BA
records but leaves their anchor union, final selected indices and sQ filling
unchanged. Thus the selector exposes two possible directions; it does not choose
which relation is true. This is compatible with supplying evidence to Qwen, but
a direction-status unit test does not demonstrate Qwen's temporal reasoning.

## 4. Real error location is not identifiable from the current public record

| Candidate explanation | What would distinguish it | Current status |
|---|---|---|
| Key event absent from the 48-frame pool | Independently valid event/instance evidence compared with the actual pool | UNKNOWN; aggregate accuracy and similarity scores are insufficient. |
| Event in pool, omitted by selector | Same evidence compared with frozen selected frames | UNKNOWN; event-score coverage cannot certify its own semantic truth. |
| Evidence selected, Qwen not using order | Verified evidence plus controlled presentation interventions, with timestamp/prompt effects specified | UNKNOWN; a changed answer alone is not correct temporal reasoning. |
| Event decomposition targets the wrong or missing event | A frozen nongold grammar applied to authorized question text | UNKNOWN; no new private question text read. |
| Input handoff prevents the experiment | Exact authorized metadata/runner entry, absent from the active handoff | Confirmed operational blocker for 024, not a GPU or method failure. |

For an hour-long interval, 48 uniformly spaced endpoint candidates are about
3600/47=76.6 seconds apart. This establishes a potential resolution limitation,
not an observed miss rate. A selector cannot recover an event absent from its
pool. No actual evidence-recall measurement exists in the admitted public data.

A question such as "What happened after event A?" contains only one specified
event. The unknown answer cannot be used to manufacture event B. A future
two-event study must freeze a grammar requiring two explicit question events,
or define a different answer-independent retrieval task. A task category or
the presence of "before/after" alone is not an eligibility certificate.

## 5. One executable next direction, conditional on concrete inputs

1. **Repair the handoff once, before declaring READY.** Obtain the exact
   previously authorized private runtime/nongold metadata entry from the user;
   initially inspect only permitted code and structural metadata. Maintain an
   explicit private/public separation and do not search unrelated directories.
   An exact directory request has been sent in the private chat; no private
   access or new private registry write is implied while it is unanswered.
2. **Specify evidence and permissions operationally.** Define which recording,
   parent-video and edit relationships establish or fail source separation.
   Different UIDs alone remain insufficient. Missing evidence stays UNKNOWN;
   any weaker exploratory claim requires an explicitly revised protocol and
   appropriate authorization, never retroactive PASS for 022/024. A question,
   label, media or credential not covered by current permission is not opened.
3. **Freeze the diagnostic, rather than invent another name.** Primary comparison:
   GlobalTop12 versus count-matched unordered event retrieval versus the ordered
   candidate mechanism. Freeze event extraction, rank/tie semantics, fallback,
   anchor padding, the candidate pool, denominators and retrieval cost accounting
   before any real output or answer is seen. Any order intervention must specify
   frame presentation, timestamp tokens and the justified expected response;
   sensitivity without a valid expected relation is only a diagnostic.
4. **Make one bounded real run only after inputs and new authorization exist.**
   Set its budget from the frozen question/arm matrix, retain invalid/not-run
   cases, and separate final CPU scoring. Do not reuse 024's expired parent
   authorization or old 013–018 gold to tune the new mechanism. If independent
   event/instance labels are unavailable, semantic evidence recall remains
   UNKNOWN; do not create manual labels without separate permission.
5. **Use the result to choose the research layer.** Candidate absence motivates
   acquisition work; pool-to-selection loss motivates retrieval/instance binding;
   verified selected evidence with poor controlled reasoning motivates model
   input/reasoning work. If ordering cannot exceed a matched unordered control,
   do not expand OEP GPU experiments or proceed directly to training.

Repeated actions and incorrect A/B instance binding are a candidate research
question, not a retained innovation. Existing temporal-logic methods remain
required comparisons; no new literature superiority claim is made here.

## 6. Scope and preservation

This review used only public repository code/receipts and one in-memory stdlib
rational-arithmetic check of the stated witnesses and published aggregates.
That check exited successfully; no old repository module or unittest was run.
No private file, question, gold, prediction, video, model, credential or source
map was accessed; no GPU, download, training, installation or environment change
occurred. Only this review and current planning-state documents are updated.
No new experimental parent/result entry, READY task, budget or data permission
is created. All historic receipts, protocols, READMEs and implementations remain
unchanged. **REAL_QA_EFFECT_UNKNOWN; NOVELTY=RETAIN0;
CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; Charades FINAL_MEDIA_STOP.**
