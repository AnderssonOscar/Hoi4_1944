"""Re-verify every claim about the fixes and the 1.19.3 update. Prints PASS/FAIL.

Run from the project folder:  python tools/verify_update.py
Needs: git, the HOI4 1.19.3 install, and the Steam Workshop copy of the mod.
Also writes docs/checksums/mod-files.sha256 (SHA-256 of every mod file).
"""
import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pdx  # noqa: E402
import rebase_helpers as rh  # noqa: E402

V = rh.VANILLA
W = os.environ.get("WORKSHOP_PATH", r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3070639276")
BASE = "253cea1"
FAILS = []


def git(*args, inp=None):
    return subprocess.run(["git"] + list(args), capture_output=True, input=inp).stdout


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        FAILS.append(name)


def canon(n):
    return (f"{n.key}=" if n.key else "") + ("{" + " ".join(canon(c) for c in n.value) + "}" if n.is_block() else n.value)


def parse_bytes(b):
    return pdx.parse(b.decode("utf-8-sig", errors="replace"))[0]


def at_base(path):
    return git("show", f"{BASE}:{path}")


def vanilla(rel):
    return open(os.path.join(V, rel), "rb").read()


def current(path):
    return open(path, "rb").read()


print("== 1. Integrity ==")
check("mod folder fully committed (no uncommitted changes in mod/)", git("status", "--porcelain", "--", "mod").strip() == b"")
tree = [l.split(b"\t", 1) for l in git("ls-tree", "-r", "HEAD", "--", "mod").splitlines()]
paths = [p.decode() for _, p in tree]
blobs = [m.split()[2] for m, _ in tree]
disk = git("hash-object", "--no-filters", "--stdin-paths", inp="\n".join(paths).encode()).split()
check(f"all {len(paths)} mod files on disk are byte-identical to the committed version", disk == blobs)
base_tree = [l.split(b"\t", 1) for l in git("ls-tree", "-r", BASE, "--", "mod").splitlines()]
rel = [p.decode()[4:] for _, p in base_tree]
ws = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], cwd=W, capture_output=True,
                    input="\n".join(rel).encode()).stdout.split()
check(f"Steam Workshop copy untouched: all {len(rel)} files identical to the baseline", ws == [m.split()[2] for m, _ in base_tree])

print("\n== 2. Exactly the intended files changed ==")
SF = ["ENG - Britain", "FIN - Finland", "GER - Germany", "HUN - Hungary", "ITA - Italy", "JAP - Japan",
      "RKN - Reichskommisariat Niederlande", "ROM - Romania", "SOV - Soviet union", "TUR - Turkey", "USA - USA"]
expected = {("M", "mod/descriptor.mod"), ("M", "mod/common/scripted_effects/japan_scripted_events_mod.txt"),
            ("D", "mod/history/states/870-North West Australia.txt"), ("D", "mod/history/states/871-South West Australia.txt"),
            ("D", "mod/history/states/873-South West Queensland.txt"), ("M", "mod/common/national_focus/netherlands.txt"),
            ("M", "mod/common/countries/cosmetic.txt"), ("M", "mod/history/countries/ARG - Argentina.txt"),
            ("M", "mod/history/countries/AST - Australia.txt"), ("M", "mod/history/countries/SIA - Siam.txt"),
            ("M", "mod/common/decisions/JAP.txt"), ("M", "mod/common/decisions/SOV.txt"), ("M", "mod/events/BFTB_NewsEvents.txt")}
expected |= {("M", f"mod/history/countries/{c}.txt") for c in SF}
expected |= {("A", "mod/events/slovak_uprising.txt"), ("A", "mod/common/on_actions/slovak_uprising_on_actions.txt"),
             ("A", "mod/localisation/english/slovak_uprising_l_english.yml")}  # flavor event (CHANGELOG section 4)
expected |= {("A", "mod/common/decisions/GER_last_stand_decisions.txt"),
             ("A", "mod/common/dynamic_modifiers/GER_last_stand_dynamic_modifiers.txt"),
             ("A", "mod/common/ideas/GER_last_stand_ideas.txt"),
             ("A", "mod/common/on_actions/GER_last_stand_on_actions.txt"),
             ("A", "mod/events/GER_last_stand_events.txt"),
             ("A", "mod/localisation/english/GER_last_stand_l_english.yml")}  # Nero Decree + Werwolf (CHANGELOG section 5)
expected |= {("M", "mod/common/national_focus/germany.txt"), ("M", "mod/localisation/english/custom_mod_l_english.yml"),
             ("A", "mod/common/scripted_effects/GER_volkssturm_effects.txt"),
             ("A", "mod/common/decisions/GER_volkssturm_decisions.txt"),
             ("A", "mod/localisation/english/GER_volkssturm_l_english.yml")}  # Volkssturm (CHANGELOG section 6)
expected |= {("M", "mod/events/mod_news.txt")}  # Konigsberg in Ruins fix (CHANGELOG section 7)
expected |= {("M", "mod/common/decisions/GER_mod.txt"), ("M", "mod/events/mod_events.txt")}  # Stettin + Antwerp fixes (section 8)
expected |= {("A", "mod/common/scripted_effects/GER_festung_berlin_effects.txt"),
             ("A", "mod/common/modifiers/GER_festung_berlin_modifiers.txt"),
             ("A", "mod/common/dynamic_modifiers/GER_festung_berlin_dynamic_modifiers.txt"),
             ("A", "mod/common/on_actions/GER_festung_berlin_on_actions.txt"),
             ("A", "mod/events/GER_festung_berlin_events.txt"),
             ("A", "mod/localisation/english/GER_festung_berlin_l_english.yml")}  # Festung Berlin (section 9)
expected |= {("M", "mod/history/units/GER_1944.txt"), ("M", "mod/history/units/GER_1944_nsb.txt"),
             ("M", "mod/common/units/names_divisions/GER_names_divisions.txt"),
             ("M", "mod/events/ss_recruitment_event.txt")}  # Wiking + Nordland (section 10)
changed ={tuple(l.decode().split("\t", 1)) for l in git("diff", "--name-status", BASE, "HEAD", "--", "mod").splitlines()}
check(f"changed files = the {len(expected)} intended ones", changed == expected,
      f"unexpected: {sorted(changed - expected)}; missing: {sorted(expected - changed)}")

print("\n== 3. Nothing of the author's was removed by accident ==")
SF_LINE = re.compile(r"^\s*(special_forces_\w+|marines_\w+|mountaineers_combat_\d|paras_\w+|rangers|ski_troops)\s*=\s*1\s*$")
allowed = {
    "mod/descriptor.mod": lambda l: l.strip() == 'supported_version="1.19.2.0"',
    "mod/common/scripted_effects/japan_scripted_events_mod.txt": lambda l: l.strip() in ("id = 7167", "id = 4028"),
    "mod/history/countries/ARG - Argentina.txt": lambda l: l.strip() in ("retire_character = ARG_agustín_pedro_justo",
                                                                        "recruit_character = ARG_roberto_maria_ortiz"),
    "mod/common/decisions/JAP.txt": lambda l: False, "mod/common/decisions/SOV.txt": lambda l: False,
    "mod/events/BFTB_NewsEvents.txt": lambda l: False,
}
for c in SF:
    allowed[f"mod/history/countries/{c}.txt"] = lambda l: bool(SF_LINE.match(l))


def old_volkssturm_block(b):
    """Lines of the author's unit-creation block in the Volkssturm focus (replaced in CHANGELOG section 6)."""
    t = b.decode("utf-8", "replace").replace("\r", "")
    h = t.index("hidden_effect = {", t.index("id = GER_form_volksturm"))
    i, depth = t.index("{", h), 0
    while True:
        depth += {"{": 1, "}": -1}.get(t[i], 0)
        if depth == 0:
            break
        i += 1
    return set(t[t.rindex("\n", 0, h) + 1:t.index("\n", i)].split("\n"))


VS_OLD = old_volkssturm_block(at_base("mod/common/national_focus/germany.txt"))
allowed["mod/common/national_focus/germany.txt"] = lambda l: l in VS_OLD
allowed["mod/localisation/english/custom_mod_l_english.yml"] = lambda l: l.startswith("GER_form_volksturm_tooltip:0 ")
allowed["mod/events/mod_news.txt"] = lambda l: l.strip() in ("remove_building = {", "type = bunker", "province = 13372",
                                                          "province = 13371", "province = 13370", "level = 5", "}", "")
allowed["mod/common/decisions/GER_mod.txt"] = lambda l: l.strip() == "62 = {"
allowed["mod/events/mod_events.txt"] = lambda l: l.strip() == "6 = {"
for f in ("mod/history/units/GER_1944.txt", "mod/history/units/GER_1944_nsb.txt",
          "mod/common/units/names_divisions/GER_names_divisions.txt", "mod/events/ss_recruitment_event.txt"):
    allowed[f] = lambda l: False  # Wiking + Nordland: pure additions, nothing of the author's removed
for path, ok_line in allowed.items():
    diff = git("diff", "-U0", "--no-color", BASE, "HEAD", "--", path).decode("utf-8", "replace").replace("\r", "")
    removed = [l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    bad = [l for l in removed if not ok_line(l)]
    check(f"{path[4:]}: {len(removed)} removed line(s), all expected", not bad, "; ".join(bad[:3]))

# germany.txt: every changed spot lies inside the Volkssturm focus (not just lines that look like it)
base_g = at_base("mod/common/national_focus/germany.txt").decode("utf-8", "replace").replace("\r", "")
g_start = base_g.index("id = GER_form_volksturm")
g_lo, g_hi = base_g.count("\n", 0, g_start) + 1, base_g.count("\n", 0, base_g.index("\tfocus = {", g_start)) + 1
g_diff = git("diff", "-U0", "--no-color", BASE, "HEAD", "--", "mod/common/national_focus/germany.txt").decode("utf-8", "replace")
g_hunks = [(int(a), int(b or 1)) for a, b in re.findall(r"^@@ -(\d+)(?:,(\d+))? ", g_diff, re.M)]
check(f"common/national_focus/germany.txt: all {len(g_hunks)} changed spot(s) are inside the Volkssturm focus (base lines {g_lo}-{g_hi})",
      bool(g_hunks) and all(g_lo <= a and a + max(b, 1) - 1 <= g_hi for a, b in g_hunks), str(g_hunks))

# rebuilt files: author's parts identical, everything else identical to 1.19.3
rel = "common/national_focus/netherlands.txt"
new_l = current("mod/" + rel).decode("utf-8").splitlines()
van_l = vanilla(rel).decode("utf-8").splitlines()
import difflib  # noqa: E402
d = [l for l in difflib.unified_diff(van_l, new_l, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("---", "+++")]
author = ["+\t\t\tOR = {", "+\t\t\t\ttag = HOL", "+\t\t\t\ttag = RKN #1944", "+\t\t\t}", "-\t\t\ttag = HOL"]
check("netherlands.txt = 1.19.3 + only the author's RKN edit and #1944 marker",
      sorted(x for x in d if "search_filters" not in x) == sorted(author) and len(d) == 7)
base_nl = at_base("mod/" + rel).decode("utf-8-sig", errors="replace")
check("  ...and that RKN edit is exactly what the Workshop version had", "tag = RKN #1944" in base_nl)

rel = "common/countries/cosmetic.txt"
new_r, van_r, base_r = parse_bytes(current("mod/" + rel)), parse_bytes(vanilla(rel)), parse_bytes(at_base("mod/" + rel))
vk = [n.key for n in van_r if n.key]
own = [n for n in base_r if n.key and n.key not in set(vk)]
newd = {}
for n in new_r:
    if n.key:
        newd.setdefault(n.key, []).append(canon(n))
check("cosmetic.txt: all 1.19.3 entries present and identical",
      all(canon(n) in newd.get(n.key, []) for n in van_r if n.key))
check(f"cosmetic.txt: all {len(own)} author entries present and identical", all(canon(n) in newd.get(n.key, []) for n in own))

for fname, stock in (("AST - Australia.txt", 4), ("SIA - Siam.txt", 0)):
    rel = f"history/countries/{fname}"
    new_r, van_r, base_r = parse_bytes(current("mod/" + rel)), parse_bytes(vanilla(rel)), parse_bytes(at_base("mod/" + rel))
    nb = [canon(n) for n in new_r if n.key == "1943.12.30"]
    bb = [canon(n) for n in base_r if n.key == "1943.12.30"]
    check(f"{fname}: the author's 1944 block is byte-for-byte the Workshop version's", nb == bb and len(nb) == 1)
    bs = [canon(n) for n in base_r if n.key == "add_equipment_to_stockpile"]
    ns = [canon(n) for n in new_r if n.key == "add_equipment_to_stockpile"]
    check(f"{fname}: the author's {stock} extra stockpile(s) identical", ns[len(ns) - len(bs):] == bs and len(bs) == stock)
    rest = [canon(n) for n in new_r if n.key != "1943.12.30"]
    rest = rest[:len(rest) - stock] if stock else rest
    van = [canon(n) for n in van_r]
    diffs = [(a, b) for a, b in zip(rest, van) if a != b]
    fixed = [(a, b) for a, b in diffs if a.replace("AST_domestic_industry", "AST_domestic_industries") == b]
    check(f"{fname}: everything else identical to 1.19.3" + (" (except the documented AST_domestic_industry fix)" if stock else ""),
          len(rest) == len(van) and len(diffs) == len(fixed) and len(fixed) == (1 if stock else 0))

print("\n== 4. Every fix is in place ==")
j = current("mod/common/scripted_effects/japan_scripted_events_mod.txt").decode()
check("A  Ichi-Go: both wrong-state provinces commented out",
      "#id = 7167 # fix" in j and "#id = 4028 # fix" in j and not re.search(r"^\s*id = (7167|4028)\s*$", j, re.M))
import check_province_modifiers as cpm  # noqa: E402
p2s, sf = cpm.province_to_state(with_files=True)
check("G  states 870/871/873 each defined exactly once", all(len(sf[s]) == 1 for s in ("870", "871", "873")))
check("U  descriptor says 1.19.3.0", b'supported_version="1.19.3.0"' in current("mod/descriptor.mod"))
nl = pdx.parse_file("mod/common/national_focus/netherlands.txt")[0]
def focus_ids(root):
    return {c.value for n, _ in pdx.walk(root) if n.key in ("focus", "shared_focus") and n.is_block() for c in n.value if c.key == "id"}
ids = focus_ids(nl)
van_ids = focus_ids(pdx.parse(vanilla("common/national_focus/netherlands.txt").decode("utf-8-sig"))[0])
base_ids = focus_ids(parse_bytes(at_base("mod/common/national_focus/netherlands.txt")))
restored = van_ids - base_ids
check(f"U  every focus of the 1.19.3 Netherlands tree is in the mod's tree ({len(van_ids)}), incl. the {len(restored)} that were missing",
      van_ids <= ids and len(restored) == 15, ", ".join(sorted(restored)[:3]) + " ...")
old_sf, subs = [], 0
for dp, _, fs in os.walk("mod/history/countries"):
    for f in fs:
        for n, _ in pdx.walk(pdx.parse_file(os.path.join(dp, f))[0]):
            if n.key and SF_LINE.match(f"{n.key} = 1") and n.value == "1":
                old_sf.append(f)
            if n.key == "set_sub_doctrine" and re.fullmatch(r"(marines|paratroopers|mountaineers)_[12]", n.value or ""):
                subs += 1
check("U  no pre-1.19 special-forces tech names left; 18 sub-doctrine grants added", not old_sf and subs == 18,
      f"old names in {sorted(set(old_sf))}, sub-doctrines {subs}")
jr = pdx.parse_file("mod/common/decisions/JAP.txt")[0]
jd = {c.key for n in jr if n.key == "operations" for c in n.value if c.key}
check("U  7 Tauran decisions in JAP.txt", sum(1 for k in jd if "tauran" in k.lower() or k.endswith("_MON")) >= 7)
check("U  Sakhalin decision in SOV.txt",
      b"SOV_cancel_the_japanese_resource_rights_to_sakhalin_decision = {" in current("mod/common/decisions/SOV.txt"))
check("U  event bftb_news.11 defined", re.search(rb"id\s*=\s*bftb_news\.11\b", current("mod/events/BFTB_NewsEvents.txt")) is not None)
allmod = b"".join(current(os.path.join(dp, f)) for dp, _, fs in os.walk("mod") for f in fs if f.endswith(".txt"))
check("U  old IDs gone (accented ARG_agustin_pedro_justo, AST_domestic_industries, SIA_pridi_phanomyong)",
      not any(x.encode() in allmod for x in ("ARG_agustín_pedro_justo", "AST_domestic_industries", "SIA_pridi_phanomyong")))

ev = pdx.parse_file("mod/events/slovak_uprising.txt")[0]
evn = next((n for n in ev if n.key == "country_event"), None)
oa = current("mod/common/on_actions/slovak_uprising_on_actions.txt")
loc = current("mod/localisation/english/slovak_uprising_l_english.yml")
loc_lines = loc[3:].decode("utf-8").split("\r\n")
ls_dec = pdx.parse_file("mod/common/decisions/GER_last_stand_decisions.txt")[0]
ls_d = {d.key: d for c in ls_dec if c.key == "war_measures" for d in c.value if d.key}
ls_dm = pdx.parse_file("mod/common/dynamic_modifiers/GER_last_stand_dynamic_modifiers.txt")[0]
ls_oa = current("mod/common/on_actions/GER_last_stand_on_actions.txt")
ls_ev = current("mod/events/GER_last_stand_events.txt")
ls_loc = current("mod/localisation/english/GER_last_stand_l_english.yml")
def ls_guarded(n):
    en = next((c for c in n.value if c.key == "enable"), None)
    return en is not None and "has_war_with" in str([x.key for x, _ in pdx.walk(en.value)]) and any(x.value == "GER" for x, _ in pdx.walk(en.value) if not x.is_block())
check("N/W  Nero Decree + Werwolf: 2 decisions at 50 PP; 4 state modifiers active only under enemy control; capture + monthly hooks; resistance threshold 25; 2 events; 25 texts with BOM",
      set(ls_d) == {"GER_nero_decree", "GER_werwolf_decision"}
      and all(next((c.value for c in d.value if c.key == "cost"), None) == "50" for d in ls_d.values())
      and len([n for n in ls_dm if n.key]) == 4 and all(ls_guarded(n) for n in ls_dm if n.key)
      and all(x in ls_oa for x in (b"on_state_control_changed", b"on_monthly_GER", b"resistance > 25", b"GER_nero_state_wrecked"))
      and b"resistance > -1" not in ls_oa
      and all(x in ls_ev for x in (b"id = downfall_ger.1", b"id = downfall_ger.2", b"GFX_report_event_GER_speer"))
      and ls_loc.startswith(bytes.fromhex("efbbbf") + b"l_english:") and ls_loc.count(b":0 ") == 25)

vs_e = current("mod/common/scripted_effects/GER_volkssturm_effects.txt").decode("ascii")
vs_d = current("mod/common/decisions/GER_volkssturm_decisions.txt").decode("ascii")
vs_l = current("mod/localisation/english/GER_volkssturm_l_english.yml")
vs_f = current("mod/common/national_focus/germany.txt").decode("utf-8", "replace").split("id = GER_form_volksturm", 1)[1].split("\tfocus = {", 1)[0]
DATED = re.compile(r"\d+\.\d+\.\d+(\.\d+)?")
def state_1944(path):
    """(id, owner, cores, population) of a state at the 1944 start: undated history plus dated blocks up to 1944.1.1."""
    st = next(n for n in pdx.parse_file(path)[0] if n.key and n.key.lower() == "state")
    hist = next((n.value for n in st.value if n.key == "history"), [])
    blocks = [[n for n in hist if not (n.is_block() and DATED.fullmatch(n.key or ""))]]
    dated = [(tuple(int(x) for x in n.key.split(".")[:3]), n.value) for n in hist if n.is_block() and DATED.fullmatch(n.key or "")]
    blocks += [b for d, b in sorted(dated, key=lambda x: x[0]) if d <= (1944, 1, 1)]
    owner, cores = None, set()
    for n in (n for b in blocks for n in b):
        if n.key == "owner":
            owner = n.value
        elif n.key == "add_core_of":
            cores.add(n.value)
        elif n.key == "remove_core_of":
            cores.discard(n.value)
    sid = next(n.value for n in st.value if n.key == "id")
    return sid, owner, cores, int(float(next(n.value for n in st.value if n.key == "manpower")))
ger = {sid: pop for sid, owner, cores, pop in (state_1944(p) for p in pdx.merged_files("mod", V, os.path.join("history", "states")).values())
       if owner == "GER" and "GER" in cores}
thr = [int(x) for x in re.findall(r"state_population_k > (\d+)", vs_e)]
first = sum(sum(1 for t in thr if pop / 1000 > t) for pop in ger.values())
per = {k: sum(int(x) for x in re.findall(r"end = (\d+) GER_volkssturm_raise_division", b))
       for k, b in re.findall(r"\n\t(GER_volkssturm_\w+) = \{(.*?)\n\t\}", vs_d, re.S)}
d_states = set(re.findall(r"^\t{4}(\d+) = \{", vs_d, re.M))
def table_ok(f):
    body = vs_e.split(f"GER_volkssturm_raise_division_{f} = {{", 1)[1].split("\n}", 1)[0]
    owners = re.findall(r'owner = \\"([A-Z]{3})\\"', body)
    return (sum(int(x) for x in re.findall(r"^\t\t(\d+) = \{", body, re.M)) == 100 and len(owners) == 9
            and body.count(f"start_equipment_factor = 0.{f} ") == 9 and body.count("start_experience_factor = 0 ") == 9
            and all(t == "GER" or f"country_exists = {t}" in body for t in owners) and "seed = random" in body
            and set(re.findall(r"infantry_equipment_(\d)", body)) == {"0", "1"})
vs_keys = set(re.findall(rb"^ (\w+):0 ", vs_l, re.M))
vs_need = set(re.findall(r"tooltip = (GER_volkssturm_\w+)", vs_d)) | set(per) | {k + "_desc" for k in per}
check("V  Volkssturm: the focus raises 42 divisions by population (38 German cores); 4 decisions add 26/10/6/5 from their historical dates; "
      "raised in every state Germany still holds (not only fully held ones), owner = ROOT; "
      "rifle tables sum to 100 at 40/50/60/75% equipment, no training, foreign rifles only while that country exists, seed = random; 20 texts with BOM",
      len(ger) == 38 and first == 42
      and per == {"GER_volkssturm_east": 26, "GER_volkssturm_oder": 10, "GER_volkssturm_west": 6, "GER_volkssturm_berlin": 5}
      and d_states <= set(ger)
      and all(f"date > {d}" in vs_d for d in ("1945.1.12", "1945.1.31", "1945.2.8", "1945.4.16"))
      and vs_d.count("cost = 25") == 4 and vs_d.count("fire_only_once = yes") == 4
      and all(table_ok(f) for f in ("40", "50", "60", "75"))
      and "create_unit" not in vs_f and "GER_volkssturm_first_levy = yes" in vs_f and "GER_volkssturm_ensure_template = yes" in vs_f
      and "has_full_control_of_state" not in vs_f + vs_d and "is_controlled_by = ROOT" in vs_f
      and vs_d.count("is_controlled_by = ROOT") == 20 and vs_d.count("NOT = { is_fully_controlled_by = ROOT }") == 4
      and vs_e.count("owner = ROOT }") == 36 and "owner = GER }" not in vs_e
      and vs_l.startswith(bytes.fromhex("efbbbf") + b"l_english:") and len(vs_keys) == 20 and {k.encode() for k in vs_need} <= vs_keys,
      f"German cores {len(ger)}, first levy {first}, decisions {per}")

kb = current("mod/events/mod_news.txt").decode("utf-8", "replace").replace("\r", "")
kb = kb[kb.index("id = mod.news.5"):]
kb = kb[:kb.index("news_event = {")] if "news_event = {" in kb else kb
kb_active = re.findall(r"^[ \t]*province = (\d+)", kb, re.M)
check("K  Konigsberg in Ruins removes forts only in Konigsberg (6332) and its ring fort (11265), no longer in Africa (13370-13372)",
      kb_active == ["6332", "11265"] and all(p2s.get(x) == "763" for x in kb_active), str(kb_active))

PROV_EFFECTS = ("add_province_modifier", "remove_province_modifier", "add_building_construction", "remove_building",
                "damage_building", "set_building_level")
def wrong_state_refs(path):
    """(province, scope state, real state) for every province effect whose province is outside its state scope."""
    out = []
    for node, parents in pdx.walk(pdx.parse_file(path)[0]):
        if node.key in PROV_EFFECTS and node.is_block():
            scope = next((x.key for x in reversed(parents) if x.key and x.key.isdigit()), None)
            for c in node.value:
                if c.key != "province":
                    continue
                ids = [x.value for x in c.value if x.key == "id"] if c.is_block() else [c.value]
                out += [(i, scope, p2s.get(i)) for i in ids if scope and i.isdigit() and p2s.get(i) != scope]
    return out
sa = {f: wrong_state_refs(f) for f in ("mod/events/mod_news.txt", "mod/common/decisions/GER_mod.txt", "mod/events/mod_events.txt")}
check("S/A  Stettin fort built in state 63 and Antwerp sabotage in state 977; no province outside its state in the three fixed files",
      not any(sa.values()) and b"63 = { " in current("mod/common/decisions/GER_mod.txt") and b"977 = { " in current("mod/events/mod_events.txt"),
      str({k: v for k, v in sa.items() if v}))

fb = {k: current("mod/" + f).decode("ascii") for k, f in (
    ("eff", "common/scripted_effects/GER_festung_berlin_effects.txt"), ("mods", "common/modifiers/GER_festung_berlin_modifiers.txt"),
    ("dyn", "common/dynamic_modifiers/GER_festung_berlin_dynamic_modifiers.txt"), ("oa", "common/on_actions/GER_festung_berlin_on_actions.txt"),
    ("ev", "events/GER_festung_berlin_events.txt"))}
fb_loc = current("mod/localisation/english/GER_festung_berlin_l_english.yml")
fb_eff = pdx.parse_file("mod/common/scripted_effects/GER_festung_berlin_effects.txt")[0]
def fb_topups(name):
    """{province: (target, ok)}: ok = every start level 0-10 ends at max(start, target), simulated branch by branch."""
    res = {}
    state = next(n for n in next(n for n in fb_eff if n.key == name).value if n.key == "64")
    for blk in (b for b in state.value if b.key == "if"):
        prov = next(c.value for c, _ in pdx.walk(blk.value) if c.key == "controls_province")
        br = [(int(next(x.value for x, _ in pdx.walk(c.value) if x.key == "level" and x.op == "<")),
               int(next(x.value for x, _ in pdx.walk(c.value) if x.key == "level" and x.op == "=")))
              for c in blk.value if c.key in ("if", "else_if")]
        target = br[-1][0]
        res[prov] = (target, all(next((s + a for c, a in br if s < c), s) == max(s, target) for s in range(11)))
    return res
FB_RING = ["375", "3499", "9428", "11444", "11505"]
fb_expect = {"GER_festung_berlin_forts_step_1": {"6521": 2, **{x: 1 for x in FB_RING}},
             "GER_festung_berlin_forts_step_2": {"6521": 4, **{x: 2 for x in FB_RING}},
             "GER_festung_berlin_forts_step_3": {"6521": 5}, "GER_seelow_forts_step_1": {"9496": 2}, "GER_seelow_forts_step_2": {"9496": 4}}
fb_sim = {n: fb_topups(n) for n in fb_expect}
fb_keys = set(re.findall(rb"^ ([\w.]+):0 ", fb_loc, re.M))
fb_need = set(re.findall(r"(?:title|desc|name|custom_effect_tooltip) = (festung_berlin\.[\w.]+)", fb["ev"]))
fb_defs = re.findall(r"^\tid = (festung_berlin\.\d+)", fb["ev"], re.M)
fb_calls = set(re.findall(r"(?:country_event|news_event) = \{ id = (festung_berlin\.\d+)", fb["ev"] + fb["oa"]))
check("B  Festung Berlin: forts only topped up (simulated for start levels 0-10), Berlin 2/4/5, ring 1/2, Seelow 2/4, never above 5; "
      "all provinces in Brandenburg; triggers on the 6 bordering states and Seelow's 4 outer neighbours; Brandenburg bonus only while "
      "Germany owns and controls it; 3 emergency divisions; human-only Berlin bonus unless the author's focus gave it; Weidling guarded; 9 events, 25 texts",
      all({p: tg for p, (tg, _) in fb_sim[n].items()} == e and all(g for _, g in fb_sim[n].values()) for n, e in fb_expect.items())
      and max(int(x) for x in re.findall(r"level < (\d+)", fb["eff"])) <= 5
      and all(p2s.get(x) == "64" for x in FB_RING + ["6521", "9496"])
      and "OR = { state = 59 state = 60 state = 61 state = 62 state = 65 state = 68 }" in fb["oa"]
      and all("NOT = { controls_province = %s }" % x in fb["oa"] for x in ("3473", "537", "3572", "3207"))
      and all(p2s.get(x) != "64" for x in ("3473", "537", "3572", "3207"))
      and "is_owned_by = GER" in fb["dyn"] and "is_controlled_by = GER" in fb["dyn"]
      and "enemy_army_speed_factor = -0.1" in fb["dyn"] and "land_bunker_effectiveness_factor = 0.1" in fb["dyn"]
      and fb["eff"].count("create_unit") == 3 and fb["eff"].count("owner = ROOT") == 3 and fb["eff"].count("prioritize_location = 6521") == 3
      and "is_ai = no" in fb["ev"] and "NOT = { has_completed_focus = GER_festung_cities }" in fb["ev"]
      and "has_completed_focus = GER_festung_cities }" in fb["oa"]
      and "has_character = GER_helmuth_weidling" in fb["ev"] and "NOT = { has_trait = urban_assault_specialist }" in fb["ev"]
      and len(fb_defs) == 9 and fb_calls == set(fb_defs)
      and fb_loc.startswith(bytes.fromhex("efbbbf") + b"l_english:") and len(fb_keys) == 25 and {k.encode() for k in fb_need} <= fb_keys,
      str({n: {p: tg for p, (tg, g) in r.items() if not g} for n, r in fb_sim.items()}))

def ss_oob(path):
    """(templates {name: (regiments, support, names group, priority)}, {name_order: (template, location, exp, equip)}, SS name_order counts)."""
    root = pdx.parse_file(path)[0]
    tpls = {}
    for n in root:
        if n.key == "division_template" and n.is_block():
            g = lambda k: next((c.value for c in n.value if c.key == k), None)
            regs = sorted((r.key, next(c.value for c in r.value if c.key == "x"), next(c.value for c in r.value if c.key == "y"))
                          for b in n.value if b.key == "regiments" for r in b.value if r.key)
            sup = sorted(r.key for b in n.value if b.key == "support" for r in b.value if r.key)
            tpls[g("name").strip('"')] = (regs, sup, g("division_names_group"), g("priority"))
    divs, orders = {}, {}
    for d in next(n for n in root if n.key == "units").value:
        if d.key != "division" or not d.is_block():
            continue
        g = lambda k: next((c.value for c in d.value if c.key == k), None)
        tn = (g("division_template") or "").strip('"')
        dn = next((c for c in d.value if c.key == "division_name"), None)
        o = next((c.value for c in dn.value if c.key == "name_order"), None) if dn else None
        if o and tpls.get(tn, (0, 0, None))[2] == "GER_SS_01":
            orders[o] = orders.get(o, 0) + 1
            divs[o] = (tn, g("location"), g("start_experience_factor"), g("start_equipment_factor"))
    return tpls, divs, orders
ss_ok, ss_detail = True, {}
for f in ("mod/history/units/GER_1944_nsb.txt", "mod/history/units/GER_1944.txt"):
    tp, dv, od = ss_oob(f)
    pg, sp = tp.get("Panzergrenadier"), tp.get("SS-Panzergrenadier-Division")
    ok = (pg is not None and sp is not None and pg[:2] == sp[:2] and sp[2:] == ("GER_SS_01", "2")
          and dv.get("5") == ("SS Panzer-Division", "11424", "1.0", "0.9")
          and dv.get("11") == ("SS-Panzergrenadier-Division", "11080", "1.0", "0.95")
          and all(v == 1 for v in od.values()))
    ss_ok = ss_ok and ok
    ss_detail[f[18:]] = (dv.get("5"), dv.get("11"), od)
st203 = current("mod/history/states/203-Cherkasy.txt").decode("utf-8-sig").replace("\r", "")
st208 = current("mod/history/states/208-Pskov.txt").decode("utf-8-sig").replace("\r", "")
ss_names = current("mod/common/units/names_divisions/GER_names_divisions.txt").decode("utf-8-sig").split("GER_SS_01 =", 1)[1].split("\n}", 1)[0]
ss_ev = current("mod/events/ss_recruitment_event.txt").decode("utf-8-sig")
check("W  Wiking (#5, SS Panzer-Division, 11424) and Nordland (#11, SS copy of the Panzergrenadier template, 11080) in both "
      "1944 OOB files with experience 1.0; both positions German-held on 1 Jan 1944; no SS number twice; name list 5 = Wiking; "
      "the recruitment event only creates Wiking in games that started before 1944",
      ss_ok and p2s.get("11424") == "203" and p2s.get("11080") == "208"
      and "1943.12.30 = {\n\t\t\tcontroller = GER\n\t\t\towner = GER" in st203 and "11424" not in re.findall(r"set_province_controller = (\d+)", st203)
      and "owner = GER" in st208 and "set_province_controller" not in st208
      and "5 = { \"%d. SS-Division 'Wiking'\" }" in ss_names and "11 = { \"%d. SS-Division 'Nordland'\" }" in ss_names
      and ss_ev.count("has_start_date < 1944.1.1") == 2 and ss_ev.count("else_if = { # 1944 start: Wiking already exists") == 2,
      str(ss_detail))

oar = pdx.parse_file("mod/common/on_actions/slovak_uprising_on_actions.txt")[0]
mp_changes = [(next((p.key for p in reversed(parents) if p.key in ("GER", "SLO")), "SLO (event scope)"), n.value)
              for n, parents in pdx.walk(oar) if n.key == "add_manpower"]
check("F  Slovak uprising: event with its picture, fired once on 29 Aug 1944 for SLO + GER, Germany -3000 manpower (Slovakia none), 4 one-line texts with BOM",
      evn is not None and any(c.key == "id" and c.value == "slovak.uprising.1" for c in evn.value)
      and any(c.key == "picture" and c.value == "GFX_report_event_czech_soldiers_02" for c in evn.value)
      and all(s in oa for s in (b"on_daily_SLO", b"date > 1944.8.28", b"SLO_slovak_uprising"))
      and mp_changes == [("GER", "-3000")]
      and (chr(167) + "YGermany" + chr(167) + "! loses " + chr(167) + "R3,000") in loc.decode("utf-8")
      and loc.startswith(b"\xef\xbb\xbfl_english:")
      and sum(1 for l in loc_lines if l.startswith(" slovak.uprising.1.")) == 4
      and all(l.count(chr(34)) == 2 for l in loc_lines[1:] if l))

print("\n== 5. The game's own error.log: fixed errors are gone ==")
before = open("docs/game-logs/2-workshop-version_error.log", encoding="utf-8", errors="replace").read()
after = open("docs/game-logs/4-after-1.19.3-update_error.log", encoding="utf-8", errors="replace").read()
for label, pat in (("duplicate states", r"State ID conflict"), ("invalid special-forces techs", r"Invalid tech|invalid database object"),
                   ("missing Netherlands focuses", r"_taog|Couldn't find dependency"), ("missing decisions", r"Invalid Decision ID for (activate_mission|targeted)"),
                   ("missing event", r"non-existant event"), ("renamed IDs", r"Unkown focus|recruit_character: Unknown|retire_character: Unknown character \n")):
    b, a = len(re.findall(pat, before)), len(re.findall(pat, after))
    check(f"{label}: {b} before -> {a} after", b > 0 and a == 0)

print("\n== 6. SHA-256 checksums ==")
os.makedirs("docs/checksums", exist_ok=True)
lines = []
for p in sorted(paths):
    lines.append(f"{hashlib.sha256(current(p)).hexdigest()}  {p[4:]}")
manifest = ("\n".join(lines) + "\n").encode()
open("docs/checksums/mod-files.sha256", "wb").write(manifest)
print(f"wrote docs/checksums/mod-files.sha256 ({len(lines)} files); digest of the whole list: {hashlib.sha256(manifest).hexdigest()[:16]}")

print("\n" + ("ALL CHECKS PASSED" if not FAILS else f"{len(FAILS)} CHECK(S) FAILED: {FAILS}"))
sys.exit(1 if FAILS else 0)
