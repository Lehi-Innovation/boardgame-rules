"""Verify whole original-record review pieces against public runtime outputs.

CLI use is production-only. The injected-byte API is exercised with neutral
JSONL fixtures; no production provenance/runtime is opened by tests or imports.
"""
import argparse
import json
import sys
from pathlib import Path
from staged_common import (Context, checked_archives, closed_draft, draft_criteria, draft_fence_errors, load, locate_runtime,
                           runtime_records, same, sha, write_new)


def declared_receipt_chunks(receipt):
    """Select the original whole-range declaration without normalizing it.

    displayed_chunks is a faithful alias only. If both keys are present their
    complete JSON values, including unknown fields and number types, must agree.
    The original list object and ranges are returned unchanged.
    """
    if 'chunks' in receipt and 'displayed_chunks' in receipt and not same(receipt['chunks'], receipt['displayed_chunks']):
        raise ValueError('Conflicting chunks and displayed_chunks declarations')
    key = 'chunks' if 'chunks' in receipt else 'displayed_chunks' if 'displayed_chunks' in receipt else None
    return key, receipt.get(key) if key is not None else None


def public_texts(value):
    """Only traverse the already-selected PUBLIC custom_tool_call_output value."""
    if isinstance(value, str):
        yield value
        try:
            decoded = json.loads(value)
        except ValueError:
            decoded = None
        if isinstance(decoded, (dict, list)):
            yield from public_texts(decoded)
        else:
            for line in value.splitlines():
                if line.startswith(('{', '[')):
                    try:
                        decoded = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(decoded, (dict, list)):
                        yield from public_texts(decoded)
    elif isinstance(value, list):
        for child in value:
            yield from public_texts(child)
    elif isinstance(value, dict):
        for child in value.values():
            yield from public_texts(child)


def context_metadata(records):
    result = []
    for ordinal, raw, row in records:
        payload = row.get('payload', {})
        if not isinstance(payload, dict):
            continue
        kind = row.get('type', payload.get('type'))
        if kind not in ('turn_context', 'model_context'):
            continue
        values = {key: payload[key] for key in ('model', 'effort', 'reasoning_effort')
                  if isinstance(payload.get(key), str)}
        if values:
            result.append({'ordinal': ordinal, 'record_sha256': sha(raw), **values})
    return {'recognized_runtime_contexts': result,
            'status': 'recorded_contexts_not_model_identity_attestation',
            'limit': 'No model/effort requirement is present in the shared manifest. Provenance settings are not independently attested by this transport validator.'}


def verify_payloads(ctx, label, runtime_path, runtime_raw):
    """Read only frozen files/own archives plus explicitly injected JSONL bytes."""
    original_path, original = closed_draft(ctx, label)
    final_path = ctx.work(label, 'final')
    final = load(final_path)
    start_path = ctx.root / ('reader-' + label + '-review-start.json')
    start = load(start_path)
    errors = []
    errors.extend(draft_fence_errors(ctx, label, start))
    if start.get('reader') != label or start.get('task') != ctx.manifest['reader_tasks'][label]:
        errors.append('Review fence reader/task mismatch')
    if start.get('runtime_path') != str(Path(runtime_path).resolve()):
        errors.append('Review runtime path differs from fenced reader runtime')
    if start.get('draft_sha256') != sha(original_path.read_bytes()) or start.get('frozen_inputs') != ctx.frozen():
        errors.append('Review fence frozen draft/input binding mismatch')
    prefix_size = start.get('runtime_prefix_bytes')
    valid_prefix_size = type(prefix_size) is int and 0 <= prefix_size <= len(runtime_raw)
    if not valid_prefix_size or sha(runtime_raw[:prefix_size]) != start.get('runtime_prefix_sha256'):
        errors.append('Runtime is not an append-only continuation of the fenced prefix')
    try:
        records = runtime_records(runtime_raw)
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append('Invalid runtime JSONL/ordinal sequence: ' + str(exc))
        records = []
    try:
        fenced = runtime_records(runtime_raw[:prefix_size]) if valid_prefix_size else []
    except (ValueError, KeyError, TypeError, AttributeError):
        errors.append('Saved runtime prefix does not end at its original JSONL record boundary')
        fenced = []
    fence = start.get('after_ordinal')
    if type(fence) is not int or fence != (fenced[-1][0] if fenced else -1) or len(fenced) != start.get('runtime_record_count_at_start'):
        errors.append('Saved runtime fence ordinal/count mismatch')
        fence = records[-1][0] if records else -1
    review_history, history_errors = checked_archives(ctx, label, 'review')
    if history_errors or len(review_history) != (ctx.n + 19) // 20:
        errors.append('Complete structurally valid review history required')
    if not review_history or final_path.read_bytes() != review_history[-1][0].read_bytes():
        errors.append('Final work bytes must equal the last review snapshot')
    public = []
    for ordinal, raw, row in records:
        payload = row.get('payload', {})
        if ordinal > fence and isinstance(payload, dict) and payload.get('type') == 'custom_tool_call_output':
            public.append((ordinal, sha(raw), list(public_texts(payload.get('output')))))
    receipts = final.get('self_review', {}).get('receipts', [])
    if not isinstance(receipts, list) or [r.get('id') if isinstance(r, dict) else None for r in receipts] != [q['id'] for q in ctx.questions]:
        errors.append('Final receipts must cover every frozen question exactly once in bank order')
        receipts = receipts if isinstance(receipts, list) else []
    proofs, used_ordinals, last_ordinal = [], set(), fence
    for index, (question, answer) in enumerate(zip(ctx.questions, original['answers'])):
        record = {'id': question['id'], 'errors': [], 'chunks': []}
        try:
            payload = ctx.method['review_display_record'](question, answer, original.get('evidence_units', {}))
            record.update({'payload_sha256': payload['sha256'], 'payload_characters': payload['characters'],
                           'original_answer_sha256': sha(json.dumps(answer, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()),
                           'explicit_shared_unit_count': len(payload['payload']['explicitly_referenced_shared_evidence'])})
            receipt = receipts[index] if index < len(receipts) else {}
            if not isinstance(receipt, dict) or receipt.get('id') != question['id'] or receipt.get('payload_sha256') != payload['sha256']:
                record['errors'].append('Original-record payload hash/ID mismatch')
                receipt = receipt if isinstance(receipt, dict) else {}
            record['original_receipt_keys_present'] = [key for key in ('chunks', 'displayed_chunks') if key in receipt]
            record['original_receipt_key'] = None
            key, chunks = declared_receipt_chunks(receipt)
            record['original_receipt_key'] = key
            cursor = 0
            if not isinstance(chunks, list) or not chunks:
                record['errors'].append('Nonempty full contiguous Unicode ranges required')
                chunks = []
            for chunk in chunks:
                if not isinstance(chunk, dict):
                    record['errors'].append('Chunk must be an object')
                    continue
                start_char, end = chunk.get('start'), chunk.get('end')
                if type(start_char) is not int or type(end) is not int or start_char != cursor or not 0 <= start_char < end <= len(payload['text']) or end - start_char > 2900:
                    record['errors'].append('Chunk is not a contiguous bounded Unicode range')
                    continue
                piece = payload['text'][start_char:end]
                digest = sha(piece.encode('utf-8'))
                chunk_proof = {'start': start_char, 'end': end, 'sha256': digest, 'runtime_matches': []}
                if digest != chunk.get('sha256'):
                    record['errors'].append('Chunk hash mismatch')
                # One whole original declared piece per actual response. A
                # response cannot be subdivided/reused as multiple receipts.
                for ordinal, raw_sha, texts in public:
                    if ordinal in used_ordinals or ordinal <= last_ordinal:
                        continue
                    for text in texts:
                        if piece not in text:
                            continue
                        # Reject a claimed piece cut out of a larger actual
                        # display of this same contiguous review payload.
                        left_extension = payload['text'][max(0, start_char - 1):end] if start_char else None
                        right_extension = payload['text'][start_char:min(len(payload['text']), end + 1)] if end < len(payload['text']) else None
                        if (left_extension is not None and left_extension in text) or (right_extension is not None and right_extension in text):
                            continue
                        chunk_proof['runtime_matches'].append({'ordinal': ordinal, 'record_sha256': raw_sha,
                                                              'public_text_sha256': sha(text.encode('utf-8'))})
                        break
                if not chunk_proof['runtime_matches']:
                    record['errors'].append('Whole declared piece absent from a distinct post-fence public output in review order')
                else:
                    selected = chunk_proof['runtime_matches'][0]
                    chunk_proof['selected_runtime_proof'] = selected
                    used_ordinals.add(selected['ordinal'])
                    last_ordinal = selected['ordinal']
                record['chunks'].append(chunk_proof)
                cursor = end
            if cursor != len(payload['text']):
                record['errors'].append('Receipt ranges do not reach original payload EOF')
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            record['errors'].append(str(exc))
        record['pass'] = not record['errors']
        proofs.append(record)
    criteria = draft_criteria(ctx, label)
    payload_pass = not errors and len(proofs) == ctx.n and all(p['pass'] for p in proofs)
    workflow_pass = criteria['draft_workflow_conformance_pass']
    return {'reader': label, 'task': ctx.manifest['reader_tasks'][label], **criteria,
            'payload_delivery_pass': payload_pass, 'workflow_conformance_pass': workflow_pass,
            'pass': payload_pass and workflow_pass,
            'overall_technical_pass': payload_pass and workflow_pass,
            'workflow_deviation_factual_grade_cap': False,
            'errors': errors, 'question_count': ctx.n, 'frozen_inputs': ctx.frozen(),
            'draft_sha256': sha(original_path.read_bytes()), 'final_sha256': sha(final_path.read_bytes()),
            'review_start_sha256': sha(start_path.read_bytes()), 'after_ordinal': fence,
            'runtime_path': str(Path(runtime_path).resolve()), 'runtime_sha256': sha(runtime_raw),
            'runtime_maximum_ordinal': records[-1][0] if records else -1,
            'payloads': proofs, 'actual_model_context_validation': context_metadata(records),
            'no_hidden_instructions_or_ciphertext_copied': True,
            'limit': 'Exact original-record text availability after the saved fence only. This proves neither reading/comprehension nor semantic correctness, tool budget, first review-continuation dispatch time, or delivery before a particular final-file write.'}


def verify_production(iteration, label):
    ctx = Context(iteration)
    path, provenance = locate_runtime(ctx, label)
    result = verify_payloads(ctx, label, path, path.read_bytes())
    result['production_runtime_locator'] = provenance
    number = 1
    while (ctx.root / ('reader-' + label + '-review-payload-validation-' + format(number, '02') + '.json')).exists():
        number += 1
    write_new(ctx.root / ('reader-' + label + '-review-payload-validation-' + format(number, '02') + '.json'), result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    parser.add_argument('label', choices=['a', 'b'])
    args = parser.parse_args()
    report = verify_production(args.iteration, args.label)
    print(json.dumps({'reader': args.label, 'pass': report['pass'], 'errors': report['errors'],
                      'payload_delivery_pass': report['payload_delivery_pass'],
                      'workflow_conformance_pass': report['workflow_conformance_pass'],
                      'verified_payloads': sum(p['pass'] for p in report['payloads']), 'question_count': report['question_count']}))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
