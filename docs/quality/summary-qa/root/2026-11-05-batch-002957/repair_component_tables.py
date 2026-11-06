from build_evidence import *
p=ROOT/'rules/root.md';s=p.read_text()
a=s.index('**Craft (4.1):**');b=s.index('- Immediate effect (paper box):',a)
s=s[:a]+'''**Craft (4.1):** Craft a card from hand when your faction permits. Its **bottom-left crafting icons** set the cost; the card's own suit does not pay or define that cost. Marquise activate workshops, Eyrie roosts, and Alliance sympathy.

| Crafting requirement | Marquise, Eyrie and Alliance | Vagabond |
|---|---|---|
| Cost for each icon | Activate one matching crafting piece | Exhaust one face-up, undamaged hammer to activate the pawn |
| Where the suit comes from | Each crafting piece has **its clearing's suit**; use it for a matching icon | The pawn has **its current clearing's suit**, which must match **every icon on the card** |
| Reuse during the turn | Each crafting piece activates only once per turn | Pawn may activate repeatedly; **each icon still requires its own hammer payment** |

A three-color question-mark icon accepts any suit. Normal factions can combine their eligible crafting pieces to pay a card's icons. Vagabond cannot pay mixed fox/rabbit/mouse icons from one clearing.

'''+s[b:]
a='- Immediate effect (paper box): resolve and discard card. An item card requires that item in the map supply, or it cannot be crafted. Take it from supply into Crafted Items and score listed VP, subject to Eyrie exception. Ordinary factions do not exhaust crafted items to use them as Vagabond does.'
b='''- Immediate effect (paper box): resolve, then discard the **crafting card**. An item card requires the corresponding **item token** in the map supply, or it cannot be crafted. Take the item token into Crafted Items and score the VP printed on the card, subject to Eyrie exception. The item token stays; the crafting card is discarded. Ordinary factions do not exhaust crafted items as Vagabond does.

| Separate component after a successful craft | Starts in | Goes to |
|---|---|---|
| Immediate-effect crafting card | Your hand | Shared discard pile after resolving |
| Persistent-effect crafting card | Your hand | Your play area |
| Item token produced by an item card | Map item supply | Crafted Items box; Vagabond can immediately take it face up into Satchel/track |
''';assert a in s;s=s.replace(a,b)
a=s.index('- Recruit: place **one warrior at one chosen roost**');b=s.index('\nIf any required action cannot be completed',a)
s=s[:a]+'''| Decree column | Match the card's suit to | Required procedure for one card |
|---|---|---|
| Recruit | Clearing with a roost | Place **one warrior at one chosen roost** there; Charismatic must instead place **two warriors** there |
| Move | Origin clearing | Move **at least one warrior**, obeying ordinary path and rule requirements |
| Battle | Clearing of battle | Initiate a battle there with Eyrie warriors and an enemy |
| Build | Target clearing | Place one roost in a clearing you rule, with an open slot and **no roost already there** |
'''+s[b:]
needle='**Marquise setup (6.3):**'
ref='''**Hidden ruin items (only when Vagabond is present, during its faction setup):**

1. Take the four ruins and R-marked bag, boot, hammer and sword. Put **one item beneath each ruin**.
2. **Shuffle the ruin/item stacks**, keeping identities hidden.
3. **Return each stack to an empty R ruin slot** on the map. With no Vagabond, leave the four ruins without hidden items.

''';assert needle in s;s=s.replace(needle,ref+needle)
needle='**Dominance (3.3):**';ref='''**Ordinary removal VP (3.2.1):**

| Removed enemy piece | Ordinary removal VP |
|---|---|
| Warrior | **0 VP** |
| Building | **1 VP** |
| Token | **1 VP** |

Faction/card scoring can add to these ordinary points. In particular, Vagabond Infamy is an **additional** point per eligible Hostile piece in battle on his own turn, except the warrior that first caused Hostile status. Do not add an ordinary removal point for a warrior.

''';assert needle in s;s=s.replace(needle,ref+needle)
p.write_text(s)
I=R/'source-audit-candidate-09';I.mkdir();shutil.copyfile(p,I/'summary-snapshot.md');save(I/'input-manifest.json',{'hashes':{str(x):sha(x) for x in [I/'summary-snapshot.md',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'reason':'General cost/component/Decree tables, hidden-ruin procedure reference and ordinary removal VP clarification; fixed question/key unchanged.'})
