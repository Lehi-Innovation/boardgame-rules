"""Collect worker progress without treating self-reported completion as approval."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib,json
import subprocess
base=Path(__file__).parent;p=base/'manifest.json';m=json.loads(p.read_text())
for g in m['games']:
 progress=Path(g['output_directory'])/'progress.json'
 if not progress.exists():continue
 try: d=json.loads(progress.read_text())
 except (ValueError,OSError):continue
 g['worker_progress']=d
 g['worker_status']=d.get('status')
 files=subprocess.run(['rg','--files',g['output_directory']],capture_output=True,text=True,check=True).stdout.splitlines()
 g['observed_recorded_reader_pairs']=sum(Path(f).name=='reader-a.json' and Path(f).with_name('reader-b.json').is_file() for f in files)
 if g['status']=='complete':continue
 for k in ['question_count','iterations','final_reader_scores','source_audit','report_path','blocking_reason','final_snapshot_path','coverage_review','coverage_stopping_rule','phase']:
  if k in d and (d[k] is not None or k in ['blocking_reason','final_reader_scores']):g[k]=d[k]
 g['worker_status']=d.get('status')
 if g.get('coordinator_source_gap',{}).get('status')=='open':
  if not g.get('blocking_reason'):g['blocking_reason']=g['coordinator_source_gap']['blocking_reason']
  major_audits=[]
  for audit_path in Path(g['output_directory']).glob('source-audit-*/source-audit.json'):
   try: actual_audit=json.loads(audit_path.read_text())
   except (ValueError,OSError):continue
   if actual_audit.get('verdict')=='MAJOR':major_audits.append((audit_path.stat().st_mtime,audit_path,actual_audit))
  if major_audits:
   _,audit_path,actual_audit=max(major_audits,key=lambda item:item[0])
   g['coordinator_latest_source_audit']={'verdict':'MAJOR','path':str(audit_path),'summary_sha256':actual_audit.get('summary_sha256'),'scope':'Latest saved independent completeness audit; full findings are in the linked report and the coordinator source gap remains open.'}
  if g.get('coordinator_latest_source_audit'):g['source_audit']=g['coordinator_latest_source_audit']
 if g.get('coordinator_pending_source_audit'):
  g['source_audit']=g['coordinator_pending_source_audit']
 if g['status'] not in ['complete','awaiting-stamp-retest','ready-for-publication']:
  if d.get('status') in ['complete','ready-for-coordinator','ready_for_coordinator','ready-for-publication','ready-for-review']:g['status']='ready-for-coordinator-review'
  elif d.get('status') in ['blocked','awaiting-source','awaiting-user','awaiting-external-input','incomplete-awaiting-source','incomplete-awaiting-external-source','blocked-awaiting-authoritative-source']:g['status']='awaiting-external-input'
  elif g.get('thread_id'):g['status']='active'
 if g.get('reassessment_queue_status')=='queued':
  g['status']='queued-for-source-reassessment'
  g['blocking_reason']=g['coordinator_source_gap']['blocking_reason']
m['updated_at']=datetime.now(ZoneInfo('America/Phoenix')).isoformat();p.write_text(json.dumps(m,indent=2)+'\n')
lines=['# Ten-game rules-summary QA batch','',f"Run: {m['run_id']}. Updated: {m['updated_at']}.",'','This batch uses the existing local checkout, three game chats at a time, Sol/high game workers and reviewers, and fresh Luna/high blind reader pairs. No commits or pushes are authorized. Game completion requires coordinator inspection of the full saved evidence and exact final stamped summary.','', '| Game | Questions | Iterations | Reader scores | Source audit | Status | Evidence |', '|---|---:|---:|---|---|---|---|']
for g in m['games']:
 a=g.get('source_audit');audit=a.get('verdict','Pending') if isinstance(a,dict) else a or 'Pending';it=g.get('iterations',[]);n=len(it) if isinstance(it,list) else it
 if g['status']=='complete' and g.get('iteration_count') is not None:n=g['iteration_count']
 if g['status']!='complete' and g.get('observed_recorded_reader_pairs') is not None:n=g['observed_recorded_reader_pairs']
 if g['status']!='complete':
  audit='Pending on current text'
  proof_path=g.get('coordinator_source_delivery_checkpoint',{}).get('path')
  if proof_path and Path(proof_path).is_file() and not g.get('coordinator_pending_source_audit') and g.get('coordinator_source_gap',{}).get('status')!='open':
   proof=json.loads(Path(proof_path).read_text());ap=Path(proof['audit_path']);current_hash=hashlib.sha256(Path(g['summary_path']).read_bytes()).hexdigest()
   if proof.get('verified') is True and proof.get('summary_sha256',g.get('coordinator_source_delivery_checkpoint',{}).get('summary_sha256'))==current_hash and hashlib.sha256(ap.read_bytes()).hexdigest()==proof['audit_sha256']:
    audit='PASS'
 if g.get('coordinator_pending_scope_choice',{}).get('status')=='awaiting-human-clarification':audit='Scope choice pending; historical candidate only'
 if g.get('user_authority_override') and audit=='PASS':audit='PASS (user scope)'
 scores=g.get('final_reader_scores') if g['status']=='complete' else None;checkpoint_scores=False
 checkpoint=g.get('coordinator_latest_reader_checkpoint',{})
 checkpoint_matches_current_text=(checkpoint.get('summary_sha256')==hashlib.sha256(Path(g['summary_path']).read_bytes()).hexdigest()) if Path(g['summary_path']).is_file() else False
 if g['status']!='complete' and checkpoint.get('N')==g.get('question_count') and checkpoint_matches_current_text:
  scores=checkpoint.get('scores');checkpoint_scores=bool(scores)
 if not scores and g['status'] in ['awaiting-external-input','queued-for-source-reassessment']:
  latest=g.get('worker_progress',{}).get('latest_reader_scores',{})
  scores={name:latest[name] for name in ['reader_a','reader_b'] if isinstance(latest.get(name),dict)}
  checkpoint_scores=bool(scores)
 parts=[]
 if isinstance(scores,dict):
  for who,value in scores.items():
   if not isinstance(value,dict) or not ('correct' in value or 'Correct' in value):continue
   correct=value.get('correct',value.get('Correct'));graded=checkpoint.get('graded_questions',{}).get(who) if checkpoint_scores else None
   if isinstance(graded,int) and graded<g['question_count']:parts.append(f"{correct}/{graded} graded ({g['question_count']} required)")
   else:parts.append(str(correct)+'/'+str(g.get('question_count')))
 st='; '.join(chr(65+i)+' '+value for i,value in enumerate(parts)) if parts else scores if isinstance(scores,str) else 'Pending'
 if checkpoint_scores:st+=' (incomplete checkpoint'+(', '+checkpoint['iteration'].rsplit('/',1)[-1] if checkpoint.get('iteration') else '')+')'
 chat=f"[chat](codex://threads/{g['thread_id']})" if g.get('thread_id') else 'Queued'
 g['report_path']=g.get('report_path') or str(Path(g['output_directory'])/'README.md')
 report=Path(g['report_path']);rel=report.relative_to(base.parents[4]) if report.is_absolute() else report
 evidence=f"{chat}; [report](../../../../../{rel})" if report.exists() else chat
 lines.append(f"| {g['game']} | {g.get('question_count') or 'Pending'} | {n} | {st} | {audit} | {g['status']} | {evidence} |")
lines+=['','Completed iteration counts are coordinator-reconciled scored reader pairs. Active counts show folders with both saved raw reader files and may still await grading. Separately retained unscored dispatched attempts are documented in each final report. Unmatched has 14 scored pairs and 1 aborted unscored pair (15 dispatched pairs). Coverage is working saturation within each documented edition and source scope. A passing fixed bank does not establish exhaustive scenario coverage or general model accuracy.','','## Assignments and ownership','']
if m.get('concurrency_events'):
 lines[lines.index('## Assignments and ownership'):lines.index('## Assignments and ownership')]=['A human continuation temporarily reactivated John Company while the three coordinator-assigned slots were occupied. The overlap is recorded in the manifest; the coordinator dispatched no additional game during it. Normal three-slot coordination resumed afterward.','']
for g in m['games']:
 lines.extend([f"- **{g['game']}**: {g.get('edition_scope') or 'Source resolution in progress.'} Canonical summary: {g['summary_path']}. Evidence: {g['output_directory']}."])
 if g.get('blocking_reason'):lines.append(f"  Blocker: {g['blocking_reason']}")
lines+=['','The [manifest](manifest.json) records chat and host IDs, source provenance, assigned paths, worker progress and coordinator verdicts. [Initial worktree hashes](initial-worktree-hashes.json) and [Git status](initial-git-status.txt) preserve the starting state. Shared catalog changes are handled by this coordinator alone, with targeted regeneration and checks.','','Coordinator evidence includes [source integrity checks](source-integrity-checks/), [recovered component and FAQ sources](source-preflight/), [actual parent model records](parent-model-provenance/), [independent final agent model checks](coordinator-runtime-model-checks/), [game approval checks](coordinator-checks/), and [targeted publication checks](publication/). Reader and reviewer model records, failed iterations, raw responses, grades, and source audits remain in each game report.','']
(base/'README.md').write_text('\n'.join(lines))
print(json.dumps([{'slug':g['slug'],'status':g['status'],'phase':g.get('phase'),'questions':g.get('question_count'),'worker_status':g.get('worker_status'),'blocker':g.get('blocking_reason')} for g in m['games']],indent=2))
