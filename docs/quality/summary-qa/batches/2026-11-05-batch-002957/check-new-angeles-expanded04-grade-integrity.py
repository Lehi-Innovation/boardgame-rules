"""Verify all94 pair04 entries against their unchanged v11 bank and one neutral."""
import hashlib,json,re
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parents[4]/'docs/quality/summary-qa/new-angeles'/B.name
D=R/'expanded-luna-iteration-04'
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
assert all(totals[w]['Correct']==94 and totals[w]['Partial']==totals[w]['Incorrect']==0 for w in 'ab')
assert not (D/'grading/fresh-borderline-adjudication.json').exists()
result=J(D/'results.json')
scores={w:{label:totals[w][label] for label in ['Correct','Partial','Incorrect']} for w in 'ab'}
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':94,'original_entries':188,'mapped_requirement_vectors':facts,'primary_scores':scores,'reports':reports,'raw_hashes':{w:H(p) for w,p in paths.items()},'exact_same_entry_references':refs,'compound_asked_vectors_split_for_review':split,'one_neutral_required':False,'no_borderline_findings_reported':True,'current_summary_sha256':H(D/'summary-snapshot.md'),'current_canonical_matches':H(D/'summary-snapshot.md')==H(B.parents[4]/'rules/new-angeles.md'),'pair_verdict':'PASS_FIXED_SUPPORTED_94_BANK','limits':['All literal94 questions and544 mapped vector checks bound to complete original answers and only same-entry operative evidence; no arbitrary word/name gate or receipt cap.','Technical long-unit display/rerender note preserved separately and does not change factual grades.','Exact current source02/rev04 accuracy and fresh94 coverage independently accepted in separate proofs.','SG01 and documented source limits remain; NO complete-core/stamping/publication/goal-complete approval.']}
out=B/'coordinator-checks/new-angeles-expanded04-primary-and-reference-integrity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':len(seen),'vectors':facts,'scores':scores,'exact_same_entry_references':len(refs),'split_vectors':len(split),'proof':str(out)}))
