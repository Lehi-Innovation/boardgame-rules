from pathlib import Path
import json, hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-02/grading-reader-b/block-02')
p=json.loads((base/'packet.json').read_text())
quotes={
'Q021':[
'Cash, trophy/passed-law tokens, dice and regiments may use proxies.',
'Cash, trophy/passed-law tokens, dice and regiments may use proxies.',
'Cash, trophy/passed-law tokens, dice and regiments may use proxies.',
'Cash, trophy/passed-law tokens, dice and regiments may use proxies.',
'Company Balance, VP and Vote tracks are unlimited.',
'Company Balance, VP and Vote tracks are unlimited.',
'Company Balance, VP and Vote tracks are unlimited.',
'Components are limited: when a supply runs out, complete as much as possible.',
'when a supply runs out, complete as much as possible.',
'All information, including discards and family cash, is public except facedown blackmail and temporarily concealed firm strategies/bids during selection.',
'All information, including discards and family cash, is public except facedown blackmail and temporarily concealed firm strategies/bids during selection.',
'All information, including discards and family cash, is public except facedown blackmail and temporarily concealed firm strategies/bids during selection.'
],
'Q022':[
'Enterprises; **facedown** blackmail; family treasury cash; Company/firm shares; promise cards',
'Enterprises; **facedown** blackmail; family treasury cash; Company/firm shares; promise cards',
'Enterprises; **facedown** blackmail; family treasury cash; Company/firm shares; promise cards',
'Enterprises; **facedown** blackmail; family treasury cash; Company/firm shares; promise cards',
'Enterprises; **facedown** blackmail; family treasury cash; Company/firm shares; promise cards',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
'Officeholders, writers, officers, prizes, spouses, trophies, passed laws, played blackmail, PM dial or Chairman piece',
"**To transfer a share:** return the old owner's family member and **replace it at the share's location with a member from the RECEIVING FAMILY**.",
"**To transfer a share:** return the old owner's family member and **replace it at the share's location with a member from the RECEIVING FAMILY**.",
'after use, keep the card faceup in your player area; it cannot be used again or traded.',
'It must stay facedown when traded.'
],
'Q023':[
'| Immediate transfer | Binding. |',
"Promise of future behavior | Nonbinding, except a printed promise card's guaranteed effect can be called **if possible**.",
"a printed promise card's guaranteed effect can be called **if possible**.",
"Follow that card's timing/limits.",
'**No promise calls during Final Scoring.**',
'| Simultaneous calls cannot all be fulfilled | Guarantor chooses which to fulfill. |',
'Transferred resources cannot activate twice: a workshop paid this Bonuses phase does not pay again after a sale during that phase.'
],
'Q024':[
"Use that scenario's player setup cards; add three extra cards for five players or six for six players.",
"Use that scenario's player setup cards; add three extra cards for five players or six for six players.",
'Shuffle and deal evenly.',
'**Place every listed holding:**',
"put each office's family member in its office and give its matching office card to that owner",
'put Company-share members in Court of Directors',
'put writers, officers and trainees in their indicated Presidency/Army/Training boxes',
"put a Commander in that Army's Commander slot **without an office card**",
'each shipyard and put its matching ship',
'in the **listed sea zone**, or **on its shipyard if unfitted**.',
'Each starting luxury gives 2 VP.',
'Shuffle **prestige and blackmail together into ONE deck**',
'deal three for the London Season display',
'prestige faceup and blackmail facedown.',
'prestige faceup and blackmail facedown.'
],
'Q025':[
"The game ends after scenario's final turn or when Standing reaches failure.",
"The game ends after scenario's final turn or when Standing reaches failure.",
'Normally failure is immediate; failure during Events finishes that phase, and legislation failure finishes vote before scoring.',
'failure during Events finishes that phase',
'legislation failure finishes vote before scoring.',
'**During all of Final Scoring, no negotiations or promise calls are allowed.**',
'**During all of Final Scoring, no negotiations or promise calls are allowed.**'
],
'Q026':[
'Count **enterprises and Company shares**, using their current Power-track rates (bottom two positions zero)',
'Count **enterprises and Company shares**, using their current Power-track rates (bottom two positions zero)',
'Count **enterprises and Company shares**, using their current Power-track rates (bottom two positions zero)',
'bottom two positions zero',
'+1 per passed-law token and trophy',
'+1 per passed-law token and trophy',
'+2 for PM',
'plus printed card power (blackmail faceup or down, applicable spouse).',
'Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**.',
'Tied first: only lower award to each tied player; no other award.',
'Tied first: only lower award to each tied player; no other award.',
'Tied second receive none.',
'Ties: most windows, then clockwise from PM.',
'Ties: most windows, then clockwise from PM.'
],
'Q027':[
"If Company survived, add Court's current VP per Company share.",
'If failed, subtract that value per share and add 1 VP per uninvested workshop.',
'If failed, subtract that value per share and add 1 VP per uninvested workshop.',
'| Survived | Roll office attrition, then retire Pensioners; **no prestige/display cards**. |',
'| Survived | Roll office attrition, then retire Pensioners; **no prestige/display cards**. |',
'| Failed | Instead draw **ONE RANDOM Company failure card** and resolve its printed consequence. |'
],
'Q028':[
'Spouses usually add VP, impose permanent restrictions and cannot be transferred.',
'Spouses usually add VP, impose permanent restrictions and cannot be transferred.',
'Make required enterprise/share trades immediately upon taking the spouse.',
'Retirement discounts can stack, are personal, and each is usable once per London Season and once during Final Scoring. Discounts reduce actual spending and therefore display priority.',
'Retirement discounts can stack, are personal',
'Retirement discounts can stack, are personal',
'each is usable once per London Season and once during Final Scoring.',
'each is usable once per London Season and once during Final Scoring.'
],
'Q029':[
'whether a shipyard is returned because of Violet Effingham or an unpaid tax, its fitted ship stays in play.',
'That shipyard cannot be purchased while its matching ship remains in play; purchase becomes possible after the ship returns.'
],
'Q030':[
"| Enlist Writer | Place a member in any Presidency's Writers box. With at least four vacant offices, place one additional writer **once this turn**, so a doubled Writer action can place three total. |",
"Place a member in any Presidency's Writers box.",
'| Enlist Officer | Place a member in Officers-in-Training. |',
'Place a member in Officers-in-Training.',
'Pay bank £4; gain luxury',
'2 VP while owned',
'and its window icon; social enterprise.',
'Pay bank £2; take shipyard',
'place its matching ship **unfitted on that shipyard**',
'Shipping enterprise, one vote and £1 bonus while fitted.',
'Pay bank £5; take workshop',
'manufacturing enterprise, two votes, £1 bonus; worth 1 VP if Company fails unless invested.',
'Place a member on an empty Stock Exchange space and pay bank: the five queue spaces are £2, £3, £3, £4, £5 (two distinct £3 spaces).',
'Place a member on an empty Stock Exchange space and pay bank: the five queue spaces are £2, £3, £3, £4, £5 (two distinct £3 spaces). It is an applicant, not yet a share.',
'the five queue spaces are £2, £3, £3, £4, £5 (two distinct £3 spaces).',
'Shipping enterprise, one vote and £1 bonus while fitted.',
'Shipping enterprise, one vote and £1 bonus while fitted.',
'manufacturing enterprise, two votes, £1 bonus; worth 1 VP if Company fails unless invested.',
'manufacturing enterprise, two votes, £1 bonus; worth 1 VP if Company fails unless invested.',
'worth 1 VP if Company fails unless invested.'
],
'Q031':[
"If placing a family piece with none in supply, take one from any of your prizes and lose that prize's printed VP.",
"If placing a family piece with none in supply, take one from any of your prizes and lose that prize's printed VP.",
'If no family action is possible, take none and return opportunity marker to supply.',
'If no family action is possible, take none and return opportunity marker to supply.'
],
'Q032':[None,None,None,None,None],
'Q033':[
'| Director of Trade | Chairman chooses current officeholder other than Chairman/Governor; if all offices vacant, any writer. Commanders are not officeholders. |',
'Chairman chooses current officeholder other than Chairman/Governor',
'if all offices vacant, any writer.',
'| Manager of Shipping | Chairman chooses any writer. |',
'| Superintendent of Trade in China | Chairman chooses any writer; office hired immediately upon creation. |',
'Chairman chooses a Presidential Commander; if none, any officer; if none, any Officer-in-Training.',
'Chairman chooses a Presidential Commander; if none, any officer; if none, any Officer-in-Training.',
'Chairman chooses a Presidential Commander; if none, any officer; if none, any Officer-in-Training.',
'| President | Director of Trade chooses **a writer OF THIS PRESIDENCY or a Governor ASSOCIATED WITH THIS PRESIDENCY**. |',
'| Governor | Associated President chooses writer or officer in the region; Commander is not an officer and is ineligible. Place member on Governor overlay. |',
'Commander is not an officer and is ineligible.'
],
'Q034':[
'Success either opens one closed order in a **non-Company** region',
'or opens China: place Superintendent overlay/card and Chairman hires writer immediately.',
'or opens China: place Superintendent overlay/card and Chairman hires writer immediately.',
'May make repeated Special Envoy checks',
'After all envoys, may make up to two transfers, each moving one writer or ship between any Presidencies/sea zones (including China once created). Cannot transfer while still taking envoys.'
],
'Q035':[
'May make up to two transfers, each officer or regiment from one Army to another, remaining in top half. Then assign **every** Officer-in-Training to any Army\'s top half. Finally appoint Commanders',
"Then assign **every** Officer-in-Training to any Army's top half.",
'Finally appoint Commanders',
"if vacancy or someone has more total family pieces in Army than current Commander's family, choose among families with most pieces.",
"if vacancy or someone has more total family pieces in Army than current Commander's family, choose among families with most pieces.",
'choose among families with most pieces.',
'Move chosen officer to Commander slot',
'return previous Commander to top as officer.',
"A tie with current Commander's family does not replace them.",
'Nepotism does not apply.'
],
'Q036':[
'Each President chooses order of its Commander, Governors and its own Trade.',
'Must allow each position an opportunity but Commander/Governors may decline.',
'Must allow each position an opportunity but Commander/Governors may decline.',
'Must allow each position an opportunity but Commander/Governors may decline.',
'Each position finishes all actions before next begins.',
'Trade can go before/after Commander or any Governor but cannot interrupt another position.',
'If President vacant, Chairman sets order only: cannot trade or approve local alliance purchases.',
'If President vacant, Chairman sets order only: cannot trade or approve local alliance purchases.',
'If President vacant, Chairman sets order only: cannot trade or approve local alliance purchases.'
],
'Q037':[
'Trade itself never exhausts ships.',
"| Writers on orders | Return to their **associated Presidency's Writers box**; use dividers to preserve affiliation. |",
'| Filled tokens and Presidency dividers | Return to supply. |'
],
'Q038':[
"**At the START of Commander operations, before Deploy attempts**, first request President's treasury funds for any printed-price local alliances in Army; President must approve purchase.",
'President must approve purchase.',
"first request President's treasury funds for any printed-price local alliances in Army; President must approve purchase.",
'Move purchased alliances to the **top/active** half.',
'**When used for Deploy or defense, exhaust the whole alliance to the bottom half.**',
'**Refresh exhausts any unused active alliances too; it does not reactivate alliances as it does officers/regiments.**',
'Move purchased alliances to the **top/active** half. **When used for Deploy or defense, exhaust the whole alliance to the bottom half.** Its strength is usable once that turn and cannot be split among more than one purpose.',
'**When used for Deploy or defense, exhaust the whole alliance to the bottom half.**',
'**When used for Deploy or defense, exhaust the whole alliance to the bottom half.** Its strength is usable once that turn and cannot be split among more than one purpose.',
'Its strength is usable once that turn and cannot be split among more than one purpose.',
'Its strength is usable once that turn and cannot be split among more than one purpose.'
],
'Q039':[
'Company-controlled defense strength is zero.',
'**minimum loot of surviving participating officers + 1 for the Commander**',
'no tower remains, so gain **zero tower trophies**.'
],
'Q040':[
'Thus the two stages require two successes in total.',
"if no partial ship is in the Governor's region, **this single success places the partial ship there**.",
"If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor's President**.",
"Place it in **the Army associated with the Governor's President**.",
'Officer-like strength, loot paid to bank, no officer-loss rolls.',
'Officer-like strength, loot paid to bank, no officer-loss rolls.',
'Officer-like strength, loot paid to bank, no officer-loss rolls.'
]
}
reasons={
'Q021':'Every requested supply, track, exhaustion and information rule is present in the complete Components attachment; proxy permission covers the unlimited supplies.',
'Q025':'The complete scoring attachment gives both end triggers, immediate and phase-completion branches, and the explicit universal negotiation/promise prohibition. Standing reaching failure identifies the failure endpoint.',
'Q026':'The complete scoring attachment covers every requested source and tie branch. Its unrestricted enterprise category includes prestige enterprises; no enterprise subtype is excluded.',
'Q028':'The complete London Season attachment covers transfer restrictions, immediate trades, personal stacking discounts and both use limits. Retirement discounts reducing actual spending conveys their cost reduction; the applicable printed discount supplies its amount.',
'Q030':'The complete family-action menu gives all costs, placements, votes, income and failure scoring. Enlistment entries specify only placement, conveying no cash cost, while paid actions state their prices.',
'Q032':"Partial: all five requested empty-Court fallback facts are omitted; the entry attaches Company Operation instead of Hiring. Reader selection error, not a missing/unclear summary. Controlling summary: III. Hiring, line 138: \"If Court is empty, former Chairman automatically returns, placing a member from supply or, if necessary and possible, a prize (lose prize VP). If impossible, there is no Chairman.\" This resolves automatic return, supply use, mandatory prize fallback/VP loss, and no Chairman when neither exists. No material contradictory fallback is stated."
}
grades=[]
for e in p['entries']:
    id=e['id']; req=e['requested_fact_scope_entry']['material_requested_facts']; qs=quotes[id]
    assert len(req)==len(qs),(id,len(req),len(qs))
    answer=e['reader_b_entry']['answer']
    for q in qs:
        if q is not None: assert q in answer,(id,q)
    grades.append({'id':id,'grade':'Partial' if id=='Q032' else 'Correct','reason':reasons.get(id,'Every exact requested fact is correctly resolved in the complete same-entry applicable summary attachment, with no material contradiction or unsupported guess.'),'material_parts':[{'requirement':r,'status':'omitted' if q is None else 'covered','reader_quotes':[] if q is None else [q]} for r,q in zip(req,qs)],'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==20
result={'block_id':'block-02','readers':{'reader-b':{'grades':grades}}}
out=base/'grades-same-entry.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))