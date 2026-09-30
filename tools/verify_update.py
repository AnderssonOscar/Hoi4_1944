"""Re-verify every claim about the fixes and the 1.19.3 update. Prints PASS/FAIL.

Run from the project folder:  python tools/verify_update.py
Needs: git, the HOI4 1.19.3 install, and the Steam Workshop copy of the mod.
Also writes docs/checksums/mod-files.sha256 (SHA-256 of every mod file).
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

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
ws_files = sorted(os.path.relpath(os.path.join(dp, f), W).replace(os.sep, "/")
                  for dp, dn, fn in os.walk(W) if not dn.__setitem__(slice(None), [d for d in dn if d != ".git"]) for f in fn)
ws = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], cwd=W, capture_output=True,
                    input="\n".join(rel).encode()).stdout.split()
ws_is_baseline = sorted(rel) == ws_files and ws == [m.split()[2] for m, _ in base_tree]
# On 29 Sep 2026 the author published the update himself: his GitHub main at the merge of pull request #3
# (c267d4f), which is this package at 470916b plus his README.md and his .gitattributes (CHANGELOG section 13).
PUBLISHED = "470916b"
pub_rel = [p[4:] for p in git("ls-tree", "-r", "--name-only", PUBLISHED, "--", "mod").decode("utf-8").splitlines()]
ws_is_published = (not ws_is_baseline and ws_files == sorted(pub_rel + ["README.md"])
                   and all(git("show", f"{PUBLISHED}:mod/{f}").replace(b"\r\n", b"\n")
                           == open(os.path.join(W, f), "rb").read().replace(b"\r\n", b"\n")
                           for f in pub_rel if f != ".gitattributes"))
check("Steam Workshop copy never edited here: it is either the July 2026 baseline (914 files) or the author's own published update "
      "of 29 Sep 2026 (this package at 470916b plus his README, ignoring line endings)",
      ws_is_baseline or ws_is_published, "baseline" if ws_is_baseline else ("published update" if ws_is_published else "neither"))


def _rm_readonly(func, path, _):
    os.chmod(path, 0o700)  # git's object files are read-only on Windows
    func(path)


# A fresh clone must get every mod file byte-for-byte: no line-ending conversion on checkout (CHANGELOG section 13).
clone_dir = tempfile.mkdtemp(prefix="downfall-clone-")
try:
    subprocess.run(["git", "clone", "-q", ".", clone_dir], capture_output=True)
    cloned = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], cwd=clone_dir, capture_output=True,
                            input="\n".join(paths).encode()).stdout.split()
finally:
    if sys.version_info >= (3, 12):
        shutil.rmtree(clone_dir, onexc=_rm_readonly)
    else:
        shutil.rmtree(clone_dir, onerror=_rm_readonly)
check(f"a fresh clone reproduces all {len(paths)} mod files byte-for-byte (no line-ending conversion on checkout)", cloned == blobs)

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
expected |= {("A", f"mod/{f}") for f in ("common/decisions/GER_1945_operations_decisions.txt",
             "common/dynamic_modifiers/GER_1945_operations_dynamic_modifiers.txt", "common/ideas/GER_1945_operations_ideas.txt",
             "common/modifiers/GER_1945_operations_modifiers.txt", "common/on_actions/GER_1945_operations_on_actions.txt",
             "common/scripted_effects/GER_1945_operations_effects.txt", "events/GER_1945_operations_events.txt",
             "localisation/english/GER_1945_operations_l_english.yml")}  # 1945 operations (section 11)
expected |= {("A", f"mod/{f}") for f in ("common/decisions/GER_reserves_decisions.txt", "common/ideas/GER_reserves_ideas.txt",
             "common/on_actions/GER_reserves_on_actions.txt", "common/scripted_effects/GER_reserves_effects.txt",
             "events/GER_reserves_events.txt", "localisation/english/GER_reserves_l_english.yml")}  # last reserves (section 12)
expected |= {("M", "mod/.gitattributes")}  # no line-ending conversion in clones (section 13)
expected |= {("A", f"mod/{f}") for f in ("common/ideas/GER_homefront_ideas.txt", "common/on_actions/GER_homefront_on_actions.txt",
             "common/scripted_effects/GER_homefront_effects.txt", "events/GER_homefront_events.txt",
             "localisation/english/GER_homefront_l_english.yml")}  # the home front, 1944-45 (section 14)
expected |= {("M", "mod/common/on_actions/do_on_actions.txt"), ("M", "mod/history/countries/YUG - Yugoslavia.txt")}  # UK start fix (section 15)
expected |= {("A", f"mod/{f}") for f in ("common/decisions/GER_measures_decisions.txt", "common/ideas/GER_measures_ideas.txt",
             "common/scripted_effects/GER_measures_effects.txt", "common/synchronized_dynamic_tokens/GER_equipment_tokens.txt",
             "events/GER_measures_events.txt", "localisation/english/GER_measures_l_english.yml")}  # five war measures (section 16)
expected |= {("A", f"mod/{f}") for f in ("common/scripted_effects/GER_legions_effects.txt", "common/on_actions/GER_legions_on_actions.txt",
             "events/GER_legions_events.txt", "localisation/english/GER_legions_l_english.yml")}  # legions, Wiking, Nordland (section 19)
expected |= {("A", f"mod/{f}") for f in ("interface/GER_legions.gfx", "gfx/events/report_event_GER_wiking_panzer.dds")}  # Wiking before Warsaw (section 21)
expected |= {("A", f"mod/{f}") for f in ("interface/GER_bomb.gfx", "gfx/events/report_event_GER_first_bomb.dds", "common/on_actions/GER_bomb_on_actions.txt",
             "events/GER_bomb_events.txt", "localisation/english/GER_bomb_l_english.yml")}  # the first German bomb (section 22)
expected |= {("A", f"mod/{f}") for f in ("interface/GER_leningrad.gfx", "gfx/events/report_event_GER_leningrad.dds",
             "common/on_actions/GER_leningrad_on_actions.txt", "events/GER_leningrad_events.txt",
             "localisation/english/GER_leningrad_l_english.yml")}  # Leningrad taken (sections 23, 25)
expected |= {("A", f"mod/{f}") for f in ("common/modifiers/GER_crimea_modifiers.txt", "common/scripted_effects/GER_crimea_effects.txt",
             "common/on_actions/GER_crimea_on_actions.txt", "common/decisions/GER_crimea_decisions.txt", "events/GER_crimea_events.txt",
             "localisation/english/GER_crimea_l_english.yml")}  # the Crimea (section 24)
expected |= {("A", f"mod/{f}") for f in ("interface/GER_dday.gfx", "gfx/events/report_event_GER_dday_repelled.dds",
             "common/on_actions/GER_dday_on_actions.txt", "events/GER_dday_events.txt",
             "localisation/english/GER_dday_l_english.yml")}  # the invasion beaten back (section 26)
expected |= {("A", f"mod/{f}") for f in ("gfx/events/report_event_GER_remagen_bridge.dds", "interface/GER_remagen.gfx",
             "common/scripted_effects/GER_remagen_effects.txt", "common/on_actions/GER_remagen_on_actions.txt",
             "events/GER_remagen_events.txt", "localisation/english/GER_remagen_l_english.yml")}  # the bridge at Remagen (section 20)
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
allowed["mod/.gitattributes"] = lambda l: l in ("# Auto detect text files and perform LF normalization", "* text=auto")
UK_FIX_REMOVED = {  # the UK start fix (section 15): these lines were turned into comments, nothing else removed
    "mod/history/countries/ENG - Britain.txt": {"add_to_faction = PHI", "add_to_faction = POL", "add_to_faction = YUG", "\tset_autonomy = {",
                                                "\t\ttarget = BRM", "\t\tautonomous_state = autonomy_colony", "\t\tfreedom_level = 0.35", "\t}"},
    "mod/history/countries/USA - USA.txt": {"set_autonomy = {", "\ttarget = PHI", "\tautonomous_state =  autonomy_colony", "}"},
    "mod/history/countries/YUG - Yugoslavia.txt": {"\tbecome_exiled_in = { target = ENG legitimacy = 30 }"},
    "mod/common/on_actions/do_on_actions.txt": set(),
}
for _f, _ok in UK_FIX_REMOVED.items():
    allowed[_f] = (lambda prev, ok: lambda l: prev(l) or l in ok)(allowed.get(_f, lambda l: False), _ok)
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
# Section 29: the game loads the 1944 order of battle only after all the history has run, so the 11 SS divisions that
# these two focus rewards create took SS numbers 1-11 first. They are now completed at game start instead.
ger_hist = current("mod/history/countries/GER - Germany.txt")
ss_start = current("mod/common/on_actions/GER_ss_names_on_actions.txt")
ss_foci = ("GER_expand_ss_recruitment", "GER_strengthen_the_waffen_ss")
ss_note = b" # now completed at game start: common/on_actions/GER_ss_names_on_actions.txt (docs/CHANGELOG.md section 29)"
ss_hist_prev = ger_hist
for f in ss_foci:
    ss_hist_prev = ss_hist_prev.replace(b"\t\t#complete_national_focus = " + f.encode() + ss_note + b"\r\n",
                                        b"\t\tcomplete_national_focus = " + f.encode() + b"\r\n")
ss_expect = ("on_actions={on_startup={effect={GER={" + " ".join(
    f"if={{limit={{NOT={{has_start_date=1943.12.30}} NOT={{has_completed_focus={f}}}}} complete_national_focus={f}}}" for f in ss_foci) + "}}}}")
ss_callers = [p for p in paths if p.endswith(".txt") and any(
    re.search(rb"^[ \t]*complete_national_focus = " + f.encode() + rb"\b", current(p), re.M) for f in ss_foci)]
check("Z  SS names at the 1944 start: the two SS focuses whose rewards create 11 SS divisions are completed at game start "
      "(on_startup, after the order of battle is loaded) instead of in the 1944 history; the history file is otherwise "
      "byte-identical to e09019a; once each, same order, only for starts from 1943.12.30; nothing else completes them; ASCII, CRLF",
      ss_hist_prev == git("show", "e09019a:mod/history/countries/GER - Germany.txt") and ss_hist_prev != ger_hist
      and ss_start.isascii() and ss_start.count(b"\n") == ss_start.count(b"\r\n")
      and canon(parse_bytes(ss_start)[0]) == ss_expect and ss_start.count(b"NOT = { has_start_date < 1943.12.30 }") == 2
      and ss_callers == ["mod/common/on_actions/GER_ss_names_on_actions.txt"],
      str(ss_callers))

op = {k: current("mod/" + f).decode("ascii") for k, f in (
    ("eff", "common/scripted_effects/GER_1945_operations_effects.txt"), ("dec", "common/decisions/GER_1945_operations_decisions.txt"),
    ("dyn", "common/dynamic_modifiers/GER_1945_operations_dynamic_modifiers.txt"), ("idea", "common/ideas/GER_1945_operations_ideas.txt"),
    ("oa", "common/on_actions/GER_1945_operations_on_actions.txt"), ("ev", "events/GER_1945_operations_events.txt"))}
op_eff = {n.key: n for n in pdx.parse_file("mod/common/scripted_effects/GER_1945_operations_effects.txt")[0] if n.key}
op_dec = {d.key: d for c in pdx.parse_file("mod/common/decisions/GER_1945_operations_decisions.txt")[0]
          if c.key == "war_measures" for d in c.value if d.key}
def op_get(node, key):
    return next((c for c in node.value if c.key == key), None)
OP_TYPES = [f"infantry_equipment_{i}" for i in range(4)] + [f"artillery_equipment_{i}" for i in (1, 2, 3)]
def op_amounts(effect):
    """(fuel, [needs set], [(type, amount) of every stockpile change], [variables added to], [variables reset]) of a set-aside or
    return effect. Since section 17 rifles and guns are taken type by type and the amount taken is stored per type."""
    nodes = [n for n, _ in pdx.walk(op_eff[effect].value)]
    return (int(next(n.value for n in op_eff[effect].value if n.key == "add_fuel")),
            [int(c.value) for n in op_eff[effect].value if n.key == "set_temp_variable" for c in n.value if c.key == "GER_1945_need"],
            [(op_get(n, "type").value, op_get(n, "amount").value) for n in nodes if n.key == "add_equipment_to_stockpile"],
            [(c.key, c.value) for n in nodes if n.key == "add_to_variable" for c in n.value],
            [(c.key, c.value) for n in nodes if n.key == "set_variable" for c in n.value])
def op_round_trip(o):
    (sf, sn, sp, sv, _), (rf, rn, rp, _, rr) = op_amounts(f"GER_1945_{o}_set_aside"), op_amounts(f"GER_1945_{o}_return")
    store = [f"GER_1945_{o}_{t}" for t in OP_TYPES]
    return (sf == -rf and [rf] + sn == op_needs(f"GER_1945_{o}") and not rn
            and sp == [(t, "GER_1945_amount") for t in OP_TYPES] and sv == [(v, "GER_1945_taken") for v in store]
            and rp == list(zip(OP_TYPES, store)) and rr == [(v, "0") for v in store])
def op_needs(dec):
    """[fuel, infantry equipment, artillery] the decision requires in stock (its '>' thresholds + 1)."""
    return [int(n.value) + 1 for n, _ in pdx.walk(op_get(op_dec[dec], "available").value)
            if n.key in ("has_fuel", "infantry_equipment", "artillery_equipment") and n.op == ">"]
def op_calls_in(dec, part):
    return {n.key for n, _ in pdx.walk(op_get(op_dec[dec], part).value) if n.value == "yes"}
op_res = {o: (op_amounts(f"GER_1945_{o}_set_aside")[:2], op_needs(f"GER_1945_{o}"), op_round_trip(o))
          for o in ("sonnenwende", "spring_awakening")}
op_units = [n for n, _ in pdx.walk(list(op_eff.values())) if n.key == "create_unit"]
op_tpl = next(n for n, _ in pdx.walk(op_eff["GER_1945_marine_template"].value) if n.key == "division_template")
op_tp = [n for n, _ in pdx.walk(op_eff["GER_1945_courland_evacuate"].value) if n.key == "teleport_armies"]
op_loc = current("mod/localisation/english/GER_1945_operations_l_english.yml")
op_keys = {k.decode() for k in re.findall(rb"^ ([\w.]+):0 ", op_loc, re.M)}
op_need = set(re.findall(r"(?:custom_effect_tooltip|tooltip|title|desc|name|text) = ((?:GER_1945|ger_1945)[\w.]+)", op["dec"] + op["ev"]))
op_defs = re.findall(r"^\tid = (ger_1945\.\d+)", op["ev"], re.M)
op_calls = set(re.findall(r"country_event = \{ id = (ger_1945\.\d+)", op["ev"] + op["dec"] + op["oa"]))
op_ns = sum(open(os.path.join(d, f), "rb").read().count(b"add_namespace = ger_1945\r") + open(os.path.join(d, f), "rb").read().count(b"add_namespace = ger_1945\n")
            for d in ("mod/events", os.path.join(V, "events")) for f in os.listdir(d) if f.endswith(".txt"))
sailors = op_get(op_dec["GER_1945_sailors_to_the_front"], "complete_effect")
check("O  1945 operations: Sonnenwende and Spring Awakening set aside exactly the fuel, rifles and guns they require, the rifles and "
      "guns type by type with what left the stockpile stored per type, and return exactly those types and amounts, both when "
      "launched and when called off (never launched when called off); 12 / 14 days of bonus after 7 / 10 days of preparation; 50 PP each; "
      "Courland moves only German armies, needs Libau or Windau, 30 days; Sailors: +1,000 manpower, -10 convoys, 3 divisions of plain "
      "infantry (not marines), 50% equipment, no experience; Stettin/Kiel/Libau/Windau in the right states; 10 events, 60 texts",
      all(ok for _, _, ok in op_res.values())
      and all({f"GER_1945_{o}_return", f"GER_1945_{o}_launch"} <= op_calls_in(f"GER_1945_{o}", "remove_effect")
              and op_calls_in(f"GER_1945_{o}", "cancel_effect") == {f"GER_1945_{o}_return"} for o in op_res)
      and [(s.key, op_get(op_get(s, "add_dynamic_modifier"), "days").value) for s in op_eff["GER_1945_sonnenwende_launch"].value]
          == [("63", "12"), ("68", "12"), ("64", "12")]
      and [n.value for n, _ in pdx.walk(op_eff["GER_1945_spring_awakening_launch"].value) if n.key == "days"] == ["14", "14"]
      and {d: (op_get(v, "cost").value, getattr(op_get(v, "days_remove"), "value", None)) for d, v in op_dec.items()}
          == {"GER_1945_sonnenwende": ("50", "7"), "GER_1945_spring_awakening": ("50", "10"),
              "GER_1945_courland_evacuation": ("50", "30"), "GER_1945_sailors_to_the_front": ("50", None)}
      and "army_core_attack_factor = 0.15" in op["dyn"] and "is_owned_by = GER" in op["dyn"]
      and [canon(n) for n, _ in pdx.walk(pdx.parse_file("mod/common/ideas/GER_1945_operations_ideas.txt")[0]) if n.key == "targeted_modifier"]
          == ["targeted_modifier={tag=SOV attack_bonus_against=0.1}"]
      and len(op_tp) == 6 and all(canon(op_get(t, "limit")) == "limit={original_tag=GER}" for t in op_tp)
      and [op_get(t, "to_state").value for t in op_tp if op_get(t, "to_state")] == ["807", "85", "63", "62", "58"]
      and "cancel_trigger = { NOT = { controls_province = 9262 } NOT = { controls_province = 3296 } }" in op["dec"]
      and op["oa"].count("remove_province_modifier") == 2
      and p2s.get("6282") == "63" and p2s.get("6389") == "58" and p2s.get("9262") == "190" and p2s.get("3296") == "190"
      and len(op_units) == 6 and all(op_get(u, "owner").value == "ROOT" for u in op_units)
      and all("start_experience_factor = 0 start_equipment_factor = 0.5 " in op_get(u, "division").value for u in op_units)
      and sorted(r.key for b in op_tpl.value if b.key == "regiments" for r in b.value) == ["infantry"] * 6
      and "marine" not in [r.key for b in op_tpl.value if b.key in ("regiments", "support") for r in b.value]
      and canon(op_get(sailors, "add_manpower")) == "add_manpower=1000"
      and canon(op_get(sailors, "add_equipment_to_stockpile")) == "add_equipment_to_stockpile={type=convoy_1 amount=-10}"
      and len(op_defs) == 10 and op_calls == set(op_defs) and op_ns == 1
      and op_loc.startswith(b"\xef\xbb\xbfl_english:\r\n") and len(op_keys) == 60 and op_need <= op_keys,
      str({o: v for o, v in op_res.items()}))

def canon_op(n):
    """Like canon, but keeps comparison operators (date > 1944.2.6 stays date>1944.2.6)."""
    return (f"{n.key}{n.op}" if n.key else "") + ("{" + " ".join(canon_op(c) for c in n.value) + "}" if n.is_block() else n.value)
rs = {k: current("mod/" + f).decode("ascii") for k, f in (
    ("dec", "common/decisions/GER_reserves_decisions.txt"), ("oa", "common/on_actions/GER_reserves_on_actions.txt"),
    ("ev", "events/GER_reserves_events.txt"))}
rs_eff = {n.key: n for n in pdx.parse_file("mod/common/scripted_effects/GER_reserves_effects.txt")[0] if n.key}
rs_dec = next(d for c in pdx.parse_file("mod/common/decisions/GER_reserves_decisions.txt")[0] if c.key == "war_measures" for d in c.value if d.key)
rs_ideas = {i.key: i for c in pdx.parse_file("mod/common/ideas/GER_reserves_ideas.txt")[0] if c.key == "ideas"
            for g in c.value if g.key == "country" for i in g.value if i.key}
rs_ifs = [canon_op(op_get(b, "limit")) for c in pdx.parse_file("mod/common/on_actions/GER_reserves_on_actions.txt")[0] if c.key == "on_actions"
          for d in c.value if d.key == "on_daily_GER" for b in op_get(d, "effect").value if b.key == "if"]
RS_AIR_TYPES = {"fighter", "interceptor", "cas", "naval_bomber", "tactical_bomber", "strategic_bomber", "suicide", "scout_plane",
                "air_transport", "heavy_fighter", "maritime_patrol_plane"}
rs_air = set()  # every aircraft type in the game, from its equipment files
for f in pdx.merged_files("mod", V, r"common\units\equipment").values():
    for t in pdx.parse_file(f)[0]:
        if t.key in ("equipments", "duplicate_archetypes") and t.is_block():
            for e in (e for e in t.value if e.key and e.is_block()):
                ty, arch = op_get(e, "type"), op_get(e, "is_archetype")
                tv = {x.value for x in ty.value} if ty is not None and ty.is_block() else ({ty.value} if ty is not None else set())
                if tv & RS_AIR_TYPES and (t.key == "duplicate_archetypes" or (arch is not None and arch.value == "yes")):
                    rs_air.add(e.key)
rs_bonus = op_get(rs_ideas["GER_reserves_swedish_parts"], "equipment_bonus")
rs_loc = current("mod/localisation/english/GER_reserves_l_english.yml")
rs_keys = {k.decode() for k in re.findall(rb"^ ([\w.]+):0 ", rs_loc, re.M)}
rs_need = (set(re.findall(r"(?:title|desc|name|custom_effect_tooltip) = (ger_reserves[\w.]+)", rs["ev"]))
           | {rs_dec.key, rs_dec.key + "_desc"} | set(rs_ideas) | {i + "_desc" for i in rs_ideas})
rs_defs = re.findall(r"^\tid = (ger_reserves\.\d+)", rs["ev"], re.M)
rs_calls = set(re.findall(r"country_event = \{ id = (ger_reserves\.\d+)", rs["oa"] + rs["dec"]))
RS_RING = ["375", "3499", "9428", "11444", "11505"]  # the five provinces around Berlin (as in Festung Berlin)
def rs_body(name):
    return [canon_op(n) for n in rs_eff[name].value]
check("R  Germany's last reserves: Estonia +38,000 (from 7 Feb 1944, Tallinn held); West +3,000 (an enemy holds Paris); up to 7,500 "
      "moved from Hungary to Germany, never more than Hungary has (30 days after the author's Arrow Cross flag); Luftwaffe decision "
      "(50 PP, from Sep 1944) +75,000 and 90 days of -10% air missions, then a story event; Sweden (28 Sep-31 Dec 1944): 3 trains, "
      "137 trucks, 1,800 support equipment, 250 fuel, 35 days of every aircraft type 13% cheaper; eastern workers +15,000 and 180 days "
      "of -1% factory output; round-ups +15,000 (from 1945, manpower < 200,000 or an enemy at Berlin's ring); each event once; "
      "7 events, 32 texts",
      rs_body("GER_reserves_estonian_mobilisation") == ["add_manpower=38000"]
      and rs_body("GER_reserves_western_volunteers") == ["add_manpower=3000"]
      and rs_body("GER_reserves_hungarian_ss") == [
          "if={limit={HUN={has_manpower>7499}} HUN={add_manpower=-7500} add_manpower=7500}",
          "else_if={limit={HUN={has_manpower>4999}} HUN={add_manpower=-5000} add_manpower=5000}",
          "else_if={limit={HUN={has_manpower>2499}} HUN={add_manpower=-2500} add_manpower=2500}"]
      and rs_body("GER_reserves_luftwaffe_transfer") == ["add_manpower=75000",
                                                         "add_timed_idea={idea=GER_reserves_luftwaffe_men_at_the_front days=90}"]
      and rs_body("GER_reserves_swedish_deliveries") == [
          "add_equipment_to_stockpile={type=train_equipment_1 amount=3}", "add_equipment_to_stockpile={type=motorized_equipment_1 amount=137}",
          "add_equipment_to_stockpile={type=support_equipment_1 amount=1800}", "add_fuel=250",
          "add_timed_idea={idea=GER_reserves_swedish_parts days=35}"]
      and rs_body("GER_reserves_eastern_volunteers") == ["add_manpower=15000",
                                                         "add_timed_idea={idea=GER_reserves_eastern_workers_enlisted days=180}"]
      and rs_body("GER_reserves_roundups") == ["add_manpower=15000"]
      and canon_op(op_get(rs_ideas["GER_reserves_luftwaffe_men_at_the_front"], "modifier")) == "modifier={air_mission_efficiency=-0.1}"
      and canon_op(op_get(rs_ideas["GER_reserves_eastern_workers_enlisted"], "modifier")) == "modifier={industrial_capacity_factory=-0.01}"
      and len(rs_air) == 20 and {b.key for b in rs_bonus.value} == rs_air
      and all(canon_op(b) == b.key + "={build_cost_ic=-0.13 instant=yes}" for b in rs_bonus.value)
      and canon_op(op_get(rs_dec, "visible")) == "visible={date>1944.8.31 has_war=yes}" and op_get(rs_dec, "cost").value == "50"
      and op_get(rs_dec, "fire_only_once").value == "yes"
      and canon_op(op_get(rs_dec, "complete_effect")) == "complete_effect={GER_reserves_luftwaffe_transfer=yes hidden_effect={country_event={id=ger_reserves.4}}}"
      and rs_ifs == [
          "limit={NOT={has_country_flag=GER_reserves_estonia_done} date>1944.2.6 date<1945.1.1 has_war_with=SOV controls_province=3152}",
          "limit={NOT={has_country_flag=GER_reserves_west_done} date>1944.6.5 has_war=yes any_enemy_country={controls_province=11506}}",
          "limit={NOT={has_country_flag=GER_reserves_hungary_done} has_global_flag={flag=arrow_cross_insurgency_happened days>29} "
          "has_war_with=SOV country_exists=HUN HUN={OR={is_in_faction_with=ROOT is_subject_of=ROOT}}}",
          "limit={NOT={has_country_flag=GER_reserves_sweden_done} date>1944.9.27 date<1945.1.1 has_war=yes country_exists=SWE "
          "SWE={NOT={has_war_with=ROOT} NOT={is_in_faction_with=ROOT}} OR={controls_province=6282 controls_province=6389}}",
          "limit={NOT={has_country_flag=GER_reserves_eastern_done} date>1945.1.31 has_war_with=SOV}",
          "limit={NOT={has_country_flag=GER_reserves_roundups_done} date>1944.12.31 has_war=yes OR={has_manpower<200000 "
          + " ".join("NOT={controls_province=%s}" % p for p in RS_RING) + "}}"]
      and all(rs["oa"].count("set_country_flag = GER_reserves_%s_done" % f) == 1 for f in ("estonia", "west", "hungary", "sweden", "eastern", "roundups"))
      and "set_global_flag = arrow_cross_insurgency_happened" in current("mod/events/mod_events.txt").decode("utf-8", "replace")
      and p2s.get("3152") == "812" and p2s.get("11506") == "16" and p2s.get("6282") == "63" and p2s.get("6389") == "58"
      and all(p2s.get(p) == "64" for p in RS_RING)
      and len(rs_defs) == 7 and rs_calls == set(rs_defs)
      and rs_loc.startswith(b"\xef\xbb\xbfl_english:\r\n") and len(rs_keys) == 32 and rs_need == rs_keys,
      f"aircraft types differing: {sorted(rs_air ^ {b.key for b in rs_bonus.value})}")

hf_ev = current("mod/events/GER_homefront_events.txt").decode("ascii")
hf_oa = current("mod/common/on_actions/GER_homefront_on_actions.txt").decode("ascii")
hf_eff = {n.key: n for n in pdx.parse_file("mod/common/scripted_effects/GER_homefront_effects.txt")[0] if n.key}
hf_ideas = {i.key: i for c in pdx.parse_file("mod/common/ideas/GER_homefront_ideas.txt")[0] if c.key == "ideas"
            for g in c.value if g.key == "country" for i in g.value if i.key}
hf_ifs = [canon_op(op_get(b, "limit")) for c in pdx.parse_file("mod/common/on_actions/GER_homefront_on_actions.txt")[0] if c.key == "on_actions"
          for d in c.value if d.key == "on_daily_GER" for b in op_get(d, "effect").value if b.key == "if"]
hf_loc = current("mod/localisation/english/GER_homefront_l_english.yml")
hf_keys = {k.decode() for k in re.findall(rb"^ ([\w.]+):0 ", hf_loc, re.M)}
hf_need = set(re.findall(r"(?:title|desc|name|custom_effect_tooltip) = (ger_homefront[\w.]+)", hf_ev)) | set(hf_ideas) | {i + "_desc" for i in hf_ideas}
hf_defs = re.findall(r"^\tid = (ger_homefront\.\d+)", hf_ev, re.M)
HF_WINDOWS = [("1944.8.14", "1945.1.1", "has_government=fascism"), ("1944.10.13", "1945.1.1", "has_government=fascism"),
              ("1944.11.16", "1945.5.9", "has_government=fascism"), ("1944.12.18", "1945.5.9", "has_war_with=SOV has_character=SOV_andrey_vlasov"),
              ("1945.1.5", "1945.5.9", "has_government=fascism"), ("1945.1.29", "1945.5.9", "has_war_with=SOV 807={is_controlled_by=ROOT}"),
              ("1945.2.11", "1945.5.9", "has_government=fascism"), ("1945.3.4", "1945.5.9", "has_government=fascism")]
def hf_body(name):
    return [canon_op(n) for n in hf_eff[name].value]
check("H  The home front, 1944-45: 8 events, each once from its historical date (15 Aug, 14 Oct, 17 Nov, 19 Dec 1944; 6 Jan, "
      "30 Jan, 12 Feb, 5 Mar 1945) while at war; labour +10,000; Rommel leaves service only if still in it; Flak +7,500 and "
      "+1.5% State AA; Vlasov's air force (only if Vlasov was recruited) -25 PP, +600 (20 per aircraft), 20 Bf 109 G, 10 Ju 87 (named designs); "
      "Volksopfer -25 PP, 1,000 support and 90 days of -10% winter attrition, no rifles; Gustloff -1,500 (while Gotenhafen is ours); women "
      "+5,000, -2% stability; class of 1929 -25% training time, +0.25% recruitable population; 35 texts",
      hf_body("GER_homefront_female_labour_to_50") == ["add_manpower=10000"]
      and hf_body("GER_homefront_rommel_dies") == ["if={limit={has_character=GER_erwin_rommel} retire_character=GER_erwin_rommel}"]
      and hf_body("GER_homefront_flak_auxiliaries") == ["add_manpower=7500", "add_ideas=GER_homefront_flak_auxiliaries"]
      and hf_body("GER_homefront_vlasov_air_force") == ["add_political_power=-25", "add_manpower=600",
          'add_equipment_to_stockpile={type=small_plane_airframe_2 amount=20 producer=GER variant_name="Bf 109 G"}',
          'add_equipment_to_stockpile={type=small_plane_cas_airframe_1 amount=10 producer=GER variant_name="Ju 87"}']
      and all(re.search(r'name = "%s"\s*\r?\n\s*type = %s\r?\n' % (v, t), current("mod/history/countries/GER - Germany.txt").decode("utf-8", "replace"))
              for v, t in (("Bf 109 G", "small_plane_airframe_2"), ("Ju 87", "small_plane_cas_airframe_1")))
      and hf_body("GER_homefront_volksopfer") == ["add_political_power=-25", "add_equipment_to_stockpile={type=support_equipment_1 amount=1000}",
          "add_timed_idea={idea=GER_homefront_volksopfer_clothing days=90}"]
      and canon_op(op_get(hf_ideas["GER_homefront_volksopfer_clothing"], "modifier")) == "modifier={winter_attrition_factor=-0.1}"
      and hf_body("GER_homefront_gustloff") == ["add_manpower=-1500"]
      and hf_body("GER_homefront_volkssturm_women") == ["add_manpower=5000", "add_stability=-0.02"]
      and hf_body("GER_homefront_class_of_1929") == ["add_ideas=GER_homefront_class_of_1929"]
      and canon_op(op_get(hf_ideas["GER_homefront_flak_auxiliaries"], "modifier")) == "modifier={static_anti_air_damage_factor=0.015 static_anti_air_hit_chance_factor=0.015}"
      and canon_op(op_get(hf_ideas["GER_homefront_class_of_1929"], "modifier")) == "modifier={training_time_factor=-0.25 conscription=0.0025}"
      and hf_ifs == ["limit={NOT={has_country_flag=GER_homefront_%d_done} date>%s date<%s has_war=yes %s}" % (i + 1, a, b, c)
                     for i, (a, b, c) in enumerate(HF_WINDOWS)]
      and all(hf_oa.count("set_country_flag = GER_homefront_%d_done" % (i + 1)) == 1 for i in range(8))
      and len(hf_defs) == 8 and set(re.findall(r"country_event = \{ id = (ger_homefront\.\d+)", hf_oa)) == set(hf_defs)
      and hf_loc.startswith(b"\xef\xbb\xbfl_english:\r\n") and len(hf_keys) == 35 and hf_need == hf_keys
      and "immediate = {\r\n\t\thidden_effect = { set_country_flag = GER_1945_courland_offered }" in op["ev"],
      str([l for l, (a, b, c) in zip(hf_ifs, HF_WINDOWS) if a not in l]))

def autonomy_targets(nodes):
    return [c.value for n, _ in pdx.walk(nodes) if n.key == "set_autonomy" and n.is_block() for c in n.value if c.key == "target"]
uk_eng = pdx.parse_file("mod/history/countries/ENG - Britain.txt")[0]
uk_faction = [n.value for n in uk_eng if n.key == "add_to_faction"]
uk_doa = pdx.parse_file("mod/common/on_actions/do_on_actions.txt")[0]
uk_startup = [(parents[-1].key, canon_op(n)) for n, parents in pdx.walk(uk_doa)
              if n.key in ("become_exiled_in", "transfer_state") and [p.key for p in parents[:3]] == ["on_actions", "on_startup", "effect"]]
check("E  UK start: the countries that have no land on 1 Jan 1944 (Poland, Yugoslavia, the Philippines, Belgium) are not put in the "
      "Allied faction in history, Burma and the Philippines are not made colonies there, Yugoslavia is not made an exile there; "
      "on_startup makes Poland, Yugoslavia and Burma exiles in the UK (legitimacy 50, 30, 50) and the Philippines in the USA (50), "
      "and still moves Singapore to Japan",
      not {"POL", "YUG", "PHI", "BEL"} & set(uk_faction) and {"ENG", "USA", "RAJ", "MAL"} <= set(uk_faction)
      and "BRM" not in autonomy_targets(uk_eng)
      and "PHI" not in autonomy_targets(pdx.parse_file("mod/history/countries/USA - USA.txt")[0])
      and not [n for n, _ in pdx.walk(pdx.parse_file("mod/history/countries/YUG - Yugoslavia.txt")[0]) if n.key == "become_exiled_in"]
      and {("POL", "become_exiled_in={target=ENG legitimacy=50}"), ("YUG", "become_exiled_in={target=ENG legitimacy=30}"),
           ("BRM", "become_exiled_in={target=ENG legitimacy=50}"), ("PHI", "become_exiled_in={target=USA legitimacy=50}"),
           ("ETH", "become_exiled_in={target=ENG legitimacy=60}"), ("ICE", "become_exiled_in={target=ENG legitimacy=65}"),
           ("JAP", "transfer_state=336")} == set(uk_startup),
      f"faction: {uk_faction}; on_startup: {uk_startup}")

ms_dec = {d.key: (c.key, d) for c in pdx.parse_file("mod/common/decisions/GER_measures_decisions.txt")[0] if c.key for d in c.value if d.key}
ms_eff = {n.key: n for n in pdx.parse_file("mod/common/scripted_effects/GER_measures_effects.txt")[0] if n.key}
ms_ev = current("mod/events/GER_measures_events.txt").decode("ascii")
ms_idea = next(i for c in pdx.parse_file("mod/common/ideas/GER_measures_ideas.txt")[0] if c.key == "ideas"
               for g in c.value if g.key == "country" for i in g.value if i.key)
ms_loc = current("mod/localisation/english/GER_measures_l_english.yml")
ms_keys = {k.decode() for k in re.findall(rb"^ ([\w.]+):0 ", ms_loc, re.M)}
ms_need = (set(ms_dec) | {d + "_desc" for d in ms_dec} | {ms_idea.key, ms_idea.key + "_desc"}
           | set(re.findall(r"(?:title|desc|name|custom_effect_tooltip) = (ger_measures[\w.]+)", ms_ev))
           | set(re.findall(r"custom_effect_tooltip = (\w+)", current("mod/common/decisions/GER_measures_decisions.txt").decode("ascii"))))
ms_tokens = [l.strip() for l in current("mod/common/synchronized_dynamic_tokens/GER_equipment_tokens.txt").decode("ascii").splitlines()
             if l.strip() and not l.startswith("#")]
ms_read = set(re.findall(r"num_equipment@(\w+)", current("mod/common/scripted_effects/GER_measures_effects.txt").decode("ascii")
                         + current("mod/common/scripted_effects/GER_1945_operations_effects.txt").decode("ascii")))
def ms_body(name):
    return [canon_op(n) for n in ms_eff[name].value]
def ms_part(dec, part):
    return canon_op(op_get(ms_dec[dec][1], part))
ms_pay = ms_eff["GER_measures_konr_pay"].value
ms_pay_needs = [int(c.value) for n in ms_pay if n.key == "set_temp_variable" for c in n.value if c.key == "GER_measures_need"]
ms_pay_types = [op_get(n, "type").value for n, _ in pdx.walk(ms_pay) if n.key == "add_equipment_to_stockpile"]
ms_units = [op_get(n, "division").value for k in ("GER_measures_konr_4th_division", "GER_measures_konr_5th_division")
            for n, _ in pdx.walk(ms_eff[k].value) if n.key == "create_unit"]
MS_RIFLES = [("50", "GER"), ("40", "SOV"), ("5", "ITA"), ("5", "FRA")]  # rolled per division (section 18)
def ms_roll(k):
    """[(weight, rifle maker, guard)] of the random rifle roll that raises a KONR division."""
    rl = next(n for n, _ in pdx.walk(ms_eff[k].value) if n.key == "random_list")
    return [(e.key, re.search(r'owner = \\"(\w+)\\"', op_get(next(n for n, _ in pdx.walk(e.value) if n.key == "create_unit"), "division").value).group(1),
             canon_op(op_get(e, "modifier")) if op_get(e, "modifier") else None) for e in rl.value if e.key != "seed"]
check("M  Five war measures: KONR (collaborationist tab, from 27 Feb 1945, needs the author's ROA template): a choice of 2 divisions "
      "(4th at once, 5th after 60 days; low experience, 30% equipment, old rifles rolled per division: German 50, captured Soviet 40, "
      "Italian 5, French 5; each paying 453/9/4 infantry/support/artillery type by type, only with that in stock) or 12,000 manpower; "
      "railway repair 90 days +30% / +20% / -10%; student companies +20,000 and a spirit -5% research, -1% stability, with a popup; "
      "weapons appeal 25 PP, from 7 Jan 1945 (the Volksopfer), +2,000 Basic Infantry Equipment; confiscation (only after the appeal, "
      "from 29 Jan 1945) +7,500 and -1% stability; 50 PP otherwise, each once; every equipment type read is in the synchronized "
      "token list; 3 events, 21 texts",
      {d: (c, ms_part(d, "cost"), ms_part(d, "fire_only_once")) for d, (c, _) in ms_dec.items()}
          == {"GER_measures_konr_expand": ("collaborationist_formation", "cost=50", "fire_only_once=yes"),
              "GER_measures_railway_repair": ("war_measures", "cost=50", "fire_only_once=yes"),
              "GER_measures_student_companies": ("war_measures", "cost=50", "fire_only_once=yes"),
              "GER_measures_weapons_appeal": ("war_measures", "cost=25", "fire_only_once=yes"),
              "GER_measures_weapons_confiscation": ("war_measures", "cost=50", "fire_only_once=yes")}
      and ms_part("GER_measures_konr_expand", "visible") == 'visible={date>1945.2.26 has_war_with=SOV has_capitulated=no has_template="Russische Befreiungsarmee"}'
      and ms_part("GER_measures_konr_expand", "available") == 'available={has_war_with=SOV has_template="Russische Befreiungsarmee"}'
      and "country_event={id=ger_measures.1}" in ms_part("GER_measures_konr_expand", "complete_effect")
      and ms_part("GER_measures_railway_repair", "visible").startswith("visible={date>1944.8.31 ")
      and ms_part("GER_measures_railway_repair", "days_remove") == "days_remove=90"
      and ms_part("GER_measures_railway_repair", "modifier") == ("modifier={repair_speed_rail_way_factor=0.30 "
                                                                 "repair_speed_infrastructure_factor=0.20 production_speed_buildings_factor=-0.10}")
      and ms_part("GER_measures_student_companies", "visible").startswith("visible={date>1944.9.30 ")
      and ms_part("GER_measures_student_companies", "complete_effect")
          == "complete_effect={GER_measures_student_companies=yes hidden_effect={country_event={id=ger_measures.3}}}"
      and ms_part("GER_measures_weapons_appeal", "visible").startswith("visible={date>1945.1.6 ")
      and ms_part("GER_measures_weapons_appeal", "complete_effect")
          == "complete_effect={GER_measures_weapons_appeal=yes hidden_effect={set_country_flag=GER_measures_weapons_appealed}}"
      and ms_part("GER_measures_weapons_confiscation", "visible")
          == "visible={date>1945.1.28 has_war=yes has_capitulated=no has_country_flag=GER_measures_weapons_appealed}"
      and ms_body("GER_measures_konr_divisions") == ["GER_measures_konr_pay=yes", "GER_measures_konr_4th_division=yes",
                                                      "hidden_effect={country_event={id=ger_measures.2 days=60}}"]
      and ms_pay_needs == [453, 9, 4]
      and ms_pay_types == [f"infantry_equipment_{i}" for i in range(4)] + ["support_equipment_1"] + [f"artillery_equipment_{i}" for i in (1, 2, 3)]
      and ms_units == [f'"name = \\"{n}th KONR Infantry Division\\" division_template = \\"Russische Befreiungsarmee\\" start_experience_factor = 0.1 '
                       f'start_equipment_factor = 0.3 force_equipment_variants = {{ infantry_equipment_0 = {{ owner = \\"{o}\\" }} }}"'
                       for n in (4, 5) for _, o in MS_RIFLES]
      and all(ms_roll(k) == [(w, o, None if o == "GER" else f"modifier={{factor=0 NOT={{country_exists={o}}}}}") for w, o in MS_RIFLES]
              for k in ("GER_measures_konr_4th_division", "GER_measures_konr_5th_division"))
      and all("prioritize={52 50}" in canon_op(ms_eff[k]) and "owner=ROOT" in canon_op(ms_eff[k])
              for k in ("GER_measures_konr_4th_division", "GER_measures_konr_5th_division"))
      and re.sub(r"\s+", " ", ms_ev).count("trigger = { has_equipment = { infantry_equipment > 452 } has_equipment = { support_equipment > 8 } "
                                           "has_equipment = { artillery_equipment > 3 } }") == 1
      and re.sub(r"\s+", " ", ms_ev).count("limit = { has_equipment = { infantry_equipment > 452 } has_equipment = { support_equipment > 8 } "
                                           "has_equipment = { artillery_equipment > 3 } } GER_measures_konr_pay = yes GER_measures_konr_5th_division = yes") == 1
      and ms_body("GER_measures_konr_manpower") == ["add_manpower=12000"]
      and ms_body("GER_measures_student_companies") == ["add_manpower=20000", "add_ideas=GER_measures_student_companies_spirit"]
      and ms_idea.key == "GER_measures_student_companies_spirit"
      and canon_op(op_get(ms_idea, "modifier")) == "modifier={research_speed_factor=-0.05 stability_factor=-0.01}"
      and ms_body("GER_measures_weapons_appeal") == ["add_equipment_to_stockpile={type=infantry_equipment_0 amount=2000}"]
      and ms_body("GER_measures_weapons_confiscation") == ["add_equipment_to_stockpile={type=infantry_equipment_0 amount=7500}", "add_stability=-0.01"]
      and ms_read == set(ms_tokens) and len(ms_tokens) == 8
      and re.findall(r"^\tid = (ger_measures\.\d+)", ms_ev, re.M) == ["ger_measures.1", "ger_measures.2", "ger_measures.3"]
      and ms_loc.startswith(b"\xef\xbb\xbfl_english:\r\n") and len(ms_keys) == 21 and ms_need == ms_keys
      and sf.get("52", [""])[0].endswith("52-Wuttemberg.txt") and sf.get("50", [""])[0].endswith("50-Baden.txt"),
      f"texts missing: {sorted(ms_need - ms_keys)}; extra: {sorted(ms_keys - ms_need)}; tokens: {sorted(set(ms_tokens) ^ ms_read)}")

def eff_bodies(path):
    return {n.key: [canon_op(c) for c in n.value] for n in pdx.parse_file(path)[0] if n.key}
def daily_ifs(path, oa="on_daily_GER"):
    """[(limit, flags set, events fired)] of each top-level if in an on_action's effect."""
    out = []
    for c in pdx.parse_file(path)[0]:
        if c.key != "on_actions":
            continue
        for d in c.value:
            if d.key != oa:
                continue
            for blk in op_get(d, "effect").value:
                if blk.key == "if":
                    nodes = [n for n, _ in pdx.walk(blk.value)]
                    out.append((canon_op(op_get(blk, "limit")),
                                [n.value for n in nodes if n.key == "set_country_flag"],
                                [op_get(n, "id").value for n in nodes if n.key == "country_event"]))
    return out
def loc_keys(path):
    raw = current(path)
    return raw.startswith(b"\xef\xbb\xbfl_english:\r\n"), {k.decode() for k in re.findall(rb"^ ([\w.]+):0 ", raw, re.M)}
BASE_PICS = set(re.findall(r'name\s*=\s*"(GFX_report_event_\w+)"', "".join(
    open(os.path.join(V, "interface", f), encoding="utf-8", errors="replace").read() for f in os.listdir(os.path.join(V, "interface")) if f.endswith(".gfx"))))
def photo_ok(name, gfx):
    """A new event picture: sprite GFX_<name> in the given .gfx, a 210 x 176 DDS with the same header as the author's own pictures."""
    g, dds = current(gfx).decode("ascii"), current(f"mod/gfx/events/{name}.dds")
    return (f'name = "GFX_{name}"' in g and f'texturefile = "gfx/events/{name}.dds"' in g
            and len(dds) == 128 + 210 * 176 * 4 and dds[:128] == current("mod/gfx/events/report_event_rhine_defence.dds")[:128])
lg_eff = eff_bodies("mod/common/scripted_effects/GER_legions_effects.txt")
lg_ifs = daily_ifs("mod/common/on_actions/GER_legions_on_actions.txt")
lg_ev = current("mod/events/GER_legions_events.txt").decode("ascii")
lg_bom, lg_keys = loc_keys("mod/localisation/english/GER_legions_l_english.yml")
lg_need = set(re.findall(r"(?:title|desc|name|custom_effect_tooltip|text) = (ger_legions[\w.]+)", lg_ev))
LG_LIMITS = [
    "limit={NOT={has_country_flag=GER_legions_1_done} date>1944.8.14 date<1945.5.9 has_war=yes OR={has_war_with=ENG has_war_with=USA} NOT={controls_province=11506}}",
    "limit={NOT={has_country_flag=GER_legions_2_done} date>1944.10.4 date<1945.5.9 has_war=yes country_exists=CRO}",
    "limit={NOT={has_country_flag=GER_legions_3_done} date>1944.12.29 date<1945.5.9 has_war_with=SOV}",
    "limit={NOT={has_country_flag=GER_legions_4_done} date>1944.2.16 date<1945.1.1 has_war_with=SOV}",
    "limit={NOT={has_country_flag=GER_legions_5_done} date>1944.8.9 date<1945.1.1 has_war_with=SOV OR={813={is_controlled_by=ROOT} 812={is_controlled_by=ROOT}}}",
    "limit={NOT={has_country_flag=GER_legions_6_done} date>1944.8.3 date<1945.1.1 has_war_with=SOV controls_province=3544 92={controller={has_war_with=ROOT}}}"]
check("L  Six flavour events, each once on or after its historical date: the Indian Legion (15 Aug 1944, an enemy holds Paris; no effect), "
      "the Handschar (5 Oct 1944, Croatia exists; -2,000 manpower), the Eastern Legions (30 Dec 1944; +3,500), Wiking at Cherkassy "
      "(17 Feb 1944; broke out or held, by who holds state 203; +10 army experience, +2% war support), Nordland at the Blue Hills "
      "(10 Aug 1944, northern Estonia held; the same), Wiking before Warsaw (4 Aug 1944, Warsaw held, the enemy holds Lublin; the same, "
      "with Oscar's photo); the other pictures from the base game; 20 texts",
      lg_eff == {"GER_legions_handschar": ["add_manpower=-2000"], "GER_legions_eastern_legions": ["add_manpower=3500"],
                 "GER_legions_wiking": ["army_experience=10", "add_war_support=0.02"],
                 "GER_legions_nordland": ["army_experience=10", "add_war_support=0.02"]}
      and [l for l, _, _ in lg_ifs] == LG_LIMITS
      and [(f, e) for _, f, e in lg_ifs] == [([f"GER_legions_{i}_done"], [f"ger_legions.{i}"]) for i in range(1, 7)]
      and re.findall(r"^\tid = (ger_legions\.\d+)", lg_ev, re.M) == [f"ger_legions.{i}" for i in range(1, 7)]
      and re.sub(r"\s+", " ", lg_ev).count("desc = { text = ger_legions.4.d.breakout trigger = { NOT = { 203 = { is_controlled_by = ROOT } } } } "
                                          "desc = { text = ger_legions.4.d.held trigger = { 203 = { is_controlled_by = ROOT } } }") == 1
      and re.sub(r"\s+", " ", lg_ev).count("option = { name = ger_legions.1.a custom_effect_tooltip = ger_legions.1.a.tt }") == 1
      and all(f"GER_legions_{k} = yes" in lg_ev for k in ("handschar", "eastern_legions", "wiking", "nordland")) and lg_ev.count("GER_legions_wiking = yes") == 2
      and re.findall(r"picture = (GFX_\w+)", lg_ev)[5] == "GFX_report_event_GER_wiking_panzer"
      and set(re.findall(r"picture = (GFX_\w+)", lg_ev)[:5]) <= BASE_PICS and photo_ok("report_event_GER_wiking_panzer", "mod/interface/GER_legions.gfx")
      and p2s.get("11506") is not None and p2s.get("11424") == "203" and p2s.get("4640") == "813" and p2s.get("3152") == "812"
      and p2s.get("3544") == "10" and p2s.get("11399") == "92"
      and lg_bom and len(lg_keys) == 20 and lg_need == lg_keys,
      f"limits differing: {[l for l in [x for x, _, _ in lg_ifs] if l not in LG_LIMITS]}; texts: {sorted(lg_need ^ lg_keys)}")

rm_eff = eff_bodies("mod/common/scripted_effects/GER_remagen_effects.txt")
rm_oa = current("mod/common/on_actions/GER_remagen_on_actions.txt").decode("ascii")
rm_ifs = daily_ifs("mod/common/on_actions/GER_remagen_on_actions.txt")
rm_ev = current("mod/events/GER_remagen_events.txt").decode("ascii")
rm_gfx = current("mod/interface/GER_remagen.gfx").decode("ascii")
rm_dds = current("mod/gfx/events/report_event_GER_remagen_bridge.dds")
rm_ref = current("mod/gfx/events/report_event_rhine_defence.dds")
rm_bom, rm_keys = loc_keys("mod/localisation/english/GER_remagen_l_english.yml")
rm_loc = current("mod/localisation/english/GER_remagen_l_english.yml").decode("utf-8")
rm_need = set(re.findall(r"(?:title|desc|name|custom_effect_tooltip) = (ger_remagen[\w.]+)", rm_ev))
check("X  The bridge at Remagen: fires once when a western enemy (not the Soviet Union) holds province 529 (the east bank opposite "
      "Remagen, state 51; the west bank 11494 is in state 42), naming the captor; option A -25 PP, -2,000 fuel, -2% stability and the "
      "collapse 10 days later (railway in 529 damaged by 2), option B nothing; the picture is a 210 x 176 DDS in the same format as the "
      "author's own; 10 texts",
      [l for l, _, _ in rm_ifs] == ["limit={NOT={has_country_flag=GER_remagen_done} has_war=yes NOT={controls_province=529} "
                                    "any_country={controls_province=529 has_war_with=ROOT NOT={original_tag=SOV}}}"]
      and [(f, e) for _, f, e in rm_ifs] == [(["GER_remagen_done"], ["ger_remagen.1"])]
      and "save_global_event_target_as = GER_remagen_captor" in rm_oa and "[GER_remagen_captor.GetAdjective]" in rm_loc
      and rm_eff == {"GER_remagen_destroy_the_bridge": ["add_political_power=-25", "add_fuel=-2000", "add_stability=-0.02",
                                                        "hidden_effect={country_event={id=ger_remagen.2 days=10}}"],
                     "GER_remagen_collapse": ["damage_building={type=rail_way province=529 damage=2}"]}
      and re.findall(r"^\tid = (ger_remagen\.\d+)", rm_ev, re.M) == ["ger_remagen.1", "ger_remagen.2"]
      and rm_ev.count("GER_remagen_destroy_the_bridge = yes") == 1 and "hidden_effect = { GER_remagen_collapse = yes }" in rm_ev
      and rm_ev.count("picture = GFX_report_event_GER_remagen_bridge") == 2
      and 'name = "GFX_report_event_GER_remagen_bridge"' in rm_gfx and 'texturefile = "gfx/events/report_event_GER_remagen_bridge.dds"' in rm_gfx
      and len(rm_dds) == 128 + 210 * 176 * 4 and rm_dds[:128] == rm_ref[:128]
      and p2s.get("529") == "51" and p2s.get("11494") == "42"
      and rm_bom and len(rm_keys) == 10 and rm_need == rm_keys,
      f"texts: {sorted(rm_need ^ rm_keys)}")

def flat(path):
    return re.sub(r"\s+", " ", re.sub(r"#[^\n]*", "", current(path).decode("utf-8-sig", errors="replace")))
bq_ifs = daily_ifs("mod/common/on_actions/GER_bomb_on_actions.txt")
bq_ev = flat("mod/events/GER_bomb_events.txt")
bq_bom, bq_keys = loc_keys("mod/localisation/english/GER_bomb_l_english.yml")
check("Q  The first German atomic bomb: fires once, the first day Germany has a bomb in its stockpile (num_of_nukes > 0); flavour only (no "
      "effect); Oscar's alt-history illustration, described as such in its .gfx; 3 texts",
      [(l, f, e) for l, f, e in bq_ifs] == [("limit={NOT={has_country_flag=GER_bomb_done} num_of_nukes>0}", ["GER_bomb_done"], ["ger_bomb.1"])]
      and re.findall(r"id = (ger_bomb\.\d+)", bq_ev) == ["ger_bomb.1"]
      and "picture = GFX_report_event_GER_first_bomb is_triggered_only = yes option = { name = ger_bomb.1.a } }" in bq_ev
      and photo_ok("report_event_GER_first_bomb", "mod/interface/GER_bomb.gfx") and b"not a historical photograph" in current("mod/interface/GER_bomb.gfx")
      and bq_bom and bq_keys == {"ger_bomb.1.t", "ger_bomb.1.d", "ger_bomb.1.a"})

ld_ifs = daily_ifs("mod/common/on_actions/GER_leningrad_on_actions.txt")
ld_ev = flat("mod/events/GER_leningrad_events.txt")
ld_bom, ld_keys = loc_keys("mod/localisation/english/GER_leningrad_l_english.yml")
ld_news = flat("mod/events/NewsEvents.txt")
check("D  Leningrad taken: fires once, from 1944, the first day we hold the city itself (province 3151, state 195) at war with the Soviet "
      "Union (the game can't tell where a battle is, so the attack itself can't be the trigger); the game's own news event news.103 "
      "also fires; flavour only; Oscar's alt-history illustration, described as such; 3 texts",
      [(l, f, e) for l, f, e in ld_ifs] == [("limit={NOT={has_country_flag=GER_leningrad_done} date>1943.12.31 has_war_with=SOV "
                                              "controls_province=3151}", ["GER_leningrad_done"], ["ger_leningrad.1"])]
      and p2s.get("3151") == "195"
      and "id = news.103" in ld_news and "195 = { is_controlled_by = GER }" in ld_news
      and re.findall(r"id = (ger_leningrad\.\d+)", ld_ev) == ["ger_leningrad.1"]
      and "picture = GFX_report_event_GER_leningrad is_triggered_only = yes option = { name = ger_leningrad.1.a } }" in ld_ev
      and photo_ok("report_event_GER_leningrad", "mod/interface/GER_leningrad.gfx") and b"not a historical photograph" in current("mod/interface/GER_leningrad.gfx")
      and ld_bom and ld_keys == {"ger_leningrad.1.t", "ger_leningrad.1.d", "ger_leningrad.1.a"})

cr_ifs = daily_ifs("mod/common/on_actions/GER_crimea_on_actions.txt")
cr_eff = flat("mod/common/scripted_effects/GER_crimea_effects.txt")
cr_dec = flat("mod/common/decisions/GER_crimea_decisions.txt")
cr_ev = flat("mod/events/GER_crimea_events.txt")
cr_bom, cr_keys = loc_keys("mod/localisation/english/GER_crimea_l_english.yml")
cr_need = set(re.findall(r"(?:title|desc|name|custom_effect_tooltip|tooltip) = ((?:ger|GER)_crimea[\w.]+)", cr_ev + cr_dec)) | {
    "GER_crimea_evacuation", "GER_crimea_evacuation_desc", "GER_crimea_fortress"}
cr_mods = {n.key: [canon_op(c) for c in n.value] for f in ("GER_crimea_modifiers.txt", "GER_1945_operations_modifiers.txt")
           for n in pdx.parse_file("mod/common/modifiers/" + f)[0] if n.key}
check("C  The Crimea: the popup fires once when we hold Sevastopol (3686) with divisions in the Crimea (137) and an enemy holds Perekop (568; "
      "true on 1 Jan 1944); evacuate (the popup starts the decision at once: 50 PP, 30 days, Sevastopol held: German divisions to "
      "Constanta 971, else Odessa 192, Mykolaiv 197, else the capital; allied Romanians with them) or hold (Fortress Sevastopol, the "
      "author's Festung values as for Courland, removed when Sevastopol falls or on evacuation; the decision stays available); AI 25/75, "
      "and the AI never evacuates after holding; 14 texts",
      [(l, f, e) for l, f, e in cr_ifs] == [
          ("limit={NOT={has_country_flag=GER_crimea_offered} has_war=yes controls_province=3686 divisions_in_state={state=137 size>0} "
           "any_country={controls_province=568 has_war_with=ROOT}}", ["GER_crimea_offered"], ["ger_crimea.1"]),
          ("limit={has_country_flag=GER_crimea_fortress NOT={controls_province=3686}}", [], [])]
      and p2s.get("3686") == "137" and p2s.get("568") == "196" and p2s.get("657") == "971"
      and re.findall(r"limit = \{ (\d+) = \{ controller = \{ OR = \{ tag = ROOT is_in_faction_with = ROOT \} \} \} \} "
                     r"137 = \{ teleport_armies = \{ to_state = (\d+) limit = \{ original_tag = GER \}", cr_eff) == [
          ("971", "971"), ("192", "192"), ("197", "197")]
      and "else = { 137 = { teleport_armies = { limit = { original_tag = GER } } } }" in cr_eff
      and "limit = { country_exists = ROM ROM = { is_in_faction_with = ROOT } }" in cr_eff
      and "137 = { teleport_armies = { to_state = 971 limit = { original_tag = ROM } } }" in cr_eff
      and "137 = { teleport_armies = { limit = { original_tag = ROM } } }" in cr_eff
      and cr_eff.rstrip().endswith("GER_crimea_fortress_off = yes }")
      and "137 = { add_province_modifier = { static_modifiers = { GER_crimea_fortress } province = { id = 3686 } } }" in cr_eff
      and "137 = { remove_province_modifier = { static_modifiers = { GER_crimea_fortress } province = { id = 3686 } } }" in cr_eff
      and cr_mods["GER_crimea_fortress"] == cr_mods["GER_1945_courland_fortress"]
      and "controls_province = 3686 } divisions_in_state = { state = 137 size > 0 } } cost = 50 days_remove = 30 fire_only_once = yes" in cr_dec
      and "remove_effect = { hidden_effect = { GER_crimea_evacuate = yes set_country_flag = GER_crimea_evacuated country_event = { id = ger_crimea.2 } } }" in cr_dec
      and "cancel_trigger = { NOT = { controls_province = 3686 } }" in cr_dec
      and re.findall(r"id = (ger_crimea\.\d+)", cr_ev) == ["ger_crimea.1", "ger_crimea.2"]
      and "immediate = { hidden_effect = { set_country_flag = GER_crimea_offered } }" in cr_ev
      and "ai_chance = { base = 25 } set_country_flag = GER_crimea_evacuate_chosen activate_decision = GER_crimea_evacuation" in cr_ev
      and "political_power" not in cr_ev and "ai_will_do = { factor = 0 }" in cr_dec
      and "ai_chance = { base = 75 } custom_effect_tooltip = ger_crimea.1.b.tt hidden_effect = { GER_crimea_fortress_on = yes }" in cr_ev
      and cr_bom and len(cr_keys) == 14 and cr_need == cr_keys,
      f"texts: {sorted(cr_need ^ cr_keys)}")

check("OL The author's D-Day decisions (common/decisions/Allies_1944.txt) are his own, byte for byte (Codex's change was reverted at Oscar's request)",
      git("rev-parse", "HEAD:mod/common/decisions/Allies_1944.txt") == git("rev-parse", f"{BASE}:mod/common/decisions/Allies_1944.txt"))

import check_dday
dd_cases = check_dday.scenarios(current("mod/common/on_actions/GER_dday_on_actions.txt").decode()) + check_dday.calibration(current("mod/common/on_actions/GER_dday_on_actions.txt").decode())
dd_ifs = daily_ifs("mod/common/on_actions/GER_dday_on_actions.txt")
dd_oa = flat("mod/common/on_actions/GER_dday_on_actions.txt")
dd_ev = flat("mod/events/GER_dday_events.txt")
dd_bom, dd_keys = loc_keys("mod/localisation/english/GER_dday_l_english.yml")
dd_news = flat("mod/events/mod_news.txt")
DD_COAST = ("15", "14", "29", "6")
dd_states = {s: flat("mod/history/states/" + next(f for f in os.listdir("mod/history/states") if f.split("-")[0].strip() == s)) for s in DD_COAST}
dd_provinces = {}
for sid in DD_COAST:
    path = "mod/history/states/" + next(f for f in os.listdir("mod/history/states") if f.split("-")[0].strip() == sid)
    state = next(n for n in pdx.parse_file(path)[0] if n.key == "state")
    dd_provinces[sid] = [n.value for n in next(n for n in state.value if n.key == "provinces").value]
check("Y  The invasion beaten back: after 1 June 1944, at war with the UK or the USA, a landing is noted when a western Allied enemy holds part of "
      "Normandy, Brittany, Nord-Pas-de-Calais or Flanders (the states the author's own D-Day news event watches; all German at the "
      "start); once we hold all four again, the event follows one day later; once only; flavour only; Oscar's picture; 3 texts",
      [(l, f, e) for l, f, e in dd_ifs] == [
          ("limit={NOT={has_country_flag=GER_dday_landed} date>1944.5.31 OR={has_war_with=ENG has_war_with=USA} any_enemy_country={"
           + "OR={tag=ENG tag=USA is_in_faction_with=ENG is_in_faction_with=USA} OR={"
           + " ".join("controls_province=" + p for s in DD_COAST for p in dd_provinces[s]) + "}}}", ["GER_dday_landed"], []),
          ("limit={has_country_flag=GER_dday_landed NOT={has_country_flag=GER_dday_repelled} "
           + " ".join(f"{s}={{is_fully_controlled_by=ROOT}}" for s in DD_COAST) + "}", ["GER_dday_repelled"], ["ger_dday.1"])]
      and "country_event = { id = ger_dday.1 days = 1 }" in dd_oa
      and all(f"{s} = {{ is_fully_controlled_by = GER }}" in dd_news for s in DD_COAST) and "id = mod.news.1" in dd_news
      and all("owner = GER controller = GER" in t for t in dd_states.values()) and p2s.get("6449") == "15"
      and re.findall(r"id = (ger_dday\.\d+)", dd_ev) == ["ger_dday.1"]
      and "picture = GFX_report_event_GER_dday_repelled is_triggered_only = yes option = { name = ger_dday.1.a } }" in dd_ev
      and photo_ok("report_event_GER_dday_repelled", "mod/interface/GER_dday.gfx")
      and dd_bom and dd_keys == {"ger_dday.1.t", "ger_dday.1.d", "ger_dday.1.a"}
      and all(ok for _, ok in dd_cases), f"{sum(ok for _, ok in dd_cases)}/{len(dd_cases)} scenarios")

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
