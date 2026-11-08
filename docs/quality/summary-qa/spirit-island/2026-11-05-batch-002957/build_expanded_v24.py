"""Add the complete independently accepted native preview procedure; preserve prior trials."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import shutil

B=Path(__file__).resolve().parent
OLD,NEW=B/'expanded-v23',B/'expanded-v24'
S=B/'novelty-adjudication-18'
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
a=load(S/'adoption.json');r=load(S/'report.json')
assert a['decisions']=={'R13-G01':'ACCEPT','R13-C01':'ACCEPT','R13-C02':'ACCEPT','R13-C03':'ACCEPT'}
assert a['evidence']['report.json']==H(S/'report.json')
assert load(S/'structural-reference-validation.json')['all_passed']
assert load(S/'actual-delivery-validation.json')['verified']
approved=a['approved_new_question_object']
q,k,f,sc=[load(OLD/n) for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json']]
originals=copy.deepcopy([q,k,f,sc])
assert not NEW.exists() and len(q['questions'])==172
source_refs=[]
evidence={x['id']:x for x in r['evidence']}
images={x['id']:x for x in load(S/'visual-manifest.json')['images']}
for ident in r['gap_decisions'][0]['primary_evidence_ids']:
    if ident in images:
        image=images[ident]
        source_refs.append(image['path']+' | Original printed Spirits May Yet Dream, first threshold and normal earning/resolution parenthetical | SHA256 '+image['full_byte_sha256']+' | native2697x1797; region1080,1080,1810,1610')
    else:
        ev=evidence[ident]
        source_refs.append(ev['path']+' | '+ev['label']+' | SHA256 '+ev['full_byte_sha256']+' | Unicode chars '+':'.join(map(str,ev['unicode_character_range']))+' | passage SHA256 '+ev['utf8_passage_sha256'])
newq={'id':'Q173','question':approved['question']}
newkey={'id':'Q173','answer':approved['predetermined_answer']['answer'],'source_refs':source_refs}
newmap={'id':'Q173','question':newq['question'],'requested_clauses':[{'clause_id':'Q173.1','actual_requested_clause':newq['question'],'required_facts':approved['predetermined_answer']['minimum_asked_facts']}],'key_context_not_required':[{'fact':text,'why_not_requested':'Independent18 expressly excludes these additional requirements from this literal preview-status question.'} for text in approved['predetermined_answer']['no_extra_grading_requirements']]}
newscope={'id':'Q173','scope_result':'base_supported','noncredited_clauses':[],'noncredited_primary_sources':[],'primary_sources':source_refs,'base_producer':r['gap_decisions'][0]['base_reachability'],'independent_source_only_adjudication':{'path':str(S/'adoption.json'),'sha256':H(S/'adoption.json')},'novelty':'One explicit original native preview/status-timing procedure, with two grading facts; not two distinct procedures.'}
q['questions'].append(newq);k['answers'].append(newkey);f['questions'].append(newmap);sc['questions'].append(newscope)
assert q['questions'][:172]==originals[0]['questions'] and k['answers'][:172]==originals[1]['answers'] and f['questions'][:172]==originals[2]['questions'] and sc['questions'][:172]==originals[3]['questions']
assert sum(len(c['required_facts']) for x in f['questions'] for c in x['requested_clauses'])==506
assert dict(collections.Counter(x['scope_result'] for x in sc['questions']))=={'base_supported':156,'mixed_supported_and_noncredited':14,'noncredited_pending_base_proof':3}
q['benchmark_version']=k['benchmark_version']='expanded-v24'
f.update(benchmark='expanded-v24',question_count=173,required_fact_count=506)
sc.update(benchmark='expanded-v24',question_count=173)
sc['scope_revision_v24']={'new_original_core_procedure_question':'Q173','required_grading_facts':506,'all172_prior_scope_objects_exact':True,'question_scope_counts':{'base_supported':156,'mixed_supported_and_noncredited':14,'noncredited_pending_base_proof':3},'prior_clause_accounting_fields_remain_labeled_historical':True,'full_current_independent_confirmation_pending':True}
NEW.mkdir()
for name,value in [('questions.json',q),('answer-key.json',k),('core-scope-credit.json',sc)]:write(NEW/name,value)
f['creator_provenance']={'role':'Complete independently accepted original-native preview procedure addition18','prior_map':str(OLD/'asked-fact-map.json'),'prior_map_sha256':H(OLD/'asked-fact-map.json'),'all172_prior_map_objects_exact':True,'independent_reviewer_saw_no_summary_or_reader_or_grades':True,'parent_knows_historical_failed_trials':True,'no_historical_trial_rescoring':True,'new_question':'Q173','new_required_fact_entries':2,'actual_new_working_zeros_and_NEW_fresh_full_review_required':True}
f['input_hashes']={str(p):H(p) for p in [NEW/'questions.json',NEW/'answer-key.json',OLD/'asked-fact-map.json',S/'report.json',S/'adoption.json']}
write(NEW/'asked-fact-map.json',f)
novelty={'id':'Q173','source_proposal':'R13-G01','question':newq,'predetermined_key':newkey,'minimum_asked_facts':newmap['requested_clauses'][0]['required_facts'],'scope':newscope,'distinct_new_procedures':1,'independent_adjudication_sha256':H(S/'adoption.json'),'no_other_surviving_new_question':True}
write(NEW/'novelty.json',[novelty])
write(NEW/'input-manifest.json',{'question_count':173,'required_fact_count':506,'prior_version':'expanded-v23','all172_prior_questions_keys_maps_and_scope_objects_exact':True,'original20_prompts_and19_original_keys_preserved':True,'versioned_Q18_key_correction_retained':True,'new_questions':['Q173'],'new_required_fact_entries':2,'independent_full_current_confirmation_pending':True,'new_working_two_zero_passes_required':True,'new_fresh_whole_corpus_challenger_required':True,'summary_unchanged_from_C22':True,'sha256':{str(p):H(p) for p in [NEW/n for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json','novelty.json']]+[S/'adoption.json']}})
lines=['# Spirit Island expanded-v24 bank','','173 questions; 506 grading facts. One independently accepted original-native preview procedure added. Only questions go to readers.','']
for question,answer in zip(q['questions'],k['answers']):lines.extend(['## '+question['id'],'',question['question'],'',answer['answer'],'','Sources: '+'; '.join(answer['source_refs']),''])
(NEW/'question-bank.md').write_text('\n'.join(lines)+'\n')

def correct_claims(m):
    changes=[]
    for decision in r['classification_decisions']:
        ident=decision['proposal_id'];old=decision['full_literal_proposal']
        if ident=='R13-C01':
            rows=[x for x in m['book_passages'] if x['passage']=='Optional timeboxing'];assert len(rows)==1
            row=rows[0];before=copy.deepcopy(row);assert row['question_ids']==[] and row['scope']=='excluded'
            row['question_ids']=['Q172'];row['scope']=decision['approved_replacement_object']['scope'];row['scope_note']=decision['approved_replacement_text']
        else:
            qid='Q116' if ident=='R13-C02' else 'Q142'
            rows=[x for x in m['precise_clause_mappings'] if qid in x['question_ids']];assert len(rows)==1
            row=rows[0];before=copy.deepcopy(row);assert old['old_text'] in row['topic']
            row['topic']=decision['approved_replacement_text'];row['scope_qualification']=decision['approved_replacement_object']
        changes.append({'proposal_id':ident,'old_complete_claim':before,'new_complete_claim':copy.deepcopy(row)})
    return changes

m=load(B/'coverage-map-for-review-13.json');changes=correct_claims(m)
m.update(benchmark='expanded-v24',question_count=173)
m['precise_clause_mappings'].append({'topic':'Original Bringer preview changes visibility, preserving ordinary earning and resolution.','source_refs':source_refs,'question_ids':['Q173'],'tested_clause':newq['question']})
m['current_map_caution']='Working source-to-question claims only; actual literal questions determine coverage. Q116/Q142 unsupported-producer branches remain fully graded with zero current-base novelty.'
m['stopping_rule']={'status':'RESET_AFTER_VALIDATED_Q173_ADDITION','working_zero_passes_required':2,'NEW_fresh_challenge_required_after_final_addition':True,'current_independent_PASS':False}
write(B/'coverage-map-for-working-45-46.json',m)
write(NEW/'coverage-claim-corrections.json',{'complete_accepted_set':changes,'source_adjudication_sha256':H(S/'adoption.json'),'no_existing_question_key_map_or_scope_requirement_changed':True})
rich=load(B/'coverage-ledger.json');backup=B/'coverage-ledger-before-v24-preview-addition.json';assert not backup.exists();shutil.copyfile(B/'coverage-ledger.json',backup)
rich_changes=correct_claims(rich)
rich['historical_stopping_rule_before_v24_preview_addition']=copy.deepcopy(rich['stopping_rule'])
rich.update(benchmark='expanded-v24',question_count=173)
rich['stopping_rule']=copy.deepcopy(m['stopping_rule'])
rich['precise_clause_mappings'].append(copy.deepcopy(m['precise_clause_mappings'][-1]))
rich['preview_addition_v24']={'new_question':novelty,'complete_claim_corrections':rich_changes,'prior_rich_ledger_snapshot':str(backup),'prior_rich_ledger_sha256':H(backup),'actual_new_working_zeros_pending':True,'NEW_fresh_independent_challenge_pending':True}
rich['pretest_asked_fact_mapping_v24']={'path':str(NEW/'asked-fact-map.json'),'sha256':H(NEW/'asked-fact-map.json'),'facts':506,'prior_fields_are_history':True}
write(B/'coverage-ledger.json',rich)
write(B/'build-status-v24.json',{'benchmark':'expanded-v24','questions':173,'required_fact_entries':506,'new_questions':['Q173'],'all172_prior_question_key_map_scope_objects_exact':True,'complete_three_classification_corrections_applied':True,'source_body_unchanged_C22':True,'new_working_zeros_and_NEW_fresh_challenge_pending':True})
print(json.dumps({'benchmark':'expanded-v24','question_count':173,'required_fact_count':506,'new_question':'Q173','new_required_facts':2,'sha256':{n:H(NEW/n) for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json']}}))
