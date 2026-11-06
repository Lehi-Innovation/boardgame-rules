"""Record an actual successful generic batch followup after preserving its preceding draft prefix."""
from pathlib import Path
import json,hashlib,datetime,sys
R=Path(__file__).resolve().parent
D=R/'full-iteration-13'
side=sys.argv[1]
assert side in ['a','b']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=read(D/('batch-progress-'+side+'.json'))
assert p['saved_answer_count']<126
last=p['batches'][-1]
assert sha(Path(last['snapshot']))==last['sha256']
initial=read(D/'dispatch-record.json')
for file,digest in initial['preplanned_protocol_hashes'].items():assert sha(Path(file))==digest
prompt=next(x for x in read(D/'reader-batch-continuation-prompts.json')['records'] if x['reader']==side)
folder=D/('batch-continuations-'+side)
folder.mkdir(exist_ok=True)
record={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reader':side,'target':'/root/source_continuation_reader13_'+side,'after_saved_step':last['step'],'after_saved_answer_count':p['saved_answer_count'],'preceding_snapshot':last['snapshot'],'preceding_snapshot_sha256':last['sha256'],'exact_preplanned_generic_prompt_sha256':prompt['sha256'],'followup_task_successfully_dispatched':True,'same_original_reader_context':True,'requested_continued_model':'gpt-6-luna','requested_continued_effort':'high','actual_runtime_settings_to_be_verified':True,'no_fact_specific_feedback_or_grading':True,'no_runtime_plaintext_message_hash_comparison_claim':True}
with (folder/('after-step-'+str(last['step']).zfill(3)+'.json')).open('x') as f:json.dump(record,f,indent=2);f.write('\n')
counts={s:read(D/('batch-progress-'+s+'.json'))['saved_answer_count'] if (D/('batch-progress-'+s+'.json')).exists() else 0 for s in 'ab'}
for status in [R/'game-status.json',R.parent/'game-status.json']:
    o=read(status);o.update(updated_utc=record['recorded_utc'],phase='full13-preplanned-small-batch-drafting',batch_answers_saved=counts,current_grading_started=False,complete_core_pass=False)
    status.write_text(json.dumps(o,indent=2)+'\n')
print(json.dumps({'reader':side,'continued_after_saved_count':p['saved_answer_count'],'exact_preplanned_prompt':True,'saved_counts':counts,'factual_feedback':False}))
