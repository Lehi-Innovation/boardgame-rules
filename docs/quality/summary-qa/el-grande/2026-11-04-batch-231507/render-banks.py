from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
for d in sorted(P.glob('benchmark-v[0-9]')):
 q=json.loads((d/'questions.json').read_text());k=json.loads((d/'answer-key.json').read_text());out=[f"# El Grande question and answer bank — {q['benchmark_version']}\n",f"Scope: {q['scope']}.\n",'Answers fixed before any reader dispatch for this version. Original Q01–Q20 remain unchanged.\n']
 for z,a in zip(q['questions'],k['answers']):
  out += [f"## {z['id']}\n",z['question']+'\n','**Expected:** '+a['expected_answer']+'\n','**Source:** '+ '; '.join('Publisher PDF pp.'+r['pdf_pages']+', '+r['section'] for r in a['source_references'])+'\n']
  if 'novelty' in a:out+=['**Distinct coverage:** '+a['novelty']+'\n']
 if d.name in ['benchmark-v5','benchmark-v6','benchmark-v7']:out[2]='Explicit source/scenario correction: Q12/Q13 now specify four players so no fifth count is unstated. Historical original20 remain intact in v1–v4; all answers unchanged. See ../benchmark-corrections-v5.json; v6 also explicitly limits Q13 to scoreboard points before bonuses (benchmark-corrections-v6.json).\n'
 (d/'question-bank.md').write_text('\n'.join(out))
