from pathlib import Path
import json,hashlib,re
R=Path(__file__).parent;proof=json.loads((R/'runtime-provenance.json').read_text());by={x['task']:x for x in proof['agents']}
pairs={'seed-iteration-01':['/root/seed_reader_a','/root/seed_reader_b'],'seed-iteration-02':['/root/seed_reader2_a','/root/seed_reader2_b'],'expanded-iteration-03':['/root/expanded_reader_a','/root/expanded_reader_b','/root/final_grader_block1','/root/final_grader_block2'],'expanded-iteration-05':['/root/expanded_reader2_a','/root/expanded_reader2_b','/root/final_grader2_block1','/root/final_grader2_block2'],'expanded-iteration-06':['/root/expanded_reader3_a','/root/expanded_reader3_b','/root/final_grader3_block1','/root/final_grader3_block2'],'expanded-iteration-10':['/root/expanded_reader6_a','/root/expanded_reader6_b'],'stamped-iteration-02':['/root/expanded_reader10_a','/root/expanded_reader10_b','/root/final_grader10_block1','/root/final_grader10_block2'],'stamped-iteration-01':['/root/expanded_reader9_a','/root/expanded_reader9_b','/root/final_grader9_block1','/root/final_grader9_block2'],'expanded-iteration-13':['/root/expanded_reader8_a','/root/expanded_reader8_b','/root/final_grader8_block1','/root/final_grader8_block2'],'expanded-iteration-11':['/root/expanded_reader7_a','/root/expanded_reader7_b','/root/final_grader7_block1','/root/final_grader7_block2'],'expanded-iteration-09':['/root/expanded_reader5_a','/root/expanded_reader5_b','/root/final_grader5_block1','/root/final_grader5_block2'],'expanded-iteration-08':['/root/expanded_reader4_a','/root/expanded_reader4_b','/root/final_grader4_block1','/root/final_grader4_block2']}
for folder,tasks in pairs.items():
 (R/folder/'model-provenance.json').write_text(json.dumps({'root_provenance_path':str((R/'runtime-provenance.json').resolve()),'agents':[by[x] for x in tasks if x in by]},indent=2)+'\n')
checks=[]
for task in by:
 if task=='/root':continue
 if task not in by:continue
 a=by[task];reads=[];out=[]
 for i,l in enumerate(Path(a['runtime_source_path']).read_bytes().splitlines()):
  o=json.loads(l);p=o.get('payload',{});name=p.get('name')
  metadata_names=['list_agents','read_thread','list_threads','list_archived_threads','wait_threads','wait_agent']
  normalized=(name or '').split('__')[-1].split('.')[-1]
  if o['type']=='response_item' and normalized in metadata_names:
   reads.append({'name':name,'ordinal':i,'record_sha256':hashlib.sha256(l).hexdigest(),'call_form':'direct'})
  elif o['type']=='response_item' and normalized=='exec':
   code=p.get('arguments',p.get('input',''))
   for found in re.finditer(r'tools\.([A-Za-z0-9_]*(?:list_agents|read_thread|list_threads|list_archived_threads|wait_threads|wait_agent))\s*\(',code):
    reads.append({'name':found.group(1),'ordinal':i,'record_sha256':hashlib.sha256(l).hexdigest(),'call_form':'nested exec tool invocation'})
  elif o['type']=='response_item' and name=='send_message':
   x=json.loads(p['arguments']);out.append({'target':x.get('target'),'ordinal':i,'record_sha256':hashlib.sha256(l).hexdigest()})
 checks.append({'task':task,'agent_or_chat_metadata_reads':reads,'outbound_coordination_to_parent':out,'note':'Outbound progress to parent does not read reader/grade metadata. Reads and declared exposure tracked separately.'})
(R/'independence-tool-check.json').write_text(json.dumps(checks,indent=2)+'\n')
print({'per_iteration_views':len(pairs),'metadata_reads':{x['task']:len(x['agent_or_chat_metadata_reads']) for x in checks}})
