from build_evidence import *
p=ROOT/'rules/root.md';s=p.read_text()
a='- **Marquise, Eyrie and Alliance cost:** Activate **one matching crafting piece for every icon**. The piece\'s suit is **the suit of its clearing**. Marquise activate workshops, Eyrie roosts, Alliance sympathy. Combine eligible pieces as needed, but **each piece may activate only once per turn**.'
b='- **Marquise, Eyrie and Alliance cost:** For **each icon**, activate **one workshop, roost or sympathy in a clearing matching that icon\'s suit**, respectively. A crafting piece gets its suit from its clearing. Combine eligible pieces as needed, but **each piece may activate only once per turn**.'
assert a in s;s=s.replace(a,b)
a='- **Vagabond cost:** Exhaust **one face-up, undamaged hammer for every icon** to activate the pawn. Its **current clearing\'s suit must match every icon on the card**. The pawn may activate repeatedly, but each icon still needs its own hammer payment. One clearing cannot pay mixed fox/rabbit/mouse icons.'
b='- **Vagabond cost and reuse:** The pawn **may activate repeatedly in a turn**. For each icon, exhaust **one face-up, undamaged hammer**, and the pawn\'s **current clearing must match every icon on the card**. Reusing the pawn never waives the hammer payment per icon. One clearing cannot pay mixed fox/rabbit/mouse icons.'
assert a in s;s=s.replace(a,b)
a='**Birdsong:** Complete **all Revolts before starting any Spread Sympathy**; each may be performed any number of times.'
b='**Birdsong:** Both Revolt and Spread Sympathy take place **during Birdsong**. Complete **all Revolts before starting any Spread Sympathy**; each may be performed any number of times.'
assert a in s;s=s.replace(a,b)
a='2. **Slip (optional):** Move to adjacent clearing or forest, exhausting **no boots**, even into hostile warriors. Ignore all effects preventing movement **out of** a clearing. Forest adjacency follows map rules, including Winter river.'
b='2. **Slip (optional):** Move to an adjacent clearing or forest, exhausting **no boots**, even into hostile warriors. Ignore all effects preventing movement **out of** a clearing. **Forest adjacency for Slip:** a forest is adjacent to clearings touching it without crossing a printed path, and to forests separated by one printed path. On Winter, the river also divides forests as paths do.'
assert a in s;s=s.replace(a,b)
a='**Allied benefits:**\n\n- **Aid:**'
b='**Allied benefits:** Aid gains two VP, warriors may accompany movement, and participating warriors increase the attacking rolled-hit limit as follows:\n\n- **Aid:**'
assert a in s;s=s.replace(a,b)
a='- **Attack:** **Maximum rolled hits = the participating Allied warriors plus all your undamaged swords.** At the start of battle **as attacker**, you may treat warriors of **one** Allied faction there as your own for that battle. They can join against a different enemy; you cannot use an ally\'s warriors to attack that ally itself.'
b='- **Attack with an increased hit limit:** At the start of battle **as attacker**, you may treat warriors of **one** Allied faction in the battle clearing as your own. **Add those warriors to all your undamaged swords to determine your maximum rolled hits**. They can join against a different enemy; you cannot use an ally\'s warriors to attack that ally itself.'
assert a in s;s=s.replace(a,b);p.write_text(s)
I=R/'source-audit-candidate-13';I.mkdir();shutil.copyfile(p,I/'summary-snapshot.md');save(I/'input-manifest.json',{'hashes':{str(x):sha(x) for x in [I/'summary-snapshot.md',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'reason':'Cost expressed through matching clearing location, pawn reuse first, explicit Birdsong action timing, complete forest Slip adjacency, Allied attack described as adding warriors to sword hit cap. Key/questions unchanged.'})
