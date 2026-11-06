"""Parent-only v5 structure/literal checks. Does not grade meaning or relevance."""
from pathlib import Path
import importlib.util,json,sys
SPEC=importlib.util.spec_from_file_location('section_check',Path(__file__).with_name('summary-section-check.py'))
BASE=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(BASE)

def check(run,role):
    result=BASE.check(run,role)
    index=BASE.sections((run/'summary-snapshot.md').read_text())
    entries=json.loads((run/f'reader-{role}.json').read_text())['answers'];by_id={e['id']:e for e in entries}
    for row in result['checks']:
        entry=by_id[row['id']];selected={s['section_id'] for s in entry.get('operative_sections',[])}
        quote_checks=[]
        for n,clause in enumerate(entry.get('clause_ledger',[]),1):
            kind=clause.get('fact_kind');sid=clause.get('fact_source_section');fact=clause.get('supported_fact_or_case_result','');errors=[]
            if kind=='quote':
                if sid not in selected or sid not in clause.get('section_ids',[]):errors.append('fact source not selected/referenced')
                if not fact or sid not in index or fact not in index[sid]['text']:errors.append('fact is not exact source span')
                if sid in index and fact.strip()==index[sid]['text'].strip():errors.append('whole section used instead of short clause fact')
            elif kind=='unsupported':
                if not fact:errors.append('unsupported clause lacks explicit statement')
            else:errors.append('fact_kind must be quote or unsupported')
            quote_checks.append(dict(clause_number=n,fact_kind=kind,fact_source_section=sid,errors=errors))
        row['fact_quote_checks']=quote_checks
        row['all_declared_facts_literal_or_explicitly_unsupported']=all(not c['errors'] for c in quote_checks)
    result['all_declared_facts_literal_or_explicitly_unsupported']=all(row['all_declared_facts_literal_or_explicitly_unsupported'] for row in result['checks'])
    result['limits']='Format/literal source checks only. Relevance, completeness, calculations, contradictions and all-substantive-field factual correctness require separate independent grading.'
    return result

if __name__=='__main__':
    run=Path(sys.argv[1]);out=run/sys.argv[2];assert not out.exists(),'Preserve all prior validation attempts'
    data={role:check(run,role) for role in 'ab'};out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({role:{k:v for k,v in d.items() if k!='checks'} for role,d in data.items()},indent=2))
