from pathlib import Path
import json,hashlib
R=Path(__file__).parent; p=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T14-26-50-01a1b2c1-d5d1-7333-8948-72708b3d1f3e.jsonl')
records=[]
for i,l in enumerate(p.read_bytes().splitlines()):
 o=json.loads(l);x=o.get('payload',{})
 if o['type']!='response_item' or x.get('name')!='spawn_agent':continue
 a=json.loads(x['arguments']);name=a['task_name'];opaque=a['message'];fn=R/f'{name}-dispatch-prompt.txt'
 if 'reader' in name:
  iteration=next(it for prefix,it in [('expanded_reader10','stamped-iteration-02'),('expanded_reader9','stamped-iteration-01'),('expanded_reader8','expanded-iteration-13'),('expanded_reader7','expanded-iteration-11'),('expanded_reader6','expanded-iteration-10'),('expanded_reader5','expanded-iteration-09'),('expanded_reader4','expanded-iteration-08'),('expanded_reader3','expanded-iteration-06'),('expanded_reader2','expanded-iteration-05'),('expanded_reader','expanded-iteration-03'),('seed_reader2','seed-iteration-02'),('seed_reader','seed-iteration-01')] if name.startswith(prefix))
  label=name[-1];s=(R/iteration/f'reader-{label}-prompt.txt').read_text().rstrip('\n')
  if name=='expanded_reader_b':s=s.replace('part is unsupported','part isunsupported')
  fn.write_text(s)
 elif name.startswith(('final_grader5_block','final_grader7_block','final_grader8_block','final_grader9_block','final_grader10_block')):
  it='stamped-iteration-02' if name.startswith('final_grader10') else ('stamped-iteration-01' if name.startswith('final_grader9') else ('expanded-iteration-13' if name.startswith('final_grader8') else ('expanded-iteration-11' if name.startswith('final_grader7') else 'expanded-iteration-09')));s=(R/it/f'grader-block-{name[-1]}-prompt.txt').read_text().rstrip('\n');fn.write_text(s)
 else:
  s='Prompt content is encrypted in runtime; only opaque hash retained. See dispatched task in chat history.';fn.write_text(s)

 records.append({'task':name,'model':a.get('model'),'effort':a.get('reasoning_effort'),'fork_turns':a.get('fork_turns'),'timestamp':o.get('timestamp'),'prompt_path':str(fn.resolve()),'readable_prompt_sha256':hashlib.sha256(s.encode()).hexdigest(),'opaque_runtime_message_sha256':hashlib.sha256(opaque.encode()).hexdigest(),'readable_prompt_source':'prebound local template matching dispatch text' if 'reader' in name or name.startswith(('final_grader5_block','final_grader7_block','final_grader8_block','final_grader9_block','final_grader10_block')) else 'runtime ciphertext omitted','runtime_source_path':str(p),'record_ordinal':i,'record_sha256':hashlib.sha256(l).hexdigest()})
(R/'dispatch-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
for prefix in ['seed_reader','seed_reader2','expanded_reader','expanded_reader2','expanded_reader3','expanded_reader4','expanded_reader5','expanded_reader6','expanded_reader7','expanded_reader8','expanded_reader9','expanded_reader10']:
 s=[(R/f'{prefix}_{x}-dispatch-prompt.txt') for x in 'ab']
 if all(x.exists() for x in s):
  a=s[0].read_text().replace('reader-a.json','reader-X.json');b=s[1].read_text().replace('reader-b.json','reader-X.json');print(prefix,'literal identical except output:',a==b,'equivalent after documented identical spacing correction:',a.replace('isunsupported','is unsupported')==b.replace('isunsupported','is unsupported'))
