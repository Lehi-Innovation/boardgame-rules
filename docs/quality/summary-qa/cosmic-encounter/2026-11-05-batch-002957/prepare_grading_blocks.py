"""After an authorized full-bank freeze, build lossless disjoint grading bundles.

This prepares evidence only. It does not launch agents or assign grades.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

R=Path(__file__).parent.resolve()
def sha(b): return hashlib.sha256(b).hexdigest()
def objsha(x): return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def unique_object(pairs):
    out={}
    for key,value in pairs:
        if key in out: raise ValueError('Duplicate JSON object key: '+key)
        out[key]=value
    return out
def read(path): return json.loads(path.read_text(),object_pairs_hook=unique_object)
def raw_entries(path):
    text=path.read_text();doc=read(path);decoder=json.JSONDecoder(object_pairs_hook=unique_object)
    candidates=[]
    for match in re.finditer(r'"answers"\s*:\s*\[',text):
        start=text.index('[',match.start())
        try: arr,end=decoder.raw_decode(text,start)
        except ValueError: continue
        if arr==doc['answers']: candidates.append((start,end))
    assert len(candidates)==1,'Unambiguous original answers array required'
    start,end=candidates[0];pos=start+1;entries=[]
    while pos<end:
        while text[pos].isspace() or text[pos]==',': pos+=1
        if text[pos]==']': break
        item,stop=decoder.raw_decode(text,pos)
        assert item==doc['answers'][len(entries)]
        raw=text[pos:stop]
        entries.append({'id':item['id'],'complete_original_entry':item,'original_raw_text_recoverable_from_exact_byte_span':True,
                        'raw_file_path':str(path),'raw_file_sha256':sha(path.read_bytes()),
                        'raw_entry_sha256':sha(raw.encode()),'normalized_entry_sha256':objsha(item),
                        'start_char':pos,'end_char':stop,'start_byte':len(text[:pos].encode()),'end_byte':len(text[:stop].encode()),
                        'all_fields_preserved':True})
        pos=stop
    assert len(entries)==len(doc['answers'])
    return entries

parser=argparse.ArgumentParser()
parser.add_argument('iteration',help='An existing frozen iteration directory below the assigned evidence root')
parser.add_argument('--questions-per-block',type=int,default=15)
args=parser.parse_args()
it=(R/args.iteration).resolve()
assert it.is_relative_to(R)
assert 1<=args.questions_per_block<=20
manifest=read(it/'input-manifest.json')
assert manifest.get('full_bank_freeze_authorized') is True,'No full-bank preparation before scope/freeze gates'
assert manifest.get('independent_actual_scope_validated') is True
assert manifest.get('pending_dependent_source_choices') == []
for path,expected in manifest['sha256'].items():
    assert sha(Path(path).read_bytes())==expected,('Frozen input changed',path)
questions=read(it/'questions.json')['questions'];key=read(it/'answer-key.json')['answers']
scope=read(it/'actual-question-scope.json')['questions']
expected=[q['id'] for q in questions]
assert len(expected)==len(set(expected))
assert [a['id'] for a in key]==expected
scope_by={a['id']:a for a in scope}
assert len(scope)==len(scope_by)==len(expected) and set(scope_by)==set(expected)
readers={letter:raw_entries(it/f'reader-{letter}.json') for letter in ['a','b']}
for entries in readers.values(): assert [x['id'] for x in entries]==expected
destination=it/'grading-inputs'
assert not destination.exists(),'Never replace previous grading inputs'
destination.mkdir()
blocks=[]
for start in range(0,len(expected),args.questions_per_block):
    end=min(start+args.questions_per_block,len(expected));ids=expected[start:end]
    items=[]
    for index in range(start,end):
        q,k=questions[index],key[index]
        items.append({'id':q['id'],'literal_question':q,'key':k,'validated_actual_scope':scope_by[q['id']],
                      'key_entry_sha256':objsha(k),'question_entry_sha256':objsha(q),
                      'raw_key_fact_refs':[{'id':f"{q['id']}-F{i+1:02}",'index':i,'sha256':sha(f.encode())} for i,f in enumerate(k['required_facts'])],
                      'readers':{letter:entries[index] for letter,entries in readers.items()}})
    path=destination/f'block-{len(blocks)+1:02}.json'
    bundle={'expected_ids':ids,'complete_summary_path':str(it/'summary-snapshot.md'),'summary_sha256':sha((it/'summary-snapshot.md').read_bytes()),'entries':items,'scope_note':'All raw key records are preserved. Only validated asked portions are mandatory; all substantive raw reader fields remain subject to material-contradiction review.'}
    path.write_text(json.dumps(bundle,indent=2,ensure_ascii=False)+'\n')
    blocks.append({'path':str(path),'sha256':sha(path.read_bytes()),'expected_ids':ids,'raw_key_fact_count':sum(len(x['key']['required_facts']) for x in items),'complete_reader_entries':2*len(ids)})
assert [ident for b in blocks for ident in b['expected_ids']]==expected
report={'iteration':it.name,'question_count':len(expected),'all_ids_once_per_reader':True,'all_raw_fields_and_entry_spans_preserved':True,'all_raw_key_facts_once_per_reader':sum(b['raw_key_fact_count'] for b in blocks)==sum(len(k['required_facts']) for k in key),'blocks':blocks,'raw_reader_files':{letter:{'path':str(it/f'reader-{letter}.json'),'sha256':sha((it/f'reader-{letter}.json').read_bytes())} for letter in readers}}
(destination/'manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('Prepared',len(blocks),'disjoint blocks covering both complete raw answer sets; no grades assigned.')
