import json,hashlib
from pathlib import Path
R=Path(__file__).parent;D=R/'expanded-v4';D.mkdir();load=lambda p:json.loads(p.read_text());dump=lambda p,o:p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
for fn in ['questions.json','answer-key.json']:
 o=load(R/'expanded-v3'/fn);o['benchmark_version']='expanded-v4';dump(D/fn,o)
m=load(R/'expanded-v3/scope-map.json');m['version']='scope-v4'
for e in m['entries']:
 i=e['id'];f=e['required_answer_facts'];b=e['contextual_key_background']
 if i=='Q01':f[1]='Mark the two initial lots and take starting money equal to the sum of their printed card money values.';b.append('These card values are only used during setup; Q03 asks that limitation explicitly.')
 if i=='Q21':f[2]='Yes, a different available color may be built on an owned lot.';b.append('Normal build cost applies; this question does not give a price or ask a monetary calculation.')
 if i=='Q23':f[1]='Casino tile remains; acquisition precedes matching casino payment.';b.append('The new value2 die pays its owner $2 on that payout, but income amount is not asked here.')
 if i=='Q34':e['scope_note']='A yes/no permission and any-number actor rule resolve the question. Ordinary restrictions remain valid context; do not require repeating all trading timing/assets/transfer rules.'
m['versioned_corrections'] += [{'id':i,'change':x} for i,x in [('Q01','Setup-only limitation is unasked here and tested by Q03.'),('Q21','No concrete price supplied; different available color legality required, monetary explanation background.'),('Q23','Dievalue2 and takeover-before-payment required; $2 income calculation unasked background.'),('Q34','No demand to repeat ordinary trading restrictions as additional asked facts.')]]
dump(D/'scope-map.json',m);dump(D/'grading-key.json',{'version':'grading-key-v4','baseline':'answer-key.json','scope_map':'scope-map.json','answers':[{**e,'expected_answer':' '.join(e['required_answer_facts'])} for e in m['entries']]})
(D/'question-bank.md').write_text('# Lords of Vegas — expanded-v4\n\n35 questions. Original wording and baseline expected answers retained. Effective required facts below implement the explicit versioned scope corrections before any full-bank reader dispatch.\n\n'+'\n\n'.join('## '+e['id']+'\n\n'+e['asked_question']+'\n\n'+' '.join(e['required_answer_facts'])+'\n\nSource: '+e['source_references'] for e in m['entries'])+'\n')
l=load(R/'coverage-ledger-v3.json');l['passes'] += [{'pass':10,'focus':'Repeat complete procedural source scan after final classification corrections: no new asked rule beyond Q35','accepted':[]},{'pass':11,'focus':'Rechallenge every cost, actor, timing, exception, destination, exhaustion and end branch against actual asked35fact map; no new source-supported outcome branch','accepted':[]}];l['stopping_rule']='All core procedures mapped; final targeted passes10/11 each add zero after independently proposed Banker question Q35. Independent correction recheck pending.';dump(R/'coverage-ledger-v4.json',l)
q=load(D/'questions.json');k=load(D/'answer-key.json');oldq=load(R/'expanded-v3/questions.json');oldk=load(R/'expanded-v3/answer-key.json');manifest={'benchmark':'expanded-v4','question_count':35,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in D.iterdir() if p.is_file()},'unchanged_baseline_entries':{'all35questions':q['questions']==oldq['questions'],'all35baseline_answers':k['answers']==oldk['answers']}}
dump(D/'bank-freeze-manifest.json',manifest);print(manifest['unchanged_baseline_entries'])
