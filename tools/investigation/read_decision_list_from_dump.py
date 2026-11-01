"""For the crash of 11 October 2026 (docs/game-logs/31-player-crash-2026-10-11.txt): read the list of running decisions
that the crashing loop was going through (slots at rdi+0x70, count at rdi+0x7c; rdi and rbx are the register values
printed by tools/read_minidump.py for that crash) out of the minidump, and look for the decisions' names: any pointer in
a decision object that leads to a text string. Usage: python <this file> <minidump.dmp>"""
import contextlib
import io
import os
import re
import struct
import sys

sys.argv = [sys.argv[0], sys.argv[1]]
src = open(os.path.join(os.path.dirname(__file__), "..", "read_minidump.py"), encoding="utf-8").read()
cut = src.index("# exception")  # reuse the reader's parsing, everything up to the exception printout
ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "read_minidump", "exec"), ns)
read = ns["read"]
regions = ns["regions"]


def q(va):
    b = read(va, 8)
    return struct.unpack("<Q", b)[0] if b and len(b) == 8 else None


def d32(va):
    b = read(va, 4)
    return struct.unpack("<I", b)[0] if b and len(b) == 4 else None


def text_at(va):
    b = read(va, 96)
    if not b:
        return None
    m = re.match(rb"[\x20-\x7e]{4,}", b)
    return m.group(0).decode() if m else None


def names_in(obj, size=0xA00):
    """Text reached from the object's fields: directly, or as a string object (inline at +0 or through a pointer)."""
    out = []
    b = read(obj, size)
    if not b:
        return ["(object not captured)"]
    for off in range(0, len(b) - 7, 8):
        p = struct.unpack_from("<Q", b, off)[0]
        if p < 0x10000 or p > 0x7FFFFFFFFFFF:
            continue
        t = text_at(p)
        if t:
            out.append("+%03X -> %r" % (off, t[:70]))
            continue
        p2 = q(p)
        if p2 and 0x10000 < p2 < 0x7FFFFFFFFFFF:
            t = text_at(p2)
            if t:
                out.append("+%03X -> -> %r" % (off, t[:70]))
    # MSVC-style short strings inline in the object
    for m in re.finditer(rb"[A-Za-z][A-Za-z0-9_]{5,}", b):
        out.append("+%03X inline %r" % (m.start(), m.group(0).decode()[:70]))
    return out or ["(no text found in %d captured bytes)" % len(b)]


rdi, rbx = 0x0000026353854060, 0x000002631E3D20E0
arr, cnt = q(rdi + 0x70), d32(rdi + 0x7C)
print("list object rdi=%X: slots at %s, count %s, field+0x78 %s" % (rdi, hex(arr) if arr else arr, cnt, d32(rdi + 0x78)))
print("second list at rdi+0x40: %s, count %s" % (hex(q(rdi + 0x40) or 0), d32(rdi + 0x4C)))
for i in range(3):
    e = q(arr + 8 * i)
    print(" slot %d @%X -> %s" % (i, arr + 8 * i, hex(e) if e is not None else "(not captured)"))
    if e:
        dec, t = q(e + 8), d32(e + 0x10)
        print("    timer +0x10 = %s, decision object +8 = %s" % (t, hex(dec) if dec else dec))
second = q(rdi + 0x40)
print("\nsecond list, entries:")
for i in range(max(d32(rdi + 0x4C) or 0, 0) + 1):
    p = q(second + 8 * i)
    print("  [%d] %s" % (i, hex(p) if p else p))
objs = {"rbx, the expired decision": rbx}
for i in range(3):
    e = q(arr + 8 * i)
    dec = q(e + 8) if e else None
    if dec and dec != rbx:
        objs["slot %d's decision" % i] = dec
p = q(second)
if p and p not in objs.values():
    objs["second list's entry"] = p
for label, o in objs.items():
    print("\n== %s %X" % (label, o))
    for line in names_in(o)[:40]:
        print("   ", line)
print("\nall decision names in the captured memory near the expired decision's strings:")
for va, sz, off in regions:
    if va <= 0x2631e34cd50 < va + sz:
        print("  region %X size %X" % (va, sz))
