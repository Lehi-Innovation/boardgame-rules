from pathlib import Path
import copy
import hashlib
import json

R=Path(__file__).parent;OLD=R/'expanded-candidate-12';OUT=R/'expanded-candidate-13'
assert not OUT.exists();OUT.mkdir()
def read(p):return json.loads(p.read_text())
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json');q['benchmark_version']=k['benchmark_version']=OUT.name
i=next(i for i,e in enumerate(q['questions']) if e['id']=='Q121');oldq,oldk=copy.deepcopy(q['questions'][i]),copy.deepcopy(k['answers'][i])
q['questions'][i]['question']+=' Does its otherwise legal second-encounter guarantee still apply if the completed first encounter was unsuccessful, such as a loss or failed deal?'
k['answers'][i]['required_facts'].append('Yes: when otherwise legal Machine Wild applies to this turn, its guarantee permits a second encounter despite a completed first loss or failed deal; the ordinary first-success condition does not defeat that guarantee.')
k['answers'][i]['contextual_background'].append('The legal-use/applicability condition is supplied. No full trigger, role, first-placement window, additional encounters beyond the second or remaining flare text is reconstructed.')
k['answers'][i]['source_references'] += ['2018 FAQ p16 extraction1543–1550, unqualified second-encounter guarantee and needed new hand; p17 1559–1561, quoted you may always have a second encounter; original rulebook p7/p11 ordinary first-success eligibility.']
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions'];assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
assert len(q['questions'])==165 and sum(len(a['required_facts']) for a in k['answers'])==536
save('questions.json',q);save('answer-key.json',k)
change={'parent_version':OLD.name,'question_id':'Q121','before_question':oldq,'before_key':oldk,'after_question':q['questions'][i],'after_key':k['answers'][i],'new_qualifying_outcome_clause':1,'reason':'Previous replacement question supplied the guarantee as a given; it did not ask whether the ordinary first-failure condition defeats it.','primary_support':'Unqualified guarantee plus quoted may always; otherwise legal-use condition preserved, no activation window or full card reconstructed.','independent_source_adjudication':'source-review/machine-wild-guarantee-source-adjudication-07.json','all_changes_before_expanded_blind_pair':True,'original_twenty_preserved_verbatim':True}
save('versioned-corrections.json',change)
ledger=read(OLD/'acceptance-rejection-ledger.json');ledger.append({'candidate':'Machine-Wild-after-completed-first-failure','question_id':'Q121','decision':'accept-bounded-source-backed-outcome','reason':change['reason'],'source_adjudication':change['independent_source_adjudication']});save('acceptance-rejection-ledger.json',ledger)
for n in ['candidate-question-map.json','withdrawn-question-ledger.json']:
    d=read(OLD/n)
    if n=='candidate-question-map.json':d['Machine-Wild-after-completed-first-failure']='Q121'
    save(n,d)
coverage=read(OLD/'coverage-map.json');coverage.update(bank_version=OUT.name,question_count=165,status='Machine guarantee outcome added; complete-source closure and own scope amendment pending; no final freeze or human policy adopted.');coverage['machine_guarantee_outcome']=change;save('coverage-map.json',coverage)
passes=read(OLD/'targeted-coverage-passes-after-review.json');passes['status']='Counter reset for one Machine Wild guarantee outcome.';passes['passes'].append({'pass':20,'focus':'Full FAQ operative-fragment census','qualifying_rule_additions':1,'extended_questions':['Q121'],'stopping_counter_reset':True});save('targeted-coverage-passes.json',passes)
(OUT/'question-bank.md').write_text('# Expanded candidate 13 — source closure pending\n\n'+'\n\n'.join(f"## {qa['id']}\n\n{qa['question']}\n\n"+'\n'.join('- '+f for f in ka['required_facts']) for qa,ka in zip(q['questions'],k['answers']))+'\n')
save('input-manifest.json',{'review_candidate_only':True,'question_count':165,'raw_key_fact_records':536,'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,165,536)
