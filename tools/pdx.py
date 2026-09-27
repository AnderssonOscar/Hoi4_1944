"""Minimal, tolerant parser for Paradox (HOI4) script files.

Used by the checks in this folder. It does not try to understand game
semantics; it only turns `key = { ... }` text into nested Python lists so
checks can walk the tree. Every node remembers the line it came from, so
reports can point at file:line.
"""
import os
import re

TOKEN_RE = re.compile(r'"(?:[^"\\]|\\.)*"|<=|>=|!=|[{}=<>]|[^\s{}=<>"#]+')


class Node:
    __slots__ = ("key", "op", "value", "line")

    def __init__(self, key, op, value, line):
        self.key = key      # str, or None for bare values inside a block
        self.op = op        # '=', '<', '>', ... or None
        self.value = value  # str, or list[Node] for blocks
        self.line = line

    def is_block(self):
        return isinstance(self.value, list)

    def __repr__(self):
        return f"Node({self.key!r} {self.op} {'{...}' if self.is_block() else self.value!r} @{self.line})"


def tokenize(text):
    tokens = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        # strip comments, but not '#' inside quoted strings. Escaped quotes
        # (\" inside division strings) do not end the string.
        out, in_str, esc = [], False, False
        for ch in raw:
            if esc:
                esc = False
            elif ch == "\\" and in_str:
                esc = True
            elif ch == '"':
                in_str = not in_str
            elif ch == "#" and not in_str:
                break
            out.append(ch)
        for m in TOKEN_RE.finditer("".join(out)):
            tokens.append((m.group(0), lineno))
    return tokens


def parse(text):
    """Returns (root_block, problems). problems lists brace imbalances."""
    tokens = tokenize(text)
    problems = []
    root = []
    stack = [(root, 0)]
    i = 0
    n = len(tokens)

    def cur():
        return stack[-1][0]

    while i < n:
        tok, line = tokens[i]
        if tok == "}":
            if len(stack) == 1:
                problems.append((line, "unexpected '}' (more closing than opening braces)"))
            else:
                stack.pop()
            i += 1
            continue
        if tok == "{":
            block = []
            cur().append(Node(None, None, block, line))
            stack.append((block, line))
            i += 1
            continue
        # key op value ?
        if i + 1 < n and tokens[i + 1][0] in ("=", "<", ">", "<=", ">=", "!="):
            op = tokens[i + 1][0]
            if i + 2 < n and tokens[i + 2][0] == "{":
                block = []
                cur().append(Node(tok.strip('"'), op, block, line))
                stack.append((block, tokens[i + 2][1]))
                i += 3
            elif i + 2 < n:
                cur().append(Node(tok.strip('"'), op, tokens[i + 2][0], line))
                i += 3
            else:
                problems.append((line, f"dangling '{tok} {op}' at end of file"))
                i += 2
            continue
        cur().append(Node(None, None, tok, line))
        i += 1

    for _, open_line in stack[1:]:
        problems.append((open_line, "'{' opened here is never closed"))
    return root, problems


def read_text(path):
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace")


def parse_file(path):
    return parse(read_text(path))


def walk(block, parents=()):
    """Yield (node, parents) for every node, depth first."""
    for node in block:
        yield node, parents
        if node.is_block():
            yield from walk(node.value, parents + (node,))


def merged_files(mod_root, vanilla_root, rel_dir, pattern=".txt"):
    """Files in rel_dir as the game sees them: a mod file replaces the vanilla
    file with the same name (HOI4's file-override rule)."""
    files = {}
    for root in (vanilla_root, mod_root):
        d = os.path.join(root, rel_dir)
        if os.path.isdir(d):
            for name in os.listdir(d):
                if name.endswith(pattern):
                    files[name] = os.path.join(d, name)
    return files
