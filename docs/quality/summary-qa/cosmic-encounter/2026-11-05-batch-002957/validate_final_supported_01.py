"""Current exact-body/schema/style checks; no source vote or verification stamp."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
R=Path(__file__).parent.resolve();WORK=R.parents[4];IT=R/'expanded-iteration-06'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected='787b88677123fc93751d1605a99e4c724faadaa891f1b0c103bcb296075952b9';canonical=WORK/'rules/cosmic-encounter.md';snapshot=R/'repair-freeze-17.md';raw=canonical.read_bytes()
commands=[]
for argv in [['.venv/bin/python','-B','-m','scripts.validate','rules/cosmic-encounter.md'],['git','diff','--check','--','rules/cosmic-encounter.md',str(R.relative_to(WORK))]]:
    result=subprocess.run(argv,cwd=WORK,text=True,capture_output=True)
    commands.append({'argv':argv,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'pass':result.returncode==0})
audit=read(IT/'bookkeeping-audit-23.json');grades=read(IT/'adjudicated-grades-aggregate.json');frozen=read(IT/'complete-reviewed-original-pair-freeze.json')
checks={'canonical_expected_sha256':sha(canonical)==expected,'all_tested_guide_bytes_equal':raw==snapshot.read_bytes()==(IT/'summary-snapshot.md').read_bytes(),'correct_character_byte_counts':len(raw.decode())==59002 and len(raw)==59165,'supported_factual_totals':grades['totals']=={'a':{'correct':168,'partial':0,'incorrect':0},'b':{'correct':168,'partial':0,'incorrect':0}},'technical_acceptance':audit['technical_pass'],'primary_reports_unchanged':all(sha(Path(p['path']))==p['sha256'] for p in grades['original_primary_reports']),'both_frozen_final_originals_unchanged':all(sha(Path(p['original_path']))==p['sha256']==sha(Path(p['frozen_original_path'])) for p in frozen['readers']),'repository_validation_and_whitespace':all(c['pass'] for c in commands)}
report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'pass':all(checks.values()),'scope':'Current tested-body identity and summary schema/style validation; accepted source/coverage/primary gates reused, not rerun. Supported-bank factual results only.','canonical_path':str(canonical),'canonical_sha256':sha(canonical),'unicode_characters':len(raw.decode()),'utf8_bytes':len(raw),'checks':checks,'repository_commands':commands,'technical_acceptance_path':str(IT/'bookkeeping-audit-23.json'),'technical_acceptance_sha256':sha(IT/'bookkeeping-audit-23.json'),'workflow_conformance_pass':False,'final_scope_readiness':False,'verified_stamp_applied':False,'full_core_verified_claim':False,'essential_external_authority_gap':'FAQ reinforcement/Negotiate conflict.'}
p=R/'validation-final-supported-01.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print({'pass':report['pass'],'canonical_sha256':report['canonical_sha256'],'checks':checks,'repository_commands':[(c['argv'][0],c['exit_code']) for c in commands]})
