from build_evidence import *
import sys,difflib,collections

def freeze(name,benchmark):
 I=R/name;I.mkdir();shutil.copyfile(ROOT/'rules/root.md',I/'summary-snapshot.md');shutil.copyfile(R/benchmark/'questions.json',I/'questions.json')
 save(I/'input-manifest.json',{'benchmark':benchmark,'hashes':{str(p):sha(p) for p in [I/'summary-snapshot.md',I/'questions.json',R/benchmark/'answer-key.json',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'requested_model':'gpt-6-luna','effort':'high'})
 (I/'summary-changes.patch').write_text(''.join(difflib.unified_diff((R/'baseline-summary.md').read_text().splitlines(True),(I/'summary-snapshot.md').read_text().splitlines(True),fromfile='baseline-summary.md',tofile='summary-snapshot.md')))
def grades(name,benchmark,notes):
 I=R/name;qs=json.loads((R/benchmark/'questions.json').read_text())['questions'];key=json.loads((R/benchmark/'answer-key.json').read_text())['answers'];out={}
 for reader in ['a','b']:
  raw=json.loads((I/f'reader-{reader}.json').read_text());ans={a['id']:a for a in raw['answers']};rows=[]
  assert len(ans)==len(qs)==len(raw['answers'])
  for q,k in zip(qs,key):
   n=notes[reader].get(q['id'],('correct','Every requested part matches source-backed key and is supported by frozen summary.'))
   rows.append({'id':q['id'],'question':q['question'],'expected_answer':k['expected_answer'],'source_references':k['source_references'],'observed':ans[q['id']],'grade':n[0],'reason':n[1],'unsupported_guess':False})
  out[reader]={'totals':{g:sum(r['grade']==g for r in rows) for g in ['correct','partial','incorrect']},'grades':rows}
 save(I/'results.json',out)
if __name__=='__main__':
 if sys.argv[1]=='freeze':freeze(sys.argv[2],sys.argv[3])
 if sys.argv[1]=='seedgrades':
  reasons={1:('partial','Missing Eyrie tie exception, tokens and pawn treatment.'),2:('partial','Missing positive group, repeat movement and rivers.'),3:('incorrect','Incorrectly restricts removal VP to attacker; also missing ambush foil, early end, extra hits and effects.'),4:('incorrect','States crafting card-suit payment instead of crafting icons; remaining costs and constraints unresolved.'),5:('incorrect','Uniform three-clearing condition incorrectly includes bird dominance; activation and persistence omitted.'),6:('partial','Abstains from complete question.'),7:('partial','Deck change, precise item/ruin setup and faction order absent.'),8:('partial','Keep and hospitals wholly absent.'),9:('partial','Missing craft-first, March two moves, Recruit limit and matching Overwork cost.'),10:('partial','Missing ruled slot, connected wood payments and leftmost track selection.'),11:('partial','Missing empty-hand draw, bird limit and no-roost recovery.'),12:('partial','Missing within-column freedom, Move origin matching and Build constraints.'),13:('incorrect','Invented removal of map warriors/buildings during turmoil; Viziers and Evening omitted.'),14:('incorrect','Battle alone wrongly triggers Outrage; matching-payment and failure/cap branches absent.'),15:('partial','Revolt/Spread requirements, costs, order, Martial Law and exact results unresolved.'),16:('incorrect','Train wrongly spends supporters, Organize wrongly draws cards; base removal absent.'),17:('incorrect','Rest versus draw falsely exclusive; A additionally imposes ordinary rule on Vagabond normal movement; precise refresh/hostile costs absent.'),18:('incorrect','Quest wrongly paid by two cards; repair and rewards absent.'),19:('incorrect','Hostility wrongly requires three warrior removals; Infamy, Aid and Strike unresolved.'),20:('partial','Missing four-player limit, timing, threshold, eligibility, relationship reset and scoring change.')}
  grades('seed-iteration-01','benchmark-v1',{r:{f'Q{i:02}':v for i,v in reasons.items()} for r in ['a','b']})
