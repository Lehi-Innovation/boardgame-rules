from pathlib import Path
import hashlib,json,shutil,sys,difflib
q=Path(__file__).resolve().parent
name,benchmark=sys.argv[1:3];version=sys.argv[3] if len(sys.argv)>3 else 'v1';d=q/name;d.mkdir(exist_ok=False)
s=Path('/home/jonny/projects/boardgame-rules/rules/dune-imperium-uprising.md');shutil.copyfile(s,d/'summary-snapshot.md');shutil.copyfile(q/benchmark/'questions.json',d/'questions.json')
prompt='''You are an independent rules-summary reader in a blind evaluation.

Read ONLY these two input files:
{summary}
{questions}

Do not read any authoritative rulebook, extracted text, answer key,
manifest, prior responses, other files, parent history or web links.
Do not browse. Use only the supplied summary as evidence, not prior
game knowledge. Do not communicate with other readers.

Answer every question in the input file, including every requested part. If a requested
fact is absent, explicitly identify that part as unsupported; do not guess.

For every question include:
- id
- answer
- support: supported, partial or unsupported
- evidence: a short quote or section from the summary

Before writing final JSON, reread every question and review your draft answer on your own. Explicitly resolve every requested part from the supplied summary, including requested quantities, timing, costs, destinations and exceptions. Do not borrow a missing fact from another answer. Identify unsupported parts instead of guessing. Check volunteered rulings for contradictions with the summary.

Save valid JSON to {output} with
top-level fields reader, inputs_read and answers (an array).
You may read only the two allowed inputs and write only your assigned
output. Do not evaluate or improve the summary.
'''
if version in ['v2','v3']:
 prompt=prompt.replace('Answer every question in the input file, including every requested part.', 'Operational reading: read the two files separately in bounded chunks, for example at most 30 summary lines or 10 questions per output. Use one chunk per tool invocation, including the outer wrapper. Never rely on truncated output; if a warning appears, reread all missing ranges in smaller chunks until the entire summary and every question have been read. Do not create helper files; write only your assigned output.\n\nAnswer every question in the input file, including every requested part. Use a separate explicit clause for each requested part; do not compress away rule consequences or exceptions. Lists or tables may be used to keep multi-part answers complete.')
if version=='v3':
 prompt=prompt.replace('Before writing final JSON,', 'Operational completeness: parse the entire assigned questions JSON and compare its actual ID set and count with your final answer array. Every ID present must be answered exactly once. Check both assigned input files through their actual final line, including any unterminated tail. Recover any unread ranges before finalizing. Use only the two assigned inputs and your assigned output; do not create helper files.\n\nBefore writing final JSON,')
for reader in ['a','b']:(d/f'reader-{reader}-prompt.txt').write_text(prompt.format(summary=d/'summary-snapshot.md',questions=d/'questions.json',output=d/f'reader-{reader}.json'))
manifest={'benchmark':benchmark,'prompt_version':('guide-reader-plus-generic-self-check-v3-complete-input-ids' if version=='v3' else 'guide-reader-plus-generic-self-check-v2-bounded-complete-clauses' if version=='v2' else 'guide-reader-plus-generic-self-check-v1'),'requested_model':'gpt-6-luna','requested_effort':'high','files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [s,d/'summary-snapshot.md',d/'questions.json',q/benchmark/'answer-key.json']}}
(d/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(d/'summary-changes.patch').write_text(''.join(difflib.unified_diff((q/'baseline-summary.md').read_text().splitlines(True),s.read_text().splitlines(True),fromfile='baseline',tofile=name)))
st=json.loads((q/'game-status.json').read_text());st.update(phase=name,question_count=len(json.loads((d/'questions.json').read_text())['questions']));st['iterations'].append({'name':name,'benchmark':benchmark,'status':'readers-running'});(q/'game-status.json').write_text(json.dumps(st,indent=2)+'\n')
print(d)
