# 025 public CPU adapter contract receipt

Date: 2026-10-20 (Asia/Shanghai). Parent: `VLM-TEMPORAL-EVIDENCE-ADAPTER-025`.
Synced public baseline: `dee3031519cc8c810a0e72d1b222dcda8f047a7c`.
User explicitly triggered 025. Current AGENTS, board, results, overview,
[README](./README.md), [protocol](../../research-protocols/temporal-distance-diagnostic-2026-10-20.md)
and all three referenced public reviews were read. Exactly one READY board
parent and no earlier 025 parent result were found. No historical task reran.

**Disposition: PUBLIC_ADAPTER_CONTRACT_PASS — invented data and code only.**
All thirty new test methods passed in the final supervised verification. The
first of the two permitted launch attempts stopped in the access guard before
any test assertion ran; that failure is included below, not hidden or reset.

## Delivered interfaces and assertions

| Component | Result | Evidence / limit |
|---|---|---|
| Streaming nongold screen/inference projections | PASS | Value-decoder instrumentation verifies skipped gold, reference, canary and out-of-batch values are not decoded. Screen excludes options; inference retains only five required string options. Nested metadata, original indices, UID consistency and protected-value mutation invariance asserted. |
| Lexical validation and bounded inputs | PASS | Escaped duplicate keys rejected even in discarded objects; skipped strings/huge numeric literals not materialized as scalar tokens; one-character chunks, Unicode, escaping, truncation, malformed numbers, depth/byte/string limits and safe constant errors exercised. |
| Narrow time-gap grammar | PASS | Supplied A-before-B form, case/whitespace/comma normalization; ambiguous auxiliaries, nested markers, unsupported or mislabelled forms rejected. No learned decomposition or inferred answer. |
| Four-arm selection | PASS | Same 48 inputs and twelve chronological distinct output indices; C and D always have two distinct anchors with identical scoring/fill/tie rules. Reverse maxima give a genuine difference; already ordered maxima give identical C/D outputs. Swapping event vectors changes the order-constrained problem. |
| No false presence certification | PASS | Fully tied, negative and shared-maximum score cases retain `EVIDENCE_PRESENCE_UNVERIFIED`. No rank threshold, semantic absence gate, hidden score clipping or candidate repair. Invalid PTS/numbers/range/length/types rejected. |
| Immutable cohort and queue | PASS | Frozen source order/original question index, explicit unsupported exclusions, full four-arm rotation and no deduplication of coincident frame sets. Mutable projection components rejected. Options never enter event clauses or plan fields. |
| Separate one-shot final scorer | PASS | Unfrozen/incomplete/nonterminal/forged queues or live-child receipts deny scoring with zero opener calls. After the logical gate, exactly one injected stream opens and closes; second attempts and failed-open/parse/close retries denied. Only current-batch gold scalar values decoded. |
| Full planned denominator and pair accounting | PASS | Strict prediction parser, missing/bad/numeric gold, INVALID/FAILED/NOT_RUN, per-source reports, partial-known counts and six hand-computed pair tables asserted. Bad gold yields full-denominator accuracy/pairs UNKNOWN, not a smaller scored cohort. |
| Scope | PASS in final verification | No third-party/model modules loaded; exactly three new public source reads and 35 standard-library reads; zero access-guard denials in the completed run. |

All identifiers, questions, options, labels, numeric features, terminal ledgers
and process receipts used in tests were newly invented fixtures. No private
question was copied into a fixture. Fixture correctness/pair tables are test
oracles, not real QA measurements; this receipt reports no model accuracy.

## Two-attempt execution and budget accounting

Both owned test children used existing Python with `-I -S -B`, a 60-second
parent-enforced `communicate` timeout and no child-created subprocesses. The
watchdogs were allowed to terminate only their own test child. They never
queried GPU state or other jobs. Source loading and audit guards were launcher
code, not environment installation or modification.

| Launch | Outcome | Owned-child wall time | Coordinator wall time |
|---|---|---:|---:|
| 1 | Exit 1: import-time read rejected by whitelist; 0 test assertions executed | 0.119151 s | 0.119202 s |
| 2 | Exit 0: 30 PASS, 0 FAIL, 0 ERROR, 0 SKIP | 0.342630 s | 0.342681 s |
| **Controlled totals** | **Two launches; no further run** | **0.461781 s / ≤180 s** | **0.461883 s / ≤240 s** |

The first trace stopped in importlib's `get_data` at the file-open audit guard.
It did not identify the denied filename, so no claim about that file's contents
or identity is made. The launcher was statically revised to compile/execute
only the three exact newly authorized source texts into their named modules,
avoiding import-loader reads of other public cache artifacts. There was no
production-code change between the two launches. The second child reported
0.279879 seconds including its initialization and a unittest body time of
0.198 seconds. No timeout or owned-child kill occurred.

The guard blocked filesystem writes, nonallowlisted reads/directory access,
research network calls, subprocess creation, ctypes use and model/third-party
imports. Only the new source files and standard-library locations were
admitted; site-packages were excluded. The initial guard rejection counts as
a failed launch, not a passed test or evidence of a private-data read.

These are measured controlled child/coordinator intervals from two invocations,
not total conversation wall time or source-editing/Git time. No old 023 tests,
historical runner or model check was used to increase the PASS count.

## Implementation boundary and scientific disposition

The projector traverses an injected text container and decodes object keys to
check duplicates; skipping protected values does not imply reading only batch
bytes. It has explicit 64 MiB input, 64-container nesting and 64 KiB admitted
string ceilings; it also limits an exact requested batch to 10,000 keys. These
are implementation bounds, not authorization to open any real annotation.
Schema/grammar mismatches fail conservatively; no claimed coverage of the
previously inspected 28 real text forms was tested in 025.

The scorer enforces an in-memory logical gate and one-shot state per instance.
It requires a nonempty matched launched/exited child registry. It cannot prove
real OS exits, gold-denied GPU processes, durable cross-process no-retry state,
licence validity or trusted source identity. A new scorer object is not a
durable authorization guard. Any future real wrapper still needs an explicitly
authorized supervisor, observed exits and independently enforced scoring boundary.
It must also bind the preparation/scoring input to the same trusted snapshot;
this injected-stream prototype does not authenticate cross-phase file identity.
No live-model runner or execution switch was added. Actual processor/grid,
visual-token equality, text truncation, resource peaks, real paired accuracy,
source independence and semantic evidence recall are **NOT_RUN/UNKNOWN**.

Public call planning is usable for future integration, not a claim that the
private 017/018 runner is now safely integrated. Raw-cosine pair ranking does
not establish event identity, correct occurrence binding or Qwen reasoning.
The four-source/one-question future diagnostic remains a proposal needing its
own accepted recorded-group scope, evidence and specific resource/data/gold
authorization. No 024 budget or strict physical-independence gate was reopened.

Research-private metadata/media/QA/options/gold/old outputs/source maps/model
reads: **0**. GPU/model forwards/generate/training: **0**. Research downloads,
environment changes, unrelated directory scans and private writes: **0**.
Only three new Python files, this anonymous receipt and one append-only parent
result are submitted. Historical code/receipts, AGENTS, plans, task README and
protocol are unchanged. One ordinary safe main push, then STOP.

**REAL_QA_EFFECT_UNKNOWN; NOVELTY=RETAIN0; CLOCK_ZERO_ASSUMED_NOT_CERTIFIED;
Charades FINAL_MEDIA_STOP. TRAIN-GPU remains HOLD.**
