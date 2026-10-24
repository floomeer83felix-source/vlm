# Fixed lmms-eval response-cache component fixture

Upstream: [EvolvingLMMs-Lab/lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval/tree/8f40097532a7bf4db6123713f1a905e02c8f5971).
Pinned commit: `8f40097532a7bf4db6123713f1a905e02c8f5971` (2026-10-22).
Retrieved 2026-10-24 for [041 qualification](../../docs/codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/README.md).

The following files retain their original contents and paths beneath this directory.
The upstream LICENSE is included verbatim. The copied pipeline modules are covered
by the upstream main-pipeline MIT terms; the full license file also describes upstream
model/task licensing. No model/task implementations or data are vendored.

| Path | UTF-8 bytes | SHA256 |
|---|---:|---|
| LICENSE | 2732 | 17358b5caadacb8108f14a6a319779cc8a20feed699f79c59e396e7e9dd5c33b |
| lmms_eval/api/instance.py | 3547 | 3cc570e20796c216d192693362030d5311c6e9054d2be5f1801d789fb197854b |
| lmms_eval/caching/fs_detect.py | 6895 | 46699b07f67f92a728ff803b4c917bcab7a1400f795dd75e5607159db49507f9 |
| lmms_eval/caching/response_cache.py | 51162 | 7a0c51ae559213a32e33b1495554da84b92169c9ecb59855f3011321892cd7e1 |

This is a source fixture, not an installed full lmms-eval distribution. The 041
harness may load these exact modules in an isolated child namespace, avoiding
the full package initializer. If loguru is absent, only the logging interface
may be adapted to stdlib logging; Instance, cache-key helpers, execute, SQLite
and response validation must remain unchanged. Report that adaptation.

Use ResponseCache's constructor/execute/close for component experiments.
Do not call create(), download datasets, invoke OmniCompass model hashing or
claim this fixture executes the official CLI/Qwen model adapter. Filesystem
helpers are retained as original dependencies; no unrestricted storage search
is authorized by their presence.

Model/processor dependencies are supplied only by the user's existing local
CPU environment under the separate 041 contract. The fixture does not include
weights, tokenizers, datasets, credentials or user-specific configuration.
