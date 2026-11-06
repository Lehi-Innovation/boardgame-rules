import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
R=HERE.parent
A=R/'final-stamped-source-audit-01'
F=R/'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
    b=Path(p).read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def read(p):return json.loads(Path(p).read_text())
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
summary=read(HERE/'runtime-summary.json')
native=read(HERE/'native-reproduction-receipts.json')
delivery=read(HERE/'text-delivery-receipts.json')
images=read(HERE/'image-delivery-receipts.json')
hashes=read(HERE/'file-hash-verification.json')
manifest=read(A/'manifest.json')
report=read(A/'source-audit.json')
original_index=read(A/'original-hashes.json')
projection=[json.loads(l) for l in (HERE/'runtime-allowlisted-projection.jsonl').read_text().split('\n') if l]
baseline=read(HERE/'unchanged-baseline.json')
after=[{**bind(p),'before_sha256':expected,'unchanged':bind(p)['sha256']==expected} for p,expected in baseline.items()]
save('unchanged-after-verification.json',after)
assert all(x['unchanged'] for x in after)
assert all(x['verified'] for x in delivery)
assert all(x['exact_derivative_bytes_match'] and x['before_verdict_writer'] for x in images)
assert all(x['requested_path_matches_declared_derivative'] for x in images)
assert all(x['sha256_matches'] and x['bytes_match'] for x in hashes)
assert all(x['matches_derivative'] and x['matches_existing_derivative_bytes'] and x['matches_original_binding'] for x in native['receipts'])
assert all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in summary['contexts'])
coverage={}
for alias in ['candidate','rules']:
    delivered=set()
    for receipt in delivery:
        if receipt['alias']==alias and receipt['verified']:
            delivered.update(range(receipt['start_lf'],receipt['end_lf']+1))
    required=set(range(1,500)) if alias=='candidate' else set(range(1,3016))|set(range(3290,3307))
    coverage[alias]={'required_count':len(required),'missing_lf':sorted(required-delivered),'complete':required<=delivered}
assert all(x['complete'] for x in coverage.values())
calls={x['record']:x for x in projection if x.get('kind')=='tool_call'}
def script(record):
    s=calls[record]['input']
    return json.JSONDecoder().raw_decode(s[s.index('cmd:')+4:])[0]
written=script(265).split("<<'PY'\n",1)[1].rsplit('\nPY\n',1)[0]+'\n'
writer_matches=written==(A/'write_reports.py').read_text()
assert writer_matches
versions=[]
for name in ['source-audit.json','source-audit.md','source-read-record.json']:
    version=name.replace('.json','-v1.json').replace('.md','-v1.md')
    versions.append({'report':bind(A/name),'version':bind(A/version),'byte_identical':(A/name).read_bytes()==(A/version).read_bytes()})
lookup={x['path']:x for x in [manifest['candidate']]+manifest['originals']}
original_index_matches=all(x['path'] in lookup and x['sha256']==lookup[x['path']]['sha256'] and x['bytes']==lookup[x['path']]['bytes'] for x in original_index.values())
assert original_index_matches and len(original_index)==18 and all(v['byte_identical'] for v in versions)
io_review=[
 {'call_records':[18,23,30,37],'classification':'Candidate/source indexing and helper construction in assigned output; first two initialization attempts failed. No substantive foreign game data.','observed_paths':'Candidate and exact original17 paths, assigned directory.'},
 {'call_records':[42,47,52,57,62,67,72,81,86,91,96,101,106,114,121,128],'classification':'Exact numbered original/candidate text delivery and basic PDF-tool discovery.','evidence':'text-delivery-receipts.json'},
 {'call_records':[135,142,149,154,161,170],'classification':'Disclosed dependency/setup IO, including /usr/bin tool checks, Python module discovery, library filename search, bundled runtime discovery, failed network pip, failed Windows Python, approved escalated pip install. This is not game-source research.','paths':['/usr/bin/pdftoppm','/usr/bin/pdftotext','/usr/bin/pdfinfo','/usr/bin/mutool','/usr/local/lib','/opt','/home/jonny/.local/lib','/mnt/c/Users/jonny/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',str(A/'runtime')],'network_qualification':'Record145 has DNS/network failures for /simple/pymupdf/. Record173 reports cached PyMuPDF1.28.2 wheel metadata and wheel, successful installation. Package/cache/network infrastructure IO exists; trace is not an OS syscall or network capture.'},
 {'call_records':[177,184,189,198,206,215,222,229,236,245,254],'classification':'Native original PDF rendering/extraction, permitted resource-section indexing, own derivative reads and 12 image deliveries. Rendering source and inline extra-render programs manually inspected.','evidence':['native-reproduction-receipts.json','image-delivery-receipts.json']},
 {'call_records':[265],'classification':'Manually authored literal report construction; 81 literal claim rows and reasons, empty findings and PASS literals. Loops attach references and serialize; they do not infer gameplay truth.','evidence':'verdict-writer-tool-program.txt','writer_matches_manifest_bound_script':writer_matches},
 {'call_records':[272],'classification':'Writes source-read/visual metadata and manifest; hashes original17 and own output/runtime tree. Updates Bridge printed-sheet labels.','output_record':275},
 {'call_records':[281],'classification':'Read-only final assertions of existing report, coverage declarations, hashes and version equality. Does not update manifest and does not independently establish source accuracy.','output_record':284}
]
assert set(calls)=={n for g in io_review for n in g['call_records']}
limitations=[
 'The dispatched plaintext explicitly requests a fresh independent source auditor, fork_turns=none and gpt-6.1-sol/high. Its exact bytes are bound. In this permitted runtime, the incoming /root-to-auditor task envelope at record13 includes an encrypted part and only a 93-byte plaintext wrapper. The substantive encrypted task body was not inspected or retained. Exact dispatch-to-actual-prompt equality and actual fork_turns=none are therefore not independently proven by this projection.',
 'Observed tool programs and outputs establish permitted game-data IO; they do not establish every implicit dependency, package installer, cache, dynamic-library or operating-system syscall. There was disclosed setup/network activity. No claim of a network-free or infrastructure-path-free run is made.',
 'Completion and transport verification does not prove the auditor cognitively assessed every delivered claim or that its gameplay conclusion is correct. The existing qualified source verdict is preserved without regrading.',
 'Only 12 PNGs actually reached the auditor as native image payloads; 19 PNG derivatives were generated. Three supplied ancillary PNG authorities were hash-only and count as zero visual receipts.',
 'Record26 reports that the assigned directory already existed. The trace does not establish that the directory was absent or empty immediately before launch; its failed initialization is preserved. Actual observed renders, report construction and current hashes are independently bound.',
 'Native Fronts physical9 has null printed_page_label in its original render entry; its visual receipt separately records printed9, corroborated by original native edge text. Null is an omitted metadata label, not a different page. Bridge labels were explicitly completed at record272.',
 'Manifest self-recursion exclusions are declared by the original manifest. This audit binds that manifest directly; it does not read unlisted manifest-v1.json or manifest.sha256.'
]
audit={
 'audit_id':HERE.name,'audit_kind':'Independent technical completion, source transport, native provenance and observed IO isolation; no gameplay regrade','overall_result':'QUALIFIED_TECHNICAL_COMPLETION_CONFIRMED',
 'results':{
  'actual_terminal_completion':'CONFIRMED: task_complete at original physical record292; report writer265 succeeded at268; manifest272 succeeded275; final read-only checks281 succeeded284.',
  'model_effort':'CONFIRMED: all actual turn_context records (one, record10) are gpt-6.1-sol/high; terminal snapshot hash/bytes match exactly.',
  'fresh_initial_prompt':'EXPLICIT_FRESH_REQUEST_BOUND_IN_DISPATCH; EXACT_RUNTIME_TASK_BODY_UNVERIFIABLE_WITHOUT_ENCRYPTED_CONTENT',
  'full_candidate_and_relevant_source_delivery':'CONFIRMED: all31 exact declared numbered ranges independently matched complete original text before record265; required LF coverage has no gaps.',
  'native_provenance':'CONFIRMED: all22 native derivatives independently reproduced byte-for-byte in memory using manifest-bound PyMuPDF1.28.2; all12 actual image payloads decode to corresponding native PNG bytes before verdict construction.',
  'hash_integrity':'CONFIRMED:190 unique manifest-bound candidate/original/output/read-record paths match SHA256 and declared byte sizes;17 originals and18-entry original-hashes index match.',
  'observed_game_data_isolation':'CONFIRMED_WITH_LIMITS: all40 tool programs manually reviewed; candidate, original17 and own outputs were the observed game data. No bank/key/reader/grade/older-audit/game-web access or collaboration/status calls observed. Infrastructure discovery/install IO disclosed separately.',
  'unqualified_process_purity':'NOT_CLAIMED: encrypted incoming task body and implicit installer/OS IO are outside the permitted visible-content verification.',
  'unchanged_originals':'CONFIRMED: candidate/original17 match original bindings; all193 unique baseline-bound inputs, reports, dependencies and provenance files remained byte-identical through this verification.'
 },
 'bindings':{'runtime':summary['runtime'],'dispatch':bind(R/'final-stamped-source-audit-01-dispatch.txt'),'terminal_provenance_container':bind(F/'source-auditor-terminal-runtime-provenance.json'),'candidate':manifest['candidate'],'original17':manifest['originals'],'source_manifest':bind(A/'manifest.json'),'source_report_json':bind(A/'source-audit.json'),'source_report_markdown':bind(A/'source-audit.md'),'source_read_record':bind(A/'source-read-record.json'),'original_hash_index':bind(A/'original-hashes.json'),'helpers':[bind(A/n) for n in ['audit_helpers.py','native_render.py','write_reports.py']]},
 'source_verdict_preserved':{'verdict':report['verdict'],'machine_verdicts':report['machine_verdicts'],'findings_count':len(report['findings']),'claim_groups':len(report['checked_claims']),'authority_qualification':report['authority_qualification'],'limitations':report['limitations'],'this_audit_reassesses_game_claims':False},
 'runtime_physical_records':summary['physical_records'],'actual_contexts':summary['contexts'],'incoming_task_envelope':summary['initial_prompt'],'terminal_events':summary['terminal_events'],
 'verdict_write_boundary':{'first_tool_program_naming_source_audit_json':265,'actual_action':'Creates write_reports.py then executes it; report output writes at its Python lines130–132 and156–158 (tool-program lines131–133 and157–159, depending wrapper).','successful_stdout_record':268,'last_source_text_and_image_record':259,'manifest_writer_record':272,'manifest_writer_stdout_record':275,'final_read_only_verifier_record':281,'final_verifier_stdout_record':284,'no_claim_that_record281_updates_manifest':True},
 'delivery':{'convention':'one-based inclusive physical LF ranges from text.split("\\n"), never splitlines()','candidate_content_lines':498,'candidate_lf_delimiters':498,'candidate_split_lf_pieces_including_empty_eof':499,'coverage':coverage,'declared_ranges':31,'independently_exact_visible_ranges':31,'nested_stdout_recovery':{'record':110,'method':'Parse full original input_text JSON representations, then value.output; both complete stdout strings independently match original numbered ranges. No missing text invented.','ranges':['rules LF2951–2983','errata LF1–247']},'truncated_source_delivery_detected':False,'receipt_file':'text-delivery-receipts.json'},
 'native':{'pymupdf':native['pymupdf_version'],'mupdf':native['mupdf_version'],'native_derivatives':22,'text_derivatives':3,'png_derivatives':19,'actual_model_visible_pngs':12,'actual_payload_mime_types':sorted({x['mime'] for x in images}),'independent_exact_reproductions':22,'image_receipts':'image-delivery-receipts.json','reproduction_receipts':'native-reproduction-receipts.json','physical_printed_mapping':'Rulebook physical4,5,33,42 = printed4,5,33,42; Bridge physical1–11 = printed12–22; Fronts physical1,6,9 = printed1,6,9; board physical1 has no page label. Recorded matrices1.5 except Bridge1.25; all clips null. Edge number text independently corroborates page labels.','ancillary_pngs_hash_only':True},
 'manual_tool_and_helper_review':io_review,'failures_and_setup':summary['failure_and_setup_markers'],'preserved_versions':versions,'original_hash_index_matches':original_index_matches,'limitations':limitations,
 'retention_policy':{'retained':'Only allowlisted tool inputs and model-visible tool text, image MIME/decoded-byte hashes, narrow actor/parent/model/effort/event labels and original record ordinals/byte offsets/lengths/hashes. Target terminal-provenance projection only.','not_retained':'No raw runtime copy, image base64, session/context/message/reasoning/profile/account/encrypted bodies. No unrelated runtime/actor discovery.','own_execution':'sys.dont_write_bytecode=True before imports; independent reproduction in memory; no source-auditor programs executed; only new assigned verification directory written.'},
 'unchanged_baseline_path_count':len(after)
}
# Correct precise Python line mapping from inspected script rather than estimated positions.
audit['verdict_write_boundary']['actual_action']='Creates write_reports.py then executes it; tool-program lines131–132 write JSON outputs,157–158 write Markdown outputs; successful stdout at268. This call is the verdict-construction boundary, not its later manifest/verification calls.'
audit['results']['unchanged_originals']=f'CONFIRMED: candidate/original17 match original bindings; all{len(after)} unique baseline-bound inputs, reports, dependencies and provenance files remained byte-identical through this verification.'
newline_receipts=[]
for path in sorted({x['path'] for x in delivery}):
    raw=Path(path).read_bytes()
    receipt={'path':path,'raw_file_sha256':sha(raw),'raw_lf_piece_count':len(raw.split(b'\n')),'crlf_pairs':raw.count(b'\r\n'),'bare_cr_count':raw.count(b'\r')-raw.count(b'\r\n'),'read_text_split_lf_pieces':len(Path(path).read_text().split('\n'))}
    assert receipt['raw_lf_piece_count']==receipt['read_text_split_lf_pieces'] and receipt['bare_cr_count']==0
    newline_receipts.append(receipt)
audit['delivery']['newline_transport']='The inspected original helper uses Path.read_text() (universal newline normalization), then split("\\n"). Verification independently mirrors those visible characters and also confirms raw LF positions/counts are preserved. Errata has246 CRLF pairs; publisher HTML has2. Raw original hashes bind all CR bytes; CR bytes normalized by the original helper are not claimed as model-visible.'
audit['delivery']['raw_newline_receipts']=newline_receipts
save('audit.json',audit)
lines=[
 '# Independent technical completion and IO audit',
 '',
 '**Qualified technical completion confirmed.** Full required text transport, actual model/effort, terminal completion, native provenance and observed permitted game-data IO are verified. The incoming substantive task body is encrypted in the permitted runtime; exact dispatch-to-prompt equality and actual fork mode cannot be independently certified. This is not a new source verdict or gameplay grade.',
 '',
 f'Candidate: `{manifest["candidate"]["path"]}`  \nSHA256 `{manifest["candidate"]["sha256"]}`; {manifest["candidate"]["bytes"]} bytes.',
 '',
 f'Original source audit remains **{report["verdict"]}**, with {len(report["checked_claims"])} manually authored claim groups and zero findings. Its official-claims PASS, human-interpretation-fidelity PASS and scoped overall PASS are preserved. The accepted defense interpretation remains explicitly human authority; no independently inspected publisher email or unqualified official-only signoff is asserted.',
 '',
 '## Runtime and completion',
 '',
 f'The only runtime inspected is `{summary["runtime"]["path"]}`: {summary["runtime"]["bytes"]} bytes, SHA256 `{summary["runtime"]["sha256"]}`. It exactly matches the final terminal-provenance snapshot. Actor `/root/v13_stamped_i1_source_auditor` and parent `01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7` match. All actual turn contexts—one at physical record10—specify `gpt-6.1-sol/high`. The actual `task_complete` event is record292.',
 '',
 'Record265 is the first tool program naming `source-audit.json`. It writes the manually authored report helper and executes it; its successful output is record268. All required text/image delivery ends by record259. Record272 writes source/visual records and manifest, with success at275. Record281 only reads/asserts existing outputs; its success is284. It does not update the manifest.',
 '',
 'The dispatch file explicitly requests a fresh independent source audit with `fork_turns=none` and the requested model/effort. It is hash-bound in `audit.json`. The runtime incoming task envelope (record13) identifies `/root` → the target actor and contains an encrypted task part plus a 93-byte plaintext wrapper. The encrypted body was neither inspected nor retained. This limits proof of exact initial-prompt delivery; it does not negate the directly verified tool deliveries or model settings.',
 '',
 '## Complete delivery before the verdict writer',
 '',
 'Every one of the31 declared read ranges was independently compared against the complete original numbered LF text, including visible whitespace and empty EOF. Verification matches each full contiguous block in the actual model-visible tool output before265, rather than trusting coverage flags or report assertions. The inspected helper uses `Path.read_text()` universal newline normalization followed by `split("\\n")`; verification mirrors that visible representation and independently confirms raw LF positions/counts are identical. Raw original hashes bind the CR bytes normalized by that original helper (246 CRLF pairs in errata;2 in publisher HTML). No bare CR lines exist in these delivered text files.',
 '',
 '| Required data | Actual original runtime records | Result |',
 '|---|---|---|',
 '| Candidate LF1–499:498 content lines and empty EOF piece |45,50,55,60|Complete exact delivery|',
 '| Rulebook LF1–3015 |65,70,75,84,89,94,99,104,110,117|Complete exact delivery|',
 '| Rulebook LF3290–3306 |232|Complete exact delivery|',
 '| Complete errata, original correction post, designer rulings and human-authority records |110,124,131|Complete exact declared ranges|',
 '| Publisher resource section and relevant own component extractions |194,218,225,232,259|Complete exact declared ranges|',
 '',
 'Record110 holds complete nested JSON stdout representations from two independent tool calls. Parsing the intact JSON `value.output` strings recovers full rulebook LF2951–2983 and errata LF1–247. No omitted text was invented. No actual source text truncation is present. Failed setup attempts remain in the allowlisted projection.',
 '',
 'Exact source paths, file hashes, LF endpoints, matching output record/content indices, representation paths, offsets and matched-block hashes appear in `text-delivery-receipts.json`.',
 '',
 '## Native provenance and actual image delivery',
 '',
 'The manually inspected original render program at177 reads the four permitted original PDFs and writes its own derivatives under the assigned source-audit directory. The inline program at236 adds Fronts1/6; Bridge7/8/11 already originated from177 and are not replaced. No previous audit render is used.',
 '',
 'An independent renderer imported only the manifest-bound PyMuPDF1.28.2 runtime, with bytecode writes disabled. It reproduced **all22 native derivatives byte-for-byte in memory**:3 text extractions and19 PNGs. No source auditor helper was executed. The12 actual model-visible `input_image` PNG payloads independently decode to exactly the12 declared inspected derivative hashes, all before265.',
 '',
 'Physical/printed numbering is corroborated by native page-edge number text: rulebook4/5/33/42 coincide; Bridge physical1–11 map to printed12–22; Fronts1/6/9 coincide. Board physical1 is unlabelled. Exact recorded matrices (1.5; Bridge1.25) and null clips reproduce the bytes. Fronts9 originally has a null printed-label field in its render entry; its visual record and native text identify printed9. All receipt paths, original hashes, render parameters, MIME/decoded payload hashes and matching records are preserved.',
 '',
 'The three supplied ancillary PNG originals were hash-only authorities and contribute zero visual receipts. Generated PNG count19 and actually received PNG count12 are distinguished.',
 '',
 '## Observed IO and report construction',
 '',
 'All40 tool programs, the source read helper, native render helper and literal report writer were manually inspected. Observed game-data inputs are the final candidate, the exact17 original authorities and the auditor’s own derivatives/reports. No question bank, answer key, reader answer, grade, older audit, other-agent/status call or external game-source access is observed. The two explicitly permitted original human-authority files remain permitted inputs.',
 '',
 'The writer’s81 claim rows, reasons, empty findings, PASS values and scope qualification are literals written by the auditor. Code attaches references/quotations and serializes those decisions. It does not infer or compute game accuracy. The current manifest-bound `write_reports.py` exactly matches the inspected tool heredoc. The later fixed-PASS assertions are output consistency checks, not independent gameplay validation.',
 '',
 'Infrastructure IO is disclosed: `python` was unavailable (21); `mkdir` encountered an existing assigned directory (26); PDF binaries were unavailable (138); ordinary pip encountered DNS/network failures and disabled an unwritable cache (145); library discovery searched system/local library filenames and loaded bundled workspace dependency paths (149/154); bundled Windows Python failed with a WSL socket error (164); approved escalated pip installed PyMuPDF1.28.2 from cached wheel metadata/wheel (173). These are dependency/setup activities. This audit does not claim no network, no cache, or no setup paths. They were not rerun.',
 '',
 '## Hashes, unchanged inputs and limits',
 '',
 f'All190 unique manifest-bound candidate/original/output/read-record files match SHA256 and declared byte sizes, including every listed helper/library/cache file. All17 original hashes match their explicit bindings; the18-entry original-hashes index also matches. The current report and source-read version copies are byte-identical. This audit separately binds the original manifest itself. All{len(after)} baseline-bound files—including reports, package/cache files and terminal provenance—remain unchanged after independent reproduction.',
 '',
 'The narrow runtime projection retains permitted tool inputs/text outputs and image-byte receipts with physical record ordinals, byte offsets, lengths and SHA256. It contains no raw runtime copy, image base64, encrypted body, reasoning body, full session/context/message/profile/account body, or unrelated actor/runtime projection.',
 '',
 'Limits remain: exact initial task-body/fork verification is unavailable from opaque saved content; observed tool IO is not a syscall/network capture; the directory already existed at launch; and transport cannot establish cognitive completeness or game-rule truth. This source task permits bounded text transport without a fixed45-line cap; separate reader45/6 restrictions do not apply. The source verdict and its component-lookup/user-authority qualifications remain unchanged. There is no new gameplay assessment.',
 '',
 'Detailed bindings and results: `audit.json`. Supporting evidence: `runtime-allowlisted-projection.jsonl`, `terminal-provenance-target.json`, `text-delivery-receipts.json`, `image-delivery-receipts.json`, `native-reproduction-receipts.json`, `file-hash-verification.json`, `unchanged-after-verification.json`.',
 ]
(HERE/'audit.md').write_text('\n'.join(lines)+'\n')
artifacts=[]
for p in sorted(HERE.iterdir()):
    if p.is_file() and p.name!='verification-artifact-manifest.json':artifacts.append(bind(p))
save('verification-artifact-manifest.json',artifacts)
print(json.dumps({'audit_json':str(HERE/'audit.json'),'audit_md':str(HERE/'audit.md'),'result':audit['overall_result'],'unchanged_count':len(after),'source_writer_matches':writer_matches,'artifact_count':len(artifacts)}))
