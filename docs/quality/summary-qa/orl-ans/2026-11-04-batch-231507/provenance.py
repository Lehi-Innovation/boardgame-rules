from pathlib import Path
import json
P=Path(__file__).parent;parent='01a1aa59-bae3-71a3-afd7-182f8b7a1490'
found={}
for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11').rglob('*.jsonl'):
 try:
  with p.open() as f:
   meta=json.loads(next(f));m=meta['payload']
   if m.get('parent_thread_id')!=parent or not m.get('agent_path'):continue
   contexts=[]
   for line in f:
    x=json.loads(line)
    if x.get('type')=='turn_context':contexts.append({'timestamp':x['timestamp'],'ordinal':x.get('ordinal'),'type':x['type'],'payload':{k:x['payload'][k] for k in ['turn_id','model','effort'] if k in x['payload']}})
   found[m['agent_path'].split('/')[-1]]={'runtime_session_path':str(p),'session_meta':{'timestamp':meta['timestamp'],'type':'session_meta','payload':{k:m.get(k) for k in ['id','parent_thread_id','agent_path','agent_nickname','model_provider','thread_source']}},'turn_context_records':contexts,'actual_model':contexts[0]['payload'].get('model') if contexts else None,'actual_effort':contexts[0]['payload'].get('effort') if contexts else None}
 except (ValueError,StopIteration):pass
mappings={'seed-iteration-01':{'a':'seed_reader_a','b':'seed_reader_b'},'seed-iteration-02':{'a':'seed_retest_a','b':'seed_retest_b'},'seed-iteration-03':{'a':'seed_final_a','b':'seed_final_b'},'expanded-iteration-01':{},'expanded-iteration-02':{'a':'expanded_reader_a','b':'expanded_reader_b'},'expanded-iteration-03':{'a':'expanded_retest_a','b':'expanded_retest_b'},'expanded-iteration-04':{'a':'expanded_final_a','b':'expanded_final_b'},'expanded-iteration-05':{'a':'expanded_certify_a','b':'expanded_certify_b'},'stamped-iteration-01':{'a':'stamped_reader_a','b':'stamped_reader_b'},'stamped-iteration-02':{'a':'stamped_retest_a','b':'stamped_retest_b'},'stamped-iteration-03':{'a':'stamped_final_a','b':'stamped_final_b'}}
for it,pair in mappings.items():
 if not (P/it).exists():continue
 out={'requested_model':'gpt-6-luna','requested_effort':'high','isolation':'Fresh subagent, fork_turns=none; read-only summary/questions instructions, no stronger filesystem isolation.','readers':{}}
 for who,agent in pair.items():
  if agent in found:
   out['readers'][who]=found[agent];out['readers'][who]['confirmed']=found[agent]['actual_model']=='gpt-6-luna' and found[agent]['actual_effort']=='high'
 (P/it/'model-provenance.json').write_text(json.dumps(out,indent=2)+'\n')
(P/'reviewer-model-provenance.json').write_text(json.dumps({k:v for k,v in found.items() if k not in {a for pair in mappings.values() for a in pair.values()}},indent=2)+'\n')
print({k:(v['actual_model'],v['actual_effort']) for k,v in found.items()})
