"""Generic exact heading-boundary checks; no rule key or expected answers."""
from pathlib import Path
import hashlib,json,re,sys

def sections(text):
    starts=list(re.finditer(r'(?m)^#{2,6} .+$',text));result={}
    for index,match in enumerate(starts):
        start=match.start();end=starts[index+1].start() if index+1<len(starts) else len(text)
        line=text[:start].count('\n')+1;slice_=text[start:end];sid='H'+str(line).zfill(3)
        result[sid]=dict(section_id=sid,heading=match.group(),start_line=line,
            end_line=line+slice_.count('\n')-(1 if slice_.endswith('\n') else 0),
            sha256=hashlib.sha256(slice_.encode()).hexdigest(),text=slice_)
    return result

def check(run,role):
    text=(run/'summary-snapshot.md').read_text();index=sections(text)
    questions=json.loads((run/'questions.json').read_text())['questions'];qmap={q['id']:q['question'] for q in questions}
    raw=json.loads((run/f'reader-{role}.json').read_text());answer_ids=[a['id'] for a in raw['answers']];rows=[]
    for entry in raw['answers']:
        errors=[];selected=entry.get('operative_sections',[]);ids=[s['section_id'] for s in selected]
        if entry['id'] not in qmap:errors.append('unknown question ID')
        if len(ids)!=len(set(ids)):errors.append('duplicate section selection')
        for supplied in selected:
            sid=supplied['section_id'];expected=index.get(sid)
            if not expected:errors.append('unknown section '+sid);continue
            for field in ['heading','start_line','end_line','sha256']:
                if supplied.get(field)!=expected[field]:errors.append(sid+' mismatched '+field)
            copies=entry['answer'].count(expected['text'].rstrip())
            if copies!=1:errors.append(sid+' complete section copy count '+str(copies)+' instead of one')
        ledger=entry.get('clause_ledger',[])
        if not ledger:errors.append('empty asked-clause ledger')
        for clause in ledger:
            if not clause.get('requested_clause') or clause['requested_clause'] not in qmap.get(entry['id'],''):errors.append('requested_clause is not literal question phrase')
            if not clause.get('supported_fact_or_case_result'):errors.append('empty fact/result')
            if not set(clause.get('section_ids',[]))<=set(ids):errors.append('clause references missing sections')
        rows.append(dict(id=entry['id'],selected_sections=ids,complete_heading_boundaries_and_literal_copies=not errors,errors=errors))
    return dict(reader=role,question_count=len(questions),answer_count=len(answer_ids),exact_ordered_ids=answer_ids==list(qmap),
        all_selected_sections_complete=all(not row['errors'] for row in rows),checks=rows,
        limits='Structural/literal checks only. Requested-fact correctness and section relevance require separate independent grading.')

if __name__=='__main__':
    run=Path(sys.argv[1]);out=run/sys.argv[2];assert not out.exists(),'Preserve prior validation attempts'
    data={role:check(run,role) for role in 'ab'};out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({role:{k:v for k,v in d.items() if k!='checks'} for role,d in data.items()},indent=2))
