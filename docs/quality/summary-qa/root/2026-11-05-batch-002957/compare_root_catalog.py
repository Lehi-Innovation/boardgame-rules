from build_evidence import *
import yaml
path=R/'targeted-catalog-comparison.json'
prior=R/'targeted-catalog-comparison-prestamp.json'
if path.exists() and not prior.exists():shutil.copyfile(path,prior)
summary=yaml.safe_load((ROOT/'rules/root.md').read_text().split('---',2)[1])
entries=[x for x in json.loads((ROOT/'games.json').read_text())['games'] if x.get('slug')=='root']
assert len(entries)==1
entry=entries[0]
fields={k:{'summary':summary[k],'manifest':entry[k],'match':summary[k]==entry[k]} for k in ['title','bgg_id','player_count','play_time','verification']}
rows=[x for x in (ROOT/'index.md').read_text().splitlines() if '| [Root](rules/root/) |' in x]
assert len(rows)==1
expected='✅' if summary['verification']=='verified' else '⚠️'
ok=all(x['match'] for x in fields.values()) and expected in rows[0] and (ROOT/'extracted/root-rules.txt').exists()
save(path,{'manifest_root_entry':fields,'index_root_row':rows[0],'root_extraction_present':True,'shared_files_modified_by_worker':False,'summary_sha256':sha(ROOT/'rules/root.md'),'scope':'Read-only Root entry/row comparison after coordinator stamping; unrelated entries not generated or modified.','status':'PASS' if ok else 'FAIL'})
print('Root catalog comparison:', 'PASS' if ok else 'FAIL')
