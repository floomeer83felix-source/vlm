"""Fixed-location, read-only metadata diagnostic. No networking, media, or data writes."""
import csv
import hashlib
import io
import json
import os
import pathlib
import sys
import zipfile
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from itertools import combinations

EXPECTED_SHA = {
    "zip": "c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866",
    "train": "59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc",
    "test": "8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb"}
PRIMARY = ("parse", "length", "time", "class", "negative", "order", "range", "OK")
ABS = ("(0,0.1]", "(0.1,1]", "(1,5]", "(5,30]", ">30")
REL = ("(0,0.01]", "(0.01,0.1]", "(0.1,1]", ">1")
HIST = ("0", "1", "2-3", "4-7", "8+")
REFERENCES = {
    "train": {"rows": 7985, "tokens": 49809, "valid": 35211, "invalid": 14598,
              "rows_invalid": 5896, "p1_gt0": 252, "p1_gt05": 227, "p1_gt1": 206,
              "p1_videos": 215, "p1_mixed": 52, "p2_pairs": 66089, "p2_strong": 49454,
              "p2_pair_denominator": 96802, "p2_videos": 6407},
    "test": {"rows": 1863, "tokens": 16691, "valid": 11664, "invalid": 5027,
             "rows_invalid": 1537, "p1_gt0": 95, "p1_gt05": 86, "p1_gt1": 82,
             "p1_videos": 77, "p1_mixed": 24, "p2_pairs": 31634, "p2_strong": 24059,
             "p2_pair_denominator": 45696, "p2_videos": 1612}}


class DiagnosticError(ValueError):
    """Use only non-identifying constant codes."""


def number(value):
    try:
        d = Decimal(str(value).strip())
        return d if d.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


def bucket(value, bounds, names):
    if value <= 0:
        raise DiagnosticError("NONPOSITIVE_BUCKET_INPUT")
    for limit, name in zip(bounds, names):
        if value <= Decimal(limit):
            return name
    return names[-1]


def token_flags(token, length, classes):
    fields = token.split()
    if len(fields) != 3:
        return {"parse"}, None
    label, a, b = fields
    start, end = number(a), number(b)
    flags = set()
    if length is None or length <= 0: flags.add("length")
    if start is None or end is None: flags.add("time")
    if label not in classes: flags.add("class")
    if start is not None and start < 0: flags.add("negative")
    if start is not None and end is not None and start >= end: flags.add("order")
    if end is not None and length is not None and length > 0 and end > length: flags.add("range")
    return flags, (label, start, end)


def row_qualification(records):
    """Independent arithmetic; never imports the previous range/qualification code."""
    result = Counter()
    by_class = defaultdict(list)
    for label, start, end in set(records):
        by_class[label].append((start, end))
    result["valid_groups"] = len(by_class)
    result["unique_valid"] = len(set(records))
    for intervals in by_class.values():
        if len(intervals) < 2: continue
        result["sameclass_multi_groups"] += 1
        gaps, ambiguous = [], False
        for (a, b), (s, e) in combinations(intervals, 2):
            if b < s: gaps.append(s-b)
            elif e < a: gaps.append(a-e)
            else: ambiguous = True
        for threshold, key in ((Decimal(0), "p1_gt0"), (Decimal('0.5'), "p1_gt05"), (Decimal(1), "p1_gt1")):
            if any(g > threshold for g in gaps): result[key] += 1
        if gaps and ambiguous: result["p1_mixed"] += 1
    result["p1_videos"] = int(result["p1_gt0"] > 0)
    classes_with_overlap = set()
    for (c, a, b), (k, s, e) in combinations(sorted(set(records)), 2):
        if c == k: continue
        result["p2_pair_denominator"] += 1
        width = min(b, e)-max(a, s)
        if width <= 0: continue
        result["p2_pairs"] += 1
        classes_with_overlap.add(tuple(sorted((c,k))))
        if width/min(b-a,e-s) >= Decimal('0.5'): result["p2_strong"] += 1
    result["p2_videos"] = int(result["p2_pairs"] > 0)
    result["p2_classpair_groups"] = len(classes_with_overlap)
    return result


def summarize_rows(rows, classes):
    counts, primary, flags = Counter(), Counter({k:0 for k in PRIMARY}), Counter({k:0 for k in PRIMARY if k!="OK"})
    absolute, relative = Counter({k:0 for k in ABS}), Counter({k:0 for k in REL})
    position = Counter({k:0 for k in ("start_gt_length", "start_le_length_lt_end", "start_unknown")})
    severity = Counter({k:0 for k in HIST})
    ids = Counter((r.get("id") or "").strip() for r in rows)
    lengths = []
    for row in rows:
        counts["rows"] += 1
        length = number(row.get("length"))
        if length is None or length <= 0: counts["length_invalid_rows"] += 1
        else: lengths.append(length)
        raw = (row.get("actions") or "").strip()
        pieces = raw.split(';') if raw else []
        if len(pieces)>1024: raise DiagnosticError("ROW_TOKEN_LIMIT")
        invalid, valid = 0, []
        for token in pieces:
            counts["tokens"] += 1
            bad, event = token_flags(token,length,classes)
            flags.update(bad)
            main = next((k for k in PRIMARY if k in bad), "OK")
            primary[main] += 1
            if bad: invalid += 1; counts["invalid"] += 1
            else: counts["valid"] += 1; valid.append(event)
            if "range" in bad:
                _,start,end = event
                delta=end-length
                absolute[bucket(delta,('0.1','1','5','30'),ABS)] += 1
                relative[bucket(delta/length,('0.01','0.1','1'),REL)] += 1
                key="start_unknown" if start is None else "start_gt_length" if start>length else "start_le_length_lt_end"
                position[key] += 1
        counts["rows_invalid"] += int(invalid>0)
        key="0" if invalid==0 else "1" if invalid==1 else "2-3" if invalid<4 else "4-7" if invalid<8 else "8+"
        severity[key] += 1
        identity=(row.get("id") or "").strip()
        if not identity or ids[identity]!=1 or None in row:
            counts["qualification_blocked_rows"] += 1
            continue
        q=row_qualification(valid)
        counts.update(q)
        if invalid:
            for name in ("p1_gt0","p1_gt05","p1_gt1","p1_videos","p1_mixed","p2_pairs","p2_strong","p2_videos","p2_classpair_groups"):
                counts[name+"_in_invalid_rows"] += q[name]
    if sum(primary.values())!=counts["tokens"] or counts["valid"]+counts["invalid"]!=counts["tokens"]:
        raise DiagnosticError("DENOMINATOR_INVARIANT")
    ordered=sorted(lengths)
    med=None if not ordered else (ordered[(len(ordered)-1)//2]+ordered[len(ordered)//2])/2
    return {"counts":dict(counts),"primary":dict(primary),"flags":dict(flags),
            "delta_seconds":dict(absolute),"delta_ratio":dict(relative),"end_range_position":dict(position),
            "video_invalid_tokens":dict(severity),"length_summary":{"valid_rows":len(ordered),
            "mean_seconds":None if not ordered else round(float(sum(ordered)/len(ordered)),1),
            "median_seconds":None if med is None else round(float(med),1)},
            "primary_sum_equals_tokens":True,"flags_are_nonexclusive":True}


def parse_csv(text):
    reader=csv.DictReader(io.StringIO(text,newline=''))
    header=reader.fieldnames
    if not header or len(header)!=len(set(header)) or not {'id','actions','length','subject'}<=set(header):
        raise DiagnosticError("HEADER_CONTRACT")
    try:
        rows=[{k:r.get(k) for k in ('id','actions','length')} | ({None:True} if None in r else {}) for r in reader]
    except csv.Error:
        raise DiagnosticError("CSV_PARSE") from None
    return header,rows


def merge_summaries(summaries):
    result={}
    for key in ('counts','primary','flags','delta_seconds','delta_ratio','end_range_position','video_invalid_tokens'):
        c=Counter()
        for summary in summaries: c.update(summary[key])
        result[key]=dict(c)
    result['primary_sum_equals_tokens']=True
    result['flags_are_nonexclusive']=True
    return result


def mask_partition(values,force=False,exclude=()):
    out=dict(values)
    small={k for k,n in values.items() if 0<n<10}
    for k in small: out[k]='WITHHELD_LT10'
    candidates=[k for k,n in values.items() if n>=10 and k not in exclude]
    if (len(small)==1 or force) and candidates:
        k=max(candidates,key=lambda k:values[k]); out[k]='WITHHELD_COMPLEMENTARY'
    elif len(small)==1 and not candidates:
        for k,n in values.items():
            if n>0: out[k]='WITHHELD'
    return out


def disclose(raw):
    """Protect linked margins, including histograms revealing suppressed range totals."""
    splits=('train','test','all')
    sensitive=any(0<n<10 for split in splits for n in raw[split]['flags'].values())
    masks={}
    for key in ('counts','primary','flags','delta_seconds','delta_ratio','end_range_position','video_invalid_tokens'):
        values={split:raw[split][key] for split in splits}
        hidden={name for split in splits for name,n in values[split].items() if 0<n<10}
        if key=='counts':
            for split in splits:
                for name,n in values[split].items():
                    suffix='_in_invalid_rows'
                    if name.endswith(suffix):
                        remainder=values[split].get(name[:-len(suffix)],0)-n
                        if 0<remainder<10: hidden.add(name)
        if key=='flags' and sensitive: hidden.add('range')
        force=sensitive and key in ('delta_seconds','delta_ratio','end_range_position')
        exclude={'OK','0'} if key in ('primary','video_invalid_tokens') else set()
        if (key!='counts' and key!='flags') and (len(hidden)==1 or force):
            candidates=[name for name,n in values['all'].items() if n>=10 and name not in hidden and name not in exclude]
            if candidates: hidden.add(max(candidates,key=lambda name:values['all'][name]))
            elif hidden: hidden.update(name for name,n in values['all'].items() if n>0)
        masks[key]=hidden
    result={}
    for split,data in raw.items():
        if split not in ('train','test','all'): continue
        d={}
        for key,value in data.items():
            if key in masks:
                d[key]={k:('WITHHELD_LT10' if 0<n<10 else 'WITHHELD_LINKED_OR_COMPLEMENTARY' if k in masks[key] and n>0 else n) for k,n in value.items()}
            else: d[key]=value
        result[split]=d
    result.update({k:v for k,v in raw.items() if k not in ('train','test','all')})
    return result


def digest_file(path,expected=None):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda:f.read(65536),b''): h.update(part)
    actual=h.hexdigest()
    if expected is not None and actual!=expected: raise DiagnosticError("SHA_MISMATCH")
    return actual


def audit_fixed_storage():
    # Safety only; independent parser, token predicates and pair arithmetic above.
    from charades_metadata_audit import check_ancestors
    base=pathlib.Path(os.environ['LOCALAPPDATA']).absolute()
    root=base/'VLM-Research-Isolated'/'Charades-v1-Metadata'
    check_ancestors(root)
    if base.resolve(strict=True) not in root.resolve(strict=True).parents:
        raise DiagnosticError("STORAGE_CONTAINMENT")
    docs=pathlib.Path(__file__).resolve().parent.parent
    if root.resolve()==docs or docs in root.resolve().parents or root.resolve() in docs.parents:
        raise DiagnosticError("STORAGE_DOCS_OVERLAP")
    files={'zip':root/'incoming'/'Charades.zip','train':root/'extracted'/'Charades_v1_train.csv',
           'test':root/'extracted'/'Charades_v1_test.csv','classes':root/'extracted'/'Charades_v1_classes.txt'}
    fingerprints={}
    for name,path in files.items():
        check_ancestors(path)
        if not path.is_file(): raise DiagnosticError("SOURCE_FILE_MISSING")
        fingerprints[name]=digest_file(path,EXPECTED_SHA.get(name))
    with zipfile.ZipFile(files['zip']) as z:
        matches=[i for i in z.infolist() if pathlib.PurePosixPath(i.filename).name=='Charades_v1_classes.txt']
        if len(matches)!=1 or matches[0].file_size>16*1024*1024: raise DiagnosticError("CLASS_ENTRY_CONTRACT")
        if hashlib.sha256(z.read(matches[0])).hexdigest()!=fingerprints['classes']:
            raise DiagnosticError("CLASS_BYTES_MISMATCH")
    classes={line.split()[0] for line in files['classes'].read_text(encoding='utf-8-sig').splitlines() if line.strip()}
    if len(classes)!=157: raise DiagnosticError("CLASS_COUNT_MISMATCH")
    raw={}; headers={}
    for split in ('train','test'):
        headers[split],rows=parse_csv(files[split].read_text(encoding='utf-8-sig'))
        raw[split]=summarize_rows(rows,classes)
        if any(raw[split]['counts'].get(k,0)!=n for k,n in REFERENCES[split].items()):
            raise DiagnosticError("BATCH010_COUNTS_MISMATCH")
    raw['all']=merge_summaries([raw['train'],raw['test']])
    raw.update({'fingerprints':fingerprints,'headers':headers,'class_count':len(classes),
                'independent_reference_match':'PASS','storage_identity':'PASS','source_writes':0,
                'data_downloads':0,'time_contract':'HOLD_TIME_CONTRACT'})
    return disclose(raw)


if __name__=='__main__':
    try:
        if len(sys.argv)!=1: raise DiagnosticError("NO_EXTERNAL_PATH_OR_URL_ARGUMENTS")
        print(json.dumps(audit_fixed_storage(),ensure_ascii=True,indent=2))
    except DiagnosticError as e:
        print('DIAGNOSTIC_BLOCKED:'+str(e)); raise SystemExit(1) from None
    except Exception:
        print('DIAGNOSTIC_BLOCKED:SOURCE_OR_ENVIRONMENT_UNVERIFIED'); raise SystemExit(1) from None
