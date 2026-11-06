from manage import *
# Retain earlier grades before fresh adjudication fixes over-demanding Q47 procedures.
I=R/'expanded-iteration-01';shutil.copyfile(I/'results.json',I/'results-before-operations-adjudication.json');out=json.loads((I/'results.json').read_text())
for who in ['a','b']:
 row=next(x for x in out[who]['grades'] if x['id']=='Q47');row.update(grade='correct',reason='Fresh independent operations-scope adjudicator: names resolve the availability clause; individual operation procedures are contextual key extras not requested by Q47. Other asked facts supplied. See operations-scope-adjudication.json.')
 out[who]['totals']={g:sum(x['grade']==g for x in out[who]['grades']) for g in ['correct','partial','incorrect']}
save(I/'results.json',out)
p=R/'grading-corrections.json';corrections=json.loads(p.read_text());corrections.append({'iteration':'expanded-iteration-01','questions':['Q47 A','Q47 B'],'old_grade':'partial','new_grade':'correct','reason':'Fresh independent adjudication found individual operation procedures outside actual requested availability clause. Original grades and independent grader report retained. Explicit Recruit procedure is reopened as new coverage.','evidence':'operations-scope-adjudication.json'});save(p,corrections)
x=json.loads((R/'expanded-iteration-02/independent-grades.json').read_text());rows={w:x['readers']['reader-'+w]['answers'] for w in ['a','b']};notes={w:{g['id']:(g['grade'],g['reason']) for g in rows[w]} for w in ['a','b']};grades('expanded-iteration-02','benchmark-v3',notes)
p=R/'expanded-iteration-02/results.json';out=json.loads(p.read_text())
for w in ['a','b']:
 for row,g in zip(out[w]['grades'],rows[w]):
  row['requested_fact_checklist']=g['requested_fact_checklist'];row['unsupported_guess']=g['unsupported_guess'];row['independent_summary_support']=g['summary_support']
save(p,out)
# A new benchmark adds a genuinely untested operation procedure, preserving all earlier entries.
B=R/'benchmark-v4';B.mkdir();q=json.loads((R/'benchmark-v3/questions.json').read_text());k=json.loads((R/'benchmark-v3/answer-key.json').read_text());q['benchmark_version']=k['benchmark_version']='v4'
q['questions'].append({'id':'Q78','question':'During Alliance Evening, how many military operations may be taken, and for one Recruit operation how many warriors are placed and where?'})
k['answers'].append({'id':'Q78','expected_answer':'Take up to the number of officers, in any order and repetition. One Recruit operation places one warrior from supply in any one clearing with an Alliance base, not one at every base. Officers stay on board when operations are used.','source_references':'8.6.1 preamble;8.6.1.III'})
save(B/'questions.json',q);save(B/'answer-key.json',k);save(B/'input-manifest.json',{'hashes':{str(p):sha(p) for p in [B/'questions.json',B/'answer-key.json',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'reason':'Explicit Alliance Recruit and military-operation allowance coverage after fresh actual-question-scope adjudication; no prior entry changed.'})
text='# Root complete question/answer bank v4\n\n'+scope+'\n\n'
for a,b in zip(q['questions'],k['answers']):text+=f"## {a['id']}\n\n{a['question']}\n\n**Expected:** {b['expected_answer']}\n\n**Law:** {b['source_references']}\n\n"
(B/'question-bank.md').write_text(text)
shutil.copyfile(R/'coverage-ledger.json',R/'coverage-ledger-v3.json');ledger=json.loads((R/'coverage-ledger.json').read_text());ledger['accepted'].append({'id':'Q78','source_references':'8.6.1 preamble;8.6.1.III','novelty':'Q47 asks available operation names, officer consumption and draw timing, not individual procedures. Fresh adjudication confirms the one-warrior-at-one-chosen-base Recruit rule is not explicitly tested elsewhere. This question directly tests that new core procedure plus the operation-budget rule.','origin':'operations-scope-adjudication.json'})
for row in ledger['coverage_map']:
 if row['source_passage']=='8.6.1-2':row['questions'].append('Q78')
ledger['coverage_map'].append({'source_passage':'8.6.1 preamble;8.6.1.III','procedure':'Officer-count operation allowance and one-warrior-at-one-chosen-base Recruit procedure','questions':['Q78']})
ledger['passes'] += [{'pass':8,'focus':'Reopen actual-question coverage after independent scope adjudication of operation-name versus procedure requests','count':1,'accepted':['Q78'],'all_core_procedural_passages_mapped':True},{'pass':9,'focus':'Audit every mapped passage against explicit question requests, distinguishing contextual key extras; revisit common rules, setup and component destinations','count':0,'accepted':[],'all_core_procedural_passages_mapped':True,'rejections':['Alternate supply counts, hand sizes and card suits repeat existing rules; Q78 now explicitly requests the operation budget and Recruit procedure.']},{'pass':10,'focus':'Challenge each faction action/effect and map/character passage again, especially definitions previously only contextual in another question','count':0,'accepted':[],'all_core_procedural_passages_mapped':True,'rejections':['Move and Battle procedures explicitly tested by Q02/Q03/Q68; Organize explicitly Q16; Recruit now Q78; base-loss, ally-hit and Infamy variants repeat fixed branches.']}]
ledger['stopping_rule']={'consecutive_zero_addition_passes':2,'after_complete_mapping':True,'passes':[9,10],'independent_challenge':'Fresh v4 challenge pending','note':'Retain prior ledger/reviews; Q47 scope adjudication reopened a specific procedure instead of over-demanding its availability question. Working saturation only.'};save(R/'coverage-ledger.json',ledger)
# General summary layout repairs, without adding question-specific worked answers.
p=ROOT/'rules/root.md';s=p.read_text();needle='**Birdsong:** Complete **all Revolts before starting any Spread Sympathy**; each may be performed any number of times.';assert needle in s;s=s.replace(needle,needle+' **For both actions, every supporter spent must match the target clearing; birds are wild.**')
a=s.index('- **Move with ally:**');b=s.index('- **Hostile:**',a)
s=s[:a]+'''**Allied benefits:**

| Action with an Allied faction | Benefit and limits |
|---|---|
| Aid | Each subsequent Aid to this Allied faction scores **two VP** |
| Move | May force warriors of **one** Allied faction to accompany the pawn to its destination clearing. They follow their own movement restrictions, including rule and Eyrie tie advantage. They cannot accompany a move specified to be alone. Moving them into sympathy triggers Outrage |
| Attack | At the start of battle **as attacker**, may treat warriors of **one** Allied faction there as your own. **Rolled-hit cap = those allied warriors plus all your undamaged swords.** They can join against a different enemy; cannot use that ally's warriors to attack the ally itself |

**Taking hits with an ally:** In a battle using Allied warriors as your own, you may absorb hits by removing those warriors or damaging your items. If you remove **more allied warriors than items you damage in that battle**, the ally becomes Hostile **at battle end**. This overrides ordinary hostility timing for those friendly warriors taken as hits against the other enemy. Equal numbers do not trigger the rule.

'''+s[b:];p.write_text(s)
p=R/'progress.json';x=json.loads(p.read_text());x.update(phase='v4_coverage_challenge',question_count=78,coverage_review='v3 PASS retained; precise Recruit procedure gap reopened after scope adjudication, v4 challenge pending',coverage_stopping_rule={'pending_fresh_challenge':True,'passes':[9,10]},final_reader_scores={'expanded-iteration-01':{'a':{'correct':70,'partial':6,'incorrect':1},'b':{'correct':61,'partial':13,'incorrect':3}},'expanded-iteration-02':{'a':{'correct':74,'partial':2,'incorrect':1},'b':{'correct':75,'partial':1,'incorrect':1}}},source_audit='Updated Allied layout and matching-supporter reminder require exact new audit',final_snapshot_path=None);save(p,x)
