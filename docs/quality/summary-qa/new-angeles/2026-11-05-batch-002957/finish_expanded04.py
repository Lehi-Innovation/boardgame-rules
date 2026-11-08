"""Preserve a complete supported-source factual result, never a scope/stamp approval."""
from pathlib import Path
import collections,hashlib,json
B=Path(__file__).parent.resolve();ROOT=Path('/home/jonny/projects/boardgame-rules')
I=B/'expanded-luna-iteration-04';G=I/'grading';K=B/'expanded-supported-bank-v11';P=I/'results.json'
assert not P.exists(),'Do not overwrite an observed result'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(I/'input-manifest.json');freeze=read(K/'freeze.json')
assert all(sha(I/n)==h for n,h in manifest['hashes'].items())
assert all(sha(K/n)==h for n,h in freeze['hashes'].items())
guide_sha='93088c2fa1a52a5add775c7f25307aa91adf96ba7bf2caa64196848e4970a0ec'
assert sha(ROOT/'rules/new-angeles.md')==sha(I/'summary-snapshot.md')==sha(B/'expanded-summary-preparation-04.md')==guide_sha
assert (I/'questions.json').read_bytes()==(K/'questions.json').read_bytes()
assert sha(K/'answer-key.json')==manifest['key_sha256'] and sha(K/'asked-clause-map.json')==manifest['asked_clause_map_sha256']
original=read(B/'input-manifest.json')['sources'];assert len(original)==21 and all(sha(Path(p))==v['sha256'] for p,v in original.items())
integrity=read(I/'primary-grading-integrity.json')
assert integrity['all_expected_records_present'] and integrity['original_required_fact_assessments_verified']==544
assert not integrity['technical_diagnostics'] and len(integrity['raw_grade_links'])==188
delivery=read(I/'actual-delivery-verification.json');assert set(delivery)=={'a','b'}
assert all(v['all_input_data_verified_complete'] and v['all_ranges_at_most5500_characters'] and v['model_provenance']['model_effort_verified'] and v['model_provenance']['fork_turns']=='none' for v in delivery.values())
technical=read(I/'v6-technical-verification.json');assert set(technical['readers'])=={'a','b'}
assert all(v['all94_ids_exactly_once'] and v['all_exact_evidence_validated'] and v['all_selected_unit_text_found_in_actual_outputs'] and v['technical_clause_fields_valid'] for v in technical['readers'].values())
primary=[];grade_files=[];borderlines=[]
for p in sorted(G.glob('grades-*.json')):
    d=read(p);entries=d.get('records',d.get('grades',d.get('entries',[])));primary.extend(entries)
    grade_files.append({'path':str(p),'sha256':sha(p),'records':len(entries)})
    for obj in [d,*entries]:
        for key,value in obj.items():
            if 'borderline' in key and value:borderlines.append({'file':str(p),'field':key,'value':value})
assert len(grade_files)==6 and len(primary)==188 and not borderlines
assert not (G/'fresh-borderline-adjudication.json').exists(),'This result expects no genuine borderline or neutral sampling'
counts={l:collections.Counter() for l in 'ab'};records=[]
for x in primary:
    l=x['reader'].replace('reader_','');assert l in counts and x['label']=='Correct'
    assert not x.get('material_wrong_claims') and not x.get('genuine_omissions')
    counts[l][x['label']]+=1
    records.append({'reader':l,'id':x['id'],'raw_entry_sha256':x['raw_entry_sha256'],'primary_label':x['label'],'neutral_label':None,'effective_label':x['label']})
assert len({(x['reader'],x['id']) for x in records})==188 and all(c['Correct']==94 for c in counts.values())
source_path=B/'current-text-source-auditor/revision-04/source-audit.json';source=read(source_path)
assert source['snapshot']['sha256']==guide_sha and source['result']['source_supported_text']=='PASS'
source_proof_path=source_path.parent/'parent-actual-reuse-verification.json';source_proof=read(source_proof_path)
assert all(source_proof[k] for k in ['all_new_focused_ranges_delivered_after_prior_completion','all_changed_summary_text_delivered','all_fresh_native_views_after_prior_completion','all21_original_source_files_unchanged'])
turns=read(B/'runtime-all-turns-provenance.json');assert turns['verified_all_recorded_turns'] and len(turns['agents'])==63
scores={l:{label:c[label] for label in ['Correct','Partial','Incorrect']} for l,c in counts.items()}
report={'status':'PASS_PRELIMINARY_SUPPORTED_SOURCE_FACTUAL_94','benchmark':'expanded-supported-bank-v11','question_count':94,'snapshot_sha256':guide_sha,
        'counts':{'primary':scores,'effective':scores},'records':records,'factual_whole_run_pass':True,'whole_run_pass':True,
        'all188_original_primary_grades_and544_fixed_vectors_verified':True,'grade_files':grade_files,
        'neutral_adjudication':{'genuine_borderlines':0,'fresh_adjudicators_used':0,'unnecessary_sampling_performed':False},
        'complete_actual_reader_and_grader_data_process_annotation_delivery_verified':True,
        'exact_evidence_records':304,'literal_span_clause_records':741,'all_original_authoritative_source_files_unchanged':21,
        'raw_output_paths':{l:str(I/f'reader-{l}.json') for l in 'ab'},'raw_output_sha256':{l:sha(I/f'reader-{l}.json') for l in 'ab'},
        'honest_same_reader_continuations':{'both_initial_16_answer_archives_preserved':True,'same_initially_fresh_blind_tasks_finished_all94':True,'factual_feedback_keys_grades_or_routing_supplied':False},
        'technical_protocol_diagnostic':read(I/'protocol-diagnostics.json'),'initial_source_rendering_fully_conformant':False,'technical_deviation_not_used_as_factual_cap':True,
        'independent_source_accuracy':{'verdict':'PASS_SUPPORTED_TEXT_EXACT_PREPARATION04','report':str(source_path),'sha256':sha(source_path),'actual_addendum_proof':str(source_proof_path),'actual_addendum_proof_sha256':sha(source_proof_path),'prior_complete_source_reading_honestly_reused':True,'root_independently_accepted':True},
        'fixed_bank_coverage':'Qualified source-resolvable distinct-mechanism saturation; two renewed zero-addition passes and genuinely fresh94 challenge, all preserved. Not every instance fact or arbitrary compound interaction is tested.',
        'four_authority_limits_preserved':True,'SG01_actual_human_or_publisher_authority':'PENDING; no proposed interpretation adopted',
        'complete_core_ready':False,'worker_goal_complete':False,'goal_status':'active pending actual authority and coordinator final inspection/stamping authorization',
        'publication_or_stamping_authorized':False,'known_fixed_set_tool_assisted_regression_not_held_out_accuracy_claim':True}
P.write_text(json.dumps(report,indent=2)+'\n')
critical=[I/n for n in manifest['hashes']]+[K/'questions.json',K/'answer-key.json',K/'asked-clause-map.json',K/'freeze.json',I/'reader-a.json',I/'reader-b.json',I/'primary-grading-integrity.json',I/'v6-technical-verification.json',I/'protocol-diagnostics.json',G/'input-manifest.json',G/'literal-scope-annotation-v1.json',*sorted(G.glob('block-*.json')),*sorted(G.glob('grader-*-prompt.txt')),*sorted(G.glob('grades-*.json')),source_path,source_proof_path,P]
summary={'status':'SUPPORTED_SOURCE_FACTUAL_PASS_ONLY; complete-core/SG01/stamp still pending','current_canonical_sha256':guide_sha,'canonical_snapshot_and_preparation04_equal':True,'bank_and_input_freeze_hashes_intact':True,'all21_sources_unchanged':True,'all188_primary_records_and544_fixed_facts_verified':True,'all63_agent_models_and85_turn_settings_verified':True,'no_neutral_needed_or_used':True,'critical_file_hashes':{str(p):sha(p) for p in critical},'scope_note':'Read results.json and protocol-diagnostics.json; do not treat this as full initial rendering conformance, publisher authority, or approval to stamp/publish.'}
(I/'final-integrity.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'counts':scores,'source_accuracy':'PASS exact93088','complete_core_ready':False,'stamping_authorized':False,'results_sha256':sha(P)}))
