"""Lists every division in a plain-text HOI4 save whose template uses a names group (default GER_SS_01), with its
number and name, template, and location (province, with its state from this mod's history files).

A save stores a division's name as a number in its template's names group (division_name = { name_order = N }).
The name shown in the game is that number's entry in the group (common/units/names_divisions), or the group's
fallback name if the number has no entry. Plain-text saves: settings.txt save_as_binary=no.

    python tools/list_ss_divisions.py "<save games folder>/autosave.hoi4" [GER_SS_01]

Used for docs/CHANGELOG.md section 29.
"""
import os
import re
import sys

save, group = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "GER_SS_01")
mod = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mod")
t = open(save, encoding="utf-8", errors="replace").read()

# province -> state file name: the mod's state history files, then the base game's for states the mod doesn't replace
vanilla = os.environ.get("HOI4_PATH", r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")
p2s = {}
mod_states = set(os.listdir(os.path.join(mod, "history", "states")))
for sd in (os.path.join(mod, "history", "states"), os.path.join(vanilla, "history", "states")):
    for fn in os.listdir(sd):
        if sd.startswith(vanilla) and fn in mod_states:
            continue
        s = open(os.path.join(sd, fn), encoding="utf-8-sig", errors="replace").read()
        m = re.search(r"provinces\s*=\s*\{([^}]*)\}", s)
        if m:
            for p in m.group(1).split():
                p2s.setdefault(p, fn.rsplit(".", 1)[0])

# the group's numbered names (active lines only) and its fallback name
lst = open(os.path.join(mod, "common", "units", "names_divisions", "GER_names_divisions.txt"), encoding="utf-8-sig").read()
blk = lst.split(group + " =", 1)[1].split("\n}", 1)[0]
names = {}
for line in blk.splitlines():
    line = line.split("#", 1)[0]
    m = re.match(r'\s*(\d+)\s*=\s*\{\s*"([^"]+)"', line)
    if m:
        names[int(m.group(1))] = m.group(2).replace("%d", m.group(1))
fallback = re.search(r'fallback_name\s*=\s*"([^"]+)"', blk).group(1)

# template id -> (name, names group)
tpl = {}
for m in re.finditer(r'division_template=\{\s*id=\{ id=(\d+) type=52 \}\s*name="([^"]*)"\s*division_names_group="([^"]*)"', t):
    tpl[m.group(1)] = (m.group(2), m.group(3))

rows = []
for m in re.finditer(r'\n(\t+)division=\{\n', t):
    ind = m.group(1)
    end = t.find("\n" + ind + "}", m.end())
    b = t[m.end():end]
    tid = re.search(r"division_template_id=\{ id=(\d+) type=52 \}", b)
    if not tid or tpl.get(tid.group(1), ("", ""))[1] != group:
        continue
    loc = re.search(r"\blocation=(\d+)", b).group(1)
    dn = re.search(r"division_name=\{(.*?)\n\t+\}", b, re.S)
    d = dict(re.findall(r"(\w+)=(\S+)", dn.group(1))) if dn else {}
    ov = re.search(r'override="([^"]*)"', dn.group(1)) if dn else None
    no = int(d["name_order"]) if "name_order" in d else None
    if ov:
        shown = ov.group(1)
    elif no is not None:
        shown = names.get(no, fallback.replace("%d", str(no)))
    else:
        shown = "?"
    rows.append((no if no is not None else 999, shown, tpl[tid.group(1)][0], loc, p2s.get(loc, "?")))
print(f"{os.path.basename(save)}: date {re.search(r'date=\"([^\"]+)\"', t).group(1)}, {len(rows)} divisions on {group} templates")
for no, shown, tn, loc, st in sorted(rows):
    print(f"  #{no if no != 999 else '-':>3}  {shown:48} {tn:30} province {loc:6} {st}")
