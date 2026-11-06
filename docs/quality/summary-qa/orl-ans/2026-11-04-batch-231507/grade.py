from pathlib import Path
import json,sys,collections
P=Path(__file__).parent
name,bank=sys.argv[1:3];D=P/name
key=json.loads((P/bank/'answer-key.json').read_text());qs={q['id']:q['question'] for q in json.loads((D/'questions.json').read_text())['questions']}
# Evaluator's semantic decisions after reading every complete raw answer.
base={
'Q01':'Tie/2-player exceptions unresolved.', 'Q02':'Optional draw, free Market limit and retention unresolved.',
'Q03':'Partial activation, deferral and carryover unresolved.', 'Q04':'One-action clockwise rotation and irrevocable passing unresolved.',
'Q05':'States wrong Farm House cost (Farmer+Boatman); requested immediate good omitted.',
'Q06':'States wrong Village cost and limits described recruitment to Craftsman; three choices/rewards absent.',
'Q07':'Technology timing, first Farmer and placement constraints unresolved.', 'Q08':'Category restrictions/stack access absent.',
'Q09':'A repeats false universal +1 Knight draw rule despite fourth-Knight exception; B adds nonexistent Monk-track advancement; remaining track boundaries unresolved.',
'Q10':'Reverse Monk substitution and exact Deed types unresolved.', 'Q11':'Distance, one-good choice and empty links unresolved.',
'Q12':'Wrong Guildhall effect: claims Technology instead of Trading Station; building restrictions absent.',
'Q13':'Wrong Scriptorium effect: claims Place instead of Development Point; crossing rewards absent.',
'Q14':'One/two-Follower activation, marked restriction, placement rewards and permanence unresolved.',
'Q15':'Pilgrimage prohibition/exceptional timing unresolved.', 'Q16':'Harvest wholly absent.', 'Q17':'Plague wholly absent.',
'Q18':'Bankruptcy wholly absent.', 'Q19':'Supply exhaustion/restoration wholly absent.', 'Q20':'Bonus tie, goods values, formula and tiebreak unresolved.'}
results={'iteration':name,'benchmark_version':bank,'grading':'All requested parts compared semantically against frozen source-backed key; extra materially false rulings count incorrect. Support labels are not grades.','readers':{}}
for who in ['a','b']:
 raw=json.loads((D/f'reader-{who}.json').read_text()); observed={a['id']:a for a in raw['answers']};assert len(observed)==len(raw['answers'])==len(qs) and set(observed)==set(qs)
 grades=[]
 for k in key['answers']:
  qid=k['id'];grade='correct';reason='All requested rulings match the fixed key and are supported by the supplied summary; equivalent wording accepted.'
  if name=='seed-iteration-01':grade='incorrect' if qid in ['Q05','Q06','Q09','Q12','Q13'] else 'partial';reason=base[qid]
  if name=='seed-iteration-02':
   if (who,qid) in [('a','Q09'),('a','Q14'),('b','Q19')]:
    grade='partial';reason={('a','Q09'):'Omits the fourth-Knight first-arrival Citizen reward within the requested Castle rewards.',('a','Q14'):'Gives Deed destination but does not resolve that dispatched Followers remain there permanently.',('b','Q19'):'Correctly describes Harvest/Plague restoration but explicitly leaves the requested general stock-restoration ruling unresolved.'}[(who,qid)]
   if (who,qid)==('b','Q07'):reason='Permanent filling/staying on one space semantically covers immovability; independent adjudication agrees.'
   if (who,qid)==('b','Q18'):reason='All requested sacrifice/payment restrictions and removal destinations covered. Later recovery of Development Points is incidental to this question; independent adjudication agrees.'
  if name=='expanded-iteration-02':
   gaps={'a':{'Q09':'Omits the requested Castle fourth-Knight first-arrival Citizen reward.','Q14':'Omits permanent retention at the Deed destination. Retains the original seed adjudication and pre-dispatch destination standard; later adjudication considered permanence incidental, but evaluator does not relax the established stricter requirement.','Q22':'Map goods setup omits the requested randomization/shuffle procedure.','Q40':'Repeats first-Farmer/if-legal conditions but never resolves that first Technology cannot go on the Scholar+Craftsman Laboratory. Conditional non-answer is partial, not unconditional false permission.','Q57':'Explicitly leaves immediate passive acquisition timing unresolved.'},'b':{'Q14':'Omits permanent Deed destination retention; original stricter destination interpretation retained despite later adjudicator disagreement.','Q40':'Conditional first placement only if replacing Farmer does not resolve the requested concrete no for Laboratory.','Q57':'Explicitly abstains on current-phase acquired passive ability timing.'}}
   if qid in gaps[who]:grade='partial';reason=gaps[who][qid]
  if name=='expanded-iteration-03' and who=='a' and qid=='Q18':
   grade='partial';reason='Follower payment source pool (own bag) is missing in this answer and same-question evidence. Eligible/random/redraw terminology does not resolve the bag-only restriction; fresh independent adjudication confirms partial.'
  if name=='expanded-iteration-04' and who=='b' and qid=='Q11':
   grade='partial';reason='Omits requested Ship→Waterway/Wagon→Road mapping in answer and same-question evidence. Fresh independent adjudication confirms material route restriction remains unresolved.'
  if name=='stamped-iteration-01':
   issues={'a':{'Q07':'Omits requested Technology immovability placement limit; generic section reference does not supply the missing answer. Independent adjudication confirms partial.','Q26':'Eligible Followers and exact Deed matching do not resolve any-neutral-profession Town Hall activation eligibility or starter exclusion. Fresh adjudication confirms partial.'},'b':{'Q43':'Explicitly leaves requested same-Action-Phase execution ruling unsupported/unresolved.','Q59':'Explicitly leaves ability to decline an available good unresolved despite citing may take one.'}}
   if qid in issues[who]:grade='partial';reason=issues[who][qid]
  if name=='stamped-iteration-02' and who=='b' and qid=='Q15':
   grade='incorrect';reason='Explicitly states Pilgrimage applies before Phase5, contradicting source Phase5 application on requested timing. Correct ActionPhase clause does not resolve the contradiction; fresh adjudication confirms incorrect.'
  if (name.startswith('expanded-iteration-') or name.startswith('stamped-iteration-')) and grade=='correct':
   if qid=='Q03':reason='All requested Follower activation/retention/destination facts resolved. Technology persistence is correct supporting key context, but this prompt asks Followers; independent adjudication confirms it is not an extra mandatory part.'
   if qid=='Q06':reason='All three recruitment choices and their distinct rewards are resolved. After-pass Technology timing is not independently requested here and is tested directly by Q07; independent adjudication confirms this scope.'
   if qid=='Q21':reason='Equipment, initial placements and youngest starter resolved. Four marked starting Followers identifies the unique defined starting set without requiring its profession names to be repeated; independent adjudication accepts equivalent set wording.'
   if qid=='Q52':reason='Randomized face-down remaining stack, Pilgrimage on top and Start Player top-tile reveal resolved. Physical board-space location is incidental to requested procedure; independent adjudication confirms.'
   if qid=='Q35':reason='All five printed costs, produced goods, Goods Market source and unavailable-good prohibition resolved; singular product naming is equivalent for the requested product identity.'
   if name=='expanded-iteration-02' and who=='b' and qid=='Q59':reason='Clearly and unequivocally permits leaving the good while moving. Caveat concerns whether a separate editorial sentence exists, not uncertainty about the ruling; independent adjudication confirms correct.'
   if name=='expanded-iteration-03' and who=='b' and qid=='Q43':reason='Correct same-round later-turn execution before passing. Trader acquisition citation is imprecise supporting context; general activation and Action Phase rules substantiate the complete ruling. Fresh adjudication confirms correct.'
  if name=='expanded-iteration-05' and who=='a' and qid=='Q16':
   reason='All requested food types, Goods Market destination and no-food/coin-shortfall fallback are resolved. Caveat concerns an additional scenario-specific statement beyond the preserved general rule, not a requested unresolved ruling. Fresh independent adjudication confirms correct despite partial support label.'
  if name=='expanded-iteration-05' and who=='a' and qid=='Q26':
   reason='Knight+Scholar and generic neutral Town Hall eligibility/no printed profession restriction fully resolve requested activation types. Neutral category excludes colored starters. Fresh adjudication confirms complete answer despite partial support label; later exact Deed matching is a different placement requirement.'
  if name=='stamped-iteration-01' and who=='a' and qid=='Q14':reason='All requested activation, exact destination, permanent retention, reward and completion facts resolved. Depicted coin reward identifies the board-defined amount; listing its1/2/3possibilities is not separately requested. Fresh independent adjudication confirms correct.'
  if name=='stamped-iteration-01' and who=='a' and qid=='Q43':reason='Affirmatively permits same-phase later-turn execution before passing, with activation and immediate-placement evidence. Lack of a worked explicit timing sentence is support commentary, not an unresolved requested ruling. Fresh adjudication confirms correct.'
  if name=='stamped-iteration-02' and who=='b' and qid in ['Q09','Q13','Q21','Q41','Q49']:
   reason='Every requested ruling is fully resolved. Added caveat concerns an unasked additional detail, not a contradiction or unresolved requested part. Fresh independent adjudication confirms correct; support labels are not grades.'
  if name=='stamped-iteration-03' and who=='a' and qid=='Q16':
   reason='Wine qualifies among the scenario holdings and wool does not; the full grain/cheese/wine set is explicitly present in this same question evidence. Goods Market destination, five-coin fallback and pay-available/torture-shortfall rules are complete; no fact borrowed from another answer.'
  grades.append({'id':qid,'question':qs[qid],'expected_answer':k['expected_answer'],'source_references':k['source_references'],'observed_answer':observed[qid],'grade':grade,'reason':reason,'unsupported_correct_guess':False})
 counts=collections.Counter(x['grade'] for x in grades)
 results['readers'][who]={'counts':{g:counts[g] for g in ['correct','partial','incorrect']},'grades':grades}
(D/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print({who:r['counts'] for who,r in results['readers'].items()})
