from pathlib import Path
import difflib,hashlib,json
B=Path(__file__).resolve().parent
ROOT=B.parents[4]
P=ROOT/'rules/spirit-island.md'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
HS=lambda s:hashlib.sha256(s.encode()).hexdigest()
load=lambda p:json.loads(p.read_text())
assert H(P)==H(B/'source-candidate-26.md')=='ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1'
assert load(B/'expanded-iteration-07/completed-trial-adoption.json')['trial_status']=='COMPLETED_DELIVERY_QUALIFIED_FACTUAL_FAILURE'
old=P.read_text()
heading='### Damage, Destroy, Remove, Replace and Defend\n\n'
overview="""Use the named operation to determine what happens to the piece:

| Instruction | Effect on the piece |
| --- | --- |
| **Damage** | Mark Damage; reaching Health destroys the piece immediately. |
| **Destroy** | Return the specified piece to supply regardless of Health or marked Damage. |
| **Remove** | Take the specified piece off the board without a Damage-to-Health test. |
| **Replace** | Remove the original piece and put the specified new piece in its place, retaining marked Damage. |

"""
changes=[('operation_comparison_overview',heading,heading+overview,['core_operation','core_glossary','faq_health']),('drowning_action_vs_completed_tree',"Humans cannot stay there between action trees: if Drowning fails, Push survivors to non-Ocean lands within that action. This is an actual Push and can trigger applicable movement effects, unlike later cleanup.","If a Drowning action fails to destroy its humans, **that same Drowning action** Pushes survivors to non-Ocean lands. This actual Push can trigger applicable movement effects; resolve the action and its triggers before completing the action tree. Humans cannot stay in the Ocean between action trees.",['faq_failed_drowning','faq_illegal_cleanup']),('posttree_cleanup_direct',"This post-action-tree correction uses the cleanup procedure below.","At this post-action-tree stage, apply cleanup directly; the failed-Drowning Push belongs to the earlier action.",['faq_failed_drowning','faq_illegal_cleanup'])]
core=ROOT/'extracted/spirit-island-rules.txt'
faq=ROOT/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island/living-faq-core-game.txt'
sources={}
for name,path,start,end,first,last,chunk in [
('core_operation',core,45000,51000,'DAMAGE, DESTRUCTION, AND REMOVAL','DEFEND','05c4ae'),
('core_glossary',core,85000,90000,'Remove: Take off the board','Sacred Site (','4eea3b'),
('faq_health',faq,20000,24000,'When an effect reduces the Health','Under a Spirit's Play Style','f1b940'),
('faq_failed_drowning',faq,186500,192500,'What happens if 1 or more Invaders/Dahan moved into the Ocean','If Bringer of Dreams and Nightmares does shadow damage','a4d8c3'),
('faq_illegal_cleanup',faq,58000,64000,"What happens if a piece winds up in a place or state it's not allowed to be?",'If an Event or Fear Card has multiple instructions','601b48')]:
 s=path.read_text();a=s.index(first,start,end);z=s.index(last,a,end);sources[name]={'path':str(path),'full_sha256':H(path),'range':[a,z],'literal_passage':s[a:z],'passage_sha256':HS(s[a:z]),'actual_parent_full_window_read':{'range':[start,end],'slice_sha256':HS(s[start:end]),'output_cap_tokens':4000,'truncated':False,'exec_command_chunk_id':chunk,'one_literal_range_per_actual_output_event':True}}
new=old
for name,before,after,refs in changes:
 assert new.count(before)==1 and before!=after
 new=new.replace(before,after)
assert new.split('---',2)[1]==old.split('---',2)[1]
back=new
for _,before,after,_ in reversed(changes):
 assert back.count(after)==1
 back=back.replace(after,before)
assert back==old
bank={n:H(B/'expanded-v24'/n) for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json']}
candidate=B/'source-candidate-27.md'
assert not candidate.exists()
candidate.write_text(new)
record={'candidate':str(candidate),'candidate_sha256':H(candidate),'canonical_not_yet_changed':True,'previous_candidate_sha256':H(B/'source-candidate-26.md'),'characters':len(new),'bytes':candidate.stat().st_size,'change_count':len(changes),'changes':[{'id':n,'old':a,'new':z,'primary_source_citations':refs} for n,a,z,refs in changes],'added_characters':len(new)-len(old),'exact_reverse_reconstruction_PASS':True,'yaml_unchanged':True,'new_rule_or_procedure_claimed':False,'new_novelty_credit':0,'bespoke_question_ids_or_case_number_answers_added':False,'bank_key_map_scope_bytes_unchanged':bank,'no_reader_resampling_or_threshold_change':True,'new_fresh_pure_source_audit_and_full173_pair_mandatory':True,'source15_C26_PASS_historical_only_after_body_change':True}
(B/'source-candidate-27-change-record.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
(B/'source-candidate-27-clarity-primary-evidence.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
(B/'source-candidate-27-changes.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='source-candidate-26.md',tofile='source-candidate-27.md')))
print(json.dumps({'candidate_sha256':H(candidate),'characters':len(new),'bytes':candidate.stat().st_size,'added_characters':len(new)-len(old),'changes':len(changes),'canonical_not_changed':True}))
