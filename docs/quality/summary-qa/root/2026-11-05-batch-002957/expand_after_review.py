from build_evidence import *
shutil.copyfile(R/'coverage-review.json',R/'coverage-review-01.json')
shutil.copyfile(R/'coverage-ledger.json',R/'coverage-ledger-v2.json')
review=json.loads((R/'coverage-review-01.json').read_text());B=R/'benchmark-v3';B.mkdir()
q=json.loads((R/'benchmark-v2/questions.json').read_text());k=json.loads((R/'benchmark-v2/answer-key.json').read_text());q['benchmark_version']='v3';k['benchmark_version']='v3'
ledger=json.loads((R/'coverage-ledger.json').read_text());new=[]
for i,p in enumerate(review['proposed_new_questions'],67):
 id=f'Q{i:02}';q['questions'].append({'id':id,'question':p['question']});k['answers'].append({'id':id,'expected_answer':p['expected_answer'],'source_references':';'.join(p['source_references'])});new.append(id)
 ledger['accepted'].append({'id':id,'source_references':p['source_references'],'novelty':p['novelty_rationale'],'origin':'coverage-review-01.json#'+p['id']})
for i,(qq,aa,ss,nn) in enumerate([
 ('What is the order of phases in a turn, and whose turn begins after Evening ends?', 'Birdsong, then Daylight, then Evening; next clockwise player begins after Evening ends. Continue until a player wins.','1.4.1','Basic turn handoff is not the phase-boundary effects rule of Q23 or setup turn-order assignment of Q66.'),
 ('When Vagabond takes a hit, which item must be chosen, where does it go, does its face change, and can already-damaged items absorb another hit?', 'Choose one undamaged item and move it to Damaged box, keeping its current face. Cannot select an already-damaged item to absorb another hit. With no undamaged items remaining, ignore remaining hits.','9.2.5;9.2.7;9.5.7','Damage destination and unchanged exhaustion state are distinct from rolled-hit caps, repair/rest, track routing or permanently removing excess items.')],76):
 id=f'Q{i:02}';q['questions'].append({'id':id,'question':qq});k['answers'].append({'id':id,'expected_answer':aa,'source_references':ss});new.append(id);ledger['accepted'].append({'id':id,'source_references':ss,'novelty':nn,'origin':'evaluator post-challenge source pass'})
save(B/'questions.json',q);save(B/'answer-key.json',k)
save(B/'input-manifest.json',{'hashes':{str(p):sha(p) for p in [B/'questions.json',B/'answer-key.json',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'reason':'Coverage additions after independent challenge. No prior question/key entries changed.'})
text='# Root complete question/answer bank v3\n\n'+scope+'\n\n'
for qq,aa in zip(q['questions'],k['answers']):text+=f"## {qq['id']}\n\n{qq['question']}\n\n**Expected:** {aa['expected_answer']}\n\n**Law:** {aa['source_references']}\n\n"
(B/'question-bank.md').write_text(text)
cr_to_id={p['id']:f'Q{i:02}' for i,p in enumerate(review['proposed_new_questions'],67)}
for row in ledger['coverage_map']:
 for checked in review['checked_passages']:
  if checked['source_passage']==row['source_passage']:
   for cr in checked['proposed_questions']:
    if cr_to_id[cr] not in row['questions']:row['questions'].append(cr_to_id[cr])
ledger['coverage_map'] += [{'source_passage':'8.5 phase preamble;8.5.2','procedure':'Free Daylight interleaving and Mobilize action','questions':['Q73']},{'source_passage':'1.4.1 turn cycle','procedure':'Phase sequence and clockwise handoff','questions':['Q76']},{'source_passage':'9.2.7 damage operation','procedure':'Undamaged item choice, damage box destination, face preserved','questions':['Q77']}]
ledger['passes'] += [
 {'pass':5,'focus':'Resolve nine independent challenge gaps; reread actual keyed answers for all mapped source clauses; add turn handoff and damage destination','accepted':new,'count':len(new),'all_core_procedural_passages_mapped':True},
 {'pass':6,'focus':'Recheck common procedural passages clause by clause against actual question wording and expected answers, including setup/card destinations/end conditions','accepted':[],'count':0,'all_core_procedural_passages_mapped':True,'rejections':['Different deck-empty count repeats Q25; alternative piece shortage repeats Q26; different simultaneous victory seats repeats Q30; ruined slot variants repeat Q58; battle actor effect order variants repeat Q69.']},
 {'pass':7,'focus':'Recheck every base faction procedure, maps and characters against actual bank; challenge conditional/timing branches','accepted':[],'count':0,'all_core_procedural_passages_mapped':True,'rejections':['Alternative Mobilize hand/card suits repeat Q73; alternative roost counts repeat Q74; alternative exhausted sword numbers repeat Q75; base-loss/Outrage battle example recombines Q69 order choice with Q14/Q16 without a distinct new timing or exception; alternative damage item types repeat Q77.']}]
ledger['rejected'].append({'candidate':'Alliance base/sympathy losses in same battle, resolve base discard before receiving Outrage','reason':'Q69 now expressly tests owner order for removal-triggered battle effects; this recombines that tested timing rule with Q14/Q16 without a distinct new exception or timing.','source':'4.3.6;8.2.4;8.2.6'})
ledger['stopping_rule']={'consecutive_zero_addition_passes':2,'after_complete_mapping':True,'independent_challenge':'Second fresh review pending after first review reopened coverage','passes':[6,7],'note':'Original passes3/4 failed independent challenge, retained in v2 ledger. Current stop is working saturation, not proof of every combination.'};save(R/'coverage-ledger.json',ledger)
p=ROOT/'rules/root.md';s=p.read_text();s=s.replace('Items are not faction pieces or enemy pieces.','Items are not faction pieces or enemy pieces. **Faction-piece ownership cannot change**: each player owns the faction chosen in setup and its listed faction pieces, except items; possessing an item does not make it faction-owned.');p.write_text(s)
save(R/'coverage-revisions.json',{'v1':20,'v2':66,'v3':77,'v2_review':'NEEDS_ADDITIONS','added_after_review':new,'unchanged_prior_entries':True,'key_corrections':[]})
