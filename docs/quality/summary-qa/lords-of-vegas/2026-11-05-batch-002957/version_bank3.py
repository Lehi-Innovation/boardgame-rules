import json,hashlib
from pathlib import Path
R=Path(__file__).parent;D=R/'expanded-v3';D.mkdir();load=lambda p:json.loads(p.read_text());dump=lambda p,o:p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
q=load(R/'expanded-v2/questions.json');k=load(R/'expanded-v2/answer-key.json');q['benchmark_version']=k['benchmark_version']='expanded-v3'
question='Besides taking their own components, what banking role must the group assign during setup?'
answer='Choose a player to be the Banker.';source='Original p2 Setting Up, second paragraph; unified physical p5 Setting Up.'
q['questions'].append({'id':'Q35','question':question});k['answers'].append({'id':'Q35','required_facts':[answer],'expected_answer':answer,'source_references':source,'contextual_background':[]})
dump(D/'questions.json',q);dump(D/'answer-key.json',k)
m=load(R/'expanded-v2/scope-map.json');m['version']='scope-v3'
for e in m['entries']:
 i=e['id'];f=e['required_answer_facts'];b=e['contextual_key_background']
 if i=='Q10':f[1]='The stated eligible lot is empty/unowned and edge-adjacent; opponent-marked and diagonal-only targets are illegal.';b.append('The question already gives that the acting player is the casino boss; no need to restate a given as an extra fact.')
 if i=='Q17':f[0]='Trade money, lots, casino dice and actions on the active player’s current turn. Trading may occur even off-turn, except no initiated trades during unresolved boss ties or after End of Game is drawn.'
 if i=='Q27':
  f[1]='Different players now tie for highest: immediately reroll both highest 6s (remaining Red and new Green), not Blue3.';b.append('Boss-tie rerolls are free; Q14 explicitly asks cost, Q27 does not.')
 if i=='Q32':e['required_answer_facts']=['No: End of Game draw immediately ends play, so players cannot initiate a money/die trade before final payouts.'];b.append('Final lots and Strip payouts, score/money win comparison are already asked by Q19; they are not additional requirements for this trade-priority question.')
m['entries'].append({'id':'Q35','asked_question':question,'required_answer_facts':[answer],'contextual_key_background':[],'source_references':source})
m['versioned_corrections'] += [{'id':x,'change':v} for x,v in [('Q10','Boss status is given, not extra explanatory requirement.'),('Q17','Broad timing asks both explicit exceptions: no initiated trades in boss-tie resolution or after End of Game.'),('Q27','Reroll cost not asked; free is background here, timing and rollers remain required.'),('Q32','Required facts narrowed to actual trade-priority question; final payout/winner recap is background.'),('Q35','Previously unasked setup Banker actor assignment added from original source.')]]
m['preservation']='All baseline Q01–34 questions and answer records remain identical to expanded-v2; the effective grading-key-v3 below is the explicitly versioned asked-scope correction, frozen before full-bank testing.'
dump(D/'scope-map.json',m);dump(D/'grading-key.json',{'version':'grading-key-v3','baseline':'answer-key.json','scope_map':'scope-map.json','answers':[{**e,'expected_answer':' '.join(e['required_answer_facts'])} for e in m['entries']]})
(D/'question-bank.md').write_text('# Lords of Vegas — expanded-v3 (35 questions)\n\nOriginal Q01–34 questions and baseline answers are preserved. The versioned [scope map](scope-map.json) and [effective grading key](grading-key.json) distinguish actual asked facts from contextual baseline notes.\n\n'+'\n\n'.join('## '+x['id']+'\n\n'+x['asked_question']+'\n\n'+' '.join(x['required_answer_facts'])+'\n\nSource: '+x['source_references'] for x in m['entries'])+'\n')
l=load(R/'coverage-ledger-v2.json');l['passes'] += [{'pass':7,'focus':'Fresh independent complete-source challenge accepted previously unasked original setup actor','accepted':[{'id':'Q35','novelty':'Choose a player as Banker: procedural actor assignment not asked by earlier setup questions.'}]},{'pass':8,'focus':'Complete baseline procedure reread with effective asked-fact mapping: setup actors/pieces/score/cards/deck, turn, every action, resources, payouts, boss, trade and end','accepted':[]},{'pass':9,'focus':'Targeted exception challenge: repeated F draws, exhausted resources, own/empty-die takeovers, reorg versus free tie rolls, interrupted/multiparty/end trades and scoring breaks','accepted':[]}]
l['coverage_map'] += [{'passage':'Original p2 Setting Up choose a Banker; unified p5','questions':['Q35']}]
l['stopping_rule']='After accepting independent Q35, passes8 and9 add zero. All core procedural passages mapped to actually asked facts. Independent final reviewer recheck pending.'
l['rejected_candidates'] += [{'candidate':'Another designated Banker example by different player color','reason':'Q35 now directly tests the sole rule; choosing a different person is cosmetic.'},{'candidate':'Trade-during-boss-tie question beyond Q27','reason':'Q27 already explicitly asks whether reroll must finish before further trades/actions; Q17 now requires both timing exceptions in own broad answer.'}]
dump(R/'coverage-ledger-v3.json',l)
manifest={'benchmark':'expanded-v3','question_count':35,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in D.iterdir() if p.is_file()},'unchanged_baseline_entries':{'questions_Q01_Q34':q['questions'][:34]==load(R/'expanded-v2/questions.json')['questions'],'key_Q01_Q34':k['answers'][:34]==load(R/'expanded-v2/answer-key.json')['answers']}}
dump(D/'bank-freeze-manifest.json',manifest);print(manifest['unchanged_baseline_entries'])
