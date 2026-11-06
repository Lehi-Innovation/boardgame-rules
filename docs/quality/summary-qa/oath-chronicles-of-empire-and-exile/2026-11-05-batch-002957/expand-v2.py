from pathlib import Path
import json,hashlib,copy,difflib
P=Path(__file__).resolve().parent;review=json.loads((P/'coverage-review-01.json').read_text());q=json.loads((P/'expanded-v1/questions.json').read_text());k=json.loads((P/'expanded-v1/answer-key.json').read_text());oldk=copy.deepcopy(k)
q['benchmark_version']='expanded-v2';k['benchmark_version']='expanded-v2';corrections=[]
for entry in k['answers']:
 before=entry['expected_answer']
 if entry['id']=='Q008':entry['expected_answer']=before.replace('Draw up to three available','Draw the prescribed three, or all available if source runs out, except when a world Vision stops drawing or a modifier changes count')
 if entry['id']=='Q017':entry['expected_answer']=before.replace('Citizen targeted by Chancellor likewise.','If Chancellor chooses Citizen as defender, that Citizen is non-Imperial during this Campaign.')
 if entry['id']=='Q030':entry['expected_answer']=before.replace('Facedown banners inactive.','Restriction banners on facedown cards do not apply.')
 if before!=entry['expected_answer']:
  entry['material_facts']=entry['expected_answer'].split('; ');corrections.append({'id':entry['id'],'old':before,'new':entry['expected_answer'],'reason':'Independent coverage review clarification; no substantive ruling relaxed. Ambiguity/terminology corrected with explicit version, historical key remains intact.','source_references':entry['source_references']})
for n,addition in enumerate(review['proposed_additions'],83):
 id=f'Q{n:03}';q['questions'].append({'id':id,'question':addition['question']});k['answers'].append({'id':id,'expected_answer':addition['expected_answer'],'material_facts':addition['expected_answer'].split('. '),'source_references':'; '.join(addition['source_references'])})
d=P/'expanded-v2';d.mkdir()
for name,x in [('questions.json',q),('answer-key.json',k)]: (d/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
(d/'question-bank.md').write_text('# Oath expanded benchmark v2\n\n92 regression questions; 10 historical overlapping candidates retained with zero novelty credit. Three explicit key clarifications are recorded separately; no prior record is overwritten.\n\n'+ '\n\n'.join(f"## {a['id']}\n\n{b['question']}\n\n**Answer:** {a['expected_answer']}\n\n**Source:** {a['source_references']}" for a,b in zip(k['answers'],q['questions']))+'\n')
(d/'input-manifest.json').write_text(json.dumps({f:hashlib.sha256((d/f).read_bytes()).hexdigest() for f in ['questions.json','answer-key.json']},indent=2)+'\n')
(d/'key-corrections.json').write_text(json.dumps(corrections,indent=2,ensure_ascii=False)+'\n')
sh=Path('rules/oath-chronicles-of-empire-and-exile.md');before=sh.read_text();t=before.replace('After first game open Archive packet: place 8 dividers;','After first game open Archive packet: place 8 cardboard dividers in the small box compartment;')
t=t.replace('Forced Citizenship powers apply acceptance without a negotiated offer.','**Forced Citizenship** powers apply the same status-conversion steps without a negotiated offer: no required Scepter offer or Reliquary relic gift, and no invented promised exchange. Only an actual removal of a Reliquary relic uncovers its modifier.')
t=t.replace('At Salt Flats, Mine or Drowned City, optionally take 1 favor or secret from that site.','At Salt Flats, Mine or Drowned City, optionally take 1 favor **or** 1 secret from that site: one token total, only if your pawn is there. Remote rule gives no income; an empty site gives nothing, with no bank substitute.')
t=t.replace('Oathkeeper +1 defense die, Usurper +2.','Oathkeeper +1 defense die, Usurper +2. The mandatory title bonus is itself a Campaign modifier.')
t=t.replace('**Draw outside Search:**','**Moving and swapping cards:** Move follows capacity, placement and restriction rules; Swap moves the two pieces to each other’s location, obeying those rules for both. A move or swap alone is not playing: it grants no site-play favor and triggers no When Played power. An instruction explicitly saying to play does trigger ordinary play effects.\n\n**Draw outside Search:**')
sh.write_text(t);(P/'coverage-summary-changes.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),t.splitlines(True),fromfile='before-coverage-additions',tofile='canonical-coverage-additions')))
oldledger=json.loads((P/'coverage-ledger.json').read_text());(P/'coverage-ledger-before-independent-challenge.json').write_text(json.dumps(oldledger,indent=2,ensure_ascii=False)+'\n');ledger=copy.deepcopy(oldledger)
rejected=review['novelty_review']['rejected_new_coverage_candidates'];ids={x['id'] for x in rejected}
for a in ledger['accepted_questions']:
 if a['id'] in ids:a.update(accepted=False,classification='historical redundant regression only',novelty_credit=0,reason=next(x['reason'] for x in rejected if x['id']==a['id']))
ledger['rejected_new_coverage_candidates']=rejected
for n,a in enumerate(review['proposed_additions'],83):ledger['accepted_questions'].append({'id':f'Q{n:03}','source_references':a['source_references'],'novelty':a['title'],'accepted':True,'reviewer_proposal':a['proposal_id']})
c=ledger['coverage_map'];c['Law 1.2 markers']=['Q083'];c['Law 4 introductory turn and round sequence']=['Q083'];c['Law 5.2 Muster']=['Q011','Q062'];c['Law 2.3–5 Reliquary/relics/banners']=['Q012','Q013','Q019','Q044','Q069'];c['Law 2.11 title defense modifier']=['Q088'];c['Law 4.1.4 opportunity-site income']=['Q092'];c['Site Reference Opportunity']=['Q092'];c['Law 7.1.2 costs']=['Q027','Q087'];c['Law 7.6.1 forced citizenship']=['Q086'];c['Playbook 29 first Archive setup']=['Q085'];c['Playbook 6–7 first-game deck and discards']=['Q025','Q084'];c['Law Glossary Move Swap Play']=['Q089'];c['Law Glossary Kill Sacrifice']=['Q090'];c['Playbook p32 bandits not competing']=['Q091']
ledger['passes'].append({'pass':5,'focus':'Independent coverage challenge and source-first gap adjudication','accepted_ids':[f'Q{x:03}' for x in range(83,93)],'count':10,'historical_novelty_rejections':sorted(ids),'key_clarifications':['Q008','Q017','Q030'],'stopping_reset':True})
ledger['stopping_rule']={'consecutive_zero_addition_passes':0,'all_core_procedural_passages_mapped':True,'independent_challenge':'reopened after coverage-review-01; pending new zero passes and fresh review'}
(P/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
x=json.loads((P/'progress.json').read_text());x.update(question_count=92,phase='coverage-reopened-and-key-clarified',coverage_review='coverage-review-01.json: reopen,10 additions',coverage_stopping_rule=ledger['stopping_rule']);(P/'progress.json').write_text(json.dumps(x,indent=2)+'\n')
print('92 questions, explicit key clarifications', [x['id'] for x in corrections])
