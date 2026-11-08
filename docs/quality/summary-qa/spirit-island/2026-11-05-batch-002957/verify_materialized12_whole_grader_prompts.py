"""Bind materialized whole grader inputs to prospectively read instructions; execute only after final freeze."""
from pathlib import Path
import copy,datetime,hashlib,json
B=Path(__file__).resolve().parent
D=B/'expanded-iteration-12'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
for r in 'ab':
 assert H(D/f'reader-{r}.json')==H(D/f'reader-{r}-original-completed.json')==load(D/f'reader-{r}-original-freeze.json')['sha256']
 assert load(D/f'reader-{r}.json')['stage']=='complete'
prior=load(B/'expanded12-planned-grader-prompts-v2/parent-full-instruction-read-receipt.json')
rows=[]
for n in range(1,10):
 block=D/'grading'/f'block-{n:02}'
 planned=B/'expanded12-planned-grader-prompts-v2'/f'block-{n:02}-prompt.txt'
 actual=block/'grader-prompt.txt'
 assert actual.read_bytes()==planned.read_bytes()
 pre=next(x for x in prior['prompts'] if x['block']==n)
 assert H(actual)==pre['sha256'] and pre['all_whole_native_instructions_actually_read']
 original=load(block/'raw-answers.json')['readers']
 ids=load(block/'input-manifest.json')['expected_ids']
 for r in ['reader-a','reader-b']:
  full=load(D/(r+'.json'))
  assert original[r]['answers']==[a for a in full['answers'] if a['id'] in ids]
 rows.append({'block':n,'actual_prompt':str(actual),'sha256':H(actual),'characters':len(actual.read_text()),'byte_equal_pre_answer_whole_native_reviewed_prompt':True,'actual_pre_answer_read_events':copy.deepcopy(pre['actual_full_read_events']),'both_whole_original_entry_subsets_exact':True})
p=D/'grading/prompts-parent-preflight.json'
assert not p.exists()
p.write_text(json.dumps({'all9_actual_whole_prompts_byte_equal_pre_answer_parent_review':True,'all346_entire_original_reader_entries_preserved':True,'all_original_field_and_quotation_delivery_required':True,'blocks':rows},indent=2)+'\n')
p=D/'grading/dispatch-log.json'
assert not p.exists()
p.write_text(json.dumps({'dispatch_events':[],'subsequent_captured_profiles':[],'all9_dispatched':False,'pending_blocks':list(range(1,10)),'completed_original_frozen_blocks':[],'active_blocks':[],'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
print(json.dumps({'whole_native_prompt_continuity_9PASS':True,'entire_original_subsets_346PASS':True,'no_graders_dispatched':True}))
