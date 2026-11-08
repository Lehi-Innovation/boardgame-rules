from pathlib import Path
import json
R=Path(__file__).parent
prompts={
'Amoeba':'what ship presence is required to Ooze, when relative to card selection/reveal does it happen, from/to where and how many ships may move, and can a shipless winner receive a colony?',
'Anti-Matter':'which card pairing triggers Negation, which side wins, how are own, opposing main-player and both sides\' allied ships counted, and which ordinary tie rule remains?',
'Barbarian':'which result triggers Loot and Pillage, when relative to compensation, who sees/chooses how many cards, and what happens to the remaining hand?',
'Calculator':'when is equalizing announced, which revealed card pairing permits it, what changes and what stays fixed, and what values result from attacks15 and8?',
'Chosen':'how often and when may Divine Intervention be used, how many cards are drawn, what happens with no encounters, what replacements/addition are allowed, and where do replaced/unused cards go?',
'Citadel':'when, where and from what may citadels be placed; which portion requires power use; when/how many activate; what bonus applies; and what happens to activated/unactivated citadels after defense wins or loses?',
'Clone':'when relative to outcome, compensation and discard may Replicate act, and which card does it return to where?',
'Cudgel':'what result and revealed card trigger Smash, how many extra ships must which player lose, who chooses them, and are normal losses replaced?',
'Dictator':'on whose turns and when is Command used, what selection information and choice does it give, and how is destiny handled on Dictator\'s turn or when zapped?',
'Fido':'when may Fetch act, which card is offered to whom, what happens on refusal versus acceptance, and what benefit may Fido receive?',
'Filch':'when may Theft act, whose encounter card is taken from where and added to whose hand?',
'Fodder':'what pairing and timing permit Overwhelm, which hand attack values qualify relative to both revealed attacks, how many can be discarded, and how do they affect the total?',
'Gambler':'when does Bluff act relative to the opponent\'s reveal, what is announced, what happens if unchallenged, and on challenge who loses how many ships from which locations and how is the encounter then resolved? State the printed incompatible alien.',
'Grudge':'when are tokens assigned, to whom, what happens for each of Grudge\'s win/deal and loss/failed-deal branches, who chooses penalty ships and which ships are ineligible?',
'Hacker':'when collecting compensation, from whose hand may Hack take cards and who looks/chooses them; when Hacker owes compensation, who selects what the opponent receives?',
'Hate':'when does Rage act, what must Hate discard, what alternatives does each other player have, what attack threshold does the original sheet print, who selects lost ships, and what happens if Hate then lacks encounters?',
'Healer':'what event and whose losses permit Heal, how many of that event\'s ships return and where, what card benefit is earned, can several players be healed, and does healing remove compensation?',
'Human':'when does Humanity act, what bonus does it add to which side, and what happens if this use is zapped?',
'Kamikaze':'when may Sacrifice act, how many ships from where may be sacrificed, what cards result, and what happens to those ships if the use is zapped?',
'Loser':'when is Upset declared, what card-selection restriction follows, how does it change the outcome and when does that reversal happen relative to other effects including zapped Human?',
'Machine':'after what outcomes may Continuity grant another encounter, how many encounters may its turn contain and what hand requirement remains?',
'Macron':'under the retained official erratum, when are Mass\'s launch/ally limitation and ship-strength uses made, what ship limit applies to offense/allies, how much is each ship worth for total versus compensation/rewards, and does the defense itself have the one-ship launch limit?',
'Masochist':'when exactly is Hurt Yourself checked, what lost-ship locations count, what is the alternate win condition, is it lost for too few home colonies, and can Masochist still win normally?',
'Mind':'when and whose hand may Knowledge inspect, how does being a main player restrict that target, and what may Mind reveal to other players?',
'Mirror':'when is Reversal declared, which revealed cards are changed, how are digits treated, and what values result from15,20 and08?',
'Miser':'what extra hands and choice are given at setup, how may Hoard substitute for the ordinary hand, can gains be put there or opponents inspect/draw from it, and when/how can the hoard be replaced?',
'Mite':'when and at what defense hand-size threshold does Bluster act, what two alternatives does defense have, how are cards discarded, and what are ship destinations and encounter status under each choice?',
'Mutant':'when and at what hand size may Regenerate act, from which sources and in what sequence/randomness are cards taken, and when does drawing stop?',
'Observer':'in what roles may Protect act, whose ships are protected in each role, during what phase and from which loss destination are they returned to where?',
'Oracle':'when does Foresee act, whose card is played in what manner first, and when does Oracle then select and play its own?',
'Pacifist':'which revealed pairing triggers Peace and who wins, and what happens when both reveal negotiate?',
'Parasite':'when may Infest act, what invitation and side choices does it change, how many ships are sent, and can it override an effect that specifically prevents alliance?',
'Philanthropist':'when may Giving act, how many cards from where go to which eligible recipient, when can that card be used, and under what own-hand/role condition is a new hand drawn?',
'Reincarnator':'what results trigger Reincarnation, where is the replacement drawn from and which candidates are rejected, what happens on later losses, what old power remains, and what happens when another power copies this one and then loses?',
'Remora':'what separate retrieval and draw events permit Cling, how much is obtained per event, where do the benefits come from, and what same-encounter retrieval restriction applies?',
'Reserve':'when may Reinforce turn which attack cards into what value, how many may it use, and what cost cancels another player\'s reinforcement and where does that canceled card go?',
'Shadow':'which destiny draws trigger Execute, who chooses whose ship from which location, how is wild handled and must its target match offense\'s chosen defense?',
'Sorcerer':'when relative to selection/reveal does Magic act, what is switched, and which card does each player reveal afterward?',
'Spiff':'under the retained official crash-landing erratum, what card pairing, losing margin and role permit Crash Land, how many ships escape what loss and land where, and which coexistence restrictions remain? Does the margin condition include a low-total-wins encounter?',
'Tick-Tock':'how many tokens are set up in the standard five-planet game, which two types of events remove tokens, what happens at the final token, and can Tick-Tock still win normally?',
'Trader':'when may Transference act, which hands are exchanged and who keeps which hand afterward?',
'Tripler':'when does Thrice act, what card type is required, what happens at values10-or-less versus above10, and what rounding applies? Calculate attacks10 and11.',
'Vacuum':'what event triggers Catharsis, how many additional ships may be lost, who chooses targets/quantities versus exact colony sources, can Vacuum target itself, and are these losses additional to ordinary losses?',
'Virus':'when does Multiply act, how are its own ships and attack card combined, how are allied ships counted, and what total results from attack8, three own ships and two allied ships?',
'Void':'what result and role trigger Eradicate, whose ships go to which destination, what minimum number of surviving ships is protected in this standard game and where do excess losses go? If an opponent has six ships not permanently removed and would lose three, how many can be eradicated and how many go to warp?',
'Vulch':'whose discarded artifacts trigger Salvage, does played versus unplayed matter, can it salvage its own played artifacts, and what special reveal/retention/new-draw procedure applies when refreshing a hand?',
'Warpish':'when and with which revealed card may Necromancy act, whose warp ships count, and how much do they add?',
'Warrior':'under the retained official experience erratum, in which role/results are tokens gained and in what quantities; when/how is the combat bonus used, what card type is required and are the tokens spent?',
'Will':'under the official timing correction, when does Choice act, how may it change the opponent/location, what third-player-system colony requirement remains, and do other effects of the drawn destiny card still occur?',
'Zombie':'when does Immortality prevent a warp loss, where are ships sent instead, which additional deal clause does not require power use, who may be liberated under the FAQ and where do freed ships go?'
}
d=json.loads((R/'source-review/alien-catalog.json').read_text())
Q=json.loads((R/'seed-v1/questions.json').read_text());K=json.loads((R/'seed-v1/answer-key.json').read_text())
Q['benchmark_version']=K['benchmark_version']='expanded-draft-01'
ledger=[]
for a in d['aliens']:
 name=a['alien'];ident=f'Q{len(Q["questions"])+1:03}'
 question=f'For {name}, state the eligible player role, whether use is optional or mandatory, and its phase(s); then explain '+prompts[name]
 facts=[f"Role: {a['role']}; use: {a['use']}.",f"Phase(s): {', '.join(['Destiny'] if name=='Will' else ['Launch','Alliance','Reveal'] if name=='Macron' else a['phases'])}."]+a['setup']+a['rules']+a['restrictions']
 facts=[x.replace(' In either case add ONE EXTRA if playing four planets per player.','').split('; EIGHT')[0]+('.' if '; EIGHT' in x else '') for x in facts]
 refs=[f"Printed original {name} sheet ({a['source']['sha256']})"]
 if name=='Anti-Matter':facts+=['Defense still wins ties under the unchanged general tie rule.'];refs+=['Rulebook p9 Attack vs Attack']
 if name=='Macron':
  facts=[x.replace('As defense or ally use after allies invited.','As ally use after allies invited. As main player or ally, use after reveal for ship strength.') for x in facts]
  facts+=['Defense does not have the one-ship launch restriction.'];refs+=['Official FAQ May6 2009 p1 Macron erratum; 2018 FAQp17']
 if name=='Calculator':facts+=['15 becomes7;8 remains8.']
 if name=='Mirror':facts+=['15→51;20→02;08→80.']
 if name=='Spiff':
  facts=[x.replace('own total was 10 OR MORE less than defense','you lost by 10 OR MORE, including low-total-wins encounters') for x in facts];refs+=['Official FAQ May6 2009 p1 Spiff erratum']
 if name=='Tripler':facts+=['Attack10→30; attack11→4.']
 if name=='Vacuum':facts+=['Cannot target itself.'];refs+=['FAQ2018p2 Vacuum erratum']
 if name=='Virus':facts+=['8×3+2=26.']
 if name=='Void':facts+=['Standard minimum is five ships remaining in game, counting ships in warp as still in game; from six ships with three losses, eradicate one and send two to warp.']
 if name=='Warrior':
  facts=[x.replace('Add one token each time you win encounter or make deal, TWO each time lose or fail deal.','After an encounter as MAIN PLAYER, add one token for win/deal or two for loss/faileddeal.') for x in facts];refs+=['Official FAQ May6 2009 p1 Warrior erratum; FAQ2018p22']
 if name=='Will':facts+=['When targeting a third-player system, the chosen defense must have a colony there; home owner can defend its empty planet.'];refs+=['FAQ2018p2 Will erratum,p22']
 if name=='Zombie':facts=[x.replace('May free ANY player\'s ships from warp back to any colonies that player has as part of deal.','Deal liberation is a non-use clause; may liberate any number of negotiating opponent\'s ships, not a third player\'s, back to that opponent\'s colonies.') for x in facts];refs+=['Rulebookp12 non-use;FAQ2018p22 Zombie']
 K['answers'].append({'id':ident,'required_facts':facts,'contextual_background':[],'source_references':refs})
 Q['questions'].append({'id':ident,'question':question})
 ledger.append({'id':ident,'source':a['source']['original_file'],'source_sha256':a['source']['sha256'],'novelty':f'Distinct {name} procedure, eligibility and outcome exceptions; not a numerical rephrasing of another power.','asked_fact_count':len(facts),'status':'candidate-parent-acceptance-pending'})
out=R/'expanded-draft-01';out.mkdir(exist_ok=True)
for fn,x in [('questions.json',Q),('answer-key.json',K),('alien-coverage-candidates.json',ledger)]: (out/fn).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
print(len(Q['questions']),'draft questions')
