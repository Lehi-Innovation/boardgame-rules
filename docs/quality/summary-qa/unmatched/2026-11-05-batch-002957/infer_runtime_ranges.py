"""Recover actual bounded original-text reads from literal runtime slice calls."""
from pathlib import Path
import json
import re
import hashlib


def strings(value):
    if isinstance(value, str):
        yield value
        try:
            decoded = json.loads(value)
            if decoded != value:
                yield from strings(decoded)
        except (ValueError, RecursionError):
            pass
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)
    elif isinstance(value, dict):
        if value.get("type") in ["image", "input_image", "image_url"]:
            return
        for key, child in value.items():
            if key not in ["data", "image_url", "encrypted_content"]:
                yield from strings(child)


def infer_exact_slices(runtime_path, file_path, maximum=5000):
    path = Path(file_path)
    text = path.read_text()
    calls, outputs = [], {}
    for ordinal, line in enumerate(Path(runtime_path).open()):
        record = json.loads(line)
        value = record.get("payload", {})
        if record.get("type") != "response_item":
            continue
        typ, cid = value.get("type"), value.get("call_id")
        if typ in ["custom_tool_call", "function_call"]:
            code = value.get("input", value.get("arguments", ""))
            code = code if isinstance(code, str) else json.dumps(code)
            if path.name in code:
                calls.append((ordinal, cid, code, hashlib.sha256(line.encode()).hexdigest()))
        elif typ == "custom_tool_call_output":
            outputs[cid] = (ordinal, list(strings(value.get("output"))),
                            hashlib.sha256(line.encode()).hexdigest())
    edges = []
    for ordinal, cid, code, digest in calls:
        if cid not in outputs:
            continue
        output_ordinal, leaves, output_digest = outputs[cid]
        for match in re.finditer(r"\[(\d*):(\d*)\]", code):
            start = int(match.group(1)) if match.group(1) else 0
            end = int(match.group(2)) if match.group(2) else len(text)
            if not 0 <= start < end <= len(text) or end - start > maximum:
                continue
            if not any(len(leaf) <= maximum + 1000 and text[start:end] in leaf
                       for leaf in leaves):
                continue
            edges.append({"start": start, "end": end,
                          "runtime_input_ordinal": ordinal,
                          "runtime_output_record_ordinals": [output_ordinal],
                          "runtime_input_sha256": digest,
                          "runtime_output_sha256": output_digest,
                          "exact_expected_text_found": True})
    # Prefer the earliest complete delivery, so later rereads do not replace
    # stronger evidence that the original text arrived before factual output.
    chosen = None
    for threshold in sorted({e["runtime_output_record_ordinals"][0] for e in edges}):
        eligible = [e for e in edges if e["runtime_output_record_ordinals"][0] <= threshold]
        position, candidate = 0, []
        while position < len(text):
            possible = [e for e in eligible if e["start"] <= position < e["end"]]
            if not possible:
                break
            edge = max(possible, key=lambda e: e["end"])
            candidate.append(edge)
            position = edge["end"]
        if position == len(text):
            chosen = candidate
            break
    if chosen is None:
        return None
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "characters": len(text), "complete_contiguous": True,
            "method": "Literal original runtime slice bounds, paired exact bounded output text, earliest complete union; original reader receipt is retained separately.",
            "slices": chosen}
