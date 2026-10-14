"""One-shot public-domain Commons long-film acquisition with reason-coded holds.

Runs only from an empty private parent-task directory. Exactly one MediaWiki
metadata GET and (only if license/source gates pass) one derivative GET.
Application media body <= 96 MiB, metadata body <= 512 KiB. No retry/redirect.
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
from urllib.request import (build_opener, HTTPSHandler, HTTPRedirectHandler,
                            ProxyHandler, Request)

TITLE = "File:One Week (1920).webm"
ALLOWED_KEYS = ("360p.vp9.webm", "240p.vp9.webm")
API_HOST = "commons.wikimedia.org"
VIDEO_HOST = "upload.wikimedia.org"
MAX_META = 512 * 1024
MAX_VIDEO = 96 * 1024 * 1024
MAX_ELAPSED = 600


class GateError(ValueError):
    def __init__(self, stage):
        self.stage = stage
        super().__init__(stage)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def require(ok, stage):
    if not ok:
        raise GateError(stage)


def read_metadata(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise GateError("META_JSON_PARSE") from None
    require(isinstance(doc, dict), "META_SCHEMA_ROOT")
    require(not doc.get("error"), "META_API_ERROR")
    require(not doc.get("warnings"), "META_API_WARNINGS")
    pages = doc.get("query", {}).get("pages") if isinstance(doc.get("query"), dict) else None
    require(isinstance(pages, list) and len(pages) == 1, "META_PAGES_SHAPE")
    page = pages[0]
    require(isinstance(page, dict) and page.get("title") == TITLE and not page.get("missing"),
            "META_PAGE_IDENTITY")
    info = page.get("videoinfo")
    require(isinstance(info, list) and len(info) == 1 and isinstance(info[0], dict),
            "META_VIDEOINFO_SHAPE")
    return info[0]


def verified_license(info):
    ext = info.get("extmetadata")
    require(isinstance(ext, dict), "LICENSE_EXTMETADATA_ABSENT")
    safe_fields = ("LicenseShortName", "License", "Copyrighted", "UsageTerms", "LicenseUrl")
    labels = {}
    for name in safe_fields:
        field = ext.get(name)
        if isinstance(field, dict):
            v = field.get("value")
            if isinstance(v, str):
                labels[name] = v.strip().lower()
    license_names = " ".join(labels.get(k, "") for k in ("LicenseShortName", "License"))
    require("public domain" in license_names or "pd-us" in license_names,
            "LICENSE_NOT_CONFIRMED_BY_STRUCTURED_FIELDS")
    copyrighted = labels.get("Copyrighted", "")
    require(copyrighted not in ("true", "yes", "1"), "LICENSE_COPYRIGHT_FLAG")
    return "US_PUBLIC_DOMAIN_DECLARED"


def verified_derivative(info):
    """Prefer 360p, then 240p; only exact real API options."""
    entries = info.get("derivatives")
    require(isinstance(entries, list), "DERIVATIVES_LIST_ABSENT")
    keys_present = tuple(x.get("transcodekey") for x in entries if isinstance(x, dict))
    for key in ALLOWED_KEYS:
        matches = [x for x in entries if isinstance(x, dict) and x.get("transcodekey") == key]
        require(len(matches) <= 1, "DERIVATIVE_DUPLICATE_KEY")
        if not matches:
            continue
        uri = matches[0].get("src")
        require(isinstance(uri, str), "DERIVATIVE_URL_MISSING")
        parts = urlsplit(uri)
        require(parts.scheme == "https" and parts.hostname == VIDEO_HOST and
                parts.port is None and not parts.username and not parts.password and
                not parts.query and not parts.fragment and
                parts.path.startswith("/wikipedia/commons/transcoded/") and
                parts.path.endswith("." + key), "DERIVATIVE_URL_NOT_OFFICIAL")
        return uri, key
    # No raw key names or metadata body logged, only this durable error category.
    raise GateError("DERIVATIVE_ALLOWED_KEYS_NOT_LISTED")


def _mock(ext, derivatives, title=TITLE):
    return json.dumps({"query": {"pages": [{
        "title": title, "videoinfo": [{"extmetadata": ext, "derivatives": derivatives}]
    }]}}, ensure_ascii=False).encode("utf-8")


def selftest():
    license_fields = {"LicenseShortName": {"value": "Public domain"},
                      "Copyrighted": {"value": "False"}}
    def derivative(key, urlhost=VIDEO_HOST):
        return {"transcodekey": key,
                "src": ("https://" + urlhost + "/wikipedia/commons/transcoded/a/ab/video.webm/video.webm." + key)}
    for key in ALLOWED_KEYS:
        info = read_metadata(_mock(license_fields, [derivative(key)]))
        require(verified_license(info) == "US_PUBLIC_DOMAIN_DECLARED",
                "SELFTEST_LICENSE_PASS")
        require(verified_derivative(info)[1] == key, "SELFTEST_KEY_" + key)
    info = read_metadata(_mock(license_fields, [derivative("240p.vp9.webm"),
                                              derivative("360p.vp9.webm")]))
    require(verified_derivative(info)[1] == "360p.vp9.webm", "SELFTEST_PRIORITY")
    cases = [
        (_mock({}, [derivative("240p.vp9.webm")]), "LICENSE_NOT_CONFIRMED_BY_STRUCTURED_FIELDS"),
        (_mock(license_fields, []), "DERIVATIVE_ALLOWED_KEYS_NOT_LISTED"),
        (_mock(license_fields, [derivative("240p.vp9.webm"),
                                derivative("240p.vp9.webm")]), "DERIVATIVE_DUPLICATE_KEY"),
        (_mock(license_fields, [derivative("240p.vp9.webm", "evil.example")]),
         "DERIVATIVE_URL_NOT_OFFICIAL"),
        (_mock(license_fields, [derivative("360p.mp4")]), "DERIVATIVE_ALLOWED_KEYS_NOT_LISTED"),
        (_mock(license_fields, [derivative("240p.vp9.webm")],
               title="File:Other.webm"), "META_PAGE_IDENTITY"),
    ]
    for raw, expected in cases:
        try:
            inf = read_metadata(raw)
            verified_license(inf)
            verified_derivative(inf)
        except GateError as exc:
            require(exc.stage == expected, "SELFTEST_REJECTION_MISMATCH")
        else:
            raise GateError("SELFTEST_FALSE_ACCEPT")
    return True


def journal(fp, **record):
    fp.write(json.dumps(record, sort_keys=True) + "\n")
    fp.flush()
    os.fsync(fp.fileno())


def open_once(opener, url, user_agent, label):
    request = Request(url, headers={"Accept-Encoding": "identity", "User-Agent": user_agent},
                      method="GET")
    response = opener.open(request, timeout=40)
    require(response.status == 200 and response.geturl() == url,
            label + "_HTTP_OR_REDIRECT")
    require(response.headers.get("Content-Encoding", "identity").lower() == "identity",
            label + "_ENCODING")
    return response


def run(root):
    require(selftest(), "OFFLINE_FIXTURE_FAILED")
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "PRIVATE_DIR_REQUIRED")
    video = root / "one-week-selected-vp9.webm"
    part = root / "one-week-selected-vp9.webm.part"
    ledger = root / "commons-v007-ledger.jsonl"
    require(not any(p.exists() or p.is_symlink() for p in [video, part, ledger]),
            "NEW_PARENT_OUTPUT_NOT_EMPTY")
    opener = build_opener(HTTPSHandler(context=ssl.create_default_context()),
                          ProxyHandler({}), NoRedirect())
    query = urlencode({"action": "query", "format": "json", "formatversion": 2,
                       "prop": "videoinfo", "viprop": "derivatives|extmetadata|size|url",
                       "titles": TITLE})
    api_url = "https://" + API_HOST + "/w/api.php?" + query
    started = time.monotonic()
    with ledger.open("x", encoding="utf-8") as jf:
        journal(jf, stage="STARTED", meta_get_limit=1, media_get_limit=1,
                meta_body_cap=MAX_META, media_body_cap=MAX_VIDEO)
        journal(jf, stage="META_GET_ATTEMPT", attempts=1)
        with open_once(opener, api_url, "VLM-PublicLongVideo/007", "META") as reply:
            declared = reply.headers.get("Content-Length")
            if declared is not None:
                require(0 < int(declared) <= MAX_META, "META_DECLARED_LENGTH")
            raw = reply.read(MAX_META)
            require(0 < len(raw) < MAX_META, "META_BODY_LIMIT_OR_UNVERIFIED_EOF")
            if declared is not None:
                require(len(raw) == int(declared), "META_BODY_TRUNCATED")
        journal(jf, stage="META_BODY_COMPLETE", bytes=len(raw))
        info = read_metadata(raw)
        journal(jf, stage="META_SCHEMA_PASS")
        status = verified_license(info)
        journal(jf, stage="LICENSE_PASS", jurisdiction="US")
        uri, selected = verified_derivative(info)
        journal(jf, stage="CANONICAL_DERIVATIVE_PASS", variant=selected)
        require(time.monotonic() - started <= MAX_ELAPSED, "PREMEDIA_TIME_EXCEEDED")
        journal(jf, stage="MEDIA_GET_ATTEMPT", attempts=1)
        count = 0
        digest = hashlib.sha256()
        with part.open("xb") as sink:
            with open_once(opener, uri, "VLM-PublicLongVideo/006", "MEDIA") as reply:
                require(reply.headers.get("Content-Type", "").lower().startswith("video/") or
                        reply.headers.get("Content-Type", "").lower().startswith("application/octet-stream"),
                        "MEDIA_CONTENT_TYPE")
                declared = reply.headers.get("Content-Length")
                require(declared is not None, "MEDIA_LENGTH_REQUIRED")
                length = int(declared)
                require(0 < length <= MAX_VIDEO, "MEDIA_DECLARED_LENGTH")
                while count < length:
                    require(time.monotonic() - started <= MAX_ELAPSED, "MEDIA_WALL_CAP")
                    chunk = reply.read(min(65536, length - count))
                    require(bool(chunk), "MEDIA_SHORT_READ")
                    count += len(chunk)
                    require(count <= MAX_VIDEO, "MEDIA_BODY_CAP")
                    sink.write(chunk)
                    digest.update(chunk)
                    if count % (8 * 1024 * 1024) < len(chunk):
                        sink.flush()
                        os.fsync(sink.fileno())
                # Do not read beyond declared bound; HTTP framing and declared size
                # must be consistent, but wire-byte volume is not measured.
            sink.flush()
            os.fsync(sink.fileno())
        require(part.stat().st_size == length, "MEDIA_FILE_LENGTH")
        with part.open("rb") as check:
            require(check.read(4) == b"\x1a\x45\xdf\xa3", "MEDIA_EBML_HEADER")
        os.replace(part, video)
        journal(jf, stage="MEDIA_COMPLETE", bytes=count)
    print(json.dumps({"status": "LONG_VIDEO_COMPLETE",
                      "body_bytes": count, "variant": selected,
                      "license_status": status, "sha256": digest.hexdigest()}))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--private-dir", required=True, type=Path)
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    try:
        if args.selftest:
            print(json.dumps({"status": "OFFLINE_SCHEMA_SELFTEST_PASS" if selftest() else "HOLD"}))
        else:
            run(args.private_dir)
    except GateError as ex:
        # Stable stage code, never raw private metadata, URL or response body.
        print(json.dumps({"status": "HOLD", "reason_code": ex.stage}))
        sys.exit(2)
    except Exception as ex:
        print(json.dumps({"status": "HOLD", "reason_code": type(ex).__name__}))
        sys.exit(2)
