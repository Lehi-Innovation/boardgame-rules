from pathlib import Path
import copy
import hashlib
import json

R=Path(__file__).parent;OLD=R/'expanded-candidate-08';OUT=R/'expanded-candidate-09'
assert not OUT.exists();OUT.mkdir()
def read(p):return json.loads(p.read_text())
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json')
q['benchmark_version']=k['benchmark_version']=OUT.name
changes=[];ledger=read(OLD/'acceptance-rejection-ledger.json')
i=next(i for i,e in enumerate(q['questions']) if e['id']=='Q146')
beforeq,beforek=copy.deepcopy(q['questions'][i]),copy.deepcopy(k['answers'][i])
q['questions'][i]['question']+=' Under its printed role and phase permissions, may an uninvolved player perform the classic Filch Wild cheating action during another player\'s Regroup?'
k['answers'][i]['required_facts'].append('Yes under those permissions: classic Filch Wild is As Any Player and Any Phase, so an uninvolved player and Regroup are allowed.')
k['answers'][i]['source_references'].append('Original rulebook p5 classic Filch Wild printed role/phase fields, extraction lines399–413; independent rulebook-component-continuation-03.')
changes.append({'question_id':'Q146','candidate':'classic-filch-wild-role-phase','before_question':beforeq,'before_key':beforek,'after_question':q['questions'][i],'after_key':k['answers'][i]})
def add(ident,question,facts,background,refs,candidate):
    qe={'id':ident,'question':question};ke={'id':ident,'required_facts':facts,'contextual_background':background,'source_references':refs}
    q['questions'].append(qe);k['answers'].append(ke)
    changes.append({'question_id':ident,'candidate':candidate,'before_question':None,'before_key':None,'after_question':qe,'after_key':ke})
add('Q162','For the FAQ-quoted Mite Super instruction to take any cards its opponent discards, is pickup restricted to encounter cards, or can it include another original-base card type such as a discarded artifact?', ['It is not restricted to encounter cards: that instruction allows taking any cards the opponent discards, including a discarded artifact.'], ['Only the quoted eligible-card clause is asked. Full trigger, role, phase, cost, persistence and card destination are not supplied or invented. No reward-deck mechanics or priority over another claimant is assumed.'], ['2018 FAQ p8 extraction lines774–784, original Mite Super quoted instruction; independent alien-cross-source-continuation-02 AC02-P01 and faq-fragment-continuation-05.'], 'mite-super-quoted-eligibility')
add('Q163','In the official FAQ Oracle Wild example, are the hands kept separate or mixed together, is the new hand chosen selectively or at random, and where is the Oracle flare during that process and afterward?', ['Mix the hands together.','Take the new hand at random from the mixed cards.','Play the Oracle flare faceup in front of its user outside the hand; return it to hand after the effect finishes.'], ['Mixing/random reassignment is new coverage. Generic flare return overlaps Q015. Hand sizes, distribution quotas, target selection, role and phase are not invented.'], ['2018 FAQ p6 extraction lines525–530, Oracle Wild example; independent alien-cross-source-continuation-02 AC02-P02 and faq-fragment-continuation-05.'], 'oracle-wild-mixed-hand-procedure')
add('Q164','For a legally played Loser Wild flare, must it be played before encounter cards are selected, or can it first be played after selection?', ['Loser Wild is played before encounter cards are selected; it cannot first be played after selection.'], ['Only this independently stated timing clause is asked; no kicker, full flare effect, role, cost or trigger is imported. Reviewer02 initially rejected novelty on the isolated fragment; independent source/novelty adjudicator08 accepted the card-specific legal window. Both decisions remain preserved.'], ['2018 FAQ p16 extraction lines1528–1532; independent loser-wild-novelty-adjudication-08 and faq-fragment-continuation-05.'], 'loser-wild-before-selection')
add('Q165','Must a player be a main player or an ally to play Cosmic Zap on an alien\'s power use, or may a bystander play it?', ['Cosmic Zap is As Any Player; an uninvolved bystander may play it on an otherwise legal power use.'], ['The actual-use/nonpreemptive window, own-power targeting and cancellation duration are already asked elsewhere; only actor eligibility is new.'], ['Original rulebook p5 Cosmic Zap illustration, As Any Player; independent rulebook-component-continuation-03.'], 'cosmic-zap-bystander-eligibility')
for c in changes:
    ledger.append({'candidate':c['candidate'],'question_id':c['question_id'],'decision':'accept-distinct-source-backed-clause-or-procedure','sources':c['after_key']['source_references'],'new_qualifying_rule_group':True})
ledger += [
 {'candidate':'FAQ05-planning-commitment','decision':'defer-not-accepted-in-original-only-procedural-bank','source_adjudication':'source-review/planning-source-scope-adjudication-06.json','reason':'Explicit mixed cosmic/reward-card premise; no positive primary-source bridge to original-only deadlock. No original-only sequence or opposite rule adopted.','new_coverage_credit':False},
 {'candidate':'Reserve power plus Reserve Wild acquisition','decision':'reject-mechanical-composition','source_adjudication':'source-review/reserve-wild-source-adjudication-07.json','novelty_adjudication':'source-review/alien-cross-source-continuation-02.json','reason':'A definite derived application is available, but only combines Q056/Q082/Q123 operators without a new sourced exception/timing/priority boundary. No new question or canonical named ruling.','new_coverage_credit':False},
 {'candidate':'Clone Super Main Player Only / Resolution recital','decision':'reject-no-distinct-outcome-beyond-ordinary-compensation','source_adjudication':'source-review/rulebook-component-continuation-03.json','new_coverage_credit':False}]
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions']
assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
ids=[x['id'] for x in q['questions']];assert len(ids)==len(set(ids))==164 and 'Q086' not in ids
assert ids==[x['id'] for x in k['answers']]
save('questions.json',q);save('answer-key.json',k);save('acceptance-rejection-ledger.json',ledger)
save('versioned-corrections.json',{'parent_version':OLD.name,'new_qualifying_rule_groups':5,'new_question_count':4,'extended_question_ids':['Q146'],'changes':changes,'original_twenty_preserved_verbatim':True,'prior_expanded_blind_readers_dispatched':False})
for n in ['candidate-question-map.json','withdrawn-question-ledger.json']:
    obj=read(OLD/n)
    if n=='candidate-question-map.json':
        for c in changes:obj[c['candidate']]=c['question_id']
    save(n,obj)
coverage=read(OLD/'coverage-map.json');coverage.update(bank_version=OUT.name,question_count=164,status='Five source-backed additions incorporated; renewed zero checks and peer-blind literal/key validation pending. Human authority choices remain unresolved.')
coverage['latest_source_decisions']=[{'candidate':c['candidate'],'question_id':c['question_id'],'primary_refs':c['after_key']['source_references']} for c in changes]
save('coverage-map.json',coverage)
passes=read(OLD/'targeted-coverage-passes-after-review.json');passes['status']='Counter reset after five accepted source-clause/procedure additions.'
passes['passes'].append({'pass':13,'focus':'Own initial source-review continuations plus isolated source/novelty adjudications','qualifying_rule_groups':5,'new_questions':['Q162','Q163','Q164','Q165'],'extended_questions':['Q146'],'stopping_counter_reset':True})
save('targeted-coverage-passes.json',passes)
(OUT/'question-bank.md').write_text('# Expanded candidate 09 — review pending\n\n'+'\n\n'.join(f"## {qe['id']}\n\n{qe['question']}\n\n"+'\n'.join('- '+f for f in ke['required_facts']) for qe,ke in zip(q['questions'],k['answers']))+'\n')
save('input-manifest.json',{'review_candidate_only':True,'question_count':164,'raw_key_fact_records':sum(len(a['required_facts']) for a in k['answers']),'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,len(ids),sum(len(a['required_facts']) for a in k['answers']))
