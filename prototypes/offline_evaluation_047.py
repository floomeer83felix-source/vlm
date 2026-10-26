"""047 offline evaluation library/CLI. Synthetic software contracts, no inference.

Predictions: finite binary64 then exact ratios. Registry: bounded rationals.
Identity keys are externally DECLARED, never a proof of real input equivalence.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import sys
from fractions import Fraction as F
from collections import Counter

ARMS = ('B0', 'P', 'N', 'T')
KIND = 'SYNTHETIC_SOFTWARE_CONTRACT_NOT_RESEARCH_DATA'
IDENTITY = 'DECLARED_FIXTURE_IDENTITY_NOT_REAL_MODEL_INPUT'
STATES = ('RETURNED', 'INVALID', 'FAILED', 'TIMEOUT', 'NOT_RUN')


class Rejected(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise Rejected(reason)


def packed(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def unique_pairs(pairs):
    d = {}
    for k, v in pairs:
        require(k not in d, 'DUPLICATE_JSON_KEY')
        d[k] = v
    return d


def reject_constant(x):
    raise Rejected('NONFINITE_CONSTANT')


def strict_json(b, **kwargs):
    return json.loads(b, object_pairs_hook=unique_pairs,
                      parse_constant=reject_constant, **kwargs)


def rational(x):
    require(type(x) is str and len(x) <= 2500, 'RATIONAL_TYPE_OR_LENGTH')
    require(re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', x) is not None, 'RATIONAL_SYNTAX')
    v = F(x)
    require(max(abs(v.numerator).bit_length(), v.denominator.bit_length()) <= 4096,
            'RATIONAL_BIT_LIMIT')
    return v


def number(x):
    v = float(x)
    require(math.isfinite(v), 'NONFINITE_BINARY64')
    return v


def parse_response(raw, duration):
    """No substring extraction, clipping, salvage, or permissive JSON numbers."""
    try:
        require(type(raw) is str, 'RESPONSE_TYPE')
        b = raw.encode('utf-8')
        require(len(b) <= 8192, 'RESPONSE_BYTE_LIMIT')
        d = strict_json(raw, parse_int=number, parse_float=number)
        require(type(d) is dict and set(d) == {'start', 'end'}, 'RESPONSE_KEYS')
        require(all(type(d[k]) is float for k in ('start', 'end')), 'NUMBER_TYPE')
        s, e = (F(*d[k].as_integer_ratio()) for k in ('start', 'end'))
        require(0 <= s < e <= duration, 'ENDPOINT_BOUNDS')
        return {'status': 'VALID', 'interval': (s, e), 'raw_sha256': sha(b), 'error': None}
    except (ValueError, TypeError, OverflowError, UnicodeError, RecursionError) as exc:
        return {'status': 'INVALID', 'interval': None,
                'raw_sha256': sha(raw.encode('utf-8')) if type(raw) is str and not any(0xd800 <= ord(c) <= 0xdfff for c in raw) else None,
                'error': str(exc) if isinstance(exc, Rejected) else type(exc).__name__}


def interval_iou(p, g):
    overlap = max(F(0), min(p[1], g[1]) - max(p[0], g[0]))
    return overlap / ((p[1]-p[0]) + (g[1]-g[0]) - overlap)


def best_match(p, intervals):
    # Sorted endpoints make diagnostics invariant to registry ordering, including ties.
    return min(((-interval_iou(p, g), g) for g in intervals))


def key(row):
    return row['source'], row['query'], row['arm']


def validate_plan(plan):
    require(type(plan) is dict and len(plan.get('sources', [])) == 8, 'REJECTED_PLAN')
    sources = plan['sources']
    require({s['source'] for s in sources} == {f'S{i:02}' for i in range(1, 9)}, 'REJECTED_PLAN')
    for s in sources:
        i = int(s['source'][1:])
        require(s['stratum'] == ('HIGH_OFFSET' if i <= 6 else 'CFR') and
                rational(s['T']) == 240 and type(s['clock_id']) is str and bool(s['clock_id']), 'REJECTED_PLAN')
    expected = {(s['source'], q, a) for s in sources for q in ('Q01', 'Q02') for a in ARMS}
    cells = plan.get('cells', [])
    require(len(cells) == 64 and {key(c) for c in cells} == expected, 'REJECTED_PLAN')
    return expected, {s['source']: s for s in sources}


def bind_results(expected, classes, records):
    require(classes.get('identity_kind') == IDENTITY, 'REJECTED_RESULT_MAP')
    rows = classes.get('rows', [])
    require(len(rows) == 64 and {key(c) for c in rows} == expected, 'REJECTED_RESULT_MAP')
    by_key, pid_fp, fp_pid = {}, {}, {}
    for c in rows:
        fp, pid = c['fingerprint'], c['physical_id']
        require(type(fp) is str and re.fullmatch('[a-f0-9]{64}', fp) and type(pid) is str and pid,
                'REJECTED_RESULT_MAP')
        require(pid not in pid_fp or pid_fp[pid] == fp, 'REJECTED_RESULT_MAP')
        require(fp not in fp_pid or fp_pid[fp] == pid, 'REJECTED_RESULT_MAP')
        pid_fp[pid], fp_pid[fp], by_key[key(c)] = fp, pid, pid
    found = {}
    for rec in records:
        pid = rec['physical_id']
        require(pid not in found and pid in pid_fp and rec['fingerprint'] == pid_fp[pid]
                and rec['state'] in STATES, 'REJECTED_RESULT_MAP')
        found[pid] = rec
    return by_key, found, len(fp_pid)


def registry_lookup(registry):
    result = {}
    for row in registry:
        k = row.get('source'), row.get('query')
        require(k not in result, 'DUPLICATE_REGISTRY')
        result[k] = row
    return result


def eligible(g, source):
    try:
        require(g is not None, 'MISSING_REGISTRY')
        require(g.get('clock_bridge_status') == 'VERIFIED', 'CLOCK_BRIDGE_UNKNOWN')
        require(g.get('question_identity_status') == 'IDENTIFIABLE_EXISTING', 'QUESTION_IDENTITY_UNKNOWN')
        require(g.get('answer_set_status') == 'COMPLETE_DECLARED', 'ANSWER_SET_UNKNOWN')
        t = rational(g['T'])
        require(t == rational(source['T']) and g['clock_id'] == source['clock_id'], 'REGISTRY_PLAN_CLOCK_MISMATCH')
        vals = g['valid_intervals']
        require(type(vals) is list and 1 <= len(vals) <= 128, 'ANSWER_SET_SIZE')
        intervals = []
        for pair in vals:
            require(type(pair) is list and len(pair) == 2, 'GOLD_INTERVAL_SHAPE')
            s, e = map(rational, pair)
            require(0 <= s < e <= t, 'GOLD_INTERVAL_BOUNDS')
            intervals.append((s, e))
        return t, intervals, None
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
        return None, None, str(exc)


def score_cells(plan, registry, classes, records):
    expected, sources = validate_plan(plan)
    mapping, found, count = bind_results(expected, classes, records)
    reg = registry_lookup(registry)
    require(set(reg) <= {(s, q) for s, q, a in expected}, 'EXTRA_REGISTRY')
    rows = []
    for s, q, a in sorted(expected):
        rec = found.get(mapping[s, q, a], {'state': 'NOT_RUN'})
        t, intervals, error = eligible(reg.get((s, q)), sources[s])
        row = dict(source=s, query=q, arm=a, run_status=rec['state'], scoring_status='SCORING_UNKNOWN',
                   score=None, hit=None, endpoint_error=None, raw_sha256=None, reason=error)
        if type(rec.get('raw')) is str:
            try:
                row['raw_sha256'] = sha(rec['raw'].encode('utf-8'))
            except UnicodeError:
                pass
        if error is None:
            row.update(scoring_status='SCORABLE', score=F(0), hit=False)
            if rec['state'] == 'RETURNED':
                parsed = parse_response(rec.get('raw'), t)
                row.update(raw_sha256=parsed['raw_sha256'], reason=parsed['error'])
                if parsed['status'] == 'INVALID':
                    row['run_status'] = 'INVALID'
                else:
                    negative, matched = best_match(parsed['interval'], intervals)
                    row.update(score=-negative, hit=-negative >= F(1, 2), endpoint_error=
                               (abs(parsed['interval'][0]-matched[0])+abs(parsed['interval'][1]-matched[1]))/2)
        rows.append(row)
    return rows, count, len(found)


def average(values):
    return sum(values, F(0))/len(values) if values else None


def group_summary(rows, names):
    sub = [r for r in rows if r['source'] in names]
    sources = {}
    for s in names:
        sources[s] = {a: None if any(r['score'] is None for r in sub if r['source'] == s and r['arm'] == a)
                      else average([r['score'] for r in sub if r['source'] == s and r['arm'] == a]) for a in ARMS}
    arms = {}
    for a in ARMS:
        vals = [r for r in sub if r['arm'] == a]
        known = [r for r in vals if r['score'] is not None]
        legal = [r['endpoint_error'] for r in vals if r['endpoint_error'] is not None]
        arms[a] = dict(planned_questions=len(vals), scorable_questions=len(known),
                       mean_iou=None if len(known) != len(vals) else average([sources[s][a] for s in names]),
                       recall_at_half=None if len(known) != len(vals) else average([F(r['hit']) for r in vals]),
                       known_subset_descriptive=average([r['score'] for r in known]),
                       legal_endpoint_error_mean=average(legal), endpoint_error_coverage=len(legal))
    pairs, deltas = {}, {}
    lookup = {key(r): r for r in sub}
    for a in ('P', 'N'):
        c = dict(both_correct=0, correction=0, harm=0, both_wrong=0, unknown=0)
        for s in names:
            for q in ('Q01', 'Q02'):
                x, y = lookup[s, q, a]['hit'], lookup[s, q, 'B0']['hit']
                label = 'unknown' if x is None or y is None else ('both_correct' if x and y else 'correction' if x else 'harm' if y else 'both_wrong')
                c[label] += 1
        pairs[a+'_B0'] = c
        ds = [None if sources[s][a] is None or sources[s]['B0'] is None else sources[s][a]-sources[s]['B0'] for s in names]
        deltas[a+'_minus_B0'] = dict(mean=None if None in ds else average(ds),
                                   positive_sources=None if None in ds else sum(v > 0 for v in ds), per_source=dict(zip(names, ds)))
    return dict(sources=sources, arms=arms, pairs=pairs, deltas=deltas,
                primary_status='SCORING_UNKNOWN' if any(r['score'] is None for r in sub) else 'SCORABLE')


def costs(events, references):
    """Receipt arithmetic, NOT a clock synchronizer or measured-work attestation."""
    try:
        require(events and references, 'MISSING_COST')
        by_id, times = {}, {}
        for e in events:
            cid = e['cost_id']
            require(cid not in by_id, 'DUPLICATE_COST_ID')
            x, y = e['start'], e['end']
            require(type(x['clock_domain']) is str and x['clock_domain'] and x['clock_domain'] == y['clock_domain'], 'MIXED_CLOCK_ENDPOINTS')
            start, end = rational(x['value']), rational(y['value'])
            require(0 <= start <= end, 'COST_ORDER')
            by_id[cid], times[cid] = e, (x['clock_domain'], start, end)
        require(all(ref in by_id for ref in references), 'MISSING_COST_REFERENCE')
        outer = [cid for cid, e in by_id.items() if e['kind'] == 'run_envelope']
        require(len(outer) == 1 and not by_id[outer[0]].get('parent_cost_id'), 'OUTER_NOT_UNIQUE')
        root = outer[0]
        def ancestors(cid, seen):
            require(cid not in seen, 'COST_CYCLE')
            parent = by_id[cid].get('parent_cost_id')
            if parent:
                require(parent in by_id and by_id[parent].get('inclusive') is True, 'MISSING_OR_NONINCLUSIVE_PARENT')
                if times[cid][0] == times[parent][0]:
                    require(times[parent][1] <= times[cid][1] <= times[cid][2] <= times[parent][2], 'COST_OUTSIDE_PARENT')
                return ancestors(parent, seen | {cid})
            return cid
        require(all(ancestors(cid, set()) == root for cid in by_id), 'UNBOUND_COST')
        direct = [cid for cid in by_id if by_id[cid].get('parent_cost_id') == root]
        ordered = sorted(direct, key=lambda cid: times[cid][1])
        comparable = bool(ordered) and all(times[cid][0] == times[root][0] for cid in direct)
        coverage = comparable and times[ordered[0]][1] == times[root][1] and times[ordered[-1]][2] == times[root][2] and all(times[x][2] == times[y][1] for x, y in zip(ordered, ordered[1:]))
        durations = {cid: t[2]-t[1] for cid, t in times.items()}
        return dict(status='KNOWN', outer_wall=durations[root], durations=durations,
                    charged_event_ids=sorted(set(references)),
                    referenced_unique_event_durations={cid: durations[cid] for cid in sorted(set(references))},
                    phase_sum_if_nonoverlap=sum((durations[cid] for cid in direct), F(0)) if coverage else None,
                    phase_latency_status='COVERED_SAME_DECLARED_DOMAIN' if coverage else 'COST_UNKNOWN',
                    clock_synchronization='NOT_CERTIFIED_BY_DOMAIN_STRING', total_latency=durations[root])
    except (ValueError, KeyError, TypeError) as exc:
        return dict(status='COST_UNKNOWN', reason=str(exc), outer_wall=None, total_latency=None)


def evaluate(plan, registry, classes, records, cost_records):
    try:
        validate_plan(plan)
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        return dict(synthetic=True, status='REJECTED_PLAN', reason=str(exc),
                    expected_logical_cells=64, scores=None, practical_numeric_condition=None)
    try:
        rows, nclass, nphysical = score_cells(plan, registry, classes, records)
    except (ValueError, KeyError, TypeError) as exc:
        reason = str(exc)
        return dict(synthetic=True, status='REJECTED_PLAN' if 'PLAN' in reason else 'REJECTED_RESULT_MAP',
                    reason=reason, expected_logical_cells=64, scores=None, practical_numeric_condition=None)
    groups = {label: group_summary(rows, names) for label, names in
              [('HIGH_OFFSET', [f'S{i:02}' for i in range(1, 7)]), ('CFR', ['S07', 'S08']), ('ALL', [f'S{i:02}' for i in range(1, 9)])]}
    delta = groups['HIGH_OFFSET']['deltas']['P_minus_B0']
    condition = None if any(r['score'] is None for r in rows) else delta['mean'] >= F(1, 10) and delta['positive_sources'] >= 4
    return dict(synthetic=True, kind=KIND, status='EVALUATED', expected_logical_cells=64,
                declared_sources=8, independent_sources_certified=False, actual_model_calls=0,
                declared_input_classes=nclass, recorded_physical_attempts=nphysical, identity_kind=IDENTITY,
                scorable_cells=sum(r['score'] is not None for r in rows),
                scoring_unknown_cells=sum(r['score'] is None for r in rows),
                run_status_counts=dict(Counter(r['run_status'] for r in rows)), rows=rows, groups=groups,
                practical_numeric_condition=condition, scientific_go='NOT_GRANTED',
                costs=costs(cost_records.get('events'), cost_records.get('references')))


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def audit_guard(root, modules):
    """Cooperative local policy, not adversarial isolation certification."""
    root = Path(root).absolute()
    stdlib = Path(os.__file__).parent.absolute()
    exact = {Path(p).absolute() for p in modules}
    def under(p, base):
        return p == base or base in p.parents
    def audit(event, args):
        if event.startswith(('socket.', 'subprocess.', 'os.system', 'os.spawn')):
            raise PermissionError('047_NETWORK_OR_CHILD_DENIED')
        if event in ('os.listdir', 'os.scandir'):
            raise PermissionError('047_ENUMERATION_DENIED')
        if event == 'open' and not isinstance(args[0], int):
            p = Path(os.path.abspath(args[0]))
            mode, flags = args[1], args[2]
            write = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)))
            allowed_stdlib = under(p, stdlib) and 'site-packages' not in p.parts
            require(under(p, root) if write else (under(p, root) or p in exact or allowed_stdlib), '047_PATH_DENIED')
    sys.addaudithook(audit)


def load_bound(path, digest, root):
    p, root = Path(path).absolute(), Path(root).absolute()
    require(root in p.parents and re.fullmatch('[0-9a-f]{64}', digest), 'INPUT_PATH_OR_HASH')
    for node in [p, *list(p.parents)[:list(p.parents).index(root)+1]]:
        st = node.lstat()
        require(not (getattr(st, 'st_file_attributes', 0) & 1024) and not node.is_symlink(), 'INPUT_LINK')
    require(p.is_file() and p.stat().st_size <= 4*1024**2, 'INPUT_SIZE_OR_TYPE')
    b = p.read_bytes()
    require(len(b) <= 4*1024**2 and sha(b) == digest, 'INPUT_SEAL_MISMATCH')
    d = strict_json(b)
    require(d.get('synthetic_fixture') is True and d.get('kind') == KIND, 'SYNTHETIC_ONLY')
    return d['payload']


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    for name in ('plan', 'registry', 'classes', 'records', 'costs'):
        parser.add_argument('--'+name, nargs=2, metavar=('EXACT_PATH', 'SHA256'), required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    audit_guard(args.root, [__file__])
    out = Path(args.output).absolute()
    require(Path(args.root).absolute() in out.parents and not out.exists(), 'OUTPUT_MUST_BE_NEW')
    out.mkdir()
    try:
        data = [load_bound(*getattr(args, n), args.root) for n in ('plan', 'registry', 'classes', 'records', 'costs')]
        result = evaluate(*data)
    except (ValueError, OSError) as exc:
        result = dict(synthetic=True, status='REJECTED_INPUT', reason=str(exc), expected_logical_cells=64,
                      scores=None, practical_numeric_condition=None)
    result['input_seals'] = {n: getattr(args, n)[1] for n in ('plan', 'registry', 'classes', 'records', 'costs')}
    result['code_sha256'] = sha(Path(__file__).read_bytes())
    (out/'summary.json').write_bytes(packed(serial(result))+b'\n')
    fields = ['source', 'query', 'arm', 'run_status', 'scoring_status', 'score', 'hit', 'endpoint_error', 'raw_sha256', 'reason']
    with (out/'cells.csv').open('x', newline='', encoding='utf-8') as h:
        w = csv.DictWriter(h, fieldnames=fields); w.writeheader()
        for row in result.get('rows', []):
            w.writerow(serial(row))
    print(result['status'])


if __name__ == '__main__':
    cli()
