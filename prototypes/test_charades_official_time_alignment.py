"""Synthetic-only sampling/quality counterexamples; never loads actual CSV or MATLAB."""
import json
import math
import unittest
import zipfile
from decimal import Decimal
from charades_official_time_alignment import (
    AlignmentError,sampling_points,hit_indices,boundary_type,geometric_counts,
    summarize_rows,combine,public_result,choose_evaluator,source_patterns)


def row(actions,length='10',identity='SYNTHETIC-ID'):
    return {'id':identity,'actions':actions,'length':length}


def safe_infos(extra=()):
    items=[zipfile.ZipInfo(n) for n in ('bundle/Charades_v1_train.csv','bundle/Charades_v1_test.csv','bundle/Charades_v1_classes.txt')]
    script=zipfile.ZipInfo('bundle/Charades_v1_localize.m'); script.file_size=100
    return items+[script]+list(extra)


class AlignmentTests(unittest.TestCase):
    def test_25_points_zero_to_24_over_25(self):
        p=sampling_points('25')
        self.assertEqual(len(p),25); self.assertEqual(p[0],0); self.assertEqual(p[-1],24)
        self.assertNotIn(25,p)

    def test_within_interval_can_map(self):
        self.assertEqual(hit_indices('2','4','25'),{2,3,4})
        self.assertEqual(boundary_type(Decimal(2),Decimal(4),Decimal(25)),'within')

    def test_end_beyond_length_still_maps_without_clamp(self):
        self.assertEqual(hit_indices('23','30','25'),{23,24})
        self.assertEqual(boundary_type(Decimal(23),Decimal(30),Decimal(25)),'crosses_end')
        s=summarize_rows([row('toy-a 23 30','25')],{'toy-a'})
        self.assertEqual(s['counts']['strict_accepted_tokens'],0)
        self.assertEqual(s['counts']['official_positive_cells'],2)

    def test_start_at_or_after_length_no_point(self):
        self.assertFalse(hit_indices('25','30','25'))
        self.assertFalse(hit_indices('26','30','25'))
        self.assertEqual(boundary_type(Decimal(25),Decimal(30),Decimal(25)),'starts_outside')

    def test_equal_endpoints_inclusive_but_bad_quality(self):
        self.assertEqual(hit_indices('3','3','25'),{3})
        self.assertEqual(boundary_type(Decimal(3),Decimal(3),Decimal(25)),'invalid')

    def test_legal_short_interval_can_miss_grid(self):
        s=summarize_rows([row('toy-a 1.01 1.02','25')],{'toy-a'})
        self.assertEqual(s['counts']['strict_accepted_tokens'],1)
        self.assertEqual(s['counts']['official_no_hit_tokens'],1)
        self.assertEqual(s['counts']['strict_positive_cells'],0)

    def test_same_class_duplicates_or_not_sum(self):
        s=summarize_rows([row('toy-a 0 2;toy-a 1 3;toy-a 0 2','25')],{'toy-a'})
        self.assertEqual(s['counts']['tokens'],3)
        self.assertEqual(s['counts']['official_positive_cells'],4)
        self.assertEqual(s['strict_geometry']['p1_gt0'],0)

    def test_different_classes_concurrent_cells(self):
        s=summarize_rows([row('toy-a 0 2;toy-b 1 3','25')],{'toy-a','toy-b'})
        self.assertEqual(s['counts']['official_positive_cells'],6)
        self.assertEqual(s['strict_geometry']['p2_pairs'],1)

    def test_zero_and_tiny_length_scope_explicit(self):
        self.assertEqual(sampling_points(0),(0.0,)*25)
        self.assertEqual(len(hit_indices(0,0,0)),25)
        self.assertEqual(len(sampling_points('0.000001')),25)
        with self.assertRaisesRegex(AlignmentError,'ACTUAL_LENGTH_DOMAIN_UNSUPPORTED'):
            summarize_rows([row('toy-a 0 1','0')],{'toy-a'})

    def test_double_order_differs_from_rearranged_decimal(self):
        l='0.1'; t=sampling_points(l)[3]
        other=(3*float(l))/25
        self.assertNotEqual(t,other)
        self.assertEqual(t,float(Decimal(3)*Decimal(l)/Decimal(25)))
        self.assertIn(3,hit_indices(str(t),str(t),l))
        self.assertFalse(t<=other<=t)

    def test_nonfinite_and_parse_unsupported_not_repaired(self):
        for bad in ('NaN','Infinity'):
            with self.assertRaises(AlignmentError): hit_indices(bad,1,10)
        for actions in ('malformed','toy-a NaN 1','unknown 0 1'):
            with self.assertRaises(AlignmentError): summarize_rows([row(actions)],{'toy-a'})
        with self.assertRaises(AlignmentError): sampling_points(math.inf)

    def test_negative_start_kernel_does_not_imply_quality(self):
        self.assertIn(0,hit_indices(-1,1,25))
        self.assertEqual(boundary_type(Decimal(-1),Decimal(1),Decimal(25)),'invalid')

    def test_geometry_baseline_and_grid_subset(self):
        s=summarize_rows([row('toy-a 0 1;toy-a 3 4;toy-a 8.01 8.02','25')],{'toy-a'})
        self.assertEqual(s['strict_geometry']['p1_gt0'],1)
        self.assertEqual(s['strict_and_grid_hit_geometry']['p1_gt0'],1)
        self.assertEqual(s['official_only_event_geometry'],'NOT_COMPARABLE')

    def test_duplicate_id_not_silently_reused(self):
        with self.assertRaisesRegex(AlignmentError,'ROW_IDENTITY_OR_SHAPE_UNSUPPORTED'):
            summarize_rows([row(''),row('')],{'toy-a'})

    def test_evaluator_unique_size_and_paths(self):
        self.assertEqual(choose_evaluator(safe_infos()).filename,'bundle/Charades_v1_localize.m')
        duplicate=zipfile.ZipInfo('other/Charades_v1_localize.m'); duplicate.file_size=100
        with self.assertRaises(AlignmentError): choose_evaluator(safe_infos([duplicate]))
        with self.assertRaises(Exception): choose_evaluator(safe_infos([zipfile.ZipInfo('../bad.m')]))
        items=safe_infos(); items[-1].file_size=256*1024+1
        with self.assertRaises(AlignmentError): choose_evaluator(items)

    def test_missing_source_formula_unknown(self):
        with self.assertRaisesRegex(AlignmentError,'EVALUATOR_SEMANTICS_UNKNOWN'):
            source_patterns('SYNTHETIC WRONG FORMULA ONLY')

    def test_output_no_identity_text_or_cell_matrix(self):
        s=summarize_rows([row('toy-a 0 1')],{'toy-a'})
        text=json.dumps(s)
        self.assertNotIn('SYNTHETIC-ID',text); self.assertNotIn('toy-a',text)
        self.assertFalse(s['frame_cells_exported'])

    def test_small_partition_and_linked_total_mask(self):
        a=summarize_rows([row('toy-a 0 2',identity='SYNTHETIC-'+str(i)) for i in range(20)],{'toy-a'})
        b=summarize_rows([row('toy-a 25 30','25',identity='SYNTHETIC-'+str(i)) for i in range(2)],{'toy-a'})
        raw={'train':a,'test':b,'all':combine([a,b])}; out=public_result(raw)
        self.assertEqual(out['test']['counts']['official_no_hit_tokens'],'WITHHELD_LT10')
        self.assertIsInstance(out['all']['counts']['official_no_hit_tokens'],str)
        self.assertIsInstance(out['train']['counts']['official_hit_tokens'],str)

    def test_subset_difference_protected_against_prior_total(self):
        a=summarize_rows([],{'toy-a'}); b=summarize_rows([],{'toy-a'})
        a['strict_geometry']['p1_gt0']=40; a['strict_and_grid_hit_geometry']['p1_gt0']=20
        b['strict_geometry']['p1_gt0']=20; b['strict_and_grid_hit_geometry']['p1_gt0']=15
        out=public_result({'train':a,'test':b,'all':combine([a,b])})
        for split in ('train','test','all'):
            self.assertIsInstance(out[split]['strict_and_grid_hit_geometry']['p1_gt0'],str)


if __name__=='__main__': unittest.main()
