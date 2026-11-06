from pathlib import Path
import datetime,hashlib,json,shutil
P=Path(__file__).resolve().parent;V=P/'expanded-v11';V.mkdir(exist_ok=False)
def J(p):return json.loads(p.read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def W(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
q=J(P/'expanded-v10/questions.json');k=J(P/'expanded-v10/answer-key.json');s=J(P/'expanded-v10/grading-scope.json')
for obj in [q,k,s]:obj['benchmark_version']='expanded-v11'
entry=next(x for x in k['answers'] if x['id']=='Q046');old_expected=entry['expected_answer'];old_clause='At retained non-winner sites flip intact edifice to ruin and discard denizens there.'
new_clause='At retained non-winner sites flip intact edifices to ruins; this ruining step discards denizens only at sites where an intact edifice actually flipped to ruin.'
assert old_clause in old_expected and old_clause in entry['material_facts'][0]
entry['expected_answer']=old_expected.replace(old_clause,new_clause)
entry['material_facts']=[text.replace(old_clause,new_clause) for text in entry['material_facts']]
assert old_clause not in json.dumps(entry)
ss=next(x for x in s['questions'] if x['id']=='Q046');old_scope=next(x for x in ss['required_facts'] if x['fact_id']=='Q046-F03')['expected_fact']
new_scope='Flip retained non-winner intact edifices to ruins; this ruining step discards denizens only at sites where an intact edifice actually flipped to ruin.'
next(x for x in ss['required_facts'] if x['fact_id']=='Q046-F03')['expected_fact']=new_scope
ss['fixed_key_expected_answer_sha256']=hashlib.sha256(entry['expected_answer'].encode()).hexdigest()
question='During the Chronicle’s edifice-ruining step, an applicable power has already kept a site that the winner does not rule. It has no intact edifice to flip. Does that step discard its denizens just because the site is retained and unruled? What actually triggers that step’s denizen discard?'
expected='No. Law8.3.3 discards denizens only at retained sites where an intact edifice actually flipped to ruin in that step. The winner not ruling a site, or a power retaining it, does not itself trigger that discard. Other retained sites keep their denizens unless another applicable instruction discards them; the earlier disposal of cards on discarded sites is a separate operation.'
refs='Law8.3.2–3,9.1; Playbookp4 embedded Chronicle aid, Forest Temple retention power (power effect supplied, no card recall required)'
q['questions'].append({'id':'Q104','question':question});k['answers'].append({'id':'Q104','expected_answer':expected,'material_facts':['This ruining step discards denizens only where an intact edifice actually flipped to ruin.','A power-kept unruled site with no intact edifice to flip does not lose its denizens through this step.'],'source_references':refs})
s['questions'].append({'id':'Q104','question':question,'fixed_key_expected_answer_sha256':hashlib.sha256(expected.encode()).hexdigest(),'source_references':refs,
 'asked_clause_map':[{'clause_id':'Q104-C01','asked_clause':'Does the given retained/unruled site without an intact edifice lose denizens in this step, and what event triggers this discard?','required_fact_ids':['Q104-F01'],'rationale':'One actual-flip trigger determines both the negative case and requested operation.'}],
 'required_facts':[{'fact_id':'Q104-F01','expected_fact':'No denizen discard through this ruining step in the given case: it occurs only at sites where an intact edifice actually flipped to ruin, not merely because a site is retained and unruled.','basis':'Law8.3.3 exact guard, independently discovered source06 finding'}],
 'contextual_exclusions':[{'key_or_source_fact':'Named Forest Temple recall, full site-disposal destinations, other possible power instructions and subsequent map packing','classification':'contextual_not_independently_required','rationale':'The question supplies retention and asks the actual-flip guard for this one step.','contradiction_policy':'Omission not penalized; any volunteered materially false universal claim still incorrect.'}],
 'contextual_exclusion_status':'No named-card recall or unrelated Chronicle recital required.','semantic_notes':'The site is already retained; apply the present ruining-step condition. Do not infer a discard from lack of winner rule alone. Equivalent complete meaning accepted.'})
s['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();s['inputs']['questions']='expanded-v11/questions.json';s['inputs']['fixed_key']='expanded-v11/answer-key.json'
s['preparation_disclosure']='New source06 P2 finding corrects the general Chronicle actual-flip guard. Q046 expected wording/F03 receive source precision; Q104 independently tests the negative power-retained/no-flip branch outside Q046’s retained-intact fixture. All103 prior questions and other102 keys preserved, all other326 prior required-fact groups unchanged. Frozen before new blind reader dispatch; no Q104 response exists.'
assert q['questions'][:103]==J(P/'expanded-v10/questions.json')['questions']
for a,b in zip(k['answers'],J(P/'expanded-v10/answer-key.json')['answers']):
 if a['id']!='Q046':assert a==b
for a,b in zip(s['questions'],J(P/'expanded-v10/grading-scope.json')['questions']):
 if a['id']!='Q046':assert a==b
 else:
  assert a['asked_clause_map']==b['asked_clause_map'] and a['contextual_exclusions']==b['contextual_exclusions']
  for x,y in zip(a['required_facts'],b['required_facts']):
   if x['fact_id']!='Q046-F03':assert x==y
W(V/'questions.json',q);W(V/'answer-key.json',k);W(V/'grading-scope.json',s)
W(V/'key-corrections.json',[{'id':'Q046','old':old_expected,'new':entry['expected_answer'],'material_fact_clause_old':old_clause,'material_fact_clause_new':new_clause,'required_fact_change':{'fact_id':'Q046-F03','old':old_scope,'new':new_scope},'source':'Law8.3.3; independent source06 P2 finding','reason':'The guard is actual intact-to-ruin flipping, not mere retention without winner rule. Original Q046 intact-edifice fixture’s outcome is unchanged; the negative branch is separately Q104.','old_versions_and_grades_preserved':True}])
W(V/'input-manifest.json',{f:H(V/f) for f in ['questions.json','answer-key.json']})
inputs=[V/'questions.json',V/'answer-key.json',P/'expanded-v10/grading-scope.json',P/'expanded-iteration-06/source-audit.json',Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-law.txt')]
W(V/'grading-scope-manifest.json',{'artifact_type':'grading-scope SHA256 freeze manifest','benchmark_version':'expanded-v11','created_utc':s['created_utc'],'scope_artifact':{'path':str((V/'grading-scope.json').resolve()),'sha256':H(V/'grading-scope.json')},'input_files':[{'path':str(f.resolve()),'sha256':H(f)} for f in inputs],'required_fact_count':328,'question_count':104,'one_Q046_fact_group_precision_corrected':True,'all_other326_prior_fact_groups_unchanged':True,'frozen_before_reader_dispatch':True})
text=['# Oath expanded benchmark v11','','104 retained questions. Q104 covers the no-flip Chronicle branch exposed by a source-audit error; Q046’s guard is made precise. Q104 novelty credit is provisional pending independent challenge; existing historical overlaps retain zero credit. All103 previous question words/IDs remain unchanged.','']
for a,b in zip(q['questions'],k['answers']):text+=['## '+a['id'],'',a['question'],'','**Answer:** '+b['expected_answer'],'','**Source:** '+b['source_references'],'']
(V/'question-bank.md').write_text('\n'.join(text))
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-before-v11.json');l=J(P/'coverage-ledger.json')
l['accepted_questions'].append({'id':'Q104','accepted':True,'source_references':[refs],'novelty':'Negative actual-flip guard: Q046 explicitly asks retained sites with intact edifices; this supplied-power case has no intact edifice and no flip. No named-card recall.','novelty_credit':'PROVISIONAL_1; independent reviewer may reject credit while retaining regression','source_discovery':'source06 audit; reviewer must not read audit/candidate text'})
l['coverage_map']['Law8.3.3 actual-flip guard, power-retained no-flip branch']=['Q046','Q104']
l['passes'] += [{'pass':29,'focus':'Repair actual Chronicle source defect; append no-flip negative regression outside retained-intact fixture','count':1,'accepted_ids':['Q104'],'novelty_credit':'provisional pending independent challenge'}, {'pass':30,'focus':'Reopen all Law8/Playbook Chronicle steps and attachment transitions after exact actual-flip guard repair','count':0,'accepted_ids':[],'rejections':[{'candidate':'A different card name or another retained-site/no-flip arrangement','reason':'Q104 supplies the retention effect and tests the generic trigger; substitutions add no rule.'}]}, {'pass':31,'focus':'Reopen all other complete source procedural maps, all Site Reference and errata after orientation/guard precision','count':0,'accepted_ids':[],'rejections':[{'candidate':'Additional setup-orientation, dice/force or phase-power permutations','reason':'Existing explicit generic operators and first/later setup clauses already test them; no new source-defined branch.'}]}]
l['stopping_rule']={'consecutive_zero_addition_passes':2,'passes':[30,31],'all_core_procedural_passages_mapped':True,'independent_challenge':{'verdict':'PENDING','report':'coverage-review-10.json','provisional_Q104_novelty_requires_review':True}}
W(P/'coverage-ledger.json',l);shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-reviewed-10.json')
W(V/'freeze-manifest.json',{'question_count':104,'required_fact_group_count':328,'historical_overlap_count':10,'Q104_novelty_credit':'provisional pending independent challenge','all_prior103_question_entries_unchanged':True,'hashes':{f:H(V/f) for f in ['questions.json','answer-key.json','grading-scope.json']}})
D=P/'expanded-iteration-07';D.mkdir(exist_ok=False);shutil.copyfile('/home/jonny/projects/boardgame-rules/rules/oath-chronicles-of-empire-and-exile.md',D/'summary-snapshot.md');shutil.copyfile(V/'questions.json',D/'questions.json')
m=J(P/'expanded-iteration-06/input-manifest.json');m['benchmark_version']='expanded-v11';m['hashes']={a.replace('expanded-iteration-06','expanded-iteration-07').replace('expanded-v10','expanded-v11'):h for a,h in m['hashes'].items()}
for a in m['hashes']:m['hashes'][a]=H(Path(a))
W(D/'input-manifest.json',m);(D/'build-grading-package.py').write_text((P/'expanded-iteration-06/build-grading-package.py').read_text().replace('expanded-v10','expanded-v11'))
W(D/'summary-changes.json',{'previous_prepared_snapshot':'expanded-iteration-06/summary-snapshot.md','sha256':H(D/'summary-snapshot.md'),'source_defect_repaired':'source06 P2; retained site denizen discard conditional on actual intact-to-ruin flip','additional_general_clarifications':['Bandit plans must have no cost; no waiver of costs','Bandit Crown last-physical-warband pickup exception in Minor actions','First/later regional discard seeds explicitly facedown'],'reader_feedback_not_supplied_to_fresh_agents':True,'no_test_numeric_example_inserted':True,'verification_banner_unchanged':True})
print('Frozen v11/iteration07:104 questions,328 fact groups;',H(D/'summary-snapshot.md'))
