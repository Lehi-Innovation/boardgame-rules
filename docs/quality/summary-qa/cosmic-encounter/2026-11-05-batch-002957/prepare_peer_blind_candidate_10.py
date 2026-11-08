"""Version process-metadata hygiene; preserve every question and required fact."""
from pathlib import Path
import copy
import hashlib
import json
import re

R=Path(__file__).parent;OLD=R/'expanded-candidate-09';OUT=R/'expanded-candidate-10'
assert not OUT.exists();OUT.mkdir()
def read(p):return json.loads(p.read_text())
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json')
q['benchmark_version']=k['benchmark_version']=OUT.name
changes=[]
for a in k['answers']:
    for i,text in enumerate(a['source_references']):
        clean=re.sub(r';\s*independent.*$','',text,flags=re.I)
        if clean!=text:
            changes.append({'id':a['id'],'field':'source_references','index':i,'old':text,'new':clean,'reason':'Remove peer/process citation; retain complete primary locator.'})
            a['source_references'][i]=clean
    if a['id'] in ['Q160','Q163','Q164']:
        old=copy.deepcopy(a['contextual_background'])
        replacement={'Q160':[],
                     'Q163':['Hand sizes, distribution quotas, target selection, role and phase are not supplied by this quoted example.'],
                     'Q164':['Only the explicit Loser Wild timing clause is included; no kicker mechanics, full flare effect, role, cost or trigger is supplied here.']}[a['id']]
        a['contextual_background']=replacement
        changes.append({'id':a['id'],'field':'contextual_background','old':old,'new':replacement,'reason':'Remove review/novelty conclusions while preserving source-rule limitations.'})
assert q['questions']==read(OLD/'questions.json')['questions']
assert all(a['required_facts']==b['required_facts'] for a,b in zip(k['answers'],read(OLD/'answer-key.json')['answers']))
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions']
assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
assert not any(re.search(r'reviewer|audit|proposal|novelty|coverage|independent|source-review',text,re.I) for a in k['answers'] for field in ['required_facts','contextual_background','source_references'] for text in a[field])
save('questions.json',q);save('answer-key.json',k)
save('process-metadata-corrections.json',{'parent_version':OLD.name,'purpose':'Fresh literal/key validator receives only current literal questions and source-key material, without prior reviewers or their conclusions.','question_objects_identical':True,'all_526_required_fact_strings_identical':True,'original_twenty_question_and_key_objects_identical':True,'substantive_rule_fields_dropped':False,'changes':changes})
for name in ['acceptance-rejection-ledger.json','versioned-corrections.json','candidate-question-map.json','withdrawn-question-ledger.json','targeted-coverage-passes.json']:
    save(name,read(OLD/name))
coverage=read(OLD/'coverage-map.json');coverage.update(bank_version=OUT.name,question_count=164,status='Metadata-clean review candidate; complete peer-blind actual-scope validation and renewed source stopping check pending. Human choices remain pending.')
save('coverage-map.json',coverage)
(OUT/'question-bank.md').write_text('# Expanded candidate 10 — source review pending\n\n'+'\n\n'.join(f"## {qe['id']}\n\n{qe['question']}\n\n"+'\n'.join('- '+f for f in ke['required_facts']) for qe,ke in zip(q['questions'],k['answers']))+'\n')
save('input-manifest.json',{'review_candidate_only':True,'question_count':164,'raw_key_fact_records':526,'all_required_fact_strings_identical_to09':True,'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,len(q['questions']),sum(len(a['required_facts']) for a in k['answers']),len(changes),'process-only field edits')
