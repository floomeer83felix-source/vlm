"""055 bounded public metadata acquisition. No import-time network/model work.

This entry point does not authorize inference or infer provenance from filenames.
All response bodies, including redirects/errors, debit the persistent byte ledger.
Consumed requests cannot be silently repeated. Private bodies stay under --root.
"""
import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

CAP = 16 * 1024**2


def persist(path, value):
    with open(path, 'x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.flush()
        os.fsync(stream.fileno())


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Acquisition:
    def __init__(self, root):
        self.root = Path(root)
        self.ledger = self.root / 'network.jsonl'
        self.used = 0
        self.consumed = set()
        if self.ledger.exists():
            for line in self.ledger.read_text(encoding='utf-8').splitlines():
                record = json.loads(line)
                self.used += record.get('bytes', 0)
                if record['event'] == 'STARTED':
                    self.consumed.add(record['key'])
        self.opener = urllib.request.build_opener(NoRedirect)

    def event(self, **record):
        record['at_unix'] = time.time()
        with open(self.ledger, 'a', encoding='utf-8') as stream:
            stream.write(json.dumps(record, sort_keys=True) + '\n')
            stream.flush()
            os.fsync(stream.fileno())

    def fetch(self, key, url):
        if key in self.consumed:
            raise RuntimeError('REQUEST_ALREADY_STARTED: ' + key)
        if self.used >= CAP:
            raise RuntimeError('METADATA_BUDGET_EXHAUSTED')
        self.event(event='STARTED', key=key, url=url)
        self.consumed.add(key)
        start = time.monotonic()
        try:
            for hop in range(6):
                parsed = urllib.parse.urlsplit(url)
                if parsed.scheme != 'https' or parsed.hostname not in (
                    'huggingface.co', 'raw.githubusercontent.com', 'api.github.com'):
                    raise ValueError('UNAPPROVED_METADATA_HOST')
                request = urllib.request.Request(url, headers={
                    'User-Agent': 'VLM055-bounded-research', 'Accept-Encoding': 'identity'})
                try:
                    response = self.opener.open(request, timeout=30)
                except urllib.error.HTTPError as error:
                    response = error
                status = response.code
                parts = []
                with response:
                    while True:
                        if time.monotonic() - start > 90:
                            raise TimeoutError('OBJECT_WALL_LIMIT')
                        remaining = CAP - self.used
                        if remaining <= 0:
                            raise RuntimeError('METADATA_BUDGET_EXHAUSTED')
                        chunk = response.read(min(65536, remaining))
                        if not chunk:
                            break
                        self.used += len(chunk)
                        self.event(event='BODY', key=key, hop=hop, bytes=len(chunk))
                        parts.append(chunk)
                    body = b''.join(parts)
                    if status in (301, 302, 303, 307, 308):
                        url = urllib.parse.urljoin(url, response.headers['Location'])
                        self.event(event='REDIRECT', key=key, status=status, url=url)
                        continue
                path = self.root / (key + '.body')
                with open(path, 'xb') as stream:
                    stream.write(body)
                    stream.flush()
                    os.fsync(stream.fileno())
                self.event(event='CLOSED', key=key, status=status,
                           sha256=hashlib.sha256(body).hexdigest(), seconds=time.monotonic()-start)
                if status != 200:
                    raise RuntimeError('HTTP_STATUS_' + str(status))
                return body
            raise RuntimeError('REDIRECT_LIMIT')
        except Exception as error:
            self.event(event='FAILED', key=key, reason=type(error).__name__,
                       detail=str(error), seconds=time.monotonic()-start)
            raise


def acquire(root):
    client = Acquisition(root)
    results = {}
    for name, repo, annotation in (
        ('dybench', 'ddz16/DyBench', 'json/event_sequence.json'),
        ('timeblind', 'BaiqiL/TimeBlind', 'data.jsonl')):
        try:
            info = json.loads(client.fetch(name+'_revision', 'https://huggingface.co/api/datasets/'+repo))
            revision = info['sha']
            persist(Path(root)/(name+'_revision.json'), dict(revision=revision,
                    files=[x['rfilename'] for x in info.get('siblings', [])]))
            client.fetch(name+'_readme', 'https://huggingface.co/datasets/'+repo+'/resolve/'+revision+'/README.md')
            client.fetch(name+'_annotations', 'https://huggingface.co/datasets/'+repo+'/resolve/'+revision+'/'+annotation)
            results[name] = dict(status='METADATA_ACQUIRED', revision=revision)
        except Exception as error:
            results[name] = dict(status='METADATA_FAILED', reason=str(error))
    persist(Path(root)/'acquisition.json', dict(datasets=results, metadata_bytes=client.used,
            media_bytes=0, model_calls=0, optimizer_steps=0))
    print(json.dumps(results))


def references(root):
    client = Acquisition(root)
    for name, repo, files in (
        ('crpo', 'ddz16/CRPO', ['README.md']),
        ('timeblind_code', 'Baiqi-Li/TimeBlind', ['README.md', 'utils.py', 'tags.json'])):
        info = json.loads(client.fetch(name+'_repo', 'https://api.github.com/repos/'+repo))
        commit = json.loads(client.fetch(name+'_commit', 'https://api.github.com/repos/'+repo+'/commits/'+info['default_branch']))['sha']
        persist(Path(root)/(name+'_revision.json'), dict(revision=commit))
        for filename in files:
            client.fetch(name+'_'+filename.replace('.', '_'), 'https://raw.githubusercontent.com/'+repo+'/'+commit+'/'+filename)


def audit(root):
    """Audit all acquired rows; do not infer physical provenance from basenames.

    No samples/splits or media requests are frozen when the prerequisite fails.
    Pair membership below is an annotation consistency candidate, not certification.
    """
    root = Path(root)
    rows = json.loads((root/'dybench_annotations.body').read_bytes())
    groups = defaultdict(list)
    for row in rows:
        groups[(row['source_subcategory'], re.sub(r'_reversed(?=\.mp4$)', '', row['video']))].append(row)
    reasons = Counter()
    answer0 = 'First action 1, then action 2'
    answer1 = 'First action 2, then action 1'
    for members in groups.values():
        if len(members) != 2:
            reasons['not_two_rows'] += 1
            continue
        a, b = members
        match = re.fullmatch(r'.*\nAction 1\. (.+)\nAction 2\. (.+)\nPlease output their order\.', a['question'], re.S)
        if a['question'] != b['question'] or not match or match[1].strip() == match[2].strip():
            reasons['unresolved_events_or_question'] += 1
        elif {a['answer'], b['answer']} != {answer0, answer1} or any(x['candidates'] != [answer0, answer1] for x in members):
            reasons['inconsistent_answers'] += 1
        else:
            reasons['annotation_pair_consistent'] += 1
    sizes = json.loads((root/'dybench_file_sizes.body').read_bytes())
    entry = next(x for x in sizes if x['path'] == 'video/event_sequence.zip')
    files = json.loads((root/'dybench_revision.json').read_text())['files']
    ledger = [json.loads(x) for x in (root/'network.jsonl').read_text().splitlines()]
    tags = json.loads((root/'timeblind_code_tags_json.body').read_bytes())
    tb = [json.loads(x) for x in (root/'timeblind_annotations.body').read_text().splitlines()]
    temporal = set(tags['Temporal_Relation'])
    report = dict(status='INPUT_NOT_QUALIFIED', scientific_status='INCOMPLETE',
        stop_reasons=['NO_SELECTED_SINGLE_VIDEO_OBJECTS_IN_FIXED_OFFICIAL_TREE',
                      'PUBLISHED_ARCHIVE_EXCEEDS_SINGLE_OBJECT_AND_TOTAL_MEDIA_CAPS',
                      'ORIGINAL_RECORDING_GROUP_MAP_NOT_VERIFIED'],
        dybench=dict(rows=len(rows), candidate_pairs=len(groups), pair_audit=dict(reasons),
                     category_rows=dict(Counter(x['source_subcategory'] for x in rows)),
                     annotation_fields=sorted(set(k for x in rows for k in x)),
                     archive_bytes=entry['size'], direct_video_objects=sum(x.endswith('.mp4') for x in files),
                     provenance='UNVERIFIED', admitted_instances=0, splits_frozen=False),
        timeblind=dict(rows=len(tb), temporal_tag_rows=sum(x['index'] in temporal for x in tb),
                       temporal_candidate_instances=len(temporal)//4,
                       strict_qualification='NOT_COMPLETED_AFTER_DEVELOPMENT_PREREQUISITE_STOP',
                       external_gate='UNKNOWN', admitted_instances=0),
        network=dict(metadata_bytes=sum(x.get('bytes', 0) for x in ledger),
                     started=sum(x['event']=='STARTED' for x in ledger),
                     closed=sum(x['event']=='CLOSED' for x in ledger),
                     failed=sum(x['event']=='FAILED' for x in ledger), media_bytes=0),
        model_calls=0, generate_forward_steps=0, optimizer_steps=0,
        gpu_stage_started=False, head_implemented=False, scientific_gate='INCOMPLETE',
        novelty='UNRESOLVED')
    persist(root/'qualification.json', report)
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--phase', choices=['acquire', 'references', 'audit'], default='acquire')
    args = parser.parse_args()
    {'acquire': acquire, 'references': references, 'audit': audit}[args.phase](args.root)
