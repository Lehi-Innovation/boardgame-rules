from pathlib import Path
import json,hashlib,shutil,sys,difflib,re
D=Path(__file__).resolve().parent
version,it=sys.argv[1:3];v=D/version;t=D/it
prompt_variant=sys.argv[5] if len(sys.argv)>5 else 'v4'
assert prompt_variant in ['v4','v5']
clause_guidance='Write each answer as separate numbered clauses, with one clause for each part asked by the question. Each clause should explicitly resolve that part from the summary.' if prompt_variant=='v4' else 'Write each answer as separate numbered clauses, explicitly covering every requested part and every named alternative. Make the scope of conditions clear within that answer; do not leave the reader to infer which alternative a qualifier applies to.'
delivery=D/sys.argv[3]/'questions.json' if len(sys.argv)>3 else v/'questions.json'
if it.startswith(('expanded-','integrated-')):
 assert len(sys.argv)>3, 'Full-bank readers require an explicit neutral reader-only payload'
 payload=json.loads(delivery.read_text())
 assert set(payload)=={'game','scope','version','questions'}
 assert payload['game']=='Ark Nova'
 assert all(set(q)=={'id','question'} for q in payload['questions'])
 assert payload['questions']==json.loads((v/'questions.json').read_text())['questions']
 assert re.fullmatch(r'r[0-9]{2}',payload['version']), 'Reader version must remain opaque'
 assert payload['scope']=='Original English base game; optional solo mode and expansions excluded.'
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
tracker=json.loads((D/'canonical-write-tracker.json').read_text())
assert h('rules/ark-nova.md')==tracker['expected_sha256'], 'Canonical bytes changed outside the recorded repair/stamp sequence'
primary=json.loads((D/'neutral-source-manifest.json').read_text())['sources']
assert all(h(s['path'])==s['sha256'] for s in primary), 'Authoritative source changed'
t.mkdir()
shutil.copyfile('rules/ark-nova.md',t/'summary-snapshot.md')
shutil.copyfile(delivery,t/'questions.json')
source=json.loads((D/'input-manifest.json').read_text())
manifest={'benchmark':version,'hashes':{str(p):h(p) for p in [t/'summary-snapshot.md',t/'questions.json',v/'answer-key.json']},'sources':source['hashes'],'requested_model':'gpt-6-luna','requested_effort':'high','reader_prompt_version':'guide+generic-self-check+complete-input+numbered-parts-v4' if prompt_variant=='v4' else 'guide+generic-self-check+complete-input+numbered-parts-and-cases-v5'}
if delivery!=v/'questions.json':
 manifest['reader_question_payload']={'path':str(delivery),'sha256':h(delivery),'accepted_bank_path':str(v/'questions.json'),'accepted_bank_sha256':h(v/'questions.json'),'question_objects_identical':True,'metadata':f"neutral game/scope/opaque {json.loads(delivery.read_text())['version']} only; delivery sanitation record preserved separately"}
for name in ['material-requested-facts.json','coverage-map.json','shared-source-lookup-facts.json','novelty-rejection-ledger.json','benchmark-freeze-manifest.json']:
 p=v/name
 if p.exists():manifest['hashes'][str(p)]=h(p)
manifest['authoritative_sources']={s['path']:h(s['path']) for s in primary}
scope_index=D/sys.argv[4] if len(sys.argv)>4 else D/'grading-request-scope-01.json'
if scope_index.exists():manifest['hashes'][str(scope_index)]=h(scope_index)
manifest['grading_scope_path']=str(scope_index)
(t/'input-manifest.json').write_text(json.dumps(manifest,indent=2))
(t/'summary-changes.patch').write_text(''.join(difflib.unified_diff((D/'original-summary.md').read_text().splitlines(True),(t/'summary-snapshot.md').read_text().splitlines(True),fromfile='original-summary',tofile=it)))
for r in 'ab':
 prompt=f'''You are an independent rules-summary reader in a blind evaluation.

Read ONLY these two input files:
{t/'summary-snapshot.md'}
{t/'questions.json'}

Read both allowed inputs completely in bounded chunks. If any tool output is truncated, reread the missing ranges before answering. A heading list or search matches alone do not establish a complete read.

Do not read any authoritative rulebook, extracted text, answer key,
manifest, prior responses, other files, parent history or web links.
Do not browse. Use only the supplied summary as evidence, not prior
game knowledge. Do not communicate with other readers.

Answer every question in the input file, including every requested part. If a requested
fact is absent, explicitly identify that part as unsupported; do not guess.

Make each answer a complete, standalone response to the question. Use as much detail as needed to resolve every requested part; do not shorten it by relying on another answer or on rules you assume the reader knows.

{clause_guidance}

For every question include:
- id
- answer
- support: supported, partial or unsupported
- evidence: a short quote or section from the summary

Before writing final JSON, reread every question and review your draft answer on your own; explicitly resolve every requested part from the supplied summary, including requested quantities, timing, costs, destinations and exceptions; do not borrow a missing fact from another answer; identify unsupported parts instead of guessing; check volunteered rulings for contradictions with the summary.

Save valid JSON to {t/f'reader-{r}.json'} with
top-level fields reader, inputs_read and answers (an array).
You may read only the two allowed inputs and write only your assigned
output. Do not evaluate or improve the summary.
'''
 (t/f'reader-{r}-prompt.txt').write_text(prompt)
print(t)
