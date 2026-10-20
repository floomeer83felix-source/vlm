# Nongold question and source feasibility audit — 2026-10-20

**Outcome: the old two-video / twelve-question gate is infeasible under the
024 whitelist plus its five temporal-marker screen. A narrower, real task is
available: two named events and a requested time gap, spread across sources.**
This records the completed, separately user-approved CPU read-only inspection.
It is a research review, not a reopened 024 parent or a new model evaluation.

## Scope and execution evidence

After the [source-only audit](./private-runner-structure-audit-2026-10-20.md),
the user explicitly approved one bounded, at-most-120-second CPU inspection of
the two exact recovered annotation/official-manifest entries. Only necessary
source/version/duration fields, task labels and nongold question text were
admitted. The exact entries remain in the private conversation; no new search
or source-map read occurred.

Stdlib children used a streaming lexical projection rather than loading the
whole annotation with `json.loads`. Protected answer, option, reference-time
and canary values were skipped without decoding/materializing, retaining or
displaying those values. Reading the container byte stream is not a claim that
the file contains no protected fields. Synthetic sentinel checks exercised
the skip boundary. No question or other raw dataset value is reproduced here.

There were three bounded projection passes: three annotation opens and two
manifest opens, with cumulative controlled child processing of 2.124 seconds.
The initial projection omitted nested `video_metadata`; its apparent zero
source/duration matches were an inspection error. Correcting that projection
produced the final 50/50 matches below. There was no dataset-conflict finding.
Input size/mtime remained unchanged; no private file was written. This timing
does not describe the entire conversation or Git collaboration time.

No media read/decode, model/Torch import, GPU, research download, training,
environment change, prediction-body read or historical experiment rerun took
place. This one-off private inspection is complete; its permission does not
authorize another read during the subsequent public planning round.

## Joined metadata: what matches and what remains unknown

| Check | Final observed count | Interpretation |
|---|---:|---|
| Annotated videos / nongold questions | 50 / 1,182 | Full metadata scope, before old-source exclusions. |
| Official manifest rows | 9,645 | The existing authorized official version list. |
| Unique annotation-to-manifest UID joins | 50/50 | No question-to-container UID mismatch found. |
| `release_1` / canonical validation flags | 50/50 for each | Recorded release/validation fields, not independent current access certification. |
| Source field / declared canonical-MP4 duration agreement | 50/50 for each | Metadata agreement, not decoded duration or a PTS bridge. |
| Distinct recorded `(video_source, origin_video_id)` groups | 50 | Recorded grouping only. |
| Distinct nonempty participant identifiers | 35 | Potential grouping covariate, not certified physical-recording independence. |

Current rights/access, capture/session/shot/edit independence, crop start and
annotation-zero-to-PTS certification remain **UNKNOWN**. A different UID,
recorded origin or participant does not by itself prove all these properties.
No additional private mapping was opened to exclude 013/014 or R1–R6 here;
all feasibility bounds below include them and can only shrink after exclusion.

## Task availability and the failed sample-size assumption

| Task family | Questions |
|---|---:|
| navigation/object_retrieval | 13 |
| navigation/object_retrieval_image | 13 |
| navigation/room_to_room | 7 |
| navigation/room_to_room_image | 7 |
| perception/information_retrieval/factual_recall | 250 |
| perception/information_retrieval/sequence_recall | 88 |
| perception/information_retrieval/temporal_distance | 31 |
| perception/tracking | 14 |
| reasoning/causal | 15 |
| reasoning/counterfactual | 21 |
| reasoning/predictive | 40 |
| reasoning/spatial/layout | 5 |
| reasoning/spatial/proximity | 91 |
| reasoning/spatial/relationship | 180 |
| reasoning/temporal/duration | 120 |
| reasoning/temporal/frequency | 146 |
| reasoning/temporal/prerequisites | 59 |
| summarization/compare_and_contrast | 10 |
| summarization/key_events_objects | 57 |
| summarization/temporal_sequencing | 15 |
| **Total** | **1,182** |

The 024 task whitelist admits 208 questions. Across all task families, 169
questions contain a standalone `before/after/then/earlier/later` marker; 102
are in that whitelist: 50 sequence-recall, 28 temporal-distance and 24
prerequisite questions. Each video contributes at most four whitelist-plus-
marker questions; the two largest counts are **4 and 4**. Therefore two videos
can supply **at most eight such candidates**, even before semantic checks and
old-source exclusions. They cannot meet the old minimum of twelve under this
screen. This is not a claim that every conceivable two-event form in the
dataset has been counted. A broader rule would be a new protocol, not a repair
that can silently change 024 after the fact.

The initial conservative yes/no or explicit-order-comparison grammar matched
zero questions. That grammar excluded WH time-gap forms; its zero is evidence
of an inappropriate parser, not absence of temporal questions in the dataset.

Of 31 temporal-distance-labelled questions, **28 explicitly ask a time gap
between two specified events, one in each of 28 different videos**. The other
three, in one video, ask for an object count, ingredient or vegetable rather
than a time gap. A task label alone is therefore insufficient qualification.
The 28 is an inspected text-form count, not the output of a future frozen
parser, a five-option/gold validation count, or a final eligible denominator.

Sequence-recall also includes forms with two given boundary events and an
unknown intervening event, as well as forms with just one specified event.
Prerequisite questions can ask for an unknown preceding action. These are
different retrieval tasks; they must not be pooled as AB-versus-BA truth labels.
In a time-gap question the order is already part of the nongold premise.

## Decision and next work

**NO-GO for rerunning the closed 024 design unchanged. GO for a bounded public
implementation of the corrected data/selection/scoring interface. Real-model
benefit and a publishable mechanism remain UNKNOWN.**

The [new protocol](../research-protocols/temporal-distance-diagnostic-2026-10-20.md)
focuses on question-specified temporal constraints. It matches the ordered and
unordered anchor quota, removes the false rank-as-presence gate, and separates
nongold preparation from final batch-only scoring. The unique next task is
[VLM-TEMPORAL-EVIDENCE-ADAPTER-025](../codex-artifacts/VLM-TEMPORAL-EVIDENCE-ADAPTER-025/README.md),
public-code-only. Future real sample counts must be frozen from genuinely
eligible sources; two time-gap videos imply at most two such questions here,
not twelve. No media/GPU/download/gold budget is created or renewed.

**NOVELTY=RETAIN0; CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; Charades FINAL_MEDIA_STOP.**
