from qa_tools import *
I=P/'expanded-iteration-01';q=json.loads((I/'questions.json').read_text())['questions'];k=json.loads((P/'expanded-v2/answer-key.json').read_text())['answers']
findings={
'a':{'Q09':('partial','Correct acquisition/availability, but expressly leaves opponent recruitment unresolved despite underbutler being unique and the summary’s unique-servant protection.'),'Q32':('partial','States same-as-Holiday rule, then leaves the Market Purchase no-refresh-between-buys consequence unsupported; contradictory unresolved procedural caveat.'),'Q36':('incorrect','Says family cannot fill a two-ladies requirement. Source allows any female family member as a Lady; casual-only does exclude family.'),'Q40':('partial','Correct admirer condition and bonus, but leaves Charles eligibility unresolved because his gender is not explicit in summary.'),'Q56':('partial','Gives front invite/upgraded dismissal but says tile favours and upgraded requirements unsupported; those requested parts remain unresolved.'),'Q58':('partial','Correct public inspection, but expressly leaves any-tile versus top-only Reserve purchase unresolved.'),'Q60':('partial','Correct independent refresh methods, but expressly leaves multiple Market Refresh VP cards in one turn unresolved.')},
'b':{'Q04':('incorrect','Correct legal activity and screening/service origins, but falsely says 6.1 minus twelve increments cannot equal3.4. Five positions per level:25 increments above minimum minus12 is13=3.4. This is a material contradiction, not an abstention.'),'Q36':('incorrect','Says family cannot fill ladies-only requirements. Female family are Ladies under the source; family cannot fill casual-only requirements.'),'Q56':('partial','States the prestige invite, then calls favours unsupported, leaving the requested favour/side comparison unresolved.'),'Q58':('partial','Public inspection correct, but explicit uncertainty about buying any stacked tile leaves requested purchase access unresolved.')}}
res={'benchmark_version':'expanded-v2','frozen_bank_unchanged':True,'readers':{}}
for w in ['a','b']:
 raw=json.loads((I/f'reader-{w}.json').read_text())['answers'];g=[]
 for a,qq,kk in zip(raw,q,k):
  grade,reason=findings[w].get(a['id'],('correct','All requested material facts match the fixed answer; this answer independently resolves the question without borrowing facts from other answers.'))
  unsupported=w=='b' and a['id']=='Q40'
  if unsupported:reason+=' However Charles’s gender is not explicit in this snapshot; the correct Charles branch relies on an unsupported assumption. This prevents final passage even though the ruling is correct.'
  g.append({'id':a['id'],'question':qq['question'],'expected_answer':kk['expected_answer'],'source_refs':kk['source_refs'],'actual_answer':a['answer'],'reader_evidence':a['evidence'],'grade':grade,'reason':reason,'unsupported_guess':unsupported})
 from collections import Counter
 c=Counter(x['grade'] for x in g);res['readers'][w]={**{x:c[x] for x in ['correct','partial','incorrect']},'unsupported_guesses':sum(x['unsupported_guess'] for x in g),'grades':g}
dump(I/'results.json',res)
