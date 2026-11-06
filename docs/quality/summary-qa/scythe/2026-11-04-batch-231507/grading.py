from qa_tools import *
# These summaries are evaluator-authored check notes, not an automated semantic scorer.
notes={
'Q01':'Factory selection/count/unseen return, 11 encounters, random face-up tile and lowest-mat starter resolved.',
'Q02':'Map and mat pieces, action-token starting location and correct assignment of starting values resolved.',
'Q03':'Mandatory token move, optional actions/ordering, Rusviet exception, top gains below, exposed full costs/optional gains resolved.',
'Q04':'Enemy worker control, owner-only persistent structure ability/Mill exception and remote resource spending resolved.',
'Q05':'Distinct-unit movement, transported worker own movement and all resource/mech worker transport restrictions resolved.',
'Q06':'Enemy-worker-only stop, immediate home retreat/resources, popularity floor and independent worker-entry restriction resolved.',
'Q07':'Combat after all movement/before bottom, attacker ordering and independent worker enter/leave prohibition resolved.',
'Q08':'Both $1 top-action choices, worker-controlled trade placement/home prohibition and deck exhaustion branches resolved.',
'Q09':'Full exposed pre-payment, terrain production, left-to-right village workers, optional benefits and future-cost timing resolved.',
'Q10':'Oil/metal resource costs, bracketed cube restrictions, worker/control/lake deployment and ability scope, completed-action payment resolved; no universal numerical cost was requested.',
'Q11':'Worker/control structure placement, single-structure/terrain restrictions, permanence and enemy-control Mill/Mine exceptions resolved.',
'Q12':'Permanent open Faction placement, four one-time choices, uncovered-section ongoing trigger, active-left-right and two-player exception resolved.',
'Q13':'Capped dial/card spending, attacker-first abilities, simultaneous reveal/tie, both dial payments and used-card face-up discard resolved.',
'Q14':'Winner control/star limit, all-unit retreat/resources, attacker/defender popularity and dial-or-card loser reward resolved.',
'Q15':'After-Move/all-combat encounter eligibility, losing-character token persistence, benefit destination and isolated costs/bonuses resolved.',
'Q16':'Every character first-visit eligibility, after-Move choice, one permanent card, independent Factory bonuses and Speed/normal movement resolved.',
'Q17':'Own-turn complete-action timing, all requirements at reveal, deck-bottom discards and Saxony keep/score second resolved; specific card text was not requested.',
'Q18':'All star achievements, permanence, shared goals and immediate sixth-star termination resolved.',
'Q19':'Pre-star bottom benefits, pending-battle rollback and neighbor recruit priority/interruption resolved.',
'Q20':'Tier-2 rates, Factory as three, floor pairs and $53, retained coins/structure eligibility and exact tiebreak order resolved.',
'Q21':'Non-territory home base/default prohibitions, explicit exceptions and inactive expansion placeholders resolved.',
'Q22':'All terrain outputs/no-output spaces, nonresource workers, unlimited resources and territory quantities resolved.',
'Q23':'All-unit resource pickup/drop, mech own-worker/no-character carriage, Speed/tunnel step and overriding stops resolved.',
'Q24':'Any unit captures enemy structure-only territory, no structure combat, all-unit printed tunnels versus personal Mine resolved.',
'Q25':'Full payment required; legal dead turn shifts token and takes neither action resolved.',
'Q26':'Trade Armory power/Bolster Monument popularity, future triggering and owner persistence versus enemy control resolved.',
'Q27':'All five Riverwalk terrain pairs/character-mech scope and worker-only Nordic river/not-lake Swim resolved.',
'Q28':'Saxony controlled mountains+tunnels and Rusviet controlled villages+Factory, character/mech-only adjacency resolved.',
'Q29':'Saxony tunnel/Mine Disarm versus Nordic paid Artillery, timing/track reductions/once-per-combat resolved.',
'Q30':'Three-card result from two mechs plus worker presence, and character/mech combat requirement resolved.',
'Q31':'Wayfare own/inactive bases, any distance/origin and no active-opponent-base/worker exception resolved.',
'Q32':'Random precombat Scout steal/once limit, Coercion one card for one arbitrary resource regardless number resolved.',
'Q33':'Lake movement versus Nordic retreat/Polania lake jumps, cargo/worker restrictions and no lake builds/deploy resolved.',
'Q34':'Camaraderie only combat-winning aggressor/on-own-turn; no undefended-worker displacement exception resolved.',
'Q35':'One card/up to two different options, either order and first gain paying second resolved.',
'Q36':'Factory Move encounter stop and after-all-combats timing resolved.',
'Q37':'Coin information/optional total disclosure, combat count versus contents/commitment concealment and objective secrecy resolved.',
'Q38':'Only coin exchanges/tournament exception, unenforceable agreements and mandatory initiated combat resolved.',
'Q39':'All three scoring tiers/rates, lakes/home/Factory, pooled floor pairs/no workers resolved.',
'Q40':'Three adjacency tile features/unique counting/rivers/removed encounter/Mine exception and exact payout ranges resolved.',
'Q41':'Printed-tunnel versus Mine, longest continuous straight row/rivers, combined farm+tundra and each exact payout resolved.',
'Q42':'Winning lake attacker loses popularity for carried defeated workers, normal retreat and named faction exceptions resolved.',
'Q43':'Permanent star versus mutable current scoring tier, other factions sharing goal resolved.',
'Q44':'Random mat assignment, complete prescribed clockwise faction order and immediate-neighbor recruit consequence resolved.',
'Q45':'River as land border, lake as entire hex extending to adjacent shores, lake-ability entry and river-only insufficiency resolved.',
'Q46':'Encounter card/art public and capitalized thematic text read aloud resolved; reading every option aloud is not required.',
'Q47':'No per-territory limit on same-faction units or resource tokens resolved; separate structure limit remains.',
'Q48':'Next clockwise player may begin while noninteractive bottom-action decision is underway; priority/end restrictions retained.',
'Q49':'Each selected action once in the turn; paying again does not authorize repetition resolved.',
'Q50':'Normal Move coin alternative gives $1 instead of movement resolved.',
'Q51':'Workers never return to Player Mat/cover Produce costs; retreat destination remains home base resolved.',
'Q52':'Zero power, zero popularity or both do not bar combat initiation resolved.',
'Q53':'Ordinary two-combat-star cap limits further stars, not future combats or winning resolved.',
'Q54':'Non-Meander encounter requires one affordable option/full printed cost, but benefits may be partly or wholly declined resolved.',
'Q55':'Simultaneous secret dial selection and simultaneous dial/card reveal, distinct from attacker-first abilities resolved.',
'Q56':'Mandatory bottom-action announcement lets immediate neighbors check ongoing recruits resolved.',
'Q57':'Earned threshold star placement mandatory/immediate; completed objective reveal may wait while requirements hold resolved.',
'Q58':'All three unit types face default river/lake movement prohibition absent applicable ability resolved.',
'Q59':'Enlisted recruit remains permanently on chosen Faction Mat space; cannot relocate to reopen space resolved.',
'Q60':'Only character triggers encounter; mech/worker entry does not resolve/remove token resolved.',
'Q61':'Controlled Mill adds bonus production territory, produces as one worker without actual worker, and actual workers may also produce resolved.',
'Q62':'Control needs unit or own structure without enemy units; resources alone do not maintain control/spending after last unit leaves resolved.',
'Q63':'Build is paid in wood and Enlist in food; exact amount follows exposed Player Mat cost resolved.'

}
def grade(folder,overrides=None):
 """Write the evaluator's completed manual semantic assessment; this does not infer grades."""
 d=P/folder;q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];out={'benchmark_version':json.loads((d/'questions.json').read_text())['benchmark_version'],'grading_method':'Evaluator manually compared every requested material part of each answer with the fixed source-backed key and frozen summary; support labels did not determine grades. Key details not requested by question are not mandatory.','readers':{}}
 for r in ['a','b']:
  actual=json.loads((d/f'reader-{r}.json').read_text())['answers'];assert len(actual)==len(q);observed={a['id']:a for a in actual};assert len(observed)==len(q);assert set(observed)=={a['id'] for a in q}
  grades=[]
  for x,y in zip(q,k):
   assert x['id']==y['id'];z=observed[x['id']];g,reason=(overrides or {}).get((r,x['id']),('correct',notes[x['id']]))
   grades.append({'id':x['id'],'question':x['question'],'expected_answer':y['expected_answer'],'source_references':y['source_references'],'observed_answer':z['answer'],'reader_support':z['support'],'reader_evidence':z['evidence'],'grade':g,'reason':reason,'unsupported_guess':False})
  out['readers'][r]={'totals':{g:sum(a['grade']==g for a in grades) for g in ['correct','partial','incorrect']},'grades':grades}
 save(d/'results.json',out);print(folder,{r:v['totals'] for r,v in out['readers'].items()})
if __name__=='__main__':
 if sys.argv[1]=='seed-iteration-02':grade(sys.argv[1],{('a','Q02'):('partial','Missing action token beside Player Mat. Exact mat-specific quantities caveat is not a requested omission; independently adjudicated in seed02-adjudication.json.'),('a','Q12'):('incorrect','False mat-specific/unsupported caveat about explicit fixed ongoing recruit bonus mapping contradicts summary and rule. Independently adjudicated.'),('a','Q13'):('partial','Missing face-up discard of used cards in requested payment/resolution. Independently adjudicated.')})
 else:grade(sys.argv[1])
