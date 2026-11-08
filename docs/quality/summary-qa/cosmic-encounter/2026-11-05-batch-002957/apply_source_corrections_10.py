from pathlib import Path
import difflib
import hashlib
import json

R=Path(__file__).parent;canonical=R.parents[4]/'rules/cosmic-encounter.md'
before=canonical.read_text();assert before==(R/'repair-freeze-09.md').read_text();assert hashlib.sha256(before.encode()).hexdigest()=='b9c67dfbe3655b3a0bbfbdd5a035e38a8949542aea1304eefea647075068d6de'
old='ships “lost to warp” actually reach it.'
new='ships “lost to warp” actually reach it involuntarily at some point in the encounter.'
assert before.count(old)==1;after=before.replace(old,new)
assert not (R/'repair-freeze-10.md').exists()
(R/'repair-freeze-10.md').write_text(after)
(R/'repair-freeze-10.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-09.md',tofile='repair-freeze-10.md')))
(R/'source-review/source-corrections-10.json').write_text(json.dumps({'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'old':old,'new':new,'primary_source':'2018 FAQ p3 extraction205–220 lost/losing/sent definitions','reason':'Make the published involuntary-arrival qualifier explicit; the immediately following sentence retains the source exception that sent ships may be voluntary and count as lost.','question_or_key_changed':False,'human_choices_adopted':False},indent=2,ensure_ascii=False)+'\n')
canonical.write_text(after)
core=R/'core-repair-draft.md';s=core.read_text();assert s.count(old)==1;core.write_text(s.replace(old,new))
print('repair-freeze-10',len(after),hashlib.sha256(after.encode()).hexdigest())
