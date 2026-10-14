"""Bounded one-shot fetch of the public MDN flower example. No retries/redirects.

Run only in a new private task-owned directory; NOT in public Git checkout.
"""
import argparse
import hashlib
import json
import os
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

URL = "https://mdn.github.io/shared-assets/videos/flower.mp4"
MAX_BODY = 8 * 1024 * 1024


class RefuseRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(target, ledger):
    target = target.resolve(strict=False)
    ledger = ledger.resolve(strict=False)
    if target == ledger or target.parent != ledger.parent or target.suffix.lower() != ".mp4":
        raise ValueError("invalid_output")
    if not target.parent.is_dir() or target.exists() or ledger.exists():
        raise FileExistsError("output_or_ledger_exists")
    part = target.with_suffix(".mp4.part")
    if part.exists():
        raise FileExistsError("part_exists")
    # One unrefundable request attempt. Ledger is deliberately retained on error.
    with ledger.open("x", encoding="utf-8") as lf:
        lf.write('{"state":"STARTED","method":"GET","max_body_bytes":8388608}\n')
        lf.flush()
        os.fsync(lf.fileno())
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        urllib.request.ProxyHandler({}),
        RefuseRedirects(),
    )
    req = urllib.request.Request(
        URL,
        method="GET",
        headers={"Accept-Encoding": "identity", "User-Agent": "VLM-bounded-CC0-pilot"},
    )
    count = 0
    digest = hashlib.sha256()
    with part.open("xb") as sink:
        with opener.open(req, timeout=30) as res:
            if res.status != 200 or res.geturl() != URL:
                raise ValueError("wrong_http_status_or_url")
            if res.headers.get("Content-Encoding", "identity").lower() != "identity":
                raise ValueError("encoded_body")
            declared_text = res.headers.get("Content-Length")
            declared = int(declared_text) if declared_text is not None else None
            if declared is not None and not (0 < declared <= MAX_BODY):
                raise ValueError("declared_body_out_of_bounds")
            while True:
                chunk = res.read(min(65536, MAX_BODY - count + 1))
                if not chunk:
                    break
                count += len(chunk)
                if count > MAX_BODY:
                    raise ValueError("body_cap_exceeded")
                digest.update(chunk)
                sink.write(chunk)
            if count <= 0 or (declared is not None and count != declared):
                raise ValueError("body_length_mismatch")
        sink.flush()
        os.fsync(sink.fileno())
    with part.open("rb") as f:
        if b"ftyp" not in f.read(16):
            raise ValueError("not_mp4_header")
    os.replace(part, target)
    # No secrets: public fixture URL, public hash, and small file size.
    return {"status": "MDN_CC0_MP4_COMPLETE", "body_bytes": count, "sha256": digest.hexdigest()}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True, type=pathlib.Path)
    p.add_argument("--ledger", required=True, type=pathlib.Path)
    a = p.parse_args()
    try:
        print(json.dumps(fetch(a.output, a.ledger), sort_keys=True))
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "reason": type(exc).__name__}))
        sys.exit(2)
