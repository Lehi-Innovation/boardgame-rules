from pathlib import Path
import json,hashlib,sys
P=Path(__file__).parent;name=sys.argv[1] if len(sys.argv)>1 else 'stamped-iteration-03';D=P/name;h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();r=json.loads((D/'results.json').read_text());audit=json.loads((D/'source-audit.json').read_text())
assert D.joinpath('summary-snapshot.md').read_bytes()==Path('rules/orl-ans.md').read_bytes()
assert all(r['readers'][w]['counts']=={'correct':60,'partial':0,'incorrect':0} for w in ['a','b']) and audit['verdict']=='PASS' and not audit['findings']
assert all(h(x['path'])==x['sha256'] for x in audit['file_hashes'])
old_inventory=json.loads((P/'evidence-hashes.json').read_text());assert all(h(P/x)==v for x,v in old_inventory.items()),'Historical immutable evidence changed'
new_inventory=dict(old_inventory)
for d in sorted(P.glob('stamped-iteration-*')):
 for leaf in ['summary-snapshot.md','questions.json','input-manifest.json','reader-a.json','reader-b.json','results.json','model-provenance.json','source-audit.json','adjudication.json','reader-a-prompt.txt','reader-b-prompt.txt','reader-prompt-record.json','summary-changes.patch','repair-from-previous.patch']:
  f=d/leaf
  if f.exists():new_inventory[str(f.relative_to(P))]=h(f)
for leaf in ['coordinator-stamping.patch','coordinator-stamping-received.json']:
 f=P/leaf;new_inventory[leaf]=h(f)
(P/'evidence-hashes.json').write_text(json.dumps(dict(sorted(new_inventory.items())),indent=2)+'\n')
s=json.loads((P/'game-status.json').read_text());iterations=[]
for prefix in ['seed','expanded','stamped']:
 for d in sorted(P.glob(prefix+'-iteration-*')):
  if not (d/'results.json').exists():continue
  x=json.loads((d/'results.json').read_text());q=json.loads((d/'questions.json').read_text());iterations.append({'name':d.name,'question_count':len(q['questions']),'benchmark_version':q['benchmark_version'],'reader_scores':{w:x['readers'][w]['counts'] for w in ['a','b']},'results_path':str((d/'results.json').resolve()),'summary_sha256':h(d/'summary-snapshot.md')})
s.update(status='ready-for-coordinator',phase='awaiting-final-coordinator-publication',iterations=iterations,final_reader_scores={w:r['readers'][w]['counts'] for w in ['a','b']},final_snapshot_path=str((D/'summary-snapshot.md').resolve()),final_reader_prompt_record=str((D/'reader-prompt-record.json').resolve()),reader_prompt_version='v2-generic-completeness',source_audit={'verdict':'PASS','path':str((D/'source-audit.json').resolve()),'summary_sha256':h(D/'summary-snapshot.md'),'model':'gpt-6.1-sol','reasoning_effort':'high','findings':[]},blocking_reason=None,all_local_checks_pass=True,evidence_hash_count=len(new_inventory),coordinator_pending=['Record updated exact-byte independent source PASS','Confirm targeted stamping is idempotent for the tested bytes','Run targeted publication/regeneration and final repository checks','Return final validation evidence so worker can finish the persistent goal'])
s['hashes'][str(Path('rules/orl-ans.md').resolve())]=h(Path('rules/orl-ans.md'));s['hashes'][str((D/'summary-snapshot.md').resolve())]=h(D/'summary-snapshot.md');s['coordinator_stamped_metadata_preserved']=Path('rules/orl-ans.md').read_text().split('## Overview')[0]==(P/'stamped-iteration-01/summary-snapshot.md').read_text().split('## Overview')[0]
assert s['coordinator_stamped_metadata_preserved'];(P/'game-status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');print('Prepared stamped handoff',h(D/'summary-snapshot.md'),len(new_inventory),'fingerprints')
