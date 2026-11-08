"""Freeze one immutable QA iteration in this exclusive run; no canonical/shared writes."""
from pathlib import Path
import argparse,json,hashlib,shutil,datetime,difflib
B=Path(__file__).parent.resolve();ROOT=Path('/home/jonny/projects/boardgame-rules')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('benchmark');p.add_argument('iteration');p.add_argument('--expected-summary-sha',required=True);p.add_argument('--previous');a=p.parse_args()
K=(B/a.benchmark).resolve();I=(B/a.iteration).resolve();assert K.is_relative_to(B) and I.is_relative_to(B)
assert not I.exists(),'Never overwrite an existing iteration';freeze=json.loads((K/'freeze.json').read_text());assert all(sha(K/n)==h for n,h in freeze['hashes'].items())
S=ROOT/'rules/new-angeles.md';assert sha(S)==a.expected_summary_sha,'Canonical changed unexpectedly: coordinate before freezing'
q=json.loads((K/'questions.json').read_text());key=json.loads((K/'answer-key.json').read_text());scope=json.loads((K/'asked-clause-map.json').read_text());ids=[x['id'] for x in q['questions']];assert len(ids)==len(set(ids))==len(key['answers'])==len(scope);assert set(ids)=={x['id'] for x in key['answers']}=={x['id'] for x in scope}
helper=q['generic_reader_process'];assert hashlib.sha256(helper['source_extractor_python'].encode()).hexdigest()==helper['source_extractor_sha256'];assert helper['source_extractor_sha256']==sha(ROOT/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/generic-reader-method/v10/source_units.py')
original=json.loads((B/'input-manifest.json').read_text())['sources'];assert all(sha(s)==v['sha256'] for s,v in original.items())
I.mkdir();shutil.copyfile(S,I/'summary-snapshot.md');shutil.copyfile(K/'questions.json',I/'questions.json')
protocol='''You are a NEW independent blind rules-summary reader. Read ONLY these two inputs:
{summary}
{questions}
Summary is the sole rules authority. The questions JSON embeds rule-agnostic process instructions and exact generic Python extraction code: execute that code in memory, choose evidence offsets yourself, and read no external helper file. No other files, sources, keys, manifests, previous outputs/grades, parent history, browsing, prior game knowledge, or communication with other readers. Do not call coordination/status tools. Write ONLY your assigned output below.

Read BOTH complete inputs before answering in contiguous ranges of AT MOST5500 Unicode characters. ONE range per functions.exec result, sufficient outer cap>=6000tokens. Compute total length and next end=min(start+5500,total) mechanically; never combine a final remainder into an oversized chunk. Print filename/start/end/total and exact text. Check no tool truncation, all[0,total) ranges contiguous, and retain actual range/hash receipts in inputs_read. Line counts are insufficient. Scenario facts explicitly given are givens; flag any asked rule absent from summary, never guess.

For EACH question, enumerate its own asked clauses, search the ENTIRE summary for all named items and relevant terms, select complete governing source units using embedded extract_unit(summary,offset), and validate every record with validate_record. Preserve governing procedure peer/child steps, complete actual table rows/headers/all cells and controlling introductions/legends/definitions. Do not crop controlling procedures or dump unrelated sections. Complete same-entry operative quotations can directly supply ordinary lookup facts; requested concrete cases/calculations require actual results and decisions. Give concise complete clause conclusions; do not merely say to apply rules. Preserve unspecified quantities/ownership/conditions using correct conditional outcomes where appropriate, without inventing a changed given case. Prepare one checked result per clause and render repeated fields consistently from that value. Self-check every clause and all substantive fields against chosen text. Technical source-unit/format bookkeeping is distinct from factual scoring; every material wrong claim still counts even beside a correct quote.

Save valid JSON to {output} with reader, inputs_read, answers. Include all N question IDs exactly once, where N is the actual questions-array length. Each entry: id, clauses, answer, support(supported/partial/unsupported), evidence(array of complete validated extraction records). Answer ALL requested parts; unsupported parts explicit. Do not evaluate or repair summary. Finish entire bank in your own batches if needed and preserve every substantive field. Final reply only saved path/count.
'''
for l in ['a','b']:(I/f'reader-{l}-prompt.txt').write_text(protocol.format(summary=I/'summary-snapshot.md',questions=I/'questions.json',output=I/f'reader-{l}.json'))
assert (I/'reader-a-prompt.txt').read_text().replace('reader-a.json','reader-b.json')==(I/'reader-b-prompt.txt').read_text()
meta={'benchmark':a.benchmark,'question_count':len(ids),'expected_ids':ids,'scope_status':freeze['scope_status'],'scope_limit':freeze.get('scope_limit'),'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','protocol':'generic-complete-units-v5-fixed-boundary-v10-embedded-process','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hashes':{n:sha(I/n) for n in ['summary-snapshot.md','questions.json','reader-a-prompt.txt','reader-b-prompt.txt']},'key_sha256':sha(K/'answer-key.json'),'asked_clause_map_sha256':sha(K/'asked-clause-map.json'),'benchmark_freeze_sha256':sha(K/'freeze.json'),'authoritative_sources_unchanged':True,'helper_sha256':helper['source_extractor_sha256'],'identical_instructions_except_output_path':True}
(I/'input-manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
if a.previous:
 P=(B/a.previous/'summary-snapshot.md').resolve();assert P.is_relative_to(B);(I/'summary-changes.patch').write_text(''.join(difflib.unified_diff(P.read_text().splitlines(True),S.read_text().splitlines(True),fromfile=str(P.relative_to(B)),tofile=a.iteration+'/summary-snapshot.md')))
print(json.dumps({'iteration':str(I),'question_count':len(ids),'summary_sha256':sha(I/'summary-snapshot.md'),'status':'frozen, not dispatched'}))
