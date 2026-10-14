# VLM-PD-LONGVIDEO-007 — official variant qualified, media read timed out

Date: 2026-10-14 (Asia/Shanghai). Clean independent documentation checkout safely synced to main `1f81d2f`; latest AGENTS/task board/results/overview, new downloader and referenced trainer contract were read. Unique READY and no existing 007 parent result were confirmed. This was one new parent execution with independent budgets, not a rerun of 005 or 006.

**Outcome: MEDIA_READ_HOLD / exact reason_code `timeout`.** Official metadata/schema and structured US Public Domain gates passed; the actual official API supplied one allowed 240p VP9 derivative. The one media GET returned HTTP 200 with admissible declared length, but body reading raised the Python timeout exception. No complete video, CPU decoding or GPU updates resulted.

## Offline and source gates

The two public scripts were copied into a new private task-owned directory; UTF-8 AST checks and ancestor no-reparse checks passed. New downloader explicit offline selftest passed: three positive cases (360p alone, 240p alone, both with 360p priority) and six rejection fixtures. Its internal pre-request selftest also passed.

Private-only conservative adjustments preserved the frozen whitelist/source/budgets: precheck duplicate counts across both whitelist keys (the original early return could overlook a duplicate fallback key), persist the two allowed-key counts, response status, media declared-body reservation, cumulative successfully returned body bytes and terminal reason_code. Public sources and historic task files/ledgers were unchanged. No expanded key, inferred address, alternate input or extra HTTP diagnostic was introduced.

| Official API qualification | This execution |
|---|---|
| Metadata GET attempts / HTTP status | **1 / 200** |
| Complete metadata application bytes | **3,155**, below 512 KiB |
| JSON/API/schema/file title/videoinfo | **PASS** |
| Structured Public Domain fields | **PASS, US declaration** |
| Exact `360p.vp9.webm` count | **0** |
| Exact `240p.vp9.webm` count | **1** |
| Chosen frozen whitelist variant | **240p.vp9.webm** |
| Actual official HTTPS/domain/transcoded-path/suffix gate | **PASS** |

The chosen address came solely from the actual API src field, not from URL synthesis or a webpage. Default TLS verification, explicit proxy disabling and redirect rejection were retained. The copyright evidence is jurisdiction-specific US Public Domain metadata, not a universal legal guarantee. This execution qualifies the requested official source representation; it does not independently certify worldwide legal status or decoded film duration.

## Actual acquisition and failure

Exactly **2 data GET attempts**: metadata1 + media1. Media returned **HTTP 200**, permitted content type/identity encoding and declared length **37,316,857 bytes**, below 100,663,296 bytes (96 MiB). That full declaration was persisted as the conservative body reservation before reading and is not refunded after failure.

Successfully returned media chunks were accumulated and fsynced through **458,752 bytes**. The private part exists at **458,752 bytes**; no completed WebM exists and no atomic completion/SHA success was recorded. This equality corroborates the successful application-read count, not full network reception. The final unsuccessful read may have received SDK/socket buffer data that was never returned; its additional quantity is **UNKNOWN**. Therefore total received application-body bytes are not falsely asserted to equal the part size; the conservative reservation remains the full **37,316,857 bytes**. Metadata/body categories are separate and TLS/wire traffic was not measured.

The private terminal record has **reason_code `timeout`**, matching the caught exception class. Failure occurred during body reading after successful metadata and media headers. It was not an exact-key mismatch, license-field failure, HTTP denial, 96 MiB overflow or GPU resource failure. The downloader used its existing 40-second connection/read timeout and monotonic 600-second acquisition checks; the observed stop was the read timeout, not a reported 10-minute deadline. Precise whole-stage duration was not persisted. The 600-second loop guard checks before blocking reads; with a 40-second read timeout it is not an independently supervised exact hard deadline. No hard-deadline PASS is claimed from this code alone; this limitation must be addressed before a future acquisition relying on that boundary.

HEAD/Range/redirect-follow/retry/mirror/original-version/second-video requests: **0**. The failed one-shot request and reservation remain consumed. The part was retained privately without repair, copying, rename, resume or another request.

## Conditional long-video experiment

Since no complete eligible video existed, CPU decoder/PTS span, ≥350 retained samples, ≥1,200-second observed duration, training/validation split and GPU resource/mutex checks were **NOT_RUN**. The trainer was only copied and AST-checked, never invoked.

| Metric | Uniform128 | Motion128 |
|---|---|---|
| Actual backward / optimizer updates | **0 / 0** | **0 / 0** |
| Selected real-frame samples | **NOT_RUN** | **NOT_RUN** |
| Loss, parameter delta, fixed-pair validation accuracy | **NOT_RUN** | **NOT_RUN** |
| GPU time / allocator peak | **NOT_RUN** | **NOT_RUN** |

No complete-container/EBML/SHA or true ≥20-minute PTS assertion is made. No former flower clip, Ego4D part, Charades/HourVideo asset or synthetic substitute was used. This batch yields official variant qualification and a real transfer blocker, not a paired training result.

## Scope and stop

No AWS/Ego4D/HourVideo/Charades requests, protected QA/credentials, weight downloads, model/cloud API calls, CUDA infrastructure retest, environment/PATH/driver change, process termination, original research workspace access or historical asset mutation occurred. All partial media, execution copies and detailed ledger stay private; no raw JSON/src/path/hash/frame/feature/model/log is uploaded. Only this authorized Markdown receipt and one appended results record are submitted.

After one ordinary main push, STOP; no queued experiment, new request or automatic continuation. **NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP** and HourVideo/Ego4D release/PTS bridge **UNKNOWN** remain. Any future transfer remedy needs a separately authorized contract; no remaining allowance is used here.
