"""Check every add_province_modifier / remove_province_modifier in the mod.

For each one it reports:
  * provinces that are not part of the state the effect runs in
    (e.g. `593 = { add_province_modifier = { province = { id = 4028 } } }`
    when province 4028 belongs to another state)
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
VANILLA = sys.argv[1] if len(sys.argv) > 1 else r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"


def province_to_state():
    prov2state = {}
    for name, path in pdx.merged_files(MOD, VANILLA, os.path.join("history", "states")).items():
        root, _ = pdx.parse_file(path)
        for node, _ in pdx.walk(root):
            if node.key == "state" and node.is_block():
                sid = next((c.value for c in node.value if c.key == "id"), None)
                for c in node.value:
                    if c.key == "provinces" and c.is_block():
                        for p in c.value:
                            if p.key is None and not p.is_block():
                                prov2state[p.value] = sid
    return prov2state


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
    prov2state = province_to_state()
    modifiers = static_modifier_names()
    adds = collections.defaultdict(list)     # (modifier, province) -> [where]
    removes = collections.defaultdict(list)
    wrong_state, unknown_mod, dynamic = [], [], 0

    for path in mod_script_files():
        rel = os.path.relpath(path, MOD).replace("\\", "/")
        root, _ = pdx.parse_file(path)
        for node, parents in pdx.walk(root):
            if node.key not in ("add_province_modifier", "remove_province_modifier") or not node.is_block():
                continue
            state_scope = next((p.key for p in reversed(parents) if p.key and p.key.isdigit()), None)
            mods, provs = [], []
            for c in node.value:
                if c.key == "static_modifiers" and c.is_block():
                    mods += [m.value for m in c.value if m.key is None and not m.is_block()]
                if c.key == "province" and c.is_block():
                    provs += [(p.value, p.line) for p in c.value if p.key == "id"]
            where = f"{rel}:{node.line}"
            for m in mods:
                if m not in modifiers:
                    unknown_mod.append((where, m))
            for prov, line in provs:
                actual = prov2state.get(prov)
                if state_scope is None:
                    dynamic += 1
                elif actual != state_scope:
                    wrong_state.append((f"{rel}:{line}", node.key, prov, state_scope, actual))
                for m in mods:
                    (adds if node.key == "add_province_modifier" else removes)[(m, prov)].append(where)

    print(f"Provinces mapped: {len(prov2state)}   static modifiers known: {len(modifiers)}\n")
    print(f"== Province not in the state the effect runs in ({len(wrong_state)}) ==")
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
