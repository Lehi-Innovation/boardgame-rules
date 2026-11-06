from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/grading-reader-a/block-01')
p=json.loads((base/'packet.json').read_text())
quotes={
'Q001':[
'Simultaneously roll one die for each held office card.',
'Add one per fatigue on that card',
'Modified 1–2: nothing',
'3–4: add fatigue',
'5+: retire.',
'Chairman also adds one.',
'Move retiree to Pensioners',
'flip card into Vacant Offices',
'return its fatigue to supply.'
],
'Q002':[
'Players who completed at least one pensioner retirement **or an eligible firm special retirement during this London Season** must each take or discard one display card',
'If the display becomes empty, immediately skip every remaining eligible player.',
'in descending actual total retirement spending.',
'Ties: most total windows, including new prizes',
'then clockwise from PM.',
'discarding all remaining cards',
'refilling exactly three: prestige faceup, blackmail facedown, even if nobody took a card',
'prestige faceup, blackmail facedown',
'Return all remaining Pensioners to their supplies.'
],
'Q003':[
'Choose a main family action: take it once',
'Check where your opportunity marker was **at phase start** (it begins off the board).\n2. Choose a main family action: take it once, or **may take it twice if the marker already matched it**.',
'**Place/move the opportunity marker onto your chosen main action.**',
'only the latest passed extra-action law may grant its extra action.',
'This extra action is never doubled by the marker',
'never moves the marker.',
'With at least four vacant offices, place one additional writer **once this turn**',
'3 writers: the matching marker permits two main Enlist Writer actions, and four vacant offices add one writer once this turn.'
],
'Q004':[
'After all family actions, if Debt and applicants remain, move the rightmost applicant into Court',
'Repeat while both remain.',
'lower Debt by one.',
'With no Debt, slide remaining applicants as far right as possible',
'preserving order.',
'Place a member on an empty Stock Exchange space and pay bank'
],
'Q005':[
'Fill vacant offices in ascending number on their card backs.',
'insert its old card, vacant, into ascending hiring order.',
'Own-family hiring needs verbal consent from every other player in that office\'s candidate pool',
'a Chairman election never requires Nepotism consent.',
'transfer its fatigue to the new card',
'If no candidate exists, or the hirer is vacant, skip the office',
'it stays vacant',
'takes no actions, including hiring.'
],
'Q006':[
'Any shareholder may campaign',
'the number of shares needed for a pure majority** (more than half of current shares)',
'first candidate supported by players controlling that many shares wins.',
'give title marker.',
'Move one winner\'s Company shares into Chairman slot',
'If no candidate gets support, former Chairman picks any shareholder including self',
'no Nepotism consent.',
'It still counts as a share for dividends, majority and scoring',
'cannot be traded or invested in firms.'
],
'Q007':[
'First commit resources/cash',
'all cash for a Company-office check comes from that acting office\'s treasury and is paid to the bank',
'Gather dice, subtract penalties, then roll.',
'Use lowest die: 1–2 success',
'3–4 failure',
'retry if resources and office-specific limits allow',
'5–6 catastrophic failure',
'no more office actions',
'return officeholder to supply',
'discard fatigue',
'flip card into Vacant Offices.',
'You cannot take a dead action with no effect or chance of success'
],
'Q008':[
'May add up to three Debt freely',
'each +£5 Balance.',
'Each additional advance requires consent of players controlling majority Company shares',
'(Chairman counts)',
'never pass Debt track end.',
'**allocate all Balance** to other offices\' treasuries',
'lowering Balance by each transfer.'
],
'Q009':[
'Must spend treasury until **£2 or less remains**.',
'Lease extra ship £2',
'fit ship from shipyard £3',
'without owner consent',
'buy Company ship £5',
'Place each acquired ship in any sea zone',
'including China once office exists.',
'only if no ships remain on shipyards'
],
'Q010':[
'Declare regions for Trade: include home region',
'only regions reachable through open orders with available ship capacity.',
'subtract one per declared nonhome region.',
'Fill as many orders as possible within declared regions.',
'Successful Trade capacity is one order per ship in this Presidency\'s sea zone.',
'First writer goes to home port.',
'Every later order must extend the connected route filled during this same Presidency\'s Trade.',
'use all available writers, then continue filling with filled-order tokens for the remaining ships.',
'No President may fill another President\'s home region, even if its office vacant.',
'President earns bank £1 per order',
'writer owners earn £1 per writer placed.',
'one successful Trade per President per turn'
],
'Q011':[
'Target own Presidency\'s home',
'any associated region',
'any region bordering an associated region.',
'Cannot target another home region',
'another Presidency\'s Company-controlled region.',
'Company region must have unrest or a closed order to give action an effect.',
'Exhaust chosen officers/regiments to bottom for one die each',
'local alliances for printed dice.',
'Subtract the combined strength of target and **all other regions in its empire, counting target only once**.',
'Company-controlled defense strength is zero.',
'After **each attempt**, owners roll one die per officer exhausted in attempt',
'each 6 returns an officer to supply.',
'Regiments never roll officer losses.'
],
'Q012':[
'£4 per target tower',
'+ faceup loot modifier',
'with a minimum of (surviving officers used in this attempt + 1)',
'The Commander also receives one trophy per target tower.',
'Remove target tower and dome.',
'If target was an empire capital, remove **every matching empire flag throughout India**.',
'Open **all** target orders',
'remove **all** its unrest.',
'Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT\'S BOX**.',
'Put it **IN THE CONQUERED REGION ON THE MAP**.',
'Put **only the CARD** in **Vacant Offices**, awaiting later Hiring.',
'Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT\'S BOX**.',
'On catastrophe, Commander returns half own family\'s trophies rounded up',
'Commander member to supply.',
'Exhausted officers still check losses.'
],
'Q013':[
'Take the printed dice pool.',
'Each attempt rolls the current pool without penalty',
'then reduces the pool by one **regardless of result**.',
'then choose exactly one option below.',
'Thus the two stages require two successes in total.',
'Place it in **the Army associated with the Governor\'s President**.',
'Add an **unsplit £2** to Company Balance or the Governor\'s President\'s treasury.',
'Success | Take £1',
'or **£2 if the immediately preceding roll was unsuccessful**',
'Each Tax after the first this turn adds regional unrest.',
'Any unsuccessful roll | Add one unrest in the region.',
'until choosing to stop',
'no dice remaining',
'Catastrophe also removes the officeholder under the normal rule.',
'if no partial ship is in the Governor\'s region, **this single success places the partial ship there**.',
'If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor\'s President**.'
],
'Q014':[
'If insufficient, take £5 emergency loans.',
'take £5 emergency loans.',
'Each loan advances Debt one **only while a track space remains**.',
'At maximum Debt, keep taking loans without advancing Debt any further.',
'Newly added emergency Debt causes no extra current-turn expense.',
'After using emergency loans, set Balance to zero.',
'One or two loans lower Standing one',
'three or more lower Standing two.',
'2. **Expectations:** Compare remaining Balance to the expectations under **current** Standing; if lower, lower Standing one.',
'if lower, lower Standing one.',
'3. **Dividends:** Chairman may pay any affordable number.',
'If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.',
'Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.'
],
'Q015':[
'primary Crisis first',
'also triggers secondary Rebellions in every other Company region with unrest.',
'Bombay → Madras → Bengal',
'Within each Presidency, that Commander chooses the order of its associated regions.',
'Attack strengths are distinct:',
'Sovereign attacker\'s whole empire strength + event modifier',
'Compare only rebelling region strength + modifier',
'only the number of unrest cubes in that secondary region',
'Associated Commander occupied | That Commander chooses and exhausts pieces',
'The acting player exhausts active Army pieces to reach at least the Crisis strength, or as many as possible if unable to reach it.',
'Military Affairs itself acts in the Commander\'s stead',
'Commander AND Military Affairs vacant | **Chairman chooses pieces**',
'**EQUAL TO OR GREATER THAN** Crisis strength | **The attack FAILS; defense SUCCEEDS.**',
'Remove all unrest in the attacked region.',
'actual Commander gains one trophy',
'Military Affairs/Chairman substitutes gain OR lose NO trophies',
'If this defeated a normal primary Invasion, also remove one attacker tower if possible.'
],
'Q016':[
'-1 or less fails',
'discard law',
'resolve dilemma\'s If Failed text',
'Zero or higher passes',
'place law with passed laws',
'PM takes passed-law token',
'Opposition Leader returns token',
'takes PM dial',
'new PM moves proposed policy one space either direction and resolves that adjacent policy.',
'resolve selected policy **then** immediate law effects.',
'Finally restore every card used for voting to its regular orientation'
],
'Q017':[
'In 1758/Long 1710',
'at turn start before London Season',
'PM **may** call special Deregulation vote if Standing and/or Debt on lined space',
'**must** if either on starred space.',
'Lower Debt one per two current Debt',
'set Standing to S',
'PM takes passed-law token',
'activate firms.',
'Increase Company-share scoring value by flipping/placing Court VP token, **up to a MAXIMUM of ±3 VP per share**.',
'No policy accompanies this vote',
'Deregulation law is NOT discarded.',
'PM stays in power',
'PM may vote against it.'
],
'Q018':[
'only if you currently manage none',
'return one eligible Company share to supply or flip workshop to invested side.',
'Flip your family board to its firm-charter side',
'place a family member as first firm share',
'set value cube to leftmost track space',
'take £5 from bank into the London treasury.',
'With manager\'s consent',
'same Company-share/workshop contribution',
'creates one firm share and £5 bank to London.',
'creates one firm share and £5 bank to London. Up to ten firm shares',
'Cannot use Company shares at all when Standing and/or Debt on lined space.',
'Cannot use shares created this turn, even after trading them away.',
'Cannot use Chairman share.',
'Invested workshops never return to uninvested: no bonus or Company-failure VP',
'Invested workshops never return to uninvested: no bonus or Company-failure VP',
'Up to ten firm shares',
'further investments still contribute £5 but create no shares.'
],
'Q019':[
'After the Firm Investments step ends, managers choose firm strategies.',
'Only a firm with at least one ship may select a trade strategy',
'it may select a closed home port.',
'Reveal cash bids simultaneously',
'keep strategy cards facedown until their matching Presidency begins.',
'At beginning of associated Presidency\'s operations, before any actions, matching firms reveal strategy',
'Each firm gets exactly one trade attempt per turn.',
'paying bid to bank.',
'After that success, fill orders lowest initiative first.',
'Firm initiative = ship count minus number of successful dice (1s/2s)',
'President\'s successful Trade creates initiative the same way using Presidency ships.',
'fill orders lowest initiative first.',
'The President chooses the order among tied traders',
'If President is vacant or never successfully trades, firms fill **after Commander/Governors had chance to act**',
'Chairman choosing initiative ties.',
'**Fill only OPEN orders**, as many as possible up to **ships + 1**, starting strategy home port, always tracing through its own filled route back there.',
'starting strategy home port',
'Each firm may fill any particular order only ONCE per turn',
'A firm may refill an order filled by a DIFFERENT firm or the Company this turn; Company may refill firms\' orders. A previously filled order pays **half listed revenue, rounded down**',
'revenue goes to India treasury.',
'Advance firm Value one space per full £6 added to India treasury this turn.'
],
'Q020':[
'Pay £1 per charter ship',
'plus higher of share count or firm value',
'can use either/both treasuries.',
'from India treasury only',
'Each dividend pays £1 per firm share',
'plus £1 manager.',
'If unable to pay, dissolve unless rescued.',
'Dissolution: shares to Debtor\'s Prison',
'(each -1 VP)',
'ships return to their matching shipyards',
'charter back to family side',
'workshops remain invested.'
]
}
# Each grade and atom status below is an independent content judgment; the code only serializes it.
reasons={
'Q001':'Correct thresholds, modifiers, separate office rolls and all retirement destinations are present.',
'Q002':'All eligibility, ordering, tiebreaking, display exhaustion/refill and pensioner-return facts are explicitly present.',
'Q003':'The complete marker and latest-law rules are given, and the stated fixture correctly yields three writers.',
'Q004':'Rightmost-first Debt-linked issuance, applicant movement with preserved order and initial bank payment are all present.',
'Q005':'The entry resolves vacancy ordering, consent exception, promoted fatigue and both vacancy fallbacks.',
'Q006':'Election eligibility, majority, first support, title/share movement, deadlock authority and nontradability are all resolved.',
'Q007':'The entry gives payment source/destination, dice and all result branches, catastrophe destinations and dead-action prohibition. Discarded fatigue clearly returns to supply.',
'Q008':'All requested borrowing counts, cash, consent, track limit and full allocation/debit duties are present.',
'Q009':'Mandatory spending, all three costs, fitting consent, destinations including China and Company-ship prerequisite are explicit.',
'Q010':'Declared regions, penalty, capacity and own connected route, token fallback, home protection, bonuses and success cap are all present.',
'Q011':'The full Deploy passage gives every target rule, dice/empire penalty and officer-loss procedure, with catastrophe losses also explicit.',
'Q012':'Loot/trophy calculation, control destinations and Presidency association, and catastrophe trophy/member/officer outcomes are covered. The token above the associated President establishes that association.',
'Q013':'The shrinking pool, benefits, two ship stages, personal bonuses, unrest and all stopping conditions are covered. The normal catastrophe rule supplies the vacancy consequence.',
'Q014':'The full emergency-loan and subsequent Revenue sequence is present. Its explicit immediate-scoring clause conditions later expectations/dividends on survival.',
'Q015':'The complete Events passage covers primary and secondary attacks, their distinct strength formulas, order, compulsory defense and substitute actors, accepted total-strength comparison and all successful-defense results.',
'Q016':'All pass/fail thresholds, law and token consequences, PM and policy movement, effect order and card cleanup are explicit.',
'Q017':'Scenario, timing, lined/starred triggers, both result branches and special-vote exceptions are complete.',
'Q018':'Formation, investment consent/resources, bank-to-London funding, every Company-share/workshop restriction and cap behavior are explicit.',
'Q019':'The full strategy and trading passage resolves selection, reveal/check/filling timing, initiative and tie rules, capacity, refills, revenue destination and Value growth.',
'Q020':'The expense formula and treasury permissions, dividend funding/amounts and all dissolution destinations/consequences are present.'
}
grades=[]
for entry in p['entries']:
    qid=entry['id']
    atoms=entry['requested_fact_scope_entry']['material_requested_facts']
    chosen=quotes[qid]
    assert len(atoms)==len(chosen),(qid,len(atoms),len(chosen))
    actual=entry['reader_a_entry']['answer']
    for quote in chosen:
        assert quote in actual,(qid,quote)
    parts=[{'requirement':atom,'status':'covered','reader_quotes':[quote]} for atom,quote in zip(atoms,chosen)]
    # Several atoms require a compound passage; add exact same-entry context to show all components.
    additions={
      ('Q011',6):['Move purchased alliances to the **top/active** half.'],
      ('Q011',10):['Exhausted officers still check losses.'],
      ('Q012',11):['Steps 3a–3c form a new Governorship only if the target was not already Company-controlled.'],
      ('Q013',13):['Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.'],
      ('Q013',14):['Partial ship has no other effect.'],
      ('Q014',0):['At maximum Debt, keep taking loans without advancing Debt any further.'],
      ('Q014',8):['Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.'],
      ('Q014',10):['Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.'],
      ('Q015',5):['normal Invasion/Rebellion attack strength **plus unrest in its target region**.'],
      ('Q015',6):['normal Invasion/Rebellion attack strength **plus unrest in its target region**.'],
      ('Q015',8):['The acting player exhausts active Army pieces to reach at least the Crisis strength, or as many as possible if unable to reach it.'],
      ('Q015',12):['The following strength comparison applies the **user-supplied interpretation** recorded under Special Rules & Edge Cases:'],
      ('Q019',0):['Managers select their strategy simultaneously and secretly:','Trade zone/home port | Commit a secret cash bid from London treasury.'],
      ('Q019',6):['roll one die per committed £1'],
      ('Q019',8):["President's successful Trade creates initiative the same way using Presidency ships.",'If President is vacant or never successfully trades, firms fill **after Commander/Governors had chance to act**, Chairman choosing initiative ties.']
    }
    for (aqid,idx),more in additions.items():
        if aqid==qid:
            for quote in more: assert quote in actual,(qid,quote)
            parts[idx]['reader_quotes'].extend(more)
    grades.append({'id':qid,'grade':'Correct','reason':reasons[qid],'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==20
out=base/'grades-same-entry.json'
data=json.dumps({'block_id':'block-01','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n'
out.write_text(data)
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(data.encode()).hexdigest()}))