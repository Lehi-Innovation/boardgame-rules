from pathlib import Path
import collections,hashlib,json
B=Path(__file__).parent.resolve();I=B/'expanded-luna-iteration-01';G=I/'grading';P=I/'results.json';assert not P.exists(),'Never overwrite historical results'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primary=[]
for p in sorted(G.glob('grades-*.json')):
 d=json.loads(p.read_text());primary+=d.get('records',d.get('grades',d.get('entries',[])))
assert len(primary)==186
neutral_path=G/'fresh-borderline-adjudication.json';neutral=json.loads(neutral_path.read_text());nm={(x['reader'],x['id']):x for x in neutral['records']};assert len(nm)==13
counts={name:collections.Counter() for name in ['primary_fixed_v7','one_neutral_fixed_v7','literal_scope_v8_assessment']};records=[]
for x in primary:
 l=x['reader'];i=x['id'];n=nm.get((l,i));effective=n['label'] if n else x['label'];literal='Correct' if (l,i)==('a','Q73') else effective
 for name,label in [('primary_fixed_v7',x['label']),('one_neutral_fixed_v7',effective),('literal_scope_v8_assessment',literal)]:counts[name][(l,label)]+=1
 records.append({'reader':l,'id':i,'raw_entry_sha256':x['raw_entry_sha256'],'primary_label':x['label'],'neutral_label':n['label'] if n else None,'effective_fixed_v7_label':effective,'literal_scope_v8_label':literal,'scope_correction':('Q73 literal question asks possibility only; independently confirmed unasked numerical detail demoted for v8; frozen v7/raw primary/raw neutral retained.' if (l,i)==('a','Q73') else None)})
assert len({(x['reader'],x['id']) for x in records})==186
scope=B/'full-bank-scope-validator/revision-04/q73-scope-review.json';confirm=B/'full-bank-scope-validator/revision-05/scope-review.json'
report={'status':'FAILED historical preliminary/current-bank run; new exact-body full pair required','benchmark':'expanded-candidate-v7','question_count':93,'snapshot_sha256':sha(I/'summary-snapshot.md'),'counts':{name:{l:{label:c[(l,label)] for label in ['Correct','Partial','Incorrect']} for l in ['a','b']} for name,c in counts.items()},'records':records,'one_neutral_adjudication':{'path':str(neutral_path),'sha256':sha(neutral_path),'pairs':13,'further_sampling':False,'actual_delivery_and_raw_links':str(I/'fresh-adjudication-integrity.json')},'scope_correction':{'next_benchmark':'expanded-candidate-v8','question_entries_and_expected_answers_unchanged':True,'scope_report':str(scope),'scope_report_sha256':sha(scope),'v8_confirmation':str(confirm),'v8_confirmation_sha256':sha(confirm),'frozen_v7_retroactively_edited':False,'raw_neutral_Q73_label':'Partial under frozen map','neutral_Q73_semantic_finding':'Actual literal possibility question fully answered; numerical magnitude is unasked context.'},'independent_source_accuracy':'FAIL NA-SRC-001 on historical e1a body; preserved original source-audit.json','source_failure_link':str(I/'source-status.json'),'canonical_repair':'preparation02 has supported-text source-only PASS; reader repairs still pending','whole_run_pass':False,'complete_core_scope':'NOT_READY essential SG01 actual human/publisher authority pending','primary_grade_integrity':str(I/'primary-grading-integrity.json'),'reader_delivery':str(I/'actual-delivery-verification.json'),'unresolved_or_guessed_parts_zero_claimed':False,'later_full_pair_required':True}
P.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['counts']))
p=B/'progress.json';d=json.loads(p.read_text());d['phase']='expanded01_failed_preserved_repairing_general_summary_before_next_full_pair';d['expanded01_results_path']=str(P);d['expanded01_effective_fixed_v7']=report['counts']['one_neutral_fixed_v7'];d['expanded01_literal_scope_v8']=report['counts']['literal_scope_v8_assessment'];d['fresh_borderline_adjudication_pending']=[];p.write_text(json.dumps(d,indent=2)+'\n')
