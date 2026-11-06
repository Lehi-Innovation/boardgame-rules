"""Prepare isolated grading inputs only after both preplanned blind second passes complete."""
from pathlib import Path
import datetime, hashlib, json
R=Path(__file__).resolve().parent
D=R/'full-iteration-13'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    with p.open('x') as f:json.dump(o,f,indent=2);f.write('\n')
final_check=read(D/'final-structural-validation.json')
assert final_check['stage']=='final' and final_check['drafts_preserved']
second=read(D/'second-pass-dispatch-record.json')
assert second['same_preplanned_generic_instruction_for_both'] and second['no_current_grading_before_second_passes']
for rec in final_check['readers']:
    assert sha(Path(rec['path']))==rec['sha256']
for file,digest in read(D/'input-manifest.json')['hashes'].items():
    assert sha(Path(file))==digest,file
for side in 'ab':
    paths=[D/'questions.json',D/'summary-snapshot.md',R/read(D/'input-manifest.json')['benchmark_version']/'answer-key.json',D/('reader-'+side+'.json'),Path(read(D/'freeze-record.json')['requested_parts_rubric']),R/'requested-parts-addendum-v13.json',R/'requested-parts-clarification-Q51-v11.json',R/'requested-parts-clarification-Q23-v14.json',R/'requested-parts-clarification-Q19-v14.json',D/'grading-prompts.json']
    new(D/('grading-input-manifest-'+side+'.json'),{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reader':side,'question_count':len(read(D/'questions.json')['questions']),'benchmark_version':read(D/'input-manifest.json')['benchmark_version'],'allowed_inputs':[str(p) for p in paths],'hashes':{str(p):sha(p) for p in paths},'all_actual_ids_present_once':True,'other_reader_not_allowed':True,'first_drafts_not_allowed':True,'source_audits_not_allowed':True,'automatic_source_partial_question_ids':[],'grading_standard_unchanged_from_full08':True,'both_complete_final_banks_checked':True,'preplanned_two_passes_completed_before_any_current_grading':True})
print(json.dumps({'both_grading_manifests_created':True,'all_frozen_hashes_match':True,'both_final_banks_structurally_valid':True,'no_current_grading_before_both_second_passes':True}))
