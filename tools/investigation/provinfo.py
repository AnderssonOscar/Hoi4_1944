"""Province lookup for the mod's 1944 start: state, map position (unitstacks type 0), 1944 owner/controller.
Usage: python provinfo.py near <province> [radius]   |   python provinfo.py info <province>..."""
import os, re, sys, math
G = r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "mod")
pos = {}
for line in open(os.path.join(G, "map", "unitstacks.txt"), encoding="utf-8"):
    p = line.strip().split(";")
    if len(p) >= 5 and p[1] == "0":
        pos.setdefault(p[0], (float(p[2]), float(p[4])))
mod_states = set(os.listdir(os.path.join(M, "history", "states")))
p2s, sinfo = {}, {}
for sd in (os.path.join(M, "history", "states"), os.path.join(G, "history", "states")):
    for fn in os.listdir(sd):
        if sd.startswith(G) and fn in mod_states:
            continue
        t = open(os.path.join(sd, fn), encoding="utf-8-sig", errors="replace").read()
        t_nc = re.sub(r"#[^\n]*", "", t)
        m = re.search(r"provinces\s*=\s*\{([^}]*)\}", t_nc)
        if not m:
            continue
        name = fn.rsplit(".", 1)[0]
        for p in m.group(1).split():
            p2s.setdefault(p, name)
        owner = re.search(r"\n\s*owner\s*=\s*(\w+)", t_nc)
        # 1944 values: dated blocks up to 1944.1.1 override
        own, ctl = (owner.group(1) if owner else "?"), None
        for dm in re.finditer(r"(\d{4})\.(\d+)\.(\d+)\s*=\s*\{", t_nc):
            y, mo, d = map(int, dm.groups())
            if (y, mo, d) > (1944, 1, 1):
                continue
            # crude: find owner/controller within the next 3000 chars of this block
            seg = t_nc[dm.end(): dm.end() + 3000]
            o = re.search(r"\n\s*owner\s*=\s*(\w+)", seg); c = re.search(r"\n\s*controller\s*=\s*(\w+)", seg)
            if o: own = o.group(1)
            if c: ctl = c.group(1)
        spc = re.findall(r"set_province_controller\s*=\s*(\d+)", t_nc)
        sinfo[name] = (own, ctl or own, spc)
vps = {}
for root in (os.path.join(G, "localisation", "english"), os.path.join(M, "localisation")):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith(".yml"):
                for line in open(os.path.join(dp, f), encoding="utf-8-sig", errors="replace"):
                    m = re.match(r'\s*VICTORY_POINTS_(\d+):\d*\s*"([^"]+)"', line)
                    if m:
                        vps.setdefault(m.group(1), m.group(2))

def info(p):
    st = p2s.get(p, "?")
    own, ctl, spc = sinfo.get(st, ("?", "?", []))
    note = " (set_province_controller in the state file)" if p in spc else ""
    return f"{p:6} {vps.get(p, ''):18} state {st:28} owner {own} controller {ctl}{note} pos {pos.get(p)}"

if sys.argv[1] == "info":
    for p in sys.argv[2:]:
        print(info(p))
elif sys.argv[1] == "near":
    c = pos[sys.argv[2]]; r = float(sys.argv[3]) if len(sys.argv) > 3 else 40
    near = sorted((math.dist(c, xy), p) for p, xy in pos.items() if math.dist(c, xy) <= r)
    for d, p in near:
        print(f"{d:6.1f}  " + info(p))
elif sys.argv[1] == "vp":
    for p, n in vps.items():
        if re.search(sys.argv[2], n, re.I):
            print(info(p))
