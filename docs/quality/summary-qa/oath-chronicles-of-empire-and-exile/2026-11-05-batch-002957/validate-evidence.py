from pathlib import Path
import json,hashlib,collections,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[4]
# P is root/docs/quality/summary-qa/slug/run, so root is parents[4].
assert (ROOT/'rules').is_dir(),ROOT
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p:json.loads(p.read_text())
checks={};errors=[]
def check(label,condition,detail=None):
 checks[label]={'pass':bool(condition),'detail':detail}
 if not condition:errors.append(label)
for source,h in J(P/'source-input-manifest.json').items():check('source_unchanged:'+source,H(ROOT/source)==h)
for source,h in J(P/'supplemental-source-manifest.json').items():check('supplemental_source_unchanged:'+source,H(Path(source))==h)
for bank in ['seed-v1','expanded-v1','expanded-v2','expanded-v3','expanded-v4','expanded-v5','expanded-v6','expanded-v7','expanded-v8','expanded-v9','expanded-v10','expanded-v11']:
 d=P/bank
 if not d.exists():continue
 for f,h in J(d/'input-manifest.json').items():check(bank+':frozen_hash:'+f,H(d/f)==h)
 q=J(d/'questions.json')['questions'];k=J(d/'answer-key.json')['answers'];ids=[v['id'] for v in q]
 check(bank+':unique_question_ids',len(ids)==len(set(ids)))
 check(bank+':key_ids',ids==[v['id'] for v in k])
 if bank=='expanded-v1':
  check(bank+':original_questions',q[:20]==J(P/'seed-v1/questions.json')['questions'])
  check(bank+':original_answers',k[:20]==J(P/'seed-v1/answer-key.json')['answers'])
 if bank=='expanded-v2':
  oq=J(P/'expanded-v1/questions.json')['questions'];ok=J(P/'expanded-v1/answer-key.json')['answers'];changes={v['id']:v for v in J(d/'key-corrections.json')}
  check(bank+':all_prior_questions_preserved',q[:len(oq)]==oq)
  for old,new in zip(ok,k):
   if old['id'] in changes:check(bank+':explicit_key_correction:'+old['id'],old['expected_answer']==changes[old['id']]['old'] and new['expected_answer']==changes[old['id']]['new'])
   else:check(bank+':unchanged_prior_key:'+old['id'],old==new)
 if bank=='expanded-v3':
  check(bank+':all_prior_questions_preserved',q[:92]==J(P/'expanded-v2/questions.json')['questions'])
  check(bank+':all_prior_answers_preserved',k[:92]==J(P/'expanded-v2/answer-key.json')['answers'])
 if bank=='expanded-v4':
  check(bank+':all_prior_questions_preserved',q[:93]==J(P/'expanded-v3/questions.json')['questions'])
  check(bank+':all_prior_answers_preserved',k[:93]==J(P/'expanded-v3/answer-key.json')['answers'])
 if bank=='expanded-v5':
  check(bank+':all_prior_questions_preserved',q[:95]==J(P/'expanded-v4/questions.json')['questions'])
  old=J(P/'expanded-v4/answer-key.json')['answers'];changes={v['id']:v for v in J(d/'key-corrections.json')}
  for a,b in zip(old,k):
   if a['id'] in changes:check(bank+':explicit_key_correction:'+a['id'],a['expected_answer']==changes[a['id']]['old'] and b['expected_answer']==changes[a['id']]['new'])
   else:check(bank+':unchanged_prior_key:'+a['id'],a==b)
 if bank=='expanded-v6':
  check(bank+':all_prior_questions_preserved',q[:100]==J(P/'expanded-v5/questions.json')['questions'])
  check(bank+':all_prior_answers_preserved',k[:100]==J(P/'expanded-v5/answer-key.json')['answers'])
  scope=J(d/'grading-scope.json');sm=J(d/'grading-scope-manifest.json')
  check(bank+':scope_frozen_hash',H(d/'grading-scope.json')==sm['scope_artifact']['sha256'])
  check(bank+':all_prior_scope_entries_preserved',scope['questions'][:100]==J(P/'expanded-v5/grading-scope.json')['questions'])
  check(bank+':all_scope_ids',[x['id'] for x in scope['questions']]==ids)
  check(bank+':fact_count',sum(len(x['required_facts']) for x in scope['questions'])==320)
  for x in sm['input_files']:check(bank+':scope_input:'+x['path'],H(Path(x['path']))==x['sha256'])
 if bank=='expanded-v7':
  check(bank+':all_prior_questions_preserved',q[:101]==J(P/'expanded-v6/questions.json')['questions'])
  check(bank+':all_prior_answers_preserved',k[:101]==J(P/'expanded-v6/answer-key.json')['answers'])
  scope=J(d/'grading-scope.json');sm=J(d/'grading-scope-manifest.json')
  check(bank+':scope_frozen_hash',H(d/'grading-scope.json')==sm['scope_artifact']['sha256'])
  check(bank+':all_prior_scope_entries_preserved',scope['questions'][:101]==J(P/'expanded-v6/grading-scope.json')['questions'])
  check(bank+':all_scope_ids',[x['id'] for x in scope['questions']]==ids)
  check(bank+':fact_count',sum(len(x['required_facts']) for x in scope['questions'])==327)
  for x in sm['input_files']:check(bank+':scope_input:'+x['path'],H(Path(x['path']))==x['sha256'])
 if bank in ['expanded-v8','expanded-v9']:
  prior=P/('expanded-v7' if bank=='expanded-v8' else 'expanded-v8')
  check(bank+':all_question_entries_unchanged',q==J(prior/'questions.json')['questions'])
  oldkeys=J(prior/'answer-key.json')['answers'];correction=J(d/'key-corrections.json')[0]
  for a,b in zip(k,oldkeys):
   if a['id']!='Q015':check(bank+':unchanged_prior_key:'+a['id'],a==b)
   elif bank=='expanded-v8':check(bank+':recorded_key_precision_correction',b['expected_answer']==correction['old'] and a['expected_answer']==correction['new'])
   else:check(bank+':recorded_duplicate_field_alignment',b['material_facts'][0]==correction['old'] and a['material_facts'][0]==correction['new'] and a['expected_answer']==b['expected_answer'] and a['material_facts'][1:]==b['material_facts'][1:])
  scope=J(d/'grading-scope.json');sm=J(d/'grading-scope-manifest.json');previous=J(prior/'grading-scope.json')
  check(bank+':scope_frozen_hash',H(d/'grading-scope.json')==sm['scope_artifact']['sha256'])
  check(bank+':required_fact_count',sum(len(x['required_facts']) for x in scope['questions'])==327)
  for a,b in zip(scope['questions'],previous['questions']):
   check(bank+':prior_required_facts_clauses_exclusions:'+a['id'],a['required_facts']==b['required_facts'] and a['asked_clause_map']==b['asked_clause_map'] and a['contextual_exclusions']==b['contextual_exclusions'])
   key=next(x for x in k if x['id']==a['id']);check(bank+':scope_key_hash:'+a['id'],a['fixed_key_expected_answer_sha256']==hashlib.sha256(key['expected_answer'].encode()).hexdigest())
  if bank=='expanded-v9':check(bank+':all_prior_scope_entries_unchanged',scope['questions']==previous['questions'])
  for x in sm['input_files']:check(bank+':scope_input:'+x['path'],H(Path(x['path']))==x['sha256'])
 if bank in ['expanded-v10','expanded-v11']:
  prior=P/('expanded-v9' if bank=='expanded-v10' else 'expanded-v10');oldq=J(prior/'questions.json')['questions'];oldk=J(prior/'answer-key.json')['answers'];olds=J(prior/'grading-scope.json')['questions'];scope=J(d/'grading-scope.json');sm=J(d/'grading-scope-manifest.json');correction=J(d/'key-corrections.json')[0]
  check(bank+':all_prior_questions_preserved',q[:len(oldq)]==oldq)
  corrected_id='Q025' if bank=='expanded-v10' else 'Q046'
  for a,b in zip(k,oldk):
   if a['id']!=corrected_id:check(bank+':unchanged_prior_key:'+a['id'],a==b)
   elif bank=='expanded-v10':
    check(bank+':exact_source_expected_correction',a['expected_answer']==correction['expected_answer_change']['new'] and b['expected_answer']==correction['expected_answer_change']['old'])
    for change in correction['material_fact_changes']:
     i=change['index_1_based']-1;check(bank+':material_correction:'+str(i),a['material_facts'][i]==change['new'] and b['material_facts'][i]==change['old'])
   else:
    check(bank+':exact_source_expected_correction',a['expected_answer']==correction['new'] and b['expected_answer']==correction['old'])
    check(bank+':structured_guard_corrected',correction['material_fact_clause_old'] not in json.dumps(a) and correction['material_fact_clause_new'] in a['material_facts'][0])
  changes={x['fact_id']:x for x in correction['required_fact_changes']} if bank=='expanded-v10' else {correction['required_fact_change']['fact_id']:correction['required_fact_change']}
  for a,b in zip(scope['questions'],olds):
   check(bank+':clause_exclusion_preservation:'+a['id'],a['asked_clause_map']==b['asked_clause_map'] and a['contextual_exclusions']==b['contextual_exclusions'])
   for x,y in zip(a['required_facts'],b['required_facts']):
    if x['fact_id'] in changes:
     c=changes[x['fact_id']];check(bank+':documented_fact_precision:'+x['fact_id'],x['expected_fact']==c['new'] and y['expected_fact']==c['old'])
    else:check(bank+':unchanged_fact:'+x['fact_id'],x==y)
  check(bank+':scope_frozen_hash',H(d/'grading-scope.json')==sm['scope_artifact']['sha256'])
  check(bank+':scope_count',sum(len(x['required_facts']) for x in scope['questions'])==sm['required_fact_count'])
  check(bank+':scope_ids',[x['id'] for x in scope['questions']]==ids)
  for x in scope['questions']:
   kk=next(y for y in k if y['id']==x['id']);check(bank+':scope_key_hash:'+x['id'],hashlib.sha256(kk['expected_answer'].encode()).hexdigest()==x['fixed_key_expected_answer_sha256'])
   check(bank+':clause_fact_map:'+x['id'],{i for c in x['asked_clause_map'] for i in c['required_fact_ids']}=={f['fact_id'] for f in x['required_facts']})
  for x in sm['input_files']:check(bank+':scope_input:'+x['path'],H(Path(x['path']))==x['sha256'])
# Separately versioned requested-scope precision; source-correct key/question text is unchanged.
precise=P/'grading-scope-v12'
if precise.exists():
 scope12=J(precise/'grading-scope.json');scope11=J(P/'expanded-v11/grading-scope.json')
 changes={x['id']:x for x in J(precise/'precision-changes.json')['changes']}
 for path,h in J(precise/'freeze-manifest.json')['files'].items():check('scopev12:frozen:'+path,H(Path(path))==h)
 check('scopev12:all_fact_IDs_and_count',[[f['fact_id'] for f in x['required_facts']] for x in scope12['questions']]==[[f['fact_id'] for f in x['required_facts']] for x in scope11['questions']] and sum(len(x['required_facts']) for x in scope12['questions'])==328)
 for a,b in zip(scope12['questions'],scope11['questions']):
  if a['id'] in changes:
   c=changes[a['id']];check('scopev12:exact_independently_recommended:'+a['id'],a==c['new'] and b==c['old'])
  else:check('scopev12:unchanged_row:'+a['id'],a==b)
scopepath=P/'expanded-v5/grading-scope.json'
if scopepath.exists():
 scope=J(scopepath);sm=J(P/'expanded-v5/grading-scope-manifest.json');check('expanded_scope_frozen_hash',H(scopepath)==sm['scope_artifact']['sha256'])
 for x in sm['input_files']:check('expanded_scope_input:'+x['path'],H(Path(x['path']))==x['sha256'])
 sq=scope['questions'];ek={x['id']:x for x in J(P/'expanded-v5/answer-key.json')['answers']};eq=J(P/'expanded-v5/questions.json')['questions']
 check('expanded_scope_ids',[x['id'] for x in sq]==[x['id'] for x in eq])
 for x in sq:
  check('expanded_scope_key:'+x['id'],hashlib.sha256(ek[x['id']]['expected_answer'].encode()).hexdigest()==x['fixed_key_expected_answer_sha256'])
  factids={f['fact_id'] for f in x['required_facts']};mapped={i for c in x['asked_clause_map'] for i in c['required_fact_ids']}
  check('expanded_scope_clauses:'+x['id'],factids==mapped and len(factids)==len(x['required_facts']))
 check('expanded_scope_fact_count',sum(len(x['required_facts']) for x in sq)==sm['required_fact_count'])
for d in sorted(P.glob('*iteration-*')):
 if not d.is_dir() or not (d/'questions.json').exists():continue
 q=J(d/'questions.json');ids=[v['id'] for v in q['questions']];bank=P/q['benchmark_version'];key=J(bank/'answer-key.json');km={v['id']:v for v in key['answers']};qm={v['id']:v['question'] for v in q['questions']}
 check(d.name+':question_copy_matches',H(d/'questions.json')==H(bank/'questions.json'))
 for p,h in J(d/'input-manifest.json').get('hashes',{}).items():check(d.name+':frozen_input:'+p,H(Path(p))==h)
 readers={}
 for who in ['a','b']:
  f=d/f'reader-{who}.json'
  if not f.exists():continue
  r=J(f);rs=r['answers'];readers['reader-'+who]={v['id']:v for v in rs};rid=[v['id'] for v in rs]
  check(d.name+':reader_'+who+'_ids',collections.Counter(rid)==collections.Counter(ids))
  allowed={str((d/'summary-snapshot.md').resolve()),str((d/'questions.json').resolve())}
  declared=r.get('inputs_read')
  if not declared:
   ri=r['inputs']
   if isinstance(ri,list):declared=[x['path'] if isinstance(x,dict) else x for x in ri]
   elif 'paths' in ri:declared=ri['paths']
   elif 'summary_path' in ri:declared=[ri['summary_path'],ri['questions_path']]
   else:declared=[x['path'] for x in ri.values()]
  normalized={str((Path(v) if Path(v).is_absolute() else ((d/v) if '/' not in v else (ROOT/v))).resolve()) for v in declared}
  check(d.name+':reader_'+who+'_allowed_inputs',normalized==allowed,{'declared':declared,'normalized':sorted(normalized)})
 if (d/'results.json').exists():
  result=J(d/'results.json')
  for rr in result['readers']:
   name=rr['reader'];grades=rr['questions'];check(d.name+':'+name+':grade_ids',collections.Counter(v['id'] for v in grades)==collections.Counter(ids))
   totals=collections.Counter(v['grade'] for v in grades)
   check(d.name+':'+name+':totals',all(totals[g]==rr['totals'][g] for g in ['correct','partial','incorrect']))
   for g in grades:
    id=g['id'];observed=g['observed_answer']
    if isinstance(observed,dict) and (d/'grading-input.json').exists():
     # Some graders retain the whole lossless transport entry as their observation.
     transported=next(x for x in J(d/'grading-input.json')['questions'] if x['id']==id)['readers'][name]
     observation_matches=observed==transported
    else:observation_matches=observed==readers[name][id]['answer']
    check(d.name+':'+name+':record_integrity:'+id,g['question']==qm[id] and g['expected_answer_from_fixed_key']==km[id]['expected_answer'] and observation_matches)
 check(d.name+':snapshot_exists',(d/'summary-snapshot.md').is_file())
 validation={'checks':{k:v for k,v in checks.items() if k.startswith(d.name+':')},'pass':not any(not v['pass'] for k,v in checks.items() if k.startswith(d.name+':'))}
 (d/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
# Targeted repository checks, read-only.
validation=subprocess.run([str(ROOT/'.venv/bin/python'),'-m','scripts.validate','rules/oath-chronicles-of-empire-and-exile.md'],cwd=ROOT,text=True,capture_output=True)
check('targeted_structural_validation',validation.returncode==0,validation.stdout+validation.stderr)
diff=subprocess.run(['git','diff','--check','--','rules/oath-chronicles-of-empire-and-exile.md',str(P.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
check('targeted_diff_check',diff.returncode==0,diff.stdout+diff.stderr)
summary=(ROOT/'rules/oath-chronicles-of-empire-and-exile.md').read_text()
check('new_summary_no_trailing_whitespace',all(line==line.rstrip() for line in summary.splitlines()))
check('new_summary_no_merge_markers',not any(line.startswith(('<<<<<<<','=======','>>>>>>>')) for line in summary.splitlines()))
# Metadata minimization is checked independently against untouched external records.
if (P/'provenance-metadata-redaction-manifest.json').exists():
 privacy_check=subprocess.run([str(ROOT/'.venv/bin/python'),str(P/'validate-provenance.py')],cwd=ROOT,text=True,capture_output=True)
 check('minimal_actual_runtime_metadata_and_redaction_chain',privacy_check.returncode==0,privacy_check.stdout+privacy_check.stderr)
out={'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,'scope':'Only this worker summary/evidence; no shared regeneration,stamping,catalog mutation or global audit claim.'}
(P/'validation-in-progress.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(checks),'checks',errors[:8])
