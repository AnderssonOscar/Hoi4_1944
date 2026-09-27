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
changed = {tuple(l.decode().split("\t", 1)) for l in git("diff", "--name-status", BASE, "HEAD", "--", "mod").splitlines()}
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
for path, ok_line in allowed.items():
    diff = git("diff", "-U0", "--no-color", BASE, "HEAD", "--", path).decode("utf-8", "replace").replace("\r", "")
    removed = [l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    bad = [l for l in removed if not ok_line(l)]
    check(f"{path[4:]}: {len(removed)} removed line(s), all expected", not bad, "; ".join(bad[:3]))

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
check("F  Slovak uprising: event with its picture, fired once on 29 Aug 1944 for SLO + GER, -3000 manpower, 4 one-line texts with BOM",
      evn is not None and any(c.key == "id" and c.value == "slovak.uprising.1" for c in evn.value)
      and any(c.key == "picture" and c.value == "GFX_report_event_czech_soldiers_02" for c in evn.value)
      and all(s in oa for s in (b"on_daily_SLO", b"date > 1944.8.28", b"SLO_slovak_uprising", b"add_manpower = -3000",
                                b"GER = { country_event = { id = slovak.uprising.1 } }"))
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
