from pathlib import Path
import copy
import hashlib
import json

R=Path(__file__).parent;OLD=R/'expanded-candidate-11';OUT=R/'expanded-candidate-12'
assert not OUT.exists();OUT.mkdir()
def read(p):return json.loads(p.read_text())
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json')
q['benchmark_version']=k['benchmark_version']=OUT.name
i=next(i for i,e in enumerate(q['questions']) if e['id']=='Q104')
oldq,oldk=copy.deepcopy(q['questions'][i]),copy.deepcopy(k['answers'][i])
q['questions'][i]['question']+=' For otherwise legal uses, what timing phrases does the official FAQ quote for the effects of Kamikaze Super, Machine Super, Masochist Super, Miser Super and Cudgel Super? For the first three, does the quoted wording refer to every player\'s Regroup or to the user\'s own Regroup phases?'
k['answers'][i]['required_facts'] += ['Kamikaze Super, Machine Super and Masochist Super quote during each of your Regroup phases: the user\'s own Regroup phases, not every player\'s.','Miser Super quotes at the start of each of your encounters.','Cudgel Super quotes whenever you use your power.']
k['answers'][i]['contextual_background'] += ['These are the quoted effect timing/owner/event clauses, not a reconstruction of when the flare may first be placed faceup or of its absent full effect, role, prerequisites, cost or target. Miser\'s start-of-each-own-encounter wording is not relabeled as the once-per-turn Start Turn step.']
k['answers'][i]['source_references'] += ['2018 FAQ p16 extraction1470–1473/1551–1554; p17 1581–1584; p18 1653–1656; p12 1125–1127.']
qe={'id':'Q166','question':'For the Fido flare effect specifically described in the official FAQ as forcing a player to draw from the discard pile, does the card come from the top of that pile, at random, or from a freely chosen position?'}
ke={'id':'Q166','required_facts':['The forced draw described by the FAQ takes the top card of the discard pile.'],'contextual_background':['The source calls this Fido flare without identifying Wild versus Super. No full trigger, role, phase, target-selection permission, cost or remaining effect is supplied.'],'source_references':['2018 FAQ p4 extraction lines280–287, Fido flare described as forcing a top-discard draw.']}
q['questions'].append(qe);k['answers'].append(ke)
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions']
assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
assert len(q['questions'])==165 and sum(len(a['required_facts']) for a in k['answers'])==535
save('questions.json',q);save('answer-key.json',k)
corrections={'parent_version':OLD.name,'original_twenty_preserved_verbatim':True,'new_bounded_source_proposals':2,'new_question_count':1,'extended_question_ids':['Q104'],'all_changes_before_expanded_blind_pair':True,'changes':[{'id':'Q104','before_question':oldq,'before_key':oldk,'after_question':q['questions'][i],'after_key':k['answers'][i]},{'id':'Q166','before_question':None,'before_key':None,'after_question':qe,'after_key':ke}],'source_challenge':'source-review/current10-faq-check-05.json'}
save('versioned-corrections.json',corrections)
ledger=read(OLD/'acceptance-rejection-ledger.json')
for ident,label,reason in [('Q104','quoted-Super-effect-timing-owner-event','Replay-per-encounter was asked, but not the independently quoted own-Regroup, own-encounter-start and power-use-event boundaries. Bundle common wording rather than split by name.'),('Q166','Fido-flare-top-discard-acquisition','Pile ordering was asked by Q077, but the expressly described forced top-card acquisition was not; no flare side or absent full effect invented.')]:
    ledger.append({'candidate':label,'question_id':ident,'decision':'accepted-bounded-direct-primary-clause','reason':reason,'source_review':'source-review/current10-faq-check-05.json'})
save('acceptance-rejection-ledger.json',ledger)
for n in ['candidate-question-map.json','withdrawn-question-ledger.json']:
    d=read(OLD/n)
    if n=='candidate-question-map.json':d.update({'quoted-Super-effect-timing-owner-event':'Q104','Fido-flare-top-discard-acquisition':'Q166'})
    save(n,d)
coverage=read(OLD/'coverage-map.json');coverage.update(bank_version=OUT.name,question_count=165,status='Two bounded FAQ clause additions incorporated; complete operative-fragment census, union overlaps and scope amendment pending. Human choices unresolved.')
coverage['latest_faq_clauses']=corrections;save('coverage-map.json',coverage)
passes=read(OLD/'targeted-coverage-passes.json');passes['status']='Stopping counter reset; latest rulebook and FAQ findings incorporated before renewed checks.'
passes['passes'].append({'pass':17,'focus':'Current10 complete FAQ/history rechallenge','accepted_bounded_proposals':2,'extended_questions':['Q104'],'new_questions':['Q166'],'stopping_counter_reset':True})
save('targeted-coverage-passes.json',passes)
(OUT/'question-bank.md').write_text('# Expanded candidate 12 — operative-source review pending\n\n'+'\n\n'.join(f"## {qa['id']}\n\n{qa['question']}\n\n"+'\n'.join('- '+f for f in ka['required_facts']) for qa,ka in zip(q['questions'],k['answers']))+'\n')
save('input-manifest.json',{'review_candidate_only':True,'question_count':165,'raw_key_fact_records':535,'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,165,535)
