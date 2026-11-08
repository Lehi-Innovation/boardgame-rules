"""Generic Markdown source extraction; no rule facts or question maps."""
import re
import hashlib


def question_records(document):
    """Original ordered records, without assuming contiguous numeric IDs."""
    records = document['questions'] if isinstance(document, dict) else document
    if not isinstance(records, list):
        raise ValueError('Question records must be a list')
    ids = []
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get('id'), str) \
                or not isinstance(record.get('question'), str):
            raise ValueError('Each question requires its original ID and literal text')
        ids.append(record['id'])
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate question ID')
    return records


def question_batch(document, completed_count, size=10):
    """Take the next actual records; never reconstruct IDs or asks from memory."""
    records = question_records(document)
    if not isinstance(completed_count, int) or not 0 <= completed_count <= len(records):
        raise ValueError('Invalid completed prefix count')
    if not isinstance(size, int) or size <= 0:
        raise ValueError('Invalid batch size')
    return records[completed_count:min(completed_count + size, len(records))]


def new_answer_record(original_question_record):
    """Start an answer with its actual ask before selecting any rule evidence."""
    question_records([original_question_record])
    return {'id': original_question_record['id'],
            'literal_question': original_question_record['question']}


def validate_question_bindings(document, answers, complete=False):
    """Structural ID/literal binding only; does not judge semantic correctness."""
    records = question_records(document)
    if not isinstance(answers, list) or len(answers) > len(records):
        raise ValueError('Invalid answer prefix')
    if complete and len(answers) != len(records):
        raise ValueError('Incomplete bank')
    for answer, record in zip(answers, records):
        if answer.get('id') != record['id'] or answer.get('literal_question') != record['question']:
            raise ValueError('Answer is not bound to its exact original question record')
    return True


def new_clause_record(answer_record, start, end):
    """Bind one asked span to the current literal question before rule lookup.

    This records text association only. It neither divides the question into
    semantic requirements nor supplies or validates any rule answer.
    """
    literal = answer_record.get('literal_question')
    if not isinstance(literal, str) or not isinstance(answer_record.get('id'), str):
        raise ValueError('Start with the current original answer record')
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(literal):
        raise ValueError('Invalid literal-question span')
    piece = literal[start:end]
    if not piece.strip():
        raise ValueError('Empty asked span')
    return {'literal_ask': piece, 'question_start': start, 'question_end': end}


def validate_clause_bindings(document, answers, complete=False):
    """Check exact current-question clause spans; semantic checks remain reader's."""
    validate_question_bindings(document, answers, complete=complete)
    for answer in answers:
        clauses = answer.get('clauses')
        if not isinstance(clauses, list) or not clauses:
            raise ValueError('Each answer needs its actual asked spans')
        for clause in clauses:
            if not isinstance(clause, dict):
                raise ValueError('A clause must retain its literal-question span')
            expected = new_clause_record(answer, clause.get('question_start'), clause.get('question_end'))
            if any(clause.get(key) != value for key, value in expected.items()):
                raise ValueError('Clause is not the exact span of this current question')
    return True


def chunk_record(text, start, limit=5800):
    """One bounded actual text block; the final remainder is also clamped."""
    if not isinstance(limit, int) or not 0 < limit <= 6000:
        raise ValueError("Invalid chunk limit")
    if not isinstance(start, int) or not 0 <= start < len(text):
        raise ValueError("Invalid chunk start")
    end = min(start + limit, len(text))
    piece = text[start:end]
    return {"start": start, "end": end, "characters": len(piece),
            "sha256": hashlib.sha256(piece.encode("utf-8")).hexdigest(),
            "text": piece}


def unit_display_blocks(record, limit=5800):
    """Display complete evidence in bounded pieces, retaining the full raw unit.

    Emit one yielded piece per actual tool response. This is transport only;
    it neither chooses relevant rules nor changes evidence saved in answers.
    """
    if not isinstance(limit, int) or not 0 < limit <= 6000:
        raise ValueError('Invalid display bound')
    spans = [(key, record[key]) for key in ('introduction', 'header', 'row', 'unit')
             if isinstance(record.get(key), dict) and isinstance(record[key].get('text'), str)]
    if not spans and isinstance(record.get('text'), str):
        spans = [('unit', record)]
    if not spans:
        raise ValueError('No complete source text to display')
    for label, span in spans:
        value = span['text']
        for start in range(0, len(value), limit):
            block = chunk_record(value, start, limit)
            origin = span.get('start')
            yield {**block, 'piece_of': label,
                   'source_start': origin + block['start'] if isinstance(origin, int) else None,
                   'source_end': origin + block['end'] if isinstance(origin, int) else None}


def _span(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    if not 0 <= start < end <= len(text):
        raise ValueError("Empty or invalid source span")
    return {"start": start, "end": end, "text": text[start:end]}


def _lines(text):
    result, start = [], 0
    for line in text.splitlines(keepends=True):
        end = start + len(line)
        result.append((start, end, line.rstrip("\r\n")))
        start = end
    return result


def _cells(line):
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError("Table row lacks an outer pipe")
    result, current, escaped = [], [], False
    for char in line[1:-1]:
        if char == "|" and not escaped:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped
    result.append("".join(current).strip())
    return result


def _separator(line):
    try:
        return all(re.fullmatch(r":?-{3,}:?", c) for c in _cells(line))
    except ValueError:
        return False


def _table(text, offset):
    lines = _lines(text)
    i = next(i for i, (a, b, _) in enumerate(lines) if a <= offset < b)
    row = _span(text, lines[i][0], lines[i][1])
    if _separator(row["text"]):
        raise ValueError("Separator is not a data row")
    first = i
    while first > 0 and lines[first - 1][2].strip().startswith("|"):
        first -= 1
    separators = [j for j in range(first + 1, i) if _separator(lines[j][2])]
    if not separators:
        raise ValueError("No controlling header before requested row")
    sep = separators[-1]
    headings = _cells(lines[sep - 1][2])
    values = _cells(row["text"])
    if len(headings) != len(values) or len(_cells(lines[sep][2])) != len(values):
        raise ValueError("Header, separator and row column counts differ")
    header = _span(text, lines[sep - 1][0], lines[sep][1])
    result = {"kind": "table", "header": header, "row": row,
            "fields": [{"column_index": n, "column": h, "value": v}
                       for n, (h, v) in enumerate(zip(headings, values))]}
    prior = [h for h in heading_index(text) if h["start"] < lines[first][0]]
    if prior and prior[-1]["level"] >= 2:
        result["introduction"] = _span(text, prior[-1]["start"], lines[first][0])
    return result


def heading_index(text):
    return [{"start": m.start(), "end": m.end(), "level": len(m.group(1)),
             "title": m.group(2)}
            for m in re.finditer(r"(?m)^(#{1,6})[ \t]+([^\n]+)", text)]


def heading_paths(text):
    """Index actual headings with ancestors; prose mentions are never headings."""
    result, ancestors = [], []
    for h in heading_index(text):
        while ancestors and ancestors[-1]["level"] >= h["level"]:
            ancestors.pop()
        result.append({**h, "path": [a["title"] for a in ancestors] + [h["title"]]})
        ancestors.append(h)
    return result


def extract_heading_unit(text, title, path=None):
    """Exact-title lookup, rejecting missing/ambiguous names and bare headings.

    This locates a complete unit; the caller must still judge its relevance and
    retrieve every other controlling rule needed for each asked clause.
    """
    def norm(s):
        return " ".join(s.split()).casefold()
    matches = [h for h in heading_paths(text) if norm(h["title"]) == norm(title)]
    if path is not None:
        wanted = [norm(part) for part in path]
        matches = [h for h in matches if [norm(part) for part in h["path"]] == wanted]
    if len(matches) != 1:
        raise ValueError("Exact heading lookup requires one unambiguous title/path")
    unit = extract_unit(text, matches[0]["start"])
    content = unit.get("unit", unit.get("row", {})).get("text", "")
    operative_lines = [line for line in content.splitlines()
                       if line.strip() and not re.match(r"^#{1,6}[ \t]+", line)]
    if not operative_lines:
        raise ValueError("Heading has no operative body")
    return unit


def _paragraph(text, offset):
    start = 0
    for match in re.finditer(r"\n[ \t\r]*\n", text):
        if start <= offset < match.start():
            return _span(text, start, match.start())
        start = match.end()
    if start <= offset < len(text):
        return _span(text, start, len(text))
    raise ValueError("Offset is in blank separation")


def extract_unit(text, offset):
    """Public API: complete row/fields or governing section, never a bare heading."""
    if not 0 <= offset < len(text):
        raise ValueError("Offset outside original source")
    line = next(line for a, b, line in _lines(text) if a <= offset < b)
    if line.strip().startswith("|"):
        return _table(text, offset)
    heads = heading_index(text)
    ancestors = []
    for item in heads:
        if item["start"] > offset:
            break
        while ancestors and ancestors[-1]["level"] >= item["level"]:
            ancestors.pop()
        ancestors.append(item)
    candidates = [h for h in ancestors if 2 <= h["level"] <= 6]
    if not candidates:
        raise ValueError("Select operative content below a source section heading")
    h = candidates[-1]
    # A nested detail can belong to a numbered procedure. Independent catalog
    # entries otherwise keep their own headings, including levels four to six.
    for parent in reversed(candidates[:-1]):
        first_child = next((other["start"] for other in heads
                            if other["start"] > parent["start"]), len(text))
        intro = text[parent["start"]:first_child]
        if re.search(r"(?m)^\s*\d+[.)][ \t]+", intro):
            h = parent
    end = next((other["start"] for other in heads
                if other["start"] > h["start"] and other["level"] <= h["level"]), len(text))
    whole = _span(text, h["start"], end)
    # Complete governing procedures include peer steps and nested details.
    # Large nonprocedural catalog chapters can use a complete paragraph instead.
    has_steps = bool(re.search(r"(?m)^\s*(?:\d+[.)]|[-+*])[ \t]+", whole["text"]))
    if len(whole["text"]) <= 6000 or has_steps:
        return {"kind": "subsection", "unit": whole, "heading": h}
    paragraph = _paragraph(text, offset)
    if paragraph["text"].startswith("#"):
        raise ValueError("A heading alone is not operative evidence; select a more specific section")
    return {"kind": "paragraph", "unit": paragraph, "heading": h}


def validate_record(text, record):
    """Validate the complete returned structure; optional unit metadata is separate."""
    if record["kind"] == "table":
        expected = extract_unit(text, record["row"]["start"])
        for key in ["header", "row"]:
            actual = {name: record[key][name] for name in ["start", "end", "text"]}
            if actual != expected[key]:
                raise ValueError("Table record differs from complete literal source")
        if record.get("introduction") != expected.get("introduction"):
            raise ValueError("Table introduction differs from governing context")
        actual_fields = [{name: field[name] for name in ["column_index", "column", "value"]}
                         for field in record["fields"]]
        if actual_fields != expected["fields"]:
            raise ValueError("Literal field values differ from source columns")
    else:
        expected = extract_unit(text, record["unit"]["start"])
        actual = {name: record["unit"][name] for name in ["start", "end", "text"]}
        if actual != expected["unit"]:
            raise ValueError("Prose/procedure record is incomplete")
    return True
