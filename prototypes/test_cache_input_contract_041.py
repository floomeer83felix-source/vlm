"""New 041 assertions only; no historical suite or model invocation."""
from pathlib import Path
import cache_input_contract_041 as c

def suite(inputs,config,root):
    checks=[]
    def check(name,value):c.require(value,name);checks.append(name)
    check('queue288',len(c.queue())==288)
    check('queries576',sum(len(x['order']) for x in c.queue())==576)
    check('clean8',len(c.queue(True))==8)
    check('unique_slots',len({(x['family'],x['s'],x['order'],x['profile']) for x in c.queue()})==288)
    a,ra=inputs.prepare(inputs.raw('EXACT_VIDEO',0,'A'));b,rb=inputs.prepare(inputs.raw('EXACT_VIDEO',0,'B'))
    check('native_video_grid',ra['grid']==[[6,12,18]] and ra['visual_tokens']==324)
    check('direct_tensor_equal',inputs.equal(a,b))
    check('full_hash_equal',ra['H']==rb['H'])
    d,rd=inputs.prepare(inputs.raw('VIDEO_FPS',0,'B'))
    check('fps_direct_difference',not inputs.equal(a,d))
    check('fps_same_visual',ra['visual_hash']==rd['visual_hash'])
    check('fps_changed_text',ra['text_hash']!=rd['text_hash'])
    image,ri=inputs.prepare(inputs.raw('IMAGE_PIXEL',0,'A'))
    check('native_image_grid',ri['grid']==[[1,12,18]] and ri['visual_tokens']==54)
    check('cuda_uninitialized',not inputs.torch.cuda.is_initialized())
    check('cpu_only',all(v.device.type=='cpu' for v in a.values() if inputs.torch.is_tensor(v)))
    check('bf16_visual',str(a['pixel_values_videos'].dtype)=='torch.bfloat16')
    Instance,Cache,adapter=c.load_component(config['fixture'])
    calls=[]
    class Backend:
        def generate_until(self,requests):calls.extend(requests);return ['INPUT_SHA256:component-owned-marker']*len(requests)
    def request(text):return Instance(request_type='generate_until',arguments=(text,dict(c.GEN),lambda d:d,0,c.TASK,'test'),idx=0,metadata=dict(task=c.TASK,doc_id=0,repeats=1))
    path=Path(root)/'component.sqlite';audit=Path(root)/'component-audit.jsonl'
    cache=Cache(str(path),str(audit),task_fingerprints={c.TASK:'fixed'})
    try:
        one=cache.execute(Backend(),'generate_until',[request('same')]);two=cache.execute(Backend(),'generate_until',[request('same')])
        check('real_sqlite_hit',one==two and len(calls)==1 and cache.get_stats()['hits']==1)
        cache.execute(Backend(),'generate_until',[request('changed')]);check('text_isolation',len(calls)==2)
    finally:cache.close()
    cache=Cache(str(path),str(audit),task_fingerprints={c.TASK:'new-namespace'})
    try:cache.execute(Backend(),'generate_until',[request('same')]);check('namespace_isolation',len(calls)==3)
    finally:cache.close()
    c.write(Path(root)/'suite.json',dict(status='PASS',assertions=checks,processor_calls=inputs.calls,logging_adapter=adapter))
