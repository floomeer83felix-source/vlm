"""039 new stdlib witnesses; no ML/old suite execution."""
import unittest
import clock_binding_components_039 as p


class Components039Tests(unittest.TestCase):
    def test_01_complete_queue(self):
        q=p.queue();self.assertEqual(len(q),120);self.assertEqual({x['slot'] for x in q},set(range(120)))
        self.assertEqual(len({(s['world'],s['clock'],s['task']) for s in q}),120)

    def test_02_rotation(self):
        self.assertEqual([(x['task'],x['clock']) for x in p.queue()[15:18]],[('SG',1),('SG',2),('SR',0)])

    def test_03_new_truth(self):
        for w in range(8):
            self.assertEqual(p.truth(w,0,'NG'),(8,16,16,8)[w//2])
            self.assertEqual(p.truth(w,1,'SG'),(6,18,18,6)[w//2])

    def test_04_signed_clock_response(self):
        for w in range(8):self.assertEqual(p.truth(w,1,'NG')-p.truth(w,0,'NG'),(-2,2,2,-2)[w//2])

    def test_05_translation_roles(self):
        for w in range(8):
            self.assertEqual(p.roles(w,2),tuple(x+600 for x in p.roles(w,0)))
            self.assertEqual(p.truth(w,0,'NG'),p.truth(w,2,'NG'))

    def test_06_role_exchange(self):
        for w in range(0,8,2):
            for g in range(3):self.assertEqual(p.roles(w,g),tuple(reversed(p.roles(w+1,g))))

    def test_07_frame_pixels(self):
        raw=p.frames(0);unit=192*288*3;self.assertEqual(len(raw),12*unit)
        for k in range(6):self.assertEqual(raw[2*k*unit:(2*k+1)*unit],raw[(2*k+1)*unit:(2*k+2)*unit])
        off=(48*288+96)*3;self.assertEqual(raw[off:off+3],bytes((240,32,32)))
        off+=4*unit;self.assertEqual(raw[off:off+3],bytes((32,64,240)))

    def test_08_montage_without_text(self):
        raw=p.frames(2);image=p.montage(2,0,False);unit=192*288*3
        self.assertEqual(len(image),384*864*3)
        for k in range(6):
            for y in (0,48,143,191):
                a=(((k//3)*192+y)*864+(k%3)*288)*3
                b=2*k*unit+y*288*3;self.assertEqual(image[a:a+864],raw[b:b+864])

    def test_09_font_definition(self):
        self.assertEqual(set(p.FONT),set('0123456789.'))
        self.assertTrue(all(len(s.split('/'))==7 and all(len(x)==5 and set(x)<=set('01') for x in s.split('/')) for s in p.FONT.values()))
        self.assertEqual(p.FONT['.'],'00000/00000/00000/00000/00000/00100/00100')

    def test_10_glyph_bounds(self):
        before=p.montage(0,2,False);after=p.montage(0,2)
        self.assertNotEqual(before,after);self.assertEqual(p.erase_label_boxes(before),p.erase_label_boxes(after))
        for k in range(6):
            for y in range(48,144):
                off=(((k//3)*192+y)*864+(k%3)*288)*3
                self.assertEqual(before[off:off+864],after[off:off+864])

    def test_11_clock_only_glyphs(self):
        a=p.montage(5,0);b=p.montage(5,1);c=p.montage(5,2)
        self.assertNotEqual(a,b);self.assertNotEqual(a,c)
        self.assertEqual(p.erase_label_boxes(a),p.erase_label_boxes(b));self.assertEqual(p.erase_label_boxes(a),p.erase_label_boxes(c))

    def test_12_gap_parser(self):
        self.assertEqual(p.parse('NG',' 08\n'),8)
        for raw in ('8 seconds','8.0','-8','８','1000','answer: 8'):self.assertIsNone(p.parse('SG',raw))

    def test_13_read_parser(self):
        self.assertEqual(p.parse('NR',' 0.5,80.5\n'),[5,805]);self.assertEqual(p.parse('SR','1.2,2.3'),[12,23])
        for raw in ('0.5, 8.5','0.50,8.5','0.5,8.5 seconds','0.5;8.5','-0.5,8.5','０.5,8.5'):self.assertIsNone(p.parse('NR',raw))

    def test_14_visual_partition(self):
        self.assertIn('pixel_values',p.VISUAL_KEYS);self.assertIn('image_grid_thw',p.VISUAL_KEYS)
        self.assertIn('pixel_values_videos',p.VISUAL_KEYS);self.assertNotIn('input_ids',p.VISUAL_KEYS)

    def fixture(self):
        return [dict(event='TERMINAL',slot=i,state='NOT_RUN') for i in range(120)],dict(pid=123,exit_code=0,job_active=0),{}

    def test_15_closure(self):
        rows,ex,b=self.fixture();self.assertEqual(len(p.validate_closed(rows,ex,b)),120)
        with self.assertRaises(ValueError):p.validate_closed(rows[:-1],ex,b)

    def test_16_job_exit(self):
        rows,ex,b=self.fixture()
        with self.assertRaises(ValueError):p.validate_closed(rows,dict(ex,job_active=1),b)

    def test_17_start_and_binding(self):
        rows,ex,b=self.fixture();rows[0]['state']='RETURNED'
        with self.assertRaises(ValueError):p.validate_closed(rows,ex,b)
        rows.append(dict(event='STARTED',slot=0,binding='bad'))
        with self.assertRaises(ValueError):p.validate_closed(rows,ex,{'0':dict(full='good')})
        rows[-1]['binding']='good';self.assertEqual(len(p.validate_closed(rows,ex,{'0':dict(full='good')})),120)
        rows.append(rows[-1])
        with self.assertRaises(ValueError):p.validate_closed(rows,ex,{'0':dict(full='good')})

    def test_18_denominators_and_tasks(self):
        self.assertEqual([sum(x['task']==task and x['clock']==g for x in p.queue()) for task in p.TASKS for g in range(3)],[8]*15)
        self.assertNotEqual(p.PROMPTS['NG'],p.PROMPTS['NR']);self.assertNotIn('{red',p.PROMPTS['SR'])

    def test_19_corrupt_chain(self):
        row=dict(seq=0,prev='0'*64,event='X');row['hash']=p.digest(row)
        row['event']='Y'
        with self.assertRaises(ValueError):p.chain(p.packed(row)+b'\n')
