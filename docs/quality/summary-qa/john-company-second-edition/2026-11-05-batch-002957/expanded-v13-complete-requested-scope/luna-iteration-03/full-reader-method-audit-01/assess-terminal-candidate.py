import sys
sys.dont_write_bytecode=True
import pathlib,json,hashlib,re,datetime
P=pathlib.Path(__file__).parent;I=P.parent;O=P/sys.argv[1];role=sys.argv[2];H=lambda b:hashlib.sha256(b).hexdigest()
ns={'__name__':'literal_checker_audit'};exec(compile((I/'source-unit-checker.py').read_text(),str(I/'source-unit-checker.py'),'exec'),ns)
q=json.loads((I/'questions.json').read_text())['questions'];s=(I/'summary-snapshot.md').read_text()
d=json.loads((O/f'prefix-reader-{role}-draft.json').read_text());f=json.loads((O/f'prefix-reader-{role}.json').read_text());sc=json.loads((O/f'prefix-reader-{role}-self-check.json').read_text());records=sc.get('checks',sc.get('records'));projection=json.loads((O/f'prefix-reader-{role}-runtime-projection.json').read_text());trace=json.loads((O/'prefix-audit.json').read_text())['readers'][role]
literal=ns['check_data'](s,q,f,role);(O/'final-literal-checks.json').write_text(json.dumps(literal,indent=2)+'\n')
dm={e['id']:e for e in d['answers']};fm={e['id']:e for e in f['answers']};changed=[qid for qid in dm if dm[qid]!=fm.get(qid)]
review=f.get('self_review',f.get('self-review'));first=P/f'first-observed-complete-{role}-draft.json';firstmatch=H(first.read_bytes())==H((O/f'prefix-reader-{role}-draft.json').read_bytes())if first.exists()else None
copies=[]
for folder in sorted((I/'bounded-turn-history').glob(f'reader-{role}-turn-*')):
 mp=folder/'manifest.json';m=json.loads(mp.read_text())
 if m.get('ordered_prefix')!=116:continue
 cp=folder/f'reader-{role}-draft.json'
 if cp.exists():copies.append({'manifest_path':str(mp),'manifest_sha256':H(mp.read_bytes()),'draft_path':str(cp),'draft_sha256':H(cp.read_bytes()),'same_as_frozen_draft':H(cp.read_bytes())==H((O/f'prefix-reader-{role}-draft.json').read_bytes()),'same_as_own_first_observed_complete':H(cp.read_bytes())==H(first.read_bytes())if first.exists()else None})
perentry=json.loads((O/f'prefix-reader-{role}-per-entry-method.json').read_text());last=next((e['first_successful_composition_append_call']for e in perentry if e['id']==q[-1]['id']),None)
postcalls=[{'physical_record':c['physical_record'],'call_id':c['call_id'],'tool_call_sha256':H(c['input'].encode())}for c in projection['tool_calls']if last and c['physical_record']>last]
recordmap={e['id']:e for e in records};alignment=[]
for e in f['answers']:
 r=recordmap.get(e['id'],{});alignment.append({'id':e['id'],'map_aligned':r.get('clause_map',r.get('clause_to_unit_map'))==e['clause_ledger'],'metadata_aligned':r.get('selected_source_metadata')==e['operative_sections']})
result={'role':role,'assessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'draft_count':len(d['answers']),'final_count':len(f['answers']),'source_record_count':len(records),'final_exact_ordered_unique_116_ids':literal['exact_ordered_unique_ids'],'final_structure_flag':literal['all_structure_and_declared_source_spans_valid'],'all_final_case_arrays_plain_strings':all(isinstance(e.get('case_conclusions'),list)and all(isinstance(c,str)for c in e['case_conclusions'])for e in f['answers']),'actual_changed_ids_from_first_frozen_complete_draft':changed,'actual_changed_fields':{qid:[k for k in sorted(set(dm[qid])|set(fm[qid]))if dm[qid].get(k)!=fm[qid].get(k)]for qid in changed},'final_self_review':review,'source_record_final_alignment':alignment,'first_observed_complete_draft_copy':str(first)if first.exists()else None,'first_observed_complete_matches_frozen_preserved_draft':firstmatch,'authorized_parent_complete_snapshot_copies':copies,'first_actual_complete_append_call':last,'post_complete_call_hashes_for_manual_draft_write_inspection':postcalls,'actual_last_runtime_event':projection['task_events'][-1],'full_trace_method':trace,'manual_draft_preservation_trace_verdict':'Pending inspection of the allowlisted post-complete calls.','qualified_full_final_response_fact_grading_admission':'Pending manual terminal review and root confirmation of actual whole-task termination.','limits':'No factual conclusions, semantic coverage rulings or score caps. A complete final and source-only trace can support qualified strict response grading despite retained procedural/format/history-note qualifications.'}
(O/'terminal-assessment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k in ['role','draft_count','final_count','source_record_count','final_exact_ordered_unique_116_ids','final_structure_flag','all_final_case_arrays_plain_strings','actual_changed_ids_from_first_frozen_complete_draft','final_self_review','first_observed_complete_matches_frozen_preserved_draft','authorized_parent_complete_snapshot_copies','first_actual_complete_append_call','actual_last_runtime_event']},indent=2))
