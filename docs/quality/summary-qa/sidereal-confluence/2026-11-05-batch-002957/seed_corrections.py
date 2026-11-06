from build_bank import *
def corrected_seed():
    for e in entries:
        q=e['id']; fs=e['required_facts']
        if q=='Q01':
            fs[-1]['fact']='Immediate invention allowed before Economy'; e['contextual_background'].append('Other Trade abilities may also be used at this boundary; not separately asked.')
        if q=='Q02':
            e['contextual_background'] += [x['fact'] for x in fs[:2]]; e['required_facts']=fs[2:]
        if q=='Q05':
            e['contextual_background'] += ['Target flips; each spent card can upgrade only one card.']; e['required_facts']=[x for x in fs if x['id']!='Q05.F03']; e['required_facts'][1]['fact']='Spent card goes underneath target'
        if q=='Q08':
            e['expected_answer'] += ' Colony bids reveal simultaneously when ready; research bids reveal simultaneously after colony resolution. Equal bids: fewer cards of that type, then higher species tiebreaker.'
            fs += [{'id':'Q08.F06','fact':'Each bid type reveals simultaneously: colony when ready, research after colony resolution'},{'id':'Q08.F07','fact':'Equal bids use fewer relevant cards, then higher species tiebreak'}]
        if q=='Q20':
            e['contextual_background'] += ['Each stealing converter targets exactly one player.',fs[-1]['fact']]; e['required_facts']=fs[:-1]; e['required_facts'][1]['fact']='No two stealing converters against same player in one turn'
        if q=='Q04':e['source_references'].append('Yengii front Secretive')
    return entries
if __name__=='__main__':
    import copy
    old=copy.deepcopy(entries); corrected_seed(); write('seed-v2',entries)
    changes=[]
    for before,after in zip(old,entries):
        if before!=after:changes.append({'id':after['id'],'before':before,'after':after})
    (ROOT/'seed-v2'/'correction-record.json').write_text(json.dumps({'reason':'Independent pre-reader source/scope review; no reader outputs existed or informed correction. Seed-v1 retained intact.','review':'../seed-v1/scope-review.json','question_wording_changed':False,'expected_answer_changes':['Q08: add simultaneous reveals and ordinary bid tie resolution to broad how-resolved answer'],'mapping_changes':changes},ensure_ascii=False,indent=2)+'\n')
