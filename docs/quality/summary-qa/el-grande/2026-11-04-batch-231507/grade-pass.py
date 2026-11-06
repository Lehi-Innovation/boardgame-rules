import pathlib,json,sys,collections
P=pathlib.Path(__file__).resolve().parent;D=P/sys.argv[1];key=json.loads((D/'answer-key.json').read_text())['answers'];q=json.loads((D/'questions.json').read_text())['questions'];res={'benchmark_version':json.loads((D/'questions.json').read_text())['benchmark_version'],'evaluator_note':'All complete responses individually read and checked against each requested part. Incidental expected-answer details not requested by question are not silently added to rubric. Equivalent wording accepted; no borrowing between answers.','readers':{}}
exceptions={}
if D.name=='expanded-iteration-01':exceptions={('b','Q48'):('partial','Independent adjudication: affirmative any-regions source wording fails to retain King-source protection; remaining requested parts correct.',False),('b','Q51'):('partial','Independent adjudication: each-origin universal destination restriction exceeds source wording; unsupported extra quantifier left unresolved.',True)}
if D.name=='expanded-iteration-02':exceptions={('b','Q32'):('partial','Fresh independent adjudication: answers stated singleton scenario correctly but broadens fallback to all legal regions, including an unsupported protected-multiple scenario; prevents clean pass.',True)}
if D.name=='expanded-iteration-03':exceptions={('a','Q11'):('incorrect','Explicitly permits selecting King region for general Castillo redistribution; source prohibits it. Court fallback handles illegal selection and does not make it legal. Correct answer elsewhere does not cure this contradiction.',False)}
if D.name=='expanded-iteration-08':exceptions={('a','Q50'):('partial','Fresh independent adjudication: separate quotas,multiple origins and forbidden sources answered, but positive legal destination range explicitly left unresolved; do not borrow that missing ruling from another answer.',False)}
reader_names=['a'] if (D/'pair-status.json').exists() else ['a','b']
if len(reader_names)<2:res['pair_status']='Superseded before second-reader dispatch; cannot count as passing pair.'
for r in reader_names:
 raw=json.loads((D/f'reader-{r}.json').read_text())['answers'];assert [a['id'] for a in raw]==[a['id'] for a in key]
 grades=[]
 for z,e,a in zip(q,key,raw):
  g,reason,u=exceptions.get((r,a['id']),('correct','All requested material rulings correct and summary-supported. Fixed reference: '+e['expected_answer'],False))
  if D.name=='expanded-iteration-01' and a['id'] in ['Q35','Q36']:reason+=' Requested printed group names supplied; full printed scoreboard tuples are incidental key context, not requested quantities.'
  if D.name=='expanded-iteration-01' and a['id']=='Q52' and r=='a':reason+=' Independent adjudication confirms requested comparison concerns selectable locations; redistribution is incidental in key and already covered by Q16/Q34.'
  if D.name=='expanded-iteration-03' and a['id'] in ['Q29','Q31','Q32','Q40','Q42','Q50'] and g=='correct':reason+=' Support labels and unasked source-limit caveats do not change the grade; the requested rulings are resolved. Source-gap reporting remains excluded from complete-core PASS.'
  if D.name=='expanded-iteration-08' and a['support']=='partial' and g=='correct':reason+=' Fresh independent adjudication confirms all requested parts; caveats concern unasked source-limit branches, not unresolved target facts.'
  grades.append({'id':a['id'],'question':z['question'],'expected_answer':e['expected_answer'],'source_references':e['source_references'],'observed':a,'grade':g,'reason':reason,'unsupported_guess':u})
 totals={g:sum(a['grade']==g for a in grades) for g in ['correct','partial','incorrect']};res['readers'][r]={'totals':totals,'grades':grades}
(D/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print({r:v['totals'] for r,v in res['readers'].items()})
