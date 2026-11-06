from pathlib import Path
import sys,json,hashlib,subprocess
OUT=Path(__file__).parent
ROOT=Path('/home/jonny/projects/boardgame-rules')
B=ROOT/'docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957'
SOURCES={
'candidate':B/'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/summary-snapshot.md',
'rules':ROOT/'extracted/john-company-second-edition-rules.txt',
'pdf':ROOT/'source_pdfs/john-company-second-edition-rules.pdf',
'scope':ROOT/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/john-company-user-approved-scope.json',
'human':B/'human-defense-interpretation-source.json',
'foreign':B/'supplements/foreign-invasion-designer-ruling.json',
'errata_provenance':B/'supplements/full-official-errata-provenance.json',
'errata':B/'supplements/full-official-errata.txt',
'board_track':B/'supplements/images/board-company-track-details.png',
'board_left':B/'supplements/images/board-left-details.png',
'cards9':B/'supplements/images/cards-Bridge-Fronts-page-9.png',
'errata_original':B/'supplements/official-errata-original-post.txt',
'board':B/'supplements/pnp/Board/John Company Game Board.pdf',
'bridge':B/'supplements/pnp/Cards/John Company Cards (Bridge, Bridge).pdf',
'fronts':B/'supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf',
'pnp_provenance':B/'supplements/publisher-pnp-download-provenance.json',
'publisher':B/'supplements/publisher-resources.html',
'ruling':B/'supplements/ruling-thread-2938749.json',
}
for alias in ['board','bridge','fronts']:
 SOURCES[alias+'_text']=OUT/f'{alias}-native-extract.txt'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(item):
 p=OUT/'source-read-record.json'
 data=json.loads(p.read_text()) if p.exists() else {'convention':'One-based physical LF lines from text.split("\\n"); inclusive endpoints. Printed page labels and PDF physical pages are separately specified. Hash-only access is not substantive reading.','reads':[],'native_renders':[],'visual_inspections':[]}
 data['reads'].append(item);p.write_text(json.dumps(data,indent=2)+'\n')
if __name__=='__main__':
 if sys.argv[1]=='read':
  alias=sys.argv[2];p=SOURCES[alias];lines=p.read_text().split('\n');start=int(sys.argv[3]);end=min(int(sys.argv[4]),len(lines))
  record({'alias':alias,'path':str(p),'sha256':sha(p),'start_lf':start,'end_lf':end,'total_lf':len(lines),'method':'visible numbered text delivery'})
  print('\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1)))
 elif sys.argv[1]=='hashes':
  data={k:{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for k,p in SOURCES.items()};(OUT/'original-hashes.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
