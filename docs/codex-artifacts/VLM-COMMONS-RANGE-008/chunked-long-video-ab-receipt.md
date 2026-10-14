# VLM-COMMONS-RANGE-008 — offline protocol verified, strong-ETag gate hold

Date: 2026-10-14 (Asia/Shanghai). Clean independent docs checkout safely fast-forwarded to main `10e0de4`. Latest AGENTS, task board, results, overview and 008 README were read; unique READY/no existing parent result confirmed. The user's current message explicitly authorized this new independent metadata1/HEAD1/Range24/48 MiB interval budget and conditional two-arm GPU experiment. No old parent budget or part was reused.

**Outcome: SOURCE_NOT_RANGE_SAFE_HOLD_ETAG.** Official metadata/source checks passed. HEAD returned 200 and the required object length, but its ETag did not satisfy the strict usable-strong-ETag requirement. Therefore **Range GET0 and both GPU arms0**. No request was made to work around this gate.

## Offline implementation and tests

A new task-private standard-library single-threaded Range worker and independent subprocess supervisor were implemented. Its existing private directory ancestors were checked for Windows reparse points; all current Python sources passed UTF-8 AST parsing before networking. Referenced public source checks and the frozen trainer were copied read-only into this new private directory; public source files and prior private tasks remain unchanged.

**21/21 offline protocol tests PASS, 0 failures/errors**, elapsed 0.251 s. Tested acceptance/rejection categories include valid206, whole-object200 rejection without a body read, wrong Content-Range, changed/weak/empty ETag, mismatched length, encoded body, duplicate security headers, oversized chunk, uncommitted offset, duplicate commit, same-interval retry reservation/third-attempt rejection, cumulative48 MiB and24-request caps, short reads, exact bounded reads, expired monotonic deadline, UTC-offset independence, actual supervision of a disposable owned child, and complete18-interval planning.

The budget simulation conservatively reserves every requested interval, including a repeated failed interval, without refunds. Actual implementation chose no automatic retry: the contract allows up to one limited retry but does not require it when uncertainty exists. Simulation results do not represent a media acquisition or GPU experiment.

## Independent 75-minute supervisor

The supervisor uses `time.monotonic()` exclusively. It launches only this task's precisely owned worker through its Popen handle, watches for ≤4,500 seconds, and would terminate/wait on that handle only if the worker hung; a kill fallback is limited to the same owned handle. It does not enumerate, terminate or unlock another user's process. Its short offline test really launched a no-network sleeping child and stopped that owned test child after a 0.15-second monotonic allowance; that test passed. No real acquisition process was terminated in this run because it exited normally on the gate hold.

The real network worker also checks a monotonic acquisition deadline between bounded reads. Direct standard-library HTTPSConnection uses verified default TLS, no proxy inheritance, connect timeout15 s and socket read timeout≤120 s, fixed official hosts, and no redirect or hidden retry. Independent supervision supplies the hard outer boundary that the prior per-read loop alone lacked. This was not a 75-minute stress test; it verifies the mechanism and confirms the actual run terminated within the guard.

## Actual official metadata and HEAD

| Actual check or counter | Result |
|---|---|
| Metadata GET attempts | **1 / 1** |
| Metadata HTTP status/body | **200 / 3,155 bytes** |
| File/schema and structured copyright evidence | **PASS / US_PUBLIC_DOMAIN_DECLARED** |
| Sole requested240p VP9 derivative and canonical source | **PASS** |
| HEAD attempts | **1 / 1** |
| HEAD HTTP status | **200** |
| HEAD Content-Length comparison | **exactly37,316,857 bytes, PASS** |
| Required strong ETag | **HOLD** |
| Accept-Ranges eligibility | **NOT_RUN after ETag hold** |
| Real Range GET attempts /206 responses | **0 / 0** |
| Interval bytes conservatively reserved | **0 / 50,331,648-byte limit** |
| Returned media body /committed bytes | **0 / 0** |
| New media part /complete media | **None /none** |

The exact terminal reason **SOURCE_NOT_RANGE_SAFE_HOLD_ETAG** was fsynced into this new private ledger and saved in the anonymous worker result. It means the HEAD ETag was absent, weak or otherwise outside the executor's strict quoted nonempty strong syntax. The returned value/subclassification was not persisted, so this receipt does not invent which of those cases occurred or publish a real ETag. It does not prove the server lacks all Range support; no206 test was authorized after this gate failed. Content-Length passed before the ETag check, while Accept-Ranges was not evaluated afterward.

Metadata response bytes are application-level counts; HEAD/media response body bytes read were0. No claim of exact TLS/wire/transport traffic is made. Default source checks and US declaration are not a worldwide public-domain warranty. No additional HEAD, conditional probe, ordinary whole-objectGET, mirror, Range attempt or old-part merge was made.

Actual worker network-stage elapsed was **9.594 s** by monotonic time. The independent supervisor recorded normal child completion within its guard. Exact whole-task preparation duration was not instrumented; no long-running CPU/GPU phase followed.

## Conditional CPU/GPU stages

No new complete film exists. SHA/EBML/ffprobe duration, real frame decoding, ≥350 samples and ≥1,200-second PTS span: **NOT_RUN**. Existing ffprobe was not called. CPU hard decoding supervision and GPU resource/mutex gates were consequently not entered or claimed as passed.

| Actual A/B metric | Uniform128 | Motion128 |
|---|---|---|
| Backward calls /optimizer updates | **0 /0** | **0 /0** |
| Selected frame samples /PTS spans | **NOT_RUN** | **NOT_RUN** |
| Loss /parameter change /late-block accuracy | **NOT_RUN** | **NOT_RUN** |
| GPU seconds /allocator peak | **NOT_RUN** | **NOT_RUN** |

The supplied frozen A/B source was only privately copied and AST-checked. No synthetic-video fallback, old short-video replay, CUDA infrastructure retest or benchmark claim occurred.

## Preservation and stop

Old005/006/007 assets, part files and budgets were neither read for media reuse nor modified. No AWS/Ego4D/Charades/HourVideo/QA or model assets were accessed; no installs/environment/PATH/driver change, other-process termination, original research workspace access or external contact occurred. All execution code, ledgers and source details stay private. Only this new anonymous Markdown receipt and one appended parent result are submitted.

After one ordinary main push, STOP. A future different validation/transfer contract requires separate approval; this gate was not relaxed. **NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP** and HourVideo/Ego4D release/PTS bridge **UNKNOWN** remain. This batch has no real long-video training or paired scientific result.
