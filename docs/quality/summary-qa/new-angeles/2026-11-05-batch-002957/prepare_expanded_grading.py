"""Create immutable disjoint whole-entry grading packs after both readers finish."""
from pathlib import Path
import argparse, hashlib, json
B=Path(__file__).parent.resolve()
p=argparse.ArgumentParser();p.add_argument('iteration');p.add_argument('benchmark');p.add_argument('--block-size',type=int,default=16);a=p.parse_args()
I=(B/a.iteration).resolve();K=(B/a.benchmark).resolve();assert I.is_relative_to(B) and K.is_relative_to(B)
G=I/'grading';assert not G.exists(),'Preserve all previous grading inputs';G.mkdir()
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
q=read(I/'questions.json')['questions'];k=read(K/'answer-key.json')['answers'];s=read(K/'asked-clause-map.json');ids=[x['id'] for x in q]
maps=[{x['id']:x for x in rows} for rows in [q,k,s]]
output_manifest=read(I/'reader-output-manifest.json') if (I/'reader-output-manifest.json').exists() else {}
reader_paths={l:Path(output_manifest.get(l,I/f'reader-{l}.json')) for l in ['a','b']}
assert all(p.resolve().is_relative_to(I) for p in reader_paths.values())
readers={l:read(p) for l,p in reader_paths.items()}
for l,d in readers.items():
    assert len(d['answers'])==len(ids) and {x['id'] for x in d['answers']}==set(ids),l
rm={l:{x['id']:x for x in d['answers']} for l,d in readers.items()}
protocol='''You are a NEW independent primary grader, gpt-6.1-sol/high, no parent context. Read ONLY the frozen summary and your assigned block JSON below. Do not call coordination/status tools, browse, view prior reports, or communicate with readers. Read both files completely in contiguous exact Unicode ranges <=5500 characters, ONE range per tool result, outer cap >=6000 tokens; mechanically compute each next end=min(start+5500,total). Retain exact ranges/hashes and verify no truncation. Do not skim complete raw answers: every substantive field and every operative quoted source unit in each assigned entry counts.

Grade BOTH readers for EVERY assigned ID against the fixed question and actual asked-clause map, using the supplied correct source key and summary. These inputs were frozen before answers. Scenario givens are not missing-rule defects. Contextual background and unasked details are not independent completeness requirements. Any volunteered materially false claim is Incorrect, including false background, even if correct text also appears elsewhere. A correct quote never cancels a contradictory claim. Correct complete operative same-entry quotations can directly supply ordinary lookup facts; do not demand redundant paraphrases. Requested concrete calculations/cases require actual results and decisions. Correct conditional outcomes for unspecified conditions are acceptable; do not demand invented givens. Confidence/support labels or source-format bookkeeping alone are not factual errors. Do not cap printed Arrest Orders instruction answers for unasked unresolved priority/impossible-placement hypotheticals (SG01); current-bank regression is preliminary while that external scope decision is pending.

Use exactly Correct, Partial, Incorrect. Correct requires every actually asked clause answered accurately and no material false assertion anywhere. Partial means a genuine asked omission/unresolved result with no material contradiction. Incorrect means ANY material wrong assertion; never label an entry Partial while finding a wrong actor, destination, quantity, timing, condition or other material rule. Distinguish a real absence from correct operative source text already in that same entry. Do not repair the summary, change question/key scope, or use a later answer to reinterpret the required scope. If an input itself has a source/scope defect, report it explicitly separately without silently changing it. Technical delivery or extraction diagnostics stay separate from factual labels.

Write only the assigned grades output. Include inputs_read receipts and one record for each reader/id pair: reader, id, label, asked_fact_assessments (each required clause, exact whole-entry support/omission/wrong-claim location), material_wrong_claims, genuine_omissions, rationale, raw_entry_sha256. Preserve any real borderline diagnostic for ONE independent whole-entry adjudication, never automatically upgrade or resample. Report exact totals and input hashes. Finish with saved path/count only.
'''
manifest=[]
for index,start in enumerate(range(0,len(ids),a.block_size),1):
    subset=ids[start:start+a.block_size]
    entries={l:[rm[l][i] for i in subset] for l in readers}
    pack={'block':index,'ids':subset,'scope_status':'preliminary current-bank; SG01 awaits actual human/publisher authority',
          'questions':[maps[0][i] for i in subset],'fixed_key':[maps[1][i] for i in subset],
          'asked_clause_map':[maps[2][i] for i in subset],'complete_raw_reader_entries':entries,
          'source_file_hashes':{str(p):sha(p) for p in [I/'summary-snapshot.md',I/'questions.json',K/'answer-key.json',K/'asked-clause-map.json',*reader_paths.values()]},
          'raw_entry_sha256':{l:{i:hashlib.sha256(json.dumps(rm[l][i],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest() for i in subset} for l in readers}}
    f=G/f'block-{index:02}.json';f.write_text(json.dumps(pack,indent=2,ensure_ascii=False)+'\n')
    out=G/f'grades-{index:02}.json';prompt=G/f'grader-{index:02}-prompt.txt';prompt.write_text(protocol+f'\nSummary: {I/"summary-snapshot.md"}\nAssigned complete block: {f}\nOutput: {out}\n')
    manifest.append({'block':index,'ids':subset,'pack':str(f),'pack_sha256':sha(f),'prompt':str(prompt),'prompt_sha256':sha(prompt),'output':str(out)})
(G/'input-manifest.json').write_text(json.dumps({'question_count':len(ids),'expected_grade_records':2*len(ids),'block_size':a.block_size,'blocks':manifest},indent=2)+'\n')
assert [i for x in manifest for i in x['ids']]==ids
print(json.dumps({'blocks':len(manifest),'records':2*len(ids),'directory':str(G)}))
