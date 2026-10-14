"""One bounded Commons metadata request + one public-domain 360p transcoded WebM GET.

For a private task directory only. No retries, proxies, HTTP redirects, AWS or
protected video access. One-shot ledger is deliberately never reset.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import ssl
import sys
import time
from urllib.parse import urlencode, urlsplit
from urllib.request import build_opener, HTTPSHandler, HTTPRedirectHandler, ProxyHandler, Request

PAGE = "File:One Week (1920).webm"
KEY = "360p.vp9.webm"
API = "https://commons.wikimedia.org/w/api.php"
MAX_META = 512 * 1024
MAX_VIDEO = 96 * 1024 * 1024
MAX_SECONDS = 600


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def clean_url(url, host):
    z = urlsplit(url)
    if z.scheme != "https" or z.hostname != host or z.username or z.password or z.query or z.fragment or z.port:
        raise ValueError("unexpected_video_source")
    if not z.path.startswith("/wikipedia/commons/") or not z.path.endswith(".webm"):
        raise ValueError("unexpected_media_path")


def journal(fp, data):
    fp.write(json.dumps(data, sort_keys=True) + "\n")
    fp.flush()
    os.fsync(fp.fileno())


def run(directory):
    root = Path(directory)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("new_private_task_dir_required")
    video = root / "one-week-360p.webm"
    part = root / "one-week-360p.webm.part"
    led = root / "one-shot-attempts.jsonl"
    if any(p.exists() or p.is_symlink() for p in (video, part, led)):
        raise FileExistsError("already_started_or_existing_output")
    opener = build_opener(HTTPSHandler(context=ssl.create_default_context()),
                          ProxyHandler({}), NoRedirect())
    query = urlencode({"action": "query", "format": "json", "formatversion": "2",
                       "prop": "videoinfo", "viprop": "derivatives|extmetadata|size|url",
                       "titles": PAGE})
    with led.open("x", encoding="utf-8") as fp:
        journal(fp, {"state": "STARTED", "meta_attempts_max": 1, "media_attempts_max": 1,
                     "media_body_cap": MAX_VIDEO})
        t0 = time.monotonic()
        journal(fp, {"stage": "META_GET_ATTEMPT", "count": 1})
        req = Request(API + "?" + query, headers={
            "Accept-Encoding": "identity",
            "User-Agent": "VLM-Open-LongVideo-Pilot/1.0 (https://github.com/floomeer83felix-source/vlm)"})
        with opener.open(req, timeout=45) as res:
            if res.status != 200 or urlsplit(res.geturl()).hostname != "commons.wikimedia.org":
                raise ValueError("metadata_status_or_redirect")
            raw = res.read(MAX_META + 1)
            if len(raw) > MAX_META:
                raise ValueError("metadata_size_limit")
        doc = json.loads(raw.decode("utf-8"))
        pages = doc.get("query", {}).get("pages", [])
        if len(pages) != 1 or pages[0].get("title") != PAGE:
            raise ValueError("metadata_identity")
        info = pages[0].get("videoinfo", [])
        if len(info) != 1:
            raise ValueError("video_metadata_missing")
        info = info[0]
        license_raw = json.dumps(info.get("extmetadata", {}), ensure_ascii=False).lower()
        if "public domain" not in license_raw and "pd-us" not in license_raw:
            raise ValueError("license_not_proven")
        derivatives = [x for x in info.get("derivatives", [])
                       if x.get("transcodekey") == KEY]
        if len(derivatives) != 1:
            raise ValueError("360p_transcode_not_unique")
        url = derivatives[0].get("src")
        if not isinstance(url, str):
            raise ValueError("no_transcode_url")
        clean_url(url, "upload.wikimedia.org")
        journal(fp, {"stage": "MEDIA_GET_ATTEMPT", "count": 1,
                     "selected_variant": KEY})
        with part.open("xb") as sink:
            req = Request(url, headers={"Accept-Encoding": "identity",
                       "User-Agent": "VLM-Open-LongVideo-Pilot/1.0 (https://github.com/floomeer83felix-source/vlm)"})
            with opener.open(req, timeout=45) as res:
                if res.status != 200 or res.geturl() != url:
                    raise ValueError("media_status_or_redirect")
                if res.headers.get("Content-Encoding", "identity").lower() != "identity":
                    raise ValueError("unexpected_content_encoding")
                length = int(res.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_VIDEO:
                    raise ValueError("content_length_out_of_bounds")
                if not "video" in res.headers.get("Content-Type", "video/webm").lower() and not res.headers.get("Content-Type", "").startswith("application/octet-stream"):
                    raise ValueError("content_type_unexpected")
                sha = hashlib.sha256()
                count = 0
                while count < length:
                    if time.monotonic() - t0 > MAX_SECONDS:
                        raise TimeoutError("bounded_wall_time")
                    chunk = res.read(min(256 * 1024, length - count))
                    if not chunk:
                        raise ValueError("truncated_media")
                    count += len(chunk)
                    sha.update(chunk)
                    sink.write(chunk)
                    if count % (8 * 1024 * 1024) < len(chunk):
                        sink.flush()
                        os.fsync(sink.fileno())
                sink.flush()
                os.fsync(sink.fileno())
        if part.stat().st_size != length:
            raise ValueError("final_length_mismatch")
        with part.open("rb") as rd:
            prefix = rd.read(4)
            if prefix != b"\x1a\x45\xdf\xa3":
                raise ValueError("not_ebml_webm")
        os.replace(part, video)
        journal(fp, {"stage": "COMPLETE", "body_bytes": count})
        print(json.dumps({"status": "PUBLIC_DOMAIN_LONG_VIDEO_READY",
                          "bytes": count, "sha256": sha.hexdigest(),
                          "variant": KEY}, sort_keys=True))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--private-dir", type=Path, required=True)
    args = p.parse_args()
    try:
        run(args.private_dir)
    except Exception as ex:
        print(json.dumps({"status": "HOLD", "reason": type(ex).__name__}))
        sys.exit(2)
