from build_evidence import *
p=ROOT/'rules/root.md';s=p.read_text()
a=s.index('**Craft (4.1):**');b=s.index('- Immediate effect (paper box):',a)
s=s[:a]+'''**Craft (4.1):** Craft a card from hand when your faction permits. Its **bottom-left crafting icons** set the cost; the card's own suit does not pay or define that cost.

- **Marquise, Eyrie and Alliance cost:** Activate **one matching crafting piece for every icon**. The piece's suit is **the suit of its clearing**. Marquise activate workshops, Eyrie roosts, Alliance sympathy. Combine eligible pieces as needed, but **each piece may activate only once per turn**.
- **Vagabond cost:** Exhaust **one face-up, undamaged hammer for every icon** to activate the pawn. Its **current clearing's suit must match every icon on the card**. The pawn may activate repeatedly, but each icon still needs its own hammer payment. One clearing cannot pay mixed fox/rabbit/mouse icons.
- A **three-color question-mark icon** accepts any suit.

'''+s[b:]
s=s.replace('Crafted Items box; Vagabond can immediately take it face up into Satchel/track','Crafting faction’s Crafted Items box; when Vagabond itself crafts, it may immediately take its crafted item face up into Satchel/track')
a='**Train:** Spend a **hand card** matching a clearing with a base to place one supply warrior in Officers box. Supporters cannot pay Train. These officers allow Evening operations, including **Organize: remove one Alliance warrior from an unsympathetic clearing, place sympathy there and score the uncovered VP**. Organize occurs in Evening, not Daylight.'
b='**Train:** Spend a **hand card** matching a clearing with a base to place one supply warrior in Officers box. Supporters cannot pay Train. Each officer allows one Evening military operation; taking operations does not consume officers.'
assert a in s;s=s.replace(a,b)
a='**Evening:** Take military operations **up to your number of officers**, in any order and repetition. Officers stay on the board; taking an operation does not consume an officer.'
b='**Evening:** The four military operations are **Move, Battle, Recruit and Organize**. Take **up to your number of officers** in operations, in any order and repetition. Officers stay on the board; taking an operation does not consume an officer. After operations, draw one card plus one per uncovered draw bonus, then discard hand down to five.'
assert a in s;s=s.replace(a,b)
s=s.replace('**Mobilize:** Add a hand card to Supporters (respect cap).','**Mobilize:** Add one hand card to Supporters. With no base on map, keep at most five supporters and discard incoming overflow; with any base, the stack has no cap.')
a=s.index('**Allied benefits:**');b=s.index('**Taking hits with an ally:**',a)
s=s[:a]+'''**Allied benefits:**

- **Aid:** Each subsequent Aid to this Allied faction scores **two VP**.
- **Move:** May force warriors of **one** Allied faction to accompany the pawn to its destination clearing. They follow their own movement restrictions, including rule and Eyrie tie advantage. They cannot accompany a move specified to be alone. Moving them into sympathy triggers Outrage.
- **Attack:** **Maximum rolled hits = the participating Allied warriors plus all your undamaged swords.** At the start of battle **as attacker**, you may treat warriors of **one** Allied faction there as your own for that battle. They can join against a different enemy; you cannot use an ally's warriors to attack that ally itself.

'''+s[b:]
a='Crafted item can immediately be taken face up into Satchel/track. Need supply item as usual.'
b='When you craft an item, you may immediately take that item face up into Satchel/track and **use it for another Daylight action immediately**, if its cost and other requirements are met. Need supply item as usual.'
assert a in s;s=s.replace(a,b)
p.write_text(s)
I=R/'source-audit-candidate-10';I.mkdir();shutil.copyfile(p,I/'summary-snapshot.md');save(I/'input-manifest.json',{'hashes':{str(x):sha(x) for x in [I/'summary-snapshot.md',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'reason':'General crafting cost prose; explicit operation names/count/draw and Mobilize cap; Allied combat cap prose; own-crafted-item immediate acquisition/use. Benchmark-v9 unchanged.'})
