from build_bank import *
import copy
# All question wording and expected answers remain exactly as seed-v2.
q=json.loads((ROOT/'seed-v2/questions.json').read_text())['questions']
k=json.loads((ROOT/'seed-v2/answer-key.json').read_text())['answers']
rows=[dict(a,question=b['question']) for a,b in zip(k,q)]
before=copy.deepcopy(rows)
for e in rows:
 fs=e['required_facts'];ctx=e['contextual_background'];i=e['id']
 if i=='Q01':ctx.append(next(f['fact'] for f in fs if f['id']=='Q01.F02')+'; internal Confluence steps are not asked by phase-order clause.');e['required_facts']=[f for f in fs if f['id']!='Q01.F02']
 if i=='Q04':
  ctx += ['Printed invention points are earned at invention; point amount is not asked.','Sharing Bonus is per invention; frequency is not separately asked.']
  next(f for f in fs if f['id']=='Q04.F03')['fact']='Flip research team'
  next(f for f in fs if f['id']=='Q04.F06')['fact']='Sharing Bonus collected at Confluence'
 if i=='Q11':
  ctx += ['Starting colony receives a seedling.','No new seedling merely for a tokenless colony traded to Caylion.']
  next(f for f in fs if f['id']=='Q11.F02')['fact']='Add seedling on acquisition from colony bid track'
  e['required_facts']=[f for f in fs if f['id']!='Q11.F03']
 if i=='Q17':
  ctx += ['Loaned pair returns at turn end; timing tested by Q03 general loan rule.','Nullspace entry converter produces no other output.']
  next(f for f in fs if f['id']=='Q17.F03')['fact']='May loan intact pair as a single card'
  next(f for f in fs if f['id']=='Q17.F04')['fact']='Nullspace enters via top converter during Trade'
 if i=='Q18':
  ctx += ['Gray Unity wild cubes may themselves pay matching-size Unity wild inputs; not separately asked here.']
  next(f for f in fs if f['id']=='Q18.F03')['fact']='Unity wild inputs match size and may mix colors'
if __name__=='__main__':
 write('seed-v3',rows)
 changes=[{'id':a['id'],'before':b,'after':a} for b,a in zip(before,rows) if a!=b]
 assert all(a['expected_answer']==b['expected_answer'] and a['question']==b['question'] for a,b in zip(before,rows))
 (ROOT/'seed-v3'/'scope-correction-record.json').write_text(json.dumps({'reason':'Fresh independent source/question-only challenge identified true but unasked atoms bundled into required facts. Asked clauses, exceptions and numeric applications retained.','review':'../seed-v2/fresh-scope-challenge.json','question_and_expected_answer_text_unchanged':True,'earlier_versions_and_raw_grades_preserved':True,'future_readers':'New readers on newly frozen seed-v3; no informed reader reuse, no retrospective replacement of historical grades.','coverage_credit':'Moved atoms receive no asked-fact coverage credit unless explicitly asked by another accepted question.','changes':changes},ensure_ascii=False,indent=2)+'\n')
 print('seed-v3 frozen; unchanged20 questions/expected answers; exact asked facts clarified')
