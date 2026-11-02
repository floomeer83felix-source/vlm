"""079 cached model-identity check, without re-reading weight payloads.

The 076 catalog binds completed hashes and file size/mtime observations.
078 registration was interrupted with unknown hash read counts. A continuation
may reuse that catalog only if its graph and every registered stat still match.
This is cached-hash/stat continuity, not a new cryptographic content verification.
No import-time file/model/network access; no Torch or processor import.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _require(condition, reason):
    if not condition:
        raise ValueError(reason)


def _relative_name(name):
    _require(isinstance(name, str) and name and "\\" not in name and ":" not in name,
             "UNSAFE_CATALOG_NAME")
    p = PurePosixPath(name)
    _require(not p.is_absolute() and all(v not in ("", ".", "..")
                                        for v in name.split("/")), "UNSAFE_CATALOG_NAME")
    return p


def validate_cached_model(catalog, installed_directory, *, read_source=None, progress=None):
    """Validate sealed catalog graph/stats and small installed source files.

    The caller authenticates the 076 catalog file against its closed asset seal.
    read_source, when supplied, reserves and records source bytes durably before
    reading them. progress is for durable stage/PID logging by the caller. It must
    never expose private paths in public reports. Neither callback reads weights.
    """
    notify = progress if progress is not None else lambda **_: None
    notify(stage="CACHED_CATALOG_BEGIN")
    graph = catalog["graph"]
    _require(hashlib.sha256(canonical(graph)).hexdigest() == catalog["graph_sha256"],
             "CACHED_GRAPH_HASH_MISMATCH")
    hashes = graph["model_files"]
    stats = catalog["model_file_stats"]
    _require(isinstance(hashes, dict) and hashes and set(hashes) == set(stats),
             "CACHED_MODEL_FILE_SET_MISMATCH")
    root = Path(catalog["model_root"])
    total = 0
    for index, name in enumerate(sorted(hashes)):
        p = root.joinpath(*_relative_name(name).parts)
        _require(isinstance(hashes[name], str) and len(hashes[name]) == 64,
                 "CACHED_MODEL_HASH_SCHEMA")
        int(hashes[name], 16)
        st = p.stat()
        expected = stats[name]
        _require(p.is_file() and st.st_size == expected["size"]
                 and st.st_mtime_ns == expected["mtime_ns"], "CACHED_MODEL_STAT_CHANGED")
        total += st.st_size
        notify(stage="CACHED_MODEL_STAT", index=index + 1, registered_bytes=total)
    _require(total == catalog["model_hash_bytes"] == 8887284080,
             "CACHED_MODEL_REGISTERED_SIZE_MISMATCH")
    installed = {}
    source_bytes = 0
    for name, expected in sorted(graph["installed_sources"].items()):
        p = Path(installed_directory).joinpath(*_relative_name(name).parts)
        body = read_source(p) if read_source is not None else p.read_bytes()
        _require(hashlib.sha256(body).hexdigest() == expected, "INSTALLED_SOURCE_CHANGED")
        installed[name] = expected
        source_bytes += len(body)
    notify(stage="CACHED_CATALOG_VALIDATED", files=len(hashes), source_bytes=source_bytes)
    return {
        "status": "CACHED_076_HASH_PLUS_UNCHANGED_STATS",
        "registered_model_bytes": total,
        "model_files_stat_checked": len(hashes),
        "new_weight_hash_read_bytes": 0,
        "new_full_weight_hash": False,
        "installed_source_bytes": source_bytes,
        "installed_sources": installed,
        "limitation": "cached content hashes with current size/mtime continuity; not fresh content hashing",
    }
