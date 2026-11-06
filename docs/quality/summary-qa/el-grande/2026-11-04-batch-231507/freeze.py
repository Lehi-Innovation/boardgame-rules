import pathlib,json,hashlib,shutil,sys,difflib
P=pathlib.Path(__file__).resolve().parent;name=sys.argv[1];D=P/name;D.mkdir();canonical=pathlib.Path('/home/jonny/projects/boardgame-rules/rules/el-grande.md')
shutil.copy(canonical,D/'summary-snapshot.md');shutil.copy(P/'questions.json',D/'questions.json');shutil.copy(P/'answer-key.json',D/'answer-key.json')
paths=[D/'summary-snapshot.md',D/'questions.json',D/'answer-key.json',pathlib.Path('/home/jonny/projects/boardgame-rules/extracted/el-grande-rules.txt'),pathlib.Path('/home/jonny/projects/boardgame-rules/source_pdfs/el-grande-publisher-rules.pdf')]
(D/'input-manifest.json').write_text(json.dumps({'hashes':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},'requested_model':'gpt-6-luna','reasoning_effort':'high'},indent=2))
for r in ['a','b']:
 prompt=f'''You are an independent rules-summary reader in a blind evaluation.
Read ONLY these two input files:
{D}/summary-snapshot.md
{D}/questions.json
Do not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, other files, parent history or web links. Do not browse. Use only the supplied summary as evidence, not prior game knowledge. Do not communicate with other readers.
Answer every question in the input file, including every requested part. Include every requested procedural quantity, timing, cost and destination within each answer. If a requested fact is absent, explicitly identify that part as unsupported; do not guess.
For every question include id, answer, support (supported, partial or unsupported), evidence (a short quote or section from the summary).
Save valid JSON to {D}/reader-{r}.json with top-level fields reader, inputs_read and answers (an array).
You may read only the two allowed inputs and write only your assigned output. Do not create temporary files; validate JSON in memory or without writing another file. Do not evaluate or improve the summary.'''
 (D/f'reader-{r}-prompt.txt').write_text(prompt)
(D/'summary-changes.patch').write_text(''.join(difflib.unified_diff((P/'baseline-summary.md').read_text().splitlines(True),canonical.read_text().splitlines(True),fromfile='baseline-summary.md',tofile='summary-snapshot.md')))
s=json.loads((P/'game-status.json').read_text());s.update(phase=name,status='active',question_count=len(json.loads((D/'questions.json').read_text())['questions']));s['iterations'].append(name);(P/'game-status.json').write_text(json.dumps(s,indent=2))
print(D)
