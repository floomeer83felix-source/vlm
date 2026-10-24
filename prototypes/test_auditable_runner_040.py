"""040 new verification; six real OS cells per suite, never old tests."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest


def local(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module


b=local('benchmark_auditable_runner_040');r=b.r
ROOT=None


class Runner040Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ROOT.mkdir();(ROOT/'stores').mkdir();cls.actual=[]
        for profile in r.PROFILES:r.initialize_store(ROOT/'stores'/profile,profile)

    def real(self,family,profile):
        row=b.run_case(ROOT/self._testMethodName,ROOT/'stores'/profile,family,0,profile,'SUITE_SMOKE')
        self.actual.append(row);r.atomic(ROOT/'actual-smoke.json',self.actual)
        self.assertTrue(row['group_zero']);self.assertFalse(row['outer_kill']);self.assertLessEqual(row['wall_seconds'],5)
        return row

    def test_01_fixed_queue(self):
        q=b.fixed_queue();self.assertEqual(len(q),540)
        self.assertEqual(len({(x['profile'],x['family'],x['rep']) for x in q}),540)
        self.assertEqual([x['profile'] for x in q[:6]],list(r.PROFILES))
        self.assertEqual([x['profile'] for x in q[6:12]],list(r.PROFILES[1:]+r.PROFILES[:1]))

    def test_02_payload(self):
        self.assertEqual(len(b.payload('N1M',3)),1048576)
        self.assertEqual(b.payload('N1K',2),hashlib.shake_256(b'VLM-040/v1/N1K/2').digest(1024))
        self.assertNotEqual(b.payload('N1K',2),b.payload('N1K',3))

    def test_03_single_component_ablations(self):
        for name,changed in (('F-NOBIND','bind'),('F-NOCONSUME','consume'),('F-NOEXIT','group_exit')):
            self.assertEqual([k for k in r.POLICIES['F'] if r.POLICIES['F'][k]!=r.POLICIES[name][k]],[changed])

    def test_04_receipt_binding_negative(self):
        plan=dict(key='K',code='a'*64,config='b'*64,manifest='c'*64,payload_hash='d'*64)
        good=dict(plan,result='d'*64)
        self.assertIsNone(r.validate_receipt(plan,good,'F'))
        for key in ('key','code','config','manifest'):
            self.assertIsNotNone(r.validate_receipt(plan,dict(good,**{key:'wrong'}),'B0'))
        changed=dict(good,payload_hash='e'*64,result='e'*64)
        self.assertIsNotNone(r.validate_receipt(plan,changed,'F'))
        self.assertIsNone(r.validate_receipt(plan,changed,'F-NOBIND'))

    def test_05_sqlite_real_normal(self):
        x=self.real('N1K','B1');self.assertEqual(x['work_entered'],1);self.assertTrue(x['legal_completion'])
        self.assertEqual(x['worker_exits_json'],[0]);self.assertEqual(x['violation_count'],0)

    def test_06_cross_process_claim(self):
        x=self.real('DUP_ACTIVE','F');self.assertEqual(x['actual_requests'],2);self.assertEqual(x['work_entered'],1)
        self.assertEqual(x['requests_json'][1]['state'],'CONSUMED')
        self.assertTrue(x['evidence_json']['first_entered_before_second_request']);self.assertTrue(x['legal_completion'])

    def test_07_actual_duplicate_without_consume(self):
        x=self.real('DUP_ACTIVE','F-NOCONSUME');self.assertEqual(x['work_entered'],2)
        self.assertEqual(x['duplicate_extra'],1);self.assertIn('DUPLICATE_EXECUTION',x['violation_types'])

    def test_08_actual_crash_uncertainty(self):
        x=self.real('CRASH_AFTER_WORK','F');self.assertEqual(x['worker_exits_json'],[17])
        self.assertTrue(x['evidence_json']['work_complete_before_recovery']);self.assertEqual(x['work_entered'],1)
        self.assertTrue(x['consumed_unrecoverable']);self.assertEqual(x['terminal'],'UNKNOWN')

    def test_09_actual_descendant_admission(self):
        x=self.real('DESCENDANT_ALIVE','F-NOEXIT');self.assertEqual(x['injection'],'DELIVERED')
        self.assertTrue(x['evidence_json']['parent_exited']);self.assertTrue(x['evidence_json']['descendant_owned_job'])
        self.assertIn('PROCESS_STILL_ALIVE',x['violation_types']);self.assertTrue(x['outer_fallback'])

    def test_10_actual_byte_drift(self):
        x=self.real('INPUT_DRIFT','F-NOBIND');self.assertEqual(x['injection'],'DELIVERED')
        self.assertNotEqual(x['evidence_json']['before_hash'],x['evidence_json']['actual_read_hash'])
        self.assertEqual(x['evidence_json']['after_hash'],x['evidence_json']['actual_read_hash'])
        self.assertIn('INPUT_BINDING',x['violation_types'])

    def test_11_no_reuse_bad_cache(self):
        store=ROOT/'bad-cache';r.initialize_store(store,'F')
        plan=dict(key='cache',code='a',config='b',manifest='c',payload_hash='d')
        r.atomic(r.cache_path(store,'cache'),dict(plan,result='d',code='WRONG'))
        self.assertEqual(r.claim(store,plan,'F'),'CACHE_MISMATCH')

    def test_12_incomplete_claim_is_not_deleted(self):
        store=ROOT/'incomplete';r.initialize_store(store,'F');key='incomplete'
        path=store/(hashlib.sha256(key.encode()).hexdigest()+'.claim');path.write_bytes(b'{')
        self.assertEqual(r.claim(store,dict(key=key),'F'),'UNKNOWN_CLAIM');self.assertEqual(path.read_bytes(),b'{')


def main():
    global ROOT
    parser=argparse.ArgumentParser(description='040 stdlib API and six actual process-fault witnesses.')
    parser.add_argument('--root',required=True);args=parser.parse_args();ROOT=Path(args.root)
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Runner040Tests))
    summary=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
                 actual_cells=len(Runner040Tests.actual),smoke_wall=sum(x['wall_seconds'] for x in Runner040Tests.actual),
                 forbidden_imports=[x for x in sys.modules if x.split('.')[0] in ('torch','numpy','transformers','development_pilot_030','clock_binding_probe_038')])
    r.atomic(ROOT/'suite-summary.json',summary);print(json.dumps(summary))
    if not result.wasSuccessful():raise SystemExit(1)


if __name__=='__main__':main()
