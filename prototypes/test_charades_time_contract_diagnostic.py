"""SYNTHETIC ONLY; no real CSV, paths, identities, network or dataset changes."""
import hashlib
import io
import json
import unittest
from unittest import mock
from decimal import Decimal
from charades_time_contract_diagnostic import (
    ABS, REL, DiagnosticError, number, bucket, token_flags, row_qualification,
    summarize_rows, parse_csv, merge_summaries, mask_partition, disclose, digest_file)


def toy_row(actions='',length='10',identity='SYNTHETIC-ROW'):
    return {'id':identity,'actions':actions,'length':length}


class DiagnosticTests(unittest.TestCase):
    def test_absolute_bucket_endpoints(self):
        bounds=('0.1','1','5','30')
        for value,expected in (('0.1',ABS[0]),('0.1001',ABS[1]),('1',ABS[1]),('5',ABS[2]),('30',ABS[3]),('30.001',ABS[4])):
            self.assertEqual(bucket(Decimal(value),bounds,ABS),expected)
        with self.assertRaises(DiagnosticError): bucket(Decimal(0),bounds,ABS)

    def test_relative_bucket_endpoints(self):
        for value,index in (('0.01',0),('0.01001',1),('0.1',1),('0.1001',2),('1',2),('1.01',3)):
            self.assertEqual(bucket(Decimal(value),('0.01','0.1','1'),REL),REL[index])

    def test_bad_lengths_nonfinite_and_parse(self):
        self.assertIsNone(number('NaN')); self.assertIsNone(number('Infinity'))
        for length in (None,Decimal(0),Decimal(-1)):
            flags,_=token_flags('toy-class 0 1',length,{'toy-class'})
            self.assertIn('length',flags)
        flags,_=token_flags('toy-class NaN 1',Decimal(10),{'toy-class'})
        self.assertIn('time',flags)
        s=summarize_rows([toy_row('toy-class NaN 20')],{'toy-class'})
        self.assertEqual(s['flags']['range'],1)
        self.assertEqual(s['end_range_position']['start_unknown'],1)
        flags,event=token_flags('malformed',Decimal(10),{'toy-class'})
        self.assertEqual(flags,{'parse'}); self.assertIsNone(event)

    def test_primary_mutually_exclusive_flags_nonexclusive(self):
        s=summarize_rows([toy_row('unknown -1 20')],{'toy-class'})
        self.assertEqual(sum(s['primary'].values()),1)
        self.assertEqual(s['primary']['class'],1)
        self.assertEqual(s['flags']['negative'],1)
        self.assertEqual(s['flags']['range'],1)
        self.assertEqual(s['counts']['invalid'],1)
        self.assertEqual(sum(s['flags'].values()),3)

    def test_end_range_position_and_delta(self):
        s=summarize_rows([toy_row('toy-class 11 12;toy-class 2 11')],{'toy-class'})
        self.assertEqual(s['end_range_position']['start_gt_length'],1)
        self.assertEqual(s['end_range_position']['start_le_length_lt_end'],1)
        self.assertEqual(sum(s['delta_seconds'].values()),2)
        self.assertEqual(s['delta_seconds']['(0.1,1]'],1)

    def test_p1_gap_repeat_touch_and_mixed(self):
        events=[('toy-class',Decimal(0),Decimal(1)),('toy-class',Decimal(1),Decimal(2)),
                ('toy-class',Decimal(4),Decimal(5)),('toy-class',Decimal(4),Decimal(5))]
        q=row_qualification(events)
        self.assertEqual(q['unique_valid'],3)
        self.assertEqual((q['p1_gt0'],q['p1_gt05'],q['p1_gt1'],q['p1_mixed']),(1,1,1,1))
        self.assertEqual(row_qualification(events[:2])['p1_gt0'],0)

    def test_p2_concurrency_strong_and_touch(self):
        q=row_qualification([('toy-a',Decimal(0),Decimal(4)),('toy-b',Decimal(1),Decimal(2)),('toy-c',Decimal(4),Decimal(5))])
        self.assertEqual(q['p2_pair_denominator'],3)
        self.assertEqual(q['p2_pairs'],1); self.assertEqual(q['p2_strong'],1)

    def test_invalid_row_association_without_repair(self):
        s=summarize_rows([toy_row('toy-a 0 1;toy-a 3 4;toy-b 0 4;toy-b 0 20')],{'toy-a','toy-b'})
        self.assertEqual(s['counts']['p1_gt0'],1)
        self.assertEqual(s['counts']['p1_gt0_in_invalid_rows'],1)
        self.assertEqual(s['counts']['p2_pairs_in_invalid_rows'],2)
        self.assertEqual(s['counts']['valid'],3)
        self.assertEqual(s['counts']['invalid'],1)

    def test_split_denominators_and_empty_no_fake_mean(self):
        a=summarize_rows([toy_row('toy-a 0 1')],{'toy-a'})
        b=summarize_rows([toy_row('toy-a 0 20')],{'toy-a'})
        total=merge_summaries([a,b])
        self.assertEqual(total['counts']['rows'],2)
        self.assertEqual(total['counts']['tokens'],2)
        self.assertEqual(total['counts']['invalid'],1)
        self.assertIsNone(summarize_rows([],set())['length_summary']['mean_seconds'])

    def test_duplicate_identity_block_not_output(self):
        rows=[toy_row('toy-a 0 1;toy-a 3 4'),toy_row('toy-a 0 1;toy-a 3 4')]
        s=summarize_rows(rows,{'toy-a'})
        self.assertEqual(s['counts']['qualification_blocked_rows'],2)
        self.assertEqual(s['counts'].get('p1_gt0',0),0)
        self.assertNotIn('SYNTHETIC-ROW',json.dumps(s))

    def test_header_and_free_text_not_in_aggregate(self):
        header,rows=parse_csv('id,subject,actions,length,script\nSYNTHETIC-ID,SYNTHETIC-SUBJECT,toy-a 0 1,10,SYNTHETIC-TEXT\n')
        out=json.dumps(summarize_rows(rows,{'toy-a'}))
        for secret in ('SYNTHETIC-ID','SYNTHETIC-SUBJECT','SYNTHETIC-TEXT','toy-a'):
            self.assertNotIn(secret,out)
        self.assertIn('actions',header)
        with self.assertRaises(DiagnosticError): parse_csv('id,actions\n')

    def test_sha_mismatch_stops_without_network(self):
        p=mock.Mock(); p.open.side_effect=lambda mode:io.BytesIO(b'SYNTHETIC-BYTES')
        self.assertEqual(digest_file(p),hashlib.sha256(b'SYNTHETIC-BYTES').hexdigest())
        with self.assertRaisesRegex(DiagnosticError,'SHA_MISMATCH'):
            digest_file(p,'0'*64)
        p.open.assert_called_with('rb')

    def test_complementary_suppression_preserves_zero(self):
        out=mask_partition({'tiny':2,'large':30,'zero':0})
        self.assertEqual(out['tiny'],'WITHHELD_LT10')
        self.assertEqual(out['large'],'WITHHELD_COMPLEMENTARY')
        self.assertEqual(out['zero'],0)

    def test_linked_split_and_total_masks_cannot_subtract_small_cell(self):
        a=summarize_rows([toy_row('toy-a 0 11',identity='SYNTHETIC-'+str(i)) for i in range(20)],{'toy-a'})
        b=summarize_rows([toy_row('toy-a 0 10.01',identity='SYNTHETIC-'+str(i)) for i in range(2)],{'toy-a'})
        raw={'train':a,'test':b,'all':merge_summaries([a,b])}
        out=disclose(raw)
        self.assertEqual(out['test']['delta_seconds']['(0,0.1]'],'WITHHELD_LT10')
        self.assertIsInstance(out['all']['delta_seconds']['(0,0.1]'],str)
        self.assertIsInstance(out['train']['delta_seconds']['(0.1,1]'],str)

    def test_subset_complement_and_linked_totals_protect_small_remainder(self):
        a=summarize_rows([],set()); b=summarize_rows([],set())
        a['counts'].update({'p1_gt1':100,'p1_gt1_in_invalid_rows':50})
        b['counts'].update({'p1_gt1':40,'p1_gt1_in_invalid_rows':35})
        out=disclose({'train':a,'test':b,'all':merge_summaries([a,b])})
        for split in ('train','test','all'):
            self.assertIsInstance(out[split]['counts']['p1_gt1_in_invalid_rows'],str)
        self.assertEqual(out['test']['counts']['p1_gt1'],40)


if __name__=='__main__': unittest.main()
