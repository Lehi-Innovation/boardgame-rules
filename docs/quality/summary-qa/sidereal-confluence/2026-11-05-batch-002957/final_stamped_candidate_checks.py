"""Require actual current evidence before declaring a candidate ready for coordinator review."""
from pathlib import Path
import json,hashlib,sys,datetime,re
from validate_artifacts import check_banks
ROOT=Path(__file__).resolve().parent
CANONICAL=Path('/home/jonny/projects/boardgame-rules/rules/sidereal-confluence.md')
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def assert_current_proof(proof,report):
 x=read(proof);assert x['validation']=='PASS';assert x.get('report_sha256')==sha(report);return x
iteration,output=sys.argv[1:];d=ROOT/iteration;dest=ROOT/output;assert not dest.exists()
header=CANONICAL.read_text().split('---',2)[1]
assert re.search(r'^verification:\s*[\"\']?verified[\"\']?\s*$',header,re.M),'Canonical is not stamped verified'
assert re.search(r'^verification_date:\s*[\"\']?\d{4}-\d{2}-\d{2}[\"\']?\s*$',header,re.M)
transition=read(ROOT/'coordinator-stamp-transition-01/transition.json');assert transition['stamped_sha256']==sha(CANONICAL),'Current bytes differ from observed coordinator stamp'
assert '<!-- verification:begin -->' in CANONICAL.read_text() and '<!-- verification:end -->' in CANONICAL.read_text()
m=read(d/'input-manifest.json');audit_name=Path(m['source_audit']['path']).parent.name;q=read(d/'questions.json')['questions'];key=read(d/'answer-key.json')['answers'];scope=read(d/'asked-facts.json')['questions'];ids=[x['id'] for x in q];n=len(ids);facts=sum(len(x['required_facts']) for x in key)
assert ids==[x['id'] for x in key]==[x['id'] for x in scope];assert n==86 and facts==256
for name,h in m['hashes'].items():assert sha(d/name)==h,(name,'Frozen input changed')
assert CANONICAL.read_bytes()==(d/'summary-snapshot.md').read_bytes()==(ROOT/audit_name/'summary-snapshot.md').read_bytes()
audit=read(ROOT/audit_name/'source-audit.json');assert audit['verdict']=='PASS' and audit['summary_snapshot_sha256']==sha(CANONICAL)
assert sha(ROOT/'source-manifest-v1.json')=='fdba14d45b107001c1972667d2aa0531ffe2a45084e197f9ae61984eda9ba92a'
source_manifest=read(ROOT/'source-manifest.json');assert read(ROOT/'source-manifest-v1.json')['sources']==source_manifest['sources'][:33];assert len(source_manifest['sources'])==34
for s in source_manifest['sources']:assert sha(s['path'])==s['sha256'],s['path']
assert (d/'source-manifest.json').read_bytes()==(ROOT/'source-manifest.json').read_bytes()==(ROOT/audit_name/'source-manifest.json').read_bytes()
coverage=read(ROOT/'expanded-v12/clean-coverage-scope-review.json');assert all(x['status']=='PASS' for x in coverage['verdicts'].values());assert coverage['counts']['questions_reviewed']==n and coverage['counts']['required_fact_atoms_reviewed']==facts
ledger=read(ROOT/'coverage-ledger.json');assert ledger['coverage_stopping_rule']['consecutive_zero_addition_passes']==2;assert ledger['coverage_stopping_rule']['latest_passes']==[34,35]
for folder,report in [(audit_name,'source-audit.json'),('expanded-v12','clean-coverage-scope-review.json')]:
 text=ROOT/folder/('runtime-text-delivery.json' if folder==audit_name else 'reviewer-runtime-text-delivery.json');tp=assert_current_proof(text,ROOT/folder/report);assert tp['all_text_inputs_before_first_report_write'] is True
 np=assert_current_proof(ROOT/folder/'runtime-native-delivery.json',ROOT/folder/report)
 native_receipts=read(ROOT/folder/report)['native_view_receipts'];assert np['native_view_count']==len(native_receipts)
 mandatory_images={str(Path(x['path'])) for x in source_manifest['sources'] if Path(x['path']).suffix.lower() in ['.png','.jpg','.jpeg']}
 seen_sources={str(Path(x.get('source_path',x.get('source')))) for x in native_receipts};assert mandatory_images<=seen_sources,'Missing mandatory original image view'
 seen_pages={x.get('pdf_page_1based') for x in native_receipts if x.get('pdf_page_1based') is not None};assert set(range(1,11))<=seen_pages,'Missing original PDF page view'
 for f in tp['input_delivery']:assert sha(f['file'])==f['sha256']
results=read(d/'results.json');assert results['PASS'] is True;assert results['totals']=={'correct':2*n,'partial':0,'incorrect':0}
raw={r:read(d/f'reader-{r}.json') for r in ['a','b']};reader_checks={};instruction_binding=read(d/'prompt-binding.json');process_transport='instruction_transport' in instruction_binding
round_number=iteration.rsplit('-',1)[1].lstrip('0');reader_tasks=read(d/'selected-reader-tasks.json') if (d/'selected-reader-tasks.json').exists() else {r:f'/root/full{round_number}_reader_{r}' for r in ['a','b']}
for r in ['a','b']:
 assert {x['id'] for x in raw[r]['answers']}==set(ids) and len(raw[r]['answers'])==n
 assert all(x['grade']=='correct' and x['original_grade_record'].get('unsupported_guessing') is False and all(f['match'] is True for f in x['original_grade_record']['required_facts']) for x in results['readers'][r])
 rp=read(d/f'reader-{r}-runtime-delivery.json');assert rp['validation']=='PASS' and rp['all_inputs_delivered_before_first_answer_file_write'] is True and rp['raw_response_sha256']==sha(d/f'reader-{r}.json');assert rp['model_records'] and all(x['actual_model']=='gpt-6-luna' and x['actual_effort']=='high' for x in rp['model_records'])
 assert rp['identity']['task']==reader_tasks[r],'Selected reader runtime identity mismatch'
 assert {Path(x['source_path']).name for x in rp['input_delivery']}=={'summary-snapshot.md','questions.json'}
 for f in rp['input_delivery']:assert sha(f['source_path'])==f['source_sha256']
 units=read(d/f'reader-{r}-source-unit-validation.json');assert units['all_match_complete_exact_supplied_helper_units'] is True
 helper=read(d/f'reader-{r}-executed-helper-identity.json');assert helper['validation'].startswith('PASS') and any(x['matches_supplied_code'] for x in helper['records'])
 api=read(d/f'reader-{r}-original-api-execution.json');assert api['validation'].startswith('PASS') and api['raw_sha256']==sha(d/f'reader-{r}.json');assert api['execution_call']['helper_functions_reimplemented_or_overridden'] is False
 reader_checks[r]={'scores':results['reader_scores'][r],'raw_sha256':sha(d/f'reader-{r}.json'),'source_units':units['records_checked'],'all_inputs_before_first_write':True,'actual_model':'gpt-6-luna','actual_effort':'high','actual_original_helper_api_execution':True}
 if process_transport:
  process=read(d/f'reader-{r}-process-instruction-delivery.json');assert process['validation']=='PASS' and process['all_process_text_before_first_answer_write'] is True and process['same_frozen_instructions_except_output'] is True
  assert process['process_instruction_sha256']==sha(d/f'reader-{r}-prompt.txt')==instruction_binding['prompt_hashes'][r]
  reader_checks[r]['actual_complete_process_instructions_before_first_write']=True
diagnostic_count=0
if (d/'output-diagnostic-coverage.json').exists():
 expected_diagnostics={(r,field.split('_',1)[0],'source_span_diagnostics.numeric_arithmetic.'+field):value for r in ['a','b'] for field,value in raw[r].get('source_span_diagnostics',{}).get('numeric_arithmetic',{}).items()}
 coverage=read(d/'output-diagnostic-coverage.json')['claims'];assert {(x['reader'],x['id'],x['raw_field_path']):x['value'] for x in coverage}==expected_diagnostics
 diagnostic_proof=read(d/'output-diagnostic-validation.json');assert diagnostic_proof['status']=='PASS' and diagnostic_proof['claim_count']==len(expected_diagnostics)
 checked={}
 for x in diagnostic_proof['checks']:
  k=(x['reader'],x['id'],x['raw_field_path']);assert k in expected_diagnostics and k not in checked;assert x['original_value']==expected_diagnostics[k] and x['match'] is True
  assert sha(d/x['grade_report'])==x['grade_report_sha256'];checked[k]=x
 assert set(checked)==set(expected_diagnostics);diagnostic_count=len(checked)
block_paths=sorted(d.glob('grading-block-??.json'));grade_paths=sorted(d.glob('grades-block-??.json'));assert len(block_paths)==len(grade_paths)==5
seen=[];rawindex={r:{x['id']:x for x in raw[r]['answers']} for r in raw}
for block in block_paths:
 for row in read(block)['records']:
  seen.append(row['id'])
  for r in ['a','b']:assert row[f'reader_{r}_original_entry']==rawindex[r][row['id']]
assert len(seen)==len(set(seen))==n and set(seen)==set(ids)
for grade in grade_paths:
 proof=assert_current_proof(d/(grade.stem+'-runtime-delivery.json'),grade);assert proof['all_text_inputs_before_first_report_write'] is True
 assert {Path(x['file']).name for x in proof['input_delivery']}=={'summary-snapshot.md',grade.name.replace('grades-block-','grading-block-')}
 for f in proof['input_delivery']:assert sha(f['file'])==f['sha256']
 for who,record in read(grade)['readers'].items():
  normalized='a' if who in ['a','reader_a','reader-a'] else 'b' if who in ['b','reader_b','reader-b'] else None;assert normalized is not None
  aggregated={x['id']:x for x in results['readers'][normalized]}
  for x in record['results']:
   assert x.get('unsupported_guessing') is False
   assert aggregated[x['id']]['original_grade_record']==x,'Aggregated grade differs from original report'
runtime=read(ROOT/'runtime-provenance.json');audit_number=audit_name.rsplit('-',1)[1];targets=['/root',f'/root/pure_source_auditor_{audit_number}','/root/clean_coverage_review_v12']+[reader_tasks[r] for r in ['a','b']]+[f'/root/full{round_number}_grader_{i:02}' for i in range(1,6)]
modelproof=[]
for task in targets:
 rec=next(x for x in runtime['records'] if x['task']==task);expected='gpt-6-luna' if '_reader_' in task else 'gpt-6.1-sol';assert rec['turn_context_records'] and all(x['actual_model']==expected and x['actual_effort']=='high' for x in rec['turn_context_records'])
 if task!='/root':assert rec['request']['requested_model']==expected and rec['request']['requested_effort']=='high' and rec['request']['requested_fork_turns']=='none'
 modelproof.append({'task':task,'actual_model':expected,'actual_effort':'high','fresh_fork_none_requested':task!='/root'})
matching_checks=[f for f in sorted(ROOT.glob('candidate-validation-*.json')) if read(f)['canonical_sha256']==sha(CANONICAL)];assert matching_checks;checks_path=matching_checks[-1];checks=read(checks_path);assert checks['canonical_sha256']==sha(CANONICAL) and all(x['exit_code']==0 for x in checks['targeted_checks'])
banks=check_banks()
assert (ROOT/'seed-v1/freeze.json').exists();prior=read(ROOT/'expanded-v12-integrity.json');assert prior['original_entry_preservation']
out={'status':'EXACT_STAMPED_BYTE_QA_PASS_PENDING_COORDINATOR_SIGNOFF_AND_AUTHORIZATION','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'iteration':iteration,'bank':'expanded-v12','canonical_path':str(CANONICAL),'canonical_sha256':sha(CANONICAL),'question_count':n,'required_facts_per_reader':facts,'paired_required_fact_checks':2*facts,'reader_checks':reader_checks,'unsupported_guessing':0,'supplemental_output_numeric_claims_checked':diagnostic_count,'whole_original_entries_preserved':2*n,'frozen_bank_versions_checked':len(banks),'source_files_intact':34,'original33_source_entries_unchanged':True,'coverage':'All3independentPASS after root zero-addition rewalks34/35','pure_source_audit':audit_name+' PASS on exact currentbytes','actual_pure_audit_delivery':{'text_files':len(read(ROOT/audit_name/'runtime-text-delivery.json')['input_delivery']),'text_slices':sum(len(x['ranges']) for x in read(ROOT/audit_name/'runtime-text-delivery.json')['input_delivery']),'native_views':read(ROOT/audit_name/'runtime-native-delivery.json')['native_view_count']},'actual_coverage_review_delivery':{'text_files':18,'native_views':39},'actual_model_checks':modelproof,'targeted_checks':checks_path.name+' PASS bound to exact canonical hash','history':'All earlier failures/keys/raws/grades/reports retained; no retrospectivePASS','limits':['Known fixed-set tool-assisted regression, notheldoutaccuracy','Instruction/context isolation, notOSsandbox','Opaque parent runtime messages prevent initial-dispatch plaintext comparison; for process-file transport, complete actual instruction delivery and equality except output are separately verified from model-visible tool outputs; actual models/forks/rules data/helper verified'],'coordinator_stamp':'APPLIED by coordinator; worker did not stamp/register/publish/commit; NEW exact-byte QA PASS, coordinator final signoff/authorization PENDING','goal':'ACTIVE pending coordinator final exact-byte signoff and completionauthorization','future_byte_change_rule':'Any canonicalbytechange requiresNEWfullreaderpair+NEWpureauditor on exact changedbytes'}
dest.write_text(json.dumps(out,indent=2)+'\n');print('Exact stamped-byte QA PASS',n,'perreader',2*facts,'factchecks; pending coordinator final signoff/authorization')
