from pathlib import Path
import json, hashlib,copy,collections
P=Path(__file__).resolve().parent.parent
I=P/'expanded-iteration-08'
data=json.loads((I/'grading-input.json').read_text());summary=(I/'summary-snapshot.md').read_text()
lines=summary.splitlines(keepends=True);starts=[];pos=0
for line in lines: starts.append(pos);pos+=len(line)
# Explicit per-fact evidence selection, one semicolon-delimited group per required fact.
MAP={
1:'225;225;223,225',2:'203,204,205,206;227;227;227',3:'229;229;229',4:'231,233,234,235,236;235;210,229,233,236,238',5:'214;215,216,217;227',6:'63;63;63;63',7:'74;75;76;77;78',8:'84;84;86;86',9:'94;94;94',10:'91;91;91;91;91,167;92',11:'109,113;107,109;111,115,116;115,116,118;118',12:'120;122;122,124,125;124;125',13:'127;127;127',14:'133;134;134;134;134',15:'134;136;137;137;137',16:'138;138;139;139;139;139;140',17:'133;146;134,147;148;147;138,150;147,149',18:'157,158,159,160,161;163;163',19:'174,176;176;178;178;178',20:'302;303;303;310;310',21:'47;47;49;50;49',22:'46;49;50',23:'48;53;48;49',24:'53;53;53;51',25:'37,38,41;37,38,41;37,38,41;41;42',26:'109,113;244;135;244',27:'246;246,75;135',28:'252;252;252',29:'252;252;248',30:'250;250;250',31:'105;105;105;105;105',32:'91,101;170;170;170;170',33:'169;169;169',34:'182;182;182',35:'184;184;184;184',36:'223;223;140',37:'135;135;135',38:'138,142;140',39:'136;136;136',40:'266;266;248',41:'266;266;266',42:'264;264;264;264',43:'264;264,176;174,176;284,264',44:'180;180;180;180;180',45:'304;304;304;304',46:'304;304;304',47:'305;305;305;305',48:'306;306',49:'306;306;306',50:'307;307;307',51:'308;308;308;308',52:'309;309;309',53:'273;273;273;273',54:'274;274',55:'279;279;279',56:'283;278;274,282,283',57:'282;270;282,283',58:'281,86;281',59:'280,270;280',60:'278;278;278',61:'275;275',62:'276,109;276,109',63:'277,160;163',64:'284;284;284',65:'288;288;288',66:'27;29;29',67:'262;262',68:'70;70',69:'139;124,125',70:'147,149;149;148',71:'178;182,184',72:'63;63',73:'227,167;227',74:'225,233;235,236,238',75:'302;303;303',76:'90;90,250',77:'139;139;139;139',78:'131,137;137',79:'76;76',80:'135;135',81:'286;286,151;286',82:'86;86',83:'39,46;57;57',84:'35,41;41;42',85:'292;292;292',86:'178;178;178',87:'246;246;246',88:'134;199,134',89:'260,250;260',90:'246;138,150',91:'27',92:'63,64,65,66;66',93:'138;140;140',94:'135,252;252',95:'61,248,252;61,78,252;66,252,272',96:'27;27;27',97:'258;258',98:'256',99:'254;254;254;254',100:'254;254',101:'52,53',102:'35,48;35;48;48',103:'39;194;214',104:'304'
}
def dec(sp):
 t=summary[sp['start']:sp['end']]
 assert hashlib.sha256(t.encode()).hexdigest()==sp['sha256_utf8']
 if sp['original_quote_type']=='string':return t
 m=copy.deepcopy(sp['original_quote_metadata']);m['quote']=t;return m

def reconstruct(e):
 e=copy.deepcopy(e)
 e['verbatim_passages']=[dec(s) for s in e.pop('attached_verbatim_passage_spans')]
 e['answer_quotations']=[dec(s) for s in e.pop('answer_quotation_spans')]
 tr=e.pop('answer_transport',None)
 if tr:
  assert tr['mode']=='join_answer_quotations'
  e['answer']=tr['separator'].join(x if isinstance(x,str) else x['quote'] for x in e['answer_quotations'])
 return e

def lineev(e,number):
 a=starts[number-1];b=a+len(lines[number-1].rstrip('\n'))
 for field in ['answer_quotation_spans','attached_verbatim_passage_spans']:
  for i,sp in enumerate(e.get(field,[])):
   if sp['start']<=a and b<=sp['end']:
    return dict(location=('answer_quotations' if field=='answer_quotation_spans' else 'verbatim_passages')+f'[{i}]',excerpt=summary[a:b],span_if_quote=dict(start=a,end=b,summary_line=number))
 return None

# Semantic adjudications of every selected fact group. s = satisfied, m = missing.
DECISIONS="""
001 sss/sss
002 ssss/ssss
003 sss/sss
004 sss/sss
005 sss/sss
006 ssss/ssss
007 sssss/sssss
008 ssss/ssss
009 sss/sss
010 ssssss/ssssss
011 sssss/sssss
012 sssss/sssss
013 sss/sss
014 sssss/sssss
015 sssss/sssss
016 sssssss/sssssss
017 sssssss/sssssss
018 sss/sss
019 sssss/sssss
020 sssss/sssss
021 sssss/sssss
022 sss/sss
023 ssss/ssss
024 ssss/ssss
025 sssss/sssss
026 ssss/ssss
027 sss/sss
028 sss/sss
029 sss/sss
030 sss/sss
031 sssss/sssss
032 sssss/mssss
033 sss/sss
034 sss/sss
035 ssss/ssss
036 sss/ssm
037 sss/sss
038 ss/ss
039 sss/sss
040 sss/sss
041 sss/sss
042 ssss/ssss
043 ssss/ssms
044 sssss/sssss
045 ssss/ssss
046 sss/sss
047 ssss/ssss
048 ss/ss
049 sss/sss
050 sss/sss
051 ssss/ssss
052 sss/sss
053 ssss/ssss
054 ss/ss
055 sss/sss
056 sss/sss
057 sss/sss
058 ms/ss
059 ss/ss
060 sss/sss
061 ss/ss
062 mm/ss
063 ss/ss
064 sss/sss
065 sss/sss
066 sss/sss
067 ss/ss
068 ss/ss
069 ss/ss
070 sss/sss
071 ss/ss
072 ss/ss
073 ss/ss
074 ss/ss
075 sss/sss
076 ss/ss
077 ssss/ssss
078 ss/ss
079 ss/ss
080 ss/ss
081 sss/sss
082 ss/ss
083 sss/sss
084 sss/mmm
085 sss/sss
086 sss/sss
087 sss/sss
088 sm/ss
089 ss/ss
090 ss/ss
091 s/s
092 ss/ss
093 sss/sss
094 ms/ss
095 sss/sss
096 sss/mmm
097 ss/ss
098 s/s
099 ssss/ssss
100 ss/ss
101 s/s
102 ssss/ssss
103 sss/sss
104 s/s
"""
# Equivalent evidence choices avoid demanding redundant explanations or unrelated quote locations.
OVERRIDES={
('Q004','reader-a',3):[229,233,236,238],('Q005','reader-b',3):[210,219],
('Q010','reader-a',5):[90,91,92],('Q010','reader-b',5):[90,91,92],
('Q043','reader-b',2):[264,284],('Q073','reader-b',1):[227],
('Q076','reader-b',2):[90],('Q081','reader-a',2):[286],
('Q083','reader-a',1):[39],('Q095','reader-a',2):[61,252],
('Q095','reader-a',3):[66,252],('Q095','reader-b',1):[61],
('Q095','reader-b',2):[61],('Q095','reader-b',3):[66,272]
}
MISSING={
('Q032','reader-b',1):'The entry lists play/discard of a facedown adviser but does not state the restriction on voluntary faceup-adviser discard. Its attached minor-action passage does not contain that requested prohibition.',
('Q036','reader-b',3):'The title-transfer passage states incumbent ties and Oathkeeper-side transfer, but gives no end-of-Campaign timing rule. The requested prohibition on transfer during temporary mid-Campaign rule losses is unresolved.',
('Q043','reader-b',3):'The attached general-power and site passages describe binding promises and Tribunal, but do not state that only a Citizenship offer may exchange a Reliquary relic.',
('Q058','reader-a',1):'The entry states pawn-local draw-one-fewer, but supplies neither the ordinary Search draw count nor the requested ordinary result of two cards. This required fact group is only partly covered.',
('Q062','reader-a',1):'The River passage supplies the conditional additional one warband, but the entry supplies neither the ordinary Muster base of two nor the required ordinary River total of three. This fact group is incomplete.',
('Q062','reader-a',2):'The conditional River bonus does not state the ordinary Muster gain of two when the player does not rule River. No attached Muster rule supplies that missing result.',
('Q084','reader-b',1):'The entry quotes later-game saved-world setup, not first-game assigned advisers or preservation of Packet B order. No explicit application of the later procedure to the first-game scenario is volunteered, so the requested facts are missing rather than contradicted.',
('Q084','reader-b',2):'The later-game passage gives three total bottom-deck seeds, not the first-game 3/3/5 regional discard allocation and remaining 41 ordered world-deck cards. It does not resolve the requested first-game procedure.',
('Q084','reader-b',3):'The later-game passage gives random Reliquary preparation, not the first-game Ivory Eye at Mountain, next four packet relics and remaining 15 packet relics. The first-game procedure is unresolved.',
('Q088','reader-a',2):'The Campaign passage supplies title bonuses and shared Imperial defense, but not the Supremacy rule that collective Imperial site holdings earn the physical title for Chancellor. That requested conjunct is missing.',
('Q094','reader-a',1):'The powers passage permits either eligible role to choose either sign and names box colors as the role-permission source, but does not define gradient as usable by attacker and defender. The gradient role permission remains unstated.',
('Q096','reader-b',1):'The attached overview concerns roles, victory, Chronicle and scope. It gives no site/card rule criterion or application to Red at a purple site versus the remote red garrison.',
('Q096','reader-b',2):'The overview does not state that pawn movement leaves site garrisons and the basis of rule unchanged.',
('Q096','reader-b',3):'The overview does not state the one-warband-color-per-site restriction or prohibit red/purple coexistence.'
}
SUPPLEMENT={
('Q038','reader-a',1):['numerical_application.equation','case_result'],
('Q038','reader-b',1):['numerical_application.equation'],
('Q038','reader-a',2):['case_result'],('Q038','reader-b',2):['case_result'],
('Q063','reader-a',1):['case_result','numerical_application.equation'],
('Q063','reader-a',2):['case_result'],('Q063','reader-b',1):['case_result','numerical_application.equation'],
('Q063','reader-b',2):['case_result'],('Q072','reader-a',1):['case_result','numerical_application.equation'],
('Q072','reader-b',1):['case_result','numerical_application.equation'],
('Q072','reader-a',2):['case_result'],('Q072','reader-b',2):['case_result'],
('Q073','reader-a',1):['case_result'],('Q073','reader-b',1):['case_result']
}
def fieldev(e,path):
 v=e
 for k in path.split('.'):v=v[k]
 assert isinstance(v,str)
 return dict(location=path,excerpt=v)

def execute():
 receipts=[]
 for name in ['grading-input.json','summary-snapshot.md']:
  text=(I/name).read_text();sha=hashlib.sha256((I/name).read_bytes()).hexdigest();offset=0
  matches=sorted((P/'delivery-audit').glob('grader08-'+name.replace('.','-')+'-*.json'))
  for f in matches:
   rec=json.loads(f.read_text());assert rec['start']==offset and rec['end']-rec['start']<=5000
   assert rec['sha256']==sha and rec['chunk_sha256']==hashlib.sha256(text[rec['start']:rec['end']].encode()).hexdigest()
   offset=rec['end'];receipts.append(str(f))
  assert offset==len(text)
 statuses={f'Q{n}':v.split('/') for n,v in (line.split() for line in DECISIONS.splitlines() if line.strip())}
 assert set(statuses)=={q['id'] for q in data['questions']}
 results=dict(benchmark_version='expanded-v11',iteration=8,status='complete',method='Fresh independent strict semantic grading of all 208 entries and 656 frozen required fact groups. Complete packet and summary delivered model-visible before grading in contiguous <=5000-character BEGIN/END chunks. Reconstructed full original entries; assessed all fields and same-entry attached verbatim passages as operative answers. No prior grades/history consulted. No cross-entry borrowing, exact-keyword demand, or label-based credit. Concrete numerical cases assessed using actual substituted results. Contextual exclusions respected.',inputhashes={x['path']:x['sha256'] for x in data['inputs']},delivery_receipt={'artifacts':receipts,'packet_characters':315182,'summary_characters':47341,'chunks':len(receipts),'max_chunk_characters':5000,'max_chunks_per_exec':2,'all_output_inspected_complete':True,'truncations':0,'format_deviations':[]},questions_graded=208,fact_assessments=656,readers=[],gold_or_scope_defects=[])
 decisions=[]
 for ri,r in enumerate(['reader-a','reader-b']):
  out=[]
  raw=json.loads((I/(r+'.json')).read_text());rawentries={e['id']:e for e in raw['answers']}
  for q in data['questions']:
   e=q['readers'][r];rec=reconstruct(e);assert rec==rawentries[q['id']]
   groups=MAP[int(q['id'][1:])].split(';');st=statuses[q['id']][ri]
   assert len(groups)==len(st)==len(q['required_facts'])
   checks=[];missing=[]
   for j,(f,g,c) in enumerate(zip(q['required_facts'],groups,st),1):
    k=(q['id'],r,j);ns=OVERRIDES.get(k,[int(n) for n in g.split(',')])
    ev=[v for n in ns if (v:=lineev(e,n))]
    ev.extend(fieldev(e,p) for p in SUPPLEMENT.get(k,[]))
    status={'s':'satisfied','m':'missing','c':'contradiction'}[c]
    if status=='satisfied':assert ev,(k,'missing evidence')
    if status=='missing':
     assert k in MISSING;k_reason=MISSING[k];missing.append(k_reason)
    else:k_reason='The selected same-entry quotation(s) state the requested rule and its conditions; all conjuncts were assessed against the frozen fact group.'
    checks.append(dict(fact_id=f['fact_id'],expected_fact=f['expected_fact'],status=status,evidence=ev,assessment=k_reason))
   grade='partial' if missing else 'correct'
   reason=' '.join(missing) if missing else 'Every requested fact group is resolved by the quoted procedures/rows and any case fields in this entry; no material contradiction was found.'
   out.append(dict(id=q['id'],question=q['question'],expected_answer_from_fixed_key=q['fixed_expected_answer'],observed_answer=rec['answer'],grade=grade,reason=reason,fact_checks=checks,attached_quote_spans=e['attached_verbatim_passage_spans'],material_contradictions=[]))
   decisions.append(dict(reader=r,id=q['id'],fact_ids=[f['fact_id'] for f in q['required_facts']],explicit_status_sequence=st,grade=grade))
  counts=collections.Counter(x['grade'] for x in out);fc=collections.Counter(f['status'] for x in out for f in x['fact_checks'])
  results['readers'].append(dict(reader=r,totals={k:counts[k] for k in ['correct','partial','incorrect']}|{'total':104},fact_totals={k:fc[k] for k in ['satisfied','missing','contradiction']}|{'total':328},questions=out))
 (I/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 (P/'delivery-audit/grader08-decisions.json').write_text(json.dumps(decisions,indent=2)+'\n')
 return results
if __name__=='__main__':
 res=execute()
 print(json.dumps([{k:r[k] for k in ['reader','totals','fact_totals']} for r in res['readers']],indent=2))
