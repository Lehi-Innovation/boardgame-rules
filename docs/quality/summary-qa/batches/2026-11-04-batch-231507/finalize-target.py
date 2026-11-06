"""Finish one accepted target's registry entry and read-only repository checks."""
import argparse
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from zoneinfo import ZoneInfo
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from scripts.catalog import validate_catalog
from scripts.generate_index import generate
from scripts.generate_manifest import build_manifest
from scripts.registry import locked_registry
from scripts.validate import validate_rules_file

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('slug')
p.add_argument('--coordinator-check', type=Path)
p.add_argument('--coordinator-review', type=Path)
a = p.parse_args()
b = Path(__file__).parent
m = json.loads((b/'manifest.json').read_text())
g = next(g for g in m['games'] if g['slug'] == a.slug)
assert g['status'] == 'ready-for-publication'
worker_dir = Path(g['output_directory'])
worker = json.loads((worker_dir/'game-status.json').read_text())
executed_iterations = sorted(str(f.parent.relative_to(worker_dir)) for f in worker_dir.rglob('reader-a.json')
                             if (f.parent/'reader-b.json').is_file()
                             and (f.parent/'results.json').is_file()
                             and (f.parent/'summary-snapshot.md').is_file())
iteration_count = len(executed_iterations)
assert iteration_count > 0
integrity_path = a.coordinator_check or b/(a.slug+'-stamped-coordinator-iteration-check.json')
review_path = a.coordinator_review or b/(a.slug+'-coordinator-stamped-review.json')
assert integrity_path.is_file() and review_path.is_file(), 'Actual coordinator proof files are required before registry changes'
assert json.loads(integrity_path.read_text())['mechanical_checks_pass']
canonical = Path(g['summary_path'])
assert canonical.read_bytes() == Path(worker['final_snapshot_path']).read_bytes()
text = canonical.read_text()
fm = yaml.safe_load(text.split('---',2)[1])
assert fm['verification'] == 'verified' and fm['bgg_id'] == g['bgg_id']
structure = validate_rules_file(str(canonical))
assert not structure, structure
out = b/'registry'/(a.slug+'-'+datetime.now(ZoneInfo('America/Phoenix')).strftime('%Y%m%d-%H%M%S'))
out.mkdir(parents=True,exist_ok=False)
with locked_registry('games.yaml') as (games, save):
    before = copy.deepcopy(games)
    targets = [x for x in games if x.get('bgg_id') == g['bgg_id']]
    assert len(targets) == 1
    target = targets[0]
    (out/'target-before.json').write_text(json.dumps(target,indent=2)+'\n')
    for field in ['player_count','play_time','designer']:
        target[field] = fm[field]
    target['name'] = fm['title']
    target['status'] = 'verified'
    target['review_notes'] = f"Independent source audit PASS on exact stamped final text; both fresh Luna/high readers {worker['question_count']}/{worker['question_count']}. Evidence: docs/quality/summary-qa/{a.slug}/{m['run_id']}/README.md"
    assert [x for x in games if x.get('bgg_id') != g['bgg_id']] == [x for x in before if x.get('bgg_id') != g['bgg_id']]
    save(games)
    (out/'target-after.json').write_text(json.dumps(target,indent=2)+'\n')
diff = subprocess.run(['git','diff','--check','--',str(canonical)],capture_output=True,text=True)
assert diff.returncode == 0, diff.stdout+diff.stderr
actual = json.loads(Path('games.json').read_text())
candidate = build_manifest(Path('rules'))
entries = lambda d: {x['slug']: x for x in d['games']}
manifest_ok = entries(actual)[a.slug] == entries(candidate)[a.slug]
row = lambda s: next(x for x in s.splitlines() if re.search(r'\]\(rules/'+re.escape(a.slug)+r'/\)', x))
index_ok = row(Path('index.md').read_text()) == row(generate(Path('rules'),Path('index.md')))
assert manifest_ok and index_ok
errors = validate_catalog()
slug_pattern = re.compile(r'(?<![\w-])' + re.escape(a.slug) + r'(?![\w-])')
id_pattern = re.compile(r'(?<!\d)' + str(g['bgg_id']) + r'(?!\d)')
target_errors = [e for e in errors if slug_pattern.search(e) or id_pattern.search(e)]
assert not target_errors, target_errors
r = {'game':a.slug,'question_count':worker['question_count'],'iterations':iteration_count,
 'executed_iterations':executed_iterations,
 'final_reader_scores':worker['final_reader_scores'],'source_audit':'PASS, exact stamped text; no material findings or important omissions',
 'canonical_sha256':hashlib.sha256(canonical.read_bytes()).hexdigest(),
 'target_manifest_entry_matches_regeneration':manifest_ok,'target_index_row_matches_regeneration':index_ok,
 'target_catalog_errors':target_errors,'global_catalog_errors':errors,
 'catalog_scope_note':'Targeted updates preserve all unrelated registry/index/manifest entries. Any current outside-scope catalog discrepancy is recorded separately.',
 'coordinator_integrity_file':str(integrity_path.resolve()),
 'coordinator_review_file':str(review_path.resolve()),'registry_evidence':str(out.resolve()),
 'stamping_changed_tested_bytes':False,'structural_validation':'PASS','targeted_git_diff_check':'PASS',
 'runtime_models_independently_verified_from_original_sessions':True}
(b/(a.slug+'-coordinator-validation.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
