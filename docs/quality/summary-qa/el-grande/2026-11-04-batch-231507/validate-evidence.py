import pathlib,json,hashlib,sys,subprocess,re
P=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('/home/jonny/projects/boardgame-rules');final=sys.argv[1] if len(sys.argv)>1 else None
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,details=None):checks.append({'check':name,'passed':bool(ok),'details':details})
original=json.loads((P/'input-manifest.json').read_text())['input_hashes']
for s,v in original.items():
 if s!='rules/el-grande.md':check('Source unchanged: '+s,h(ROOT/s)==v)
check('Original canonical preserved',h(P/'baseline-summary.md')==original['rules/el-grande.md'])
q0=json.loads((P/'benchmark-v1/questions.json').read_text())['questions'];k0=json.loads((P/'benchmark-v1/answer-key.json').read_text())['answers']
for d in sorted(P.glob('benchmark-v[0-9]*')):
 if not (d/'input-manifest.json').exists():continue
 q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];m=json.loads((d/'input-manifest.json').read_text())
 original_questions_ok=q[:20]==q0
 if d.name in ['benchmark-v5','benchmark-v6','benchmark-v7']:original_questions_ok=all(a==b if a['id'] not in ['Q12','Q13'] else a['question']==b['question'].replace('five-player','four-player') for a,b in zip(q[:20],q0)) and (P/'benchmark-corrections-v5.json').exists()
 if d.name in ['benchmark-v6','benchmark-v7']:
  old13=next(a for a in q0 if a['id']=='Q13')['question'];original_questions_ok=all(a==b for a,b in zip(q[:20],q0) if a['id'] not in ['Q12','Q13']) and q[11]['question']==q0[11]['question'].replace('five-player','four-player') and q[12]['question']==json.loads((P/'benchmark-corrections-v6.json').read_text())['new_question']
 answer_preservation=k[:20]==k0 if d.name not in ['benchmark-v6','benchmark-v7'] else all(a==b for a,b in zip(k[:20],k0) if a['id']!='Q13') and k[12]['expected_answer']==json.loads((P/'benchmark-corrections-v6.json').read_text())['new_expected_answer']
 check(d.name+' original20 questions preserved or explicit independently reviewed source correction',original_questions_ok);check(d.name+' original20 answers preserved or explicit score-scope correction',answer_preservation)
 for n,v in m['hashes'].items():check(d.name+' frozen '+n,h(d/n)==v)
 check(d.name+' unique aligned IDs',[x['id'] for x in q]==[x['id'] for x in k] and len(set(x['id'] for x in q))==len(q))
q3=json.loads((P/'benchmark-v3/questions.json').read_text())['questions'];k3=json.loads((P/'benchmark-v3/answer-key.json').read_text())['answers'];q4=json.loads((P/'benchmark-v4/questions.json').read_text())['questions'];k4=json.loads((P/'benchmark-v4/answer-key.json').read_text())['answers']
check('v4 preserves all52 v3 questions/answers',q4[:52]==q3 and k4[:52]==k3)
q2=json.loads((P/'benchmark-v2/questions.json').read_text())['questions'];k2=json.loads((P/'benchmark-v2/answer-key.json').read_text())['answers']
check('v3 preserves all51 v2 question wordings',q3[:51]==q2)
check('Only documented v2 key corrections changed',[a['id'] for a,b in zip(k2,k3) if a!=b]==['Q47','Q49'])
q5=json.loads((P/'benchmark-v5/questions.json').read_text())['questions'];k5=json.loads((P/'benchmark-v5/answer-key.json').read_text())['answers']
check('V5 changes only documented Q12/Q13 stems',[a['id'] for a,b in zip(q4,q5) if a!=b]==['Q12','Q13'])
check('V5 preserves all53 answer objects',k5==k4)
q6=json.loads((P/'benchmark-v6/questions.json').read_text())['questions'];k6=json.loads((P/'benchmark-v6/answer-key.json').read_text())['answers']
check('V6 changes only documented Q13 question',[a['id'] for a,b in zip(q5,q6) if a!=b]==['Q13'])
check('V6 changes only documented Q13 expected-score scope',[a['id'] for a,b in zip(k5,k6) if a!=b]==['Q13'])
q7=json.loads((P/'benchmark-v7/questions.json').read_text())['questions'];k7=json.loads((P/'benchmark-v7/answer-key.json').read_text())['answers']
check('V7 preserves all53 V6 questions/answers',q7[:53]==q6 and k7[:53]==k6 and len(q7)==54)
for d in sorted(P.glob('*-iteration-*')):
 if not d.is_dir():continue
 iteration_check_start=len(checks)
 m=json.loads((d/'input-manifest.json').read_text());q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];ids=[x['id'] for x in q]
 for s,v in m['hashes'].items():check(d.name+' frozen input '+pathlib.Path(s).name,h(pathlib.Path(s))==v)
 version=json.loads((d/'questions.json').read_text())['benchmark_version']
 bank=next(x for x in P.glob('benchmark-v[0-9]') if json.loads((x/'questions.json').read_text())['benchmark_version']==version)
 check(d.name+' question copy equals frozen benchmark', (d/'questions.json').read_bytes()==(bank/'questions.json').read_bytes())
 check(d.name+' key copy equals frozen benchmark', (d/'answer-key.json').read_bytes()==(bank/'answer-key.json').read_bytes())
 if not (d/'results.json').exists():continue
 results=json.loads((d/'results.json').read_text())['readers'];validation=[]
 for r in results:
  raw=json.loads((d/f'reader-{r}.json').read_text())['answers'];grades=results[r]['grades']
  check(d.name+' '+r+' reader IDs',len(raw)==len(ids) and sorted(a['id'] for a in raw)==sorted(ids))
  check(d.name+' '+r+' grade IDs',len(grades)==len(ids) and sorted(a['id'] for a in grades)==sorted(ids))
  ra={a['id']:a for a in raw};ka={a['id']:a for a in k};qa={a['id']:a for a in q}
  check(d.name+' '+r+' grades use exact raw/key/question',all(g['observed']==ra[g['id']] and g['expected_answer']==ka[g['id']]['expected_answer'] and g['question']==qa[g['id']]['question'] for g in grades))
  counts={g:sum(x['grade']==g for x in grades) for g in ['correct','partial','incorrect']};check(d.name+' '+r+' totals',all(results[r]['totals'].get(g,0)==n for g,n in counts.items()))
  (d/f'reader-{r}-sha256.txt').write_text(h(d/f'reader-{r}.json')+'\n')
 prov=json.loads((d/'model-provenance.json').read_text());check(d.name+' runtime readers verified',len([n for n in prov if n.endswith(('_a','_b'))])==len(results) and all(x['confirmed'] for x in prov.values()))
 if d.name==final:
  check('Final snapshot byte identical to canonical', (d/'summary-snapshot.md').read_bytes()==(ROOT/'rules/el-grande.md').read_bytes())
  check('Final pair perfect',all(results[r]['totals'].get('correct')==len(ids) and not results[r]['totals'].get('partial',0) and not results[r]['totals'].get('incorrect',0) and not any(g.get('unsupported_guess') for g in results[r]['grades']) for r in ['a','b']))
  audit=json.loads((d/'source-audit.json').read_text()) if (d/'source-audit.json').exists() else {};check('Final source fidelity audit PASS',audit.get('verdict')=='PASS')
  check('Audit exact summary/source input hashes',all(h(pathlib.Path(s) if pathlib.Path(s).is_absolute() else ROOT/s)==v for s,v in (audit.get('sha256') or audit.get('input_sha256') or {}).items()) and (audit.get('sha256') or audit.get('input_sha256') or {}))
  check('Complete-core outcome remains explicitly incomplete',audit.get('complete_core_verdict')!='PASS')
 (d/'validation.json').write_text(json.dumps({'validation_scope':'This iteration artifact integrity; source fidelity and benchmark scores do not resolve missing core rulings','checks':checks[iteration_check_start:]},ensure_ascii=False,indent=2)+'\n')
for cmd in [[str(ROOT/'.venv/bin/python'),'-m','scripts.validate','rules/el-grande.md'],['git','diff','--check','--','rules/el-grande.md',str(P.relative_to(ROOT))]]:
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);check('Repository: '+' '.join(cmd),r.returncode==0,r.stdout+r.stderr)
report={'validation_scope':'Artifact integrity, exact supported-bank pass and source fidelity only; not complete-core gameplay certification','full_completion':False,'source_resolution':'awaiting-source','passed':all(c['passed'] for c in checks),'checks':checks,'final_iteration':final,'source_limitations':'source-gap-register.json','coordinator_work':'Shared audit registry, targeted stamping, index/manifest/catalog integration delegated exclusively to coordinator.'};(P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'checks':len(checks),'failures':[c for c in checks if not c['passed']]},ensure_ascii=False))
