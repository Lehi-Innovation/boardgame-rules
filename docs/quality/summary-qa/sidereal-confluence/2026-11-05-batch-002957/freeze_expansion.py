from build_bank import *
from seed_corrections import corrected_seed
from expand_bank import expand
import copy

def prepare():
 corrected_seed(); rows=expand(); rejected=[]
 # Preserve the final independently scoped seed-v3 entries exactly.
 seedq=json.loads((ROOT/'seed-v3/questions.json').read_text())['questions']; seedk=json.loads((ROOT/'seed-v3/answer-key.json').read_text())['answers']
 rows[:20]=[dict(k,question=q['question']) for k,q in zip(seedk,seedq)]
 rows[:]=[e for e in rows if not (e['id']=='Q30' and rejected.append({'candidate_question':e['question'],'decision':'reject','reason':'No new rule/outcome branch: ordinary tie priority now explicitly required by corrected seed Q08. Changed names/concrete tie ordering repeats that priority.'}) is None)]
 # Above filter rejects Q30 while preserving all original seed records.
 for e in rows:
  old=e['id'];fs=e['required_facts'];ctx=e['contextual_background']
  if old=='Q28':ctx.append(fs[0]['fact']);e['required_facts']=fs[1:]
  if old=='Q32':ctx.append(fs[-1]['fact']);e['required_facts']=fs[:-1]
  if old=='Q37':fs[-1]['fact']='Consumed ordinary colony goes beneath colony deck';ctx.append('Top relic enters; ordinary colony goes front side face up.')
  if old=='Q38':e['expected_answer']='Gain one point and take the top two colonies. Holder gains two Colony Support; loan card for turn transfers support. Im’dril can use it to hold colonies into Economy.';fs.insert(0,{'fact':'Gain one point when played from deck'});e['source_references'].append('Original Automated Transport Network printed card61/396')
  if old=='Q41':fs[-1]['fact']='Ordinary colony goes beneath colony deck';ctx.append('Ordinary colony is front-side face up (orientation tested separately).')
  if old=='Q42':e['source_references'].append('Original Star’s Ruin printed card66/396 identifies Sharing Bonus as sheet’s Invention Bonus')
  if old=='Q45':ctx.append(fs[-1]['fact']);e['required_facts']=fs[:-1]
  if old=='Q46':fs[1]['fact']='Top enters, bottom upgrades/flips, both during Trade';ctx.append('Pay the converters’ printed costs; exact costs not asked.')
  if old=='Q48':fs[1]['fact']='Dispose of excess before Economy-start support check';ctx.append('One support is a given. Remaining excess goes beneath deck at check; destination covered separately.')
  if old=='Q55':ctx.append(fs[0]['fact']+'; expressly stated in scenario.');e['required_facts']=fs[1:]
  if old=='Q61':ctx.append('Normal economic simultaneous-production restriction also remains; not independently asked here.')
 for n,e in enumerate(rows,1):
  if n<=20:continue
  e['id']=f'Q{n:02}'
  for j,f in enumerate(e['required_facts'],1):f['id']=f"{e['id']}.F{j:02}"
 seedq=json.loads((ROOT/'seed-v3/questions.json').read_text())['questions'];seedkey=json.loads((ROOT/'seed-v3/answer-key.json').read_text())['answers']
 assert [{'id':e['id'],'question':e['question']} for e in rows[:20]]==seedq
 assert [{k:v for k,v in e.items() if k!='question'} for e in rows[:20]]==seedkey
 return rows,rejected
if __name__=='__main__':
 grade=json.loads((ROOT/'seed-iteration-03/results.json').read_text())
 assert grade['totals']=={'correct':40,'partial':0,'incorrect':0}, 'Initial fixed-bank pair must pass before expansion freeze'
 rows,rejected=prepare();write('expanded-v1',rows)
 (ROOT/'expanded-v1'/'initial-rejections.json').write_text(json.dumps(rejected,indent=2)+'\n')
 print('Expanded bank frozen',len(rows))
 for e in rows:print(e['id'],e['novelty'])
