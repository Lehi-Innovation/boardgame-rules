"""Versioned source-only Markdown units and parent-side literal checks; no QA key."""
from pathlib import Path
import hashlib,json,re,sys
METHOD='recognized-atx-1to6-subtrees-and-introductions-v2-quote-or-paraphrase'

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
    from collections import Counter
    index=units(text)
    question_ids=[q['id'] for q in questions]
    if not all(isinstance(q,str) for q in question_ids) or len(question_ids)!=len(set(question_ids)):
        raise ValueError('Question IDs require explicit format review; input preserved')
    qmap={q['id']:q['question'] for q in questions}
    answers=raw.get('answers',[])
    if not isinstance(answers,list):raise ValueError('answers must be a list; input preserved')
    ids=[a.get('id') if isinstance(a,dict) else None for a in answers];rows=[]
    for original in answers:
        entry=original if isinstance(original,dict) else {}
        errors=[];qid=entry.get('id');qtext=qmap.get(qid,'') if isinstance(qid,str) else ''
        if not isinstance(original,dict):errors.append('non-object answer entry')
        if not isinstance(qid,str):errors.append('nontext question ID')
        elif qid not in qmap:errors.append('unknown question ID')
        selected=entry.get('operative_sections',[])
        if not isinstance(selected,list):errors.append('operative_sections must be a list');selected=[]
        selected_ids=[s.get('section_id') for s in selected if isinstance(s,dict) and isinstance(s.get('section_id'),str)]
        if len(selected_ids)!=len(set(selected_ids)):errors.append('duplicate selected unit ID')
        answer=entry.get('answer','')
        if not isinstance(answer,str):errors.append('answer must be text');answer=''
        # Every reserved marker is accounted for, including unknown/dangling syntax.
        marker_matches=list(re.finditer(r'<!-- qa-unit:(.*?) -->',answer))
        if answer.count('<!-- qa-unit:')!=len(marker_matches):errors.append('malformed or unterminated reserved marker')
        observed=[]
        for match in marker_matches:
            parsed=re.fullmatch(r'([TI][0-9]{3,}):(begin|end)',match.group(1))
            if parsed is None:errors.append('malformed reserved marker payload');continue
            uid,side=parsed.groups();observed.append((uid,side))
            if uid not in selected_ids or uid not in index:errors.append('unknown or unselected attachment marker '+uid)
        expected_markers=[(uid,side) for uid in selected_ids for side in ['begin','end']]
        if Counter(observed)!=Counter(expected_markers):errors.append('reserved marker set differs from declared units')
        intervals=[];positions=[];matched_blocks=[];expected_units=[]
        for supplied in selected:
            if not isinstance(supplied,dict):errors.append('non-object source-unit metadata');continue
            uid=supplied.get('section_id')
            if not isinstance(uid,str):errors.append('nontext selected unit ID');continue
            expected=index.get(uid)
            if expected is None:errors.append('unknown source unit '+uid);continue
            expected_units.append(expected)
            for field in ['kind','heading','level','start_offset','end_offset','start_line','end_line','sha256']:
                if supplied.get(field)!=expected[field]:errors.append(uid+' mismatched '+field)
            begin=start_marker(uid);end=end_marker(uid)
            if answer.count(begin)!=1 or answer.count(end)!=1:
                errors.append(uid+' attachment markers must each occur exactly once')
            else:
                left=answer.index(begin);right=answer.index(end);content_start=left+len(begin)
                if right<content_start or answer[content_start:right]!=expected['text']:
                    errors.append(uid+' identified full attachment differs from exact source slice')
                else:matched_blocks.append((left,right+len(end)))
                positions.append((expected['start_offset'],left))
            intervals.append((expected['start_offset'],expected['end_offset'],uid))
        ordered=sorted(intervals)
        for previous,current in zip(ordered,ordered[1:]):
            if previous[1]>current[0]:errors.append('overlapping selected source units '+previous[2]+'/'+current[2])
        if [p[1] for p in sorted(positions)]!=sorted(p[1] for p in positions):errors.append('attachments not in source order')
        # Mask valid identified blocks first: disjoint ID-distinct units with
        # identical source text remain valid; unmarked long duplicates do not.
        outside=list(answer)
        for left,right in matched_blocks:outside[left:right]=' '*(right-left)
        outside=''.join(outside)
        for expected in expected_units:
            if expected['text'].rstrip() in outside:errors.append(expected['section_id']+' unmarked duplicate complete source unit')
        ledger=entry.get('clause_ledger',[])
        if not isinstance(ledger,list):errors.append('clause_ledger must be a list');ledger=[]
        if not ledger:errors.append('empty asked-clause ledger')
        quote_checks=[]
        for n,clause in enumerate(ledger,1):
            ce=[]
            if not isinstance(clause,dict):
                quote_checks.append(dict(clause_number=n,errors=['non-object clause']));continue
            kind=clause.get('fact_kind');uid=clause.get('fact_source_section');fact=clause.get('supported_fact_or_case_result','');request=clause.get('requested_clause','')
            if not isinstance(request,str) or not request or request not in qtext:ce.append('requested clause not literal question phrase')
            refs=clause.get('section_ids',[])
            if not isinstance(refs,list) or any(not isinstance(x,str) for x in refs):ce.append('nontext or invalid source-reference IDs');refs=[]
            if not set(refs)<=set(selected_ids):ce.append('clause references unselected source unit')
            if not isinstance(fact,str) or not fact.strip():ce.append('empty/nontext fact or abstention')
            if kind in ['quote','paraphrase']:
                if not isinstance(uid,str):ce.append('nontext fact source ID');expected=None
                else:expected=index.get(uid)
                if not isinstance(uid,str) or uid not in selected_ids or uid not in refs:ce.append('fact source not selected/referenced')
                if kind=='quote' and (expected is None or not isinstance(fact,str) or not fact or fact not in expected['text']):ce.append('fact is not exact source span')
                if expected is not None and isinstance(fact,str) and fact.strip()==expected['text'].strip():ce.append('whole unit substituted for individual fact')
            elif kind!='unsupported':ce.append('fact_kind must be quote, paraphrase or unsupported')
            quote_checks.append(dict(clause_number=n,fact_kind=kind,paraphrase_meaning_requires_independent_grading=kind=='paraphrase',errors=ce))
        rows.append(dict(id=qid,selected_units=selected_ids,boundary_attachment_errors=errors,
            fact_quote_checks=quote_checks,all_structure_and_declared_source_spans_valid=not errors and all(not x['errors'] for x in quote_checks)))
    return dict(method=METHOD,reader=role,question_count=len(questions),answer_count=len(ids),
        exact_ordered_unique_ids=all(isinstance(x,str) for x in ids) and ids==question_ids and len(ids)==len(set(ids)),
        all_structure_and_declared_source_spans_valid=all(row['all_structure_and_declared_source_spans_valid'] for row in rows),checks=rows,
        limits='Parent-only structural proof and exact spans ONLY for quote-kind facts. Paraphrases require valid declared selected source references and nonempty facts, but their truth, relevance, qualifiers and asked-fact completeness require independent semantic grading. No content-score cap from technical format.')

def check(run,role):
    return check_data((run/'summary-snapshot.md').read_text(),json.loads((run/'questions.json').read_text())['questions'],
        json.loads((run/f'reader-{role}.json').read_text()),role)

if __name__=='__main__':
    run=Path(sys.argv[1]);out=run/sys.argv[2];assert not out.exists(),'Preserve earlier verification attempts'
    data={role:check(run,role) for role in 'ab'};out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({role:{k:v for k,v in result.items() if k!='checks'} for role,result in data.items()},indent=2))
