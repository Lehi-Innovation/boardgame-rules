from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copyfile(R/'coverage-ledger.json',R/'coverage-ledger-draft-v2.json')
l=load(R/'coverage-ledger.json')
accepted=l['passes'][0]['accepted'].pop()
l['passes'][0]['rejected'].append({'candidate':'Q21: right card/location but wrong orientation on verification','reason':'Independent coverage finding F01: existing Q12 orientation plus Q16 incorrect-card feedback; mechanical recombination. Draft was never reader-tested; preserve benchmark-v2 as an unaccepted candidate bank.'})
l['passes'][0]['classification_correction']='Initial proposed acceptance of Q21 rejected by independent coverage reviewer; no source/key change to Q01–Q20.'
l['source_map'][11]['questions']=['Q12','Q16'];l['source_map'][11]['coverage_note']='Orientation is explicit in Q12 key; incorrect-card procedure in Q16. Fresh reviewer rejected candidate Q21 as redundant.'
l['passes'].extend([
 {'pass':4,'focus':'Post-review re-read of complete source and original-bank mapping, with branch novelty challenge','accepted':[],'rejected':[
 {'candidate':'Wrong rotation at original location','reason':'Review finding F01: Q12 plus Q16, no new rule or branch.'},
 {'candidate':'First Spectator decided by age, marker color or left neighbor','reason':'Source merely says choose first Spectator. No mandatory chooser or method; Q11 already asks chosen first role.'},
 {'candidate':'After a perfect first attempt, do not perform retry','reason':'Q15 expressly requests whether second attempt needed.'},
 {'candidate':'Score original correct cards on both attempts','reason':'Q18 asks final score after second attempt; second-attempt per-card total already tested, no extra temporal exception in source.'}]},
 {'pass':5,'focus':'Second post-review pass through all setup, permissions, geometry, attempt bounds, card destinations and terminal procedure','accepted':[],'rejected':[
 {'candidate':'A different number of correct cards at final check','reason':'Q18 per-card branch, changed number only.'},
 {'candidate':'Board/marker quantities and alternative legal Clue examples','reason':'Stock inventory or renamed examples of Q01/Q03–Q07; no new binding procedure.'},
 {'candidate':'Illegal Clue penalty, exchanging original cards, deck exhaustion or moving correct retry cards','reason':'No explicit ruling in supplied source; outside source-backed standard procedure.'},
 {'candidate':'Next Spectator after final player finishes','reason':'Q19 gives normal leftward succession; Q20 expressly terminates after each once. No additional resolution after terminal condition.'}]}
])
l['independent_challenge']={'path':str(R/'coverage-review.json'),'outcome':'Original Q01–Q20 source-supported and saturated; Q21 rejected as overlapping, no qualifying additions.'}
l['consecutive_zero_addition_passes']=4
l['coverage_stopping_rule_met']=True
l['saturation_claim']='Working saturation at20 after all standard procedural passages mapped, zero-addition passes2/3, fresh independent challenge with no real gap, and confirmation zero-addition passes4/5. No quota or artificial question expansion.'
save(R/'coverage-ledger.json',l)
q=load(R/'benchmark-v1/questions.json');k=load(R/'benchmark-v1/answer-key.json')
q['benchmark_version']=k['benchmark_version']='v3-complete-20'
b=R/'benchmark-v3';b.mkdir(exist_ok=False)
save(b/'questions.json',q);save(b/'answer-key.json',k)
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'complete bank frozen after coverage stopping check; original20 unchanged; untested draftQ21 rejected for novelty, not reader performance','original_question_entries_preserved':q['questions']==load(R/'benchmark-v1/questions.json')['questions'],'original_answer_entries_preserved':k['answers']==load(R/'benchmark-v1/answer-key.json')['answers'],'inputs':{str(p):sha(p) for p in [b/'questions.json',b/'answer-key.json',R/'coverage-ledger.json',R/'coverage-review.json',R.parents[4]/'extracted/so-clover-rules.txt',R.parents[4]/'source_pdfs/so-clover-rules.pdf']}}
save(b/'input-manifest.json',manifest)
# Freeze rejected draft inputs and provenance separately, without changing its contents.
save(R/'benchmark-v2/input-manifest.json',{'status':'UNACCEPTED/UNTESTED candidate bank; Q21 rejected by independent novelty review; retained as history','inputs':{str(p):sha(p) for p in [R/'benchmark-v2/questions.json',R/'benchmark-v2/answer-key.json',R/'coverage-ledger-draft-v2.json']}})
for name in ['questions.json','answer-key.json']:shutil.copyfile(b/name,R/name)
text=['# So Clover! standard-play question and answer bank','',q['scope'],'','Complete bank: **20** questions. The original20 were written source-first before the new summary. Targeted expansion found no qualifying new branch; draftQ21 was rejected by the independent reviewer as Q12+Q16 recombination. The original wording, IDs and answers remain unchanged.','']
for question,key in zip(q['questions'],k['answers']):
 text.extend([f"## {question['id']}",'',question['question'],'',f"**Expected answer:** {key['expected_answer']}",'',f"**Source:** PDF p.{key['source_references'][0]['pdf_page']}; extraction lines {key['source_references'][0]['extraction_lines']} (not PDF line numbers).",''])
(R/'question-bank.md').write_text('\n'.join(text))
p=load(R/'progress.json');p.update(question_count=20,coverage_review='PASS for complete original20; Q21 novelty rejection resolved in ledger',coverage_stopping_rule='MET: passes2/3 zero, fresh independent challenge no new branch, passes4/5 zero; working saturation at20',phase='seed-retest-and-final-bank-frozen');save(R/'progress.json',p)
