from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
q=json.loads((P/'v2-expanded/questions.json').read_text());k=json.loads((P/'v2-expanded/answer-key.json').read_text());rev=json.loads((P/'coverage-review-01.json').read_text())
corrections=[]
for a in k['answers']:
 if a['id']=='Q21':
  old=a.copy();a['expected_answer']='Round Start reveals next Conflict atop prior and each human draws5. Non-ending Recall returns current Mentat to Landsraad, Agents to Leaders, passes first player clockwise. Sort Through the Chaos winner takes Mentat at start next round per FAQ, not before Recall.';a['source_references']=['Main PDF pp8,13,16; official FAQ p4 Sort Through the Chaos supersedes old p16 timing'];corrections.append({'id':'Q21','old':old,'new':a.copy(),'reason':'Independent coverage F01: official FAQ correction to original printed reward timing.'})
 if a['id']=='Q35':
  old=a.copy();a['expected_answer']='May play on own Agent or Reveal turn. If awaiting applicable Reveal, keep face up until then; use and discard during that Reveal, including current Reveal if played there.';corrections.append({'id':'Q35','old':old,'new':a.copy(),'reason':'Independent coverage F05: current Reveal is included; no delay to another round.'})
for i,addition in enumerate(rev['proposed_additions'],60):
 id=f'Q{i:02}';q['questions'].append({'id':id,'question':addition['question']});k['answers'].append({'id':id,'expected_answer':addition['expected_answer'],'source_references':[rev['source_references'][s] for s in addition['source_references']]})
q['benchmark_version']=k['benchmark_version']='v3-expanded-corrected';D=P/'v3-expanded-corrected';D.mkdir();(D/'questions.json').write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n');(D/'answer-key.json').write_text(json.dumps(k,indent=2,ensure_ascii=False)+'\n');(D/'key-corrections.json').write_text(json.dumps(corrections,indent=2,ensure_ascii=False)+'\n')
ledger=json.loads((P/'coverage-ledger.json').read_text());(P/'coverage-ledger-before-review.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
ledger['passes'] += [{'pass':4,'focus':'Independent challenge accepted five proposed omitted procedures and corrected two non-seed key entries','accepted_ids':[f'Q{i:02}' for i in range(60,65)]},{'pass':5,'focus':'Recheck main procedural passages against explicit question wording, including setup, draws, icons, finite supply, Recall and FAQ corrections','accepted_ids':[]},{'pass':6,'focus':'Recheck all relevant base FAQ entries and timing/priority/outcome exceptions against expanded64, rejecting changed numbers and out-of-scope interactions','accepted_ids':[]}]
for i,a in enumerate(rev['proposed_additions'],60):ledger['accepted'].append({'id':f'Q{i:02}','novelty':a['novelty'],'source_references':a['source_references'],'origin':'Independent reviewer CR01'})
ledger['coverage_map'] += [{'source':'Previously undercovered setup/shuffle/initial first-player procedures pp4–5','ids':['Q64']},{'source':'Normal exhausted-deck draw/reshuffle and in-play boundary pp6,11,16','ids':['Q63']},{'source':'FAQ p2 Foldspace and Dispatch an Envoy','ids':['Q60','Q61']},{'source':'FAQ p4 any-source recruits and ban on re-recruiting garrison','ids':['Q62']}]
ledger['rejected'] += [{'candidate':'Staged Incident named-card example','reason':'Strength marker adjustment already tested Q09,Q10; no new branch.'},{'candidate':'Repeated Cult/Influence scenario with different track values','reason':'Threshold outcomes already covered Q14,Q15,Q53.'}]
ledger['status']='Awaiting fresh challenge after passes5–6 with zero additions';(P/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
(P/'question-bank.md').write_text('# Dune: Imperium — v3 expanded corrected bank (64 questions)\n\nOriginal base 2020, standard 2–4 player; solo, optional variants and expansions excluded. Seed Q01–Q20 are unchanged. Q21/Q35 corrected explicitly before expanded reader testing.\n\n'+''.join(f"## {a['id']}\n\n{b['question']}\n\n**Expected:** {a['expected_answer']}\n\n**Source:** {json.dumps(a['source_references'],ensure_ascii=False)}\n\n" for b,a in zip(q['questions'],k['answers'])))
# Correct summary globally, preserving frozen seed2 snapshot.
R=Path('/home/jonny/projects/boardgame-rules/rules/dune-imperium.md');s=R.read_text();s=s.replace(' (Exception: a player who took the Mentat as a Conflict reward keeps it as an Agent for the next round instead of returning it.)',' At the start of the next round, the winner of Sort Through the Chaos takes the Mentat as its Conflict reward (official FAQ timing).')
s=s.replace('If you gain the Mentat as a Conflict reward, keep it as an Agent for the next round instead of returning it at the end of this one.','For the Sort Through the Chaos Conflict reward, take the Mentat at the start of the next round and use it that round (official FAQ timing).')
s=s.replace('- **Double Cross / Gun Thopter / Guild Envoy:**','- **Dispatch an Envoy:** it adds only missing Faction Agent icons. Existing icons remain, including non-Faction icons; it never creates a duplicate icon.\n- **Double Cross / Gun Thopter / Guild Envoy:**')
R.write_text(s)
# Frozen benchmark fingerprints (independent of reader iterations).
for d in ['v1-seed','v2-expanded','v3-expanded-corrected']:
 path=P/d;(path/'input-manifest.json').write_text(json.dumps({'sha256':{name:hashlib.sha256((path/name).read_bytes()).hexdigest() for name in ['questions.json','answer-key.json']},'frozen':True},indent=2)+'\n')
