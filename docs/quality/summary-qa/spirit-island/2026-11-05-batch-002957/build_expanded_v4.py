from pathlib import Path
import json,hashlib
B=Path(__file__).parent;old=B/'expanded-v3';q=json.loads((old/'questions.json').read_text());k=json.loads((old/'answer-key.json').read_text())
q['questions'].append({'id':'Q103','question':'What is the order of the Invader Phase, and if a Blighted Island start-of-phase effect destroys a Spirit’s last Presence, may an earned Fear Card resolve first to avert defeat?'})
k['answers'].append({'id':'Q103','answer':'Resolve Blighted Island instructions first, then earned Fear, Ravage, Build, Explore and advance Invader cards. Finish the Blighted effect action tree and check outcomes before Fear; if a Spirit still has no island Presence and no win condition is met then, lose without resolving the later Fear card. Cannot reorder to avert loss.','source_refs':['CORE pp.9-10,12','FAQ Core: .9v5kfq7']})
q['benchmark_version']=k['benchmark_version']='expanded-v4';D=B/'expanded-v4';D.mkdir(exist_ok=True)
for name,x in [('questions.json',q),('answer-key.json',k),('novelty.json',[{'id':'Q103','new_coverage':'Invader phase ordering has a consequential outcome check before earned Fear can resolve.','source_refs':k['answers'][-1]['source_refs']}])]:
 p=D/name
 if p.exists():raise RuntimeError('Refuse overwrite')
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
(D/'question-bank.md').write_text('# Spirit Island expanded bank v4\n\nAll prior entries preserved.\n\n'+'\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n**Expected:** {y['answer']}\n\n**Sources:** {'; '.join(y['source_refs'])}" for x,y in zip(q['questions'],k['answers']))+'\n')
(D/'input-manifest.json').write_text(json.dumps({'question_count':103,'prior_version':'expanded-v3','prior_entries_preserved':q['questions'][:102]==json.loads((old/'questions.json').read_text())['questions'] and k['answers'][:102]==json.loads((old/'answer-key.json').read_text())['answers'],'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'questions.json',D/'answer-key.json',old/'questions.json',old/'answer-key.json']},'source_manifest':'../source-manifest.json'},indent=2)+'\n')
print('Frozen expanded-v4:103')
