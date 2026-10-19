# VLM-ORDERED-EVIDENCE-023 — synthetic OEP-12 implementation and counterexamples

2026-10-19 (Asia/Shanghai). **SYNTHETIC_IMPLEMENTATION_PASS**.
**REAL_QA_EFFECT_UNKNOWN; NOVELTY=RETAIN0**.

The clean, separate public checkout was safely fast-forwarded from `8aba2e3`
to `25f56316a0bb336e624a72eb59927aef5d3c455d`. Latest AGENTS, task board,
results, overview, 023 README and the frozen
[research protocol](../../research-protocols/ordered-evidence-2026-10-19.md)
were reread. Exactly one task-board row was READY (023), with no prior 023
parent result. The 017/018 public anonymous receipts supplied historical
context only; no historical experiment or asset/environment check was repeated.

## Implemented contract

Two new standard-library modules:

- [Pure selector](../../../prototypes/ordered_evidence_selector_023.py):
  `oep12`, `global_top12`, `unordered12`; immutable selection/pair records.
- [Synthetic tests](../../../prototypes/test_ordered_evidence_selector_023.py):
  31 independent unittest methods with real assertions and negative witnesses.

The API accepts only list/tuple arrays of exactly 48 toy nonnegative integer
IDs, 48 finite strictly increasing relative PTS, three normalized finite
numeric score arrays in [0,1], and an actual decomposition bool. IDs must be
unique. Booleans are rejected as numeric scores/IDs/PTS. The API has no text,
options, answer, real UID, feature, file-path or relation-truth argument and no
file/network/model operation. Calling it on real evidence is outside this task.

Budget is fixed at 12 and synthetic tau at 0.70. For AB, enumerate i<j with
sA[i]>=tau and sB[j]>=tau; BA uses sB[i] and sA[j]. Each direction maximizes
its two-score sum, with exact Python numeric comparisons and lexicographically
earliest (i,j) resolving ties. A missing direction is UNSUPPORTED, not invented.
Union the supported pairs' endpoints (at most four anchors), then fill remaining
slots from the same global sQ ranking. Its ties use earlier PTS/index. Output
contains exactly 12 unique frames in PTS order, with separately exposed anchors
and direction candidates; no field claims AB/BA truth or causal validity.

When decomposition is unavailable, direction status is NOT_EVALUATED and the
selected indices/IDs/PTS exactly equal Global Top12. With decomposition but no
qualified pair in either direction, both are UNSUPPORTED and frame selection
is also exactly Global Top12. Validation runs before either fallback. Invalid
lengths, IDs, PTS, scores, containers or bool flags return an explicit reasoned
HOLD with empty selections; no sorting, frame duplication, coercion, budget
expansion or silent repair occurs.

The unordered ablation is concretely frozen as the earliest maximum-support
frame per event independently, provided each maximum meets the same tau.
Deduplicate coincident maxima, then use identical sQ filling and chronological
output. A lone supported event can supply one anchor; both event maxima can
collapse to one frame. It does not test i<j, emit an ordered pair, or infer a
relation. These limitations are asserted rather than hidden by extra frames.

Finite increasing PTS may have a negative relative origin. The protocol does
not require nonnegativity; translation of the time origin preserves selected
indices and pair directions. This does not certify any real annotation clock.

## Bounded execution and results

Only this task's new unittest module was executed, in two supervised owned
children, each with a 60-second communicate deadline and termination on timeout.
The second deadline also subtracted prior controlled execution from the
240-second parent budget. No third run occurred. Python used isolated mode,
disabled site initialization and disabled bytecode writes (`-I -S -B`). The
in-memory child bootstrap denied socket events, subprocess creation, shell
execution and ctypes library loading; the only child process creation was by
the owning supervisor. No private helper, log or cache was written.

| Execution | PASS | FAIL | ERROR | task/test HOLD | SKIP | unittest seconds | supervised parent seconds | exit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| First implementation | 30 | 0 | 0 | 0 | 0 | 0.015 | 0.140 | 0 |
| Final protocol-aligned revision | 31 | 0 | 0 | 0 | 0 | 0.014 | 0.140 | 0 |

**Final unique tests: 31 PASS / 0 FAIL / 0 ERROR / 0 HOLD / 0 SKIP.**
Expected input-HOLD cases are passing rejection assertions, not skipped or
blocked tests. Controlled CPU test execution totaled 0.280 supervised seconds,
below 240 seconds; both children completed below 60 seconds. Editing and Git
collaboration are not additional test invocations. Both loaded-module checks
reported torch/numpy/transformers/av absent.

After the first passing run, one static protocol review removed an unnecessarily
strict nonnegative-PTS condition and added the time-origin assertion (test 31).
The single permitted revision was validated by the second/final run; no failed
outcome was retried or concealed. No third-party test, old task or dynamic
environment/model validation was executed.

| Tests | Asserted behavior / counterexample |
|---|---|
| 01 | 48 inputs yield exactly 12 unique PTS-sorted outputs for all three policies. |
| 02 / 03 | AB-only and BA-only inputs never fabricate the opposite direction. |
| 04 / 05 | Both directions retain four distinct anchors; tied pair sums choose earliest indices. |
| 06 / 07 | sQ ties follow chronology, not ID value; no-event fallback equals an independently calculated nonuniform Top12. |
| 08 | Missing decomposition ignores apparent event pairs and exactly falls back. |
| 09 | Single-event sQ crowding makes baseline omit B at index 30; OEP retains A/B anchors (0,30) at unchanged budget. |
| 10 | Reversing event evidence on a valid increasing synthetic timeline swaps direction status. |
| 11 | Pure arithmetic: abs difference/elementwise product is unchanged by frame exchange, while ordered concatenation differs. |
| 12 / 13 / 14 | Duplicate IDs, repeated PTS and descending PTS HOLD with no repaired output. |
| 15 / 16 / 17 | Nonfinite/nonnumeric timestamps, illegal scores in all channels, and all wrong lengths HOLD, including insufficient candidates. |
| 18 | tau is inclusive; just-below-threshold evidence is unsupported. |
| 19 / 20 | A single doubly high-scoring frame is not an ordered pair; shared endpoints across directions deduplicate. |
| 21 | Unordered event maxima differ from pair-constrained anchors; sum ties remain lexicographic. |
| 22 | Repeated A-like instances around B support both candidate directions without authenticating an instance identity. |
| 23 | Sixteen fixed-seed synthetic score worlds match an independent exhaustive-combinations optimum for both directions. |
| 24 / 25 / 26 | Repeated calls are deterministic and do not mutate inputs; illegal flag/ID types and invalid fallback inputs HOLD. |
| 27 / 28 | Unordered ties/lone events are explicit; nonuniform actual synthetic PTS preserve chronological behavior. |
| 29 | Low-sQ anchors evict higher-sQ baseline frames: retention is not a dominance or QA guarantee. |
| 30 / 31 | Reject iterators/strings without consumption; finite increasing negative-origin PTS remain valid and translation-invariant. |

## Falsification findings and limits

The code demonstrates a conditional anchor-retention guarantee, not an event
detector or answer solver. Threshold-qualified scores can be wrong. Repeated
actions or visually similar but unrelated instances can generate both directions
from indistinguishable inputs. A single-frame A/B maximum can collapse the
unordered control; OEP instead requires distinct frames but still cannot verify
event identity. Swapping evidence positions changes candidate direction state,
which is weaker than showing Qwen actually reasons about temporal order.

Retaining anchors can remove useful question-related frames (test 29), and
fallback can miss a rare event (test 09). Neither policy dominates on all worlds.
No event decomposition, real score normalization/calibration, semantic evidence
recall, actual Qwen 324-token construction, retrieval latency, accuracy,
source-general performance or novelty was measured. O(48^2) pair enumeration
and O(48 log 48) filling are small synthetic algorithmic costs; they do not
include future event-query/embedding/model costs. The .70 threshold must not be
reused as an assumed calibrated real SigLIP cosine boundary.

Future scientific evaluation remains separately gated by legal, unseen,
physically independent source groups, clock evidence, fair near-neighbor
baselines and explicitly authorized resources. Old 013–018 development
questions/gold/outcomes cannot be reused as a blind test or fit the selector.
The protocol's proposed 8-group/120-question target and failure rules remain
paper requirements, not a license to acquire data or run models.

## Publication and stop boundary

Exactly four allowed paths are changed: two new Python modules, this anonymous
receipt and one append-only 023 parent result. Historical logs, README, research
protocol, planning files and previous implementations are unchanged.

Private media/stat/probe/decode, protected QA/gold, UID/source maps, real model
features/weights, Torch/model imports, GPU/driver APIs, optimizer updates,
training, research network/downloads, environment changes and private writes:
all zero. Only public repository evidence and standard-library code were used;
ordinary Git synchronization/publication is the network exception. No private
path, identity, media name, hash, prediction or raw private log is published.

**REAL_QA_EFFECT_UNKNOWN; NOVELTY=RETAIN0;
CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; Charades FINAL_MEDIA_STOP.**
TRAIN-GPU remains QUEUED/HOLD. One ordinary main push, then STOP for review;
no GPU or other follow-on task starts automatically.
