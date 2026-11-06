from build_evidence import *
p=ROOT/'rules/root.md';s=p.read_text()
replacements=[
('by activating crafting pieces matching the **crafting icons at bottom left**, rather than paying its card suit.','by activating crafting pieces matching the **crafting icons at bottom left**, rather than paying its card suit. Each icon needs one matching piece activation; the printed icons completely define this crafting cost.'),
('- Ambush and dominance cards cannot be crafted.','- **Ambush cards cannot be crafted:** the defender may play one for two immediate hits, or the attacker may play one to foil a defending ambush, matching the clearing. **Dominance cards cannot be crafted:** activate one to change victory condition, or spend it for suit.'),
('Choose a clearing with your warriors or pawn and an enemy there as defender. Resolve these six steps:', 'Choose a clearing with your warriors or pawn and an enemy there as defender. **Battle does not require you to rule the clearing.** Resolve these six steps:'),
('When an instruction cannot place/take/remove all prompted pieces, do as many as possible;', 'When an instruction cannot place/take/remove all prompted pieces, **you must do the maximum possible and cannot voluntarily do fewer**;'),
('- Recruit: place one warrior at a roost in a clearing matching card (two with Charismatic).','- Recruit: place **one warrior at one chosen roost** in a clearing matching card (two warriors there with Charismatic).'),
('End Daylight and proceed to Evening. **Turmoil does not remove your map warriors or buildings.**', 'End Daylight and proceed to the full normal Evening: **score the roost track, draw one plus uncovered bonuses, then discard to five**. **Turmoil does not remove your map warriors or buildings.**'),
('Capacity still applies. Merely battling there', '**If Supporters is full, discard the incoming Outrage card; payment or the no-match draw still occurs.** Merely battling there'),
('**Birdsong:** First **Revolt** any number of times, then **Spread Sympathy** any number of times:', '**Birdsong:** Complete **all Revolts before starting any Spread Sympathy**; each may be performed any number of times. Once spreading starts, you cannot return to Revolt this Birdsong, so newly spread sympathy cannot support a same-Birdsong Revolt:'),
('- **Quest:** Choose a face-up quest matching clearing;', '- **Quest (matching clearing only):** Choose a face-up quest matching clearing;'),
('Rolled cap is their warriors plus all your undamaged swords.', '**Rolled-hit cap = that ally\'s warriors plus all your undamaged swords.**'),
('Add ordinary building/token removal points. No Infamy while defending on another player\'s turn or from Strike.', '**Each hostile building/token removed in battle on your turn normally scores two VP: one removal VP plus one Infamy. A hostile warrior scores one Infamy, except the warrior that first caused Hostile status.** Infamy depends on whose turn it is, rather than which side attacks: no Infamy on another player\'s turn, and none from Strike.')]
for a,b in replacements:
 assert a in s,a
 s=s.replace(a,b)
p.write_text(s)
I=R/'source-audit-candidate-03';I.mkdir();shutil.copyfile(p,I/'summary-snapshot.md');save(I/'input-manifest.json',{'hashes':{str(x):sha(x) for x in [I/'summary-snapshot.md',ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']},'reason':'General rule clarifications after expanded readers; question/key unchanged.'})
