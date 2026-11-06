from pathlib import Path
import ast, json
import fitz
D = Path(__file__).resolve().parent
provenance = json.loads((D/'model-provenance.json').read_text())

def flatten(value):
    if isinstance(value, list):
        return '\n'.join(flatten(x) for x in value)
    if isinstance(value, dict):
        if value.get('type') in ['input_image', 'image', 'image_url']:
            return ''
        return '\n'.join(flatten(value[k]) for k in ['text','output','content'] if k in value)
    if isinstance(value, str):
        if value[:1] in '[{':
            for parser in [json.loads, ast.literal_eval]:
                try:
                    parsed = parser(value)
                except Exception:
                    continue
                wrapper = isinstance(parsed, dict) and any(k in parsed for k in ['text','output','content'])
                blocks = isinstance(parsed, list) and all(isinstance(x, dict) and 'type' in x for x in parsed)
                if wrapper or blocks:
                    return flatten(parsed)
        return value
    return ''

def images(value):
    if isinstance(value, list): return sum(images(x) for x in value)
    if isinstance(value, dict):
        return int(value.get('type') in ['input_image','image','image_url']) + sum(images(v) for k,v in value.items() if k not in ['data','image_url'])
    if isinstance(value, str) and value[:1] in '[{':
        for parser in [json.loads,ast.literal_eval]:
            try:return images(parser(value))
            except Exception:pass
    return 0

calls = {}
trace = []
all_calls = []
for line in Path(provenance['runtime_file']).open():
    record = json.loads(line)
    p = record.get('payload',{})
    if record.get('type') != 'response_item':continue
    if p.get('type') == 'custom_tool_call':
        item = {'call_id':p['call_id'],'name':p.get('name'),'input':p.get('input','')}
        all_calls.append(item)
        if not any(x in item['input'] for x in ['write_text','json.dump']):calls[p['call_id']] = item
    if p.get('type') == 'custom_tool_call_output' and p.get('call_id') in calls:
        text = flatten(p.get('output'))
        trace.append({**calls[p['call_id']],'visible_text':text,'image_count':images(p.get('output')),'initial_truncation_marker':'truncat' in text.lower()})
normal = '\n'.join(x['visible_text'] for x in trace)
for _ in range(4):normal = normal.replace('\\n','\n').replace('\\"','"').replace("\\'", "'")
packet = json.loads((D/'cases.json').read_text())
checks = {'question_visible':packet['question']['question'] in normal,'key_visible':packet['fixed_key']['expected_answer'] in normal}
for response in packet['responses']:
    for field in ['answer','evidence']:
        checks[response['response_id']+'_'+field+'_visible'] = response['raw_response'][field] in normal
missing_summary = [n for n,line in enumerate((D/'summary-snapshot.md').read_text().splitlines(),1) if line.strip() and line not in normal]
source = Path('/home/jonny/projects/boardgame-rules/extracted/dune-imperium-rules.txt')
missing_setup = [n for n,line in enumerate(source.read_text().splitlines(),1) if 155<=n<=168 and line.strip() and line not in normal]
pdf = fitz.open('/home/jonny/projects/boardgame-rules/source_pdfs/dune-imperium-rules.pdf')
missing_pdf = {str(i+1):[n for n,line in enumerate(pdf[i].get_text().splitlines(),1) if line.strip() and line not in normal] for i in [3,4]}
checks.update(complete_summary_visible=not missing_summary,complete_setup_text_visible=not missing_setup,complete_pdf_setup_pages_visible=not any(missing_pdf.values()),two_setup_images_returned=sum(x['image_count'] for x in trace)==2,actual_sol_high_fork_none=provenance['actual_spawn_configuration']['fork_turns']=='none' and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in provenance['contexts']))
audit = {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'runtime_file':provenance['runtime_file'],'missing_summary_lines':missing_summary,'missing_setup_lines':missing_setup,'missing_pdf_page_lines':missing_pdf,'initial_truncation_recovered':any(x['initial_truncation_marker'] for x in trace) and not missing_summary,'unresolved_missing_input':not all(checks.values()),'actual_tool_calls':all_calls,'method':'Inspected actual returned text, bounded recovery ranges and image returns; exact relevant text presence supplements range inspection. JSON source documents are retained as visible text, not discarded as tool wrappers.'}
(D/'actual-input-read-trace.json').write_text(json.dumps(trace,indent=2,ensure_ascii=False)+'\n')
(D/'input-read-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in audit.items() if k not in ['actual_tool_calls']},indent=2))
