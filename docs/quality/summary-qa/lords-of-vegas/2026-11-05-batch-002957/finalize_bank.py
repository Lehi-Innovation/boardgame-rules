import json,shutil,hashlib
from pathlib import Path
from build_bank import R,rows,save_bank
from expand_bank import extra
review=json.loads((R/'coverage-review.json').read_text())
adds=[(x['question'],[x['answer']],x['source']) for x in review['proposed_additions']]
q,k=save_bank('expanded-v2',rows+extra+adds)
D=R/'expanded-v2';previous=json.loads((R/'expanded-v1/scope-map.json').read_text());entries=previous['entries']
for e in entries:
 i=e['id'];facts=e['required_answer_facts'];bg=e['contextual_key_background']
 if i=='Q03':facts[1]='The newly acquired marked lot pays you $1 in the coming lot payout.';bg.append('All other marked lots also pay their owners $1, tested by Q02/Q06.')
 if i=='Q08':facts[2]='No player takes actions on another player’s turn.';bg.append('Trading may occur at any time subject to exceptions; tested by Q17/Q27/Q32.')
 if i=='Q11':facts.append('Return replaced old-color tiles to their supply.')
 if i=='Q20':facts[-1]='Each such draw pays, so multiple payouts occur in one turn before Play.';bg.append('An End of Game draw interrupts immediately; Q19 and Q32 test end priority.')
 if i=='Q31':e['scope_note']='The proposed sprawl is an intended action by the active player during this same turn. Question wording is preserved. No future-turn promise or off-turn action is authorized.'
for x in review['proposed_additions']:
 entries.append({'id':x['proposed_id'],'asked_question':x['question'],'required_answer_facts':[x['answer']],'contextual_key_background':[],'source_references':x['source']})
corrections={'version':'scope-v2','principle':'Actual asked clauses only; baseline questions and answer records preserved, explicit scope supplement governs required facts.','entries':entries,'versioned_corrections':[{'id':x,'change':why} for x,why in [('Q03','Singular newly acquired lot is asked, other-lot payout is background.'),('Q05','Casino/player color independence is background.'),('Q08','Trading is not an action and not asked.'),('Q09','No neighboring casino stated or asked, so merger is background.'),('Q11','Explicitly require replaced old tiles returned to supply, positively sourced by unified p11; no effect on seed grades because both seed answers already supply it.'),('Q15','Opponent boss is given; require House recipient, computed cap and frequency.'),('Q20','End-card interruption is unasked background.'),('Q22','Trade-to-free-die is an alternative not asked.'),('Q31','Preserve wording and explicitly bind proposed sprawl to active player this turn.')]],'preservation':'Baseline answer-key.json and expected_answer fields remain unchanged for all Q01–31. This scope map is the versioned correction to classifications; no silent target changes.'}
(D/'scope-map.json').write_text(json.dumps(corrections,indent=2,ensure_ascii=False)+'\n')
# Harmonized effective key in separate versioned supplement; originals unchanged.
effective={'version':'grading-key-v2','baseline':'answer-key.json','scope_map':'scope-map.json','answers':[{**e,'expected_answer':' '.join(e['required_answer_facts'])} for e in entries]}
(D/'grading-key.json').write_text(json.dumps(effective,indent=2,ensure_ascii=False)+'\n')
ledger=json.loads((R/'coverage-ledger.json').read_text());ledger['historical_correction']='Initial pass stopping claim was challenged by independent coverage-review.json; final stopping sequence follows accepted Q32–34.'
ledger['passes'] += [ {'pass':4,'focus':'Independent source/coverage challenge accepted additions','accepted':[{'id':x['proposed_id'],'novelty':x['novelty']} for x in review['proposed_additions']]}, {'pass':5,'focus':'Re-read every original procedural passage and base-only clarification against actual asked clauses, including setup pieces, all action and resource conditions, payout order, boss/trade and end priority','accepted':[]}, {'pass':6,'focus':'Challenge outcome branches and interaction timing again: F setup/turn/end, full-casino Strip, die/marker exhaustion, reorg/free reroll distinction, failed trade and end-card trades','accepted':[]}]
for x in ledger['coverage_map']:
 if x['passage']=='Original p2 Setting Up':x['questions'].append('Q33')
 if x['passage']=='Unified p15 interrupted trade':x['questions'].append('Q34')
 if x['passage']=='Unified p16 two-player setup and final no actions/trades':x['questions'].append('Q32')
ledger['coverage_map'] += [{'passage':'Unified p15 Trading any number of participants','questions':['Q34']},{'passage':'Unified p16 Winning no initiated trades after end-card draw','questions':['Q32']}]
ledger['rejected_candidates'] += [{'candidate':'Another last-minute die trade with different score/cash totals','reason':'Q32 tests end-trigger priority over all initiated trades, no new branch.'},{'candidate':'A four-player trade instead of three','reason':'Q34 explicitly tests any-number participants; numeric substitution.'},{'candidate':'A separate dice sum to choose first roller','reason':'Q02 already asks two-dice highest roller and left succession.'},{'candidate':'Exact tie after first-player roll; both score and money tied at end','reason':'No explicit resolution in applicable authority; no invented rule or false gap cap. Summary acknowledges no further end tiebreak.'}]
ledger['stopping_rule']='After independent additions, passes5 and6 add zero; all core procedural passages mapped to asked clauses. Pending fresh challenge of corrected final bank.'
(R/'coverage-ledger-v2.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
manifest={'benchmark':'expanded-v2','question_count':34,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in D.iterdir() if p.is_file()},'unchanged_baseline_entries':{'questions_Q01_Q20':q['questions'][:20]==json.loads((R/'seed-v1/questions.json').read_text())['questions'],'key_Q01_Q20':k['answers'][:20]==json.loads((R/'seed-v1/answer-key.json').read_text())['answers'],'questions_Q01_Q31':q['questions'][:31]==json.loads((R/'expanded-v1/questions.json').read_text())['questions'],'key_Q01_Q31':k['answers'][:31]==json.loads((R/'expanded-v1/answer-key.json').read_text())['answers']}}
(D/'bank-freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(manifest['unchanged_baseline_entries'])
