"""Faithful receipt-coordinate normalization, never proof of visible delivery."""
import hashlib


def normalize_offset_receipts(text, chunks):
    """Accept one consistent, complete, hash-verified character or UTF8-byte scheme.

    A returned range always describes the same whole original chunk. Actual
    model-visible payload matching and timing must be checked separately.
    """
    raw = text.encode('utf-8')
    if not isinstance(chunks, list) or not chunks:
        raise ValueError('Nonempty original chunk receipts required')
    for mode in ('unicode_characters', 'utf8_bytes'):
        normalized, cursor = [], 0
        try:
            for chunk in chunks:
                start = chunk.get('start', chunk.get('start_char'))
                end = chunk.get('end', chunk.get('end_char_exclusive'))
                digest = chunk.get('sha256', chunk.get('utf8_chunk_sha256'))
                limit = len(text) if mode == 'unicode_characters' else len(raw)
                if type(start) is not int or type(end) is not int or not 0 <= start < end <= limit or start != cursor:
                    raise ValueError('Incomplete or invalid coordinate sequence')
                if mode == 'unicode_characters':
                    first, last, piece = start, end, text[start:end]
                else:
                    first = len(raw[:start].decode('utf-8'))
                    piece = raw[start:end].decode('utf-8')
                    last = first + len(piece)
                if hashlib.sha256(piece.encode()).hexdigest() != digest:
                    raise ValueError('Original chunk hash does not match these coordinates')
                normalized.append({'start': first, 'end': last, 'sha256': digest,
                                   'original_start': start, 'original_end': end})
                cursor = end
            if cursor != limit:
                raise ValueError('Receipt does not reach EOF')
        except (ValueError, UnicodeError):
            continue
        return {'original_offset_unit': mode, 'chunks': normalized,
                'one_original_payload_per_normalized_range': True,
                'actual_visibility_or_pre_save_timing_certified': False}
    raise ValueError('No complete faithful hash-verified coordinate interpretation')
