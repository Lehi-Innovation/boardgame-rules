from pathlib import Path
import sys,json,shutil,hashlib
P=Path(__file__).resolve().parent;R=P.parents[4];I=P/sys.argv[1];B=P/sys.argv[2];review=P/sys.argv[3]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
canonical=R/'rules/unmatched.md';audit=P/(sys.argv[5] if len(sys.argv)>5 else 'source-audit-02/source-audit.json');a=json.loads(audit.read_text());assert a['verdict']=='PASS' and not a['findings'];assert a['summary_sha256']==sha(canonical)==sha(audit.parent/'summary-snapshot.md')
assert review.is_file();bm=json.loads((B/'input-manifest.json').read_text());assert all(sha(B/n)==v for n,v in bm['hashes'].items())
I.mkdir(exist_ok=False);shutil.copyfile(canonical,I/'summary-snapshot.md');shutil.copyfile(B/'questions.json',I/'questions.json')
protocol=sys.argv[4] if len(sys.argv)>4 else 'reader-protocol-v2'
T=P/protocol/'prompt-template.txt';template=T.read_text();prompts={}
protocol_manifest=P/protocol/'protocol-manifest.json'
protocol_version=json.loads(protocol_manifest.read_text())['version'] if protocol_manifest.exists() else 'v2-complete-operative-units'
for r in ['a','b']:
 f=I/f'reader-{r}-prompt.txt';rendered=template.replace('{summary}',str(I/'summary-snapshot.md')).replace('{questions}',str(I/'questions.json')).replace('{output}',str(I/f'reader-{r}.json'));f.write_text(rendered);prompts[str(f)]=sha(f)
# Pair messages must differ only in assigned output filename.
assert (I/'reader-a-prompt.txt').read_text().replace('reader-a.json','READER.json')==(I/'reader-b-prompt.txt').read_text().replace('reader-b.json','READER.json')
source_paths=json.loads((P/'progress.json').read_text())['source_paths'];sources={x:sha(Path(x)) for x in source_paths}
manifest={'benchmark':B.name,'question_count':len(json.loads((I/'questions.json').read_text())['questions']),'model':'gpt-6-luna','effort':'high','fork_turns':'none','protocol_version':protocol_version,'hashes':{str(f):sha(f) for f in [I/'summary-snapshot.md',I/'questions.json',B/'answer-key.json',B/'scope-map.json',review,audit,T,P/'reader-protocol-v2/validate_operative_units.py']},'prompt_hashes':prompts,'authoritative_source_hashes':sources,'source_audit_exact_byte_match':True,'scope_review_path':str(review),'reader_isolation':'Only frozen summary/question inputs; own assigned output allowed for assembly; no stronger OS-level filesystem isolation asserted.'}
(I/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(I/'grading-scope-reference.json').write_text(json.dumps({'key':str(B/'answer-key.json'),'scope':str(B/'scope-map.json'),'all_ids_fixed':True,'true_contextual_key_background_not_additional_required_facts':True,'no_unrelated_source_gap_caps':True},indent=2)+'\n')
print(I);print(manifest['question_count'],sha(I/'summary-snapshot.md'));print('Frozen prompt hashes:',prompts)
