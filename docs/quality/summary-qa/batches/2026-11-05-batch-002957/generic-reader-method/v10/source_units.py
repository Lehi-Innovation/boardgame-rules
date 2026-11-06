"""Generic Markdown source extraction; no rule facts or question maps."""
import re


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
    return {"kind": "table", "header": header, "row": row,
            "fields": [{"column_index": n, "column": h, "value": v}
                       for n, (h, v) in enumerate(zip(headings, values))]}


def heading_index(text):
    return [{"start": m.start(), "end": m.end(), "level": len(m.group(1)),
             "title": m.group(2)}
            for m in re.finditer(r"(?m)^(#{1,6})[ \t]+([^\n]+)", text)]


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
    candidates = [h for h in heads if h["start"] <= offset and 2 <= h["level"] <= 3]
    if not candidates:
        raise ValueError("Select operative content below a source section heading")
    h = candidates[-1]
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
