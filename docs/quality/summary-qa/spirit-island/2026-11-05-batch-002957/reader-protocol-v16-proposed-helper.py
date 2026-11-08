"""Rule-agnostic exact Markdown units. Offsets are Unicode code points."""
import re


def unit(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    if not 0 <= start < end <= len(text):
        raise ValueError("Empty or invalid unit")
    return {"start": start, "end": end, "text": text[start:end]}


def lines(text):
    result, start = [], 0
    for value in text.splitlines(keepends=True):
        end = start + len(value)
        result.append((start, end, value.rstrip("\r\n")))
        start = end
    return result


def line_index(text, offset):
    if not 0 <= offset < len(text):
        raise ValueError("Offset outside original text")
    return next(i for i, (a, b, _) in enumerate(lines(text)) if a <= offset < b)


def cells(value):
    value = value.strip()
    if not value.startswith("|") or not value.endswith("|"):
        raise ValueError("A complete table row needs both outer pipes")
    result, current, escaped = [], [], False
    for char in value[1:-1]:
        if char == "|" and not escaped:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped
    result.append("".join(current).strip())
    return result


def separator(value):
    try:
        return all(re.fullmatch(r":?-{3,}:?", c) for c in cells(value))
    except ValueError:
        return False


def table_units(text, offset):
    """Return nearest controlling header and complete row, never fixed lengths."""
    ls = lines(text)
    i = line_index(text, offset)
    row = ls[i][2].strip()
    cells(row)
    if separator(row):
        raise ValueError("Separator is not a data row")
    first = i
    while first > 0 and ls[first - 1][2].strip().startswith("|"):
        first -= 1
    separators = [j for j in range(first + 1, i) if separator(ls[j][2])]
    if not separators:
        raise ValueError("No preceding complete table header/separator")
    sep = separators[-1]
    header = unit(text, ls[sep - 1][0], ls[sep - 1][1])
    data = unit(text, ls[i][0], ls[i][1])
    count = len(cells(header["text"]))
    if len(cells(ls[sep][2])) != count or len(cells(data["text"])) != count:
        raise ValueError("Row/header/separator column count differs")
    validate_table_unit(text, data, header)
    return {"header": header, "row": data, "cell_count": count}


def validate_table_unit(text, row, header=None):
    if row["text"] != text[row["start"]:row["end"]]:
        raise ValueError("Quote differs from original Unicode span")
    ls = lines(text)
    a, b, value = ls[line_index(text, row["start"])]
    expected = unit(text, a, b)
    actual = {key: row[key] for key in ("start", "end", "text")}
    if actual != expected or "\n" in row["text"] or "\r" in row["text"]:
        raise ValueError("Quote is not the complete original table line")
    count = len(cells(row["text"]))
    if header is not None:
        if header["text"] != text[header["start"]:header["end"]]:
            raise ValueError("Header differs from original Unicode span")
        if count != len(cells(header["text"])):
            raise ValueError("Row/header column count differs")
    return True


def paragraph_unit(text, offset):
    """Select the complete blank-line-delimited paragraph containing offset."""
    if not 0 <= offset < len(text):
        raise ValueError("Offset outside original text")
    left = 0
    for match in re.finditer(r"\n[ \t\r]*\n", text):
        if left <= offset < match.start():
            return unit(text, left, match.start())
        left = match.end()
    if left <= offset < len(text):
        return unit(text, left, len(text))
    raise ValueError("Offset selects blank separation rather than content")


def list_item_unit(text, offset):
    """Select one complete item, including nested items and indented paragraphs."""
    ls = lines(text)
    marker = re.compile(r"^( *)(?:[-+*]|\d+[.)])[ \t]+")
    candidates = []
    for i, (start, _, value) in enumerate(ls):
        match = marker.match(value)
        if not match or start > offset:
            continue
        indent = len(match.group(1))
        end, after_blank = len(text), False
        for a, _, following in ls[i + 1:]:
            other = marker.match(following)
            if other and len(other.group(1)) <= indent:
                end = a
                break
            if re.match(r"^#{1,6}\s", following):
                end = a
                break
            if not following.strip():
                after_blank = True
                continue
            leading = len(following) - len(following.lstrip(" "))
            if after_blank and not other and leading <= indent:
                end = a
                break
            after_blank = False
        result = unit(text, start, end)
        if result["start"] <= offset < result["end"]:
            candidates.append((indent, start, result))
    if not candidates:
        raise ValueError("Offset is not inside a complete list item")
    return max(candidates, key=lambda x: (x[0], x[1]))[2]


def validate_text_unit(text, selected, kind):
    extractor = {"paragraph": paragraph_unit, "list_item": list_item_unit}[kind]
    actual = {key: selected[key] for key in ("start", "end", "text")}
    if actual != extractor(text, selected["start"]):
        raise ValueError("Selection is not the complete original unit")
    return True


def table_field_values(text, offset):
    """Render lookup attributes from source columns without regenerating values."""
    selected = table_units(text, offset)
    headings = cells(selected["header"]["text"])
    values = cells(selected["row"]["text"])
    selected["fields"] = [
        {"column_index": i, "column": heading, "value": value}
        for i, (heading, value) in enumerate(zip(headings, values))
    ]
    return selected


def subsection_unit(text, offset):
    """Complete requested section, including its opening and nested subsections."""
    if not 0 <= offset < len(text):
        raise ValueError("Offset outside original text")
    headings = list(re.finditer(r"(?m)^(#{1,6})[ \t]+[^\n]+", text))
    preceding = [i for i, h in enumerate(headings) if h.start() <= offset]
    if not preceding:
        raise ValueError("No preceding section heading")
    i = preceding[-1]
    level = len(headings[i].group(1))
    end = next((h.start() for h in headings[i + 1:]
                if len(h.group(1)) <= level), len(text))
    return unit(text, headings[i].start(), end)
