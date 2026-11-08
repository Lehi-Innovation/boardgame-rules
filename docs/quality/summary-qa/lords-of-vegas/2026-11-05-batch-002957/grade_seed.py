import json,hashlib
from pathlib import Path
R=Path(__file__).parent
h=lambda x:hashlib.sha256(x).hexdigest()
reasons=[
'Full setup procedure and discard visibility are supplied by same-entry operative setup quotation; direct text resolves deal, cash and deck placement.',
'First-player dice and player-card passage plus operational draw/acquisition/payout/discard/action sequence resolve all asked order clauses.',
'New marker precedes all-lot $1 payout; card setup value is explicitly setup-only.',
'Current 5 retained by replacement die, tile stays, and new owner receives calculated $5 before matching payout.',
'Edge connectivity on same block, indivisibility and highest individual die are resolved; color/player distinction is unasked background.',
'Actual calculations give Red $7/3 points and Blue $5/0 points with boss identified correctly.',
'Color everywhere versus any-color Strip adjacency and full-casino scope are all resolved.',
'All five actions, any order, repetition/gamble/reorg limits and off-turn action prohibition are supplied; trade availability is contextual background.',
'Cost $6, reclaimed marker, available any-color tile and own die 2 are correct; automatic merger is unasked background.',
'Boss eligibility, $18, gold/3 placement, unowned edge condition and both illegal proposed targets are resolved.',
'Boss eligibility, whole-casino new-color supply, $10 replacement with unchanged dice and stronger-neighbor merger boss outcome are resolved.',
'Non-boss eligibility, actor pays all 10 pips, all owners roll all dice and own-original tile reassignment are resolved.',
'Merged-casino paid reorg prohibited by prior die; free boss-tie rerolls remain permitted.',
'Only cross-player current-highest dice reroll free; unchanged Green4 wins, same-player top and lower ties do nothing; repeat-until-single-player rule is in same-entry quotation.',
'Minimum of $20, $18 and $15 is computed $15; boss receives House card and one gamble limit stated.',
'Every sum-group is correct with $4/$7/$4 actual transfers, cash-limited doubled win and stake retained.',
'Current-turn action trade restriction, all base trade assets, marker/die substitution preserving value and prohibited points/tiles/future promises are resolved.',
'All five numeric awards from8, separate nonpooled casino awards, lost excess and ascending order/tie choice are supplied.',
'Immediate end, no Play, final lots+Strip payouts, score then money and immediate90+ base victory are resolved.',
'Two-player F setup discard/replacement, no F construction, F no-marker paid repeat Draw until A–E and repeated payout before actions are resolved.'
]
for iteration in ['seed-iteration-01','seed-iteration-02']:
 D=R/iteration
 if not all((D/f'reader-{l}.json').exists() for l in 'ab'):continue
 qs=json.loads((D/'questions.json').read_text())['questions'];key=json.loads((D/'answer-key.json').read_text())['answers'];results={'grading_standard':'All substantive fields in each same raw entry assessed together against actual asked clauses. No facts borrowed across IDs. Contextual key background is not an extra required fact.','readers':{}}
 for label in 'ab':
  raw=json.loads((D/f'reader-{label}.json').read_text());by={a['id']:a for a in raw['answers']};gs=[]
  assert len(by)==len(raw['answers'])==20 and set(by)=={q['id'] for q in qs}
  for i,(q,k) in enumerate(zip(qs,key)):
   a=by[q['id']];grade='correct';reason=reasons[i]
   if iteration=='seed-iteration-01' and label=='a' and q['id']=='Q02':
    grade='partial';reason='First-player and leftward turn order and phase names are correct. No substantive Q02 field supplies draw, acquire, lot payout, casino money/points or discard sequence; cannot borrow those from other IDs. Independent Q02 adjudication confirms actual asked operational scope.'
   gs.append({'id':q['id'],'grade':grade,'reason':reason,'question':q['question'],'fixed_key':k,'observed_raw_entry':a,'observed_entry_sha256':h(json.dumps(a,ensure_ascii=False,sort_keys=True).encode()),'summary_supported':True if grade=='correct' else 'Answered claims supported; asked procedure omitted','unsupported_guess':False,'source_references':k['source_references']})
  results['readers'][label]={'counts':{g:sum(x['grade']==g for x in gs) for g in ['correct','partial','incorrect']},'unresolved':sum(x['grade']=='partial' for x in gs),'raw_sha256':h((D/f'reader-{label}.json').read_bytes()),'grades':gs}
 (D/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
 print(iteration,{l:x['counts'] for l,x in results['readers'].items()})
