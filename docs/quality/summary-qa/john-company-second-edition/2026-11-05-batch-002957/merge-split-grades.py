"""Preserve raw graders; combine complete per-reader arrays with fixed inputs."""
from pathlib import Path
import collections,json,sys
R=Path(__file__).resolve().parent
benchmark,iteration=sys.argv[1:3]
i=R/benchmark/iteration
q={x['id']:x for x in json.loads((R/benchmark/'questions.json').read_text())['questions']}
k={x['id']:x for x in json.loads((R/benchmark/'answer-key.json').read_text())['answers']}
out={'benchmark_version':benchmark,'iteration':iteration,'status':'FAILED','grading_policy':'Independent grades for every material requested part; equivalent wording accepted, no cross-answer borrowing. Omissions or express abstentions Partial; contradictions Incorrect. Q015 remains independently SOURCE-BLOCKED Partial, with known-rule recovery assessed separately.','readers':{}}
for role in 'ab':
 raw={x['id']:x for x in json.loads((i/f'reader-{role}.json').read_text())['answers']}
 report=json.loads((i/f'grades-reader-{role}.json').read_text());gs=report.get('grades',report.get('answers',report.get('adjudications')))
 assert collections.Counter(x['id'] for x in gs)==collections.Counter(q.keys())
 grades=[]
 for g in gs:
  z=dict(g);qid=g['id'];z['grade']=z['grade'].capitalize();assert z['grade'] in ['Correct','Partial','Incorrect']
  z.update(question=q[qid]['question'],expected_answer=k[qid]['expected_answer'],observed_answer=raw[qid]['answer'],source_references=k[qid]['source_references'],summary_evidence=raw[qid].get('evidence'),reader_support_label=raw[qid].get('support'));grades.append(z)
 out['readers']['reader-'+role]={'grade_report':f'grades-reader-{role}.json','grades':grades,'counts':{s:sum(x['grade']==s for x in grades) for s in ['Correct','Partial','Incorrect']}}
 assert next(x for x in grades if x['id']=='Q015')['grade'] in ['Partial','Incorrect'],'Do not erase known source gap or excuse a known-rule contradiction.'
out['source_supported_questions_all_correct']=all(x['counts']['Correct']==len(q)-1 and x['counts']['Partial']==1 and x['counts']['Incorrect']==0 for x in out['readers'].values())
out['complete_core_PASS']=False
p=i/'results.json';assert not p.exists(),'Preserve existing results';p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({role:rv['counts'] for role,rv in out['readers'].items()},indent=2))
