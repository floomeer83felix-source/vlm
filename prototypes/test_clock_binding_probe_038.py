"""New038 pure stdlib assertions; no prior suite or ML import."""
import unittest
import clock_binding_probe_038 as p


class Probe038Tests(unittest.TestCase):
    def test_01_queue(self):
        q=p.queue();self.assertEqual(len(q),48)
        self.assertEqual({x['slot'] for x in q},set(range(48)))
        self.assertEqual(len({(x['world'],x['clock'],x['channel']) for x in q}),48)

    def test_02_rotations(self):
        q=p.queue()
        self.assertEqual([(s['channel'],s['clock']) for s in q[6:12]],[('V',1),('V',2),('O',0),('O',1),('O',2),('V',0)])

    def test_03_truth(self):
        for w in range(8):
            self.assertEqual(p.truth(w,0),(8,12,4,8)[w//2]);self.assertEqual(p.truth(w,1),(12,16,8,12)[w//2])

    def test_04_shift(self):
        self.assertEqual(p.times(2),[x+60 for x in p.times(0)])
        self.assertTrue(all(p.truth(w,0)==p.truth(w,2) for w in range(8)))

    def test_05_fixed_endpoints(self):
        self.assertEqual((p.CLOCKS[0][0],p.CLOCKS[0][-1]),(p.CLOCKS[1][0],p.CLOCKS[1][-1]))
        self.assertNotEqual(p.times(0),p.times(1))

    def test_06_color_exchange(self):
        for w in range(0,8,2):
            for g in range(3):self.assertEqual(p.operands(w,g),tuple(reversed(p.operands(w+1,g))))

    def test_07_owned_pixels(self):
        raw=p.frame_bytes(0);unit=192*288*3
        self.assertEqual(len(raw),12*unit)
        for k in range(6):self.assertEqual(raw[k*2*unit:(k*2+1)*unit],raw[(k*2+1)*unit:(k*2+2)*unit])
        offset=(2*192*288+48*288+96)*3
        self.assertEqual(raw[offset:offset+3],bytes((240,32,32)))
        self.assertEqual(raw[:3],bytes((16,16,16)))

    def test_08_clock_independent_pixels(self):
        # Clock is absent from the pixel-generating function's interface.
        self.assertEqual(p.sha(p.frame_bytes(3)),p.sha(p.frame_bytes(3)))
        self.assertNotEqual(p.sha(p.frame_bytes(2)),p.sha(p.frame_bytes(3)))

    def test_09_parser(self):
        for raw,want in [('0',0),(' 012\n',12),('999',999)]:self.assertEqual(p.parse(raw),want)
        for raw in ('-1','1.0','12 seconds','answer: 8','1000','１２',''):
            self.assertIsNone(p.parse(raw))

    def test_10_templates(self):
        self.assertEqual(p.spec()['max_new_tokens'],16)
        self.assertNotIn('world',p.VIDEO_QUESTION)
        self.assertIn('64.5',p.TEXT_QUESTION.format(red=64.5,blue=72.5))

    def test_11_chain_tamper(self):
        row=dict(seq=0,prev='0'*64,event='X');row['hash']=p.digest(row)
        self.assertEqual(len(p.chain(p.packed(row)+b'\n')),1)
        row['event']='Y'
        with self.assertRaises(ValueError):p.chain(p.packed(row)+b'\n')
        with self.assertRaises(ValueError):p.chain(b'{}')

    def fixture(self):
        rows=[dict(event='TERMINAL',slot=i,state='NOT_RUN') for i in range(48)]
        return rows,dict(pid=123,exit_code=0,job_active=0),{}

    def test_12_score_complete(self):
        rows,ex,b=self.fixture();self.assertEqual(len(p.validate_closed(rows,ex,b)),48)

    def test_13_score_partial_or_active(self):
        rows,ex,b=self.fixture()
        with self.assertRaises(ValueError):p.validate_closed(rows[:-1],ex,b)
        with self.assertRaises(ValueError):p.validate_closed(rows,dict(ex,job_active=1),b)

    def test_14_duplicate_start(self):
        rows,ex,b=self.fixture();rows.extend([dict(event='STARTED',slot=0,binding='x')]*2)
        with self.assertRaises(ValueError):p.validate_closed(rows,ex,{'0':dict(full='x')})

    def test_15_binding_mismatch(self):
        rows,ex,b=self.fixture();rows.append(dict(event='STARTED',slot=0,binding='wrong'))
        with self.assertRaises(ValueError):p.validate_closed(rows,ex,{'0':dict(full='right')})

    def test_16_state_and_denominator(self):
        rows,ex,b=self.fixture();rows[0]['state']='SKIPPED'
        with self.assertRaises(ValueError):p.validate_closed(rows,ex,b)
        self.assertEqual([sum(s['channel']==ch and s['clock']==g for s in p.queue()) for ch in ('V','O') for g in range(3)],[8]*6)
