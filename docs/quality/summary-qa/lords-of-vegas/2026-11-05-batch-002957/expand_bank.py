import json
from pathlib import Path
from build_bank import R,rows,save_bank
extra=[
('All nine gold tiles are on the board. Can you build another gold tile using the spare tenth tile, sprawl a gold casino, or remodel a three-tile casino to gold? May you build a different available color?', ['The tenth is a replacement, not a tenth usable tile.','Cannot build gold, sprawl gold or remodel to gold without sufficient available tiles.','A different available color may be built on own lot at normal cost.'], 'Original p1 Casino Tiles; p3 Available Tiles/Build/Sprawl/Remodel'),
('All twelve of your dice are on the board when you build, sprawl or inherit a sprawled tile. How do you place the required die, what happens to the vacated tile and its scoring, and what if it was the casino’s only die?', ['Remove one of your existing ownership dice and place it on the new tile at the value required by the placement.','Vacated tile remains ownerless but counts for casino points.','If no dice remain in a casino it has no owner/boss.','Trading may free a die.'], 'Original p3 Available Dice; unified p6 Available Dice'),
('A property draw claims a sprawled casino tile with no die; the board prints 2, while the die removed from it used to be 5. What die do you place, does the tile change, and when does its matching casino pay?', ['Place own die at printed board value 2; former removed value 5 is not retained.','Tile remains; takeover precedes matching casino payout, which includes your $2 for that die.'], 'Original p2 Take Over Your Lot/Money Paid; unified p7'),
('You draw the card for your own sprawled tile, whose die is now 6 although the board prints 2. Does ownership or value change, and what does that die earn if its casino pays?', ['Leave your existing die unchanged at 6.','Matching payout pays you $6 for that die.'], 'Unified p7 Step 2; original p2 Money Paid'),
('All ten of your markers are on lots and you acquire another empty lot. How is ownership marked, what happens to the vacated lot, and which of the two lots receives the coming owned-lot payout?', ['Move one existing marker to newly gained lot.','You no longer own vacated lot; it does not pay you lot income.','New marked lot pays you $1 in upcoming payout.'], 'Unified p6 Available Player Markers; original p2 Draw/Owned Lots Pay'),
('May a player conceal money or piece counts, forbid inspection of a discard pile, or deny a bank payout because the physical bank is empty?', ['Money, piece counts and discarded cards are public; anyone may inspect discards.','Bank money unlimited; physical bank exhaustion does not cancel a payout.'], 'Original p1 Money; unified p6 Your Resources/Available Money'),
('A casino has two Red 6s and a Blue 3. During a trade one Red 6 is replaced by Green’s die. What value does Green’s die have, must anything reroll before further trades or actions, and who rolls?', ['Green replacement remains 6.','Different players now tie for highest: immediately reroll both highest 6s (the remaining Red and new Green), not Blue 3, for free.','Each owner rolls own tied dice; finish resolving current-highest cross-player ties before actions or initiating trades.'], 'Original p4 Trading/Reroll if Tied; unified p9 Settling Who’s the Boss'),
('You draw a card and replace one of Red’s tied highest 5s in a casino with your own 5; another Red 5 remains. Is the boss tie postponed until after payment or Play, and does this reroll count as a paid reorganization?', ['Resolve cross-player highest tie immediately on takeover before casino payouts, not postponed to Play.','Reroll only current highest dice free; this is not paid reorganization and does not use its limit.'], 'Unified p7 Step 2/p9 Settling Who’s the Boss; p11 Reorganize'),
('May you reorganize a casino where you alone own all dice, or one where you own none? Does reorganizing only one of your dice avoid paying for the opponents’ pips?', ['Sole owner may reorganize; no-own-die casino may not.','Reorganization always rerolls every die and costs all pips, including opponents, not just selected own dice.'], 'Original p3 Reorganize; unified p11'),
('All twelve of your ownership dice are on casino tiles. Must you remove a tile’s die just to gamble, and may you gamble at your own casino if no opponent bosses any casino?', ['Any dice may be used to gamble; no ownership placement or removal required for the gambling roll.','Cannot gamble at own casino; if no opponent bosses a casino there is no legal gambling action.'], 'Unified p6 Available Dice; p13 Gamble'),
('On your turn you trade for an opponent’s die so that you can reorganize their casino, then promise to pay them for a sprawl only if the reorganization gives you control. If the reroll does not make you boss so the agreed sprawl cannot happen, do the subsequent steps of the trade proceed? Could the opponent instead perform the sprawl on your turn?', ['When an element of trade is prevented, subsequent steps do not occur.','Cannot sprawl without boss control.','Opponent cannot take action on your turn.'], 'Unified p15 Trading; original p3 Sprawl/p4 Trading')]
q,k=save_bank('expanded-v1',rows+extra)
# A mapping of actual asked clauses, kept separate from immutable baseline answers.
context={'Q05':[2],'Q08':[],'Q09':[2],'Q10':[],'Q11':[],'Q14':[],'Q15':[1],'Q20':[],'Q22':[3]}
# Q15 fact1 contains both asked House-card recipient and background eligibility; retain asked content explicitly.
entries=[]
for rec in k['answers']:
 facts=rec['required_facts']; bg=[]; required=[]
 for i,f in enumerate(facts):
  (bg if i in context.get(rec['id'],[]) else required).append(f)
 if rec['id']=='Q15':
  required.append('Give the casino boss the House card.'); bg=['Casino must be bossed by another player.']
 entries.append({'id':rec['id'],'asked_question':next(x['question'] for x in q['questions'] if x['id']==rec['id']),'required_answer_facts':required,'contextual_key_background':bg,'source_references':rec['source_references']})
(R/'expanded-v1'/'scope-map.json').write_text(json.dumps({'version':'scope-v1','principle':'Actual asked clauses only; contextual background is not an extra grading requirement.','entries':entries},indent=2,ensure_ascii=False)+'\n')
# Parent coverage passes. Each maps actual asked facts, not key-only background.
coverage=[
('Original p1 Casino Tiles, Dice, Markers, Money and Property Cards',['Q05','Q21','Q22','Q25','Q26']),
('Original p2 Setting Up',['Q01','Q03','Q20']),('Original p2 Who Owns What',['Q05']),('Original p2 Taking Turns',['Q02']),
('Original p2 Draw/Take Over Your Lot',['Q02','Q03','Q04','Q23','Q24','Q28']),('Original p2 Owned Lots Pay',['Q03','Q06','Q25']),
('Original p2 Pay Based on Color/Pay The Strip',['Q06','Q07']),('Original p2 Money Paid/Points Earned',['Q04','Q06','Q07','Q23','Q24']),
('Original p2 Scoring and p3 continuation',['Q18']),('Original p3 Ending Step 1/Step 2 Play',['Q02','Q08']),
('Original p3 Available Tiles/Dice',['Q21','Q22']),('Original p3 Build',['Q09','Q21']),('Original p3 Sprawl',['Q10','Q21','Q31']),
('Original p3 Remodel',['Q11','Q21']),('Original p3 Reorganize plus p4 continuation',['Q12','Q13','Q29']),
('Original p4 After Each Action Reroll if Tied',['Q14','Q27','Q28']),('Original p4 Gamble',['Q15','Q16','Q30']),
('Original p4 Trading',['Q17','Q27','Q31']),('Original p4 Winning',['Q19']),('Original p4 Two-player rules',['Q20']),
('Unified p6 resource clarifications (base only)',['Q22','Q25','Q26','Q30']),('Unified p7 own-die takeover',['Q24']),
('Unified p9 tie at takeover; no interruptions',['Q27','Q28']),('Unified p11 reorg limit and sole-owner clarification',['Q13','Q29']),
('Unified p13 base gamble stakes and any dice',['Q16','Q30']),('Unified p15 interrupted trade',['Q31']),
('Unified p16 two-player setup and final no actions/trades',['Q19','Q20'])]
ledger={'scope':q['scope'],'passes':[
 {'pass':1,'focus':'Resource exhaustion, takeover branches, tie timing, reorganization eligibility, gambling supply exception, interrupted trades','accepted':[{'id':f'Q{i:02}','novelty':why} for i,why in enumerate(['No tiles/extra replacement branch','Dice exhaustion and ownerless casino','Empty-die inheritance uses board value','Own-die takeover unchanged','Marker exhaustion and loss of old lot','Public resources and unlimited bank','Trade creates tie immediately','Draw takeover tie precedes payout','Sole-owner/no-own-die reorganization eligibility','Any-dice gambling exception and absent eligible host','Failed conditional trade halts later steps'],21)]},
 {'pass':2,'focus':'Full baseline re-read: setup, every action cost/eligibility/supply, payout and end branches','accepted':[]},
 {'pass':3,'focus':'Independent targeted parent re-pass: scoring boundaries, boss cascades, two-player sequence, destinations and trading timing','accepted':[]}],
 'coverage_map':[{'passage':x,'questions':ids} for x,ids in coverage],
 'rejected_candidates':[
 {'candidate':'A second bet example with a different casino size or cash balance','reason':'Same min-of-three cap and doubled insolvency branches already Q15–16.'},
 {'candidate':'More awards from score 8 with different numbers','reason':'Q18 already asks gap loss, separate awards and order; cosmetic numeric substitution.'},
 {'candidate':'Another highest tie cascade where unchanged lower die wins','reason':'Q14 explicitly asks this outcome and repeated current-highest procedure.'},
 {'candidate':'Sprawl onto own marker instead of opponent marker','reason':'Same empty-unowned target rule tested by Q10, no different timing/exception.'},
 {'candidate':'Raise or acquire action; Underworld scoring','reason':'Excluded expansion mechanics.'},
 {'candidate':'Laying off an odd bet','reason':'Explicitly excluded optional Gamble Variant.'},
 {'candidate':'2024 setup F-card set-aside/reshuffle','reason':'Excluded edition; applicable previous-Mayfair p16 instead says discard and replace.'},
 {'candidate':'Build and immediately reorganize a new low die','reason':'Mechanical combination of Q8–9 and Q12 eligibility/cost, no distinct exception beyond existing action order.'}
 ],'stopping_rule':'Two consecutive complete targeted passes with no additions, pending fresh independent challenge.'}
(R/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
print('Expanded questions:',len(q['questions']))
