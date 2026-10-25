"""For the crash of 11 October 2026 (docs/game-logs/31-player-crash-2026-10-11.txt): read the list of running decisions
that the crashing loop was going through (slots at rdi+0x70, count at rdi+0x7c; rdi and rbx are the register values
printed by tools/read_minidump.py for that crash) out of the minidump. Usage: python <this file> <minidump.dmp>"""
import re
import struct
import sys

sys.argv = [sys.argv[0], sys.argv[1]]
src = open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "read_minidump.py"), encoding="utf-8").read()
# reuse the reader's parsing (everything up to the exception printout)
cut = src.index("# exception")
ns = {}
import io, contextlib  # noqa: E401
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], "read_minidump", "exec"), ns)
read = ns["read"]


def q(va):
    b = read(va, 8)
    return struct.unpack("<Q", b)[0] if b and len(b) == 8 else None


def d32(va):
    b = read(va, 4)
    return struct.unpack("<I", b)[0] if b and len(b) == 4 else None


def strs(va, n=0x400):
    b = read(va, n)
    if not b:
        return "(not captured)"
    return " | ".join(s.decode() for s in re.findall(rb"[\x20-\x7e]{5,}", b))[:300]


rdi = 0x0000026353854060
arr, cnt, cap = q(rdi + 0x70), d32(rdi + 0x7C), d32(rdi + 0x78)
print("list object rdi=%X: array %s, count %s, field+0x78 %s" % (rdi, hex(arr) if arr else arr, cnt, cap))
print("other list at rdi+0x40: %s count %s" % (hex(q(rdi + 0x40) or 0), d32(rdi + 0x4C)))
for i in range(0, 6):
    e = q(arr + 8 * i)
    print(" slot %d @%X -> %s" % (i, arr + 8 * i, hex(e) if e is not None else "(not captured)"))
    if e:
        t = d32(e + 0x10)
        dec = q(e + 8)
        print("    timer field +0x10 = %s, decision object +8 = %s" % (t, hex(dec) if dec else dec))
        if dec:
            for off in (0, 8, 0x10, 0x18, 0x20, 0x28, 0x30):
                p = q(dec + off)
                if p:
                    s = strs(p, 0x60)
                    if s and s != "(not captured)":
                        print("      dec+%02X -> %s" % (off, s))
rbx = 0x000002631E3D20E0
print("rbx (the expired decision) = %X:" % rbx)
for off in range(0, 0x60, 8):
    p = q(rbx + off)
    print("   +%02X = %s %s" % (off, hex(p) if p is not None else None, strs(p, 0x80) if p and p > 0x10000 else ""))
