"""Incorporate independent challenge02 without changing original twenty records."""
from pathlib import Path
import copy
import hashlib
import json

R=Path(__file__).parent
OLD=R/'expanded-candidate-06'
OUT=R/'expanded-candidate-07'
assert not OUT.exists()
OUT.mkdir()
def read(p): return json.loads(p.read_text())
def write(name,value): (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json')
q['benchmark_version']=k['benchmark_version']=OUT.name
proposals={p['proposal_id']:p for p in read(R/'source-review/coverage-key-scope-review-02.json')['accepted_proposals']}
ledger=read(OLD/'acceptance-rejection-ledger.json')
changes=[]
def sources(*ids):
    return [f"{s['path']} PDF p{s['pdf_page']} extraction lines{s['lines_1_based'][0]}–{s['lines_1_based'][1]} ({ident})" for ident in ids for s in proposals[ident]['sources']]
def add(ident,question,facts,proposal_ids,background=None):
    qe={'id':ident,'question':question}
    ke={'id':ident,'required_facts':facts,'contextual_background':background or [],'source_references':sources(*proposal_ids)}
    q['questions'].append(qe);k['answers'].append(ke)
    changes.append({'question_id':ident,'action':'add-distinct-actually-unasked-procedure','proposal_ids':proposal_ids,'before_question':None,'before_key':None,'after_question':qe,'after_key':ke})
idx=next(i for i,e in enumerate(q['questions']) if e['id']=='Q082')
beforeq,beforek=copy.deepcopy(q['questions'][idx]),copy.deepcopy(k['answers'][idx])
q['questions'][idx]['question'] += ' Unless a specific effect says otherwise, which type/value do effects strictly determining compensation, rewards or disposition of involved ships use?'
k['answers'][idx]['required_facts'].append('These effects strictly affecting encounter resolution also use the card\'s current modified type/value, unless a specific effect says otherwise.')
k['answers'][idx]['source_references'] += sources('CKS02-P02')
changes.append({'question_id':'Q082','action':'explicitly-ask-non-total-resolution-category','proposal_ids':['CKS02-P02'],'before_question':beforeq,'before_key':beforek,'after_question':q['questions'][idx],'after_key':k['answers'][idx]})
add('Q157',proposals['CKS02-P01']['proposed_question'],['No automatic draw is caused merely by an encounter ending, a turn ending or the hand becoming empty.'],['CKS02-P01'])
add('Q158','During an ordinary Launch after destiny specifies the system, who chooses the target planet within that system, and where are the offense\'s launched ships placed? During Alliance, where does a joining offensive ally place its committed ships?', ['The offense points the gate at one planet in the system indicated by destiny.','Place the launched offense ships on the wide end of the hyperspace gate.','Place the joining offensive ally\'s ships on the hyperspace gate.'],['CKS02-P03','CKS02-P04'])
add('Q159',proposals['CKS02-P05']['proposed_question'],['Receive one defender reward for each ship contributed to the successful defense.','For each contributed ship the ally must draw one cosmic-deck card or retrieve one own warp ship; the ordinary rule does not permit declining the reward.'],['CKS02-P05'],['Mixing the two sources and reward destinations are already asked by Q010; full-source commitment before taking any is Q155.'])
add('Q160','Under the original rulebook, name the seven phases of an ordinary encounter in order. How is the separate Start Turn step related to this sequence on the first encounter?', ['Regroup, Destiny, Launch, Alliance, Planning, Reveal, Resolution, in that order.','Start Turn occurs before the first encounter\'s Regroup effects, and only on that first encounter.'],['CKS02-P06'],['Only the complete seven-phase order adds novelty; Start Turn versus Regroup was already asked by Q076.'])
add('Q161',proposals['CKS02-P07']['proposed_question'],['Add the legally played reinforcement card\'s printed amount to the chosen side\'s encounter total.'],['CKS02-P07'],['The attack-versus-attack case avoids choosing an interpretation of the pending reinforcement/Negotiate conflict.'])
for c in changes:
    for ident in c['proposal_ids']:
        p=proposals[ident]
        ledger.append({'candidate':ident,'question_id':c['question_id'],'decision':'accepted-distinct-actually-unasked-procedure','novelty':p['novelty_rationale'],'positive_base_applicability':p['positive_base_applicability'],'source_review':'source-review/coverage-key-scope-review-02.json'})
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions']
assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
ids=[x['id'] for x in q['questions']]
assert len(ids)==len(set(ids))==160 and 'Q086' not in ids
assert ids==[x['id'] for x in k['answers']]
write('questions.json',q);write('answer-key.json',k)
write('acceptance-rejection-ledger.json',ledger)
write('versioned-corrections.json',{'parent_version':OLD.name,'independent_challenge':'source-review/coverage-key-scope-review-02.json','original_twenty_preserved_verbatim':True,'prior_bank_blind_test_dispatched':False,'accepted_rule_proposals':7,'new_questions':5,'extended_questions':1,'changes':changes})
write('withdrawn-question-ledger.json',read(OLD/'withdrawn-question-ledger.json'))
mapping=read(OLD/'candidate-question-map.json')
for c in changes:
    for ident in c['proposal_ids']: mapping[ident]=c['question_id']
write('candidate-question-map.json',mapping)
scope=read(R/'source-review/coverage-key-scope-map-02.json')
scope.update(bank_version=OUT.name,status='Parent carry-forward proposal: independent02 scope validated unchanged entries; Q082 and Q157–Q161 require new independent validation.',question_count=160,raw_key_fact_count=sum(len(a['required_facts']) for a in k['answers']))
changed={c['question_id']:c for c in changes}
for i,e in enumerate(scope['questions']):
    if e['id'] in changed:
        c=changed[e['id']]
        scope['questions'][i]={'id':e['id'],'literal_question':c['after_question']['question'],'current_key':c['after_key'],'status':'changed-needs-independent-remapping','prior_validated_entry':e}
for ident,c in changed.items():
    if ident not in [e['id'] for e in scope['questions']]:
        scope['questions'].append({'id':ident,'literal_question':c['after_question']['question'],'current_key':c['after_key'],'status':'new-needs-independent-mapping'})
scope['integrity_from_prior_version_only']=scope.pop('integrity')
write('question-scope-map-candidate.json',scope)
coverage=read(OLD/'coverage-map.json')
coverage.update(bank_version=OUT.name,question_count=160,status='Seven independent02 unasked procedures incorporated; renewed targeted passes and new independent challenge pending.')
coverage['independent02_additions']=[{'proposal':ident,'question_id':mapping[ident],'primary_sources':p['sources'],'novelty':p['novelty_rationale']} for ident,p in proposals.items()]
coverage['source_coverage_caution']='Original broad paragraph mappings do not certify every clause. Actual coverage is only the validated literal-question overlay plus these explicit additions. No key-only context credit.'
write('coverage-map.json',coverage)
passes=read(OLD/'targeted-coverage-passes-after-review.json')
passes['status']='Counter reset after seven independent02 coverage additions; renewed zero checks pending.'
passes['passes'].append({'pass':10,'focus':'Independent source/literal-scope challenge02','new_questions':['Q157','Q158','Q159','Q160','Q161'],'extended_questions':['Q082'],'qualifying_rule_proposals':7,'stopping_counter_reset':True})
write('targeted-coverage-passes.json',passes)
(OUT/'question-bank.md').write_text('# Expanded candidate 07 — renewed independent review pending\n\n'+'\n\n'.join(f"## {qe['id']}\n\n{qe['question']}\n\n"+'\n'.join('- '+f for f in ke['required_facts']) for qe,ke in zip(q['questions'],k['answers']))+'\n')
write('input-manifest.json',{'frozen_for_review_only':True,'question_count':160,'raw_key_fact_records':sum(len(a['required_facts']) for a in k['answers']),'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,len(ids),sum(len(a['required_facts']) for a in k['answers']))
