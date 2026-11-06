from pathlib import Path
import json,hashlib,datetime,shutil,sys,difflib
ROOT=Path(__file__).resolve().parent
CANONICAL=ROOT.parents[4]/'rules/sidereal-confluence.md'
# parents: slug, summary-qa, quality, docs, repository
CANONICAL=Path('/home/jonny/projects/boardgame-rules/rules/sidereal-confluence.md')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def freeze(bank,iteration):
    dest=ROOT/iteration; dest.mkdir(exist_ok=False)
    shutil.copyfile(CANONICAL,dest/'summary-snapshot.md')
    for n in ['questions.json','answer-key.json','asked-facts.json']:shutil.copyfile(ROOT/bank/n,dest/n)
    save(dest/'input-manifest.json',{'iteration':iteration,'bank':bank,'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'canonical':str(CANONICAL),'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','hashes':{n:sha(dest/n) for n in ['summary-snapshot.md','questions.json','answer-key.json','asked-facts.json']},'sources':json.loads((ROOT/('source-manifest.json' if (ROOT/'source-manifest.json').exists() else 'input-manifest.json')).read_text())['sources']})
    prompt='''You are an independent rules-summary reader in a blind evaluation.
Read ONLY these two rules DATA files:
{summary}
{questions}
Do not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, other files, parent history or web links. Do not browse. Use only the supplied frozen summary as the rules authority, never prior game knowledge. Do not communicate with other readers. Scenario facts expressly stated in a question are givens; they need not be narrated as hypothetical setups in the summary. Still flag any requested RULE absent from the summary, and do not guess.

Read the COMPLETE summary and EVERY question before answering. To avoid tool truncation, use Python character slicing and print only one bounded contiguous chunk per tool response, at most 6000 characters, with sufficient max_output_tokens (at least 4500). Request separate sequential outputs for ranges [0,6000), [6000,12000), etc through actual length. Include range start/end/total and SHA-256 in each receipt. A call that prints all chunks at once is not safe. Check each tool response for truncation; reread any truncated range using smaller chunks. Preserve complete input-delivery receipts (file, length, hash, contiguous ranges and truncation checks) in your output. You may use Python to load the two allowed files for searching and writing your output; no other file may be read.

For EVERY question, use the same generic procedure: enumerate its own requested clauses; search the entire frozen summary for EVERY named item and relevant terms before declaring missing information; choose complete appropriate operative summary units; give a concise direct ruling per clause and actual calculated values for numeric cases; self-check every clause against the chosen text. A unit may be a complete paragraph/list, a heading-bounded subsection including child subsections through the next same/higher heading, or an explicit union of complete relevant leaf units. A parent heading introduction alone is not the entire procedure. Table evidence must contain actual COMPLETE newline-bounded row through final pipe, local header, and controlling introductions/legends/definitions needed for the fact. Never crop by an arbitrary character limit, midword or midcell. Before saving, mechanically check excerpts are literal complete units from the snapshot and attach their actual character spans. Include full governing context if a table row inherits a rule. Do not duplicate identical text under multiple labels within one entry or attach unrelated whole-summary dumps. Operative quotes can supply ordinary lookup facts directly; still give direct case rulings and actual requested calculations. Do not substitute quotations for necessary applications. Technical format/source-span diagnostics are separate from factual correctness.

Answer ALL questions and ALL requested parts. If a requested part lacks rules support, explicitly identify that part as unsupported. Save valid JSON ONLY to {output}, top-level reader, inputs_read, delivery_receipts, source_span_diagnostics, answers. Each answers entry: id, clauses, answer (direct ruling), support (supported/partial/unsupported), evidence (array of complete literal operative units with section, start, end, text). Do not evaluate or improve the summary. You may write only your assigned output. Do not read a helper or any other files. If the output is large, build it in memory or append your own remaining answer batches to that same assigned JSON, ensuring all expected IDs exactly once and valid final JSON. Retain substantive rulings and evidence; do not omit difficult questions. In your final response give only output path and number answered.
'''
    helper=(ROOT/'reader-protocol-v2/source_units.py').read_text()
    method='''
Generic prebound extraction method (process code only, no rules data): execute the exact Python code below in your own processing code, without reading a helper file. For every operative evidence location YOU choose, call extract_unit(summary_text, chosen_offset), then validate_record(summary_text, returned_record). Keep its complete returned source text and actual bounds in the same answer entry. Do not crop the returned unit. A returned table record includes the complete actual row, headers and literal fields; select additional governing context when needed. You may attach the returned source record directly as evidence, with an optional section label; this supersedes the flat evidence-format example above. Before saving all answers, validate every selected evidence record against the frozen summary. Evidence choice remains yours and does not replace direct case conclusions or requested calculations. Each answer still needs all its own clauses resolved. The only rules DATA remain the frozen summary and questions. Do not read this code from a file or any other files. Record the embedded code SHA-256 and actual execution/validation in source_span_diagnostics.
BEGIN GENERIC PYTHON CODE
'''+helper+'\nEND GENERIC PYTHON CODE\n'
    for reader in ['a','b']:
        (dest/f'reader-{reader}-prompt.txt').write_text(prompt.format(summary=dest/'summary-snapshot.md',questions=dest/'questions.json',output=dest/f'reader-{reader}.json')+method)
    save(dest/'prompt-binding.json',{'protocol':'generic-lookup-complete-units-v2-with-embedded-v10-helper','same_instructions_except_output':(dest/'reader-a-prompt.txt').read_text().replace('reader-a.json','reader-OUTPUT.json')==(dest/'reader-b-prompt.txt').read_text().replace('reader-b.json','reader-OUTPUT.json'),'prompt_hashes':{f'reader-{x}':sha(dest/f'reader-{x}-prompt.txt') for x in ['a','b']},'known_limits':'Fixed-set tool-assisted regression; context isolation by fork none and instructions, not OS file isolation; not held-out accuracy.'})
    print(dest)
def provenance():
    logdir=Path('/mnt/c/Users/jonny/.codex/sessions')
    records=[]
    requests={}
    parent_logs=list(logdir.glob('2026/11/*/*01a1b0b3-0030-70b2-8947-7a940fdf364f.jsonl'))
    for parent_log in parent_logs:
        for ordinal,line in enumerate(parent_log.open(),1):
            try: rec=json.loads(line); pay=rec.get('payload',{})
            except: continue
            if pay.get('name')=='spawn_agent' and pay.get('type')=='function_call':
                try: args=json.loads(pay['arguments'])
                except: continue
                requests['/root/'+args['task_name']]={'requested_model':args.get('model'),'requested_effort':args.get('reasoning_effort'),'requested_fork_turns':args.get('fork_turns'),'parent_request_record_ordinal':ordinal,'parent_runtime_source':str(parent_log),'parent_request_record_sha256':hashlib.sha256(line.encode()).hexdigest()}
    for p in logdir.glob('2026/11/*/*.jsonl'):
        try:
            with p.open() as f:first=f.readline()
            meta=json.loads(first).get('payload',{})
        except:continue
        if meta.get('id')!='01a1b0b3-0030-70b2-8947-7a940fdf364f' and meta.get('parent_thread_id')!='01a1b0b3-0030-70b2-8947-7a940fdf364f':continue
        agent=meta.get('agent_path')
        if agent is None and meta.get('id')!='01a1b0b3-0030-70b2-8947-7a940fdf364f':continue
        item={'identity':meta.get('id'),'parent':meta.get('parent_thread_id'),'task':agent or '/root','timestamp':meta.get('timestamp'),'runtime_source_path':str(p),'runtime_log_history_mode':meta.get('history_mode'), 'request':requests.get(agent or '/root',{'requested_model':'gpt-6.1-sol','requested_effort':'high','role':'primary worker'}),'identity_record':{'ordinal':1,'sha256':hashlib.sha256(first.encode()).hexdigest()},'turn_context_records':[]}
        for n,line in enumerate(p.open(),1):
            try:r=json.loads(line)
            except:continue
            if r.get('type')=='turn_context':
                t=r.get('payload',{}); item['turn_context_records'].append({'ordinal':n,'timestamp':r.get('timestamp'),'actual_model':t.get('model'),'actual_effort':t.get('effort'),'sha256':hashlib.sha256(line.encode()).hexdigest()})
        records.append(item)
    save(ROOT/'runtime-provenance.json',{'runtime_logs_remain_untouched':True,'context_note':'fork_turns none is verified from the actual parent spawn request. runtime_log_history_mode paginated describes runtime storage, not inherited parent context. No full session metadata, turn context, instructions, permissions or account objects copied. Complete actual rules-data delivery is separately verified from tool outputs.','records':records})
    print([(x['task'],[(t['actual_model'],t['actual_effort']) for t in x['turn_context_records']]) for x in records])
if __name__=='__main__':
    if sys.argv[1]=='freeze':freeze(*sys.argv[2:])
    elif sys.argv[1]=='provenance':provenance()
