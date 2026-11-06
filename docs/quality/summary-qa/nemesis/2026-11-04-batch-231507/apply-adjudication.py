from pathlib import Path
import json,shutil,runpy
R=Path(__file__).resolve().parent;grade=runpy.run_path(str(R/'record-grades.py'))['grade']
# Record full04 independent grades, preserving detailed raw reviewer judgments.
fs={}
for reader in 'ab':
 d=json.loads((R/f'full-iteration-04/grading-review-{reader}.json').read_text());fs[reader]={x['id']:(x['grade'],x['reason']) for x in d['reviews'] if x['grade']!='correct'}
grade('full-iteration-04','benchmark-v7',fs)
changes=[]
adj=json.loads((R/'q13-adjudication.json').read_text())
for candidate in adj['candidates']:
 name,reader=candidate['candidate_id'].split(':');p=R/name/'results.json'
 if not p.exists():continue
 v=json.loads(p.read_text());row=next(x for x in v['readers'][reader]['grades'] if x['id']=='Q13')
 # Adjudicator used binary failure labels; retain repository Partial for omissions/abstention.
 new='correct' if candidate['grade']=='correct' else 'partial'
 if row['grade']!=new:
  backup=p.with_name('results-before-q13-adjudication.json')
  if not backup.exists():shutil.copyfile(p,backup)
  changes.append({'iteration':name,'reader':reader,'id':'Q13','old_grade':row['grade'],'new_grade':new,'reason':candidate['reason']})
  row.update(grade=new,reason='Fresh scope adjudication: '+candidate['reason']);v['readers'][reader]['counts']={x:sum(g['grade']==x for g in v['readers'][reader]['grades']) for x in ['correct','partial','incorrect']};v['q13_adjudication']='../q13-adjudication.json';p.write_text(json.dumps(v,indent=2)+'\n')
for name in ['full-iteration-02','full-iteration-04']:
 p=R/name/'results.json';v=json.loads(p.read_text());v.update(source_unresolved_ids=['Q18','Q51'],complete_core_pass=False,source_unresolved_explanation='Truthful corrected-key matches preserve missing source rulings; factual key-match counts do not establish a full-core PASS.')
 for reader in 'ab':
  d=json.loads((R/name/f'grading-review-{reader}.json').read_text());items=d.get('reviews',d.get('answers'));by={x['id']:x for x in items}
  for x in v['readers'][reader]['grades']:
   rev=by[x['id']];x['requested_parts']=rev.get('requested_parts');x['summary_support_assessment']=rev.get('summary_support');x['source_unresolved']=rev.get('source_unresolved',False)
   if name=='full-iteration-04' and reader=='b' and x['id']=='Q69':x['unsupported_guess']=True
 v['independent_adjudication']=['grading-review-a.json','grading-review-b.json','../q13-adjudication.json'];p.write_text(json.dumps(v,indent=2)+'\n')
(R/'q13-adjudication-application.json').write_text(json.dumps({'scope':'Uniform interpretation of actual question wording; Event route/discard is contextual rather than separately requested. No question/key/source edits.','changes':changes,'category_mapping':'Narrow adjudicator used binary correct/incorrect labels. Repository standard retains Partial for missing facts or unresolved caveats, rather than Incorrect absent a positive false ruling.','historical_results_retained':'results-before-q13-adjudication.json alongside affected results; raw reader responses and raw reviews untouched.'},indent=2)+'\n')
(R/'grading-rubric.json').write_text(json.dumps({'standard':{'correct':'All requested material rulings resolved, source/key matched, no contradictory or unresolved requested part.','partial':'One or more requested parts omitted or explicitly unresolved, without a materially false affirmative ruling.','incorrect':'A materially false ruling or contradiction, even if other parts correct.','support_labels':'Not grades; evaluate content.','unrequested_key_context':'Not automatically required merely because included in fixed key.','source_limits':'Q18/Q51 truthful source-limit statements match corrected key but source_unresolved flags prevent unconditional core PASS.'},'Q13_required_parts':adj['required_parts'],'Q13_scope':adj['arrow_scope_adjudication']['decision'],'authority':'Fresh question-wording adjudication q13-adjudication.json; fixed before final-full5 grading, without viewing final-full5 reader outputs.'},indent=2)+'\n')
print(changes)
