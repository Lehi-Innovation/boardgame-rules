"""Run the unchanged full public-delivery matcher for explicitly completed blocks."""
from pathlib import Path
import hashlib,json,sys
B=Path(__file__).resolve().parent
blocks=sorted({int(x) for x in sys.argv[1:]})
assert blocks and all(1<=x<=9 for x in blocks)
source=B/'verify_expanded5_grader_actual_delivery.py'
code=source.read_text()
needle='for number in range(1, 10):\n'
assert code.count(needle)==1
code=code.replace(needle,'for number in '+repr(blocks)+':\n')
needle="dest = D / 'grader-actual-delivery-validation.json'"
assert code.count(needle)==1
filename='grader-actual-delivery-blocks-'+'-'.join(f'{x:02}' for x in blocks)+'.json'
metadata={'subset_only':True,'selected_blocks':blocks,'full_nine_block_proof_still_required':True,'unmodified_matcher_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
code=code.replace(needle,'proof.update('+repr(metadata)+')\n'+'dest = D / '+repr(filename))
namespace={'__file__':str(source)}
exec(compile(code,str(source)+'[selected completed blocks]', 'exec'),namespace)
