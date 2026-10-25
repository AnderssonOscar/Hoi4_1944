"""Disassemble the hoi4.exe function that contains a given offset (hex, as printed by tools/crash_site.py or
tools/read_minidump.py), with the text strings it references and the functions it calls. The marked line is the offset itself.

Read-only. Needs pefile and capstone (pip install pefile capstone). Usage: python tools/disasm_function.py 7375DA [more offsets]"""
import bisect
import re
import sys

import capstone
import pefile

exe = r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\hoi4.exe"
pe = pefile.PE(exe, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])
image = pe.get_memory_mapped_image()
base = pe.OPTIONAL_HEADER.ImageBase
functions = sorted((f.struct.BeginAddress, f.struct.EndAddress) for f in pe.DIRECTORY_ENTRY_EXCEPTION)
starts = [f[0] for f in functions]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False


def fn(rva):
    i = bisect.bisect_right(starts, rva) - 1
    return functions[i]


def string_at(rva):
    b = image[rva:rva + 120]
    m = re.match(rb"[\x20-\x7e]{3,}", b)
    return m.group(0).decode() if m else None


for arg in sys.argv[1:]:
    mark = int(arg, 16)
    s, e = fn(mark)
    # chained unwind info can split a function; widen a little backwards if mark is near start
    print("==== function 0x%X-0x%X (mark 0x%X)" % (s, e, mark))
    code = image[s:e]
    for ins in md.disasm(code, base + s):
        rva = ins.address - base
        extra = ""
        m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", ins.op_str)
        if m:
            tgt = rva + ins.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
            st = string_at(tgt)
            extra = "   ; rva 0x%X %s" % (tgt, repr(st) if st else "")
        if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
            tgt = int(ins.op_str, 16) - base
            extra = "   ; call 0x%X" % tgt
        flag = "  <== CRASH/RET" if rva == mark else ""
        print("%08X  %-7s %s%s%s" % (rva, ins.mnemonic, ins.op_str, extra, flag))
