from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent
refs={
1:'467-507',2:'589-602;1008-1028',3:'987-998;1235-1250',4:'723-747;1545-1565',5:'1288-1300;1336-1353;1430-1473',6:'1150-1168;1260-1285;3038-3041',7:'1380-1389;1685-1720;1778-1794',8:'1392-1411;1437-1454;1528-1542;1682-1684',9:'815-821;1721-1731',10:'1640-1673',11:'1475-1507',12:'1751-1776;1795-1806;1816-1839;3076-3091',13:'1976-2033;2247-2252',14:'1841-1865;1898-1903',15:'1874-1953',16:'2035-2089',17:'2135-2150;2556-2566;2606-2621;2669-2682',18:'2623-2662',19:'2443-2463;2684-2737;3045-3047',20:'900-958',
21:'438-550;2420-2422;2525-2527',22:'571-655;2374-2382',23:'677-688;703-721;2330-2339',24:'750-838;1918-1920',25:'787-829',26:'879-896;1545-1630',27:'1587-1630',28:'2200-2246',29:'632-635;2232-2235;2270-2276',30:'2330-2373;2741-2749',31:'1203-1210;2283-2329;3038-3041',32:'1180-1202;3038-3041',33:'1102-1120;2090-2121;2506-2518',34:'1584-1586;2405-2422;3045-3047',35:'2423-2429',36:'2068-2089;2437-2442',37:'1087-1092;2420-2422;2430-2436',38:'2464-2475',39:'2476-2505',40:'2528-2547',41:'2548-2555',42:'1654-1660;2567-2573',43:'2574-2583',44:'2584-2598',45:'1351-1353;1528-1544;1599-1601;2599-2621',46:'2750-2773',47:'2774-2808',48:'1608-1611;2809-2834',49:'869-899',50:'2383-2403',51:'1412-1429',52:'1755-1776;1816-1839',53:'935-958;2712-2720',54:'2283-2329',55:'1129-1143',56:'1057-1086',57:'1499-1500;1631-1673'}
D=R/'benchmark-v4';D.mkdir(exist_ok=True)
q=json.loads((R/'benchmark-v3/questions.json').read_text());a=json.loads((R/'benchmark-v3/answer-key.json').read_text());q['benchmark_version']=a['benchmark_version']='benchmark-v4'
corrections=[]
for e in a['answers']:
 i=int(e['id'][1:]);old=e['source_references'];e['source_references']=[{'path':'extracted/nemesis-rules.txt','extraction_lines':refs[i]}]
 if i in [52,54]:e['source_references'].append({'path':'nemesis-original-rules.pdf','printed_pages':[18,19] if i==52 else [23],'basis':'Visual inspection of matching original-edition diagram/icons'})
 corrections.append({'id':e['id'],'old':old,'new':e['source_references'],'answer_changed':False,'question_changed':False})
for n,v in [('questions.json',q),('answer-key.json',a)]: (D/n).write_text(json.dumps(v,indent=2)+'\n')
(D/'question-bank.md').write_text('# Nemesis expanded bank v4\n\nReference-only correction of v3. All question wording and expected-answer strings preserved.\n\n'+'\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n**Expected:** {y['expected_answer']}\n\nSource: {json.dumps(y['source_references'])}" for x,y in zip(q['questions'],a['answers']))+'\n')
(R/'benchmark-corrections.json').write_text(json.dumps({'reason':'Independent seed adjudication identified inaccurate line-range offsets. Evaluator re-indexed every procedural reference against numbered authoritative extraction. Only references corrected; no ruling or question changed. Original v1-v3 files remain historical and immutable.','from':'benchmark-v3','to':'benchmark-v4','corrections':corrections},indent=2)+'\n')
l=json.loads((R/'coverage-ledger.json').read_text())
for i,e in enumerate(l['coverage'],1):e['source_lines']=refs[i]
l['exclusions'][0]['passages']='2837-2984';l['exclusions'][1]['passages']='1-437';l['core_procedural_span']='438-2834;2985-3126 (reference repeats)';l['source_reference_correction']='benchmark-corrections.json';(R/'coverage-ledger.json').write_text(json.dumps(l,indent=2)+'\n')
print('v4: reference correction only; 57 question/answer strings preserved')
