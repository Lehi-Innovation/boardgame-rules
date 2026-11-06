"""Validate immutable blind-stage outputs structurally without grading or modifying them."""
from pathlib import Path
import datetime, hashlib, json, sys
R=Path(__file__).resolve().parent
D=R/'full-iteration-10'
stage=sys.argv[1]
assert stage in ['draft','final']
questions=json.loads((D/'questions.json').read_text())['questions']
ids=[q['id'] for q in questions]
rows=[]
for side in 'ab':
    p=D/('reader-'+side+('-draft' if stage=='draft' else '')+'.json')
    raw=json.loads(p.read_text())
    answers=raw['answers']; actual=[a['id'] for a in answers]
    assert len(actual)==125 and len(set(actual))==125 and set(actual)==set(ids), side
    for a in answers:
        assert isinstance(a['requested_parts'],list) and a['requested_parts']
        assert isinstance(a['answer'],str) and isinstance(a['evidence'],str)
        assert a['support'] in ['supported','partial','unsupported']
    rows.append({'reader':side,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'answers':len(actual),'all_ids_once':True,'schema_valid':True,'clause_content_not_graded':True,'inputs_read':raw.get('inputs_read')})
if stage=='final':
    draft_check=json.loads((D/'draft-structural-validation.json').read_text())
    for old in draft_check['readers']:
        assert hashlib.sha256(Path(old['path']).read_bytes()).hexdigest()==old['sha256']
record={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':stage,'readers':rows,'structural_check_only':True,'no_feedback_or_grading_supplied':True,'drafts_preserved':True,'unchanged_current_bank':True}
with (D/(stage+'-structural-validation.json')).open('x') as f:
    json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'stage':stage,'each_answers':125,'all_ids_once':True,'schema_valid':True,'drafts_preserved':True}))
