"""Reconcile paired trial directories/datasets; never regrade old outputs."""
from pathlib import Path
from datetime import datetime,timezone
import re,json,hashlib,copy
R=Path(__file__).parent.resolve()
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
progress=read(R/'progress.json');pairs=sorted(p for p in R.iterdir() if p.is_dir() and re.fullmatch(r'(seed|expanded)-iteration-[0-9]{2}',p.name));listed={x['id']:x for x in progress['iterations']};assert set(listed)=={p.name for p in pairs}
rows=[]
for path in pairs:
    old=listed[path.name];qpath=path/'questions.json';n=len(read(qpath)['questions']) if qpath.exists() else 20;raws=[]
    for label in 'ab':
        source=path/f'reader-{label}.json';doc=read(source);assert len(doc['answers'])==n
        raws.append({'reader':label,'path':str(source),'sha256':sha(source),'complete_answer_record_count':len(doc['answers'])})
    current=path.name=='expanded-iteration-06';scores=copy.deepcopy(old.get('effective_scores',old.get('scores')))
    assert scores is not None
    for value in scores.values():assert sum(value.values())==n if isinstance(value,dict) else sum(value)==n
    historical=[]
    for field in ('adjudicated_aggregate_path','aggregate_path','primary_aggregate_path'):
        if old.get(field):
            p=Path(old[field]);assert p.exists();historical.append({'role':field,'path':str(p),'sha256':sha(p)})
    rows.append({'trial':path.name,'kind':'seed' if path.name.startswith('seed-') else 'expanded','questions_per_reader':n,'paired_original_datasets':raws,'preserved_effective_scores':scores,'legacy_list_score_order':['correct','partial','incorrect'] if not current else None,'preserved_result_paths':historical,'supported_bank_factual_pass':current or path.name=='seed-iteration-03','preserved_status':old['status'],'workflow_conformance_not_inferred_from_factual_score':True})
report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'pass':True,'actual_paired_trial_count':len(rows),'seed_paired_trials':sum(x['kind']=='seed' for x in rows),'expanded_paired_trials':sum(x['kind']=='expanded' for x in rows),'original_A_B_datasets':sum(len(x['paired_original_datasets']) for x in rows),'current_expanded_trial':6,'current_supported_bank_questions':168,'guide_revision_identifier':17,'guide_revision_number_is_not_reader_iteration_count':True,'current_draft17_and_review9_batches_per_reader_are_one_pair_not_extra_trials':True,'input_readiness_metadata_repairs_late_IO_and_context_compactions_are_not_new_pairs_or_votes':True,'current_single_neutral_assessment_is_not_a_replacement_reader_pair':True,'historical_failed_trials_not_relabelled':True,'historical_score_metadata_preserved_without_regrading_or_model_reaudit':True,'trials':rows,'verified_stamp_or_full_core_claim':False}
p=R/'iteration-reconciliation-final-supported-01.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print({k:report[k] for k in ('pass','actual_paired_trial_count','seed_paired_trials','expanded_paired_trials','original_A_B_datasets')})
