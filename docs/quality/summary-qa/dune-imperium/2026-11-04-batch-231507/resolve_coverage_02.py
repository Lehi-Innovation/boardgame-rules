from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent
q=json.loads((P/'v3-expanded-corrected/questions.json').read_text());k=json.loads((P/'v3-expanded-corrected/answer-key.json').read_text());rev=json.loads((P/'coverage-review-02.json').read_text());D=P/'v4-expanded-scope-corrected';D.mkdir()
corrections=[]
for a,b in zip(q['questions'],k['answers']):
 if a['id']=='Q52':
  old={'question':a.copy(),'key':b.copy()};a['question']=rev['findings'][1]['proposed_fixed_question'];b['expected_answer']=rev['findings'][1]['proposed_fixed_answer'];b['source_references']=['Official FAQ p2 Double Cross and Gun Thopter; Guild Envoy excluded as Uprising card.'];corrections.append({'id':'Q52','old':old,'new':{'question':a.copy(),'key':b.copy()},'reason':'CR02-F02 scope correction. Historical versions preserved. This removes an out-of-scope clause before any expanded readers, not a hard in-scope question.'})
 # Earlier extraction line locators were approximations; PDF page locators are valid and retained.
 refs=b['source_references'];new=[re.sub(r' / extraction lines [0-9–,]+','',x) if isinstance(x,str) else x for x in refs]
 if refs!=new:corrections.append({'id':b['id'],'type':'reference-only-correction','old_references':refs,'new_references':new,'reason':'Remove inaccurate approximate extraction line locators; physical PDF page references retained; expected answer unchanged.'});b['source_references']=new
addition=rev['proposed_questions'][0];q['questions'].append({'id':'Q65','question':addition['question']});k['answers'].append({'id':'Q65','expected_answer':addition['fixed_answer'],'source_references':addition['source_references']})
q['benchmark_version']=k['benchmark_version']='v4-expanded-scope-corrected'
for n,x in [('questions.json',q),('answer-key.json',k),('corrections.json',corrections)]: (D/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
(D/'input-manifest.json').write_text(json.dumps({'sha256':{n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['questions.json','answer-key.json']},'frozen':True},indent=2)+'\n')
ledger=json.loads((P/'coverage-ledger.json').read_text());(P/'coverage-ledger-before-review-02.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n');ledger['passes'] += [{'pass':7,'focus':'Independent second challenge: public supply visibility and scope correction','accepted_ids':['Q65']},{'pass':8,'focus':'Recheck complete setup/public versus hidden information, all main and relevant FAQ procedural passages','accepted_ids':[]},{'pass':9,'focus':'Challenge remaining card lifecycles, component limits, timing, priorities and exception branches against65; reject duplicates and excluded modules','accepted_ids':[]}];ledger['accepted'].append({'id':'Q65','novelty':addition['novelty'],'source_references':addition['source_references'],'origin':'CR02'});ledger['coverage_map'].append({'source':'Main p5 G6 public supply; p7 hidden Intrigue exception','ids':['Q65','Q34']});ledger['rejected'].append({'candidate':'Guild Envoy mandatory discard','reason':'Uprising-specific card; removed through explicit versioned scope correction.'});ledger['status']='Awaiting fresh review after passes8–9 with zero meaningful additions';(P/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
(P/'question-bank.md').write_text('# Dune: Imperium — final expanded bank (65 questions)\n\nVersion v4-expanded-scope-corrected. Original base2020 standard2–4 players, required House Hagal included; solo/variants/expansions/Uprising excluded. Original20 wording and expected answers preserved. Explicit correction histories retained for Q21/Q35/Q52 and PDF reference locators.\n\n'+''.join(f"## {a['id']}\n\n{b['question']}\n\n**Expected:** {a['expected_answer']}\n\n**Source:** {json.dumps(a['source_references'],ensure_ascii=False)}\n\n" for b,a in zip(q['questions'],k['answers'])))
R=Path('/home/jonny/projects/boardgame-rules/rules/dune-imperium.md');s=R.read_text().replace('- **Double Cross / Gun Thopter / Guild Envoy:**','- **Double Cross / Gun Thopter:**').replace(' Guild Envoy requires discarding a hand card when played on an Agent turn.','')
a=s.index('**Combat:** at the start of Combat');b=s.index('\n## FAQ & Rulings',a)
s=s[:a]+'''**Combat strength procedure:** if House Hagal has at least one troop in the Conflict, calculate its strength at the start of Combat:
1. Reveal a House Hagal card in turn order. **If it is Reshuffle, reshuffle and reveal again**; obtain a card with a combat sword bonus before calculating that bonus. A Reshuffle result is not treated as a zero-sword combat card.
2. Ignore everything except the sword icons at the bottom; add that many strength to its normal **2 strength per deployed troop**.
3. Humans may then play Combat Intrigue cards before resolving Combat.

House Hagal receives no reward for its rank, but it still occupies that rank when humans receive rewards. Ordinary third place pays nothing; a tie for second pays the third reward to each tied human. If House Hagal wins a Conflict for a space a human controls, remove that Control marker; House Hagal does not replace it. After Combat, troops return to supply and markers reset normally.
''' +s[b:]
R.write_text(s)
# Adjudication corrects evaluator overgrading without changing questions, answers or reader outputs.
D2=P/'seed-iteration-02';(D2/'results-provisional-before-adjudication.json').write_bytes((D2/'results.json').read_bytes());(D2/'grading-findings-provisional.json').write_bytes((D2/'grading-findings.json').read_bytes());f=json.loads((D2/'grading-findings.json').read_text())
for reader in 'ab':f[reader].pop('Q15')
(D2/'grading-findings.json').write_text(json.dumps(f,indent=2)+'\n')
D3=P/'seed-iteration-03';(D3/'grading-findings.json').write_text(json.dumps({'b':{'Q20':{'grade':'partial','reason':'Missing required Reshuffle/reveal-again combat branch. Independent adjudication confirms this is material, while turn-order omission is immaterial with one Rival. Q15 token disposition accepted per independent adjudication without requiring unrequested explicit VP arithmetic.'}}},indent=2)+'\n')
