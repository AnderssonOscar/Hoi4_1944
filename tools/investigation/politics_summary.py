"""Summarise the PL lines of one or two politics runs (run_<name>/game.log): setup events, later events, daily GER/SOV,
civil wars, subjects of GER. With two runs: also what differs at setup."""
import re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
import os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

def load(name):
    out = []
    for line in open(f"{S}\\run_{name}\\game.log", encoding="utf-8", errors="replace"):
        m = re.search(r"\]: PL (.*)$", line.rstrip("\n"))
        if m:
            out.append(m.group(1).strip())
    return out

def summary(name):
    pl = load(name)
    ev = [l for l in pl if not l.startswith(("day ", "startup"))]
    days = [l for l in pl if l.startswith("day ")]
    conf = collections.Counter()
    other = []
    for l in ev:
        m = re.search(r"on_peaceconference_(started|ended): winner (\S+) .*? loser (\S+) (.*?)( \(|$)", l)
        if m:
            conf[(m.group(1), m.group(3), m.group(4).strip())] += 1
        else:
            other.append(l)
    last = [l for l in days if " GER: " in l and "stab" in l][-1:] + [l for l in days if " SOV: " in l and "stab" in l][-1:]
    cw = collections.Counter(re.sub(r"^day .*? CIVIL WAR in ", "", l) for l in days if "CIVIL WAR" in l)
    subj = collections.Counter(re.sub(r"^day .*? subject of GER: ", "", l) for l in days if "subject of GER" in l)
    gov = sorted(set(re.sub(r" stab .*", "", re.sub(r"^day .*?, 1944 ", "", l)) for l in days if "stab" in l))
    return dict(events=other, conf=conf, last=last, cw=cw, subj=subj, gov=gov, n=len(pl))

names = sys.argv[1:]
res = {n: summary(n) for n in names}
for n in names:
    r = res[n]
    print(f"===== run_{n}: {r['n']} PL lines; last day lines:")
    for l in r["last"]: print("   ", l[:200])
    print("  GER/SOV government as logged (distinct):", r["gov"])
    print("  peace conferences (phase, loser, name -> number of winners):")
    for k, v in sorted(r["conf"].items()): print("    ", k, v)
    print("  civil wars seen (days):", dict(r["cw"]))
    print("  subjects of GER (days):", dict(r["subj"]))
    print("  events (not conferences):")
    for l in r["events"]: print("    ", l[:210])
if len(names) == 2:
    a, b = res[names[0]], res[names[1]]
    strip = lambda l: re.sub(r"^\s*\d+:\d+, \d+ \w+, 1944 ", "", l)
    sa, sb = collections.Counter(map(strip, a["events"])), collections.Counter(map(strip, b["events"]))
    print(f"===== only in run_{names[0]}:")
    for l in sorted((sa - sb).elements()): print("    ", l[:210])
    print(f"===== only in run_{names[1]}:")
    for l in sorted((sb - sa).elements()): print("    ", l[:210])
    print("===== conferences only in", names[0], ":", sorted(set(a["conf"]) - set(b["conf"])))
    print("===== conferences only in", names[1], ":", sorted(set(b["conf"]) - set(a["conf"])))
