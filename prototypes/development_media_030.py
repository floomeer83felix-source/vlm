"""030 exact-object/PTS helpers with fixed031 gates; no private defaults."""
import argparse
import ast
import hashlib
import inspect
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
from urllib.parse import quote, urlsplit, parse_qsl

from development_pilot_030 import Journal, require, require_ready, load, MIB, GIB
from source_provenance_029 import canonical_object, dotted


class SendGate:
    def __init__(self, journal, slot, method, url, version=None):
        self.journal, self.slot, self.method, self.url, self.version = journal, slot, method, url, version

    def reserve(self, method, url):
        base = urlsplit(self.url); actual = urlsplit(url)
        expected_query = [('versionId', self.version)] if self.version else []
        require(method == self.method and actual.scheme == 'https' and not actual.fragment
                and (actual.netloc, actual.path) == (base.netloc, base.path)
                and parse_qsl(actual.query, keep_blank_values=True) == expected_query, 'EXACT_SEND_REQUIRED')
        rows = self.journal.events('HTTPS')
        api = self.slot.split(':')[0]
        require(api in ('HeadBucket', 'HeadObject', 'GetObject') and len(rows) < 12
                and sum(r['api'] == api for r in rows) < 4, 'HTTPS_CAP')
        require(not any(r['method']==method and r['url']==url for r in rows),'OBJECT_ALREADY_ATTEMPTED_ACROSS_ALIAS')
        self.journal.once('HTTPS', self.slot, api=api, method=method, url=url)


def proven_transport(source):
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or not dotted(node.func).endswith('urlopen'):
            continue
        keywords = {k.arg: k.value for k in node.keywords}
        retry = keywords.get('retries'); preload = keywords.get('preload_content')
        if (isinstance(retry, ast.Call) and dotted(retry.func).endswith('Retry')
                and len(retry.args) == 1 and isinstance(retry.args[0], ast.Constant)
                and retry.args[0].value is False and isinstance(preload, ast.Constant) and preload.value is False):
            return True
    return False


def match_headers(headers, expected):
    lowered = {str(k).lower(): str(v) for k, v in headers.items()}
    require(sum(len(k.encode()) + len(v.encode()) for k, v in lowered.items()) <= 65536, 'HEADER_RETENTION')
    require(int(lowered.get('content-length', '-1')) == expected['ContentLength']
            and lowered.get('etag') == expected['ETag'], 'GET_HEADER_BINDING')
    require(lowered.get('x-amz-version-id') == expected.get('VersionId'), 'GET_VERSION_BINDING')


class EmptyBody:
    def stream(self, *args, **kwargs):
        return iter(())
    def read(self, *args, **kwargs):
        return b''
    def close(self):
        pass


def install_transport(client, gate, context, source, expected=None):
    require(proven_transport(source), 'LOW_LEVEL_RETRY_PRELOAD_UNPROVEN')
    pending = []
    def before(request, **kwargs):
        method = request.method.decode() if isinstance(request.method, bytes) else request.method
        gate.reserve(method, request.url)
        if expected is not None:
            value = request.headers.get('If-Match')
            if isinstance(value, bytes):
                value = value.decode()
            require(value == expected['ETag'], 'GET_IF_MATCH_REQUIRED')
        pending.append((method, request.url))
    client.meta.events.register_first('before-send.s3', before, unique_id='030-exact-send')
    original = client._endpoint.http_session.send
    def send(request):
        method = request.method.decode() if isinstance(request.method, bytes) else request.method
        require(pending and pending.pop(0) == (method, request.url), 'TRANSPORT_WITHOUT_GATE')
        gate.journal.add('TRANSPORT_SEND',slot=gate.slot,method=method,url=request.url)
        response = original(request)
        context.update(status=response.status_code, region=response.headers.get('x-amz-bucket-region'))
        raw = response.raw
        try:
            gate.journal.add('TRANSPORT_RESPONSE',slot=gate.slot,status=response.status_code,
                             observed_region=context.get('region'))
            require(sum(len(str(k).encode()) + len(str(v).encode()) for k, v in response.headers.items()) <= 65536, 'HEADER_RETENTION')
            if method == 'HEAD':
                require(getattr(raw, 'length_remaining', None) == 0 and not getattr(raw, 'chunked', False), 'HEAD_BODY_HOLD')
            elif response.status_code == 200:
                require(expected is not None and not getattr(raw, 'chunked', False), 'GET_STREAM_HOLD')
                match_headers(response.headers, expected)
                require(raw.length_remaining == expected['ContentLength'], 'GET_RAW_LENGTH')
                return response  # StreamingBody remains unconsumed until caller's debit.
        except BaseException:
            raw.close(); response.raw = EmptyBody(); raise
        raw.close(); response.raw = EmptyBody()  # Error/HEAD bodies never read or drain.
        return response
    client._endpoint.http_session.send = send


def sdk(journal, save_sources=False):
    import botocore.session
    from botocore.credentials import SharedCredentialProvider, CredentialResolver, Credentials
    from botocore.httpsession import URLLib3Session
    import ego4d.cli.universities as universities
    require(not any(os.environ.get(k) for k in ('AWS_SHARED_CREDENTIALS_FILE', 'AWS_CONFIG_FILE')), 'PROFILE_OVERRIDE')
    session = botocore.session.Session(profile='ego4d')
    profile = session.full_config.get('profiles', {}).get('ego4d', {})
    forbidden = ('role_arn', 'credential_source', 'credential_process', 'source_profile', 'web_identity_token_file', 'sso_session', 'sso_start_url')
    require(not any(profile.get(k) for k in forbidden), 'NONSTATIC_PROFILE')
    provider = SharedCredentialProvider(session.get_config_variable('credentials_file'), profile_name='ego4d')
    session.register_component('credential_provider', CredentialResolver([provider]))
    credentials = session.get_credentials()
    require(type(credentials) is Credentials and credentials.method == 'shared-credentials-file', 'STATIC_CREDENTIALS_REQUIRED')
    if save_sources:
        for alias, filename in (('sdk_transport', inspect.getsourcefile(URLLib3Session)), ('sdk_universities', universities.__file__)):
            raw = journal.input(alias, filename, 'source')
            journal.reserve_output(alias + '.py', len(raw))
            with open(journal.root / (alias + '.py'), 'xb') as target:
                target.write(raw); target.flush(); os.fsync(target.fileno())
    source = (journal.root / 'sdk_transport.py').read_text(encoding='utf-8')
    require(proven_transport(source), 'LOW_LEVEL_RETRY_PRELOAD_UNPROVEN')
    buckets = set(universities.UNIV_TO_BUCKET.values())
    require(buckets and all(type(x) is str for x in buckets), 'OFFICIAL_BUCKET_SCHEMA')
    regions = set(session.get_available_regions('s3', partition_name='aws'))
    return session, buckets, regions, source


def client_for(session, journal, source, region, slot, bucket, key=None, expected=None):
    from botocore.config import Config
    from botocore.httpsession import URLLib3Session
    discovery = slot.startswith('HeadBucket:')
    endpoint = 'https://s3.amazonaws.com' if discovery else 'https://s3.' + region + '.amazonaws.com'
    client = session.create_client('s3', region_name=region, endpoint_url=endpoint,
        config=Config(signature_version='s3v4', connect_timeout=10, read_timeout=90 if expected else 10,
                      retries={'total_max_attempts': 1, 'mode': 'standard'}, proxies={}, max_pool_connections=1,
                      s3={'addressing_style': 'path'}))
    require(type(client._endpoint.http_session) is URLLib3Session, 'SDK_TRANSPORT_TYPE')
    url = endpoint + '/' + bucket + ('/' + quote(key, safe='/~') if key is not None else '')
    context = {}
    gate = SendGate(journal, slot, 'GET' if expected else 'HEAD', url, expected.get('VersionId') if expected else None)
    install_transport(client, gate, context, source, expected)
    return client, context


def metadata(root):
    journal = Journal(root)
    try:
        require_ready(journal)
        journal.once('PHASE', 'metadata')
        session, buckets, regions, source = sdk(journal, save_sources=True)
        targets = load(root, 'targets.json')['targets']
        prior = {x['alias']: x for x in load(root, 'heads029.json')['results']}
        region_cache = {}
        for target in targets:
            p = prior.get(target['alias'], {})
            if p.get('status') == 200 and p.get('region') in regions:
                region_cache[target['bucket']] = p['region']
        records = []
        for target in targets:
            alias = target['alias']; record = dict(alias=alias, status='HOLD')
            try:
                require(target['bucket'] in buckets and canonical_object(target['uri']) == (target['bucket'], target['key']), 'OFFICIAL_TARGET_BINDING')
                region = region_cache.get(target['bucket'])
                if region not in regions:
                    client, context = client_for(session, journal, source, 'us-east-1', 'HeadBucket:' + target['bucket'], target['bucket'])
                    exception = None
                    try:
                        client.head_bucket(Bucket=target['bucket'])
                    except Exception as error:
                        exception = type(error).__name__
                    finally:
                        client.close()
                        journal.add('BUCKET_TERMINAL', bucket=target['bucket'], status=context.get('status'), region=context.get('region'), exception=exception)
                    require(context.get('region') in regions, 'TRUSTED_REGION_UNKNOWN')
                    region = context['region']; region_cache[target['bucket']] = region
                client, context = client_for(session, journal, source, region, 'HeadObject:' + alias, target['bucket'], target['key'])
                try:
                    result = client.head_object(Bucket=target['bucket'], Key=target['key'])
                    record.update(status=result['ResponseMetadata']['HTTPStatusCode'], region=region,
                                  ContentLength=result.get('ContentLength'), ETag=result.get('ETag'), VersionId=result.get('VersionId'))
                finally:
                    client.close()
                    journal.add('OBJECT_HEAD_TERMINAL', alias=alias, observed_status=context.get('status'))
                size = record.get('ContentLength'); etag = record.get('ETag')
                require(record['status'] == 200 and type(size) is int and 0 < size <= 4 * GIB, 'HEAD_SIZE_STATUS')
                require(type(etag) is str and etag.startswith('"') and etag.endswith('"') and not etag.startswith('W/'), 'STRONG_ETAG_REQUIRED')
                if alias == 'P1':
                    require(size <= 890 * MIB and size == prior[alias]['ContentLength'] and etag == prior[alias]['ETag']
                            and record.get('VersionId') == prior[alias].get('VersionId'), 'P1_029_OBJECT_CHANGED')
                record['eligible'] = True
            except Exception as error:
                record.update(eligible=False, reason=str(error) if isinstance(error, ValueError) and str(error).isupper() else type(error).__name__)
            records.append(record)
            journal.write(alias + '-head.json', record)
        journal.write('metadata-summary.json', dict(results=records))
    finally:
        journal.close()


def transfer(body, target, expected, journal, alias):
    size = expected['ContentLength']; received = 0; sha = hashlib.sha256()
    while received < size:
        amount = min(MIB, size - received)
        debits = journal.events('BODY_DEBIT')
        require(sum(r['amount'] for r in debits) + amount <= 16 * GIB and
                sum(r['amount'] for r in debits if r['alias'] == alias) + amount <= size, 'BODY_BYTE_CAP')
        journal.add('BODY_DEBIT', alias=alias, amount=amount)
        chunk = body.read(amount)
        require(type(chunk) is bytes and 0 < len(chunk) <= amount, 'TRUNCATED_BODY')
        target.write(chunk); sha.update(chunk); received += len(chunk)
    require(body._amount_read == size and body._raw_stream.length_remaining == 0, 'RESPONSE_NOT_COMPLETE')
    target.flush(); os.fsync(target.fileno())
    require(os.fstat(target.fileno()).st_size == size, 'LOCAL_MEDIA_LENGTH')
    return sha.hexdigest(), received


def get_object(root, alias):
    journal = Journal(root); body = client = None; context = {}
    try:
        require_ready(journal)
        journal.once('PHASE', 'get-' + alias)
        target = next(t for t in load(root, 'targets.json')['targets'] if t['alias'] == alias)
        expected = load(root, alias + '-head.json'); require(expected.get('eligible') is True, 'HEAD_NOT_ELIGIBLE')
        session, buckets, regions, source = sdk(journal)
        require(target['bucket'] in buckets and expected['region'] in regions, 'OFFICIAL_ENDPOINT')
        size = expected['ContentLength']
        require(shutil.disk_usage(root).free >= size + 2 * GIB, 'DISK_HEADROOM')
        partial = alias + '.partial'; final = alias + '.mp4'
        journal.reserve_output(partial, size, 'media')
        # Same-directory rename, one storage reservation, explicit final identity.
        require(not (Path(root) / final).exists(), 'MEDIA_FINAL_EXISTS')
        journal.add('RENAME_PLANNED', old=partial, new=final)
        client, context = client_for(session, journal, source, expected['region'], 'GetObject:' + alias,
                                     target['bucket'], target['key'], expected)
        kwargs = dict(Bucket=target['bucket'], Key=target['key'], IfMatch=expected['ETag'])
        if expected.get('VersionId'):
            kwargs['VersionId'] = expected['VersionId']
        result = client.get_object(**kwargs); body = result['Body']
        match_headers(result['ResponseMetadata']['HTTPHeaders'], expected)
        with open(Path(root) / partial, 'xb') as destination:
            sha, received = transfer(body, destination, expected, journal, alias)
        body.close(); body = None
        os.rename(Path(root) / partial, Path(root) / final)
        stat = (Path(root) / final).stat()
        journal.write(alias + '-media-binding.json', dict(alias=alias, file=final, uri=target['uri'],
                      ContentLength=size, ETag=expected['ETag'], VersionId=expected.get('VersionId'),
                      sha256=sha, size=stat.st_size, mtime_ns=stat.st_mtime_ns, received=received))
        journal.add('MEDIA_COMPLETE', alias=alias, size=received)
    except Exception as error:
        # Diagnostics only: never read an error body, retry, or print SDK error
        # messages/headers. Earlier031 attempts predate this added persistence.
        response=getattr(error,'response',{})
        status=context.get('status',response.get('ResponseMetadata',{}).get('HTTPStatusCode'))
        code=response.get('Error',{}).get('Code')
        if not isinstance(code,str) or len(code)>64 or not all(c.isalnum() or c in '._-' for c in code):code=None
        journal.write(alias + '-acquisition-failure.json', dict(reason=str(error) if isinstance(error, ValueError) and str(error).isupper() else type(error).__name__,
                                                              observed_status=status,service_code=code))
    finally:
        if body is not None:
            body.close()
        if client is not None:
            client.close()
        journal.close()


def candidates(root, alias):
    import av
    import numpy as np
    journal = Journal(root); start = time.monotonic()
    try:
        require_ready(journal)
        journal.once('PHASE', 'candidates-' + alias)
        binding = load(root, alias + '-media-binding.json')
        path = Path(root) / binding['file']; stat = path.stat()
        require(stat.st_size == binding['size'] and stat.st_mtime_ns == binding['mtime_ns'], 'MEDIA_CHANGED')
        task = next(x for x in load(root, 'worker-input.json')['sources'] if x['alias'] == alias)
        pts_min = math.inf; pts_max = -math.inf; count = corrupt = missing = 0
        with av.open(str(path)) as container:
            require(len(container.streams.video) == 1, 'VIDEO_STREAM_COUNT')
            stream = container.streams.video[0]; stream.thread_count = 2
            fps = float(stream.average_rate) if stream.average_rate else None
            duration = float(container.duration / av.time_base)
            video_duration = float(stream.duration * stream.time_base) if stream.duration else None
            tolerance = max(.10, 2 / fps) if fps and fps > 0 else .10
            require(math.isfinite(duration) and abs(duration - task['declared_duration']) <= tolerance, 'CONTAINER_DURATION_MISMATCH')
            require(video_duration is not None and abs(video_duration - task['declared_duration']) <= tolerance, 'VIDEO_DURATION_MISMATCH')
            require(fps and math.isfinite(fps) and fps > 0, 'FPS_REQUIRED_FOR_FROZEN_HELPER')
            shape = (stream.height, stream.width, 3)
            frame_bytes = 48 * math.prod(shape)
            require(shutil.disk_usage(root).free >= frame_bytes + 4096 + 2 * GIB, 'FRAME_HEADROOM')
            for packet in container.demux(stream):
                require(time.monotonic() - start < 295, 'MEDIA_DEADLINE')
                if not packet.size:
                    continue
                count += 1; corrupt += bool(packet.is_corrupt)
                if packet.pts is None:
                    missing += 1; continue
                value = float(packet.pts * packet.time_base)
                require(math.isfinite(value), 'PACKET_NONFINITE')
                pts_min = min(pts_min, value); pts_max = max(pts_max, value)
            require(count > 0 and corrupt == 0 and missing == 0 and pts_max - pts_min >= 1200, 'PACKET_INTEGRITY')
            filename = alias + '-frames.npy'
            journal.reserve_output(filename, frame_bytes + 4096, 'frames')
            with open(Path(root) / filename, 'xb') as destination:
                # NPY header plus raw RGB, preserves original pixels.
                np.lib.format.write_array_header_1_0(destination, dict(descr=np.dtype('uint8').str, fortran_order=False, shape=(48,) + shape))
                times = []; seen = 0; frame_hashes = []
                for target in np.linspace(pts_min, pts_max - .10, 48):
                    require(time.monotonic() - start < 295, 'MEDIA_DEADLINE')
                    container.seek(int(target / float(stream.time_base)), stream=stream, backward=True, any_frame=False)
                    found = False
                    for frame in container.decode(stream):
                        seen += 1; require(frame.pts is not None, 'DECODE_PTS_MISSING')
                        value = float(frame.pts * frame.time_base)
                        if value + 1e-6 < target:
                            continue
                        require(math.isfinite(value) and value >= 0 and (not times or value > times[-1]), 'DECODE_PTS_ORDER')
                        rgb = frame.to_ndarray(format='rgb24'); require(rgb.shape == shape, 'RGB_SHAPE_CHANGE')
                        raw = rgb.tobytes(); destination.write(raw); frame_hashes.append(hashlib.sha256(raw).hexdigest())
                        times.append(value); found = True; break
                    require(found, 'CANDIDATE_UNAVAILABLE')
                destination.flush(); os.fsync(destination.fileno())
        journal.write(alias + '-candidates.json', dict(alias=alias, frames=filename, times=times, fps=fps, duration=duration,
                      video_duration=video_duration, declared_duration=task['declared_duration'], duration_delta=duration-task['declared_duration'],
                      prior=dict(video_packets=count), min_packet_pts=pts_min, max_packet_pts=pts_max, demux_eof=True,
                      packets=count, corrupt=corrupt, missing=missing, actual_decoded_frames=seen, rgb_hashes=frame_hashes,
                      seconds=time.monotonic()-start, frame_bytes=frame_bytes))
    except Exception as error:
        journal.write(alias + '-candidate-failure.json', dict(reason=str(error) if isinstance(error, ValueError) and str(error).isupper() else type(error).__name__))
    finally:
        journal.close()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('mode', choices=['metadata', 'get', 'candidates'])
    parser.add_argument('root'); parser.add_argument('alias', nargs='?'); args = parser.parse_args()
    sys.stdin.readline()  # Job/parent handshake before SDK/PyAV imports.
    if args.mode == 'metadata':
        metadata(args.root)
    elif args.mode == 'get':
        get_object(args.root, args.alias)
    else:
        candidates(args.root, args.alias)


if __name__ == '__main__':
    main()
