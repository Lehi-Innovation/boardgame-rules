from pathlib import Path
import datetime
import hashlib
import json
import shutil

B=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):p.write_text(json.dumps(value,indent=2)+'\n')
p=B/'progress.json';pr=load(p)
shutil.copyfile(p,B/'progress-before-v24-Q173-addition.json')
pr.update(phase='v24-Q173-frozen-working45-46-active-source-C22-unchanged-pure11-PASS',question_count=173,current_bank='expanded-v24',current_required_fact_count=506)
pr['historical_stopping_rule_before_validated_Q173_addition']=pr['coverage_stopping_rule']
pr['coverage_stopping_rule']={'passes':[],'new_questions':[],'status':'RESET_AFTER_VALIDATED_NEW_Q173','independent_challenge':'NEW_FRESH_REVIEW_REQUIRED_AFTER_NEW_TWO_WORKING_ZEROS','old43_44_only_historical172_questions':True}
pr['coverage_review'].update(benchmark='expanded-v24',status='PENDING_NEW_WORKING_ZEROS_AND_NEW_FRESH_REVIEW',current_PASS=False,historical13_FAIL_adoption='scope13-adoption.json',question_count=173,required_fact_count=506)
pr['scope_check']={'status':'PENDING_NEW_FULL_CURRENT173_REVIEW','current_benchmark':'expanded-v24','current_questions':173,'current_required_facts':506,'historical13_keys_map_PASS_only_v23':True}
pr['hashes'].update({key:H(B/'expanded-v24'/name) for key,name in [('questions_sha256','questions.json'),('answer_key_sha256','answer-key.json'),('asked_fact_map_sha256','asked-fact-map.json'),('core_scope_credit_sha256','core-scope-credit.json')]})
pr['novelty_adjudication18'].update(status='COMPLETE_ADOPTED_FOUR_ACCEPT',adoption='novelty-adjudication-18/adoption.json',new_question_added='Q173')
pr['working45_46']={'status':'ACTIVE','agent':'/root/novelty_adjudication_18','role':'Working continuation after completed independent source-only adjudication; not the NEW fresh final challenger.','input_manifest':'working45-46-input-manifest.json','native_full_prompt':'working-source-sweeps-45-46-prompt.txt','prompt_sha256':H(B/'working-source-sweeps-45-46-prompt.txt'),'prompt_characters':5690,'root_full_prompt_read_chunk':'da2ebc','native_literal_full_followup':True,'prior_adjudication_runtime_boundary':'novelty-adjudication-18/completed-runtime-boundary.json','actual_counts_pending':True}
pr['planned_body_clarification_after_working_survivor_consolidation']={'status':'NOT_APPLIED','source':'Original Bringer panel normal earning/resolution parenthetical, independently accepted18','intent':'State preview changes visibility without earning the card or resolving Fear early; preserve already-earned-card behavior.','requires_NEW_fresh_pure_source_auditor_when_applied':True,'current_C22_pure11_PASS_remains_current_until_body_changes':True}
pr['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(p,pr)
p=B/'pending-work-state.json';pending=load(p)
shutil.copyfile(p,B/'pending-work-state-before-v24-addition.json')
pending['phase']=pr['phase']
pending['current_bank']={'version':'expanded-v24','questions':173,'required_grading_fact_entries':506,'full_pair_fact_assessments_if_unchanged':1012,'all172_prior_question_key_map_scope_objects_exact':True,'scope_question_counts':{'base_supported':156,'mixed_supported_and_noncredited':14,'noncredited_pending_base_proof':3},'new_question':'Q173','current_stopping_PASS':False}
pending['active_agents']=[{'agent':'/root/novelty_adjudication_18','role':'Actual working sweeps45/46 after completed independent adjudication; own prior source reuse only.','outputs':['working-source-sweeps-45-46.json','working-source-sweeps-45-46-read-ledger.json','working-source-sweeps-45-46-visual-manifest.json']}]
pending['current_candidate']['source11_gate']='PASS_ADOPTED_EXACT_C22'
pending['source11_adoption']='source-audit11-adoption.json'
pending['source13']={'adoption':'scope13-adoption.json','keys_map':'PASS_v23_172_504','coverage_stopping':'FAIL_one_gap','counts':load(B/'scope13-structural-reference-validation.json')['counts']}
pending['source18']={'adoption':'novelty-adjudication-18/adoption.json','all_four':'ACCEPT','new_question_applied':'Q173','new_facts':2,'counts':load(B/'novelty-adjudication-18/structural-reference-validation.json')['counts'],'original_completed_runtime_boundary_records':549,'later_working_phase_does_not_retroactively_change_that_adjudication':True}
pending['planned_body_clarification']=pr['planned_body_clarification_after_working_survivor_consolidation']
pending['next_steps']=[
    'Validate completed actual working45/46 complete source delivery, own-source reuse and actual counts; no assumed zeros.',
    'If any new gaps, independently adjudicate complete survivors and add every genuine new procedure, then repeat two actual working zeros after final additions.',
    'After full working survivor consolidation, apply the source-backed Bringer preview clarity sentence; NEW pure source auditor required for that changed body.',
    'After actual current173 (or later) working0/0, dispatch NEW fresh whole-corpus/key/map/scope challenger. Source13 originalFAIL and all prior zeros remain historical.',
    'Only after current exact source and coverage gates PASS freeze mandatory NEW full Luna/high/none pair using v12 pre-authoring actual-delivery checkpoint. Then9 balanced fresh Sol/high/none grading blocks, all actual facts once per reader and complete borderline adjudication.',
    'Retain failed02/03, all raw reports, grading and metadata deviations, rewrite final report coherently, keep goalACTIVE until coordinator stamp/exact-byte QA authorization.'
]
write(p,pending)
print('Current173/506 state and reset stopping gates saved; no new reader pair or body change.')
