from pathlib import Path
import json,hashlib,sys,collections
q=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(label,value):checks.append({'check':label,'passed':bool(value)});assert value,label
root=json.loads((q/'input-manifest.json').read_text());check('baseline summary preserved',H(q/'baseline-summary.md')==root['files'][0]['sha256'])
for x in root['files'][1:]:check('source unchanged '+x['path'],H(Path(x['path']))==x['sha256'])
baseq=json.loads((q/'benchmark-v1/questions.json').read_text())['questions'];basek=json.loads((q/'benchmark-v1/answer-key.json').read_text())['answers']
for b in sorted(q.glob('benchmark-v*')):
 manifest=json.loads((b/'frozen-hashes.json').read_text())
 for name,digest in manifest.items():check(str(b.name+'/'+name)+' frozen hash',H(b/name)==digest)
 qs=json.loads((b/'questions.json').read_text())['questions'];keys=json.loads((b/'answer-key.json').read_text())['answers'];check(b.name+' original 20 question entries identical',qs[:20]==baseq)
 if int(b.name.rsplit('v',1)[1])>=17:
  expected17=json.loads((q/'benchmark-v17/answer-key.json').read_text())['answers'][:20]
  check(b.name+' original20 keys preserved except explicit source-qualifiedv17 Q17',keys[:20]==expected17 and all(a==c for a,c in zip(expected17,basek) if a['id']!='Q17'))
 else:check(b.name+' original 20 key entries identical',keys[:20]==basek)
 check(b.name+' question IDs unique',len(set(x['id'] for x in qs))==len(qs));check(b.name+' key IDs match', [x['id'] for x in qs]==[x['id'] for x in keys])
if (q/'benchmark-v4').exists():
 for kind,field in [('questions','questions'),('answer-key','answers')]:
  prev=json.loads((q/f'benchmark-v3/{kind}.json').read_text())[field];now=json.loads((q/f'benchmark-v4/{kind}.json').read_text())[field]
  check('v4 all 73 surviving v3 '+kind+' entries identical',now[:73]==[x for x in prev if x['id']!='Q59'])
versions=sorted(int(p.name.rsplit('v',1)[1]) for p in q.glob('benchmark-v*'))
for prevnum,nextnum in zip(versions,versions[1:]):
 if (prevnum,nextnum)==(3,4):continue
 if (prevnum,nextnum)==(16,17):
  oldqs=json.loads((q/'benchmark-v16/questions.json').read_text())['questions'];newqs=json.loads((q/'benchmark-v17/questions.json').read_text())['questions']
  oldkeys=json.loads((q/'benchmark-v16/answer-key.json').read_text())['answers'];newkeys=json.loads((q/'benchmark-v17/answer-key.json').read_text())['answers'];corrections=json.loads((q/'benchmark-v17/source-key-corrections.json').read_text())['corrections'];independent=json.loads((q/'contract-availability-independent-source-key-coverage.json').read_text())
  check('v17 all101 actual question objects unchanged',newqs==oldqs and len(newqs)==101)
  check('v17 only Q17/Q46 keyentries explicitly source-qualified',[a['id'] for a,c in zip(oldkeys,newkeys) if a!=c]==['Q17','Q46'])
  for c in corrections:
   prior=next(x for x in oldkeys if x['id']==c['id']);now=next(x for x in newkeys if x['id']==c['id']);r=next(x for x in independent['key_corrections'] if x['id']==c['id'])
   check('v17 '+c['id']+' exact before/after and independently proposed complete expectedstring',prior==c['before'] and now==c['after'] and prior['expected_answer']==r['original_expected_answer'] and now['expected_answer']==r['proposed_complete_expected_answer'])
  check('v17 independent availability review no new mandatory question',not independent['genuine_additions'] and independent['verdict']['new_question_count_recommended']==0)
  proof=json.loads((q/'contract-availability-review-input-read-integrity.json').read_text());imageproof=json.loads((q/'contract-availability-review-primary-image-read-integrity.json').read_text())
  check('v17 source correction reviewer actual complete rawprimaries/whole101Q/key/image',proof['all_authorized_sources_and_bank_key_visible'] and imageproof['original_leader_image_returned_to_agent'])
  continue
 if (prevnum,nextnum)==(15,16):
  for kind,field in [('questions','questions'),('answer-key','answers')]:
   old=json.loads((q/f'benchmark-v15/{kind}.json').read_text())[field];new=json.loads((q/f'benchmark-v16/{kind}.json').read_text())[field]
   check('v16 preserves all101 surviving v15 '+kind+' entries exactly',new==[x for x in old if x['id']!='Q103'])
  continue
 prev=q/f'benchmark-v{prevnum}';nxt=q/f'benchmark-v{nextnum}'
 if not prev.exists() or not nxt.exists():continue
 for kind,field in [('questions','questions'),('answer-key','answers')]:
  old=json.loads((prev/f'{kind}.json').read_text())[field];new=json.loads((nxt/f'{kind}.json').read_text())[field]
  check(f'v{nextnum} preserves all v{prevnum} '+kind+' entries',new[:len(old)]==old)
if (q/'benchmark-v16').exists():
 novelty=json.loads((q/'q103-independent-novelty-review.json').read_text());proof=json.loads((q/'q103-novelty-input-read-integrity.json').read_text())
 check('Q103 independent whole-bank novelty retirement',novelty['verdict']=='retire' and not novelty['strict_procedural_novelty'])
 check('Q103 reviewer actual complete101 bank/key and original image',proof['all101_prior_questions_and_keys_visible'] and proof['original_leader_image_returned_to_agent'])
 check('Q103 retired before any prepared13 reader output',not any((q/'expanded-iteration-13'/f'reader-{r}.json').exists() for r in 'ab'))
if (q/'expanded-iteration-15/q19-policy-resolution.md').exists():
 isolated=json.loads((q/'expanded-iteration-15/q19a-isolated-adjudication.json').read_text());proof=json.loads((q/'expanded-iteration-15/q19a-input-read-integrity.json').read_text())
 check('Final A19 isolated same-key scope review correct/no unsupported guess',isolated['grade']=='correct' and not isolated['unsupported_guess'])
 check('Final A19 isolated reviewer actual complete summary/case input',proof['all324_summary_lines_and_complete_isolated_case_visible'])
 metas=[x for x in json.loads((q/'model-provenance.json').read_text()) if x['agent_path']=='/root/expanded15_q19a_isolated']
 check('One actual NEW isolated A19 reviewer',len(metas)==1)
 for x in metas:
  check('Isolated A19 reviewer Sol/high fresh context',x['fork_turns']=='none' and all(z['model']=='gpt-6.1-sol' and z['effort']=='high' for z in x['turn_contexts']))
iterations=[];answer_count=0
for d in sorted(q.glob('*iteration-*')):
 if not d.is_dir():continue
 m=json.loads((d/'input-manifest.json').read_text());qs=json.loads((d/'questions.json').read_text())['questions'];keys=json.loads((q/m['benchmark']/'answer-key.json').read_text())['answers'];ids=[x['id'] for x in qs]
 check(d.name+' questions unchanged',H(d/'questions.json')==H(q/m['benchmark']/'questions.json'))
 check(d.name+' snapshot frozen',H(d/'summary-snapshot.md')==m['files'][str(d/'summary-snapshot.md')]);check(d.name+' key unchanged',H(q/m['benchmark']/'answer-key.json')==m['files'][str(q/m['benchmark']/'answer-key.json')])
 if 'grading_boundary_snapshot' in m:
  policy=m['grading_boundary_snapshot'];check(d.name+' pre-reader grading-boundary snapshot frozen',H(Path(policy['path']))==policy['sha256'])
 if not (d/'results.json').exists():iterations.append({'iteration':d.name,'status':'not-graded'});continue
 results=json.loads((d/'results.json').read_text());scores={}
 for r in ['a','b']:
  raw=json.loads((d/f'reader-{r}.json').read_text())['answers'];grades=results['readers'][r]['grades'];answer_count+=len(raw)
  check(d.name+' reader '+r+' every expected ID exactly once',collections.Counter(x['id'] for x in raw)==collections.Counter(ids));check(d.name+' grades '+r+' every ID once',collections.Counter(x['id'] for x in grades)==collections.Counter(ids))
  for grade in grades:
   orig=next(x for x in raw if x['id']==grade['id']);key=next(x for x in keys if x['id']==grade['id']);quest=next(x for x in qs if x['id']==grade['id'])
   check(d.name+r+grade['id']+' grade quotes exact raw answer and fixed question/key',grade['observed']==orig and grade['expected']==key['expected_answer'] and grade['question']==quest['question'])
  scores[r]={g:sum(x['grade']==g for x in grades) for g in ['correct','partial','incorrect']};check(d.name+r+' totals match',scores[r]==results['readers'][r]['totals'])
 iterations.append({'iteration':d.name,'n':len(ids),'status':'graded','scores':scores,'summary_sha256':H(d/'summary-snapshot.md')})
final=sys.argv[1] if len(sys.argv)>1 else None
if final:
 if final=='expanded-iteration-17' and (q/final/'q61-isolated-adjudication.json').exists():
  resolution=q/final/'q61-policy-resolution.json'
  check('Final17 Q61 isolated/full-grader semantic conflict resolved before handoff',resolution.exists() and json.loads(resolution.read_text()).get('resolved_for_handoff',False))
 d=q/final;check('final canonical byte-identical to tested snapshot',d.joinpath('summary-snapshot.md').read_bytes()==Path('/home/jonny/projects/boardgame-rules/rules/dune-imperium-uprising.md').read_bytes())
 res=json.loads((d/'results.json').read_text());n=len(json.loads((d/'questions.json').read_text())['questions'])
 for r in ['a','b']:
  read_audit=json.loads((d/f'reader-{r}-input-read-audit.json').read_text())
  check('final '+r+' complete visible summary and all question texts',read_audit['all_summary_lines_and_question_texts_visible_in_reads'])
  check('final '+r+' N/N zero partial incorrect',res['readers'][r]['totals']=={'correct':n,'partial':0,'incorrect':0});check('final '+r+' no unsupported guess',not any(x['unsupported_guess'] for x in res['readers'][r]['grades']))
 metadata=json.loads((d/'model-provenance.json').read_text());check('two final fresh reader runtime identities',len(metadata)==2 and len({x['session_id'] for x in metadata})==2)
 for x in metadata:check('runtime Luna/high '+x['agent_path'],all(t['model']=='gpt-6-luna' and t['effort']=='high' for t in x['turn_contexts']))
 for x in metadata:check('final reader requested fresh context '+x['agent_path'],x['fork_turns']=='none')
 benchmark=json.loads((d/'input-manifest.json').read_text())['benchmark'];version=benchmark.rsplit('-',1)[1]
 coverage=json.loads((q/('coverage-final-independent-'+version+'.json')).read_text())
 coverage_complete=coverage.get('complete_in_scope_procedural_coverage', coverage.get('verdict',{}).get('complete_in_scope_procedural_coverage',False) if isinstance(coverage.get('verdict'),dict) else False)
 check('NEW final bank challenger certifies complete scoped procedural coverage',coverage_complete)
 check('NEW final bank challenger has no genuine additions',not coverage['genuine_additions'])
 coverage_reads=json.loads((q/benchmark/'coverage-input-read-integrity.json').read_text())
 check('NEW final bank challenger actual complete source/bank/key reads',coverage_reads['all_authorized_sources_and_bank_key_visible'])
 if int(version[1:])>=14:
  check('NEW final bank challenger actual original printed Leader image read',json.loads((q/benchmark/'primary-image-read-integrity.json').read_text())['original_leader_image_returned_to_agent'])
 covmeta=[x for x in json.loads((q/'model-provenance.json').read_text()) if x['agent_path']=='/root/coverage_final_independent_'+version]
 check('one actual NEW final bank challenger',len(covmeta)==1)
 for x in covmeta:
  check('final bank challenger requested fresh context',x['fork_turns']=='none')
  check('final bank challenger actual Sol/high',all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in x['turn_contexts']))
 appendix=json.loads((q/benchmark/'source-reference-appendix.json').read_text())
 questions=json.loads((q/benchmark/'questions.json').read_text())['questions']
 check('complete authoritative corrected locator supplement covers all final question IDs', [x['id'] for x in appendix['references']]==[x['id'] for x in questions])
 for entry in appendix['references']:
  check('corrected locators exist '+entry['id'],bool(entry['corrected_authoritative_source_references']))
  for ref in entry['corrected_authoritative_source_references']:
   f=Path(ref['file']);check('corrected source fingerprint '+entry['id']+f.name,H(f)==ref['sha256'])
   if 'lines' in ref:
    start,end=ref['lines'];check('corrected exact source line range '+entry['id']+f.name,1<=start<=end<=len(f.read_text().splitlines()))
if final and int(json.loads((q/final/'input-manifest.json').read_text())['benchmark'].rsplit('v',1)[1])>=17:
 scope_resolution=json.loads((q/'expanded-iteration-20/q46-policy-resolution.json').read_text())
 if (q/'expanded-iteration-22/q14-policy-resolution.json').exists():
  q14=json.loads((q/'expanded-iteration-22/q14-policy-resolution.json').read_text());q14proof=json.loads((q/'expanded-iteration-22/q14-isolated-input-read-integrity.json').read_text())
  check('Coordinator-requested Q14 contextual semantic scope resolved and accepted',q14['resolved_for_handoff'] and q14['coordinator_explicitly_accepted'])
  check('Q14 isolated report remains exact',H(Path(q14['scope_report_path']))==q14['scope_report_sha256'])
  check('Q14 isolated actualcomplete348summary andwholeexactcase',q14proof['all348_summary_lines_and_complete_isolated_case_visible'])
  check('Q14 isolated actualNEW Sol/high/forknone',q14proof['fork_turns']=='none' and all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in q14proof['actual_models']))
 if int((q/final).name.rsplit('-',1)[1])>=23:
  q60=json.loads((q/'expanded-iteration-23/q60-policy-resolution.json').read_text());q60proof=json.loads((q/'expanded-iteration-23/q60-isolated-input-read-integrity.json').read_text())
  check('Requested single Q60 neutral actual-scope review resolved for candidate handoff',q60['resolved_for_handoff'] and q60['both_Q60_correct'] and q60['coordinator_explicitly_accepted'])
  check('Q60 isolated report exact',H(Path(q60['scope_report_path']))==q60['scope_report_sha256'])
  check('Q60 isolated actualcomplete359summary andexactwholecase',q60proof['all359_summary_lines_and_complete_isolated_case_visible'])
  check('Q60 isolated actualNEW Sol/high/forknone',q60proof['fork_turns']=='none' and all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in q60proof['actual_models']))
 check('Coordinator-requested Q46 exact-case scope boundary resolved',scope_resolution['resolved_for_handoff'])
 check('Q46 scope report exact and explicitly coordinator-accepted',scope_resolution['coordinator_explicitly_accepted'] and H(Path(scope_resolution['new_independent_scope_report_path']))==scope_resolution['scope_report_sha256'])
 scopeproof=json.loads((q/'expanded-iteration-20/q46-isolated-input-read-integrity.json').read_text())
 check('Q46 isolated actual complete330summary and exactwholecase',scopeproof['all330_summary_lines_and_complete_isolated_case_visible'])
 check('Q46 isolated actual NEW Sol/high/forknone',scopeproof['fork_turns']=='none' and all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in scopeproof['actual_models']))
 if 'grading_scope_addendum' in json.loads((q/final/'input-manifest.json').read_text()):
  annex=json.loads((q/final/'input-manifest.json').read_text())['grading_scope_addendum']
  check('Prospective scope addendum frozen before final fullgrader and not readeraccessible',H(Path(annex['path']))==annex['sha256'] and annex['before_NEW_fullgrader_dispatch'] and annex['reader_access'] is False)
 resolution=json.loads((q/'shaddam-empty-public-playability-resolution.json').read_text())
 check('Own-empty-public case remains inside full adopted CHOAM scope',not resolution['scope_shrunk'])
 check('Own-empty-public independent source/playability criterion completed',not resolution['assessment_pending'])
 check('Full-scope source-supported legal procedure established without essential unresolved ruling',resolution['core_playability_established'] is True and resolution['essential_unresolved'] is False)
 check('Source/playability report remains exact',H(Path(resolution['assessment_path']))==resolution['assessment_sha256'])
 playability=json.loads(Path(resolution['assessment_path']).read_text())
 check('Source/playability assessor finds no essential unresolved point',all(x['essential_to_legal_play'] is False for x in playability['unresolved_matters']))
 playabilityproof=json.loads((q/'shaddam-empty-public-input-read-integrity.json').read_text());playabilityimage=json.loads((q/'shaddam-empty-public-primary-image-read-integrity.json').read_text())
 check('Source/playability assessor actual complete original primaries and Leader image',playabilityproof['all_authorized_primary_texts_visible'] and playabilityimage['original_leader_image_returned_to_agent'])
 meta=[x for x in json.loads((q/'model-provenance.json').read_text()) if x['agent_path']=='/root/shaddam_empty_public_playability']
 check('One NEW independent source/playability assessor',len(meta)==1)
 for x in meta:check('Source/playability actual Sol/high/forknone',x['fork_turns']=='none' and all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in x['turn_contexts']))
if final:
 source_dir=q/final
 if (source_dir/'source-audit-reference.json').exists():
  reference=json.loads((source_dir/'source-audit-reference.json').read_text());source_dir=q/reference['audit_iteration']
  check('Coordinator-authorized exact-byte source-audit reuse snapshot equality',source_dir.joinpath('summary-snapshot.md').read_bytes()==(q/final/'summary-snapshot.md').read_bytes() and H(source_dir/'summary-snapshot.md')==reference['audited_snapshot_sha256']==reference['new_snapshot_sha256'])
  check('Referenced actual fresh source audit unchanged',H(source_dir/'source-audit.json')==reference['source_audit_sha256'])
  check('No fictitious new source auditor claimed',reference.get('no_new_source_auditor_claimed',reference.get('no_new_source17_auditor_claimed',False)))
 audit=json.loads((source_dir/'source-audit.json').read_text());check('fresh final source verdict PASS',audit['verdict']=='PASS')
 sources=json.loads((source_dir/'source-audit-input-read-integrity.json').read_text());check('final source auditor complete primary texts and exact summary',sources['all_authorized_primary_texts_and_summary_visible'])
 if int(source_dir.name.rsplit('-',1)[1])>=12:
  check('fresh final auditor actual original printed Leader image read',json.loads((source_dir/'primary-image-read-integrity.json').read_text())['original_leader_image_returned_to_agent'])
 provenance=json.loads((source_dir/'source-audit-model-provenance.json').read_text());check('one actual fresh final source auditor',len(provenance)==1)
 for x in provenance:check('runtime source Sol/high',all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in x['turn_contexts']))
 for x in provenance:check('final source auditor requested fresh context',x['fork_turns']=='none')
 grading=json.loads((q/final/'independent-full-grading.json').read_text())
 grading_reads=json.loads((q/final/'independent-grader-input-read-integrity.json').read_text())
 check(f'final independent full grader actual complete summary/questions/key rulings/{n*2} answers/evidence',grading_reads['all_summary_questions_key_rulings_and_both_answers_evidence_visible'])
 grading_meta=[x for x in json.loads((q/'model-provenance.json').read_text()) if x['agent_path']=='/root/expanded'+final.rsplit('-',1)[1]+'_full_grader']
 check('one actual NEW independent full grader',len(grading_meta)==1)
 for x in grading_meta:
  check('independent full grader requested fresh context',x['fork_turns']=='none')
  check('independent full grader actual Sol/high',all(t['model']=='gpt-6.1-sol' and t['effort']=='high' for t in x['turn_contexts']))
report={'all_checks_passed':all(x['passed'] for x in checks),'checked_answer_count':answer_count,'iterations':iterations,'checks':checks,'final_iteration':final,'scope':('Targeted game and QA directory evidence revalidated after explicit coordinator integration. Final canonical remains exact tested/audited bytes; coordinator validation separately confirms registry/publication/catalog checks.' if json.loads((q/'game-status.json').read_text()).get('coordinator_integration_verified') else 'Targeted game and QA directory only. Coordinator owns shared catalog checks/stamping; these are pending until explicit integration follow-up.')}
(q/('validation.json' if final else 'validation-progress.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print({'checks':len(checks),'answers':answer_count,'pass':report['all_checks_passed']})
