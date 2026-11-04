"""085: explicit, schema-attested metadata only; no discovery or media opens.

The four readable schemas are attested by the public 081 writers. Known mixed
files are denied BEFORE open, not read and filtered. Unknown schemas are denied.
Only registered media paths may receive stat; no video payload is read/hashed.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import time

SAFE = frozenset(('parent.json', 'manifest-seal.json',
                  'media-manifest-gate.json', 'media-manifest.json'))
MIXED = frozenset(('media-plan.json', 'prepared-index.json', 'observations.json',
                   'truth.json', 'answers.json', 'relations.json'))
MAX_FILES = 64
MAX_BYTES = 16 * 1024**2


class StopAudit(Exception):
    pass


def require(ok, reason):
    if not ok:
        raise StopAudit(reason)


def inside(root, path):
    """Lexical check first: never resolve an already outside-root reference."""
    root = Path(root).resolve(strict=True)
    path = Path(path)
    path = path if path.is_absolute() else root / path
    lexical = Path(os.path.abspath(path))
    try:
        require(os.path.commonpath((str(root), str(lexical))) == str(root),
                'OUTSIDE_APPROVED_ROOT')
        resolved = lexical.resolve(strict=False)
        require(os.path.commonpath((str(root), str(resolved))) == str(root),
                'OUTSIDE_APPROVED_ROOT')
    except ValueError:
        raise StopAudit('OUTSIDE_APPROVED_ROOT') from None
    return resolved


class MetadataReader:
    def __init__(self, root, whitelist, max_files=MAX_FILES, max_bytes=MAX_BYTES):
        self.root = Path(root).resolve(strict=True)
        require(self.root.is_dir(), 'BLOCKED_MISSING_REGISTERED_ROOT')
        self.whitelist = frozenset(whitelist)
        self.max_files, self.max_bytes = max_files, max_bytes
        require(0 < max_files <= MAX_FILES and 0 <= max_bytes <= MAX_BYTES,
                'INVALID_BUDGET')
        self.files = self.bytes = self.media_stats = 0
        self.cache = {}
        self.denials = {}
        self.cpu_start = time.process_time()

    def cpu_gate(self):
        require(time.process_time() - self.cpu_start <= 60, 'CPU_BUDGET')

    def read(self, name):
        self.cpu_gate()
        require(name in self.whitelist, 'NOT_EXPLICITLY_ALLOWLISTED')
        if name in MIXED:
            raise StopAudit('NOT_PERMITTED_MIXED_FILE')
        require(name in SAFE, 'NOT_PERMITTED_UNATTESTED_SCHEMA')
        path = inside(self.root, name)
        if name not in self.cache:
            try:
                info = path.stat()
            except FileNotFoundError:
                raise StopAudit('MISSING_REGISTERED_METADATA') from None
            require(stat.S_ISREG(info.st_mode), 'NOT_REGULAR_METADATA')
            require(self.files + 1 <= self.max_files, 'FILE_BUDGET')
            require(self.bytes + info.st_size <= self.max_bytes, 'BYTE_BUDGET')
            # Charge the complete bounded read BEFORE opening. A failed read
            # keeps its reservation; there is no retry or quota reset.
            self.files += 1
            self.bytes += info.st_size
            with path.open('rb') as stream:
                body = stream.read(info.st_size)
                require(os.fstat(stream.fileno()).st_size == info.st_size,
                        'METADATA_SIZE_CHANGED')
            require(len(body) == info.st_size, 'METADATA_SHORT_READ')
            require(inside(self.root, name) == path, 'PATH_CHANGED')
            self.cache[name] = body
        return self.cache[name]

    def meta(self, name):
        try:
            return json.loads(self.read(name).decode('utf-8-sig'))
        except (UnicodeError, json.JSONDecodeError):
            raise StopAudit('BLOCKED_SAFE_SCHEMA') from None

    def media_stat(self, registered_path, expected_bytes):
        self.cpu_gate()
        try:
            path = inside(self.root, registered_path)
        except StopAudit:
            return 'EXTERNAL_REF_UNVERIFIED'
        self.media_stats += 1
        try:
            info = os.stat(path)  # metadata only; never open the media
        except FileNotFoundError:
            return 'MISSING_REGISTERED_MEDIA'
        if not stat.S_ISREG(info.st_mode):
            return 'NOT_REGULAR_MEDIA'
        return 'SIZE_MATCH' if info.st_size == expected_bytes else 'SIZE_MISMATCH'


def classify_continuity(evidence):
    """Necessary metadata conditions, illustrated on synthetic evidence only.

    Counts below are proof counts, never assertions that absent evidence means
    absent media. No intervals are inferred from original 081 event questions.
    """
    if evidence.get('media_kind') in ('cut_only', 'reassembled_only'):
        return 'ONLY_CUT_OR_REASSEMBLED_EVIDENCE'
    if not evidence.get('complete_original_recording_sealed'):
        return 'ORIGINAL_CONTINUITY_NOT_PROVED'
    intervals = evidence.get('intervals')
    if evidence.get('time_basis') != 'original_recording' or not intervals:
        return 'INSUFFICIENT_TIMESTAMPS'
    if len(intervals) != 3:
        return 'INSUFFICIENT_TIMESTAMPS'
    if not all(len(pair) == 2 and all(isinstance(v, (int, float)) and
               not isinstance(v, bool) and math.isfinite(v) for v in pair)
               and 0 <= pair[0] < pair[1] for pair in intervals):
        return 'INVALID_INTERVALS'
    duration = evidence.get('recorded_duration')
    if not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
        return 'INSUFFICIENT_TIMESTAMPS'
    if intervals[-1][1] > duration:
        return 'INVALID_INTERVALS'
    gaps = [intervals[i+1][0] - intervals[i][1] for i in (0, 1)]
    if min(gaps) < 0:
        return 'INVALID_INTERVALS'
    tolerance = evidence.get('sealed_gap_tolerance')
    if max(gaps) > 0 and tolerance is None:
        return 'CONTIGUITY_UNCONFIRMED'
    if tolerance is not None:
        if not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance < 0:
            return 'INVALID_TOLERANCE'
        if max(gaps) > tolerance:
            return 'CONTIGUITY_UNCONFIRMED'
    return 'METADATA_CANDIDATE_EXISTS'


def audit(root, whitelist, prior_files=0, prior_bytes=0, known_missing=()):
    start = time.process_time()
    try:
        a = MetadataReader(root, whitelist)
    except (FileNotFoundError, OSError):
        return dict(status='BLOCKED_MISSING_REGISTERED_ROOT', files_read=0, bytes_read=0)
    result = dict(status='BLOCKED', registered_sources=None, files_read=0, bytes_read=0)
    try:
        require(0 <= prior_files <= MAX_FILES and 0 <= prior_bytes <= MAX_BYTES,
                'INVALID_PRIOR_USAGE')
        a.files, a.bytes = prior_files, prior_bytes
        require(set(known_missing).issubset({'manifest-seal.json'}),
                'INVALID_KNOWN_MISSING')
        # These are the only file schemas approved before any real read. The
        # allowlist may include a known mixed file solely to record its refusal.
        for name in whitelist:
            if name in MIXED:
                a.denials['NOT_PERMITTED_MIXED_FILE'] = a.denials.get('NOT_PERMITTED_MIXED_FILE', 0) + 1
            else:
                require(name in SAFE, 'NOT_PERMITTED_UNATTESTED_SCHEMA')
        parent = a.meta('parent.json')
        require(parent.get('task') == 'VLM-TIMESTAMPED-TRIPLES-STREAM-081' and
                parent.get('sync_sha') == 'be0d3ca', 'BLOCKED_IDENTITY_UNKNOWN')
        # Optional historical summary: absence is recorded, not repaired by
        # opening its mixed media-plan or searching a different root.
        manifest_seal = None
        if 'manifest-seal.json' not in known_missing:
            try:
                manifest_seal = a.meta('manifest-seal.json')
            except StopAudit as exc:
                if str(exc) != 'MISSING_REGISTERED_METADATA':
                    raise
        if manifest_seal is None:
            a.denials['MISSING_REGISTERED_METADATA'] = 1
        gate = a.meta('media-manifest-gate.json')
        require((manifest_seal is None or manifest_seal.get('groups') == 32) and gate.get('status') == 'PASS' and
                gate.get('members') == 32 and gate.get('reused') == 5 and gate.get('new') == 27,
                'BLOCKED_IDENTITY_UNKNOWN')
        body = a.read('media-manifest.json')
        require(hashlib.sha256(body).hexdigest() == gate.get('manifest_sha256'),
                'BLOCKED_IDENTITY_UNKNOWN')
        records = json.loads(body.decode('utf-8-sig'))
        require(len(records) == 32 and [x['group'] for x in records] == list(range(32)),
                'BLOCKED_IDENTITY_UNKNOWN')
        require(sum(x['bytes'] for x in records) == 579702574 and
                (manifest_seal is None or manifest_seal.get('uncompressed') == 579702574),
                'BLOCKED_IDENTITY_UNKNOWN')
        counts = {}
        for rec in records:
            a.cpu_gate()
            require(type(rec['bytes']) is int and rec['bytes'] > 0 and
                    rec.get('source_generation') == '1685446268139925' and
                    rec['bytes'] == rec['media_directory']['uncompressed'] and
                    rec['crc'] == rec['media_directory']['crc'], 'BLOCKED_IDENTITY_UNKNOWN')
            require(rec.get('pipeline_code_sha256') ==
                    'bb0a1736f4fa4d48ace4a91182c96c1841529d52bfe8352d4075c0d69cf4edc3',
                    'BLOCKED_IDENTITY_UNKNOWN')
            state = a.media_stat(rec['path'], rec['bytes'])
            counts[state] = counts.get(state, 0) + 1
        result.update(status='HOLD_INSUFFICIENT_TIMESTAMPS', registered_sources=32,
            source_split_registered=[20, 4, 8], source_split_scope='081 rank partition from the published frozen protocol; no protected source-to-label map read',
            optional_manifest_summary_present=manifest_seal is not None,
            current_media_metadata_counts=counts, media_stat_calls=a.media_stats,
            complete_original_continuous_media_proved=0,
            only_cut_or_reassembled_proved=0,
            natural_same_recording_LMR_candidates_proved=0,
            original_LMR_timestamps_unknown=32,
            recorded_duration_or_PTS_proof_available_in_safe_schemas=0,
            contiguity_status='NOT_PROVED_WITHIN_ALLOWED_METADATA',
            physical_recording_participant_independence='UNKNOWN',
            alternative_middle_candidate_similarity='UNKNOWN',
            interpretation='Size-matched registered archive members do not prove original natural continuity; event-plan/derived-index mixed files were not used to infer L/M/R.')
    except StopAudit as exc:
        result['status'] = str(exc)
    except (KeyError, TypeError, ValueError):
        result['status'] = 'BLOCKED_SAFE_SCHEMA'
    finally:
        result.update(files_read=a.files, bytes_read=a.bytes, denial_reason_counts=a.denials,
                      prior_content_reads_charged=prior_files,
                      prior_bytes_charged=prior_bytes,
                      current_unique_content_files=len(a.cache),
                      cpu_seconds=time.process_time()-start, content_file_cap=MAX_FILES,
                      explicit_read_cap=MAX_BYTES, private_CPU_cap=60,
                      no_media_content_reads=True, no_protected_label_reads=True,
                      evidence_categories_not_an_exhaustive_partition=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--prior-files', type=int, default=0)
    parser.add_argument('--prior-bytes', type=int, default=0)
    parser.add_argument('--known-missing', nargs='*', default=[])
    args = parser.parse_args()
    result = audit(args.root, args.files, args.prior_files, args.prior_bytes,
                   args.known_missing)
    with Path(args.out).open('x', encoding='utf-8') as stream:
        json.dump(result, stream, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
