"""Versioned source-only Markdown units and parent-side literal checks; no QA key."""
from pathlib import Path
import hashlib,json,re,sys
METHOD='recognized-atx-1to6-subtrees-and-introductions-v1'

def units(text):
    # Deliberately narrow, frozen lexer. Actual source has no fenced code.
    if re.search(r'(?m)^ {0,3}(?:```|~~~)',text):
        raise ValueError('Fenced code is outside this lexer; preserve input for explicit method review')
    if '<!-- qa-unit:' in text:
        raise ValueError('Reserved attachment marker occurs in source')
    headings=list(re.finditer(r'(?m)^(#{1,6}) (.+)$',text));result={};stack=[]
    for index,match in enumerate(headings):
        level=len(match.group(1));start=match.start();line=text[:start].count('\n')+1
        while stack and stack[-1][0]>=level:stack.pop()
        ancestors=[('T'+str(n).zfill(3),title) for lev,n,title in stack if lev>=2]
        intro_end=headings[index+1].start() if index+1<len(headings) else len(text)
        subtree_end=next((later.start() for later in headings[index+1:] if len(later.group(1))<=level),len(text))
        if level>=2:
            for prefix,kind,end in [('I','introduction',intro_end),('T','subtree',subtree_end)]:
                uid=prefix+str(line).zfill(3);slice_=text[start:end]
                result[uid]=dict(section_id=uid,kind=kind,heading=match.group(),level=level,
                    start_offset=start,end_offset=end,start_line=line,
                    end_line=line+slice_.count('\n')-(1 if slice_.endswith('\n') else 0),
                    sha256=hashlib.sha256(slice_.encode()).hexdigest(),
                    parent_section_id=ancestors[-1][0] if ancestors else None,
                    ancestor_headings=[title for _,title in ancestors],text=slice_)
        stack.append((level,line,match.group()))
    return result

def start_marker(uid):return '<!-- qa-unit:'+uid+':begin -->\n'
def end_marker(uid):return '<!-- qa-unit:'+uid+':end -->'
def attachment(unit):return start_marker(unit['section_id'])+unit['text']+end_marker(unit['section_id'])

def check_data(text,questions,raw,role):
    index=units(text);qmap={q['id']:q['question'] for q in questions};ids=[a['id'] for a in raw['answers']];rows=[]
    for entry in raw['answers']:
        errors=[];qid=entry['id'];selected=entry.get('operative_sections',[]);selected_ids=[s['section_id'] for s in selected]
        if qid not in qmap:errors.append('unknown question ID')
        if len(selected_ids)!=len(set(selected_ids)):errors.append('duplicate selected unit ID')
        intervals=[];positions=[]
        for supplied in selected:
            uid=supplied['section_id'];expected=index.get(uid)
            if expected is None:errors.append('unknown source unit '+uid);continue
            for field in ['kind','heading','level','start_offset','end_offset','start_line','end_line','sha256']:
                if supplied.get(field)!=expected[field]:errors.append(uid+' mismatched '+field)
            begin=start_marker(uid);end=end_marker(uid);answer=entry.get('answer','')
            if answer.count(begin)!=1 or answer.count(end)!=1:
                errors.append(uid+' attachment markers must each occur exactly once')
            else:
                a=answer.index(begin)+len(begin);b=answer.index(end)
                if b<a or answer[a:b]!=expected['text']:errors.append(uid+' identified full attachment differs from exact source slice')
                positions.append((expected['start_offset'],answer.index(begin)))
            intervals.append((expected['start_offset'],expected['end_offset'],uid))
        ordered=sorted(intervals)
        for previous,current in zip(ordered,ordered[1:]):
            if previous[1]>current[0]:errors.append('overlapping selected source units '+previous[2]+'/'+current[2])
        if [p[1] for p in sorted(positions)]!=sorted(p[1] for p in positions):errors.append('attachments not in source order')
        ledger=entry.get('clause_ledger',[])
        if not ledger:errors.append('empty asked-clause ledger')
        quote_checks=[]
        for n,clause in enumerate(ledger,1):
            ce=[];kind=clause.get('fact_kind');uid=clause.get('fact_source_section');fact=clause.get('supported_fact_or_case_result','')
            request=clause.get('requested_clause','')
            if not request or request not in qmap.get(qid,''):ce.append('requested clause not literal question phrase')
            if not set(clause.get('section_ids',[]))<=set(selected_ids):ce.append('clause references unselected source unit')
            if not isinstance(fact,str) or not fact.strip():ce.append('empty/nontext fact or abstention')
            if kind=='quote':
                if uid not in selected_ids or uid not in clause.get('section_ids',[]):ce.append('fact source not selected/referenced')
                if uid not in index or not isinstance(fact,str) or not fact or fact not in index[uid]['text']:ce.append('fact is not exact source span')
                if uid in index and isinstance(fact,str) and fact.strip()==index[uid]['text'].strip():ce.append('whole unit substituted for individual fact')
            elif kind!='unsupported':ce.append('fact_kind must be quote or unsupported')
            quote_checks.append(dict(clause_number=n,errors=ce))
        rows.append(dict(id=qid,selected_units=selected_ids,boundary_attachment_errors=errors,
            fact_quote_checks=quote_checks,all_structure_and_declared_source_spans_valid=not errors and all(not x['errors'] for x in quote_checks)))
    return dict(method=METHOD,reader=role,question_count=len(questions),answer_count=len(ids),
        exact_ordered_unique_ids=ids==list(qmap) and len(ids)==len(set(ids)),
        all_structure_and_declared_source_spans_valid=all(row['all_structure_and_declared_source_spans_valid'] for row in rows),checks=rows,
        limits='Parent-only structural/literal proof. Does not prove relevance, asked-fact completeness, calculations or factual correctness. Never creates a content-score cap.')

def check(run,role):
    return check_data((run/'summary-snapshot.md').read_text(),json.loads((run/'questions.json').read_text())['questions'],
        json.loads((run/f'reader-{role}.json').read_text()),role)

if __name__=='__main__':
    run=Path(sys.argv[1]);out=run/sys.argv[2];assert not out.exists(),'Preserve earlier verification attempts'
    data={role:check(run,role) for role in 'ab'};out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({role:{k:v for k,v in result.items() if k!='checks'} for role,result in data.items()},indent=2))
