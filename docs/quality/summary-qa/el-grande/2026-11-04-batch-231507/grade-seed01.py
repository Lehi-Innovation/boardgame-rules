import pathlib,json,collections
P=pathlib.Path(__file__).parent;D=P/'seed-iteration-01';key=json.loads((D/'answer-key.json').read_text())['answers'];questions=json.loads((D/'questions.json').read_text())['questions']
notes={
'Q01':('correct','Assignment and all ten destinations correct; summary evidence includes shuffled region cards.'),
'Q02':('incorrect','Wrong first-round starter: source says players choose, not youngest. Clockwise also omitted.'),
'Q03':('partial','Recruitment timing/value correct but does not resolve at-most/optional recruitment allowance.'),
'Q04':('partial','Fails to resolve every protected source, especially Castillo.'),
'Q05':('partial','Gives maximum but explicitly leaves fewer-than-maximum use unresolved.'),
'Q06':('partial','Noninterleaving requirement explicitly unresolved.'),
'Q07':('partial','Unselected round-end card destination omitted/unresolved.'),
'Q08':('partial','Reader A leaves King movement’s change to protected region explicitly unresolved.'),
'Q09':('correct','Announced amount, unrestricted entry and general-only exit correctly resolved.'),
'Q10':('correct','All four scoring stages, rounds and selection before revelation correct.'),
'Q11':('partial','Illegal King-region selection consequence (own court) unresolved.'),
'Q12':('partial','Reader A resolves leaders correctly but next player’s third rank/1 point unresolved.'),
'Q13':('incorrect','Reader A awards tied third players2 instead of dropping to fourth/0.'),
'Q14':('partial','Player-count rank cutoffs and tie result unresolved; abstention is partial.'),
'Q15':('correct','Both2-point bonuses on scoring and sole-majority/tie conditions correctly stated.'),
'Q16':('correct','No emptying/redistribution, remains until general scoring correctly resolved.'),
'Q17':('partial','Castillo placement, stacking and orientation unresolved.'),
'Q18':('partial','Complete legal move/destination and new home effects unresolved.'),
'Q19':('partial','Recovery choice, current-turn eligibility and secrecy unresolved.'),
'Q20':('partial','Rounds/winner correct but answer does not specify game ends after third/final general scoring.')}
res={'benchmark_version':'v1-seed','grading_standard':'../grading-standard.json','readers':{}}
for r in ['a','b']:
 obs=json.loads((D/f'reader-{r}.json').read_text())['answers']; assert [a['id'] for a in obs]==[a['id'] for a in key]
 grades=[]
 for question,e,a in zip(questions,key,obs):
  grade,reason=notes[a['id']]
  if r=='b':
   if a['id']=='Q08':grade,reason='correct','Answers taboo objects, scoring permission and King movement changing protected region; generic other-details caveat does not leave a requested ruling unresolved.'
   if a['id']=='Q12':grade,reason='incorrect','Wrong3-way-tie rank: awards1 each instead of3 each; next player unresolved.'
   if a['id']=='Q13':grade,reason='partial','Tied-third fourth-place score explicitly unresolved rather than source-contradicting.'
   if a['id']=='Q16':grade,reason='partial','Explicitly leaves redistribution unsupported despite correct no-emptying statement.'
  grades.append({'id':a['id'],'question':question['question'],'expected_answer':e['expected_answer'],'source_references':e['source_references'],'observed':a,'grade':grade,'reason':reason,'unsupported_guess':a['id'] in (['Q13'] if r=='a' else ['Q12'])})
 res['readers'][r]={'totals':dict(collections.Counter(x['grade'] for x in grades)),'grades':grades}
(D/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print({r:v['totals'] for r,v in res['readers'].items()})
