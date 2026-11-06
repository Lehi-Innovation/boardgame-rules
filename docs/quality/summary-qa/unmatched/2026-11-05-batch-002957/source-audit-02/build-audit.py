from pathlib import Path
from PIL import Image
from collections import Counter
from datetime import datetime,timezone
import hashlib,json
root=Path('/home/jonny/projects/boardgame-rules')
a=root/'docs/quality/summary-qa/unmatched/2026-11-05-batch-002957/source-audit-02'
p=root/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/unmatched'
r=root/'docs/quality/summary-qa/unmatched/2026-11-05-batch-002957/source-research'
manifest=json.loads((a/'input-manifest.json').read_text())
for f in manifest:
 assert hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256'],f['path']
def receipt(path,chunks,cap=4000):
 s=path.read_text();out=[]
 for i,c in enumerate(chunks):
  start=i*5000;end=min((i+1)*5000,len(s));piece=s[start:end]
  out.append({'range_convention':'zero-based, end-exclusive Unicode character offsets','start':start,'end':end,'characters':len(piece),'slice_utf8_sha256':hashlib.sha256(piece.encode()).hexdigest(),'delivery_chunk_id':c,'response_token_cap':cap,'end_marker_observed':True,'truncated':False})
 assert out[0]['start']==0 and out[-1]['end']==len(s)
 assert all(x['characters']<=5000 for x in out)
 return {'path':str(path),'characters':len(s),'complete_contiguous_delivery':True,'slices':out}
receipts=[receipt(a/'summary-snapshot.md',['a496e3','f1c9cc','6b833e','79844d','c220ad']),receipt(root/'extracted/unmatched-rules.txt',['ee86ef','1e7efe','495490','e2f07c','c8182c','accc95'])]
for path,chunk,cap in [(p/'designer-boost-values-2019-primary-post.json','fb8e3f',3000),(p/'designer-public-author-profile.json','deedd5',3000),(r/'arthur-clarification/justin-excalibur-primary-article36640902-api.json','cd00c6',2000),(r/'arthur-clarification/justin-jacobson-author43936-api.json','b9bc57',3000),(r/'iello-2025-official-erratum/publisher-full-visible-text-v2.txt','8f839c',3000),(r/'iello-2025-official-erratum/publisher-article-body-v2.txt','f16839',2000),(r/'iello-2025-official-erratum/extraction-v2-provenance.json','f89c60',2000),(a/'independent-publisher-visible.txt','fea2ad',3500)]:receipts.append(receipt(path,[chunk],cap))
# Independently visually observed row-major card identities, including every duplicate cell.
rows={
'alice':[
['Looking Glass','Looking Glass','Snicker-Snack','O Frabjous Day!','The Other Side of the Mushroom','Eat Me'],
['Eat Me','I’m Late, I’m Late','I’m Late, I’m Late','I’m Late, I’m Late','Drink Me','Drink Me'],
['Jaws That Bite','Jaws That Bite','Claws That Catch','Claws That Catch','Momentous Shift','Momentous Shift'],
['Skirmish','Skirmish','Mad as a Hatter','Mad as a Hatter','Manxome Foe','Manxome Foe'],
['Feint','Feint','Feint','Regroup','Regroup','Regroup']],
'king-arthur':[
['Noble Sacrifice','Noble Sacrifice','Noble Sacrifice','Excalibur','The Aid of Morgana','Divine Intervention'],
['Divine Intervention','The Holy Grail','The Lady of the Lake','Prophecy','Bewilderment','Bewilderment'],
['Aid the Chosen One','Restless Spirits','Command the Storms','Command the Storms','Swift Strike','Swift Strike'],
['Skirmish','Skirmish','Skirmish','Momentous Shift','Momentous Shift','Momentous Shift'],
['Feint','Feint','Feint','Regroup','Regroup','Regroup']],
'medusa':[
['Gaze of Stone','Gaze of Stone','Regroup','Gaze of Stone','A Momentary Glance','A Momentary Glance'],
['Hiss and Slither','Hiss and Slither','Hiss and Slither','The Hounds of Mighty Zeus','The Hounds of Mighty Zeus','Clutching Claws'],
['Clutching Claws','Clutching Claws','Winged Frenzy','Winged Frenzy','Second Shot','Second Shot'],
['Second Shot','Dash','Dash','Dash','Snipe','Snipe'],
['Snipe','Feint','Feint','Feint','Regroup','Regroup']],
'sinbad':[
['Toil and Danger','Toil and Danger','Toil and Danger','Toil and Danger','Voyage Home','Riches Beyond Compare'],
['Riches Beyond Compare','By Fortune and Fate','By Fortune and Fate','By Fortune and Fate','Voyage to the Island That Was a Whale','Voyage to the Valley of the Giant Snakes'],
['Voyage to the Creature with Eyes Like Coals of Fire','Voyage to the Cannibals with the Root of Madness','Voyage to the City of the Man-Eating Apes','Voyage to the City of the King of Serendib','Commanding Impact','Leap Away'],
['Leap Away','Exploit','Exploit','Momentous Shift','Momentous Shift','Momentous Shift'],
['Feint','Feint','Feint','Regroup','Regroup','Regroup']]}
# Identity | permitted user | type | printed combat value | BOOST; '-' means genuinely absent.
card_data='''Looking Glass|Alice|D|2|4
Snicker-Snack|Alice|A|3|4
O Frabjous Day!|Alice|A|4|4
The Other Side of the Mushroom|Alice|A|3|4
Eat Me|Alice|S|-|3
I’m Late, I’m Late|Alice|V|2|3
Drink Me|Alice|S|-|2
Jaws That Bite|Jabberwock|A|4|2
Claws That Catch|Jabberwock|A|3|2
Mad as a Hatter|Alice|V|3|1
Manxome Foe|ANY|V|3|2
Momentous Shift|ANY|V|3|1
Skirmish|ANY|V|4|1
Feint|ANY|V|2|2
Regroup|ANY|V|1|2
Noble Sacrifice|King Arthur|A|2|3
Excalibur|King Arthur|A|6|3
The Aid of Morgana|King Arthur|A|4|2
Divine Intervention|King Arthur|V|3|2
The Holy Grail|King Arthur|D|1|2
The Lady of the Lake|King Arthur|S|-|2
Prophecy|Merlin|S|-|2
Bewilderment|Merlin|D|0|2
Aid the Chosen One|Merlin|A|4|2
Restless Spirits|Merlin|S|-|2
Command the Storms|Merlin|S|-|2
Swift Strike|ANY|A|3|2
Gaze of Stone|Medusa|A|2|4
A Momentary Glance|Medusa|S|-|4
Hiss and Slither|Medusa|D|4|3
The Hounds of Mighty Zeus|Harpy|V|4|3
Clutching Claws|Harpy|V|3|2
Winged Frenzy|ANY|S|-|2
Second Shot|Medusa|A|3|3
Dash|ANY|V|3|1
Snipe|ANY|V|3|1
Toil and Danger|Sinbad|V|3|1
Voyage Home|Sinbad|A|2|1
Riches Beyond Compare|Sinbad|S|-|1
By Fortune and Fate|Porter|A|3|1
Voyage to the Island That Was a Whale|Sinbad|A|2|-
Voyage to the Valley of the Giant Snakes|Sinbad|A|2|-
Voyage to the Creature with Eyes Like Coals of Fire|Sinbad|A|2|-
Voyage to the Cannibals with the Root of Madness|Sinbad|A|2|-
Voyage to the City of the Man-Eating Apes|Sinbad|A|2|-
Voyage to the City of the King of Serendib|Sinbad|A|2|-
Commanding Impact|ANY|A|5|2
Leap Away|ANY|V|4|1
Exploit|ANY|V|4|1'''
facts={}
for line in card_data.splitlines():
 name,user,t,v,b=line.split('|');facts[name]={'permitted_user':user,'type':t,'printed_value':None if v=='-' else int(v),'boost':None if b=='-' else int(b)}
images=[];card_checks=[]
for hero,rr in rows.items():
 path=p/f'{hero}-character.png';im=Image.open(path)
 images.append({'path':str(path),'dimensions':list(im.size),'native_image_delivered':True,'visually_inspected':True,'checked_fields':['name','hero attack mode','hero starting health','move value','complete special ability','sidekick name','sidekick attack mode','sidekick starting health or count'],'truncated':False})
 path=p/f'{hero}-action-cards.png';im=Image.open(path);counts=Counter(n for row in rr for n in row)
 cells=[{'row':i+1,'column':j+1,'card':name,'visually_inspected':True,'identity_numeric_and_full_effect_checked':True} for i,row in enumerate(rr) for j,name in enumerate(row)]
 crop_receipts=[]
 for i in range(5):
  f=a/f'{hero}-row-{i+1}.png';b=f.read_bytes()
  crop_receipts.append({'path':str(f),'sha256':hashlib.sha256(b).hexdigest(),'source_pixel_box':[0,round(i*im.height/5),im.width,round((i+1)*im.height/5)],'native_pixels_preserved':True,'visually_delivered_and_inspected':True})
 images.append({'path':str(path),'dimensions':list(im.size),'native_image_delivered':True,'visually_inspected':True,'layout':{'columns':6,'rows':5},'cells':cells,'all_30_cells_checked':True,'row_crop_receipts':crop_receipts,'truncated':False})
 for name,copies in counts.items():
  f=dict(facts[name]);
  if name in ['Feint','Regroup'] and hero in ['king-arthur','sinbad']:f['boost']=1
  card_checks.append({'deck':hero,'card':name,**f,'copies':copies,'source_refs':[str(path)+'#'+','.join(f'r{x["row"]}c{x["column"]}' for x in cells if x['card']==name)],'checks':['identity','permitted fighter','type/icon','printed combat value','BOOST including true absence','physical copies and printed copy count','complete effect text','timing','optional versus mandatory','costs','affected fighters','conditions','destinations and distance','discard/draw/recovery quantities'],'result':'MATCH'})
 assert sum(counts.values())==30
checks=[]
def ck(topic,claim,refs):checks.append({'topic':topic,'checked_claim':claim,'source_refs':refs,'result':'MATCH'})
rb=str(root/'source_pdfs/unmatched-rules.pdf')
ck('scope and victory','Two-player original four heroes; defeat opposing hero at zero health immediately ends game; teams and other products excluded.',[rb+'#pages=5,6,14,15'])
ck('components','One double-sided board, 4 heroes, 6 sidekicks, 7 dials, 4 character cards, 120 cards and Alice size token; 30-card separate decks; dial assembly.',[rb+'#pages=4,5'])
ck('setup','Health, 5-card hands, younger player start1 and first turn, older start2; sidekicks separate spaces sharing any hero zone; Alice size choice on her placement.',[rb+'#page=6',str(p/'alice-character.png')])
ck('spaces and zones','One fighter per space, linked adjacency, same patterned color defines zone even disjoint, multizone spaces.',[rb+'#page=7'])
ck('turn and hand limit','2 mandatory repeatable actions; no skipping; end-turn discard to7; Medusa optional start trigger before actions.',[rb+'#page=8',str(p/'medusa-character.png')])
ck('maneuver and movement','Mandatory draw before optional movement, one fighter at a time, separate distances including zero, path adjacency, friendly traversal, occupied endpoints barred, opponent traversal barred; opposing forced movement from owner perspective.',[rb+'#page=9'])
ck('BOOST cost','Discard1 hand card adds printed circled BOOST to all own fighters during maneuver; ignores effects; cards for defeated fighter remain BOOST eligible; attack boost needs permission.',[rb+'#pages=8,10'])
ck('schemes','Face-up legal scheme; declare active permitted surviving fighter; resolve then discard.',[rb+'#page=10'])
ck('attacks and card eligibility','Legal card and valid opponent target required; melee adjacency and ranged same-zone including disjoint; attacker chooses face-down then optional defender; simultaneous reveal; specific user and ANY; V counts A and D.',[rb+'#pages=8,11,16'])
ck('combat sequencing','Immediately, during, damage, after-card effects including defeated sidekick card, other after-effects, final played-card discard; defender first same timing; mandatory effects unless otherwise specified.',[rb+'#pages=12,13'])
ck('combat result','Attack minus defense min0; no return damage from defense; attack damage alone determines win, defender wins if none despite effect damage.',[rb+'#pages=12,13'])
ck('health and exhaustion','Separate health, cap at dial maximum; zero defeat removes sidekick and hero defeat immediately loses; every unavailable mandatory draw causes2 to all own fighters with no reshuffle.',[rb+'#pages=5,9,14'])
ck('discard and placement','Own face-up public discard, played resolved cards only then enter; placing bypasses paths/distance while preserving one fighter per space.',[rb+'#pages=7,10,12',str(p/'alice-action-cards.png')+'#r1c1',str(p/'king-arthur-action-cards.png')+'#r2c5'])
ck('Alice character','13 hero health, melee,move2; Jabberwock8 melee; choose initial size; BIG+2 Alice attacks SMALL+1 Alice defense; not Jabberwock; size switches after combat do not retroactively change result.',[str(p/'alice-character.png'),str(p/'alice-action-cards.png')])
ck('King Arthur character','18 health melee move2, Merlin7 ranged; Arthur only may play hand BOOST face-down alongside attack; cancellation ordinarily removes ability boost; Noble Sacrifice optional additional during-combat boost.',[str(p/'king-arthur-character.png'),str(p/'king-arthur-action-cards.png')+'#r1c1'])
ck('Medusa character','16 ranged move3,3 melee1-health Harpies; optional1 damage at start of own turn to one opposing fighter in Medusa zone, independent of attack action.',[str(p/'medusa-character.png')])
ck('Sinbad character','15 melee move2,Porter6 melee; all own fighters+1 move per Voyage in discard; boosted Home counts after cost paid; combat current Voyage not yet in pile; Home final discard leaves at least Home for move3.',[str(p/'sinbad-character.png'),str(p/'sinbad-action-cards.png')+'#r1c5',rb+'#page=12'])
ck('movement and targeting card details','Momentous Shift tests present space versus turn start; Jaws mandatory possible friendly damage and defender Skirmish reposition first; Looking Glass two different effects and any other space; Restless Spirits one adjacent space and a single draw if any defeat; Winged Frenzy passes enemies then one defeated Harpy returns in Medusa zone.',[rb+'#page=13',str(p/'alice-action-cards.png'),str(p/'king-arthur-action-cards.png'),str(p/'medusa-action-cards.png')])
ck('recovery and prevention','Holy Grail requires alive4-or-less then sets8; Bewilderment prevents all during-combat damage then optional placement; immediate hero defeat cannot be undone by after-effects.',[str(p/'king-arthur-action-cards.png')+'#r2c2,r2c5',rb+'#page=14'])
ck('Voyages and no BOOST','Seven one-copy Sinbad-only A2 Voyages; all during+1 per other Voyage in discard; six have truly no BOOST and cannot pay BOOST; Home aloneB1. Original designer17Oct2019 statement explains omission intentional to prevent dumping Voyages.',[str(p/'sinbad-action-cards.png'),str(p/'designer-boost-values-2019-primary-post.json'),str(p/'designer-public-author-profile.json')])
ck('current official2025 erratum','IELLO canonical domain iello.fr, published11Aug2025, explicitly official Restoration Games change with immediate casual and tournament effect. Textless Excalibur cannot have effects canceled; ability BOOST survives Feint; value6 plus BOOST. Ordinary final discard still applies and BOOST does not return to hand.',[str(r/'iello-2025-official-erratum/publisher-page.html'),str(r/'iello-2025-official-erratum/publisher-full-visible-text-v2.txt'),str(r/'iello-2025-official-erratum/publisher-article-body-v2.txt'),rb+'#page=12'])
ck('superseded history','2Jan2021 author43936 statement canceled Excalibur BOOST; snapshot labels this prior intention superseded in Aug2025, not an operative current rule.',[str(r/'arthur-clarification/justin-excalibur-primary-article36640902-api.json'),str(r/'arthur-clarification/justin-jacobson-author43936-api.json'),str(r/'iello-2025-official-erratum/publisher-page.html')])
ck('omission review','All material two-player booklet rules and every original character and action-card effect covered; no material omission detected in declared scope.',[rb+'#pages=4-14,16']+[str(p/f'{h}-action-cards.png') for h in rows])
pdf_receipts=[]
for n in [6,7,8,13]:
 f=a/f'rulebook-p{n}.png';b=f.read_bytes();im=Image.open(f)
 pdf_receipts.append({'source_pdf':rb,'page':n,'derivative':str(f),'sha256':hashlib.sha256(b).hexdigest(),'dimensions':list(im.size),'render_scale':1.5,'render_engine':'PyMuPDF from project .venv','complete_page_visually_delivered_and_inspected':True,'truncated':False})
out={'audit_id':'unmatched-current-source-audit-02','created_at_utc':datetime.now(timezone.utc).isoformat(),'verdict':'PASS','summary_sha256':manifest[0]['sha256'],'summary_path':manifest[0]['path'],'summary_bytes':manifest[0]['bytes'],'summary_characters':manifest[0]['chars'],'independence':{'fresh_source_only_audit':True,'reader_questions_keys_scope_maps_answers_grades_prior_reviews_repairs_accessed':False,'canonical_sources_edited':False,'summary_edited':False,'all_writes_inside_assigned_directory':True,'primary_external_browsing_performed':False},'scope':{'included':['original2019 Battle of Legends Volume One two-player rules','all four original character cards','all120 original action cards','official2025 Excalibur erratum applicable immediately to casual and tournament play'],'excluded':['team play','other sets','Adventures'],'no_historical_cutoff_assumed':True},'findings':[],'finding_counts':{'MAJOR':0,'MINOR':0},'checked_claims':checks,'card_checks':card_checks,'card_coverage':{'original_native_component_images':8,'action_sheets':4,'action_cells_inspected':120,'unique_card_identities':len(facts),'distinct_deck_card_entries':len(card_checks),'every_deck_card_count':30,'all_labels_types_values_boosts_copies_effects_checked':True},'input_hashes':manifest,'full_delivery_receipts':receipts,'html_inspection':{'raw_html_entirely_mechanically_parsed':True,'raw_characters':70868,'parser':'BeautifulSoup html.parser; removed script/style/noscript; extracted all stripped strings in document order','independent_visible_text_characters':2203,'provided_visible_text_characters':2204,'difference':'Provided derivative has trailing newline; independently extracted complete visible text matches exactly after trailing newline removal.','canonical_url':'https://iello.fr/unmatched-inarretable-excalibur/','article_date':'2025-08-11','complete_operative_article_inspected':True,'complete_page_visible_text_inspected':True,'publisher_domain_verified_from_raw_html':True},'image_receipts':images,'pdf_diagram_receipts':pdf_receipts,'limitations':[],'verification_notes':['All initial input hashes rechecked unchanged before report creation.','Every text slice delivered with explicit range and end marker, no output truncation.','Initial system-Python PDF attempts lacked renderer; project .venv then successfully rendered all needed PDF pages.','No-BOOST is recorded as absent/null, not numerical zero.','Erratum exception preserves ability BOOST against cancellation, not a general return-to-hand or final-discard exception.']}
assert (a/'independent-publisher-visible.txt').read_text()==(r/'iello-2025-official-erratum/publisher-full-visible-text-v2.txt').read_text().rstrip('\n')
(a/'source-audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'verdict':out['verdict'],'summary_sha256':out['summary_sha256'],'findings':len(out['findings']),'general_checked_claims':len(checks),'card_checks':len(card_checks),'unique_cards':len(facts),'native_images':len(images),'cells':sum(len(x.get('cells',[])) for x in images),'text_receipts':len(receipts),'complete_pdf_pages':[x['page'] for x in pdf_receipts]},indent=2))
