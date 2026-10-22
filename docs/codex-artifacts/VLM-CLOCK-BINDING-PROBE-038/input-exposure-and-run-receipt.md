# 038 input exposure and bounded synthetic run

2026-10-22, Asia/Shanghai. **INPUT_EXPOSURE_PASS / REAL_SYNTHETIC_GENERATION_COMPLETE / SCORED.**
This is a new owned synthetic probe, not a recovery of C/D or a natural-video experiment.

## A/B: authority, implementation and separation

Clean independent documentation main was safely fast-forwarded to `aa51e93`.
AGENTS, current board/results/overview,038 README, the
[scientific protocol](../../research-protocols/clock-visual-binding-probe-2026-10-22.md)
and [post037 disposition](../../research-decisions/post-037-scientific-disposition-2026-10-22.md)
were reread.038 was the only unreported READY parent; the user's complete new
scope activated this run. Old C/D remains NO_GO_AS_CORE.

Two new modules: [probe](../../../prototypes/clock_binding_probe_038.py) and
[new stdlib witnesses](../../../prototypes/test_clock_binding_probe_038.py).
Read-only reuse is confined to the existing pure command/Win32 Job/lock helpers
and resource XML parser; no historical Journal/run/test was instantiated.

A new dedicated038 root and exclusive parent lock were created once, never
deleted or resumed. Its fresh append-only hash-chain ledger records reservations,
48 unique STARTED records,48 terminal records, actual model exit, queue closure
and STOP. One live coordinator held the lock throughout execution. The overall
deadline was conservatively bounded from before the public-main sync, including
implementation time, rather than resetting it when the coordinator started.

Exactly the five permitted036 files were read once each: closed ledger plus
startup/runtime/device/policy configurations, totaling **62,761 bytes**.
Their stat/size/SHA evidence stayed private. The ledger chain, REAL_036/STOP,
three bootstraps and absence of real model/gold actions were checked read-only.
Only Qwen/runtime/device fields were retained; old helpers, scientific prompts,
annotation references and SigLIP assets were not opened or used.

Two exact Qwen configuration files contributed **1,895 bytes**. Three authorized
installed modules (processing_qwen3_vl.py, video_processing_qwen3_vl.py,
video_utils.py) contributed **62,566 bytes**. **Research-text total:10 external
opens /127,222 bytes**, below12MiB. Exact copied sources established the local
VideoMetadata API, native timestamp insertion and temporal-block averaging.
No upstream-version assumption or environment change was needed.
Normal local runtime/CPU processor assets, and later the conditional Qwen
weights, were loaded by their separate execution roles, not counted as these
ten research-text reads; their total runtime I/O bytes were not instrumented.

## C/D: one new suite and actual CPU input gate

**16/16 new stdlib tests PASS**,0 failures/errors/skips, internal0.026s,
supervised Job window0.203s. Assertions cover complete rotated48 queue, truth,
clock maps/translation, color exchange, owned pixels, strict answer parsing,
tampered/truncated ledger rejection, incomplete/active exit, duplicate STARTED,
binding mismatch and full denominator. No old suite was run; no second suite.

One actual CPU exposure child: internal8.188s, supervised8.813s, exit0/Job0.
NumPy1.26.4, Torch2.5.1, Transformers4.57.6; Qwen3VLProcessor.
**CUDA remained uninitialized. CPU model weights0, no forward.**
No compatibility failure, repair or second input preflight occurred.

All48 inputs were constructed one at a time, not accumulated as full tensors:

| Input fact | Actual observation |
|---|---|
| Owned RGB |12×192×288×3 uint8, protocol background/central-square colors, paired identical frames |
| V per world across clocks | Same raw-RGB binding and same model-visible BF16 visual-tensor binding;24 V checked |
| Native G0 timecodes |0.5,4.5,8.5,12.5,16.5,20.5 seconds |
| Native G1 timecodes |0.5,2.5,6.5,14.5,18.5,20.5 seconds |
| Native G2 timecodes |60.5,64.5,68.5,72.5,76.5,80.5 seconds |
| Native grid/tokens | Every V: `[6,12,18]`,324 video tokens; V input length427 or430 |
| Text control |24 O, zero video tokens/no visual tensor; input length58 or59; exact matching operands |
| Text intervention | All six decoded native timecodes match; same normalized V prompt after replacing only timecode strings; full/text bindings differ across clocks |

The native processor received explicit fps1, frozen frame indices/total frames,
do_sample_frames=False and do_resize=False. No MP4, decode, manual token editing,
fake inserted timestamps or changed scientific constants. Six timestamp blocks
were verified by decoding actual input_ids, not just reading metadata.

Bindings include tensor keys, shape, dtype and content. CPU signatures apply
the declared final BF16 cast to floating tensors; integer tensors stay int64.
For V the visual payload is `[1296,1536]` BF16 plus `[1,3]` int64 grid.
During the model phase, every slot was rebuilt, matched against its CPU receipt,
transferred to CUDA, then copied back for an additional exact final-representation
binding check before STARTED. This certifies the model-visible dtype path;
it is not a separate bitwise claim about all pre-cast float32 intermediates.

Frozen execution code SHA256:
`5fc6eee79ff5c8518ccd1dd64f256edef693eeb986fe48b82041f177887eefd2`.
Spec SHA256:
`a387a92dd20059428ef3872dfe526be0d74fa3e99c1ecd906591c0e0b2c23316`.
Queue SHA256:
`59f0975d3790ca9c897fc7c3817c21d24c2ed8cac1beb83b306553126c6c5274`.
These are public-code/synthetic bindings, not weight or private-source hashes.

## E/F: single model phase and independent score

One current nvidia-smi query (query child0.656s) matched the frozen3090/index/
UUID/bus; free22,954MiB, utilization10%,29 existing C+G contexts were recorded.
Utilization/contexts did not veto or grant exclusivity. Private device identifiers
are omitted. The sole worker passed its additional torch free≥20GiB predicate
before weights; that second free value was not separately retained.

One local-only Qwen3-VL-4B load, BF16/SDPA/eval/inference_mode, seed19.
All48 slots followed the frozen per-world left rotations. Each had fresh messages,
no previous replies/past-key-values, batch1, greedy and max_new_tokens16.
No warmup, extra forward, model restart, requery or repeated slot.
Inherited sampling-only generation-config flags produced an ignored-flags warning
under do_sample=False; a torch_dtype deprecation warning was also retained.
Neither warning triggered any parameter change or retry.

**48 STARTED /48 actual generate /48 RETURNED; INVALID0/FAILED0/NOT_RUN0.**
All48 returned EOS,0 truncation,121 generated tokens total.
Generation-call time8.673s; worker load-stage time25.265s (includes imports and
processor/free setup); internal worker35.922s; complete supervised model Job36.703s.
Peak allocated **9,140,584,960 bytes**, reserved9,189,720,064 bytes;
model Job peak committed **17,851,752,448 bytes**, below24GiB.

Model exit0 and actual Job active0 were observed before scoring.
Ledger order: MODEL_EXIT seq109 → QUEUE_CLOSED seq110 → scorer reservation seq111.
The independent stdlib scorer consumed an exclusive one-use guard, checked
48 terminal slots/unique STARTED/input bindings/actual exit and frozen
code/spec/queue, then read this run's program truth once and rederived it from
the frozen source constants. Exit0/Job0,0.156s. No original annotation/gold
or old predictions participated. Model/config choice was frozen by the exact
configuration-read receipts and unchanged local runtime config; this is a
trusted local execution binding, not an adversarial snapshot of model storage.

## G/H: resource close and delivery

| Resource | Actual / limit |
|---|---|
| New suite / CPU exposure |1×0.203s /2×60s;1×8.813s /2×90s |
| Non-model supervised children |9.828s combined wall; not per-PID kernel CPU measurement |
| Conservative CPU reservation |250s incl60s initialization/bookkeeping allowance /480s |
| Full model Job |36.703s /600s,1 worker,1 load,48/48 calls |
| Parent through execution cleanup |725.944s from conservative pre-sync origin /1800s |
| New private output after final summary |25 files,159,595 bytes /96 files,64MiB; no reparse entries |
| Actual child exits |All five children exit0/Job0; no kill, overflow or timeout |

Resource-evidence limitation: the separate prelaunch2GiB disk-headroom check
was omitted. A post-run check found433,993,371,648 bytes free, but cannot
retroactively certify that precondition. The observed output is below quota;
this omission is retained explicitly rather than labelled a fully evidenced
resource preflight. No additional run or test was used to repair the record.

No external real annotation/QA/gold/old frames/predictions/manifest/source map/
private helper access. Experiment networking, media/download/decode, training,
installation, permanent environment/ACL/profile/credential changes all0.
Child-only TEMP/cache routing and offline flags were used. The audit denies
network, arbitrary subprocesses, out-of-policy reads/writes and model access
to the score directory; it is not a whole-machine malicious-code guarantee.
No original-annotation handle/probe certificate is asserted.

See [scientific results](./scientific-results.md) for all48 outcomes and the
fixed interpretation. Only two new modules, two reports and one038 results
append are delivered; old code/tests/protocol/planning/history are unchanged.
One ordinary safe push then STOP; no039/extra generation/expansion/training.
