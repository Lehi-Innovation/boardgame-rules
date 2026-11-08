"""Verify all94 pair03 entries against their unchanged v11 bank and one neutral."""
import hashlib,json,re
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parents[4]/'docs/quality/summary-qa/new-angeles'/B.name
D=R/'expanded-luna-iteration-03'
J=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
q={x['id']:x for x in J(D/'questions.json')['questions']}
k={x['id']:x for x in J(R/'expanded-candidate-v11/answer-key.json')['answers']}
s={x['id']:x for x in J(R/'expanded-candidate-v11/asked-clause-map.json')}
paths={w:D/('reader-'+w+'.json') for w in 'ab'}
raw={w:{x['id']:x for x in J(p)['answers']} for w,p in paths.items()}
assert all(list(raw[w])==list(q) for w in 'ab')
def location(v,p):
    assert p.startswith('$')
    for field,index in re.findall(r'\.([^\.\[\]]+)|\[(\d+)\]',p[1:]):v=v[field] if field else v[int(index)]
    return v
refs=[]
def walk(v,entry,who,ident):
    if isinstance(v,dict):
        if all(a in v for a in ['location','unicode_start','unicode_end','quote']):
            text=location(entry,v['location']);assert isinstance(text,str) and text[v['unicode_start']:v['unicode_end']]==v['quote']
            refs.append({'reader':who,'id':ident,**v})
        for child in v.values():walk(child,entry,who,ident)
    elif isinstance(v,list):
        for child in v:walk(child,entry,who,ident)
plan=J(D/'grading/input-manifest.json');totals={w:Counter() for w in 'ab'}
seen=set();reports=[];facts={w:0 for w in 'ab'};split=[];labels={}
for task in plan['blocks']:
    pp=Path(task['pack']);rp=Path(task['output']);assert H(pp)==task['pack_sha256']
    pack=J(pp);report=J(rp);ids=task['ids'];assert pack['ids']==ids
    for name,digest in pack['source_file_hashes'].items():assert H(Path(name))==digest
    assert pack['questions']==[q[i] for i in ids] and pack['fixed_key']==[k[i] for i in ids] and pack['asked_clause_map']==[s[i] for i in ids]
    for w in 'ab':
        assert pack['complete_raw_reader_entries'][w]==[raw[w][i] for i in ids]
        for i in ids:assert pack['raw_entry_sha256'][w][i]==C(raw[w][i])
    records=report.get('records',report.get('grades'));assert len(records)==2*len(ids)
    actual=set()
    for x in records:
        w,i=x['reader'],x['id'];assert w in 'ab' and i in ids and (w,i) not in actual
        actual.add((w,i));assert x['raw_entry_sha256']==C(raw[w][i])
        assert x['label'] in ['Correct','Partial','Incorrect']
        if x['material_wrong_claims']:assert x['label']=='Incorrect'
        if len(x['asked_fact_assessments'])!=len(s[i]['asked_facts']):split.append({'reader':w,'id':i,'fixed':s[i]['asked_facts'],'actual':[a['asked_fact'] for a in x['asked_fact_assessments']]})
        walk(x,raw[w][i],w,i);totals[w][x['label']]+=1;facts[w]+=len(s[i]['asked_facts']);labels[w,i]=x['label']
    assert actual=={(w,i) for w in 'ab' for i in ids} and not seen.intersection(actual)
    seen.update(actual);reports.append({'path':str(rp),'sha256':H(rp),'pack_sha256':H(pp),'ids':ids})
assert len(seen)==188 and all(v==272 for v in facts.values()) and len(reports)==6
np=D/'grading/fresh-borderline-adjudication.json';ip=D/'grading/fresh-borderline-input.json'
neutral=J(np);packet=J(ip);entries={(x['reader'],x['id']):x for x in packet['entries']}
assert set(entries)=={('b','Q13'),('b','Q21'),('a','Q52'),('b','Q52')}
for (w,i),x in entries.items():assert x['complete_raw_entry']==raw[w][i]
effective={w:Counter(v) for w,v in totals.items()}
for x in neutral['records']:
    w,i=x['reader'],x['id'];assert (w,i) in entries and x['raw_entry_sha256']==C(raw[w][i])
    effective[w][labels[w,i]]-=1;effective[w][x['label']]+=1
    walk(x,raw[w][i],w,i)
assert {(x['reader'],x['id']) for x in neutral['records']}==set(entries)
counts=lambda t:{w:{k:v[k] for k in ['Correct','Partial','Incorrect']} for w,v in t.items()}
assert counts(totals)==counts(effective)=={'a':{'Correct':93,'Partial':1,'Incorrect':0},'b':{'Correct':92,'Partial':2,'Incorrect':0}}
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':94,'original_entries':188,'mapped_requirement_vectors':facts,'primary_scores':counts(totals),'one_neutral_effective_scores':counts(effective),'reports':reports,'raw_hashes':{w:H(p) for w,p in paths.items()},'exact_same_entry_references':refs,'compound_asked_vectors_split_for_review':split,'one_neutral_report_sha256':H(np),'one_neutral_packet_sha256':H(ip),'semantic_acceptance':{'Q13_B':'Full context and quotation make disputed pre-agreement binding nonbinding, without imposing a mandatory advance-discussion requirement on ordinary immediate agreed trades. Correct.','Q21_B':'Caps and exhaustive mover list supply development exclusion. Android movement destination prohibition is actually absent. Partial; unrest background unasked.','Q52_both':'Illness waiver and ordinary two-threat contrast correct. Entire action quotation/entry lacks general any-district ignoring-paths movement procedure asked by literal how-to. Partial.'},'limits':['Historical pair03; current guide changed and pair04 is separate.','One neutral only; all primary labels and complete original entries preserved.','Whole-entry quotations count, without cross-answer borrowing, paraphrase/name gates or receipt caps.','Actual model/input delivery and current source/scope/publication gates remain separate.']}
out=B/'coordinator-checks/new-angeles-expanded03-primary-and-one-neutral-integrity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':len(seen),'facts':facts,'scores':counts(effective),'exact_references':len(refs),'split_vectors':len(split),'proof':str(out)}))
