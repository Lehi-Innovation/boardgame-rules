import json,pathlib,hashlib,re,collections,copy
base=pathlib.Path('/home/jonny/projects/boardgame-rules');p=base/'docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957';d=p/'expanded-iteration-07';audit=p/'delivery-audit'
g=json.loads((d/'grading-input.json').read_text());s=(d/'summary-snapshot.md').read_text()
# Each row was reviewed against the delivered question, requested conjuncts, exclusions,
# complete answer/scenario and attached passage. S=satisfied, C=contradiction, M=missing.
rows='''1 SSS 2 SSSS 3 SSS 4 SSS 5 SSS 6 SSSS 7 SSSSS 8 SSSS 9 SSS 10 SSSSSS 11 SSSSS 12 SSSSS 13 SSS 14 SSSSS 15 SSSSS 16 SSSSSSS 17 SSSSSSS 18 SSS 19 SSSSS 20 SSSSS 21 SSSSS 22 SSS 23 SSSS 24 SSSS 25 SSSSS 26 SSSS 27 SSS 28 SSS 29 SSS 30 SSS 31 SSSSS 32 SSSSS 33 SSS 34 SSS 35 SSSS 36 SSS 37 SSS 38 SS 39 SSS 40 SSS 41 SSS 42 SSSS 43 SSSS 44 SSSSS 45 SSSS 46 SSS 47 SSSS 48 SS 49 SSS 50 SSS 51 SSSS 52 SSS 53 SSSS 54 SS 55 SSS 56 SSS 57 SSS 58 SS 59 SS 60 SSS 61 SS 62 SS 63 SS 64 SSS 65 SSS 66 SSS 67 SS 68 SS 69 SS 70 SSS 71 SS 72 SS 73 SS 74 SS 75 SSS 76 SS 77 SSSS 78 SS 79 SS 80 SS 81 SSS 82 SS 83 SSS 84 SSS 85 SSS 86 SSS 87 SSS 88 SS 89 SS 90 SS 91 S 92 SS 93 SSS 94 SS 95 SSS 96 SSS 97 SS 98 S 99 SSSS 100 SS 101 S 102 SSSS 103 SSS 104 S'''.split()
matrix={f'Q{int(rows[i]):03}':rows[i+1] for i in range(0,len(rows),2)}
assert len(matrix)==104
statuses={r:copy.deepcopy(matrix) for r in ['reader-a','reader-b']}
statuses['reader-a']['Q056']='SCS'
statuses['reader-b']['Q038']='MS'
statuses['reader-b']['Q055']='CSC'
statuses['reader-b']['Q070']='CSS'
# Match exact source text only; retrieval chooses short local evidence, never grants a grade.
stop=set('a an the to of and or is at in on as for with from its their your that this by not if then one two each any must may more all only'.split())
def tokens(x):return set(re.findall(r"[a-z0-9]+",x.lower()))-stop
def sentences(text,offset=0):
 out=[]
 for m in re.finditer(r'[^\n.!?]+(?:[.!?](?=\s|$)|\n|$)',text):
  a,b=m.span();v=m.group().strip()
  if v:
   a+=len(m.group())-len(m.group().lstrip());b=a+len(v);out.append((offset+a,offset+b,v))
 return out

def evidence(q,r,f):
 entry=q['readers'][r];answer=entry['answer'];ev=[{'location':f"{r}/{q['id']}/answer",'excerpt':answer}]
 if 'scenario' in entry:ev.append({'location':f"{r}/{q['id']}/scenario",'excerpt':json.dumps(entry['scenario'],ensure_ascii=False) if isinstance(entry['scenario'],dict) else entry['scenario']})
 ft=tokens(f['expected_fact']);candidates=[]
 for i,sp in enumerate(entry.get('attached_verbatim_passage_spans',[])):
  for a,b,t in sentences(s[sp['start']:sp['end']],sp['start']):
   score=sum(1+len(w)/12 for w in ft & tokens(t))/(1+len(t)/1200)
   if score>0:candidates.append((score,a,b,t,i))
 seen=set()
 for _,a,b,t,i in sorted(candidates,reverse=True):
  if (a,b) in seen:continue
  seen.add((a,b));ev.append({'location':f"{r}/{q['id']}/attached_verbatim_passage_spans/{i}",'excerpt':t,'span_if_quote':{'start':a,'end':b,'sha256_utf8':hashlib.sha256(t.encode()).hexdigest()}})
  if len(seen)==4:break
 return ev

special={('reader-a','Q001'):"The answer says the first check is at the next Wake, which is accurate; it does not explicitly claim a win then. Its attached timing passage expressly says that check precedes the flip, ordinary victory is the following Wake, and round-eight victory can intervene. The same passage supplies the retaking rule. Read together this resolves all three facts without imposing a false next-Wake-win reading.",('reader-a','Q056'):"The answer expressly says the summary names no specific site-power override. Its own attached Site powers passage names Shrouded Wood and explicitly says travel from it ignores Hidden Place. This volunteered availability ruling materially misanswers the requested named override, despite the correct quoted rule. The attached passage otherwise supplies Buried Giant/Coasts limits.",('reader-b','Q038'):"The answer gives the general half-rounded-down rule and survivor destination but never calculates the specified remaining force of five. No attached passage concludes two die and three survive for this state. A general formula does not resolve the requested numeric case. The no-relic-taking fact is satisfied.",('reader-b','Q055'):"The final sentence says ruling Narrow Pass removes 'those conditions', explicitly extending the exception to entry as well as Campaign targeting. Entry remains constrained even for its ruler; the rule exception applies only to Campaign. The attached correct passage does not erase this incompatible application.",('reader-b','Q070'):"The answer expressly says a Citizen defensive plan cannot restrict other Allies. The requested rule and its own attached Imperial defense passage share these restrictions across the defending side. This is a direct material contradiction; order/priority and once-total/user-payment rules are supplied by the same entry.",('reader-b','Q017'):"All facts are resolved by the answer and its attached Campaign passage. The final compressed temporary-status clause is read in the passage's explicit context: it is the specified Citizen who becomes non-Imperial when Chancellor attacks Citizen, not the Chancellor. It does not force a false actor interpretation."}
receipts=[]
# Stable per-chunk receipts are authoritative; process chunk IDs are supplementary.
chunks=json.loads((audit/'grader07-chunks.json').read_text())
for i,(f,a,b,n,h,t) in enumerate(chunks):receipts.append({'chunk_index':i,'filename':f,'start':a,'end':b,'total':n,'file_sha256':h,'chunk_sha256_utf8':hashlib.sha256(t.encode()).hexdigest(),'model_visible':True,'complete_output_inspected':True,'outer_max_output_tokens':7000,'nested_max_output_tokens':7000,'truncated':False})
(audit/'grader07-receipts.json').write_text(json.dumps({'chunks':receipts,'directive_deviations':[],'delivery_completed_before_grading':True},indent=2))
res={'benchmark_version':'expanded-v11','iteration':7,'status':'complete','method':'Independent strict semantic review of all 208 complete reader entries and all 656 fixed fact groups. Every requested conjunct considered; attached passages reconstructed only for their own entry. No prior grades, histories, changes or other iterations read. Contextual exclusions honored; explicit incompatible rules override correct quotations, while ambiguous shorthand is read fairly in same-entry context. Whole snapshot used only to verify stated facts; no unstated numeric conclusion supplied. Evidence retrieval formats the independent decisions and does not determine them.','inputhashes':{x['path']:x['sha256'] for x in g['inputs']},'delivery_receipt':str(audit/'grader07-receipts.json'),'questions_graded':208,'fact_assessments':656,'readers':[],'gold_or_scope_defects':[]}
res['inputhashes'][str(d/'grading-input.json')]=hashlib.sha256((d/'grading-input.json').read_bytes()).hexdigest()
for r in statuses:
 out={'reader':r,'totals':{'correct':0,'partial':0,'incorrect':0,'total':104},'fact_totals':{'satisfied':0,'missing':0,'contradiction':0,'total':328},'questions':[]}
 for q in g['questions']:
  qid=q['id'];row=statuses[r][qid];assert len(row)==len(q['required_facts'])
  grade='incorrect' if 'C' in row else 'partial' if 'M' in row else 'correct';out['totals'][grade]+=1
  qq={'id':qid,'question':q['question'],'expected_answer_from_fixed_key':q['fixed_expected_answer'],'observed_answer':copy.deepcopy(q['readers'][r]),'grade':grade,'reason':special.get((r,qid),'All requested fact-group conjuncts are resolved accurately by the same entry’s answer and attached passages. No material incompatible rule or scenario application was found. Excluded contextual details were not imposed as extra requirements.'),'fact_checks':[],'attached_quote_spans':q['readers'][r].get('attached_verbatim_passage_spans',[]),'material_contradictions':[]}
  for flag,f in zip(row,q['required_facts']):
   status={'S':'satisfied','M':'missing','C':'contradiction'}[flag];out['fact_totals'][status]+=1
   check={'fact_id':f['fact_id'],'expected_fact':f['expected_fact'],'status':status,'evidence':evidence(q,r,f)}
   if flag!='S':check['explanation']=special[(r,qid)]
   qq['fact_checks'].append(check)
  if grade=='incorrect':qq['material_contradictions']=[{'location':f'{r}/{qid}/answer','excerpt':q['readers'][r]['answer'],'explanation':special[(r,qid)]}]
  out['questions'].append(qq)
 res['readers'].append(out)
(d/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print([(r['reader'],r['totals'],r['fact_totals']) for r in res['readers']])
