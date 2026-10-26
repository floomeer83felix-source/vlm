"""New 047 verification only: owned mathematics, never a model simulator."""
import copy
import csv
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

CORE_PATH = Path(__file__).with_name('offline_evaluation_047.py')
spec = importlib.util.spec_from_file_location('evaluation047', CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


def wrap(payload):
    return dict(synthetic_fixture=True, kind=core.KIND, payload=payload)


def make_costs():
    def event(cid, kind, start, end, parent=None):
        return dict(cost_id=cid, kind=kind, parent_cost_id=parent, inclusive=True,
                    start=dict(clock_domain='FIXTURE_CLOCK_A', value=start),
                    end=dict(clock_domain='FIXTURE_CLOCK_A', value=end))
    return dict(events=[event('outer', 'run_envelope', '0', '10'),
                        event('prepare', 'shared_prepare', '0', '2', 'outer'),
                        event('generate', 'generate', '2', '8', 'outer'),
                        event('score', 'score', '8', '10', 'outer'),
                        event('letterbox', 'letterbox', '1/2', '1', 'prepare')],
                references=['prepare']*4+['generate', 'score', 'letterbox'])


def make_grid(name):
    sources, cells, registry, mapping, records = [], [], [], [], []
    seen = set()
    for i in range(1, 9):
        s = f'S{i:02}'
        sources.append(dict(source=s, stratum='HIGH_OFFSET' if i <= 6 else 'CFR', T='240', clock_id='fixture:'+s))
        for q in ('Q01', 'Q02'):
            registry.append(dict(source=s, query=q, T='240', clock_id='fixture:'+s,
                                 clock_bridge_status='UNKNOWN' if name == 'G04' and (s, q) == ('S01', 'Q01') else 'VERIFIED',
                                 question_identity_status='IDENTIFIABLE_EXISTING', answer_set_status='COMPLETE_DECLARED',
                                 valid_intervals=[['30', '60']] if name == 'G01' else [['0', '10']]))
            for a in core.ARMS:
                cells.append(dict(source=s, query=q, arm=a))
                identity_arm = 'B0' if name == 'G01' and a == 'P' else a
                material = f'fixture:input+model+generation+freshcontext:{name}:{s}:{q}:{identity_arm}'
                fp = hashlib.sha256(material.encode()).hexdigest()
                pid = 'fixture-physical:'+fp
                mapping.append(dict(source=s, query=q, arm=a, fingerprint=fp, physical_id=pid))
                if pid in seen:
                    continue
                seen.add(pid)
                state = 'FAILED' if name != 'G01' and a == 'T' else 'RETURNED'
                interval = [30, 60] if name == 'G01' else ([0, 20] if (i <= 4 and a == 'B0') or (5 <= i <= 6 and a == 'P') else [0, 10])
                raw = json.dumps(dict(start=interval[0], end=interval[1]))
                if name == 'G03' and (s, q, a) == ('S01', 'Q01', 'P'):
                    raw = '{invalid'
                records.append(dict(physical_id=pid, fingerprint=fp, state=state, raw=raw))
    return [dict(sources=sources, cells=cells), registry,
            dict(identity_kind=core.IDENTITY, rows=mapping), records, make_costs()]


def run_suite(root, contract):
    rows = []
    assertions = 0
    def check(ok, detail='assertion'):
        nonlocal assertions
        assertions += 1
        if not ok:
            raise AssertionError(detail)
    def case(cid, category, fn):
        try:
            fn()
            rows.append(dict(case_id=cid, category=category, round='initial', status='PASS', detail='', synthetic=True))
        except Exception as exc:
            rows.append(dict(case_id=cid, category=category, round='initial', status='FAIL', detail=type(exc).__name__+':'+str(exc), synthetic=True))
    for p in contract['parser_cases']:
        case(p['id'], 'parser', lambda p=p: check(core.parse_response(p['raw'], F(240))['status'] == p['expected']))
    for x in contract['interval_cases']:
        def interval_case(x=x):
            pred = tuple(F(v) for v in x['prediction'])
            gold = [tuple(map(F, g)) for g in x['gold']]
            # Independent oracle is the contract's precomputed rational constant.
            value = -core.best_match(pred, gold)[0]
            check(value == F(x['expected_iou']))
            if 'expected_hit' in x:
                check((value >= F(1, 2)) == x['expected_hit'])
        case(x['id'], 'max_single_interval_iou', interval_case)
    summaries, index = {}, {}
    for g in contract['grids']:
        name = g['id']
        data = make_grid(name)
        bundle = root/name; bundle.mkdir()
        index[name] = {}
        for field, payload in zip(('plan', 'registry', 'classes', 'records', 'costs'), data):
            b = core.packed(wrap(payload))
            path = bundle/(field+'.json'); path.write_bytes(b)
            index[name][field] = dict(path=str(path), sha256=core.sha(b))
        result = core.evaluate(*data)
        summaries[name] = core.serial(result)
        def grid_case(result=result, expected=g['expected']):
            check(result['status'] == 'EVALUATED')
            high = result['groups']['HIGH_OFFSET']
            for field in ('logical_cells', 'scorable_cells', 'scoring_unknown_cells', 'declared_input_classes', 'recorded_physical_attempts'):
                if field in expected:
                    check(result['expected_logical_cells' if field == 'logical_cells' else field] == expected[field], field)
            for arm, value in expected.get('high_arm_iou', {}).items():
                check(high['arms'][arm]['mean_iou'] == F(value), arm)
            for a, field in [('P', 'high_p_minus_b0'), ('N', 'high_n_minus_b0')]:
                if field in expected:
                    check(high['deltas'][a+'_minus_B0']['mean'] == F(expected[field]), field)
            if 'high_positive_sources' in expected:
                check(high['deltas']['P_minus_B0']['positive_sources'] == expected['high_positive_sources'])
            check(result['practical_numeric_condition'] == (None if expected['practical_numeric_trigger'] == 'UNKNOWN' else expected['practical_numeric_trigger']))
            if 'high_primary_status' in expected:
                check(high['primary_status'] == expected['high_primary_status'])
            if 'high_p_b0_hit_pairs' in expected:
                for k, v in expected['high_p_b0_hit_pairs'].items():
                    check(high['pairs']['P_B0'][k] == v)
            check(len(result['rows']) == 64)
            check(all(result['groups']['ALL']['arms'][a]['planned_questions'] == 16 for a in core.ARMS))
        case(name, 'complete_64_cell_grid', grid_case)

    def mutate(f):
        data = make_grid('G02'); f(data); return core.evaluate(*data)
    def unknown_field(field, value):
        out = mutate(lambda d: d[1][0].__setitem__(field, value))
        check(out['scoring_unknown_cells'] == 4)
        check(out['groups']['HIGH_OFFSET']['primary_status'] == 'SCORING_UNKNOWN')
        check(out['practical_numeric_condition'] is None)
    def rejected(f, kind='REJECTED_RESULT_MAP'):
        out = mutate(f); check(out['status'] == kind); check(out['expected_logical_cells'] == 64)
        check(out['practical_numeric_condition'] is None and out['scores'] is None)
    def bad_seal():
        for name in ('plan', 'registry'):
            p = root/('seal-negative-'+name+'.json')
            b = core.packed(wrap(make_grid('G02')[0 if name == 'plan' else 1]))
            expected = core.sha(b); p.write_bytes(b+b' ')
            try:
                core.load_bound(p, expected, root)
            except core.Rejected as e:
                check(str(e) == 'INPUT_SEAL_MISMATCH')
            else:
                check(False, 'seal accepted')
    def plan_faults():
        rejected(lambda d: d[0]['cells'].append(copy.deepcopy(d[0]['cells'][0])), 'REJECTED_PLAN')
        rejected(lambda d: d[0]['cells'].pop(), 'REJECTED_PLAN')
    def denominator():
        rejected(lambda d: d[0]['sources'].pop(), 'REJECTED_PLAN')
        rejected(lambda d: d[0]['cells'][0].__setitem__('query', 'Q03'), 'REJECTED_PLAN')
    def class_multiple(d):
        d[2]['rows'][1]['fingerprint'] = d[2]['rows'][0]['fingerprint']
    def physical_multiple(d):
        d[2]['rows'][1]['physical_id'] = d[2]['rows'][0]['physical_id']
    def failed_json():
        out = mutate(lambda d: d[3][0].update(state='FAILED', raw='{"start":0,"end":10}'))
        r = out['rows'][0]; check(r['run_status'] == 'FAILED' and r['score'] == 0)
    def permutation():
        data = make_grid('G02'); before = core.evaluate(*data)
        data[0]['cells'].reverse(); data[0]['sources'].reverse(); data[1].reverse(); data[2]['rows'].reverse(); data[3].reverse()
        check(before == core.evaluate(*data))
    def interval_order():
        data = make_grid('G02'); data[1][0]['valid_intervals'] = [['100', '110'], ['0', '10']]
        before = core.evaluate(*data); data[1][0]['valid_intervals'].reverse()
        check(before == core.evaluate(*data))
    def aliases():
        out = core.evaluate(*make_grid('G01'))
        check(out['expected_logical_cells'] == 64 and out['recorded_physical_attempts'] == 48 and out['declared_input_classes'] == 48)
    def sources():
        out = core.evaluate(*make_grid('G01'))
        check(out['declared_sources'] == 8 and out['independent_sources_certified'] is False and out['actual_model_calls'] == 0)
    def shared():
        out = core.costs(**dict(events=make_costs()['events'], references=make_costs()['references']))
        check(out['referenced_unique_event_durations']['prepare'] == 2)
        check(len([c for c in out['charged_event_ids'] if c == 'prepare']) == 1)
    def inclusive():
        out = core.costs(**make_costs()); check(out['outer_wall'] == 10 and out['phase_sum_if_nonoverlap'] == 10 and out['durations']['letterbox'] == F(1, 2) and out['total_latency'] == 10)
    def mixed():
        c = make_costs(); c['events'][1]['end']['clock_domain'] = 'FIXTURE_CLOCK_B'
        check(core.costs(**c)['status'] == 'COST_UNKNOWN')
        c = make_costs()
        for field in ('start', 'end'):
            c['events'][1][field]['clock_domain'] = 'FIXTURE_CLOCK_B'
        out = core.costs(**c); check(out['phase_sum_if_nonoverlap'] is None and out['outer_wall'] == 10)
    def missing_cost():
        check(core.costs([], [])['status'] == 'COST_UNKNOWN')
        c = make_costs(); c['references'].append('absent'); check(core.costs(**c)['status'] == 'COST_UNKNOWN')
    def overlapping():
        c = make_costs(); c['events'][2]['start']['value'] = '1'
        out = core.costs(**c); check(out['phase_sum_if_nonoverlap'] is None and out['outer_wall'] == 10)
    def missing_response():
        data = make_grid('G02'); data[3].pop(0); out = core.evaluate(*data)
        check(out['rows'][0]['run_status'] == 'NOT_RUN' and out['rows'][0]['score'] == 0 and out['scorable_cells'] == 64)
        data[1][0]['clock_bridge_status'] = 'UNKNOWN'; out = core.evaluate(*data)
        check(out['rows'][0]['score'] is None and out['scoring_unknown_cells'] == 4)
    def unknown_invalid():
        data = make_grid('G04'); data[3][0]['raw'] = 'invalid'
        out = core.evaluate(*data); check(out['rows'][0]['score'] is None and out['rows'][0]['scoring_status'] == 'SCORING_UNKNOWN')
    def oversize():
        parsed = core.parse_response('{"start":0,"end":10}'+' '*8192, F(240))
        check(parsed['status'] == 'INVALID' and parsed['error'] == 'RESPONSE_BYTE_LIMIT')
    faults = [lambda: unknown_field('question_identity_status', 'UNKNOWN'),
              lambda: unknown_field('answer_set_status', 'INCOMPLETE'),
              lambda: unknown_field('valid_intervals', [['0', '10'], ['20', '10']]),
              bad_seal, plan_faults, denominator,
              lambda: rejected(lambda d: d[3].append(copy.deepcopy(d[3][0]))),
              lambda: rejected(physical_multiple), lambda: rejected(class_multiple),
              failed_json, permutation, interval_order, aliases, sources, shared,
              inclusive, mixed, missing_cost, overlapping, missing_response, unknown_invalid, oversize]
    for name, fn in zip(contract['mandatory_faults'], faults):
        case(name, 'mandatory_fault', fn)
    case('C01', 'cost_fixture', inclusive)
    def extra_limits():
        for raw in ('{"start":0,"end":-Infinity}', '{"start":0,"end":1e9999}', '{"start":0,"end":10} trailing'):
            check(core.parse_response(raw, F(240))['status'] == 'INVALID')
        check(core.parse_response('{"start":0.1,"end":1}', F(240))['interval'][0] == F(*float(.1).as_integer_ratio()))
        for field, value in [('T', '241'), ('clock_id', 'other'), ('valid_intervals', [['0', '1']]*129)]:
            unknown_field(field, value)
        try:
            core.rational(str(2**4096))
        except core.Rejected:
            check(True)
        else:
            check(False)
        c = make_costs(); c['events'].append(copy.deepcopy(c['events'][0]))
        check(core.costs(**c)['status'] == 'COST_UNKNOWN')
    case('X01', 'numeric_limits_and_duplicate_cost', extra_limits)
    def guards():
        try:
            import socket
            socket.socket()
        except PermissionError:
            check(True)
        else:
            check(False, 'network guard')
        try:
            Path(__file__).parent.parent.joinpath('AGENTS.md').read_bytes()
        except (PermissionError, core.Rejected):
            check(True)
        else:
            check(False, 'unrelated path guard')
    case('X02', 'policy_denials', guards)
    # Bad map CLI fixture uses exactly the same five explicit, separately bound inputs.
    bad = make_grid('G02'); bad[3].append(copy.deepcopy(bad[3][0]))
    target = root/'BAD_MAP'; target.mkdir(); index['BAD_MAP'] = {}
    for field, payload in zip(('plan', 'registry', 'classes', 'records', 'costs'), bad):
        b = core.packed(wrap(payload)); p = target/(field+'.json'); p.write_bytes(b)
        index['BAD_MAP'][field] = dict(path=str(p), sha256=core.sha(b))
    (root/'cli-input-seals.json').write_bytes(core.packed(index))
    (root/'suite-summaries.json').write_bytes(core.packed(summaries))
    (root/'suite.json').write_bytes(core.packed(dict(synthetic=True, assertions=assertions, cases=rows,
                                                    passed=sum(r['status'] == 'PASS' for r in rows), failed=sum(r['status'] == 'FAIL' for r in rows))))
    print('CASES', len(rows), 'ASSERTIONS', assertions, 'FAIL', sum(r['status'] == 'FAIL' for r in rows))
    return not any(r['status'] == 'FAIL' for r in rows)


if __name__ == '__main__':
    root = Path(sys.argv[1]).absolute()
    contract_path = root/'contract.json'
    contract = core.strict_json(contract_path.read_bytes())
    core.audit_guard(root, [__file__, CORE_PATH])
    sys.exit(0 if run_suite(root, contract) else 1)
