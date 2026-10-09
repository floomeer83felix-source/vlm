"""Read-only fixed-source label sampling translation; no scores, media, or data writes."""
import csv
import hashlib
import io
import json
import math
import os
import pathlib
import re
import sys
import zipfile
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from itertools import combinations

SHA = {
    'zip':'c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866',
    'train':'59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc',
    'test':'8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb',
    'classes':'7b95127e60300d6a69849d161869eb3e9657fa320fc9e92b6f2c9403b49c1887',
    'evaluator':'83eb3a2f30c87cc45db76235886f8d5331edb943acfdee8bab5656c5d51e0096'}
BOUNDARY=('within','crosses_end','starts_outside','invalid')
BASELINE={'train':(7985,49809,35211,252,66089),'test':(1863,16691,11664,95,31634)}


class AlignmentError(ValueError):
    """Fixed codes only; never source paths or data strings."""


def decimal_number(text):
    try:
        d=Decimal(str(text).strip())
        return d if d.is_finite() else None
    except (InvalidOperation,ValueError): return None


def sampling_points(length):
    value=float(length)
    if not math.isfinite(value): raise AlignmentError('DOUBLE_DOMAIN_UNSUPPORTED')
    # Official line 138: division precedes multiplication. No rounding/clamping.
    return tuple((j/25.0)*value for j in range(25))


def hit_indices(start,end,length):
    a,b=float(start),float(end)
    if not math.isfinite(a) or not math.isfinite(b):
        raise AlignmentError('DOUBLE_DOMAIN_UNSUPPORTED')
    return frozenset(j for j,t in enumerate(sampling_points(length)) if a<=t<=b)


def boundary_type(start,end,length):
    if any(x is None for x in (start,end,length)) or length<=0 or start<0 or start>=end:
        return 'invalid'
    if end<=length: return 'within'
    if start<length: return 'crosses_end'
    return 'starts_outside'


def geometric_counts(records):
    out=Counter(); groups=defaultdict(list)
    for c,a,b in set(records): groups[c].append((a,b))
    for events in groups.values():
        gaps=[]; ambiguous=False
        for (a,b),(s,e) in combinations(events,2):
            if b<s: gaps.append(s-b)
            elif e<a: gaps.append(a-e)
            else: ambiguous=True
        for threshold,name in ((Decimal(0),'p1_gt0'),(Decimal('0.5'),'p1_gt05'),(Decimal(1),'p1_gt1')):
            out[name]+=int(any(g>threshold for g in gaps))
        out['p1_mixed']+=int(bool(gaps) and ambiguous)
    for (c,a,b),(d,s,e) in combinations(sorted(set(records)),2):
        if c==d: continue
        out['p2_denominator']+=1
        width=min(b,e)-max(a,s)
        if width>0:
            out['p2_pairs']+=1
            out['p2_strong']+=int(width/min(b-a,e-s)>=Decimal('0.5'))
    return dict(out)


def summarize_rows(rows,classes):
    counts=Counter(); boundary=Counter({k:0 for k in BOUNDARY}); flags=Counter()
    strict_geo=Counter(); grid_geo=Counter(); associated=Counter()
    identifiers=Counter((r.get('id') or '').strip() for r in rows)
    for row in rows:
        counts['rows']+=1
        identity=(row.get('id') or '').strip()
        if not identity or identifiers[identity]!=1 or None in row:
            raise AlignmentError('ROW_IDENTITY_OR_SHAPE_UNSUPPORTED')
        length=decimal_number(row.get('length'))
        if length is None or length<=0: raise AlignmentError('ACTUAL_LENGTH_DOMAIN_UNSUPPORTED')
        official_cells=set(); strict_cells=set(); events=[]; strict_events=[]; grid_events=[]
        raw=(row.get('actions') or '').strip()
        tokens=raw.split(';') if raw else []
        if len(tokens)>1024: raise AlignmentError('ROW_TOKEN_LIMIT')
        bad_row=False
        for token in tokens:
            counts['tokens']+=1
            parts=token.split()
            if len(parts)!=3 or parts[0] not in classes:
                raise AlignmentError('ACTUAL_PARSE_OR_CLASS_UNSUPPORTED')
            c,a,b=parts; start,end=decimal_number(a),decimal_number(b)
            if start is None or end is None: raise AlignmentError('ACTUAL_TIME_DOMAIN_UNSUPPORTED')
            kind=boundary_type(start,end,length); boundary[kind]+=1
            strict=(kind=='within'); bad_row|=not strict
            points=hit_indices(a,b,row['length'])
            cells={(c,j) for j in points}
            official_cells.update(cells)
            counts['official_hit_tokens']+=int(bool(points))
            counts['official_no_hit_tokens']+=int(not points)
            counts['strict_accepted_tokens']+=int(strict)
            counts['strict_rejected_tokens']+=int(not strict)
            name='strict' if strict else 'rejected'
            counts[name+'_hit_tokens']+=int(bool(points))
            counts[name+'_no_hit_tokens']+=int(not points)
            counts['boundary_'+kind+'_hit_tokens']+=int(bool(points))
            counts['boundary_'+kind+'_no_hit_tokens']+=int(not points)
            if end>length:
                flags['end_gt_length']+=1
                counts['range_rejected_hit_tokens']+=int(bool(points))
                counts['range_rejected_no_hit_tokens']+=int(not points)
            if start>=length: flags['start_ge_length']+=1
            if start>=end: flags['start_ge_end']+=1
            if start<0: flags['start_negative']+=1
            event=(c,start,end); events.append(event)
            if strict:
                strict_events.append(event); strict_cells.update(cells)
                if points: grid_events.append(event)
        if not strict_cells<=official_cells: raise AlignmentError('CELL_SUBSET_INVARIANT')
        counts['videos_with_strict_rejected_tokens']+=int(bad_row)
        counts['official_positive_cells']+=len(official_cells)
        counts['strict_positive_cells']+=len(strict_cells)
        counts['extra_official_positive_cells']+=len(official_cells-strict_cells)
        counts['videos_with_cell_difference']+=int(official_cells!=strict_cells)
        counts['all_label_cell_denominator']+=25*len(classes)
        old,new=geometric_counts(strict_events),geometric_counts(grid_events)
        strict_geo.update(old); grid_geo.update(new)
        if bad_row:
            associated.update({k:v for k,v in old.items() if k in ('p1_gt0','p2_pairs')})
    if sum(boundary.values())!=counts['tokens'] or counts['official_hit_tokens']+counts['official_no_hit_tokens']!=counts['tokens']:
        raise AlignmentError('TOKEN_PARTITION_INVARIANT')
    return {'counts':dict(counts),'boundary':dict(boundary),'flags':dict(flags),
            'strict_geometry':dict(strict_geo),'strict_and_grid_hit_geometry':dict(grid_geo),
            'strict_geometry_in_bad_rows':dict(associated),
            'official_only_event_geometry':'NOT_COMPARABLE',
            'sampling_scope':'BINARY64_FINITE_PARSEABLE_POSITIVE_LENGTH',
            'frame_cells_exported':False}


def combine(summaries):
    result={}
    for name in ('counts','boundary','flags','strict_geometry','strict_and_grid_hit_geometry','strict_geometry_in_bad_rows'):
        c=Counter()
        for s in summaries: c.update(s[name])
        result[name]=dict(c)
    result['official_only_event_geometry']='NOT_COMPARABLE'
    return result


def public_result(raw):
    splits=('train','test','all'); result={s:{} for s in splits}
    quality_small=any(0<n<10 for s in splits for n in raw[s]['boundary'].values())
    sections=('counts','boundary','flags','strict_geometry','strict_and_grid_hit_geometry','strict_geometry_in_bad_rows')
    for section in sections:
        values={s:raw[s][section] for s in splits}
        hidden={k for s in splits for k,n in values[s].items() if 0<n<10}
        if quality_small:
            if section=='boundary': hidden.add('crosses_end')
            if section=='flags': hidden.add('end_gt_length')
            if section=='counts': hidden.update(k for k in values['all'] if k.startswith(('range_','boundary_')))
        if section=='counts':
            partitions=(('tokens','official_hit_tokens','official_no_hit_tokens'),
                        ('strict_accepted_tokens','strict_hit_tokens','strict_no_hit_tokens'),
                        ('strict_rejected_tokens','rejected_hit_tokens','rejected_no_hit_tokens'))
            for parent,a,b in partitions:
                if any(0<values[s].get(k,0)<10 for s in splits for k in (a,b)):
                    hidden.update((a,b))
            if any(0<values[s].get('videos_with_strict_rejected_tokens',0)-values[s].get('videos_with_cell_difference',0)<10 for s in splits):
                hidden.add('videos_with_cell_difference')
            if any(0<values[s].get('extra_official_positive_cells',0)<10 for s in splits):
                hidden.update(('strict_positive_cells','extra_official_positive_cells'))
        if section in ('strict_and_grid_hit_geometry','strict_geometry_in_bad_rows'):
            for s in splits:
                for k,n in values[s].items():
                    remainder=raw[s]['strict_geometry'].get(k,0)-n
                    if 0<remainder<10: hidden.add(k)
        for s in splits:
            result[s][section]={k:('WITHHELD_LT10' if 0<n<10 else 'WITHHELD_LINKED_OR_COMPLEMENTARY' if k in hidden and n>0 else n) for k,n in values[s].items()}
    for s in splits:
        for k,v in raw[s].items():
            if k not in sections: result[s][k]=v
        c=result[s]['counts']
        a,b=c.get('extra_official_positive_cells'),c.get('official_positive_cells')
        result[s]['extra_cells_fraction_of_official']=round(a/b,6) if isinstance(a,int) and isinstance(b,int) and a>=10 and b>=10 else 'WITHHELD_OR_UNDEFINED'
        n=raw[s]['counts'].get('range_rejected_hit_tokens',0)
        result[s]['range_hit_coarse_1000_bin']='WITHHELD_LT10' if 0<n<10 else [1000*(n//1000),1000*(n//1000)+999] if n>=10 else [0,0]
    result.update({k:v for k,v in raw.items() if k not in splits})
    return result


def source_patterns(text):
    compact=re.sub(r'\s+','',text)
    needed=('frames_per_video=25;','nclasses=157;',
            'timepoint=(j-1)/frames_per_video*time;',
            '(classes(k,2)<=timepoint)&&(timepoint<=classes(k,3))',
            'gtlabel(i,gtclasses{i}+1)=1;','gtcsv{headers.length}{i}',
            'uncell=@(x)x{1};')
    if not all(x in compact for x in needed): raise AlignmentError('EVALUATOR_SEMANTICS_UNKNOWN')


def choose_evaluator(infos):
    from charades_metadata_audit import safe_members
    safe_members(infos)
    found=[i for i in infos if pathlib.PurePosixPath(i.filename).name=='Charades_v1_localize.m']
    if len(found)!=1 or not 0<found[0].file_size<=256*1024:
        raise AlignmentError('EVALUATOR_ENTRY_UNKNOWN')
    return found[0]


def verified_digest(path,expected):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda:f.read(65536),b''): h.update(part)
    if h.hexdigest()!=expected: raise AlignmentError('SOURCE_SHA_MISMATCH')
    return h.hexdigest()


def audit_fixed_source():
    from charades_metadata_audit import check_ancestors
    base=pathlib.Path(os.environ['LOCALAPPDATA']).absolute()
    root=base/'VLM-Research-Isolated'/'Charades-v1-Metadata'; check_ancestors(root)
    if base.resolve(strict=True) not in root.resolve(strict=True).parents:
        raise AlignmentError('STORAGE_CONTAINMENT')
    files={'zip':root/'incoming'/'Charades.zip','train':root/'extracted'/'Charades_v1_train.csv',
           'test':root/'extracted'/'Charades_v1_test.csv','classes':root/'extracted'/'Charades_v1_classes.txt'}
    fingerprints={}
    for k,p in files.items(): check_ancestors(p); fingerprints[k]=verified_digest(p,SHA[k])
    with zipfile.ZipFile(files['zip']) as z:
        info=choose_evaluator(z.infolist())
        with z.open(info) as f: body=f.read(256*1024+1)
        if len(body)!=info.file_size or hashlib.sha256(body).hexdigest()!=SHA['evaluator']:
            raise AlignmentError('EVALUATOR_BYTES_UNKNOWN')
    source_patterns(body.decode('utf-8'))
    classes={line.split()[0] for line in files['classes'].read_text(encoding='utf-8-sig').splitlines() if line.strip()}
    if len(classes)!=157: raise AlignmentError('CLASS_COUNT')
    raw={}; headers={}
    for split in ('train','test'):
        with files[split].open('r',encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f); headers[split]=reader.fieldnames
            if not reader.fieldnames or not {'id','actions','length'}<=set(reader.fieldnames): raise AlignmentError('CSV_HEADER')
            rows=[{k:r.get(k) for k in ('id','actions','length')} | ({None:True} if None in r else {}) for r in reader]
        raw[split]=summarize_rows(rows,classes)
        c=raw[split]['counts']; g=raw[split]['strict_geometry']
        actual=(c['rows'],c['tokens'],c['strict_accepted_tokens'],g.get('p1_gt0',0),g.get('p2_pairs',0))
        if actual!=BASELINE[split]: raise AlignmentError('STRICT_BASELINE_MISMATCH')
    raw['all']=combine([raw['train'],raw['test']])
    raw.update({'fingerprints':fingerprints,'evaluator_sha256':SHA['evaluator'],'headers':headers,
                'evaluator_bytes':len(body),'central_safety':'PASS','target_crc':'PASS',
                'official_label_sampling_compatibility':'VERIFIED_WITHIN_STATED_SCOPE',
                'time_range_quality':'HOLD','event_truth':'HOLD','model_map':'NOT_COMPUTED',
                'source_writes':0,'data_downloads':0})
    return public_result(raw)


if __name__=='__main__':
    try:
        if len(sys.argv)!=1: raise AlignmentError('NO_EXTERNAL_PATH_OR_URL_ARGUMENTS')
        print(json.dumps(audit_fixed_source(),ensure_ascii=True,indent=2))
    except AlignmentError as e:
        print('ALIGNMENT_BLOCKED:'+str(e)); raise SystemExit(1) from None
    except Exception:
        print('ALIGNMENT_BLOCKED:SOURCE_OR_DOMAIN_UNVERIFIED'); raise SystemExit(1) from None
