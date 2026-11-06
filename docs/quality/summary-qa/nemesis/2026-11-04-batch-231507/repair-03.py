from pathlib import Path
import difflib
R=Path(__file__).resolve().parent;p=Path('rules/nemesis.md');old=p.read_text();s=old
s=s.replace('if any drawn card\'s blood icon contains the Retreat arrow, the Intruder flees:', 'if any drawn card\'s blood icon contains the Retreat arrow, resolve retreat **instead of a numerical endurance/death result**. The Intruder flees:')
s=s.replace('Another Character entering your Pod may launch it immediately. Heavy Objects','**A second Character who boards your waiting Pod may immediately launch it with you aboard; the first occupant does not reserve control of launch.** Heavy Objects')
s=s.replace('### Combat quick reference\n\n','### Combat quick reference\n\n- **Encounter:** clear all connected Noise (including Technical Corridors if connected), draw a bag token, place its matching Intruder, compare its number to all cards in the triggering hand (including Contamination): fewer means Surprise Attack. **Keep the drawn non-Blank token aside outside the bag** until a rule returns it, such as an Intruder hiding in Technical Corridors. A Blank instead restores connected Noise and returns to the bag.\n')
s=s.replace('discover the corresponding Weakness card. The Object is not consumed.','reveal the corresponding Weakness card face up and leave it on the Intruder board. Its rule benefits all players. The Object is not consumed.')
s=s.replace('uses an Escape Pod.** Then:', 'launches in an Escape Pod.** Then:')
(R/'repair-03.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='repair-02',tofile='repair-03')));p.write_text(s)
