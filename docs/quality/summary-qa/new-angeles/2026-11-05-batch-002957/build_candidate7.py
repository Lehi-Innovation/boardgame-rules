from pathlib import Path
import datetime, hashlib, json, shutil
B=Path(__file__).parent; O=B/'expanded-candidate-v6'; V=B/'expanded-candidate-v7'
assert not V.exists(); V.mkdir()
for name in ['questions.json','answer-key.json','asked-clause-map.json','coverage-map.json','coverage-ledger.json']:
    shutil.copyfile(O/name,V/name)
q=json.loads((V/'questions.json').read_text());k=json.loads((V/'answer-key.json').read_text());s=json.loads((V/'asked-clause-map.json').read_text())
km={x['id']:x for x in k['answers']};sm={x['id']:x for x in s}
sm['Q27']['asked_facts'][0]="At end of each deal, including another player's, zero hand actions allows an optional draw of the owner's sheet's topmost action type."
sm['Q27']['contextual_background'].append('The draw quantity is one card; this correct quantity is not separately requested. A volunteered false quantity remains a material contradiction.')
sm['Q46']['asked_facts'][1]='If the chosen player wins the deal, the Jackson user gains capital.'
sm['Q46']['contextual_background'].append('The payment is two capital; its quantity is not separately requested. A volunteered false amount remains a material contradiction.')
for i in ['Q27','Q46']:
    km[i]['required_facts']=sm[i]['asked_facts'].copy();km[i]['contextual_background']=sm[i]['contextual_background'].copy()
q['benchmark_version']=k['benchmark_version']='expanded-candidate-v7'
for n,o in [('questions.json',q),('answer-key.json',k),('asked-clause-map.json',s)]: (V/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
p=B/'full-bank-scope-validator/revision-02/scope-review.json';r=json.loads(p.read_text())
change={'from':'candidate-v6','to':'candidate-v7','count':93,'question_entries_unchanged':True,'expected_answers_unchanged':True,'changed_required_scope_ids':['Q27','Q46'],'source_outcomes_changed':False,'new_questions':[],'historical_inputs_preserved':True,'readers_not_yet_run':True,'review_path':str(p.resolve()),'review_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all13_prior_findings_confirmed_addressed':r['original_13_findings_all_addressed'],'corrections':r['new_findings_and_proposed_versioned_corrections']}
(V/'version-changes.json').write_text(json.dumps(change,indent=2,ensure_ascii=False)+'\n')
l=json.loads((V/'coverage-ledger.json').read_text());l['scope_version_corrections_v7']={'demoted_unasked_quantities':['Q27 draw one','Q46 gain two'],'no_rule_outcome_or_novelty_change':True};l['stopping_rule']['NEW_scope_validator']='v6 confirms all13 prior findings; v7 applies2 newly noticed unasked quantities; final narrow confirmation pending';(V/'coverage-ledger.json').write_text(json.dumps(l,indent=2)+'\n')
parts=['# New Angeles candidate bank v7','93 entries; two additional unasked quantities moved to context before testing. All v6 question wording and expected answers are preserved. SG01 remains pending.']
for x in q['questions']:
    i=x['id'];parts += ['## '+i,x['question'],'**Required answer facts:**\n\n'+'\n'.join('- '+f for f in sm[i]['asked_facts']),'**Sources:** '+'; '.join(km[i]['source_refs'])]
(V/'question-bank.md').write_text('\n\n'.join(parts)+'\n')
names=['questions.json','answer-key.json','asked-clause-map.json','coverage-map.json','coverage-ledger.json','question-bank.md','version-changes.json']
(V/'input-manifest.json').write_text(json.dumps({'status':'candidate frozen for final scope/source confirmation','question_count':93,'hashes':{n:hashlib.sha256((V/n).read_bytes()).hexdigest() for n in names},'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
p=B/'progress.json';d=json.loads(p.read_text());d['candidate_bank_path']=str(V.resolve());d['phase']='candidate_v7_scope_confirmation_pending';p.write_text(json.dumps(d,indent=2)+'\n');print('Created v7, questions and expected answers unchanged from v6.')
