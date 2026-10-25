# 045 native PTS adapter and actual CPU boundary receipt

**CPU_NATIVE_PTS_ADAPTER_BOUNDARY_PASS / NATURAL_MEDIA_AND_TASK_EFFECT_UNKNOWN.** All9 fixed formal slots PASS after one source-located import-guard compatibility correction. Actual processor calls10/12: one construction/callback probe plus nine newly executed formal calls. No model load/forward/generate, GPU, media/decoder, labels or application network. Controlled PTS are program fixtures, not evidence of natural VFR.

## Contract and fixed sources

2026-10-25 Asia/Shanghai. Independent document main safely fast-forwarded frome27e175 to5a569dd0fba5067682ec4a55d886c3cca2eb1c6f; AGENTS/current board/overview/results/045 contract and referenced design reread. Exactly one unreported READY045 confirmed.041 source Git blob `bf763213b74a15db7dbb31bc29f7515be12cdb9b` and040 platform3e56faf30afea1bed850c085bceb2afcc4fb257c verified.041 was inspected only; no cache/oracle/suite/runtime recovery was imported or run. Only040 Job/Process platform reused, no old workload.043/044 public receipts confirm the fetch route remains stopped; no prior private root/partial/ledger/QA/helper was accessed.

Installed Qwen3 processor source exactly matches frozen Git blob17bdd975eef337371aa763824edc7e6ec1987dbf,17149B, SHA256efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9. Target/observed Transformers4.57.6. No remote source/asset retrieval or API chase. [Native implementation](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3_vl/processing_qwen3_vl.py) retains its upstream formatting/tokenization; no upstream implementation snippets or tokenizer assets redistributed.

## Adapter implementation and request isolation

native_pts_adapter_045.bind_processor constructs a fresh Qwen3VLProcessor subclass instance per P request using the base's existing tokenizer/image/video components, with no second from_pretrained load. It never changes the installed library, a global method, base class, base instance method or shared configuration. __call__ only validates the narrow contract, marks single use and forwards the original kwargs into the inherited native __call__. The scientific change is solely _calculate_timestamps: immutable96-source index→Fraction seconds, verify actual indices/fps/merge, then return float of exact first/last PTS mean for each pair. Native __call__ supplies its unchanged one-decimal timestamp string, visual placeholder expansion, tokenizer and BatchFeature.

Scope is one48-frame192×288 RGB video,96-source metadata, merge2, known source indices and declared fps; not a general multi-video/variable-merge/production concurrent adapter. P request instances cannot be reused; immutable maps are copied and protected. The input validator rejects missing/nonfinite/negative/nonincreasing PTS, missing/nonpositive/mismatched fps, unknown/reordered/float indices, missing metadata, multiple videos and wrong frames/merge. Missing fps is rejected before the native fps24 fallback. Original integer indices/fps are never forged, replaced by fake fractional indices or adjusted to fit time.

Serial A→B→new explicitA and P→native tests establish only this serial request isolation. No multithreaded safety certification. Actual native/adapter call arguments are profiled noninvasively, P also records its request map and raw output; the profiler is removed after each call. No input_ids/attention mask edits or hand-built video placeholders/timecode strings are fed into the processor. Decode/encode roundtrip and timecode removal occur only in verification, never fed back.

## Initial failure and single compatibility repair

The initial CPU library bootstrap failed importing torchvision.io.video: its optional `import av` catches ImportError, while the initial no-decoder guard raised PermissionError. No AutoProcessor.from_pretrained, processor call or real probe was reached; that failed worker exited1 and its own Job drained to active0. The initial CUDA is_initialized assertion had not yet been reached; visibility had already been masked. Initial traceback/receipts remain local, not rewritten as successful processor work.

Read the exact installed torchvision/io/video.py dependency from that traceback and Transformers/video_utils.py to verify decoder imports are optional/function-local. The sole compatibility change makes the audit guard raise ImportError before av/torchcodec can import. Decoder remains unavailable; no installed file, availability metadata, global module stub or environment was changed. Current worker actually records refused av imports and never invokes media loading. This is a guard/optional-import compatibility correction, not a changed stimulus or timestamp API/format.

Initial pure suite43 assertions PASS; after the fix, the second and final pure suite44 PASS, including an explicit unavailable decoder-import test. All initial failures/resources retained. Only one processor/tokenizer asset load occurred, in the surviving formal worker; the failed initial bootstrap loaded no processor assets. Probe1 P/CFR confirmed one actual callback with48 expected integer indices,fps integer1,merge2 and24 returned times. No second probe or further unused-budget experiment.

## Formal seal and nine actual slots

Before the surviving worker continued, source/validator SHA, base identity, all four96-entry fixtures, indices, prompt and nine-slot order were sealed. Probe data were discarded for scientific comparisons; every formal slot actually preprocessed again, once. Same worker and same already loaded base assets across probe/handshake/formal queue. No formal retry, post-output condition change or source repair.

Controlled inputs: F96,T96s,fps1;48 integer ties-to-even selections; RGB[j,y,x,c]=(17*indices_j+3*y+5*x+29*c) mod256. No font/time overlay, audio, real frames or decoder. Four tables CFR/A/B/Q share identical RGB/indices/fps/T. All end at96000ticks with1/1000 time base. Q's initial interval1010ticks and final990ticks leave every nonzero sourcePTS+10ticks; all data are owned numeric fixtures, outside natural180–900s media qualification.

| Slot | Path / table | Compared with | Full direct equal | Visual/grid direct equal | Native times PASS | Tokens / visual | Status |
|---|---|---|---|---|---|---|---|
|Q01|native / CFR|Q01|True|True|yes|1532 / 1296|PASS|
|Q02|P / CFR|Q01|True|True|yes|1532 / 1296|PASS|
|Q03|native / A|Q01|True|True|yes|1532 / 1296|PASS|
|Q04|P / A|Q03|False|True|yes|1530 / 1296|PASS|
|Q05|P / B|Q04|False|True|yes|1533 / 1296|PASS|
|Q06|native / A|Q03|True|True|yes|1532 / 1296|PASS|
|Q07|P / A|Q04|True|True|yes|1530 / 1296|PASS|
|Q08|native / Q|Q01|True|True|yes|1532 / 1296|PASS|
|Q09|P / Q|Q08|True|True|yes|1532 / 1296|PASS|

All nine actual grids[[24,12,18]],1296 visual tokens. Direct comparison checked key sets, CPU device, dtype, shape and torch.equal on final BF16 pixels/grid, not only hashes or nominal metadata. Full comparison checks every actual returned kwarg: attention_mask,input_ids,pixel_values_videos,video_grid_thw. Native integer tensors remain unchanged; only visual floats converted to CPU BF16. Common base processor/tokenizer/runtime identity belongs in full H; fixture label, map digest and adapter source are separately recorded and excluded, preventing manufactured inequality.

All base config identities before/after match, base class/native timestamp function remain the original, no instance timestamp override added to base. Q06==Q03 after adapters; Q07==Q04 after B but explicit newA. Native A/Q never received their external PTS tables and equal Q01. Exactly one timestamp callback in every formal slot; P returned times were independently checked against Fraction first/last means, all24 actual arguments/outputs retained in CSV.

## Actual timecodes and quantization

| Effective path |24 actual native timecodes /seconds|
|---|---|
|Q01|1.0, 5.0, 9.0, 13.0, 17.0, 21.0, 25.0, 29.0, 33.0, 37.0, 41.0, 45.0, 50.0, 54.0, 58.0, 62.0, 66.0, 70.0, 74.0, 78.0, 82.0, 86.0, 90.0, 94.0|
|Q04|0.5, 2.5, 4.5, 6.5, 8.5, 10.5, 12.5, 14.5, 16.5, 18.5, 20.5, 22.5, 27.0, 33.0, 39.0, 45.0, 51.0, 57.0, 63.0, 69.0, 75.0, 81.0, 87.0, 93.0|
|Q05|1.5, 7.5, 13.5, 19.5, 25.5, 31.5, 37.5, 43.5, 49.5, 55.5, 61.5, 67.5, 73.0, 75.0, 77.0, 79.0, 81.0, 83.0, 85.0, 87.0, 89.0, 91.0, 93.0, 95.0|
|Q09|1.0, 5.0, 9.0, 13.0, 17.0, 21.0, 25.0, 29.0, 33.0, 37.0, 41.0, 45.0, 50.0, 54.0, 58.0, 62.0, 66.0, 70.0, 74.0, 78.0, 82.0, 86.0, 90.0, 94.0|

Q09 raw P/Q minus Q08 native/Q is exactly1/200s at the first patch and1/100s at each of the other23 by independent rational oracle. Actual callback float deltas are retained separately from those exact fractions. All24 one-decimal differences are0; all tensors and full hash match, not only decoded time strings. Q quantization-equivalence is a measured outcome, not evidence of model insensitivity.

Nine physical preprocessing slots collapse to three complete-input classes: `[["Q01", "Q02", "Q03", "Q06", "Q08", "Q09"], ["Q04", "Q07"], ["Q05"]]`. This does not represent three or nine model observations: model calls0. Equal inputs cannot count as independent model evidence. Same1296 visual tokens also do not imply identical total text token count/computation: native/CFR-like1532, A-P1530, B-P1533.

Every decoded input roundtrips to exactly the original token IDs under the same tokenizer without special-token addition. Exactly24 known timecode fragments are replaced only for audit; all remaining text is identical. With all other nonvisual kwargs explicitly limited to input_ids/attention_mask and all attention entries1 of matching shape, the gate “only expected timecode text differs” is PASS, not TEXT_DIFFERENCE_UNKNOWN. Tokenizer/processor incompatibility would have retained UNKNOWN; no such bypass occurred.

[Complete9-row CSV](input-boundaries.csv) preserves actual arguments, map/PTS/indices identity, all24 raw/quantized times/errors, per-key dtype/shape/device/continuous-byte SHA, input IDs/attention, complete/visual/text hashes, roundtrip/strip-text hashes, direct relationships and all statuses. Raw RGB/visual tensor blocks and private config text/paths are never uploaded.

## Runtime, API reads and resources

Runtime versions: `{"numpy": "1.26.4", "torch": "2.5.1", "transformers": "4.57.6"}`; one loaded Qwen3VLProcessor, anonymous shared config identity `4d213e00387bb03c9e73dd248c96ba92161c8d940f50c95f0546ebf73d60ff6d`. No weight/model identity inferred. Observed current-worker CUDA is_initialized=False, threads4; CPU visibility mask and offline/local-only/trust_remote_code=False set before imports. No device enumeration/nvidia-smi/forward/generate/decoder.

Explicit installed-source inspection:3 unique exact files, 102520B total including repeated reads (processing_qwen3_vl.py3×17149B; torchvision/io/video.py17217B; transformers/video_utils.py33856B), below4files/4MiB. Normal installed-runtime and processor/tokenizer asset imports are a separate permitted role. No site-packages/media/cache directory scan or039/041 runtime/helper lookup.

| Exact source basename / role | Bytes per read | SHA256 |
|---|---:|---|
|processing_qwen3_vl.py / API target|17149|efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9|
|torchvision/io/video.py / optional import boundary|17217|a361c29dc0fe1b4de543820feb95e958490f0d2e4f19514122c0a67034953746|
|transformers/video_utils.py / function-local decoder calls|33856|3bc174f4cf68115ead399b49521dfc699b1bf6055e5afe9a4372fd98ed819dbe|

| Phase | Outer wall s | Exit | Job user / kernel s | Peak Job bytes | Active / killed |
|---|---:|---|---|---:|---|
|stdlib-suite-initial|0.181336400|0|0.062500 / 0.062500|14860288|0 / False|
|initial-library-bootstrap|29.365995900|1|2.703125 / 3.093750|762437632|0 / False|
|stdlib-suite-after-fix|0.166955500|0|0.109375 / 0.031250|14868480|0 / False|
|current-single-processor-worker|80.330496300|0|6.828125 / 5.125000|1388044288|0 / False|

Total supervised wall **110.044784100/600s**, including the failed bootstrap and bounded parent/worker seal-handshake wait; each current worker≤300s and pure suite≤60s. Parent elapsed at receipt1425.507/3600s. Per-slot processor wall in CSV excludes signature/export/tokenizer-audit work; outer Job wall/CPU includes it. No GPU speed/compute claim. Processor reservations/executed calls10/12 = probe1 +formal9, no failed processor calls in the library-import bootstrap, no more than one probe used.

Every child created suspended then assigned a fresh nonbreakaway4GiB Job; all actual groups active0 naturally, no termination or peer cleanup. Actual peak current Job1388044288B<4GiB; failed bootstrap peak762437632B retained. CPU threads≤4, no old lock or shared GPU process touched.

New-root resident snapshot 29 files/952918B≤1024/64MiB. Before first output free348748251136B exceeded64MiB+2GiB=2214592512. Bounded receipts/one9-slot sequence, no on-disk RGB/full tensor/weight blocks. Snapshot is not a Windows volume quota or cumulative-write peak certificate.

Process-local audit denies network/child processes, weight/media body reads and writes outside the new root. TEMP/HF cache routes are temporary child-only; permanent environment/ACL/profile changes0. Pure suites' socket/DNS negative probes were refused (4 attempts, not real sockets); empty owned weight-denial canaries demonstrate refused reads, not actual weight access. Decoder import attempts were refused as shown in source-located failure/guard receipts; no decoder body/function or media opened.

## What this closes and what remains HOLD

This closes one narrow implementation uncertainty: the exact PTS table reaches the real native timestamp callback, then native text/tokenizer/BF16 boundary as intended, without changing pictures or polluting base/request state. It also measures the format's controlled quantization-equivalence. It is neither a new temporal algorithm nor evidence that P improves answers or that a natural source has nonuniform PTS.

Still absent:8 independent lawful complete natural assets, actual display/origin/edit certification, label-to-media clock bridge, repeated-action question identifiability/valid-answer sets, strong N baseline, actual task data/model input qualification and any effect/score experiment. The T96s fixture is not a natural180–900s source.64-slot admission remains HOLD; all media/label/model/GPU gates remain unapproved.

044 direct official fetch remains paused,042–044 attempts/partial/liabilities remain closed and untouched. No downloads or path search, fake-transmission task, literature/graphic-clock variant, automatic046, GPU, Issue/PR/submission or training is activated. NOVELTY=RETAIN0; NATURAL_MEDIA_AND_TASK_EFFECT_UNKNOWN. Only five allowlisted artifacts/one append, one ordinary safe push then STOP.

## Final sealed source and fixture identity

```json
{
  "base_identity": "4d213e00387bb03c9e73dd248c96ba92161c8d940f50c95f0546ebf73d60ff6d",
  "fixture_hashes": {
    "A": "5074e29e2a436284111ecf6e113f2b3d7232d75e3a40d9b367a19c91315a05c9",
    "B": "be57753154be4e0d080fc8d480cbc4e4b43bcf3086d7f489515812d1d87211fc",
    "CFR": "c3cba7d08dcf35aff3f7b484656666313b842e0476eb92998985b63332e751b0",
    "Q": "0525d80dd059c4d2d374087d512b99c250156ece5af1ea27ed53dc28906d719b"
  },
  "indices": [
    0,
    2,
    4,
    6,
    8,
    10,
    12,
    14,
    16,
    18,
    20,
    22,
    24,
    26,
    28,
    30,
    32,
    34,
    36,
    38,
    40,
    42,
    44,
    46,
    49,
    51,
    53,
    55,
    57,
    59,
    61,
    63,
    65,
    67,
    69,
    71,
    73,
    75,
    77,
    79,
    81,
    83,
    85,
    87,
    89,
    91,
    93,
    95
  ],
  "prompt": {
    "question": "Describe the video.",
    "system": "You are a helpful assistant."
  },
  "slots": [
    [
      "Q01",
      "native",
      "CFR"
    ],
    [
      "Q02",
      "P",
      "CFR"
    ],
    [
      "Q03",
      "native",
      "A"
    ],
    [
      "Q04",
      "P",
      "A"
    ],
    [
      "Q05",
      "P",
      "B"
    ],
    [
      "Q06",
      "native",
      "A"
    ],
    [
      "Q07",
      "P",
      "A"
    ],
    [
      "Q08",
      "native",
      "Q"
    ],
    [
      "Q09",
      "P",
      "Q"
    ]
  ],
  "source_sha256": "605b6299ce397a90d51509a0debf2a113dd5269890ff47f5e0813ece8fef7f94",
  "test_sha256": "e65909a05c38c0d48bb88e25f715a219cccd56ea4ad1aa0de4cc083fee109efd"
}
```
