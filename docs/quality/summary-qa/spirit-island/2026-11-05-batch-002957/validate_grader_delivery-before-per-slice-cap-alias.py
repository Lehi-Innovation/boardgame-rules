"""Verify every grader received the five exact, complete bounded inputs."""
from pathlib import Path
import json,hashlib,sys
D=Path(sys.argv[1]).resolve();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
for block in sorted((D/'grading').glob('block-*')):
 m=json.loads((block/'input-manifest.json').read_text());g=json.loads((block/'grades.json').read_text());declared=g['inputs_read'];allowed={str(Path(p).resolve()):v for p,v in m['inputs'].items()};seen=[];rows=[]
 for x in declared:
  p=Path(x.get('path',x.get('file',''))).resolve();name=str(p);seen.append(name);s=p.read_text();ranges=next((x[k] for k in ['read_ranges','complete_read_ranges','ranges','delivered_character_ranges','complete_read_ranges_zero_based_half_open'] if k in x),[])
  pairs=[(c['start'],c.get('end',c.get('end_exclusive'))) if isinstance(c,dict) else tuple(c) for c in ranges]
  complete=bool(pairs) and pairs[0][0]==0 and pairs[-1][1]==len(s) and all(a[1]==b[0] for a,b in zip(pairs,pairs[1:]))
  bounded=all(isinstance(a,int) and isinstance(z,int) and 0<z-a<=6000 for a,z in pairs)
  cap=next((x[k] for k in ['output_cap_tokens','max_output_tokens_per_call','per_call_output_cap_tokens','tool_output_cap_tokens'] if k in x),None)
  truncated=any(x.get(k,False) for k in ['truncated','truncation_observed','source_output_truncated'])
  match=name in allowed and H(p)==allowed[name]['sha256']==x['sha256']
  rows.append({'path':name,'sha256':H(p),'characters':len(s),'ranges':pairs,'complete':complete,'bounded':bounded,'input_hash_match':match,'output_cap_when_declared':cap,'truncation':truncated,'pass':match and complete and bounded and not truncated and (isinstance(cap,int) and cap>=4000)})
 exact=set(seen)==set(allowed) and len(seen)==len(allowed)==5
 checks.append({'block':block.name,'grades_sha256':H(block/'grades.json'),'manifest_sha256':H(block/'input-manifest.json'),'exact_five_input_set':exact,'inputs':rows,'pass':exact and all(x['pass'] for x in rows)})
out={'checks':checks,'all_passed':bool(checks) and all(x['pass'] for x in checks),'scope':'Verifies declared complete input delivery, exact frozen hashes, bounded ranges and declared caps. Actual tool-call transcripts and actual-model records are retained independently; declarations alone are not proof of permitted filesystem enforcement.'};p=D/'grader-delivery-validation.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'blocks':len(checks),'all_passed':out['all_passed'],'failures':[x['block'] for x in checks if not x['pass']]}))
