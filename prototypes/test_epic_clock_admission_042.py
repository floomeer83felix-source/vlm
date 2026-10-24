"""Risk-focused new stdlib checks; no media, labels or network."""
from fractions import Fraction as Q
from pathlib import Path
import epic_clock_admission_042 as c

def suite(root):
    passed=[]
    def check(name,ok):c.require(ok,name);passed.append(name)
    def rejects(name,fn):
        try:fn()
        except ValueError:passed.append(name);return
        raise AssertionError(name)
    check('ties_even',round(Q(5,2))==2 and round(Q(7,2))==4)
    check('indices48',len(c.indices(60))==48 and c.indices(60)[-1]==59)
    rejects('missing_length',lambda:c.length({}))
    rejects('compressed_body',lambda:c.length({'content-length':'10','content-encoding':'gzip'}))
    rejects('per_file_budget',lambda:c.limit_length(4*c.GIB+1,32*c.GIB))
    rejects('shared_budget',lambda:c.limit_length(11,10))
    points=[(i*2,2) for i in range(100)]
    check('certified_cfr',c.qualify(points,Q(5),Q(1,10),True,True)['layer']=='CFR')
    check('unknown_origin',c.qualify(points,Q(5),Q(1,10),False,True)['clock_status']=='CLOCK_UNKNOWN')
    check('missing_duration',c.qualify([(0,0)]+points[1:],Q(5),Q(1,10),True,True)['clock_status']=='CLOCK_UNKNOWN')
    check('gap_rejected',c.qualify([(0,1)]+points[1:],Q(5),Q(1,10),True,True)['clock_status']=='CLOCK_UNKNOWN')
    # Decoded B-frame display order can pass while packet-arrival permutation fails.
    check('display_order_pass',c.qualify(points,Q(5),Q(1,10),True,True)['clock_status']=='CLOCK_CERTIFIED')
    swapped=points.copy();swapped[1],swapped[2]=swapped[2],swapped[1]
    check('packet_order_not_substitute',c.qualify(swapped,Q(5),Q(1,10),True,True)['clock_status']=='CLOCK_UNKNOWN')
    # Actual request function has a single connect/request, no retry/redirect machinery.
    class DummyResponse:
        status=302
        def getheaders(self):return [('Location','https://elsewhere.invalid')]
    calls=[]
    class DummyConnection:
        def __init__(self,*a,**kw):self.sock=self
        def connect(self):calls.append('connect')
        def settimeout(self,x):pass
        def request(self,*a,**kw):calls.append(a[0])
        def getresponse(self):return DummyResponse()
    original=c.http.client.HTTPSConnection;c.http.client.HTTPSConnection=DummyConnection
    try:
        c.request(root,dict(candidate_rank=0,media_url='https://data.bris.ac.uk/owned-test'),'HEAD',c.time.monotonic()+5)
        check('one_send_no_redirect',calls==['connect','HEAD'])
    finally:c.http.client.HTTPSConnection=original
    c.write(Path(root)/'suite.json',dict(status='PASS',assertions=passed,real_http=0))
