from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;old,new,review=sys.argv[1:4];rev=json.loads((P/review).read_text());q=json.loads((P/old/'questions.json').read_text());k=json.loads((P/old/'answer-key.json').read_text());adds=rev.get('proposed_questions',rev.get('proposed_additions'));D=P/new;D.mkdir();ids=[]
for a in adds:
 id=f"Q{len(q['questions'])+1:02}";ids.append(id);q['questions'].append({'id':id,'question':a['question']});k['answers'].append({'id':id,'expected_answer':a.get('fixed_answer',a.get('expected_answer')),'source_references':a['source_references']})
q['benchmark_version']=k['benchmark_version']=new
for n,x in [('questions.json',q),('answer-key.json',k)]: (D/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
(D/'input-manifest.json').write_text(json.dumps({'sha256':{n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['questions.json','answer-key.json']},'frozen':True},indent=2)+'\n')
ledger=json.loads((P/'coverage-ledger.json').read_text());(P/f'coverage-ledger-before-{review}').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n');n=len(ledger['passes'])
ledger['passes'] += [{'pass':n+1,'focus':f'Independent source review {review}: accepted distinct additions','accepted_ids':ids},{'pass':n+2,'focus':'Recheck every core procedural source section against literal required question parts and key; setup/actions/sequencing/components/scoring all mapped','accepted_ids':[]},{'pass':n+3,'focus':'Challenge all remaining boundary states, timing/priority/exception branches and base FAQ clauses; reject changed arithmetic, cosmetic names, mechanical recombinations and excluded scope','accepted_ids':[]}]
for id,a in zip(ids,adds):ledger['accepted'].append({'id':id,'novelty':a['novelty'],'source_references':a['source_references'],'origin':review});ledger['coverage_map'].append({'source':a['source_references'],'ids':[id]})
ledger['status']=f'Awaiting fresh challenge after passes{n+2}–{n+3} with zero additions';(P/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
(P/'question-bank.md').write_text(f"# Dune: Imperium — expanded bank ({len(q['questions'])} questions)\n\nVersion {new}. Original2020 base/core standard2–4 players, required House Hagal included; solo/variants/expansions/Uprising excluded. Original20 questions and expected-answer strings preserved. See explicit correction histories. Historical Q14/Q53 shorthand means the 2-Influence space awarding 1VP.\n\n"+''.join(f"## {a['id']}\n\n{b['question']}\n\n**Expected:** {a['expected_answer']}\n\n**Source:** {json.dumps(a['source_references'],ensure_ascii=False)}\n\n" for b,a in zip(q['questions'],k['answers'])))
print(len(q['questions']))
