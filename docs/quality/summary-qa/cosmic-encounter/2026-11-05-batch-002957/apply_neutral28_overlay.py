"""Create a separate exact-source overlay; never rewrite primary reports."""
from pathlib import Path
from collections import Counter
import copy,hashlib,json
R=Path(__file__).parent.resolve();IT=R/'expanded-iteration-06'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=IT/'original-grades-aggregate.json';original=read(source);neutral=read(IT/'neutral28-adjudication.json')
assert read(IT/'neutral28-runtime-delivery-validation.json')['pass']
assert read(IT/'neutral28-case-integrity-validation.json')['pass']
readers=copy.deepcopy(original['readers']);changes=[];confirmed=[]
for index,result in enumerate(neutral['assessments']):
    label,qid=result['reader_label'],result['id'];entry=next(x for x in readers[label] if x['id']==qid)
    previous=entry['grade'];entry['original_primary_grade']=previous;entry['grade']=result['grade']
    entry['neutral_adjudication']={'path':str(IT/'neutral28-adjudication.json'),'sha256':sha(IT/'neutral28-adjudication.json'),'json_pointer':f'/assessments/{index}','case_id':result['case_id']}
    record={'reader':label,'id':qid,'original_primary_grade':previous,'effective_grade':result['grade'],'case_id':result['case_id']}
    (changes if previous!=result['grade'] else confirmed).append(record)
for primary in original['original_reports']:assert sha(Path(primary['path']))==primary['sha256']
counts={label:dict(Counter(x['grade'] for x in entries)) for label,entries in readers.items()}
totals={label:{key:counts[label].get(key,0) for key in ('correct','partial','incorrect')} for label in readers}
report={'iteration':IT.name,'status':'Supported-bank factual results after one fresh whole-entry adjudication; workflow and authority limits remain separate.','question_count':original['question_count'],'readers':readers,'totals':totals,'original_primary_totals':original['totals'],'original_primary_aggregate_path':str(source),'original_primary_aggregate_sha256':sha(source),'original_primary_reports':original['original_reports'],'all_original_primary_reports_unchanged':True,'adjudications_applied':True,'fresh_neutral_count':1,'whole_neutral_case_count':len(neutral['assessments']),'grade_changes':changes,'original_grades_confirmed_by_neutral':confirmed,'neutral_report_path':str(IT/'neutral28-adjudication.json'),'neutral_report_sha256':sha(IT/'neutral28-adjudication.json'),'neutral_actual_delivery_validation_path':str(IT/'neutral28-runtime-delivery-validation.json'),'neutral_case_integrity_validation_path':str(IT/'neutral28-case-integrity-validation.json'),'both_readers_all_correct':all(x['grade']=='correct' for rows in readers.values() for x in rows),'workflow_conformance_pass':False,'workflow_failures_not_factual_grade_caps':True,'underlying_original_two_input_availability_independently_verified':True,'independent_final_bookkeeping_delta_pending':True,'final_scope_readiness':False,'verified_stamp_applied':False,'full_core_verified_claim':False,'essential_external_authority_gap':'FAQ reinforcement/Negotiate conflict.','human_interpretation_adopted':False,'no_new_source_vote_or_native_image_quota_inferred':True}
p=IT/'adjudicated-grades-aggregate.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n')
print({'effective_totals':totals,'changed_labels':len(changes),'confirmed_original_labels':len(confirmed),'workflow_conformance_pass':False,'final_scope_readiness':False})
