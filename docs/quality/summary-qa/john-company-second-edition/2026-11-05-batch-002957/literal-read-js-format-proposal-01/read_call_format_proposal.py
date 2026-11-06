"""UNADOPTED narrow read-call normalization proposal. Never evaluates JavaScript or shell.

Normalization is not approval: the frozen proof's whole-command allowlist and all
delivery/boundary/output checks remain authoritative. No runtime is read at import.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

_FROZEN_SOURCE_HASHES = {
    'prove-single-reader-grading-delivery-literal-equivalent.py':
        '07b3402017f1207c6b16513614b783f4e554cee0864637e48adc98b2adb37589',
    'prove-bounded-delivery.py':
        '5f95d57189dbf3c449d47ad375e35cbf32b83bfb2bd00bb876f27f40ab857318',
}

_WS = r'[ \t\r\n\v\f]*'
_REQUIRED_WS = r'[ \t\r\n\v\f]+'
# A strict JSON string token. Excluding raw U+2028/U+2029 avoids historical JS
# line-terminator ambiguity; their JSON-escaped forms remain supported.
_STRING = r'"(?:[^"\\\x00-\x1f\u2028\u2029]|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*"'
_CALL = re.compile(
    rf'\A{_WS}const{_REQUIRED_WS}r{_WS}={_WS}await{_REQUIRED_WS}'
    rf'tools{_WS}\.{_WS}exec_command{_WS}\({_WS}\{{{_WS}'
    rf'(?:cmd|"cmd"){_WS}:{_WS}(?P<first>{_STRING})'
    rf'(?:{_WS}\+{_WS}(?P<second>{_STRING}))?{_WS},{_WS}'
    rf'(?:max_output_tokens|"max_output_tokens"){_WS}:{_WS}24000{_WS}'
    rf'\}}{_WS}\){_WS};{_WS}text{_WS}\({_WS}r{_WS}\.{_WS}output{_WS}\){_WS};{_WS}\Z'
)


def canonical_read_body(body):
    """Return the original literal_read_call spelling, or None for other syntax.

    This function knows no paths, modes, source facts or approved commands. A
    canonical result still requires exact membership in the frozen allowlist.
    Only the two literal values are decoded; no JS/shell parser or evaluator runs.
    """
    if not isinstance(body, str):
        return None
    match = _CALL.fullmatch(body)
    if match is None:
        return None
    try:
        parts = [json.loads(match.group('first'))]
        if match.group('second') is not None:
            parts.append(json.loads(match.group('second')))
    except (ValueError, TypeError):
        return None
    command = ''.join(parts)
    # Reject lone surrogates. Valid escaped pairs decode to one code point.
    if any(0xD800 <= ord(char) <= 0xDFFF for char in command):
        return None
    return ('const r = await tools.exec_command({cmd: ' + json.dumps(command)
            + ', max_output_tokens: 24000});\ntext(r.output);')


def make_call_body(original_call_body):
    """Preserve the original strip/leading-@exec/first-write behavior, then normalize.

    Failed parsing retains the original body, so unknown calls remain unknown.
    Raw call inputs continue to be recorded by the original session_delivery.
    """
    def call_body(code):
        body = original_call_body(code)
        canonical = canonical_read_body(body)
        return body if canonical is None else canonical
    return call_body


def install_on_module(original):
    """Override only an in-memory imported module's call_body; no files are edited."""
    original.call_body = make_call_body(original.call_body)
    return original


def load_proposal_proof():
    """Import only the two permitted generic proof sources; read no runtime/data."""
    root = Path(__file__).resolve().parent.parent
    for name, expected in _FROZEN_SOURCE_HASHES.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Generic proof source differs from reviewed frozen hash: ' + name)
    path = root / 'prove-single-reader-grading-delivery-literal-equivalent.py'
    spec = importlib.util.spec_from_file_location('literal_delivery_js_format_proposal', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return install_on_module(module)


def prove(bank_name, iteration, role, prefix, *, output_name):
    """Future-use API only; NOT called by the neutral suite or during this review.

    An independent fresh technical review and explicit future authorization are
    required before actual use. The frozen prove still writes exclusively ('x').
    No default/old proof filename is available through this wrapper.
    """
    if not isinstance(output_name, str) or not re.fullmatch(
            r'[A-Za-z0-9][A-Za-z0-9._-]*-js-format-proposal-proof\.json', output_name):
        raise ValueError('Require an explicit new *-js-format-proposal-proof.json basename')
    original = load_proposal_proof()
    return original.prove(bank_name, iteration, role, prefix, output_name=output_name)


if __name__ == '__main__':
    raise SystemExit('Unadopted proposal: no command-line runtime execution is provided.')
