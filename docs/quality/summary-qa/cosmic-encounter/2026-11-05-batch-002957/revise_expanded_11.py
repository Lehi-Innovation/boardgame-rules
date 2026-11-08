from pathlib import Path
import copy
import hashlib
import json

R=Path(__file__).parent;OLD=R/'expanded-candidate-10';OUT=R/'expanded-candidate-11'
assert not OUT.exists();OUT.mkdir()
def read(p):return json.loads(p.read_text())
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json')
q['benchmark_version']=k['benchmark_version']=OUT.name
changes=[]
for ident in ['Q033','Q151']:
    i=next(i for i,e in enumerate(q['questions']) if e['id']==ident)
    oldq,oldk=copy.deepcopy(q['questions'][i]),copy.deepcopy(k['answers'][i])
    if ident=='Q033':
        k['answers'][i]['required_facts'].append('The losing player chooses ships under their control outside the encounter, ordinarily ships on their colonies in this original-base scope.')
        k['answers'][i]['source_references'] += ['2018 FAQ p5 extraction lines419–423 and450–453; original Gambler sheet excludes ships involved in the encounter.']
        group=0;reason='Explicitly supply positive holdings for an already-asked source-location clause; non-exhaustive ordinarily, no invented new holding rule.'
    else:
        q['questions'][i]['question']+=' For the special destiny card illustrated on page7 of the original rulebook, what criterion selects the defense, may the offense qualify, how are ties broken, and where must the encounter take place?'
        k['answers'][i]['required_facts'] += ['Select the player with the most current foreign colonies.','The offense itself is excluded.','Break a tie to the offense\'s left: use the first tied eligible player in that direction.','The encounter takes place in the selected other player\'s home system.']
        k['answers'][i]['source_references'] += ['Original rulebook p7 illustrated special destiny card, extraction lines603–612.']
        group=1;reason='One coherent illustrated-card selection procedure, including its distinct leftward target-selection priority. Printed home-system location overlaps ordinary destination rules and adds no separate novelty group.'
    changes.append({'id':ident,'before_question':oldq,'before_key':oldk,'after_question':q['questions'][i],'after_key':k['answers'][i],'qualifying_new_rule_groups':group,'reason':reason})
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions']
assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
assert len(q['questions'])==164 and sum(len(a['required_facts']) for a in k['answers'])==531
save('questions.json',q);save('answer-key.json',k)
save('versioned-corrections.json',{'parent_version':OLD.name,'original_twenty_preserved_verbatim':True,'new_rule_groups':1,'key_precision_corrections_not_new_rules':1,'all_changes_before_any_expanded_blind_pair':True,'changes':changes,'source_decisions':['source-review/current10-rulebook-check-03.json','source-review/gambler-source-precision-02.json','source-review/peer-blind-actual-scope-review-09.json']})
ledger=read(OLD/'acceptance-rejection-ledger.json')
for c in changes:ledger.append({'candidate':'illustrated-special-selection' if c['id']=='Q151' else 'Gambler-positive-source-holdings','question_id':c['id'],'decision':'accepted-source-backed-new-group' if c['qualifying_new_rule_groups'] else 'accepted-source-backed-key-precision','new_rule_groups':c['qualifying_new_rule_groups'],'reason':c['reason'],'primary_sources':c['after_key']['source_references']})
save('acceptance-rejection-ledger.json',ledger)
for n in ['candidate-question-map.json','withdrawn-question-ledger.json']:
    d=read(OLD/n)
    if n=='candidate-question-map.json':d.update({'illustrated-special-selection':'Q151','Gambler-positive-source-holdings':'Q033'})
    save(n,d)
coverage=read(OLD/'coverage-map.json');coverage.update(bank_version=OUT.name,question_count=164,status='Illustrated special selection procedure and Gambler key precision incorporated; current union/scope amendment and renewed stopping checks pending. Human choices unresolved.')
coverage['latest_changes']=changes;save('coverage-map.json',coverage)
passes=read(OLD/'targeted-coverage-passes-after-review.json');passes['status']='Counter reset for one new illustrated-card selection procedure; Gambler precision adds no new group.'
passes['passes'].append({'pass':16,'focus':'Current10 complete source/scope challenge','qualifying_rule_groups':1,'extended_questions':['Q151'],'key_precision_only':['Q033'],'stopping_counter_reset':True})
save('targeted-coverage-passes.json',passes)
(OUT/'question-bank.md').write_text('# Expanded candidate 11 — current review pending\n\n'+'\n\n'.join(f"## {qe['id']}\n\n{qe['question']}\n\n"+'\n'.join('- '+f for f in ke['required_facts']) for qe,ke in zip(q['questions'],k['answers']))+'\n')
save('input-manifest.json',{'review_candidate_only':True,'question_count':164,'raw_key_fact_records':531,'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,164,531)
