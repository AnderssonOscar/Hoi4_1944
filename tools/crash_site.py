"""Show which part of HOI4 a crash happened in.

HOI4's crash reports (Documents\\Paradox Interactive\\Hearts of Iron IV\\crashes\\<folder>\\exception.txt)
list the stack as offsets from a few exported names, because hoi4.exe ships without debug symbols.
This script turns each frame into the function it lies in (from the exe's own function table) and
prints the text strings that function uses: the game's log and assert messages carry the name of the
source file (for example ...\\geography\\country.cpp) and the localisation keys it shows, which says
what the game was doing when it crashed.

Read-only. Needs Python 3 with pefile and capstone (pip install pefile capstone).
Usage: python tools/crash_site.py "<crash folder>" [path to hoi4.exe]
"""
import bisect
import re
import sys

import capstone
import pefile

folder = sys.argv[1]
exe = sys.argv[2] if len(sys.argv) > 2 else r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\hoi4.exe"
report = open(folder + r"\exception.txt", encoding="utf-8", errors="replace").read()

pe = pefile.PE(exe, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"],
                                       pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])
exports = {}
for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
    if e.name:
        name = e.name.decode()
        m = re.match(r"\?(\w+)@@", name)  # C++ decorated names: ?PHYSFS_swapULE64@@...
        exports[m.group(1) if m else name] = e.address
image = pe.get_memory_mapped_image()
base = pe.OPTIONAL_HEADER.ImageBase
functions = sorted((f.struct.BeginAddress, f.struct.EndAddress) for f in pe.DIRECTORY_ENTRY_EXCEPTION)
starts = [f[0] for f in functions]


def function_of(rva):
    i = bisect.bisect_right(starts, rva) - 1
    return functions[i] if i >= 0 and functions[i][0] <= rva < functions[i][1] else None


def c_string(rva, limit=160):
    s = image[rva:rva + limit]
    end = s.find(b"\0")
    if end < 4:
        return None
    s = s[:end]
    return s.decode() if all(32 <= c < 127 or c in (9, 10) for c in s) else None


disasm = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
print(re.search(r"^Unhandled Exception.*$", report, re.M).group(0))
for num, sym, off in re.findall(r"^\s*(\d+)\s+hoi4\.exe\s+(\w+) \(\+ (\d+)\)", report, re.M):
    if sym not in exports:
        continue
    rva = exports[sym] + int(off)
    f = function_of(rva)
    print(f"\nframe {num}: offset 0x{rva:X}" + (f" in function 0x{f[0]:X}-0x{f[1]:X}" if f else ""))
    if not f:
        continue
    seen = []
    for ins in disasm.disasm(image[f[0]:f[1]], base + f[0]):
        m = re.search(r"\[rip \+ 0x([0-9a-f]+)\]", ins.op_str)
        if m and ins.mnemonic in ("lea", "mov"):
            s = c_string(ins.address + ins.size + int(m.group(1), 16) - base)
            if s and s not in seen:
                seen.append(s)
    for s in seen[:20]:
        print("   ", repr(s)[:150])
