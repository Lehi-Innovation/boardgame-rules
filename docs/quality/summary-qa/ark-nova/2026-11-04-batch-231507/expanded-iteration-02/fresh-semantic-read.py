from pathlib import Path
import json,sys
p=Path(__file__).parents[1]
def read(f):return json.loads((p/f).read_text())
files={'Q':read('expanded-iteration-02/questions.json')['questions'],'K':read('benchmark-v2/answer-key.json')['answers'],'F':read('benchmark-v2/material-requested-facts.json'),'S':read('grading-request-scope-01.json')['questions'],'A':read('expanded-iteration-02/reader-a.json')['answers'],'B':read('expanded-iteration-02/reader-b.json')['answers'],'GA':read('expanded-iteration-02/independent-grade-a.json')['judgments'],'GB':read('expanded-iteration-02/independent-grade-b.json')['judgments']}
M={k:({v['id']:v for v in d} if isinstance(d,list) else d) for k,d in files.items()}
summary=(p/'expanded-iteration-02/summary-snapshot.md').read_text();lines=summary.splitlines()
# Exact string backreferences only; no content is summarized or suppressed.
cache={line:f'L{i+1}' for i,line in enumerate(lines) if len(line)>30}
keys={'question':'q','expected_answer':'key','source_references':'src','material_requested_facts':'facts','requested_parts':'parts','requestedparts':'parts','unrequested_context':'context','observedquote':'obs','observed_quote':'obs','summarysupportquote':'sup','summary_support_quote':'sup','summary_support_lines':'lines','observedquote_scope':'obs_scope','explanation':'note','overallgrade':'grade','overall_grade':'grade','context_volunteered_ruling_check':'extra','context_and_volunteered_ruling_check':'extra','unrequested_key_context':'keycontext','material_false_or_contradictory_volunteered_rule_found':'false','unsupported_volunteered_rule_found':'unsupported','support_lines_for_answer_and_extras':'supportlines','checked_complete_answer':'allchecked','unrequested_context_omissions_not_penalized':'contextok'}
def norm(x,path):
 if isinstance(x,str):
  if len(x)>30 and x in cache:return '@'+cache[x]
  if len(x)>30 and x in summary:
   off=summary.index(x);return '@L'+str(summary[:off].count('\n')+1)+'[exact substring]'
  if len(x)>30:cache[x]=path
  return x
 if isinstance(x,list):return [norm(v,path+'.'+str(i)) for i,v in enumerate(x)]
 if isinstance(x,dict):return {keys.get(k,k):norm(v,path+'.'+keys.get(k,k)) for k,v in x.items()}
 return x
start,end=map(int,sys.argv[1:])
for i,q in enumerate(files['Q'],1):
 id=q['id'];bundle={k:norm(d[id],id+'.'+k) for k,d in M.items()}
 if start<=i<=end:
  print('POSITION',i,id)
  for k,v in bundle.items():print(k,json.dumps(v,ensure_ascii=False,separators=(',',':')))
