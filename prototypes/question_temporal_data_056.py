"""Bounded 056 data preparation; no network, model or decoding on import.

All paths are explicit. Source joins require official annotation identities.
FEATURE_RUNTIME_UNVERIFIED: this module does not extract Qwen features.
"""
import argparse
from collections import defaultdict, Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tarfile
import time
import urllib.request
import urllib.error
import urllib.parse
import zipfile
import xml.etree.ElementTree as ET

REVISION = 'fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405'
MIB = 1024**2


def save(path, data):
    with open(path, 'x', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=2)
        f.flush(); os.fsync(f.fileno())


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(MIB), b''): h.update(block)
    return h.hexdigest()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args): return None


class Fetcher:
    def __init__(self, root):
        self.root = Path(root)
        self.ledger = self.root/'network.jsonl'
        self.records = [json.loads(x) for x in self.ledger.read_text().splitlines()] if self.ledger.exists() else []
        self.opener = urllib.request.build_opener(NoRedirect)

    def record(self, **data):
        data['at'] = time.time()
        with open(self.ledger, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
        self.records.append(data)

    def get(self, key, url, media=False, expected_size=None, expected_sha=None):
        category = 'media' if media else 'metadata'
        if any(x.get('key')==key and x['event']=='STARTED' for x in self.records):
            raise RuntimeError('CONSUMED_REQUEST')
        if media and any(x.get('category')=='media' and x['event']=='STARTED' for x in self.records):
            raise RuntimeError('MEDIA_ALREADY_ATTEMPTED')
        cap = 3*1024**3 if media else 16*MIB
        used = sum(x.get('bytes',0) for x in self.records if x.get('category')==category)
        self.record(event='STARTED', key=key, category=category, url=url)
        start=time.monotonic(); path=self.root/(key+'.partial'); final=self.root/(key+'.body')
        try:
            for hop in range(6):
                host=urllib.parse.urlsplit(url).hostname or ''
                allowed=(host in ['huggingface.co','serre.lab.brown.edu','arxiv.org','raw.githubusercontent.com','api.github.com'] or host.endswith('.hf.co') or host.endswith('.huggingface.co'))
                if not url.startswith('https://') or not allowed: raise ValueError('REDIRECT_HOST_NOT_APPROVED')
                req=urllib.request.Request(url,headers={'User-Agent':'VLM056-bounded-research','Accept-Encoding':'identity'})
                try: response=self.opener.open(req,timeout=30)
                except urllib.error.HTTPError as error: response=error
                with response:
                    status=response.code; written=0; h=hashlib.sha256()
                    with open(path,'xb') as f:
                        while True:
                            if time.monotonic()-start>(3600 if media else 180): raise TimeoutError('OUTER_TIMEOUT')
                            remaining=cap-used
                            if remaining<=0: raise RuntimeError('BODY_CAP')
                            block=response.read(min(65536,remaining))
                            if not block: break
                            used+=len(block); written+=len(block); h.update(block); f.write(block)
                            self.record(event='BODY',key=key,category=category,bytes=len(block),hop=hop)
                        f.flush(); os.fsync(f.fileno())
                    if status in (301,302,303,307,308):
                        # Small redirect body is retained; never forward credentials.
                        path.rename(self.root/(key+'.redirect'+str(hop)))
                        url=urllib.parse.urljoin(url,response.headers['Location'])
                        self.record(event='REDIRECT',key=key,category=category,url=url,status=status)
                        continue
                if status!=200: raise RuntimeError('HTTP_'+str(status))
                if expected_size is not None and written!=expected_size: raise ValueError('SIZE_MISMATCH')
                if expected_sha is not None and h.hexdigest()!=expected_sha: raise ValueError('PUBLISHER_SHA_MISMATCH')
                path.rename(final)
                self.record(event='CLOSED',key=key,category=category,bytes_object=written,sha256=h.hexdigest(),seconds=time.monotonic()-start)
                return final
            raise RuntimeError('REDIRECT_LIMIT')
        except Exception as error:
            self.record(event='FAILED',key=key,category=category,reason=str(error),seconds=time.monotonic()-start)
            raise


def acquire(root, old):
    root=Path(root); old=Path(old); total=0; copied=[]
    for name in ['dybench_annotations.body','dybench_revision.json','dybench_file_sizes.body','dybench_readme.body','timeblind_revision.json','qualification.json','network.jsonl']:
        size=(old/name).stat().st_size
        if size>2*MIB or total+size>8*MIB: raise ValueError('OLD_METADATA_LIMIT')
        body=(old/name).read_bytes(); total+=len(body)
        with open(root/('prior_'+name),'xb') as f: f.write(body)
        copied.append(dict(name=name,bytes=len(body),sha256=hashlib.sha256(body).hexdigest()))
    save(root/'prior-copies.json',dict(bytes=total,files=copied))
    client=Fetcher(root); errors={}
    requests=[('official_page','https://serre.lab.brown.edu/breakfast-actions-dataset.html'),
              ('breakfast_repo','https://huggingface.co/api/datasets/Serrelab/breakfast-actions')]
    for key,url in requests:
        try: client.get(key,url)
        except Exception as e: errors[key]=str(e)
    if (root/'breakfast_repo.body').exists():
        info=json.loads((root/'breakfast_repo.body').read_bytes()); revision=info['sha']
        save(root/'breakfast-revision.json',dict(revision=revision,files=info.get('siblings',[])))
        for name in ['README.md','SHA256SUMS','segmentation_coarse.tar.gz','segmentation_fine.tar.gz']:
            try: client.get('breakfast_'+name.replace('.','_'),'https://huggingface.co/datasets/Serrelab/breakfast-actions/resolve/'+revision+'/'+name)
            except Exception as e: errors[name]=str(e)
    try: client.get('construction','https://arxiv.org/html/2605.21988v2')
    except Exception as e: errors['construction']=str(e)
    save(root/'acquisition-status.json',dict(errors=errors))


def fixed_split(instances):
    groups=defaultdict(list)
    for row in instances: groups[row['group_key']].append(row)
    selected={x:[] for x in ['train','validation','development_test']}; skipped=[]
    caps=dict(train=96,validation=16,development_test=48)
    for key in sorted(groups,key=lambda k:hashlib.sha256(('VLM055/'+k).encode()).hexdigest()):
        bucket=int(hashlib.sha256(('VLM055/'+key).encode()).hexdigest()[:8],16)%10
        split='train' if bucket<6 else 'validation' if bucket==6 else 'development_test'
        if len(selected[split])+len(groups[key])>caps[split]: skipped.append(key)
        else: selected[split].extend(groups[key])
    return selected,skipped


def safe_annotation_members(path, remaining=64*MIB):
    """Read only regular small label members, without extracting paths."""
    result={}; total=0
    with tarfile.open(path,'r:gz') as archive:
        for item in archive:
            p=PurePosixPath(item.name)
            if p.is_absolute() or '..' in p.parts or item.issym() or item.islnk(): raise ValueError('UNSAFE_TAR')
            if not item.isfile(): continue
            total+=item.size
            if total>remaining or item.size>2*MIB: raise ValueError('ANNOTATION_EXPANSION_CAP')
            if item.name in result: raise ValueError('DUPLICATE_ANNOTATION')
            result[item.name]=archive.extractfile(item).read(item.size+1).decode('utf-8')
    return result,total


def join_breakfast(root):
    root=Path(root)
    checksums={line.split()[1]:line.split()[0] for line in (root/'breakfast_SHA256SUMS.body').read_text().splitlines()}
    expansion=0; annotations={}
    for level in ['coarse','fine']:
        name='segmentation_'+level+'.tar.gz'; path=root/('breakfast_'+name.replace('.','_')+'.body')
        if sha(path)!=checksums[name]: raise ValueError('PUBLISHER_ANNOTATION_SHA')
        content,used=safe_annotation_members(path,64*MIB-expansion); expansion+=used
        if level=='coarse': annotations=content
    xml={}
    for path,body in annotations.items():
        if path.endswith('.xml'): xml.setdefault(PurePosixPath(path).stem,[]).append((path,body))
    rows=json.loads((root/'prior_dybench_annotations.body').read_bytes())
    prior=json.loads((root/'prior_dybench_revision.json').read_text())
    if prior['revision']!=REVISION or len(rows)!=814: raise ValueError('PRIOR_IDENTITY')
    pairs=defaultdict(list)
    for row in rows:
        if row['source_subcategory']=='Breakfast': pairs[re.sub('_reversed(?=\\.mp4$)','',row['video'])].append(row)
    excluded=[]; instances=[]; joined=[]
    normalize=lambda value: ' '.join(value.replace('_',' ').split())
    for filename,pair in sorted(pairs.items()):
        reason=None; parsed=None; record=None
        if len(pair)!=2 or len(set(x['video'] for x in pair))!=2 or pair[0]['question']!=pair[1]['question']: reason='PAIR_STRUCTURE'
        else:
            parsed=re.fullmatch(r'.*\nAction 1\. (.+)\nAction 2\. (.+)\nPlease output their order\.',pair[0]['question'],re.S)
            if not parsed or normalize(parsed[1])==normalize(parsed[2]): reason='EVENT_PARSE'
        matches=xml.get(PurePosixPath(filename).stem,[])
        if not reason and len(matches)!=1: reason='ORIGINAL_RECORDING_NOT_UNIQUE'
        if not reason:
            original_path,body=matches[0]; tree=ET.fromstring(body)
            participant=tree.attrib.get('motionSequenceName','')
            match=re.fullmatch(r'(P\d+)_(cam\d+|webcam\d+|stereo\d+)_(P\d+)_(.+)',PurePosixPath(filename).stem)
            motion=tree.attrib.get('motionFile','').replace('\\','/')
            if not match or match[1]!=participant or match[3]!=participant or not motion.startswith(participant+'/') or not re.fullmatch('P(?:0[3-9]|[1-4][0-9]|5[0-4])',participant): reason='PARTICIPANT_RECORDING_CONFLICT'
            else:
                record=dict(recording=PurePosixPath(filename).stem,annotation=original_path,participant=participant,camera=match[2],motion_file=motion,group_key='Breakfast/participant='+participant)
                joined.append(record)
                segments=[dict(label=x.attrib['name'],start=int(x.attrib['startPoint']),end=int(x.attrib['endPoint'])) for x in tree.iter('MotionLabel')]
                a=[(i,x) for i,x in enumerate(segments) if normalize(x['label'])==normalize(parsed[1])]
                b=[(i,x) for i,x in enumerate(segments) if normalize(x['label'])==normalize(parsed[2])]
                if len(a)!=1 or len(b)!=1: reason='EVENT_MISSING_OR_REPEATED'
                elif abs(a[0][0]-b[0][0])<2 or not (a[0][1]['end']<b[0][1]['start'] or b[0][1]['end']<a[0][1]['start']): reason='NOT_NONADJACENT_STRICT_ORDER'
                else:
                    original=[x for x in pair if not x['video'].endswith('_reversed.mp4')]
                    reverse=[x for x in pair if x['video'].endswith('_reversed.mp4')]
                    options=['First action 1, then action 2','First action 2, then action 1']
                    if len(original)!=1 or len(reverse)!=1 or any(x['candidates']!=options for x in pair) or {x['answer'] for x in pair}!=set(options): reason='LABEL_PAIR_BINDING'
                    else:
                        yes=original[0]['answer']==options[0]
                        if (a[0][1]['start']<b[0][1]['start'])!=yes: reason='ORIGINAL_ANNOTATION_ORDER_CONFLICT'
                        else:
                            instances.append(dict(**record,videos=[original[0]['video'],reverse[0]['video']],
                                events=[parsed[1],parsed[2]],questions=[f'Does the event "{parsed[1]}" happen before the event "{parsed[2]}"? Answer Yes or No.',f'Does the event "{parsed[2]}" happen before the event "{parsed[1]}"? Answer Yes or No.'],
                                labels=[[int(yes),int(not yes)],[int(not yes),int(yes)]],segments=[a[0][1],b[0][1]],evidence='ANNOTATION_JOIN'))
        if reason: excluded.append(dict(video=filename,reason=reason))
    selected,skipped=fixed_split(instances)
    sizes={key:len(value) for key,value in selected.items()}
    groups={key:len(set(x['group_key'] for x in value)) for key,value in selected.items()}
    gate=sizes['train']>=64 and sizes['validation']>=8 and sizes['development_test']>=32 and groups['development_test']>=8
    summary=dict(status='CANDIDATE_PASS' if gate else 'SOURCE_OR_SIZE_HOLD',source_mapping='ANNOTATION_JOIN' if joined else 'UNKNOWN',
                 breakfast_pairs=len(pairs),other_category_rows=len(rows)-2*len(pairs),recording_joins=len(joined),
                 qualified_before_split=len(instances),exclusions=dict(Counter(x['reason'] for x in excluded)),
                 split_instances=sizes,split_groups=groups,groups_skipped_cap=len(skipped),annotation_expanded_bytes=expansion,
                 annotation_units='published frame indices; official release15fps; no boundaries used for sampling',
                 kitchen_independence='UNKNOWN',feature_runtime='UNVERIFIED',media_permitted=gate)
    save(root/'source-table.json',dict(records=joined,qualified=instances,excluded=excluded))
    save(root/'candidate-split.json',dict(selected=selected,skipped_groups=skipped,frozen_for_media=gate))
    save(root/'source-summary.json',summary)
    print(json.dumps(summary))


def extract_selected(archive_path, members, destination):
    destination=Path(destination); total=0; records=[]
    with zipfile.ZipFile(archive_path) as archive:
        infos=archive.infolist()
        if len(infos)>4096 or sum(len(x.filename.encode())+46+len(x.extra)+len(x.comment) for x in infos)>16*MIB: raise ValueError('DIRECTORY_LIMIT')
        names=[x.filename for x in infos]
        if len(names)!=len(set(names)): raise ValueError('DUPLICATE_ZIP_PATH')
        for x in infos:
            p=PurePosixPath(x.filename.replace('\\','/'))
            if p.is_absolute() or '..' in p.parts or ':' in x.filename or (x.external_attr>>16)&0o170000==0o120000 or x.flag_bits&1: raise ValueError('UNSAFE_ZIP')
            if x.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED): raise ValueError('COMPRESSION')
        for ordinal,name in enumerate(members):
            matches=[x for x in infos if x.filename==name]
            if len(matches)!=1: raise ValueError('MEMBER_NOT_UNIQUE')
            x=matches[0]; total+=x.file_size
            if x.file_size>64*MIB or total>2*1024**3 or x.file_size>100*max(1,x.compress_size): raise ValueError('MEMBER_LIMIT')
            target=destination/(str(ordinal)+'.mp4'); h=hashlib.sha256(); size=0
            with archive.open(x) as src,open(target,'xb') as dst:
                while True:
                    block=src.read(65536)
                    if not block: break
                    size+=len(block); h.update(block); dst.write(block)
            if size!=x.file_size: raise ValueError('EXTRACT_SIZE')
            records.append(dict(member=name,path=target.name,bytes=size,sha256=h.hexdigest(),crc=x.CRC))
    return records


def download_event(root):
    """Explicit gated, one-attempt media fetch; never called by import or join."""
    root=Path(root); candidate=json.loads((root/'source-summary.json').read_text())
    if not candidate['media_permitted']: raise RuntimeError('SOURCE_OR_SIZE_HOLD')
    import shutil
    if shutil.disk_usage(root).free<10*1024**3: raise RuntimeError('DISK_GATE')
    client=Fetcher(root)
    info=json.loads(client.get('event_identity','https://huggingface.co/api/datasets/ddz16/DyBench/tree/'+REVISION+'/video?expand=false').read_bytes())
    matches=[x for x in info if x['path']=='video/event_sequence.zip']
    if len(matches)!=1 or matches[0]['size']!=2783546023: raise ValueError('OBJECT_IDENTITY')
    content_sha=matches[0].get('lfs',{}).get('oid','')
    if not re.fullmatch('[0-9a-f]{64}',content_sha): raise ValueError('PUBLISHER_CONTENT_SHA_MISSING')
    save(root/'media-plan.json',dict(bytes=2783546023,publisher_content_sha256=content_sha,revision=REVISION))
    return client.get('event_sequence_zip','https://huggingface.co/datasets/ddz16/DyBench/resolve/'+REVISION+'/video/event_sequence.zip',media=True,expected_size=2783546023,expected_sha=content_sha)


def seal_handoff(root, cache_records):
    """Separate label files; observation records omit source IDs and labels."""
    root=Path(root); plan=json.loads((root/'candidate-split.json').read_text())
    if not plan['frozen_for_media']: raise RuntimeError('NOT_FROZEN_FOR_MEDIA')
    for split,instances in plan['selected'].items():
        observations=[]; labels=[]; failures=[]
        for i,row in enumerate(instances):
            caches=[cache_records.get(name) for name in row['videos']]
            valid=all(c and c.get('status')=='CLOSED' for c in caches)
            if not valid: failures.append(dict(index=i,status='FAILED_CACHE'))
            observations.append(dict(index=i,video_cache=[c.get('array') if c else None for c in caches],questions=row['questions'],status='CLOSED' if valid else 'FAILED_CACHE'))
            labels.append(dict(index=i,labels=row['labels']))
        save(root/(split+'-observations.json'),observations)
        save(root/(split+'-labels.json'),labels)
        save(root/(split+'-failures.json'),failures)
    save(root/'feature-runtime.json',dict(status='FEATURE_RUNTIME_UNVERIFIED',qwen_weights_opened=False))


def cache_video(path, output, frame_budget, deadline):
    """Explicit CPU decode only; nearest timestamps, unique source frames.

    Bounded linear decode keeps only 12 nearest frames, never a full-frame stream.
    This conservative implementation debits every decoded frame in frame_budget.
    """
    import av
    import numpy as np
    with av.open(str(path)) as container:
        stream=container.streams.video[0]; stream.thread_count=1
        if stream.duration is None: raise ValueError('DURATION_UNKNOWN')
        base=float(stream.start_time or 0)*float(stream.time_base)
        duration=float(stream.duration*stream.time_base)
        targets=base+(np.arange(12)+.5)*duration/12
        best=[None]*12; distance=np.full(12,np.inf); indices=[None]*12; timestamps=[None]*12
        for index,frame in enumerate(container.decode(stream)):
            frame_budget[0]+=1
            if frame_budget[0]>500000 or time.monotonic()>deadline: raise TimeoutError('DECODE_BUDGET')
            if frame.pts is None: continue
            stamp=float(frame.pts*stream.time_base); delta=np.abs(targets-stamp)
            update=np.where(delta<distance)[0]
            if len(update):
                rgb=frame.reformat(width=224,height=224,format='rgb24').to_ndarray()
                for k in update: best[k]=rgb; distance[k]=delta[k]; indices[k]=index; timestamps[k]=stamp
        if any(x is None for x in best) or len(set(indices))!=12: raise ValueError('INSUFFICIENT_UNIQUE_TIMESTEPS')
        array=np.stack(best)
        with open(output,'xb') as f: np.save(f,array,allow_pickle=False)
        return dict(shape=list(array.shape),dtype=str(array.dtype),indices=indices,timestamps=timestamps,
                    targets=targets.tolist(),time_base=str(stream.time_base),sha256=sha(output))


def prepare_cache(path, cache_root, frame_budget, deadline):
    """Exactly-once cache claim; closed exact-content results may be reused."""
    cache_root=Path(cache_root); identity=sha(path)
    claim=cache_root/(identity+'.claim'); closed=cache_root/(identity+'.json')
    array=cache_root/(identity+'.npy')
    if closed.exists():
        record=json.loads(closed.read_text())
        if record['input_sha256']!=identity or sha(array)!=record['sha256']: raise ValueError('CACHE_IDENTITY')
        return record
    if claim.exists(): raise RuntimeError('CONSUMED_CACHE_INPUT')
    save(claim,dict(status='STARTED',input_sha256=identity))
    try:
        record=cache_video(path,array,frame_budget,deadline)
        record.update(status='CLOSED',array=array.name,input_sha256=identity)
        save(closed,record)
        return record
    except Exception as error:
        save(cache_root/(identity+'.failed'),dict(status='FAILED',reason=str(error)))
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--root',required=True); parser.add_argument('--old'); parser.add_argument('--phase',choices=['acquire','join'],default='acquire')
    args=parser.parse_args()
    if args.phase=='acquire': acquire(args.root,args.old)
    else: join_breakfast(args.root)
