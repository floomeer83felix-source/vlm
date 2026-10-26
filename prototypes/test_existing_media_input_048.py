"""048 bounded pure tests and independent post-exit stdlib reader.

The verify role does not import the implementation, ML libraries, or media.
Tensor equality is a worker observation, not independently reproduced here.
"""
import bisect
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time


def load(path):
    return json.loads(Path(path).read_bytes())


def hash_json(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def suite(root):
    path = Path(__file__).with_name('existing_media_input_048.py')
    spec = importlib.util.spec_from_file_location('new048', path)
    core = importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
    cfg = load(root/'config.json'); gate = {}
    core.policy(root, cfg, gate)
    assertions = 0; cases = []
    def check(ok):
        nonlocal assertions
        assertions += 1
        assert ok
    def rejected(fn):
        try:
            fn()
        except (ValueError, AttributeError, PermissionError, TypeError):
            check(True)
        else:
            check(False)
    def case(name, fn):
        try:
            fn(); cases.append(dict(name=name, status='PASS'))
        except Exception as exc:
            cases.append(dict(name=name, status='FAIL', error=type(exc).__name__))
    points = tuple(F(10)+F(i*31, 2) for i in range(96))
    normalized, indices, ni, targets = core.choose(points)
    mapping = core.RequestMap(normalized, indices, F(2))
    case('exact_ties_even', lambda: check(round(F(1, 2)) == 0 and round(F(3, 2)) == 2 and round(F(5, 2)) == 2))
    case('dynamic_endpoints_48_indices', lambda: check(len(indices) == 48 and indices[0] == 0 and indices[-1] == 95 and len(set(indices)) == 48))
    case('engineering_zero_not_origin', lambda: check(normalized[0] == 0 and points[0] != 0 and normalized[-1] == points[-1]-points[0]))
    case('hold_halfopen', lambda: check(all(normalized[i] <= u < normalized[i+1] for i, u in zip(ni, targets))))
    case('hold_exact_boundary', lambda: check(core.choose(tuple(F(i*48) for i in range(49)))[2] == tuple(range(48))))
    case('unordered_pts_refused', lambda: rejected(lambda: core.choose(tuple([F(0)]*48))))
    case('insufficient_pts_refused', lambda: rejected(lambda: core.choose(tuple(F(i) for i in range(47)))))
    case('patch_pair_mean', lambda: check(mapping.resolve(indices, 2., 2)[0] == (normalized[indices[0]]+normalized[indices[1]])/2))
    case('wrong_callback_index_refused', lambda: rejected(lambda: mapping.resolve(tuple(reversed(indices)), 2., 2)))
    case('wrong_callback_rate_refused', lambda: rejected(lambda: mapping.resolve(indices, 3., 2)))
    case('wrong_merge_refused', lambda: rejected(lambda: mapping.resolve(indices, 2., 4)))
    case('immutable_request_attribute', lambda: rejected(lambda: setattr(mapping, 'F', 99)))
    case('immutable_mapping', lambda: rejected(lambda: mapping.points.__setitem__(0, F(3))))
    case('letterbox_exact_rational', lambda: check(core.letterbox_size(640, 480) == (256, 192, 16, 0)))
    case('frame_dimension_refusal', lambda: rejected(lambda: core.letterbox_size(4097, 480)))
    def stat_compatibility():
        initial = dict(size=100, mtime_ns=200, ino=300, dev=400)
        alternate = dict(initial, dev=999)
        check(core.initial_stat_agrees(alternate, initial))
        for k in ('size', 'mtime_ns', 'ino'):
            changed = dict(initial); changed[k] += 1
            check(not core.initial_stat_agrees(changed, initial))
    case('cross_runtime_dev_same_runtime_identity', stat_compatibility)
    def budget_test():
        temporary = root/'owned-budget-fixture.txt'; temporary.write_bytes(b'abcd')
        budget_root = root/'budget-unit'; budget_root.mkdir()
        b = core.ReadBudget(budget_root, 8); m = core.Meter(temporary, b, 'unit', gate)
        try:
            check(m.read(5) == b'abcd')
            check(b.reserved == 5 and b.returned == 4)
            rejected(lambda: m.read(4))
            check(b.reserved == 5 and b.returned == 4)
        finally:
            m.close()
    case('precharge_before_read_and_no_refund', budget_test)
    case('unmetered_media_denied', lambda: rejected(lambda: Path(cfg['media']).open('rb')))
    case('unrelated_public_path_denied', lambda: rejected(lambda: path.parent.parent.joinpath('AGENTS.md').read_bytes()))
    def network_test():
        import socket
        rejected(socket.socket)
    case('network_denied', network_test)
    core.write(root/'suite.json', dict(assertions=assertions, cases=cases, passed=sum(r['status'] == 'PASS' for r in cases), failed=sum(r['status'] == 'FAIL' for r in cases)))
    print('PURE_CASES', len(cases), 'ASSERTIONS', assertions, 'FAIL', sum(r['status'] == 'FAIL' for r in cases))
    return all(r['status'] == 'PASS' for r in cases)


def verify(root):
    """Independent formulas over NEW receipts only; never opens the media."""
    cfg = load(root/'config.json')
    # The read-only scope is this new root + stdlib; no core import in this role.
    import os
    std = Path(os.__file__).parent.absolute()
    def guard(event, args):
        if event.startswith('socket.') or event in ('subprocess.Popen', 'os.system'):
            raise PermissionError('OFFLINE_VERIFY')
        if event == 'open' and not isinstance(args[0], int):
            p = Path(os.path.abspath(args[0])); mode, flags = args[1], args[2]
            writing = (isinstance(mode, str) and any(x in mode for x in 'wax+')) or (isinstance(flags, int) and flags & (os.O_CREAT | os.O_WRONLY | os.O_RDWR | os.O_TRUNC))
            allowed = p == root or root in p.parents
            if not writing:
                allowed = allowed or (std in p.parents and 'site-packages' not in p.parts)
            if not allowed:
                raise PermissionError('VERIFY_PATH')
    sys.addaudithook(guard)
    count = 0
    def check(ok):
        nonlocal count
        count += 1
        assert ok
    result = dict(status='INPUT_UNKNOWN', assertions=0, rows=[dict(arm=a, status='NOT_RUN') for a in ('B0', 'P', 'N')],
                  qualification='REAL_SCIENTIFIC_COHORT_NOT_QUALIFIED', experiment='NO_MODEL_EXPERIMENT')
    try:
        supervisor = load(root/'worker-phase.json'); check(supervisor['active'] == 0)
        if not (root/'complete.json').exists():
            if (root/'rows.json').exists():
                result['rows'] = [dict(arm=r['arm'], status='NOT_RUN' if r['status'] == 'NOT_RUN' else 'UNKNOWN_UNQUALIFIED') for r in load(root/'rows.json')]
            result['reason'] = 'WORKER_NOT_COMPLETE_NO_FINAL_BINDING'
        else:
            complete = load(root/'complete.json'); plan = load(root/'plan.json')
            frozen = load(root/'formal-seal.json'); plan_seal = load(root/'plan-seal.json')
            table = load(root/'clock-table.json'); before = load(root/'before.json'); after = load(root/'after.json')
            rows = load(root/'rows.json'); costs = load(root/'costs.json'); select = load(root/'selection.json')
            budget = load(root/'read-budget.json'); processor = load(root/'processor-complete.json')
            check(supervisor['exitcode'] == 0 and not supervisor['killed'])
            check(complete['status'] == 'CPU_REAL_MEDIA_INPUT_PASS' and after['stable'] and complete['stable'])
            check(before['stat'] == after['stat'] and before['sha256'] == after['sha256'])
            check(all(before['stat'][k] == cfg['before_stat'][k] for k in ('size', 'mtime_ns', 'ino')))
            check(hash_json(plan) == frozen['plan_sha'] == plan_seal['plan_sha'])
            check(hash_json(table) == plan['clock_table_sha'])
            raw = table['rows']; points = [F(r[0])*F(r[1]) for r in raw]
            check(table['eof'] and all(F(r[1]) > 0 for r in raw) and all(a < b for a, b in zip(points, points[1:])))
            normalized = [p-points[0] for p in points]; span = normalized[-1]; rate = F(table['average_rate'])
            check(48 <= len(raw) <= 60000 and 1200 <= span <= 1800 and rate > 0)
            expected_ix = [round(F(j*(len(raw)-1), 47)) for j in range(48)]
            targets = [F(j)*span/48 for j in range(48)]
            # Independent explicit covering-interval search, not core.choose/bisect.
            expected_ni = [next(i for i in range(len(raw)-1) if normalized[i] <= u < normalized[i+1]) for u in targets]
            check(plan['F'] == len(raw) and F(plan['T_cov']) == span and F(plan['rate']) == rate)
            check(plan['indices'] == expected_ix and plan['n_indices'] == expected_ni and plan['n_targets'] == list(map(str, targets)))
            check(plan['selected_t'] == [str(normalized[i]) for i in expected_ix])
            offset = max(abs(F(i)/rate-normalized[i]) for i in expected_ix)
            check(F(plan['max_offset']) == offset)
            check(select['frames'] == len(raw) and select['eof'] and select['buffered'] == len(set(expected_ix+expected_ni)) <= 96)
            check(select['n_duplicate_count'] == 48-len(set(expected_ni)) and select['differing_indices'] == sum(i != j for i, j in zip(expected_ix, expected_ni)))
            check(processor['calls'] == complete['calls'] == 4 and processor['load_count'] == 1 and not processor['cuda_initialized'] and processor['base_unchanged'])
            check([r['arm'] for r in rows] == ['B0', 'P', 'N'] and all(r['status'] == 'PASS' for r in rows))
            check(len(costs) == 5 and [c['stage'] for c in costs] == ['sha_pre', 'scan', 'select', 'processor', 'sha_post'])
            check(all(c['clock_domain'] == 'WORKER_LOCAL' and 0 <= c['wall'] <= {'sha_pre':60, 'scan':600, 'select':600, 'processor':300, 'sha_post':60}[c['stage']] for c in costs))
            check(all(a['end'] <= b['start'] for a, b in zip(costs, costs[1:])))
            check(budget['returned'] <= budget['reserved'] <= cfg['media_read_cap'])
            check(set(budget['phases']) == {'sha_pre', 'scan', 'select', 'sha_post'})
            check(budget['phases']['sha_pre']['returned'] == budget['phases']['sha_post']['returned'] == cfg['before_stat']['size'])
            classes = {}; public_rows = []
            for r in rows:
                arm = r['arm']; ix = list(range(48)) if arm == 'N' else expected_ix
                fps = float(F(48)/span) if arm == 'N' else float(rate)
                raw_times = [(normalized[expected_ix[j]]+normalized[expected_ix[j+1]])/2 for j in range(0,48,2)] if arm == 'P' else [(F(ix[j])+F(ix[j+1]))/(2*F.from_float(fps)) for j in range(0,48,2)]
                callback_times = list(map(float, raw_times)) if arm == 'P' else [(ix[j]/fps+ix[j+1]/fps)/2 for j in range(0,48,2)]
                check(r['raw_rational'] == list(map(str, raw_times)))
                check(len(r['callbacks']) == 1 and r['callbacks'][0]['indices'] == ix and r['callbacks'][0]['fps'] == fps and r['callbacks'][0]['merge'] == 2)
                check(r['callbacks'][0]['returned'] == callback_times)
                check(r['timecodes'] == [f'{v:.1f}' for v in callback_times])
                check(r['grid'] == [[24,12,18]] and r['visual_tokens'] == 1296 and r['roundtrip'] and r['base_unchanged'])
                check(set(r['fields']) == {'input_ids','attention_mask','pixel_values_videos','video_grid_thw'} and all(v['device'] == 'cpu' for v in r['fields'].values()))
                check(r['fields']['input_ids']['dtype'] == r['fields']['attention_mask']['dtype'] == 'torch.int64' and r['fields']['pixel_values_videos']['dtype'] == 'torch.bfloat16')
                check(r['full_hash'] == hash_json(dict(fields=r['fields'], common=frozen['base_identity'])))
                for other, equal in r['full_equal'].items():
                    found = next(x for x in rows if x['arm'] == other)
                    check(equal == (r['full_hash'] == found['full_hash']))
                if r['full_hash'] not in classes:
                    classes[r['full_hash']] = 'EQ'+str(len(classes)+1)
                public_rows.append(dict(arm=arm, status='PASS', equivalence_class=classes[r['full_hash']],
                     grid=r['grid'], visual_tokens=r['visual_tokens'], fields={k:{n:v for n,v in val.items() if n != 'sha256'} for k,val in r['fields'].items()},
                     token_length=r['fields']['input_ids']['shape'][1], roundtrip=True, base_unchanged=True,
                     visual_equal_B0=r['visual_equal_B0'], wall=r['wall']))
            check(rows[1]['visual_equal_B0'] and rows[1]['stripped'] == rows[0]['stripped'])
            check(all(r['stripped'] == rows[0]['stripped'] for r in rows))
            baseline = [F(x) for x in rows[0]['raw_rational']]
            for r, p in zip(rows, public_rows):
                p['raw_max_abs_delta_B0_seconds'] = float(max(abs(F(a)-b) for a,b in zip(r['raw_rational'], baseline)))
                p['native_timecode_difference_count_B0'] = sum(a != b for a,b in zip(r['timecodes'], rows[0]['timecodes']))
                p['classification'] = 'INPUT_EQUIVALENT_AFTER_NATIVE_QUANTIZATION' if r['arm'] == 'P' and p['equivalence_class'] == public_rows[0]['equivalence_class'] else 'CPU_INPUT_BOUNDARY_MEASURED'
            result.update(status='CPU_REAL_MEDIA_INPUT_PASS', rows=public_rows, equivalence_classes=len(classes),
                          frames=len(raw), max_index_rate_offset_seconds=float(offset), engineering_span_gate=True,
                          origin_and_annotation_bridge='NOT_CERTIFIED', n_duplicate_count=select['n_duplicate_count'],
                          n_different_indices=select['differing_indices'], processor_calls=processor['calls'], processor_loads=processor['load_count'],
                          stable_before_after=True, cuda_initialized=False, actual_model_calls=0, versions=processor['versions'],
                          media_read_returns=budget['returned'], media_read_reservations=budget['reserved'],
                          media_read_by_phase={k:{'returned':v['returned'],'reserved':v['reserved'],'seeks_demux_metadata':v['seeks']} for k,v in budget['phases'].items()},
                          worker_phase_costs=[dict(stage=c['stage'], wall=c['wall'], clock_domain='W1') for c in costs],
                          shared_select_details={k:select[k] for k in ('decoder_next_inclusive','convert','letterbox','stack')},
                          verification_scope='FORMULAS_AND_RECEIPT_BINDINGS; TENSOR_EQUALITY_WORKER_OBSERVATION_ONLY')
    except Exception as exc:
        result.update(status='INPUT_UNKNOWN', reason='INDEPENDENT_RECEIPT_CHECK_FAILED', private_exception=type(exc).__name__)
        result['rows'] = [dict(arm=a, status='UNKNOWN_UNQUALIFIED') for a in ('B0','P','N')]
    result['assertions'] = count
    (root/'post-exit.json').write_text(json.dumps(result, sort_keys=True, allow_nan=False))
    print('POST_EXIT', result['status'], 'ASSERTIONS', count)
    return result['status'] == 'CPU_REAL_MEDIA_INPUT_PASS'


if __name__ == '__main__':
    role, path = sys.argv[1:]; root = Path(path).absolute()
    sys.exit(0 if (suite(root) if role == 'suite' else verify(root)) else 1)
