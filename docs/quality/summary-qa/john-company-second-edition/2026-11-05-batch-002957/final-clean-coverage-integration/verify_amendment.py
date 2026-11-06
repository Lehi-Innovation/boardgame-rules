from pathlib import Path
import json,hashlib,datetime
b=Path(__file__).parent.parent;v=b/'expanded-v10-complete-user-scope';o=Path(__file__).parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
canonical=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
orig=json.loads((v/'answer-key.json').read_text());rev=json.loads((v/'answer-key-revision-01.json').read_text());scope=json.loads((v/'requested-fact-scope-reviewed.json').read_text());qs=json.loads((v/'questions.json').read_text());baseline=json.loads((o/'input-hashes.json').read_text());first=json.loads((o/'entry-validation.json').read_text())
oldmap={x['id']:x for x in orig['answers']};newmap={x['id']:x for x in rev['answers']};scopemap={x['id']:x for x in scope['questions']}
expected_ids=[f'Q{i:03}' for i in range(1,94)]
changed=[i for i in expected_ids if oldmap[i]!=newmap[i]]
assert changed==['Q007']
assert newmap['Q007']['expected_answer']==oldmap['Q007']['expected_answer'].replace('Commit office treasury money/resources,','Commit office treasury money/resources (pay cash to the bank),',1)
assert newmap['Q007']['source_references']=='Rules p17; lines 1330–1365; cash destination physical-LF lines1348–1349.'
assert all(orig[k]==rev[k] for k in orig if k!='answers')
assert set(rev)-set(orig)=={'key_revision'}
unchanged={name:h(v/name)==baseline[str(v/name)]['sha256'] for name in ['questions.json','answer-key.json','grading-scope.json','requested-fact-scope-reviewed.json']}
assert all(unchanged.values())
assert [x['id'] for x in qs['questions']]==[x['id'] for x in rev['answers']]==[x['id'] for x in scope['questions']]==expected_ids
assert all(canonical(scopemap[row['id']])==row['scope_sha256'] for row in first['entry_hashes'])
assert 'pay office cash to bank' in scopemap['Q007']['material_requested_facts'][0]
paths=[v/x for x in ['questions.json','answer-key.json','answer-key-revision-01.json','grading-scope.json','requested-fact-scope-reviewed.json','source-key-amendment-01.json']]+[Path('/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt')]
hashes={str(p):{'sha256':h(p),'bytes':p.stat().st_size} for p in paths}
other92=[{'id':i,'original_key_sha256':canonical(oldmap[i]),'revised_key_sha256':canonical(newmap[i]),'equal':oldmap[i]==newmap[i]} for i in expected_ids if i!='Q007']
rows93=[{'id':i,'current_scope_sha256':canonical(scopemap[i]),'initial_observed_scope_sha256':next(x['scope_sha256'] for x in first['entry_hashes'] if x['id']==i),'equal':True} for i in expected_ids]
report={
 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'review_kind':'Independent source/key amendment verification, separate from preserved initial report',
 'final_source_key_integration_disposition':'SUPPORTED_WITH_KEY_REVISION_01_WITHIN_ASSIGNED_SCOPE',
 'finding':'The Q007 representation omission identified independently in the initial integration report is resolved by answer-key-revision-01.json. The frozen prospective checklist already made cash-to-bank material; the amendment completes the key representation without adding or changing a grading requirement. No unresolved material source/key integration issue was found in this amendment verification.',
 'resolved_initial_issue':'ALIGN-Q007',
 'frozen_requirement_proof':{
  'question_id':'Q007',
  'question':scopemap['Q007']['question'],
  'material_requested_facts_before_and_after':scopemap['Q007']['material_requested_facts'],
  'exact_preexisting_payment_requirement':scopemap['Q007']['material_requested_facts'][0],
  'contextual_key_extras':scopemap['Q007']['contextual_key_extras'],
  'classification':'Bank destination was already expressly material, not a newly promoted contextual extra.',
  'temporal_basis':'The assignment designates this as the PRE-READER frozen checklist. Independently, its entire-file SHA-256 and all93 row hashes are identical to the baseline recorded in my earlier source/key integration check before this amendment. No reader output, score, history or freeze/status manifest was inspected to establish or modify this finding.'
 },
 'source_verification':{'source':'extracted/john-company-second-edition-rules.txt','page':17,'physical_LF_lines':[1344,1353],'operative_lines':[1348,1349],'finding':'The original passage expressly says money spent comes from the office treasury and is paid to the bank. The amendment is accurate and the more precise source reference points to that passage.'},
 'exact_change_proof':{
  'changed_answer_ids':changed,
  'Q007_changed_fields':['expected_answer','source_references'],
  'expected_answer_change':{'original':oldmap['Q007']['expected_answer'],'revised':newmap['Q007']['expected_answer'],'exact_single_insertion':' (pay cash to the bank)'},
  'source_reference_change':{'original':oldmap['Q007']['source_references'],'revised':newmap['Q007']['source_references']},
  'Q007_other_fields_exact':all(oldmap['Q007'][k]==newmap['Q007'][k] for k in oldmap['Q007'] if k not in ['expected_answer','source_references']),
  'all_other92_key_entries_exact':all(x['equal'] for x in other92),
  'unchanged_root_fields':['benchmark_version','grading_standard','grading_scope'],
  'only_added_root_field':'key_revision',
  'added_root_metadata':rev['key_revision'],
  'all93_id_sequences_exact':True,
  'all93_per_question_scope_rows_exact_against_initial_baseline':True,
  'all93_question_wording_and_entire_questions_file_exact':True,
  'full_file_baseline_unchanged':unchanged,
  'original88_preservation_boundary':'The original frozen answer-key.json is unchanged and retains its original88 entries exactly. The revised key intentionally changes Q007 expected text and source reference, so do not describe the revised first88 key entries as byte-for-byte or entry-for-entry identical to original88. The other87 retained entries and five added entries are exact.'
 },
 'grading_requirement_changed':False,
 'question_or_per_question_scope_changed':False,
 'summary_check_boundary':'No summary was opened. The amendment record states the summary was unchanged; that file assertion was not independently re-inspected because the summary is outside the allowed source/key read set.',
 'remaining_issues':{'material_source_key_integration_issues':[],'additional_distinct_questions_required':[],'nonblocking_carried_note':'The initial report’s Q006 former-Chairman threshold-announcement scope precision note remains advisory. The source’s “should declare” announcement need not become a separate grading demand; the substantive majority threshold and election rules are already represented.'},
 'coverage_and_authority_boundary':'This disposition carries forward the independent five-topic source/fact matrix and coverage/case checks from the preserved initial report, with its one material Q007 key representation issue now resolved. It is source/key integration evidence within official multiplayer/all standard scenarios/firms plus attributed user >= defense scope. It is not a reader grade, a publication decision, an independently verified publisher-email claim, or a guarantee over every possible recombination.',
 'other92_key_entry_hash_proof':other92,
 'all93_scope_row_hash_proof':rows93,
 'input_hashes':hashes,
 'process_record':{
  'newly_allowed_inputs':['expanded-v10-complete-user-scope/answer-key-revision-01.json','expanded-v10-complete-user-scope/source-key-amendment-01.json'],
  'displayed_q_key_entries':['Q007 original','Q007 revised'],
  'displayed_scope_entries':['Q007 material facts/context/source fields'],
  'source_text_lines_displayed':[1344,1353],
  'other_file_reads':'Original allowed questions/key/grading-scope/checklist and own prior hash/entry-validation derivatives for exact comparisons. Amendment declaration inspected but its assertions independently tested rather than accepted as proof.',
  'excluded_reader_summary_grade_results_files_opened':False,
  'status_session_history_tools_called':False,
  'other_agents_contacted':False,
  'reader_feedback_used':False,
  'freeze_manifest_opened':False,
  'output_truncation':False,
  'source_and_q_key_display_bounds_respected':True,
  'frozen_inputs_edited':False,
  'initial_report_preserved':True
 }
}
(o/'key-amendment-verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
lines=[
 '# Independent key amendment verification',
 '',
 '**Final source/key integration disposition: supported with answer-key revision01 within assigned scope.** Q007’s independently discovered representation omission is resolved. No unresolved material integration issue was found in this verification.',
 '',
 'The frozen Q007 material checklist already states: “Commit office resources and pay office cash to bank, gather dice then subtract penalty.” Its contextual extras are empty. Cash-to-bank was therefore already a material grading requirement. The amendment completes the expected-answer representation; it does not add a new requirement or promote an unasked extra.',
 '',
 'Rules p17, physical-LF lines1348–1349 explicitly state that cash spent comes from the office treasury and is paid to the bank. The revised key inserts only “ (pay cash to the bank)” into Q007’s expected text and adds the precise source-line reference. Its remaining fields are exact. All other92 answer entries are exact. Root benchmark, grading standard and grading scope are unchanged; the sole new root field is a descriptive key_revision string.',
 '',
 'The entire questions, original answer key, grading-scope and requested-fact checklist files retain the exact SHA-256 hashes recorded in the initial independent check. Every one of the93 scope-row hashes matches that initial baseline. All question/key/scope sequences remain Q001–Q093. The assignment supplies the pre-reader freeze chronology; no reader outputs, grades, status/history tools or freeze manifest were inspected. The checklist independently observed before this amendment is byte-identical now.',
 '',
 'Preservation boundary: original answer-key.json remains untouched and preserves original88 exactly. Revision01 deliberately differs at Q007, so its first88 answer entries should not be described as entirely identical to original88. Its other87 retained entries and five added entries are exact. No question or per-question scope changed. The summary was not opened; its unchanged state is asserted by the amendment record, not independently re-inspected here.',
 '',
 'The initial five-topic source/fact findings and source/case boundaries remain in the preserved source-key-integration report. Its Q006 threshold-announcement precision note remains nonblocking; the advisory source declaration should not become a separate grading demand. No new distinct consequential question is required by this amendment.',
 '',
 '| Input | SHA-256 |','|---|---|'
]
for p,info in hashes.items():lines.append(f'| {Path(p).name} | `{info["sha256"]}` |')
lines+=['','The JSON companion contains exact other92-key and all93-scope row hash proofs, the original/revised Q007 text, input hashes and read record. The initial report and frozen inputs were preserved.','']
(o/'key-amendment-verification.md').write_text('\n'.join(lines))
print('Wrote separate key-amendment-verification.json/.md')
print(report['final_source_key_integration_disposition'])
print('Other92 key entries exact:',report['exact_change_proof']['all_other92_key_entries_exact'])
print('All93 scopes exact: True; grading requirement changed: False')
print('verification.json SHA256',h(o/'key-amendment-verification.json'))
print('verification.md SHA256',h(o/'key-amendment-verification.md'))
