"""Final gates; never stamp the summary or update shared registries."""
from pathlib import Path
import collections
import hashlib
import json
import sys

P = Path(__file__).resolve().parent
ROOT = Path('/home/jonny/projects/boardgame-rules')
D = P / (sys.argv[1] if len(sys.argv) > 1 else Path(json.loads((P/'progress.json').read_text())['final_snapshot_path']).parent.name)
tag = f"{int(D.name.rsplit('-',1)[1]):02d}"
def J(path): return json.loads(path.read_text())
def H(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def validation_passed(v):
 def bools(x):
  if isinstance(x,bool):return [x]
  if isinstance(x,dict):return [b for z in x.values() for b in bools(z)]
  if isinstance(x,list):return [b for z in x for b in bools(z)]
  return []
 if v.get('status') in ['passed','PASS']:return True
 checked=bools(v.get('checks',{}))+bools(v.get('reader_checks',{}))+bools(v.get('raw_equality_checks',{}))
 return v.get('status')=='complete' and v.get('valid',True) is True and bool(checked) and all(checked) and not v.get('errors')
gates = {}
def check(name, condition, detail=None): gates[name] = {'pass': bool(condition), 'detail': detail}
summary = ROOT/'rules/oath-chronicles-of-empire-and-exile.md'
check('canonical_equals_tested_snapshot', H(summary) == H(D/'summary-snapshot.md'))
check('minimal_runtime_metadata_validated',J(P/'provenance-metadata-validation.json')['status']=='PASS')
check('all_integrity_and_targeted_checks', J(P/'validation-in-progress.json')['status'] == 'PASS')
check('grading_transport_full_entry_equality', J(D/'grading-input-losslessness.json')['full_entry_reconstruction_equality'])
manifest = J(D/'grading-input.json')
for inp in manifest['inputs']:
    check('frozen_graded_input:'+inp['path'], H(Path(inp['path'])) == inp['sha256'])
source = J(D/'source-audit.json')
check('fresh_source_audit_exact_bytes', source['status'] == 'PASS' and source['candidate']['sha256'] == H(summary) and not source['findings'])
coverage = J(P/'coverage-review-10.json')
verdict = coverage.get('verdict', coverage.get('status'))
check('fresh_coverage_challenge', verdict == 'PASS_WORKING_SATURATION', verdict)
ledger=J(P/'coverage-ledger.json');stop=ledger['stopping_rule'];reviewed_ledger=J(P/'coverage-ledger-reviewed-10.json');zero_ids=stop['passes']
check('two_consecutive_zero_addition_root_passes',len(zero_ids)==2 and zero_ids[1]==zero_ids[0]+1 and all(next(p for p in ledger['passes'] if p['pass']==i)['count']==0 for i in zero_ids) and all(next(p for p in reviewed_ledger['passes'] if p['pass']==i)['count']==0 for i in zero_ids) and stop['all_core_procedural_passages_mapped'])
check('exact_independently_reviewed_coverage_ledger',H(P/'coverage-ledger-reviewed-10.json')==stop['independent_challenge']['reviewed_ledger_sha256'])

check('current_bank_is_reviewed_v11',J(D/'questions.json')['benchmark_version']=='expanded-v11')
check('independent_scope_precision_review_delivery',J(P/'delivery-audit/scope_adjudicator_09.verified-delivery.json')['status']=='PASS')
for path,h in J(P/'grading-scope-v12/freeze-manifest.json')['files'].items():
    check('scope_precision_frozen:'+path,H(Path(path))==h)
check('complete_final_core_review_delivery',J(P/'delivery-audit/coverage_challenge_10.verified-delivery.json')['status']=='PASS')
selection=J(D/'grading-transport-selection.json') if (D/'grading-transport-selection.json').exists() else {'grader_agent':f'full{tag}_grader','packet_filename':'grading-input.json'}
if selection.get('mode')=='bounded_blocks':
    bm=J(D/selection['manifest'])
    check('bounded_blocks_exact_full_ID_cover',[i for b in bm['blocks'] for i in b['question_ids']]==[q['id'] for q in manifest['questions']])
    check('bounded_blocks_full_fact_cover',sum(b['required_fact_groups_per_reader'] for b in bm['blocks'])==328)
    for block in bm['blocks']:
        bd=Path(block['directory']);proof=J(bd/'losslessness.json')
        check('bounded_block_losslessness:'+block['block_id'],proof['status']=='PASS' and proof['both_complete_original_raw_entries_reconstructed_exactly'] and proof['no_original_fields_or_quotations_discarded'] and proof['packet_sha256']==H(bd/'packet.json')==block['packet_sha256'] and proof['summary_sha256']==H(summary))
        check('bounded_block_independent_validation:'+block['block_id'],validation_passed(J(bd/'grading-validation.json')))
    grader_agents=selection['grader_agents']
else:
    grader_agents=[selection['grader_agent']]
    if selection['packet_filename']!='grading-input.json':
        proof=J(D/selection['losslessness_proof'])
        check('compact_transport_exact_full_packet_reconstruction',proof['v3_to_v1_entire_packet_reconstruction_equality'] and proof['v1_to_entire_raw_entry_reconstruction_equality'] and proof['v3_sha256']==H(D/selection['packet_filename']) and proof['v1_sha256']==H(D/'grading-input.json'))
for agent in [f'expanded{tag}_reader_a',f'expanded{tag}_reader_b',f'final_source_auditor_{tag}','coverage_challenge_10','scope_adjudicator_09']+grader_agents:
    delivery = J(P/'delivery-audit'/f'{agent}.verified-delivery.json')
    check('complete_actual_input_delivery:'+agent, delivery['status'] == 'PASS')
    runtime = next(x for x in J(P/'runtime-provenance.json') if x.get('agent_path') == '/root/'+agent)
    expected_model = 'gpt-6-luna' if 'reader' in agent else 'gpt-6.1-sol'
    check('actual_model_effort:'+agent, runtime['model_confirmed'] and runtime['models'] == [expected_model] and runtime['efforts'] == ['high'])
    sp=runtime.get('actual_spawn_request',{}).get('fields',{})
    check('actual_fresh_context_spawn:'+agent,sp.get('fork_turns')=='none' and sp.get('model')==expected_model and sp.get('reasoning_effort')=='high')
check('identical_blind_reader_technical_prompts', J(D/'prompt-comparison.json')['identical_after_identity_and_output_normalization'])
if (D/'reader-access-provenance.json').exists():
    access=J(D/'reader-access-provenance.json')
    for name,rec in access.items():
        check('recorded_reader_access_scope:'+name,not rec['forbidden_content_markers'] and H(Path(rec['record_path']))==rec['record_sha256'])

if int(tag)>=11:
    for who in ['a','b']:
        fmt=J(D/f'reader-{who}.section-format-validation.json')
        check('complete_named_section_format:'+who,fmt['status']=='PASS' and not fmt['errors'] and fmt['raw_sha256']==H(D/f'reader-{who}.json'))
qids = [x['id'] for x in J(D/'questions.json')['questions']]
check('original_twenty_question_wording_retained',J(D/'questions.json')['questions'][:20]==J(P/'seed-v1/questions.json')['questions'])
result = J(D/'results.json')
check('no_unresolved_gold_or_scope_defects', not result.get('gold_or_scope_defects'))
check('all208_entries_and_all_facts_assessed', result.get('questions_graded') == 2*len(qids) and result.get('fact_assessments') == 2*manifest['required_fact_count_per_reader'])
fixed_records = {x['id']: x for x in manifest['questions']}
check('independent_grading_validation', J(D/'grading-validation.json').get('status') in ['PASS','passed'])
scores = {}
for reader in result['readers']:
    name = reader['reader']
    grades = reader['questions']
    count = collections.Counter(x['grade'] for x in grades)
    check('all_grade_ids:'+name, collections.Counter(x['id'] for x in grades) == collections.Counter(qids))
    check('full_bank_perfect:'+name, len(grades) == len(qids) and count['correct'] == len(qids) and count['partial'] == count['incorrect'] == 0, dict(count))
    check('declared_totals:'+name, all(count[g] == reader['totals'][g] for g in ['correct','partial','incorrect']))
    for grade in grades:
        expected = fixed_records[grade['id']]['required_facts']
        actual = grade.get('fact_checks',[])
        check('all_exact_fact_ids_and_text:'+name+':'+grade['id'], [(x['fact_id'],x['expected_fact']) for x in actual] == [(x['fact_id'],x['expected_fact']) for x in expected])
        check('all_facts_satisfied_with_evidence:'+name+':'+grade['id'], all(x.get('status') == 'satisfied' and x.get('evidence') for x in actual))
    scores[name] = dict(count)
check('two_readers', len(result['readers']) == 2 and set(scores) == {'reader-a','reader-b'})
check('actual208_entries_and656_fact_records',sum(len(r['questions']) for r in result['readers'])==2*len(qids) and sum(len(g.get('fact_checks',[])) for r in result['readers'] for g in r['questions'])==2*manifest['required_fact_count_per_reader'])
report = {'status': 'READY_FOR_COORDINATOR' if all(x['pass'] for x in gates.values()) else 'NOT_READY',
          'summary_path': str(summary), 'summary_sha256': H(summary), 'question_count': len(qids),
          'scores': scores, 'gates': gates,
          'scope': 'Fixed regression bank, working procedural saturation, first-printing base multiplayer. Historical failures retained. No held-out/exhaustive claim; no coordinator stamping or shared registry changes.'}
(P/'final-certificate.json').write_text(json.dumps(report, indent=2)+'\n')
print(report['status'], {k:v for k,v in gates.items() if not v['pass']})
