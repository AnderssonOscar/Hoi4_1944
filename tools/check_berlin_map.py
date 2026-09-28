"""Re-derive the Festung Berlin geography from the game's own map.

From map/provinces.bmp and map/definition.csv (base game; the mod has its own
copies of neither) plus the state files the game loads, this prints:
  * the provinces bordering Berlin (6521)         -> the "ring" in the chain
  * Seelow's (9496) neighbours outside Brandenburg -> the Seelow trigger
  * the states bordering Brandenburg (state 64)    -> the first event's trigger
and checks them against common/on_actions/GER_festung_berlin_on_actions.txt
and common/scripted_effects/GER_festung_berlin_effects.txt.

Needs Pillow and numpy (pip install pillow numpy). Read-only.
Usage:  python tools/check_berlin_map.py [path-to-HOI4-install]
"""
import csv
import os
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import check_province_modifiers as cpm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "..", "mod")
VANILLA = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HOI4_PATH", r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")


def adjacency():
    """Province id -> set of neighbouring province ids, from touching pixels."""
    col2id = {}
    with open(os.path.join(VANILLA, "map", "definition.csv"), encoding="utf-8", errors="replace") as f:
        for row in csv.reader(f, delimiter=";"):
            if row and row[0].isdigit():
                col2id[(int(row[1]) << 16) | (int(row[2]) << 8) | int(row[3])] = int(row[0])
    img = np.asarray(Image.open(os.path.join(VANILLA, "map", "provinces.bmp")).convert("RGB")).astype(np.int32)
    key = (img[:, :, 0] << 16) | (img[:, :, 1] << 8) | img[:, :, 2]
    colours, inverse = np.unique(key, return_inverse=True)
    ids = np.array([col2id.get(int(c), -1) for c in colours])[inverse].reshape(key.shape)
    adj = {}
    for a, b in ((ids[:, :-1], ids[:, 1:]), (ids[:-1, :], ids[1:, :])):
        differ = a != b
        for x, y in set(zip(a[differ].tolist(), b[differ].tolist())):
            adj.setdefault(x, set()).add(y)
            adj.setdefault(y, set()).add(x)
    return adj


def main():
    p2s = cpm.province_to_state()
    adj = adjacency()
    ring = sorted(adj[6521])
    seelow_front = sorted(p for p in adj[9496] if p2s.get(str(p)) != "64")
    brandenburg = [int(p) for p, s in p2s.items() if s == "64"]
    states = sorted({int(p2s[str(q)]) for p in brandenburg for q in adj.get(p, ()) if p2s.get(str(q)) not in (None, "64")})
    print("Provinces bordering Berlin (6521):", ring, "- states", sorted({p2s.get(str(p)) for p in ring}))
    print("Seelow (9496) neighbours outside Brandenburg:", seelow_front)
    print("States bordering Brandenburg (64):", states)

    oa = open(os.path.join(MOD, "common", "on_actions", "GER_festung_berlin_on_actions.txt"), encoding="ascii").read()
    eff = open(os.path.join(MOD, "common", "scripted_effects", "GER_festung_berlin_effects.txt"), encoding="ascii").read()
    used_states = sorted(int(s) for s in re.search(r"OR = \{ ((?:state = \d+ ?)+)\}", oa).group(1).split() if s.isdigit())
    step1 = eff.split("GER_festung_berlin_forts_step_1 = {", 1)[1].split("\n}", 1)[0]
    used_ring = sorted({int(p) for p in re.findall(r"controls_province = (\d+)", step1)} - {6521})
    seelow_block = oa.split("# 2.", 1)[1].split("# 3.", 1)[0]
    used_front = sorted(int(p) for p in re.findall(r"NOT = \{ controls_province = (\d+) \}", seelow_block))
    fails = 0
    for label, map_value, used in (("ring", ring, used_ring), ("Seelow front", seelow_front, used_front),
                                   ("bordering states", states, used_states)):
        ok = map_value == used
        fails += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}: map says {map_value}, the chain uses {used}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
