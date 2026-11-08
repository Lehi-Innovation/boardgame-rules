"""Check current primary grader input availability against original runtime outputs."""
import argparse, ast, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--iteration',type=int,required=True)
args=parser.parse_args()
assert args.iteration>=9
label=f'{args.iteration:02d}'
B=Path(__file__).resolve().parent
G=B.parents[4]/'docs/quality/summary-qa/spirit-island'/B.name
D=G/('expanded-iteration-'+label)
J=lambda p:json.loads(p.read_text())
H=lambda x:hashlib.sha256(x).hexdigest()
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text())
fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='strings')
ns={'json':json}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
strings=ns['strings']
parent_path=D/'grader-actual-delivery-validation.json'
declared=J(parent_path)
profiles={x['agent']:x for x in J(G/'model-provenance.json')}
files=subprocess.run(['rg','--files','/mnt/c/Users/jonny/.codex/sessions'],capture_output=True,text=True,check=True).stdout.splitlines()
checks=[]
for grader in declared['graders']:
    ident=profiles[grader['agent']]['thread_id']
    runtime=Path(next(x for x in files if x.endswith(ident+'.jsonl')))
    lines=runtime.read_bytes().splitlines(keepends=True)
    outputs,writers=[],[]
    for n,line in enumerate(lines,1):
        row=json.loads(line)
        p=row.get('payload',{})
        if row['type']=='response_item':
            if p.get('type') in ['function_call_output','custom_tool_call_output']:
                outputs.append((n,H(line),list(strings(p.get('output')))))
            if p.get('type') in ['function_call','custom_tool_call']:
                code=p.get('input',p.get('arguments',''))
                if 'grades.json' in code and any(x in code for x in ['write_text','writeFile','apply_patch','json.dump']):
                    writers.append(n)
        if row['type']=='event_msg' and p.get('type')=='item_completed':
            item=p.get('item',{})
            if item.get('type')=='CommandExecution':
                outputs.append((n,H(line),list(strings(item.get('aggregated_output','')))))
    assert writers,grader['agent']
    boundary=min(writers)
    parts=[]
    for f in grader['inputs']:
        path=Path(f['path'])
        body=path.read_text()
        assert H(path.read_bytes())==f['sha256'] and len(body)==f['characters']
        cursor=0
        for c in f['slices']:
            a,z=c['range']
            assert a==cursor and a<z<=len(body) and H(body[a:z].encode())==c['slice_sha256']
            piece=body[a:z]
            escaped=json.dumps(piece,ensure_ascii=False)[1:-1]
            matches=[{'record':n,'raw_record_sha256':digest} for n,digest,vals in outputs if n<boundary and any(piece in v or escaped in v for v in vals)]
            assert matches,(grader['agent'],path.name,a,z)
            parts.append({'input_path':str(path),'range':[a,z],'sha256':c['slice_sha256'],'actual_private_runtime_outputs_before_first_grade_writer':matches})
            cursor=z
        assert cursor==len(body)
    assert len(grader['inputs'])==5
    block=grader['agent'].rsplit('_',1)[-1]
    grade=D/'grading'/('block-'+block)/'grades-original-completed.json'
    assert H(grade.read_bytes())==grader['grade_sha256']
    checks.append({'agent':grader['agent'],'id':ident,'runtime':str(runtime),'runtime_sha256_at_check':H(runtime.read_bytes()),'first_grade_writer':boundary,'grade_sha256':H(grade.read_bytes()),'whole_input_count':5,'parts':parts})
assert len(checks)==9
out=B/'coordinator-checks'/('spirit-expanded'+label+'-all9-primary-actual-delivery.json')
assert not out.exists()
result={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'parent_delivery_report':str(parent_path),'parent_delivery_report_sha256':H(parent_path.read_bytes()),'graders':checks,'whole_inputs':45,'source_ranges':sum(len(x['parts']) for x in checks),'limits':'Every whole frozen input slice independently matched in original private runtime outputs before first grade writer. Public event numbering remains separate. No private bodies copied, new semantic vote, factual cap or source/stamp/publication approval.'}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verified':True,'graders':9,'whole_inputs':45,'ranges':result['source_ranges'],'proof':str(out)}))
