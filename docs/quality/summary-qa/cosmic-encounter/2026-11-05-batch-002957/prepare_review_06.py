from pathlib import Path
import hashlib
import json

R = Path(__file__).parent
B = R/'expanded-candidate-06'
D = B/'review-inputs'
assert not D.exists()
D.mkdir()
def read(p): return json.loads(p.read_text())
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n')
scope=read(B/'question-scope-map-candidate.json')
compact=[]
for e in scope['questions']:
    item={'id':e['id'],'clauses':[{'paraphrase':c['asked_clause_paraphrase'],'fact_ids':[f['unique_fact_id'] for f in c['required_fact_refs']]} for c in e['asked_clauses']],
          'fact_scope':[{'id':f['unique_fact_id'],'key_index':f['required_facts_zero_based_index'],'classification':f['scope_classification'],'asked':f['asked_content'],'background':f['contextual_content'],'conditional':f['conditional_scope_note']} for f in e['candidate_facts']]}
    if e.get('renewed_validation_required'):
        item={'id':e['id'],'status':'Changed question/key; reviewer must remap current literal text and all facts afresh.'}
    compact.append(item)
compact.append({'id':'Q156','status':'New question; reviewer must map its literal question and fact.'})
save(D/'proposed-asked-scope.json',{'status':'parent proposal, needs independent validation','bank_version':B.name,'questions':compact,'Q001_equivalence':'Include all dealt flares including rejected aliens plus random extras to ten; six-plus-four numeric wording is an equivalent derivation, not a separate recital requirement.','conditional_policy':'Q054/Q143 explicitly printed documentary conditionals retained; no reachable-current-base-branch novelty credit. Q086 withdrawn with independent disposition, never reuse its ID.'})
coverage=read(B/'coverage-map.json')
for e in coverage['original_fifty_printed_abilities']:
    e.pop('tested_claims',None)
save(D/'coverage-map.json',coverage)
passes=read(B/'targeted-coverage-passes.json')
passes['passes'] += [
 {'pass':8,'focus':'Renewed core procedure/source-to-actual-question pass after CKS changes: setup, all phase actors, legal actions, destinations, reward/cost commitment, exhaustion and end conditions.', 'added_question_ids':[],'qualifying_rule_additions':0,'evidence':'Parent reread complete current155 questions/509 raw key facts, all44 original-rulebook passage mappings, and every applicable FAQ mapping; re-read all currently unmapped FAQ source passages. Earlier complete source reading remains authority; no new source interpretation adopted.','rejections':['Further attack or reward arithmetic repeatsQ008/Q010.','Reclaim cap/source is now actually asked inQ078.','Q086 cannot be reinstated merely by an assumed expanded win threshold.','FAQ terminology and alert-level teaching suggestions are not new procedural branches.']},
 {'pass':9,'focus':'Renewed fifty-alien/flare/FAQ scope pass: roles, timing strips, atomic selections, identity, retention, transfer, arrival and prevention. Distinguish key context from actual tested content.', 'added_question_ids':[],'qualifying_rule_additions':0,'evidence':'Parent compared all current alien questions and actual-scope exceptions with the previously completely inspected native fifty sheets and source-derived catalog; checked retained2009errata and currentFAQ mappings. New Reserve action/eligibility and Mobius arrival rules are now explicitly asked.','rejections':['Extra quantity/color substitutions do not add branches.','Q054 copying andQ143 self-special remain printed documentary conditionals without assumed expansion enablers.','All unprovided full flare effects remain outside available card-text authority.','Reward-deck/back-selection specifics and Saboteur trap commitments remain excluded.']}
]
passes['status']='Two renewed parent targeted passes add zero for source-resolvable stratum; fresh independent challenge and human source choices still required.'
save(D/'targeted-coverage-passes.json',passes)
(B/'targeted-coverage-passes-after-review.json').write_text(json.dumps(passes,indent=2,ensure_ascii=False)+'\n')
save(D/'input-manifest.json',{'question_count':155,'raw_key_fact_records':509,'sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'questions.json',B/'answer-key.json',B/'acceptance-rejection-ledger.json',B/'versioned-corrections.json',B/'withdrawn-question-ledger.json',*D.iterdir()] if p.is_file()}})
print([(p.name,p.stat().st_size) for p in D.iterdir()])
