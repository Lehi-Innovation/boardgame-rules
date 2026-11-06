from qa_tools import *
d=P/'seed-iteration-01';q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers']
reasons=[
'Missing players+1 random Factory selection/unseen removal, 11 marked encounters, random face-up structure tile, lowest-mat starter.',
'Incorrectly attributes popularity to Faction Mat; it is supplied by Player Mat. Mat setup and two land-adjoined worker specificity also incomplete.',
'Missing full exposed red-cost payment, optional green benefit, using top gains below and explicit bottom-first prohibition.',
'No ruling for enemy unit control, persistent owner structure abilities/Mill exception or remote resource spending.',
'No decisive different-units ruling, resource carriage by all units or carried-worker subsequent movement.',
'Missing stop, no further turn movement, zero-popularity retreat and independent worker-entry prohibition.',
'Missing multiple-combat order, before-bottom timing and independent worker enter/leave restriction.',
'Missing all-workers-home restriction and exhaustion reshuffle/no-draw branches.',
'Missing exposed costs paid before production, full affordability, optional benefits and left-to-right permanent worker placement/future-cost timing.',
'Missing bracketed/empty box limits, controlled territory/lake restriction and paying completed bottom action.',
'Missing permanence, legal territories and enemy-controlled Mill/Mine rulings.',
'Missing open Faction destination/permanence, uncovered-action link and active-left-right/two-player timing.',
'Dial range incorrectly stated up to current power without cap seven. Missing combat ability priority and payment/discard procedure.',
'Missing attacker versus defender popularity distinction, resource abandonment and explicit card-only retreat-reward branch.',
'Missing lose/no-encounter branch, benefit destination, affordable printed cost and isolation from mat benefits.',
'Missing each character first visit/card permanence and Factory action/movement differences; first-visitor wording insufficient.',
'Missing own-turn timing, full requirements at reveal, deck-bottom discard and Saxony second-objective exception.',
'Missing irreversible stars and shared non-blocking achievements.',
'Missing pre-star primary/coin/recruit collection, unresolved-battle undo and recruit-star priority.',
'Incorrect Factory value: three territories, not one; result must be $53 rather than $47. Structure eligibility/tiebreakers absent.'
]
result={'benchmark_version':'seed-v1','grading_method':'Manual semantic comparison of every requested part, independently per answer. Reader support labels do not decide grade.','readers':{}}
for r in ['a','b']:
 answers=json.loads((d/f'reader-{r}.json').read_text())['answers'];grades=[]
 for i,(x,y,z) in enumerate(zip(q,k,answers)):
  assert x['id']==y['id']==z['id'];g='incorrect' if x['id'] in ['Q02','Q13','Q20'] else 'partial'
  grades.append({'id':x['id'],'question':x['question'],'expected_answer':y['expected_answer'],'source_references':y['source_references'],'observed_answer':z['answer'],'reader_support':z['support'],'reader_evidence':z['evidence'],'grade':g,'reason':reasons[i],'unsupported_guess':False})
 result['readers'][r]={'totals':{'correct':0,'partial':17,'incorrect':3},'grades':grades}
save(d/'results.json',result)
