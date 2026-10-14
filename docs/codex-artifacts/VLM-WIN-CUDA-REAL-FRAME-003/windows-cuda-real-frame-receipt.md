# VLM-WIN-CUDA-REAL-FRAME-003 execution receipt

Date: 2026-10-14 (Asia/Shanghai). Contract baseline: main `fb49adb`. One foreground execution; A and B independent; C conditional.

**Outcome: GPU_INFRA_PASS / PART_NOT_DECODEABLE / REAL_FRAME_TRAINING_HOLD.** RTX3090 CUDA allocation, backward and optimizer updates were actually executed. The existing partial media failed its CPU container probe; no real-frame training was performed.

## A — read-only partial media check

The single previously known private entry was a regular file with no reparse ancestors, outside the public checkout, in the 64–128 MiB band and below 256 MiB. No completed media file existed at the known entry. The old state remained STARTED with its existing TERMINATED_EXECUTOR_ERROR record.

Exactly one existing CPU ffprobe invocation returned a container error classified as **MISSING_MOOV**. CPU stage elapsed 0.703 s. No PyAV/OpenCV decode was attempted after that conclusive failure. Verified decoded frames: 0; actual positive/strictly increasing frame PTS: UNVERIFIED; usable time-window span: UNVERIFIED. No repair, copying, remuxing or resumption occurred. Read-only SHA comparisons of the part and the two consulted old ledger files matched before/after; no hashes or identities are published.

RAM peak was not instrumented. No frame arrays were allocated; file hashing used 1 MiB chunks. This does not claim an independently measured process-RAM peak or that the partial media represents a complete long video.

## B — actual CUDA infrastructure experiment

The known cooperative protection mutex and this task's own mutex were absent and then acquired nonblockingly. Only handles owned by this execution were released. No external locks or processes were altered.

| Resource observation | Snapshot 1 | Snapshot 2 |
|---|---:|---:|
| Target device | RTX3090 | RTX3090 |
| Total memory, MiB | 24,576 | 24,576 |
| Free memory, MiB | 22,906 | 22,906 |
| GPU utilization | 6% | 3% |

Snapshots were separated by at least 2.1 s. Both passed free ≥8 GiB and utilization ≤30%. Driver metadata contained 30 C+G contexts; that count was not treated as a blocking condition. No positively confirmed conflicting training task was found in the scoped checks; snapshots and the cooperative mutex do not guarantee exclusive device access.

Existing pytorch environment: torch 2.5.1, CUDA build 12.4. `torch.cuda.is_available()` returned True. Device 0 was verified as RTX3090. Fixed-seed linear 4→2/MSE/SGD computation used actual cuda:0 tensors.

- Actual backward calls / optimizer updates: **2 / 2**.
- MSE before each update: **1.0669527054**, **0.6710797548**.
- Loss and gradients: finite; parameter absolute-change sum: **1.0163352489**.
- Torch peak allocated memory: **18,092,032 bytes (17.254 MiB)**.
- Torch peak reserved memory: **23,068,672 bytes (22 MiB)**.
- Monotonic GPU-stage elapsed: **8.094 s**, including torch import and initialization; below 2 min. No retry, OOM or nonfinite-value recovery occurred.

Memory figures are framework allocator measurements, not a measured physical-device peak including driver/context overhead. This is a hardware infrastructure test using small synthetic tensors, not real-video research training.

## C — conditional true-frame training

**REAL_FRAME_TRAINING_HOLD: 0 backward calls, 0 optimizer updates.** A supplied no verified real frames or PTS, so the conditional training gate was not met. Signed terms for this specific training use were not independently proven in this round; no permission PASS is asserted. No features, train/validation split, head loss, checkpoint or real-video GPU-memory figure exists. The pre-existing future-heldout exclusion is not changed or promoted to independent scientific validation.

## Scope and execution integrity

Private executor AST precheck initially encountered Windows default text-encoding mismatch; explicitly reading its UTF-8 source corrected the pre-execution check. AST then passed, followed by exactly one A/B execution. That precheck failure made no CUDA or media probe call.

Measured executor foreground duration: **11.360 s** using monotonic time. No AWS, GET, Range, new media/model download, dependency installation, GPU model/backbone run, old experiment replay, original research-tree access or process termination occurred. Existing Python/PyTorch/CUDA, partial media and consulted historical ledgers were preserved. Only this sanitized receipt and one appended parent result are submitted.

Scientific status remains **NOVELTY=RETAIN0**, Charades **FINAL_MEDIA_STOP**, release-PTS bridge **UNKNOWN**. CUDA readiness is now evidenced; complete legal media and valid real-frame/PTS input remain required before a future separately authorized training task. No follow-on task is started.
