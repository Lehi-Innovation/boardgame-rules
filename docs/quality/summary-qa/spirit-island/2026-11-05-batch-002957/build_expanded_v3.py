from pathlib import Path
import json,hashlib
B=Path(__file__).parent;old=B/'expanded-v2';q=json.loads((old/'questions.json').read_text());k=json.loads((old/'answer-key.json').read_text());nov=[]
def add(ques,ans,refs,new):
 i=f"Q{len(q['questions'])+1:02}";q['questions'].append({'id':i,'question':ques});k['answers'].append({'id':i,'answer':ans,'source_refs':refs});nov.append({'id':i,'new_coverage':new,'source_refs':refs})
add('A Ravage adds Blight that reduces Vital Strength of the Earth’s Sacred Site to one Presence. Does losing the site retroactively remove its Defend from the Damage simultaneously dealt to Dahan in that Ravage?', 'No. Land and Dahan damage are simultaneous, so the existing Sacred Site’s Defend protects both in that Ravage. Loss of site from resulting Blight does not retroactively remove that protection.', ['FAQ Core: .bu6oc8y; .7w4g8ot'], 'Simultaneous Ravage prevents retroactive loss of defending site; distinct timing interaction beyond general damage arithmetic.')
add('Can a Spirit give its unused Energy or Card Plays to another Spirit, or save unused Card Plays for the next turn? How does this differ from an explicit Power that grants another Spirit Energy or an extra play?', 'No ordinary sharing of individual Energy or Card Plays; Energy stays with its Spirit and can carry over, unused Card Plays expire. Explicit Power grants follow their instructions and can grant Energy or extra plays, but are not free sharing of the ordinary limits/resources.', ['CORE p.13','FAQ Core: .bu6ocb5'], 'Individual resource ownership versus explicit grant exception.')
q['benchmark_version']=k['benchmark_version']='expanded-v3';D=B/'expanded-v3';D.mkdir(exist_ok=True)
for name,x in [('questions.json',q),('answer-key.json',k),('novelty.json',nov)]:
 p=D/name
 if p.exists():raise RuntimeError('Refuse overwrite')
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
(D/'question-bank.md').write_text('# Spirit Island expanded bank v3\n\nOriginal and previous entries preserved.\n\n'+'\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n**Expected:** {y['answer']}\n\n**Sources:** {'; '.join(y['source_refs'])}" for x,y in zip(q['questions'],k['answers']))+'\n')
(D/'input-manifest.json').write_text(json.dumps({'question_count':len(q['questions']),'prior_version':'expanded-v2','prior_entries_preserved':q['questions'][:100]==json.loads((old/'questions.json').read_text())['questions'] and k['answers'][:100]==json.loads((old/'answer-key.json').read_text())['answers'],'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'questions.json',D/'answer-key.json',old/'questions.json',old/'answer-key.json']},'source_manifest':'../source-manifest.json'},indent=2)+'\n')
print('Frozen expanded-v3:',len(q['questions']))
