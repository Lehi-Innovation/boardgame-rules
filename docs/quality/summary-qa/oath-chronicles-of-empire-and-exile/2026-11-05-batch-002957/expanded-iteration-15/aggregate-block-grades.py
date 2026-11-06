from pathlib import Path
import collections,copy,hashlib,json
D=Path(__file__).resolve().parent
J=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def validation_passed(v):
 def bools(x):
  if isinstance(x,bool):return [x]
  if isinstance(x,dict):return [b for z in x.values() for b in bools(z)]
  if isinstance(x,list):return [b for z in x for b in bools(z)]
  return []
 if v.get('status') in ['passed','PASS']:return True
 checked=bools(v.get('checks',{}))+bools(v.get('reader_checks',{}))+bools(v.get('raw_equality_checks',{}))
 return v.get('status')=='complete' and v.get('valid',True) is True and bool(checked) and all(checked) and not v.get('errors')
m=J(D/'grading-block-manifest.json');full=J(D/'grading-input.json');records={q['id']:q for q in full['questions']};ids=list(records)
raw={f'reader-{w}':{q['id']:q for q in J(D/f'reader-{w}.json')['answers']} for w in ['a','b']};merged={r:{} for r in raw};findings=[];proofs=[];checks={};errors=[]
def check(name,value):
 checks[name]=bool(value)
 if not value:errors.append(name)
def strings(x):
 if isinstance(x,str):yield x
 elif isinstance(x,dict):
  for v in x.values():yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
 else:yield str(x)
check('summary_frozen',H(D/'summary-snapshot.md')==m['summary_sha256'])
for x in m['original_input_hashes']:check('input_hash:'+x['path'],H(Path(x['path']))==x['sha256'])
for b in m['blocks']:
 bd=Path(b['directory']);r=J(bd/'results.json');bv=J(bd/'grading-validation.json');bp=J(bd/'losslessness.json');key=b['block_id'];check(key+':packet_frozen',H(bd/'packet.json')==b['packet_sha256']==bp['packet_sha256']);check(key+':full_raw_reconstruction',bp['both_complete_original_raw_entries_reconstructed_exactly']);check(key+':independent_validation',validation_passed(bv))
 check(key+':two_readers',len(r['readers'])==2 and {x['reader'] for x in r['readers']}==set(raw));check(key+':declared_entries',r['questions_graded']==2*b['question_count']);check(key+':declared_facts',r['fact_assessments']==2*b['required_fact_groups_per_reader'])
 for f in r.get('gold_or_scope_defects',[]):findings.append({'block_id':key,'original_finding':f})
 for rr in r['readers']:
  who=rr['reader'];grades=rr['questions'];check(key+':IDs:'+who,[g['id'] for g in grades]==b['question_ids']);ct=collections.Counter(g['grade'] for g in grades);check(key+':totals:'+who,all(ct[g]==rr['totals'][g] for g in ['correct','partial','incorrect']))
  for grade in grades:
   id=grade['id'];tag=key+':'+who+':'+id;expect=records[id];original=raw[who][id]
   check(tag+':no_duplicate',id not in merged[who]);check(tag+':question',grade['question']==expect['question']);check(tag+':key',grade['expected_answer_from_fixed_key']==expect['fixed_expected_answer']);check(tag+':raw_answer',grade['observed_answer']==original['answer']);facts=grade['fact_checks'];check(tag+':all_exact_facts',[(x['fact_id'],x['expected_fact']) for x in facts]==[(x['fact_id'],x['expected_fact']) for x in expect['required_facts']]);check(tag+':grade_enum',grade['grade'] in ['correct','partial','incorrect'])
   if grade['grade']=='correct':check(tag+':all_correct_facts_satisfied',all(f['status']=='satisfied' for f in facts))
   source_texts=list(strings(original))+[json.dumps(original,ensure_ascii=False),json.dumps(original,ensure_ascii=False,separators=(',',':'))]
   for fact in facts:
    ft=tag+':'+fact['fact_id'];check(ft+':status',fact['status'] in ['satisfied','missing','contradicted']);check(ft+':evidence_if_satisfied',fact['status']!='satisfied' or bool(fact.get('evidence')))
    for n,e in enumerate(fact.get('evidence',[])):
     excerpt=e.get('excerpt','');check(ft+':literal_evidence:'+str(n),bool(excerpt) and any(excerpt in t for t in source_texts))
     sp=e.get('span_if_quote')
     if isinstance(sp,dict) and 'start' in sp and 'end' in sp:check(ft+':literal_span:'+str(n),excerpt in (D/'summary-snapshot.md').read_text()[sp['start']:sp['end']])
   merged[who][id]=copy.deepcopy(grade)
 proofs.append({'block_id':key,'agent_name':b['agent_name'],'result_path':str(bd/'results.json'),'result_sha256':H(bd/'results.json'),'packet_sha256':H(bd/'packet.json'),'question_ids':b['question_ids'],'fact_groups_per_reader':b['required_fact_groups_per_reader'],'validation_sha256':H(bd/'grading-validation.json')})
check('manifest_disjoint_full104_IDs',[i for b in m['blocks'] for i in b['question_ids']]==ids);check('manifest_full328_fact_groups',sum(b['required_fact_groups_per_reader'] for b in m['blocks'])==328)
readers=[]
for who,byid in merged.items():
 check('full104_no_missing_or_extra:'+who,set(byid)==set(ids));ordered=[byid[i] for i in ids];ct=collections.Counter(q['grade'] for q in ordered);readers.append({'reader':who,'totals':{g:ct[g] for g in ['correct','partial','incorrect']},'questions':ordered})
check('actual208_entry_count',sum(len(r['questions']) for r in readers)==208);check('actual656_fact_count',sum(len(g['fact_checks']) for r in readers for g in r['questions'])==656)
validation={'status':'passed' if not errors else 'FAIL','method':'Mechanical aggregation only; each semantic judgment and finding is preserved byte-for-value from its fresh independent block grader.','questions_graded':208,'fact_assessments':656,'checks':checks,'errors':errors,'blocks':proofs}
(D/'grading-validation.json').write_text(json.dumps(validation,indent=2)+'\n')
if errors:
 print('FAIL',errors);raise SystemExit(1)
result={'benchmark_version':'expanded-v11','grading_scope_version':'scope-v12','iteration':15,'status':'complete','method':'Six fresh independent Sol/high none graders, disjoint fixed 18/18/18/18/18/14-question blocks, both entire original entries per ID, entire current frozen summary per grader. Root aggregates without changing any question grade/fact assessment/evidence/finding. No cross-entry/cross-reader borrowing.','questions_graded':208,'fact_assessments':656,'inputhashes':{x['path']:x['sha256'] for x in m['original_input_hashes']},'blocks':proofs,'readers':readers,'gold_or_scope_defects':findings}
(D/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
lines=['# Iteration15 disjoint independent grading','', 'All block-level judgments and findings remain in their original directories; this file aggregates them without semantic edits.','']
for r in readers:
 lines.append(f"{r['reader']}: {r['totals']}");lines.append('')
 for q in r['questions']:
  if q['grade']!='correct':lines.append(f"- {q['id']} — {q['grade']}: {q['reason']}")
 lines.append('')
(D/'adjudication.md').write_text('\n'.join(lines)+'\n')
print('AGGREGATED',[(r['reader'],r['totals']) for r in readers],'all208/656; all findings retained')
