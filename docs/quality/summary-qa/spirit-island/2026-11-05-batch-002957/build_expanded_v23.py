"""Apply the complete independently accepted focused precision review for future trials."""
from pathlib import Path
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
OLD, NEW = B/'expanded-v22', B/'expanded-v23'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
def write(p, value):
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

S = B/'scope-precision-17'
adoption = load(S/'adoption.json')
assert adoption['status'] == 'ADOPTED_FOCUSED_SOURCE_ONLY_MAP_PRECISION'
assert adoption['report_sha256'] == H(S/'report.json')
assert load(S/'structural-reference-validation.json')['all_passed']
assert load(S/'actual-delivery-validation.json')['all_actual_source_slices_verified']
r = load(S/'report.json')
q,k,f,sc = [load(OLD/n) for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json']]
originals = copy.deepcopy([q,k,f,sc])
assert not NEW.exists()
corrections = {x['question_id']:x for x in r['consolidated_corrections']}
assert set(corrections) == set(adoption['complete_accepted_set'])
for row in f['questions']:
    if row['id'] not in corrections:
        continue
    c = corrections[row['id']]
    for clause in row['requested_clauses']:
        newclause = next(x for x in c['requested_clauses'] if x['clause_id'] == clause['clause_id'])
        clause['required_facts'] = copy.deepcopy(newclause['required_facts'])
    # Keep existing contexts byte-for-object; append every newly classified item.
    existing = row['key_context_not_required']
    additions = [copy.deepcopy(x) for x in c['key_context_not_required'] if 'original_context_index' not in x]
    row['key_context_not_required'] = existing + additions

changed = [x['id'] for x,y in zip(f['questions'],originals[2]['questions']) if x != y]
assert changed == list(corrections)
assert q['questions'] == originals[0]['questions'] and k['answers'] == originals[1]['answers']
assert sc['questions'] == originals[3]['questions']
assert len(q['questions']) == 172
assert sum(len(c['required_facts']) for x in f['questions'] for c in x['requested_clauses']) == 504
q['benchmark_version'] = k['benchmark_version'] = 'expanded-v23'
f.update(benchmark='expanded-v23',question_count=172,required_fact_count=504)
sc['benchmark'] = 'expanded-v23'
sc['scope_revision_v23'] = {'map_precision_ids':changed,'all172_scope_question_objects_exact':True,'question_scope_counts_unchanged':True,'grading_fact_entries':504,'prior_v21_v22_clause_counts_are_historical':True,'three_old_required_entries_removed_or_merged':{'Q48':3,'Q79':3,'Q101':2},'new_base_novelty':0,'independent_whole_corpus_and_current_scope_confirmation_pending':True}
NEW.mkdir()
for name,value in [('questions.json',q),('answer-key.json',k),('core-scope-credit.json',sc),('novelty.json',[])]:
    write(NEW/name,value)
f['creator_provenance'] = {'role':'Complete independently accepted source-only precision17 corrections for future trials','prior_map':str(OLD/'asked-fact-map.json'),'prior_map_sha256':H(OLD/'asked-fact-map.json'),'independent_review':str(S/'report.json'),'independent_review_sha256':H(S/'report.json'),'independent_reviewer_saw_reader_or_grade_data':False,'parent_knows_failed_expanded_trial_history':True,'no_historical_trial_rescoring':True,'all172_question_and_fixed_key_objects_exact':True,'all161_other_map_objects_exact':True,'independent_full_current_bank_and_corpus_confirmation_pending':True}
f['input_hashes'] = {str(p):H(p) for p in [NEW/'questions.json',NEW/'answer-key.json',OLD/'asked-fact-map.json',S/'report.json',S/'adoption.json']}
write(NEW/'asked-fact-map.json',f)
write(NEW/'map-corrections.json',{'prior_version':'expanded-v22','new_version':'expanded-v23','complete_accepted_set':r['consolidated_corrections'],'reason':'Independent literal-ask classification of complete focused set; both reductions of unasked context and a genuine operative Energy amount included. Not retroactive rescoring.','all172_question_key_scope_objects_exact':True,'all161_unaffected_map_entries_exact':True,'required_fact_entries_before_after':[507,504],'new_questions':0,'new_procedure_claims':0,'whole_current_bank_and_corpus_confirmation_pending':True})
write(NEW/'input-manifest.json',{'question_count':172,'required_fact_count':504,'prior_version':'expanded-v22','changed_map_ids':changed,'all172_question_key_scope_objects_exact':True,'original20_prompts_preserved':True,'all_explicit_historical_key_scope_transcription_corrections_retained':True,'no_historical_trial_rescoring':True,'new_procedure_questions':0,'new_reader_trial_started':False,'whole_current_bank_and_corpus_confirmation_pending':True,'sha256':{str(p):H(p) for p in [NEW/n for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json','map-corrections.json']]}})
lines=['# Spirit Island expanded-v23 bank','','172 unchanged questions; 504 required grading fact entries. Evaluator data; only questions go to readers.','']
for question,answer in zip(q['questions'],k['answers']):
    lines.extend(['## '+question['id'],'',question['question'],'',answer['answer'],'','Sources: '+'; '.join(answer['source_refs']),''])
(NEW/'question-bank.md').write_text('\n'.join(lines)+'\n')
write(B/'build-status-v23.json',{'benchmark':'expanded-v23','questions':172,'required_fact_entries':504,'all172_question_key_scope_objects_exact':True,'changed_map_ids':changed,'whole_current_bank_and_corpus_confirmation_pending':True})
print(json.dumps({'benchmark':'expanded-v23','question_count':172,'required_fact_count':504,'changed_map_ids':changed,'sha256':{n:H(NEW/n) for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json']}}))
