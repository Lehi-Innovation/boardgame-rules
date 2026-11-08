from pathlib import Path
import difflib
import hashlib
import json
import runpy

R=Path(__file__).parent;canonical=R.parents[4]/'rules/cosmic-encounter.md'
before=canonical.read_text();assert before==(R/'repair-freeze-08.md').read_text();assert hashlib.sha256(before.encode()).hexdigest()=='6d8289ac949020645264acc7dd592f725f8fbafee6cd67634f2f646aa1b02f33'
notes=runpy.run_path(str(R/'assemble_repair.py'),run_name='metadata_only')['notes'];ref,body=notes['Machine']
old='it guarantees a second encounter and permits a new hand if needed'
new='it guarantees a second encounter even after an unsuccessful completed first encounter, and permits a new hand if needed'
assert body.count(old)==1 and before.count(old)==1
after=before.replace(old,new);updated=(ref,body.replace(old,new));assert not (R/'repair-freeze-09.md').exists()
(R/'repair-freeze-09.md').write_text(after)
(R/'repair-freeze-09.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-08.md',tofile='repair-freeze-09.md')))
(R/'source-review/source-corrections-09.json').write_text(json.dumps({'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'old':old,'new':new,'primary_sources':['2018 FAQ p16 1543–1550','2018 FAQ p17 1559–1561 quoted may always have a second encounter'],'scope':'Otherwise legal use and applicability supplied; no full activation window or role inferred.','human_choices_adopted':False},indent=2)+'\n')
canonical.write_text(after)
assembly=R/'assemble_repair.py';s=assembly.read_text();marker='\ndef assemble():';assert s.count(marker)==1;assembly.write_text(s.replace(marker,'\n# Source-backed Machine Wild guarantee consequence, corrections09.\nnotes[\'Machine\']='+repr(updated)+'\n'+marker))
print('repair-freeze-09',len(after),hashlib.sha256(after.encode()).hexdigest())
