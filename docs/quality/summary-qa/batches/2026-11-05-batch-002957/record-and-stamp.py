"""Publish only coordinator-approved independent QA verdicts and stamp those summaries."""
from pathlib import Path
from datetime import date,datetime
from zoneinfo import ZoneInfo
from argparse import Namespace
import argparse,copy,json,hashlib,os,re,sys,yaml
base=Path(__file__).parent;root=base.parents[4];sys.path.insert(0,str(root))
from scripts import audit
from scripts.registry import locked_registry
from scripts.stamp_verification import stamp_file
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('slugs',nargs='+');parser.add_argument('--preserve-tested-stamp',action='store_true',help='For complete exact-byte approvals only, retain the verified date already tested and independently audited.');args=parser.parse_args();selected=set(args.slugs)
mp=base/'manifest.json';batch=json.loads(mp.read_text());assigned={g['slug']:g for g in batch['games']};approved=json.loads((base/'coordinator-approvals.json').read_text())
now=datetime.now(ZoneInfo('America/Phoenix'));out=base/'audit-publication'/now.strftime('%Y%m%d-%H%M%S');out.mkdir(parents=True);stamp_dates={}
for slug in selected:
 assert assigned[slug].get('coordinator_pending_scope_choice',{}).get('status')!='awaiting-human-clarification', 'The pending human source-scope choice must be resolved before verified publication'
 g=assigned[slug];assert g.get('coordinator_source_gap',{}).get('status')!='open', 'An unresolved core source gap prevents verified publication';assert not g.get('coordinator_pending_source_audit'), 'Coordinator source findings must be independently resolved before verified publication';a=approved[slug];canonical=Path(g['summary_path']);assert a['approved'] is True;assert hashlib.sha256(canonical.read_bytes()).hexdigest()==a['summary_sha256'];assert a['source_audit_verdict']=='PASS';assert Path(a['source_audit_path']).exists()
 actual_audit=json.loads(Path(a['source_audit_path']).read_text());actual_verdict=actual_audit.get('verdict',actual_audit.get('overall_verdict',actual_audit.get('status')))
 if actual_verdict is None and g.get('user_authority_override'):
  scoped=actual_audit.get('machine_verdicts',{});assert scoped.get('official_claims')=='PASS' and scoped.get('human_interpretation_fidelity')=='PASS' and scoped.get('scoped_signoff') is True
  assert scoped.get('unqualified_independently_verified_official_core_signoff') is False and scoped.get('publisher_email_independently_verified') is False, 'An explicit user-scope audit must retain its source qualification'
  actual_verdict=scoped.get('overall_scoped_result')
 assert actual_verdict=='PASS', 'The actual saved source audit must return PASS within the explicitly approved source scope'
 stamp_dates[slug]=now.date().isoformat()
 if args.preserve_tested_stamp:
  assert a.get('phase')=='complete', 'Only an accepted full-bank exact-byte completion may retain its tested verification date'
  front=re.match(r'\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)',canonical.read_text(),re.S);assert front
  metadata=yaml.safe_load(front.group(1));assert metadata.get('verification')=='verified'
  tested_date=str(metadata['verification_date']);assert date.fromisoformat(tested_date)<=now.date()
  assert Path(a['final_snapshot_path']).read_bytes()==canonical.read_bytes(), 'Retained verification date must belong to the exact passing snapshot'
  stamp_dates[slug]=tested_date
 if g.get('user_authority_override'):
  override=g['user_authority_override'];assert hashlib.sha256(Path(override['path']).read_bytes()).hexdigest()==override['sha256'];assert a.get('scope_note')==override['scope_note'], 'User-approved source scope must remain explicit in the approval and publication records'
 (out/(slug+'-coordinator-approval.json')).write_text(json.dumps(a,indent=2)+'\n')
 target=out/'before-summaries'/canonical.name;target.parent.mkdir(exist_ok=True);target.write_bytes(canonical.read_bytes())
results_path=root/'docs/quality/semantic-audit-results.yaml';audit_manifest_path=root/'docs/quality/semantic-audit-manifest.json'
original_results=results_path.read_bytes();original_manifest=audit_manifest_path.read_bytes();(out/'before-semantic-audit-results.yaml').write_bytes(original_results);(out/'before-semantic-audit-manifest.json').write_bytes(original_manifest);old_audits=yaml.safe_load(original_results);old_manifest=json.loads(original_manifest);temporary_manifest=copy.deepcopy(old_manifest);bid='summary-qa-'+batch['run_id']+'-'+('-'.join(args.slugs));temporary_manifest['batches'][bid]={'status':'pending','slugs':args.slugs,'evidence':{s:approved[s]['source_audit_path'] for s in args.slugs}}
(out/'semantic-audit-manifest.json').write_text(json.dumps(temporary_manifest,indent=1)+'\n');(out/'semantic-audit-results.yaml').write_bytes(original_results)
records=[]
for slug in args.slugs:
 a=approved[slug];reason=f"Independent source audit PASS on summary {a['summary_sha256']}; both Luna readers {a['question_count']}/{a['question_count']}; evidence {Path(a['source_audit_path']).relative_to(root)}. Exact stamped-byte recheck pending."
 if a.get('phase')=='complete':reason=reason.replace('Exact stamped-byte recheck pending.','Exact stamped summary independently audited and full-bank retested successfully.')
 if a.get('scope_note'):reason+=' Scope qualification: '+a['scope_note']
 records.append(f'RESULT|{slug}|PASS|{reason}')
(out/'audit-record-input.txt').write_text('\n'.join(records)+'\n')
audit.RESULTS_PATH=str(out/'semantic-audit-results.yaml');audit.MANIFEST_PATH=str(out/'semantic-audit-manifest.json');audit.cmd_record(Namespace(results_file=str(out/'audit-record-input.txt'),batch_ids=[bid]))
new_audits=yaml.safe_load((out/'semantic-audit-results.yaml').read_text());new_manifest=json.loads((out/'semantic-audit-manifest.json').read_text())
# Preserve existing unrelated YAML blocks byte-for-byte while using audit.record's actual selected results.
text=original_results.decode();pattern=re.compile('(?m)^([a-z0-9][a-z0-9-]*):[ '+chr(9)+']*'+chr(10));matches=list(pattern.finditer(text));chunks=[];seen=set();last=0
for i,match in enumerate(matches):
 end=matches[i+1].start() if i+1<len(matches) else len(text);chunks.append(text[last:match.start()]);slug=match.group(1)
 if slug in selected:chunks.append(yaml.safe_dump({slug:new_audits[slug]},sort_keys=False,allow_unicode=True,width=100000));seen.add(slug)
 else:chunks.append(text[match.start():end])
 last=end
chunks.append(text[last:]);updated=''.join(chunks)
for slug in args.slugs:
 if slug not in seen:updated+='\n'+yaml.safe_dump({slug:new_audits[slug]},sort_keys=False,allow_unicode=True,width=100000)
parsed=yaml.safe_load(updated);assert all(parsed[s]==v for s,v in old_audits.items() if s not in selected);assert all(parsed[s]==new_audits[s] for s in selected)
assert results_path.read_bytes()==original_results;assert audit_manifest_path.read_bytes()==original_manifest
for path,data in [(results_path,updated.encode()),(audit_manifest_path,(json.dumps(new_manifest,indent=1)+'\n').encode())]:
 temp=path.with_name(path.name+'.summary-qa-tmp');temp.write_bytes(data);os.replace(temp,path)
# The existing registry lock preserves concurrent updates by other game batches.
with locked_registry(str(root/'games.yaml')) as (games,save):
 before=copy.deepcopy(games);changed_names=set();(out/'before-games.yaml').write_bytes((root/'games.yaml').read_bytes())
 for slug in args.slugs:
  g=assigned[slug];matches=[r for r in games if r.get('slug')==slug or r.get('name','').lower()==g['game'].lower()]
  assert len(matches)<=1,(slug,matches)
  if matches:row=matches[0];changed_names.add(row['name'])
  else:row={'name':g['game'],'bgg_id':g['bgg_id']};games.append(row)
  changed_names.add(row['name'])
  row.update(bgg_id=g['bgg_id'],status='verified',verified_date=stamp_dates[slug],review_notes='Independent summary QA source audit PASS; evidence '+str(Path(g['report_path']).relative_to(root)))
  if approved[slug].get('scope_note'):row['review_notes']+=' Scope qualification: '+approved[slug]['scope_note']
  if slug!=re.sub(r'[^a-z0-9]+','-',g['game'].lower()).strip('-'):row['slug']=slug
  for k in ['claimed_at','notes']:
   if k=='claimed_at' or row.get(k) in ['Complex rules, too large to summarize in batch','Registered from BGG top-200 mirror (2026-08-05); PDF hunt requires normal network access.']:row.pop(k,None)
 assert [r for r in games if r['name'] not in changed_names]==[r for r in before if r['name'] not in changed_names]
 save(games)
stamped={}
for slug in args.slugs:
 path=Path(assigned[slug]['summary_path']);before_hash=hashlib.sha256(path.read_bytes()).hexdigest();assert before_hash==approved[slug]['summary_sha256'];state=stamp_file(str(path),parsed,stamp_date=stamp_dates[slug]);assert state=='verified';after_hash=hashlib.sha256(path.read_bytes()).hexdigest();stamped[slug]={'before_sha256':before_hash,'after_sha256':after_hash,'changed':before_hash!=after_hash};assigned[slug]['status']='ready-for-publication';assigned[slug].setdefault('publication_history',[]).append(assigned[slug].get('publication'));assigned[slug]['publication']={'directory':str(out),'stamp':stamped[slug]}
mp.write_text(json.dumps(batch,indent=2)+'\n');report={'selected':args.slugs,'audit_record_workflow':'scripts.audit.cmd_record on isolated copies; selected actual records integrated with unrelated blocks retained','unrelated_audit_entries_preserved':True,'unrelated_registry_rows_preserved':True,'verification_dates':stamp_dates,'preserved_exact_tested_stamp_dates':args.preserve_tested_stamp,'stamps':stamped};(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
