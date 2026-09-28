"""Check every add_province_modifier / remove_province_modifier in the mod,
and every province-level building effect (add_building_construction,
remove_building, damage_building, set_building_level with a province).

For each one it reports:
  * provinces that are not part of the state the effect runs in
    (e.g. `593 = { add_province_modifier = { province = { id = 4028 } } }`
    when province 4028 belongs to another state, or
    `763 = { remove_building = { type = bunker province = 13370 } }`)
  * static modifiers that are not defined anywhere (mod or base game)
  * removals of a modifier from a province that no script in the mod ever adds
    it to

Usage:  python tools/check_province_modifiers.py [path-to-HOI4-install]
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pdx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "..", "mod")
VANILLA = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HOI4_PATH", r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")
BUILDING_EFFECTS = ("add_building_construction", "remove_building", "damage_building", "set_building_level")


def province_to_state(with_files=False):
    """Province -> state id, from history/states as the game loads them.
    With with_files=True also returns state id -> [files defining it]."""
    prov2state = {}
    state_files = collections.defaultdict(list)
    for name, path in pdx.merged_files(MOD, VANILLA, os.path.join("history", "states")).items():
        root, _ = pdx.parse_file(path)
        for node, _ in pdx.walk(root):
            if node.key and node.key.lower() == "state" and node.is_block():
                sid = next((c.value for c in node.value if c.key == "id"), None)
                state_files[sid].append(name)
                for c in node.value:
                    if c.key == "provinces" and c.is_block():
                        for p in c.value:
                            if p.key is None and not p.is_block():
                                prov2state[p.value] = sid
    return (prov2state, state_files) if with_files else prov2state


def static_modifier_names():
    names = set()
    for _, path in pdx.merged_files(MOD, VANILLA, os.path.join("common", "modifiers")).items():
        root, _ = pdx.parse_file(path)
        names.update(n.key for n in root if n.key)
    return names


def mod_script_files():
    for sub in ("common", "events", "history"):
        for dirpath, _, files in os.walk(os.path.join(MOD, sub)):
            for f in files:
                if f.endswith(".txt"):
                    yield os.path.join(dirpath, f)


def main():
    prov2state, state_files = province_to_state(with_files=True)
    modifiers = static_modifier_names()
    adds = collections.defaultdict(list)     # (modifier, province) -> [where]
    removes = collections.defaultdict(list)
    wrong_state, unknown_mod, dynamic, checked = [], [], 0, 0

    for path in mod_script_files():
        rel = os.path.relpath(path, MOD).replace("\\", "/")
        root, _ = pdx.parse_file(path)
        for node, parents in pdx.walk(root):
            if node.key not in ("add_province_modifier", "remove_province_modifier") + BUILDING_EFFECTS or not node.is_block():
                continue
            state_scope = next((p.key for p in reversed(parents) if p.key and p.key.isdigit()), None)
            mods, provs = [], []
            for c in node.value:
                if c.key == "static_modifiers" and c.is_block():
                    mods += [m.value for m in c.value if m.key is None and not m.is_block()]
                if c.key == "province" and c.is_block():
                    provs += [(p.value, p.line) for p in c.value if p.key == "id"]
                elif c.key == "province" and c.value.isdigit():
                    provs.append((c.value, c.line))
            where = f"{rel}:{node.line}"
            for m in mods:
                if m not in modifiers:
                    unknown_mod.append((where, m))
            for prov, line in provs:
                actual = prov2state.get(prov)
                if state_scope is None:
                    dynamic += 1
                else:
                    checked += 1
                    if actual != state_scope:
                        wrong_state.append((f"{rel}:{line}", node.key, prov, state_scope, actual))
                for m in mods:
                    (adds if node.key == "add_province_modifier" else removes)[(m, prov)].append(where)

    print(f"Provinces mapped: {len(prov2state)}   static modifiers known: {len(modifiers)}"
          f"   province references checked: {checked}\n")
    dup_states = {sid: files for sid, files in state_files.items() if len(files) > 1}
    print(f"== State ids defined by more than one file ({len(dup_states)}) ==")
    print("   (a mod file only replaces a vanilla file with the exact same name; otherwise both load)")
    for sid, files in sorted(dup_states.items(), key=lambda kv: int(kv[0]) if kv[0] and kv[0].isdigit() else 0):
        print(f"  state {sid}: {', '.join(files)}")
    print(f"\n== Province not in the state the effect runs in ({len(wrong_state)}) ==")
    for where, kind, prov, scope, actual in sorted(wrong_state):
        print(f"  {where}  {kind}: province {prov} used in state {scope}, but it belongs to state {actual}")
    print(f"\n== Unknown static modifiers ({len(unknown_mod)}) ==")
    for where, m in sorted(unknown_mod):
        print(f"  {where}  {m}")
    never_added = [(k, v) for k, v in removes.items() if k not in adds]
    print(f"\n== Removed but never added anywhere in the mod ({len(never_added)}) ==")
    for (m, prov), wheres in sorted(never_added):
        print(f"  {m} on province {prov}: removed at {', '.join(wheres)}")
    print(f"\n({dynamic} province references were in dynamic scopes and not checked)")


if __name__ == "__main__":
    main()
