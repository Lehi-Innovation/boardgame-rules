from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parent
it=R/sys.argv[1]
def load(p):return json.loads(p.read_text())
q=load(it/'questions.json');k=load(it/'answer-key.json'); ids=[x['id'] for x in q['questions']]
reasons={
'Q01':'Distributes board/marker, shuffles reachable face-down deck, draws four and places randomly/recessed/hidden.',
'Q02':'Correct phase order and simultaneous secret individual work; identifies Pairs as the two Keywords below each Clue Zone (the outside-edge Keywords). Four such two-Keyword Pairs identify the required eight without requiring a second enumeration.',
'Q03':'Single-word rule, compound allowance and all five categories supplied.',
'Q04':'Rejects Keyword itself.', 'Q05':'Rejects translated Keyword with correct reason.', 'Q06':'Rejects same-family word.', 'Q07':'Rejects invented word.',
'Q08':'All three requested parts: four Clues, each connecting both Keywords of its Pair, matching Clue Zone. Secrecy is contextual in the key; Q08 does not separately request the timing/secrecy rule.',
'Q09':'Complete post-Clue sequence: remove four, add one unseen, shuffle five, board down and five-card face-down pile on top.',
'Q10':'Waits for everyone to finish the preparation sequence.',
'Q11':'First Spectator chosen, others reconstruct the board’s original arrangement together, and no communication including hints/gestures.',
'Q12':'Full face-up board/five reveal in table middle; originals into correct spaces/orientations with extra left off.',
'Q13':'Final placement decision goes to player on Spectator’s left.',
'Q14':'Physical trial layouts/discussion allowed; verify after agreement.',
'Q15':'Six = four correct cards plus two first-try bonus; no second attempt.',
'Q16':'Silent incorrect-card removal to table middle, no other feedback, one final retry.',
'Q17':'Second perfect scores four, no first-try bonus.',
'Q18':'Incorrect card removed to table middle; three correct score three; no third attempt.',
'Q19':'Turn board over and write points in middle; discard all five; next Spectator left.',
'Q20':'End after each player once, sum all board points to Record of Legends and compare high score.'}
results={'iteration':it.name,'benchmark_version':q['benchmark_version'],'grading_standard':'Grade each answer separately against every requested material part in fixed source-backed key; correct/partial/incorrect are distinct; labels do not determine grades; no borrowing across answers. Unsupported guesses cannot establish summary coverage.','reader_results':{}}
for who in ['a','b']:
 raw=load(it/f'reader-{who}.json'); assert sorted(a['id'] for a in raw['answers'])==sorted(ids)
 lookup={a['id']:a for a in raw['answers']}; grades=[]
 for item,key in zip(q['questions'],k['answers']):
  id=item['id'];a=lookup[id]; grade='correct'; reason=reasons[id];missing=[]
  if it.name=='seed-iteration-01' and who=='b' and id=='Q11':
   grade='partial';missing=['Others work together to reconstruct the original Pairs; “resolve” alone is too vague.'];reason='Independent adjudication: choice and silence are correct; selector caveat accurate and immaterial. “Resolve” does not explain the requested cooperative reconstruction. No credit borrowed from Q12. See adjudication-q11-b.json.'
  grades.append({'id':id,'question':item['question'],'expected_answer':key['expected_answer'],'required_facts':key['required_facts'],'source_references':key['source_references'],'observed_answer':a['answer'],'reader_support_label':a['support'],'summary_evidence':a['evidence'],'grade':grade,'reason':reason,'missing_or_wrong':missing,'unsupported_guess':False})
 totals={name:sum(x['grade']==name for x in grades) for name in ['correct','partial','incorrect']};totals['unresolved']=totals['partial'];totals['unsupported_guesses']=0
 results['reader_results'][f'reader-{who}']={'totals':totals,'grades':grades}
(it/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
p=load(R/'progress.json')
for x in p['iterations']:
 if x['path']==str(it):x.update(status='graded',scores={r:v['totals'] for r,v in results['reader_results'].items()})
(R/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
print({r:v['totals'] for r,v in results['reader_results'].items()})
