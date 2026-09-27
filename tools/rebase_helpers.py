"""Byte-exact helpers used for the 1.19.3 update (see docs/CHANGELOG.md).

Everything works on raw bytes so encodings (BOM or not) and line endings are
preserved exactly; nothing is re-encoded.
"""
import re

import os
VANILLA = os.environ.get("HOI4_PATH", r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")


def eol_of(data):
    return b"\r\n" if b"\r\n" in data else b"\n"


def to_eol(data, eol):
    data = data.replace(b"\r\n", b"\n")
    return data.replace(b"\n", eol) if eol == b"\r\n" else data


def block_end(data, open_brace_index):
    """Index just past the '}' matching the '{' at open_brace_index.
    Skips '#' comments and quoted strings (with \\" escapes)."""
    i, depth, n = open_brace_index, 0, len(data)
    while i < n:
        c = data[i:i + 1]
        if c == b"#":
            j = data.find(b"\n", i)
            i = n if j < 0 else j
            continue
        if c == b'"':
            i += 1
            while i < n and data[i:i + 1] != b'"':
                i += 2 if data[i:i + 1] == b"\\" else 1
        elif c == b"{":
            depth += 1
        elif c == b"}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced block")


def find_block(data, key, start=0, top_level_only=True):
    """(start, end) byte span of `key = { ... }`, including leading indentation."""
    pat = re.compile(rb"(?m)^" + (b"" if top_level_only else rb"[ \t]*") + re.escape(key) + rb"[ \t]*=[ \t]*\{")
    m = pat.search(data, start)
    if not m:
        return None
    return m.start(), block_end(data, m.end() - 1)
