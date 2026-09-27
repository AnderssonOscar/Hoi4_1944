"""Find references to things that do not exist in the game as it loads with the mod.

Covers what the game only notices *during play* (so error.log at startup
misses it): events fired by effects, ideas (national spirits), characters and
cosmetic tags. Decisions, focuses and technologies are already checked by the
game itself at startup (see error.log).

The "loaded set" is what the game loads: a mod file replaces the base-game
file with the same relative path. Every problem is also looked up in the base
game alone, so the report separates problems caused by the mod from the base
game's own.

Usage:  python tools/check_references.py [path-to-HOI4-install]
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pdx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(HERE, "..", "mod"))
VANILLA = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HOI4_PATH", r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")

EVENT_KEYS = {"country_event", "news_event", "state_event", "unit_leader_event", "operative_leader_event"}
SCOPES = {"THIS", "ROOT", "PREV", "FROM", "PREV.PREV", "FROM.FROM", "yes", "no"}


def scripts(root):
    out = {}
    for sub in ("common", "events", "history"):
        for dp, _, fs in os.walk(os.path.join(root, sub)):
            for f in fs:
                if f.endswith(".txt"):
                    full = os.path.join(dp, f)
                    out[os.path.relpath(full, root).replace("\\", "/").lower()] = full
    return out


def usable(v):
    return v and v not in SCOPES and not any(c in v for c in ":@[") and not v.startswith("$")


def scan(rel, root):
    """Definitions and references found in one parsed file."""
    defs = collections.defaultdict(set)
    refs = []          # (kind, id, line)
    top_events = rel.startswith("events/")
    if top_events:
        for n in root:
            if n.key in EVENT_KEYS and n.is_block():
                i = next((c.value for c in n.value if c.key == "id"), None)
                if i:
                    defs["event"].add(i)
    if rel.startswith("common/ideas/"):
        for top in root:
            if top.key == "ideas" and top.is_block():
                for cat in top.value:
                    if cat.is_block():
                        defs["idea"].update(c.key for c in cat.value if c.key and c.is_block())
    if rel.startswith("common/characters/"):
        for top in root:
            if top.key == "characters" and top.is_block():
                defs["character"].update(c.key for c in top.value if c.key and c.is_block())
    if rel == "common/countries/cosmetic.txt":
        defs["cosmetic tag"].update(n.key for n in root if n.key)

    for n, parents in pdx.walk(root):
        k = n.key
        if k in EVENT_KEYS:
            if top_events and not parents:
                continue                                   # a definition
            v = next((c.value for c in n.value if c.key == "id"), None) if n.is_block() else n.value
            if usable(v):
                refs.append(("event", v, n.line))
        elif k in ("add_ideas", "remove_ideas"):
            vals = [c.value for c in n.value if c.key is None and not c.is_block()] if n.is_block() else [n.value]
            refs += [("idea", v, n.line) for v in vals if usable(v)]
        elif k == "has_idea" and not n.is_block():
            if usable(n.value):
                refs.append(("idea", n.value, n.line))
        elif k in ("add_timed_idea", "modify_timed_idea") and n.is_block():
            v = next((c.value for c in n.value if c.key == "idea"), None)
            if usable(v):
                refs.append(("idea", v, n.line))
        elif k == "swap_ideas" and n.is_block():
            refs += [("idea", c.value, c.line) for c in n.value if c.key in ("add_idea", "remove_idea") and usable(c.value)]
        elif k in ("recruit_character", "retire_character", "promote_character", "has_character") and not n.is_block():
            if usable(n.value):
                refs.append(("character", n.value, n.line))
        elif k in ("set_cosmetic_tag", "has_cosmetic_tag") and not n.is_block():
            if usable(n.value):
                refs.append(("cosmetic tag", n.value, n.line))
    return defs, refs


def build(files, cache):
    defs = collections.defaultdict(set)
    refs = []
    for rel, full in files.items():
        if full not in cache:
            cache[full] = scan(rel, pdx.parse_file(full)[0])
        d, r = cache[full]
        for kind, s in d.items():
            defs[kind] |= s
        refs += [(kind, i, rel, line, full) for kind, i, line in r]
    return defs, refs


def main():
    van_files, mod_files = scripts(VANILLA), scripts(MOD)
    loaded = dict(van_files)
    loaded.update(mod_files)
    cache = {}
    ldefs, lrefs = build(loaded, cache)
    vdefs, vrefs = build(van_files, cache)
    vmissing = {(k, i) for k, i, *_ in vrefs if i not in vdefs[k]}

    missing = [(k, i, rel, line, full) for k, i, rel, line, full in lrefs if i not in ldefs[k]]
    by_mod = [m for m in missing if (m[0], m[1]) not in vmissing]
    print(f"Files loaded: {len(loaded)} ({len(mod_files)} from the mod)")
    print("Defined in the loaded game: " + ", ".join(f"{len(ldefs[k])} {k}s" for k in ("event", "idea", "character", "cosmetic tag")))
    print(f"References checked: {len(lrefs)}")
    print(f"\nBase game alone has {len(vmissing)} references to things it doesn't define (its own issues, "
          "often DLC or unused content) - not counted below.")
    print(f"\n== Missing things caused by the mod ({len(by_mod)}) ==")
    for k, i, rel, line, full in sorted(by_mod, key=lambda m: (m[0], m[2], m[3])):
        where = "mod file" if full.startswith(MOD) else "base-game file"
        also = " (exists in base game: the mod's copy dropped it)" if i in vdefs[k] else ""
        print(f"  {k:13s} {i:50s} {rel}:{line} [{where}]{also}")


if __name__ == "__main__":
    main()
