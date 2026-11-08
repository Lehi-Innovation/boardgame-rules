"""Neutral end-to-end regression for exact dictionary/list reference joins."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

R = Path(__file__).parent.resolve()


def normalized(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


class ReferenceFormatsTest(unittest.TestCase):
    def test_exact_same_entry_join_preserves_wrong_quotes_and_excludes_unreferenced_units(self):
        with tempfile.TemporaryDirectory(prefix='neutral-reference-') as temp:
            root = Path(temp)
            script = root / 'materialize_reader_evidence_v2.py'
            shutil.copyfile(R / script.name, script)
            it = root / 'sample'
            (it / 'grading-inputs').mkdir(parents=True)
            summary = '## Neutral\n\nComplete permitted text.\n'
            (it / 'summary-snapshot.md').write_text(summary)
            a = {'id': 'T001', 'answer': {'evidence_refs': ['item/α']}}
            b = {'id': 'T001', 'evidence': [1]}
            wrong = {'text': 'An intentionally wrong quotation.', 'start': 0, 'end': 5}
            exact = {'number': 1, 'text': summary,
                     'source_span': {'start': 0, 'end': len(summary)}}
            docs = {'a': {'answers': [a], 'evidence_units': {
                'item/α': wrong, 'unreferenced': {'text': summary}}},
                'b': {'answers': [b], 'evidence_units': [exact]}}
            wrappers = {}
            for c, doc in docs.items():
                (it / f'reader-{c}.json').write_text(json.dumps(doc, ensure_ascii=False) + '\n')
                entry = doc['answers'][0]
                wrappers[c] = {'complete_original_entry': entry,
                               'normalized_entry_sha256': normalized(entry),
                               'raw_entry_sha256': 'neutral-wrapper-source-hash'}
            bundle = {'entries': [{'id': 'T001', 'readers': wrappers}]}
            p = it / 'grading-inputs/block-01.json'
            p.write_text(json.dumps(bundle, ensure_ascii=False) + '\n')
            manifest = {'question_count': 1, 'blocks': [{'path': str(p)}]}
            (it / 'grading-inputs/manifest.json').write_text(json.dumps(manifest))
            run = subprocess.run([sys.executable, str(script), 'sample'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads((it / 'grading-inputs-v2/block-01.json').read_text())
            for c, original in [('a', a), ('b', b)]:
                self.assertEqual(result['entries'][0]['readers'][c]['complete_original_entry'], original)
            joined_a = result['entries'][0]['readers']['a']['explicitly_referenced_shared_evidence']['resolved_units']
            self.assertEqual(len(joined_a), 1)
            self.assertEqual(joined_a[0]['original_unit'], wrong)
            self.assertFalse(joined_a[0]['unit_text_matches_frozen_summary'])
            self.assertEqual(joined_a[0]['original_raw_unit_span']['json_pointer'], '/evidence_units/item~1α')
            self.assertEqual(joined_a[0]['explicit_reference_paths_in_original_entry'], ['/answer/evidence_refs/0'])
            joined_b = result['entries'][0]['readers']['b']['explicitly_referenced_shared_evidence']['resolved_units']
            self.assertEqual(joined_b[0]['original_unit'], exact)
            self.assertTrue(joined_b[0]['unit_text_matches_frozen_summary'])
            self.assertEqual(joined_b[0]['original_raw_unit_span']['json_pointer'], '/evidence_units/0')
            for c, joined in [('a', joined_a), ('b', joined_b)]:
                raw = (it / f'reader-{c}.json').read_bytes()
                span = joined[0]['original_raw_unit_span']
                chunk = raw[span['start_byte']:span['end_byte']]
                self.assertEqual(json.loads(chunk), joined[0]['original_unit'])
                self.assertEqual(hashlib.sha256(chunk).hexdigest(), span['raw_sha256'])


if __name__ == '__main__':
    unittest.main()
