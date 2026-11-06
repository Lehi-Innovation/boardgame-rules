from pathlib import Path
import difflib
R=Path(__file__).resolve().parent;p=Path('rules/nemesis.md');old=p.read_text();s=old
s=s.replace('Player 1 draws 2, reveals them, keeps 1, and shuffles the other back;','Player 1 draws 2 and **reveals both choices publicly**, keeps 1, and shuffles the other back;')
s=s.replace('2. Draw 1 Intruder Attack card: if it shows','2. **Larva exception: draw no Attack card; use Infest below.** For other Intruders, draw 1 Intruder Attack card: if it shows')
s=s.replace('**If an ordinary Scan shows INFECTED (follow the specific Action procedure; Surgery instead removes Infected cards and the Larva):**','**If an ordinary Scan shows INFECTED (follow its specific Action procedure; Surgery removes Infected cards/Larva, while Rest and Alcohol have the FAQ exceptions below):**')
# Explicit pre-/post-infection outcome reference preserves Room procedures rather than a scenario key.
needle='- When a rule removes a Contamination card, remove it from the game.\n'
addition='''
For the optional **Canteen/Shower hand scan**, the complete outcome is:

| Scan result | Card destination | Character outcome |
|---|---|---|
| Non-Infected | Remove the scanned non-Infected card from the game | No Larva from that result |
| Infected, no Larva already on board | Keep the Infected card | Place a Larva on Character board |
| Infected, Larva already on board | Keep the Infected card | Character dies; place **1 Creeper** in the death Room |

Surgery uses its separate all-zones removal procedure rather than these ordinary scan outcomes.
'''
s=s.replace(needle,needle+addition)
start=s.index('### Victory Check (');end=s.index('### Leaving the game early',start)
s=s[:start]+'''### Victory Check (if at least 1 Character survived by hibernating or launching)

Resolve **Engines → Coordinates → Contamination → Objectives** in that order.

1. **Engines**, only if the ship has survived: reveal all three top Engine tokens. **2 or 3 Damaged Engines make the ship explode. EVERYTHING aboard dies**, including hibernating Characters and Intruders. Launched Pod passengers are already away. A Room Malfunction never changes a Working Engine's token status.
2. **Coordinates**, only if the ship has survived: reveal the Coordinates card and read the destination selected by the Destination marker. **Non-Earth kills hibernating Characters**, while the ship is not destroyed and Intruders remain alive. A sleeper with the **Quarantine Objective** survives if the destination is Mars.
3. **Contamination**, for **every surviving Character, including launched Pod passengers**:
   - **No Larva already on board:** Scan every Contamination card from **Action deck, hand and discard pile**. If none is Infected, there is no four-card draw.
   - **At least one Infected card, OR a Larva already on board:** shuffle **all Action and Contamination cards from deck, hand and discard** into a single new Action deck, then draw the **top 4 cards**. A Larva bypasses only the initial Scan; it does not bypass this shuffle/draw test.
   - **Any Contamination card in those four**, whether Infected or not, kills the Character. No Contamination in those four means survival.
   - This endgame procedure does not remove cards merely because they scanned non-Infected.
4. **Objectives:** each still-living Character reveals their chosen Objective and wins only if all requirements are fulfilled. Merely surviving is insufficient.

'''+s[end:]
(R/'repair-10-full-clarity.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='full-repair-01',tofile='full-repair-02')));p.write_text(s)
