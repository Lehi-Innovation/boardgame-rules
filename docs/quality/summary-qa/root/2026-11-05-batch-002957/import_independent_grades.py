from build_evidence import *
import manage,sys
name=sys.argv[1];benchmark=sys.argv[2];I=R/name
d=json.loads((I/'independent-grades.json').read_text());allrows={}
expected_ids={q['id'] for q in json.loads((R/benchmark/'questions.json').read_text())['questions']}
for w in ['a','b']:
 reader=d['readers']['reader-'+w]
 rows=reader.get('answers',reader.get('grades'));assert rows is not None
 allrows[w]={x['id']:x for x in rows};assert len(allrows[w])==len(rows)
 assert set(allrows[w])==expected_ids
 assert reader['totals']=={g:sum(x['grade']==g for x in rows) for g in ['correct','partial','incorrect']}
notes={w:{id:(row['grade'],row['reason']) for id,row in rows.items()} for w,rows in allrows.items()}
manage.grades(name,benchmark,notes)
out=json.loads((I/'results.json').read_text())
for w in ['a','b']:
 for row in out[w]['grades']:
  raw=allrows[w][row['id']]
  for k in ['requested_fact_checklist','summary_support','unsupported_guess']:row[k]=raw[k]
 out[w]['independent_grader']='independent-grades.json'
save(I/'results.json',out)
print(json.dumps({w:out[w]['totals'] for w in ['a','b']},indent=2))
