"""Read-only checks of owned evidence; writes a new versioned check report."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import argparse

R = Path(__file__).parent.resolve()
WORK = R.parents[4]
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def entrysha(e): return hashlib.sha256(json.dumps(e,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--snapshot',default='repair-freeze-04.md')
parser.add_argument('--output',default='validation-in-progress-02.json')
args=parser.parse_args()
snapshot=R/args.snapshot
out=R/args.output
assert snapshot.resolve().is_relative_to(R) and out.resolve().is_relative_to(R)
assert not out.exists()
initial=read(R/'input-manifest.json')
sources=[]
for path,expected in initial['sources_sha256'].items():
    p=Path(path)
    if p==WORK/'rules/cosmic-encounter.md': continue
    sources.append({'path':path,'expected_sha256':expected,'actual_sha256':sha(p),'bytes':p.stat().st_size,'unchanged':sha(p)==expected})
originalq,originalk=read(R/'seed-v1/questions.json'),read(R/'seed-v1/answer-key.json')
preservation=[]
for d in [R/'expanded-draft-01',*sorted(R.glob('expanded-candidate-*'))]:
    if not (d/'questions.json').exists(): continue
    q,k=read(d/'questions.json'),read(d/'answer-key.json')
    checks=[{'id':x['id'],'question_entry_sha256':entrysha(x),'key_entry_sha256':entrysha(y),'question_identical':x==ox,'key_identical':y==oy} for x,y,ox,oy in zip(q['questions'][:20],k['answers'][:20],originalq['questions'],originalk['answers'])]
    preservation.append({'version':d.name,'question_count':len(q['questions']),'question_file_sha256':sha(d/'questions.json'),'key_file_sha256':sha(d/'answer-key.json'),'seed_entries':checks,'pass':len(checks)==20 and all(x['question_identical'] and x['key_identical'] for x in checks)})
native=[]
for name in ['parent-native-image-delivery.json','preliminary-audit-delivery.json','coverage-key-delivery-01.json','coverage-key-delivery-02.json']:
    p=R/'source-review'/name
    native.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'note':'Receipt preserved; payload proof details remain in original receipt and external runtime logs. Independent final auditor must provide its own final delivery.'})
commands=[]
for cmd in [['.venv/bin/python','-m','scripts.validate','rules/cosmic-encounter.md'],['git','diff','--check','--','rules/cosmic-encounter.md',str(R.relative_to(WORK))]]:
    run=subprocess.run(cmd,cwd=WORK,text=True,capture_output=True)
    commands.append({'argv':cmd,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'pass':run.returncode==0})
manifest={
 'checked_at_utc':datetime.now(timezone.utc).isoformat(),
 'status':'IN PROGRESS: expanded runs and source assessments are tracked separately in progress.json; no final readiness is implied by these integrity checks.',
 'canonical_sha256':sha(WORK/'rules/cosmic-encounter.md'),
 'candidate_snapshot':str(snapshot),
 'canonical_equals_candidate_snapshot':(WORK/'rules/cosmic-encounter.md').read_bytes()==snapshot.read_bytes(),
 'authoritative_original_sources':sources,
 'all_assigned_original_source_hashes_unchanged':all(x['unchanged'] for x in sources),
 'baseline_hash':sha(R/'baseline/summary-snapshot.md'),
 'baseline_matches_original':sha(R/'baseline/summary-snapshot.md')==initial['sources_sha256'][str(WORK/'rules/cosmic-encounter.md')],
 'additional_historical_authority':{'original_pdf_bytes_available':False,'original_pdf_sha256':None,'cached_official_extraction_sha256':sha(R/'source-review/additional/historical-official-faq-cached-extraction.txt'),'retrieval_provenance':str(R/'source-review/additional/web-retrieval-provenance.json'),'cache_files':[{ 'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted((R/'source-review/additional').glob('*.txt'))]},
 'all_seed_entries_preserved':all(x['pass'] for x in preservation),'preservation':preservation,
 'native_image_receipts':native,'repository_commands':commands,
 'final_reader_scores':None,'final_source_audit':None,
 'human_scope_decision':read(WORK/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/coordinator-checks/cosmic-pending-human-scope-choice.json'),
 'stamping':'Not run: assigned coordinator owns shared verification/stamping.',
 'prior_failed_check_preserved':'validation-in-progress.json records earlier whitespace failure. This report checks current exact bytes; it does not relabel historical results.',
}
out.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print({k:manifest[k] for k in ['status','canonical_sha256','canonical_equals_candidate_snapshot','all_assigned_original_source_hashes_unchanged','baseline_matches_original','all_seed_entries_preserved']})
print('repository_checks',[(x['argv'][0],x['pass']) for x in commands])
