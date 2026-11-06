from pathlib import Path
import json,sys
b=Path(__file__).parent.parent
q=json.loads((b/'expanded-v10-complete-user-scope/questions.json').read_text())['questions'];a=json.loads((b/'expanded-v10-complete-user-scope/answer-key.json').read_text())['answers'];s=json.loads((b/'expanded-v10-complete-user-scope/requested-fact-scope-reviewed.json').read_text())['questions']
nums=[int(x) for x in sys.argv[1:]]
assert len(nums)<=5
for n in nums:
 i=n-1
 print(json.dumps({'q':q[i],'key':a[i]['expected_answer'],'source':a[i]['source_references'],'facts':s[i]['material_requested_facts'],'extras':s[i]['contextual_key_extras']},ensure_ascii=False))
with (Path(__file__).parent/'bank-read-log.jsonl').open('a') as f:f.write(json.dumps({'ids':[q[n-1]['id'] for n in nums],'bounded_q_key_objects':2*len(nums)})+'\n')
