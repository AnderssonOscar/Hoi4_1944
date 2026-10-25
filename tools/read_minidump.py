r"""Read a HOI4 crash minidump (crashes\<folder>\minidump.dmp): the exception, the crashing thread's registers and the
first part of its stack, each value shown as hoi4.exe+offset (code), a text string, or the bytes it points at.
Extra arguments are strings to look for in the captured memory (for example a decision name).

Read-only, standard library only. Usage: python tools/read_minidump.py <minidump.dmp> [string ...]
Offsets of the form hoi4.exe+0x... can be fed to tools/disasm_function.py (same game version only)."""
import re
import struct
import sys

d = open(sys.argv[1], "rb").read()
sig, ver, nstreams, dir_rva = struct.unpack_from("<IIII", d, 0)
assert sig == 0x504D444D, hex(sig)
streams = {}
for i in range(nstreams):
    st, size, rva = struct.unpack_from("<III", d, dir_rva + 12 * i)
    streams.setdefault(st, []).append((size, rva))
print("streams:", sorted(streams))

# memory regions: list of (va, size, file_offset)
regions = []
if 9 in streams:  # Memory64ListStream
    size, rva = streams[9][0]
    n, base_rva = struct.unpack_from("<QQ", d, rva)
    off = base_rva
    for i in range(n):
        va, sz = struct.unpack_from("<QQ", d, rva + 16 + 16 * i)
        regions.append((va, sz, off))
        off += sz
if 5 in streams:  # MemoryListStream
    size, rva = streams[5][0]
    n = struct.unpack_from("<I", d, rva)[0]
    for i in range(n):
        va, sz, mrva = struct.unpack_from("<QII", d, rva + 4 + 16 * i)
        regions.append((va, sz, mrva))
regions.sort()
print("memory regions:", len(regions), "total", sum(r[1] for r in regions) // 1024, "KB")


def read(va, n):
    for rva_, sz, off in regions:
        if rva_ <= va < rva_ + sz:
            k = min(n, rva_ + sz - va)
            return d[off + (va - rva_): off + (va - rva_) + k]
    return None


def file_to_va(fo):
    for va, sz, off in regions:
        if off <= fo < off + sz:
            return va + (fo - off)
    return None


# modules
mods = []
if 4 in streams:
    size, rva = streams[4][0]
    n = struct.unpack_from("<I", d, rva)[0]
    for i in range(n):
        e = rva + 4 + 108 * i
        base, sz = struct.unpack_from("<QI", d, e)
        name_rva = struct.unpack_from("<I", d, e + 20)[0]
        ln = struct.unpack_from("<I", d, name_rva)[0]
        name = d[name_rva + 4: name_rva + 4 + ln].decode("utf-16le")
        mods.append((base, sz, name.split("\\")[-1]))
hoi = [m for m in mods if m[2].lower() == "hoi4.exe"][0]
print("hoi4.exe base", hex(hoi[0]), "size", hex(hoi[1]))


def describe(v):
    for base, sz, name in mods:
        if base <= v < base + sz:
            return "%s+0x%X" % (name, v - base)
    b = read(v, 96)
    if b is None:
        return ""
    s = re.match(rb"[\x20-\x7e]{4,}", b)
    if s:
        return "-> str %r" % s.group(0)[:80].decode()
    # pointer to pointer to string?
    if len(b) >= 8:
        p = struct.unpack_from("<Q", b, 0)[0]
        b2 = read(p, 96)
        if b2:
            s2 = re.match(rb"[\x20-\x7e]{4,}", b2)
            if s2:
                return "-> ptr -> str %r" % s2.group(0)[:80].decode()
    return "-> mem " + b[:24].hex()


# exception
size, rva = streams[6][0]
tid = struct.unpack_from("<I", d, rva)[0]
code, flags, rec, addr = struct.unpack_from("<IIQQ", d, rva + 8)
nparams = struct.unpack_from("<I", d, rva + 8 + 24)[0]
params = struct.unpack_from("<15Q", d, rva + 8 + 32)
ctx_size, ctx_rva = struct.unpack_from("<II", d, rva + 8 + 152)
print("exception code %X at %s (%s), thread %d" % (code, hex(addr), describe(addr), tid))
if code == 0xC0000005:
    print("  access violation: %s address %s" % ({0: "READ", 1: "WRITE", 8: "EXECUTE"}.get(params[0], params[0]), hex(params[1])))
# CONTEXT (AMD64): registers at offset 0x78
names = ["rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
regs = struct.unpack_from("<16Q", d, ctx_rva + 0x78)
rip = struct.unpack_from("<Q", d, ctx_rva + 0xF8)[0]
print("rip", hex(rip), describe(rip))
for n_, v in zip(names, regs):
    print("  %-4s %016X %s" % (n_, v, describe(v)))
rsp = regs[4]
print("\nstack from rsp (first 160 qwords that point at something readable):")
stack = read(rsp, 0x2000) or b""
shown = 0
for i in range(0, len(stack) - 7, 8):
    v = struct.unpack_from("<Q", stack, i)[0]
    desc = describe(v)
    if desc and not desc.startswith("-> mem 0000"):
        print("  rsp+%04X %016X %s" % (i, v, desc))
        shown += 1
        if shown >= 160:
            break

for pat in sys.argv[2:]:
    for m in re.finditer(re.escape(pat.encode()), d):
        print("string %s at file 0x%X = va %s" % (pat, m.start(), hex(file_to_va(m.start()) or 0)))
