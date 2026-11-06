from pathlib import Path
import json,hashlib
B=Path(__file__).parent;old=B/'expanded-v4';q=json.loads((old/'questions.json').read_text());k=json.loads((old/'answer-key.json').read_text());adds=json.loads((B/'coverage-additions-draft.json').read_text())
adds.append({'id':'Q112','question':'For a standard game, how many balanced Island Boards are used and chosen, how are their initial Invaders, Dahan and Blight placed, and how are the Minor/Major decks and shared piece supplies prepared?','answer':'Randomly choose one balanced Island Board per Spirit and join them into the island. Populate every land according to its printed Invader, Dahan and Blight icons, taking setup Blight from the box rather than depleting the pool; setup Blight does not cascade or destroy Presence. Shuffle Minor and Major decks separately, each with its own shared discard space, and put Energy, Invaders and Dahan in shared supplies accessible to players.','source_refs':['CORE p.6 Island and Supply; pp.13,15','FAQ Setup: .9v5ka5b'],'new_coverage':'Whole initial island population and shared supply setup were not actually requested by the earlier deck/pool or Spirit-personal-setup questions. Parent found in reopened procedural sweep.'})
for a in adds:q['questions'].append({'id':a['id'],'question':a['question']});k['answers'].append({'id':a['id'],'answer':a['answer'],'source_refs':a['source_refs']})
q['benchmark_version']=k['benchmark_version']='expanded-v5';D=B/'expanded-v5';D.mkdir(exist_ok=True)
for name,x in [('questions.json',q),('answer-key.json',k),('novelty.json',adds)]:
 p=D/name
 if p.exists():raise RuntimeError('Refuse overwrite '+str(p))
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
(D/'question-bank.md').write_text('# Spirit Island expanded bank v5\n\nAll original and earlier entries preserved. New questions follow the independent challenge and reopened procedural sweep.\n\n'+'\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n**Expected:** {y['answer']}\n\n**Sources:** {'; '.join(y['source_refs'])}" for x,y in zip(q['questions'],k['answers']))+'\n')
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(D/'input-manifest.json').write_text(json.dumps({'question_count':len(q['questions']),'prior_version':'expanded-v4','prior_entries_preserved':q['questions'][:103]==json.loads((old/'questions.json').read_text())['questions'] and k['answers'][:103]==json.loads((old/'answer-key.json').read_text())['answers'],'sha256':{str(p):H(p) for p in [D/'questions.json',D/'answer-key.json',old/'questions.json',old/'answer-key.json']},'source_manifest':'../source-manifest.json','source_key_corrections':[],'new_questions':len(adds)},indent=2)+'\n')
print('Frozen expanded-v5:',len(q['questions']),'prior103 preserved.')
