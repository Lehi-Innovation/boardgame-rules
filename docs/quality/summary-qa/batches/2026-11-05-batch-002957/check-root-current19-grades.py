"""Bind passing current19 originals, every fixed Q/key, all primary labels and quotations."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
V=ROOT/'docs/quality/summary-qa/root'/B.name/'current-snapshot-revalidation-2026-11-07';D=V/'iteration-02'
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
q={x['id']:x for x in J(D/'questions.json')['questions']};key={x['id']:x for x in J(D/'answer-key.json')['answers']}
body=(D/'summary-snapshot.md').read_text();raw={w:{x['id']:x for x in J(D/('reader-'+w+'.json'))['answers']} for w in 'ab'}
freeze=J(D/'raw-output-manifest.json')
for w in 'ab':
    f=freeze['readers'][w];assert H(Path(f['path']))==f['sha256']==H(Path(f['exact_original_copy']))==f['copy_sha256'] and f['answer_count']==81
    assert list(raw[w])==list(q)
assert freeze['existing_primary_count']==0 and not freeze['existing_prefix_primary_labels_preserved'] and freeze['chronology_deviation'] is None
for path,digest in freeze['existing_prefix_primary_labels_preserved'].items():assert H(Path(path))==digest
counts={w:Counter() for w in 'ab'};seen=set();reports=[];quote_count=0
for p in sorted((D/'primary-grades').glob('*.json')):
    x=J(p);w,i=x['reader'],x['id'];assert (w,i) not in seen and x['question']==q[i] and x['expected']==key[i]
    assert x['observed_original_entry']==raw[w][i] and x['observed_entry_sha256']==C(raw[w][i])
    assert x['every_substantive_field_reviewed'] and x['whole_entry_policy']
    assert x['grade'] in ['correct','partial','incorrect','borderline']
    for passage in raw[w][i]['source_passages']:
        quote=passage['quotation'];assert quote and quote in body;quote_count+=1
    counts[w][x['grade']]+=1;seen.add((w,i));reports.append({'path':str(p),'sha256':H(p),'reader':w,'id':i,'primary_grade':x['grade']})
assert seen=={(w,i) for w in 'ab' for i in q}
assert all(counts[w]['correct']==81 and sum(counts[w].values())==81 for w in 'ab')
assert all(x['grade']=='correct' and not x.get('unsupported_guess') and not x.get('unresolved_requested_fact') for p in (D/'primary-grades').glob('*.json') for x in [J(p)])
for f in ['results-primary.json','results.json']:
    result=J(D/f);assert all(all(result['readers'][w]['totals'].get(k,0)==v for k,v in {'correct':81,'partial':0,'incorrect':0,'borderline':0}.items()) for w in 'ab')
assert J(D/'primary-review-declaration.json')['originals_frozen_before_any_semantic_grading']
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':81,'complete_original_entries':162,'all_fixed_Q_and_prose_key_records_exact':True,'all162_original_entry_hashes_and_full_fields_bound':True,'exact_nonempty_same_entry_source_quotations':quote_count,'primary_scores':{w:dict(c) for w,c in counts.items()},'reports':reports,'raw_hashes':{w:H(D/('reader-'+w+'.json')) for w in 'ab'},'no_neutral_needed':True,'primary_review_declaration_sha256':H(D/'primary-review-declaration.json'),'pair_verdict':'PASS','technical_qualifications':['Originals frozen before all factual grading, no factual feedback.','B actual dispatch repeats the same nonfactual access restriction; intended and actual prompts retained.','One B five-question mid-turn draft refined its dominance wording before a completed turn. Draft and completed original retained; all completed-turn entries unchanged.','Parent evaluator may repair per QA guide; independent pure source actor is separate.'],'limits':['Reader model and full delivery proofs are separate. Pure source audit current18 remains valid on unchanged exact da0 body.','Working fixed81 benchmark within documented base/core source scope, not heldout model-generalization evidence.']}
out=B/'coordinator-checks/root-current19-primary-grade-integrity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':162,'exact_source_quotes':quote_count,'scores':proof['primary_scores'],'proof':str(out)}))
