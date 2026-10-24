# 041 reproducibility and value decision

**CPU_BOUNDARY_CONTRACT_REPRODUCED; LOCAL_COMPONENT_REGRESSION_ONLY; NOVELTY=RETAIN0.** Simple existing source/configuration namespace eliminated every observed incompatible reuse. This supports a bounded regression test and explicit data-version contract, not a distinct hashing mechanism or an engineering-paper breakthrough. No next experiment, GPU, upstream Issue, submission or042 is activated.

## Fixed component and actual interface

Base document main `6298e2d831c79196a74161516537610b90d41421`; unique unreported READY041 verified before work. Fixed [lmms-eval source](https://github.com/EvolvingLMMs-Lab/lmms-eval/tree/8f40097532a7bf4db6123713f1a905e02c8f5971), complete upstream LICENSE preserved. Only these fixture files were imported with namespace packages; ResponseCache/Instance/key/SQLite functions unchanged. The checkout uses CRLF: original Git blob bytes were exported locally and SHA-verified, rather than claiming the working-tree hashes matched. All four differences were line endings only. No download or upstream source edit.

| Exact fixture | Bytes | SHA256 |
|---|---:|---|
|LICENSE|2732|17358b5caadacb8108f14a6a319779cc8a20feed699f79c59e396e7e9dd5c33b|
|lmms_eval/api/instance.py|3547|3cc570e20796c216d192693362030d5311c6e9054d2be5f1801d789fb197854b|
|lmms_eval/caching/fs_detect.py|6895|46699b07f67f92a728ff803b4c917bcab7a1400f795dd75e5607159db49507f9|
|lmms_eval/caching/response_cache.py|51162|7a0c51ae559213a32e33b1495554da84b92169c9ecb59855f3011321892cd7e1|

The actual installed environment lacked loguru, so the expressly permitted stdlib logging logger adapter was used in suite/formal/clean. It adapts logging only. Actual ResponseCache constructor/execute/get_stats/close and actual Instance were used, not create(), full package initialization, OmniCompass download/finalize or model identity scanning.

Instance arguments are raw question, frozen generation dict, callback, doc_id, task and split. `execute` derives its existing prefix-text identity before the callback; a hit skips backend, callback and processor. The owned backend calls the actual request callback and returns only INPUT_SHA256 plus the actual CPU boundary hash. SOURCE/EFFECTIVE explicitly change task_fingerprints between requests by closing/reopening the same DB; UPSTREAM has the identical lifecycle but fixed fingerprint. This intervention is not a claim that default CLI automatically updates those identities.

## Actual processor and source receipt

Versions: `{"numpy": "1.26.4", "torch": "2.5.1", "transformers": "4.57.6"}`. Declared model ID Qwen3-VL-4B; anonymous processor/tokenizer/configuration identity `6910dd184a9c5b249401db7051030b4d54c550b04d298fdbe003e7e8a52ed9bb`. This is not a weight identity. Processor loaded once per new suite/formal/clean process, three loads total, zero model loads. No039 config was needed because the exact processor directory was already supplied in the current conversation.

| Installed API source (basename only) | Bytes | SHA256 |
|---|---:|---|
|processing_qwen3_vl.py|17149|efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9|
|video_processing_qwen3_vl.py|11561|a49a83fc45cd9baa3e391a68af79743c70d47b86d7d6c81a262fda4104f89db7|
|image_processing_qwen2_vl_fast.py|12723|09bfa9b17df7c3f0c6159bc34008ee50f21d2472cd5bae7e5c21ba1ca13a423c|
|video_utils.py|33856|3bc174f4cf68115ead399b49521dfc699b1bf6055e5afe9a4372fd98ed819dbe|

Four unique exact source files, 75289 bytes per phase, 225867 bytes across three explicit source receipts, below4MiB. Normal local module/processor/tokenizer assets are a separate authorized role. No source compatibility repair was necessary.

## Seal and clean reproduction

Formal source/fixture/stimulus formula/generation/queue seals preceded the sole formal worker; post-run source and queue hashes matched. The72 oracle states are freshly actual-processed before any formal cache queries. One formal processor load, no restarts or selected reruns. Queue rotation and both AB/BA orders retained. Complete report and CSV retain full planned denominators.

Source SHA256:

```json
{
  "docs/research-protocols/cache-input-qualification-2026-10-24.md": "ed5de82ebf2bfc30ea627d08c212848731994f42d412d724da5528b112c60ddd",
  "prototypes/auditable_runner_040.py": "a82810e4a5909aa1978f15ede6222be6616ae0b651a55c4b4431d17be2f48381",
  "prototypes/cache_input_contract_041.py": "90b184416b1de1b000a60886d89a01af71665cdc22fd45136b5c6188454fef1e",
  "prototypes/test_cache_input_contract_041.py": "ddb60dc75f7b2697534547b338d24d9619ef5197e5561e892ccf17ef461111a5"
}
```

Clean root copied only the two041 modules, unchanged public040 platform module, four exact fixture files including LICENSE, and new local locator/queue config. No old private code, output, original annotation or media needed. Fixed EXACT_VIDEO and VIDEO_FPS, s0, AB, four profiles:8 sequences/16 queries, 13 actual processor calls; every status, marker, decision and per-query processor count matched the formal subset. Its configuration identity matched too. It reuses the new formal oracle receipt for comparison, not free prepared inputs; no independent oracle72 is claimed. Same Windows/Python/runtime/processor machine, not independent-machine replication.

Reproduction template (substitute authorized new roots/runtime/processor locators; never model weights):

```powershell
python -I -S -B cache_input_contract_041.py supervise NEW_ROOT NEW_CONFIG suite 60
python -I -S -B cache_input_contract_041.py supervise NEW_ROOT NEW_CONFIG formal 600
python -I -S -B cache_input_contract_041.py export NEW_ROOT exported.csv
python -I -S -B cache_input_contract_041.py recompute exported.csv
# Clean: copied modules + platform + fixture/LICENSE; its config references the new formal oracle
python -I -S -B cache_input_contract_041.py supervise CLEAN_ROOT CLEAN_CONFIG clean 90
```

The parent must create new roots/config/queue and seal source before formal, ensure initial free space and limits, and never rerun an already started formal root. The CLI is not a hardened admission service: it uses exclusive receipt files and bounded Job execution, while operational one-use authorization is enforced by this single execution rather than a tamper-proof cross-host lock. The new owned local locators stay private. No claim of adversarial containment/exactly-once. Independent CSV export/recompute needs only stdlib and the published module/data, no processor.

## Prior coverage and scientific interpretation

These comparisons use the owner's frozen [prior-art review](../../research-proposals/cache-input-contract-qualification-2026-10-24.md), not new online verification or execution of those systems. [Issue1244](https://github.com/EvolvingLMMs-Lab/lmms-eval/issues/1244) covers Qwen timestamp metadata forwarding;041 forwards metadata correctly and does not reproduce an artificial omission. [Issue1255](https://github.com/EvolvingLMMs-Lab/lmms-eval/issues/1255) covers code-version identity; the fixed component has evaluation-version/model/task identity and pre-question text hashing. Neither is absent in this test.

OmniCompass has nearby selection/sampling/runtime/local-model identity controls; it was not run and complete fingerprints are not novel here. vLLM's documented multimodal content hash is likewise existing coverage. The inference that a response-layer hit skips any lower backend hashing follows this measured callback order; it is not a vLLM test, vulnerability or speed result.

Under an immutable task/doc_id/data contract, keeping a static fingerprint is reasonable: changing synthetic content while intentionally preserving identity violates that premise. A plausible risk would be a legitimate preprocessing/timing/data revision without a corresponding namespace revision. This round proves the conditional interface behavior, not that such an unversioned revision occurs in a real supported workflow, nor its natural incidence. That workflow evidence remains absent.

SOURCE_NAMESPACE fully handled all observed changes at the existing API, paying raw hash costs and16 conservative equal-input misses. EFFECTIVE_INPUT canonicalizes equivalent actual inputs but pays processor on every query; no GPU savings may be inferred from marker-backend calls. NO_CACHE removes reuse at the cost of all preprocessing and all reuse opportunities; refusal/recomputation alone is not superiority. Four synthetic stimuli are not independent natural videos; no significance, accuracy, latency generalization or new algorithm claim.

**Decision:** retain the regression/contract evidence; stop this line as a standalone novelty claim. Continue only under a separately approved contract with independently documented legitimate workflow relevance and a question beyond existing namespace/full-input hashes. Prior040 NO_DISTINCT_MECHANISM_EVIDENCE and old scientific/media/training restrictions are unchanged. STOP after one ordinary safe push.
