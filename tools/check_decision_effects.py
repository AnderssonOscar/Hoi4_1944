"""List the timed decisions and missions whose remove_effect, timeout_effect or cancel_effect does something that can end
other running decisions of a country while the game is going through its list of running decisions (docs/CHANGELOG.md
section 31). Reads the game's decision files with the mod's files overriding them, the way the game loads them.

Read-only. Usage: python tools/check_decision_effects.py [--base]   (--base: the base game alone, for comparison)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx  # noqa: E402

GAME = r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\common\decisions"
MOD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mod", "common", "decisions")
HEAVY = {"white_peace", "start_peace_conference", "transfer_state", "set_state_owner", "set_autonomy", "puppet", "end_puppet",
         "release", "release_puppet", "annex_country", "remove_from_faction", "add_to_faction", "dismantle_faction", "leave_faction",
         "add_to_war", "declare_war_on", "start_civil_war", "set_politics", "remove_decision", "remove_targeted_decision",
         "remove_mission", "activate_decision", "activate_targeted_decision", "activate_mission", "activate_mission_tooltip"}
EFFECTS = ("remove_effect", "timeout_effect", "cancel_effect")

base_only = "--base" in sys.argv
files = {f: os.path.join(GAME, f) for f in os.listdir(GAME) if f.endswith(".txt")}
if not base_only:
    files.update({f: os.path.join(MOD, f) for f in os.listdir(MOD) if f.endswith(".txt")})

rows, timed = [], 0
for name, path in sorted(files.items()):
    src = "base" if path.startswith(GAME) else "mod"
    for cat in pdx.parse_file(path)[0]:
        if not cat.key or not isinstance(cat.value, list):
            continue
        for dec in cat.value:
            if not dec.key or not isinstance(dec.value, list):
                continue
            keys = {c.key for c in dec.value}
            if not keys & {"days_remove", "days_mission_timeout"}:
                continue
            timed += 1
            for eff in EFFECTS:
                node = next((c for c in dec.value if c.key == eff), None)
                if node is None or not isinstance(node.value, list):
                    continue
                found = sorted({n.key for n, _ in pdx.walk(node.value)} & HEAVY)
                if found:
                    rows.append((src, name, dec.key, eff, found))
print(f"{timed} timed decisions and missions read; {len(rows)} effect blocks with something heavy")
for src, name, dec, eff, found in rows:
    print(f"{src:4} {name:34} {dec:48} {eff:14} {', '.join(found)}")
