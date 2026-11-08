"""Freeze a single adjudication packet for explicit genuine borderline pairs."""
from pathlib import Path
import argparse,hashlib,json,sys
B=Path(__file__).parent.resolve()
parser=argparse.ArgumentParser();parser.add_argument('pairs',nargs='+');parser.add_argument('--iteration',default='expanded-luna-iteration-03');args=parser.parse_args()
I=(B/args.iteration).resolve();assert I.is_relative_to(B)
G=I/'grading';K=B/'expanded-supported-bank-v11'
assert json.loads((I/'primary-grading-integrity.json').read_text())['all_expected_records_present']
P=G/'fresh-borderline-input.json';assert not P.exists(),'Never resample an existing neutral packet'
pairs=[tuple(x.split(':')) for x in args.pairs];assert pairs and len(set(pairs))==len(pairs)
q={x['id']:x for x in json.loads((I/'questions.json').read_text())['questions']}
key={x['id']:x for x in json.loads((K/'answer-key.json').read_text())['answers']}
scope={x['id']:x for x in json.loads((K/'asked-clause-map.json').read_text())}
raw={l:{x['id']:x for x in json.loads((I/f'reader-{l}.json').read_text())['answers']} for l in 'ab'}
primary={};diagnostics={}
for p in sorted(G.glob('grades-*.json')):
    d=json.loads(p.read_text())
    for x in d.get('records',d.get('grades',d.get('entries',[]))):primary[(x['reader'].replace('reader_',''),x['id'])]=x
    for x in d.get('borderline_diagnostics',[]):
        if 'reader' in x and 'id' in x:diagnostics.setdefault((x['reader'].replace('reader_',''),x['id']),[]).append(x)
entries=[]
for l,ident in pairs:
    assert (l,ident) in primary and diagnostics.get((l,ident)),('Require genuine recorded borderline',l,ident)
    entries.append({'reader':l,'id':ident,'complete_raw_entry':raw[l][ident],'primary_grade':primary[(l,ident)],'original_borderline_diagnostics':diagnostics[(l,ident)]})
ids=list(dict.fromkeys(i for l,i in pairs))
pack={'purpose':'ONE fresh whole-entry adjudication of genuine recorded borderlines; primary findings and labels preserved.','questions':[q[i] for i in ids],'fixed_key':[key[i] for i in ids],'fixed_asked_clause_map':[scope[i] for i in ids],'entries':entries,'scope_status':'Preliminary supported-source94; actual SG01 authority pending; no new compound rulings.','process_annotation':json.loads((G/'literal-scope-annotation-v1.json').read_text())}
P.write_text(json.dumps(pack,indent=2,ensure_ascii=False)+'\n')
prompt='''You are a NEW independent neutral whole-entry adjudicator, gpt-6.1-sol/high, no parent context. This is the ONE adjudication allowed for these current cases; do not seek other graders or further samples. Read ONLY the named frozen summary and complete assigned packet as game-data inputs. First read this complete process prompt; also read the small process-only literal-scope annotation named below. No browsing, coordination/status tools, other files/history, or reader communications.

Read BOTH game-data files COMPLETELY in exact contiguous Unicode ranges <=5500 characters, ONE range per tool result, outer cap >=6000 tokens. Retain actual ranges/hashes; do not skim any complete structured entry or quoted evidence.

Adjudicate every assigned pair using its literal question, unchanged fixed asked-fact map/key and complete original raw entry. Primary findings identify real borderlines but do not dictate your decision. Every substantive field counts. Scenario givens do not require restatement; unasked background does not create completeness requirements. Do not borrow phantom scenario metadata to supply a missing actually asked procedure. Correct complete same-entry operative source text can supply ordinary lookup answers without redundant paraphrase. Actual given cases/calculations need actual decisions/results. Correct conditionals for unspecified conditions are acceptable. Interpret a phrase in its full question/entry context, without inventing new givens. Confidence and extraction bookkeeping stay separate from factual correctness.

Use exactly Correct, Partial, Incorrect. Correct requires every actually asked fact and no material false assertion anywhere. Partial means a genuine asked omission/unresolved result with no material false claim. ANY material wrong actor, timing, quantity, destination, condition or rule is Incorrect, even beside correct quotations; never call a wrong claim Partial. If a map or key appears to exceed the literal question or conflict with the source, explicitly diagnose it separately without silently changing inputs. Do not repair the guide or add generic impossible-cost, stack or revival rules. SG01 unasked authority hypotheticals are not factual caps.

Write ONLY the named output, valid JSON with inputs_read (the TWO game-data receipts), process_instructions_read, records, totals. Each record: reader, id, label, asked_fact_assessments for EVERY original required fact, material_wrong_claims, genuine_omissions, full-context rationale and raw_entry_sha256 (canonical JSON sorted keys, ensure_ascii=False, separators(',',':')). Finish with saved path/count only.
'''
prompt+=f'\nSummary: {I/"summary-snapshot.md"}\nComplete packet: {P}\nProcess-only annotation: {G/"literal-scope-annotation-v1.json"}\nOutput: {G/"fresh-borderline-adjudication.json"}\n'
assert len(prompt)<=5500
T=G/'neutral-adjudicator-prompt.txt';T.write_text(prompt)
manifest={'pairs':[{'reader':l,'id':i} for l,i in pairs],'packet_path':str(P),'packet_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'prompt_path':str(T),'prompt_sha256':hashlib.sha256(T.read_bytes()).hexdigest(),'one_fresh_adjudicator_only':True,'further_sampling_authorized':False}
(G/'fresh-borderline-input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest))
