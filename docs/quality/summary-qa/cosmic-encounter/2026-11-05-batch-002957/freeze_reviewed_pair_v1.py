"""Archive both complete reviewed originals byte-for-byte before factual grading."""
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).parent.resolve();it=Path(sys.argv[1]).resolve()
assert it.is_relative_to(R)
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
history=read(it/'staged-history-validation-01.json')
assert history['content_completion_pass']
manifest=read(it/'input-manifest-final.json');expected=[q['id'] for q in read(it/'questions.json')['questions']]
assert len(expected)==manifest['question_count']
assert not (it/'grading-dispatch-plan.json').exists()
assert not list(it.glob('grades-[0-9][0-9].json'))
provenance=read(Path(manifest['model_provenance_path']))
assert not any(x['task'].startswith('/root/expanded6_grader_') for x in provenance['agents'])
rows=[]
raw_copies=[]
for c in 'ab':
    path=Path(manifest['reader_work_paths'][c]['final']);doc=read(path)
    assert doc['stage']=='review_complete' and doc['self_review']['complete'] is True
    assert [a['id'] for a in doc['answers']]==expected
    item=next(x for x in history['readers'] if x['reader']==c)
    assert item['content_completion_pass']
    assert sha(path)==item['effective_terminals']['review']['sha256']
    draft=Path(manifest['reader_work_paths'][c]['draft'])
    assert sha(draft)==item['effective_terminals']['draft']['sha256']
    payload=read(it/f'reader-{c}-review-payload-validation-01.json')
    assert payload['payload_delivery_pass']
    assert payload['final_sha256']==sha(path) and payload['draft_sha256']==sha(draft)
    archive=it/f'reader-{c}-complete-reviewed-original.json'
    assert not archive.exists()
    raw_copies.append((archive,path.read_bytes()))
    rows.append({'reader':c,'original_path':str(path),'frozen_original_path':str(archive),
                 'sha256':sha(path),'characters':len(path.read_text()),'utf8_bytes':path.stat().st_size,
                 'question_count':len(expected),'closed_draft_path':str(draft),'closed_draft_sha256':sha(draft),
                 'workflow_conformance_pass':item['workflow_conformance_pass'],
                 'parent_scheduling_assertion_frozen_before_factual_grading':True})
for archive,raw in raw_copies:
    with archive.open('xb') as f:f.write(raw)
report={'content_completion_pass':True,'workflow_conformance_pass':history['workflow_conformance_pass'],
        'question_count_per_reader':len(expected),'all_original_entry_count':len(expected)*2,
        'readers':rows,'parent_scheduling_assertion_factual_grading_unstarted':True,
        'no_grade_outputs_dispatch_plan_or_current_grader_provenance_at_freeze':True,
        'chronology_limit':'Parent scheduling assertion plus absence of grading artifacts/currentgrader provenance; actual dispatch chronology is independently audited separately.','no_workflow_deviation_factual_grade_cap':True,
        'staged_history_sha256':sha(it/'staged-history-validation-01.json'),
        'coordinator_draft_delivery_acceptance_path':str(it/'coordinator-complete-draft-actual-delivery-acceptance.json'),
        'no_verified_stamp_or_full_core_claim':True}
with (it/'complete-reviewed-original-pair-freeze.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print({'frozen_originals':2,'entries':len(expected)*2,'workflow_conformance_pass':history['workflow_conformance_pass']})
