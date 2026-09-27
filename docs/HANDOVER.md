# Handover: 1944 - Downfall bug-fix project

For the next assistant (ChatGPT or another AI) continuing this work.
Written by Claude on 2026-09-27. Read this first, then `docs/INVESTIGATION.md`.

---

## 1. The situation

Oscar's brother made the Hearts of Iron IV mod **1944 - Downfall** (Steam
Workshop id 3070639276; his Steam/GitHub name is "gastav3"). He has no time
to maintain it, and players report crashes. Oscar is trying to fix it with
AI help.

**The brother distrusts AI and expects it to fail.** The work only helps if:

- every claim has evidence he can check himself (file, line number, reason),
- every change is small, separate, and easy to review,
- uncertainty is stated honestly. "Suspected" is not "fixed".

Overclaiming is the quickest way to lose his trust. Record false alarms
instead of hiding them. Section 3 of INVESTIGATION.md does this on purpose.

## 2. Status

- **Final state (2026-09-27):** two bug fixes (A, G) and the update to HOI4
  1.19.3 are applied, plus one flavor event (Slovak National Uprising, commit
  `7de1ce8`, CHANGELOG §4): 27 files differ from the Workshop version (21
  edited, 3 deleted, 3 new). Then the Nero Decree and Werwolf decisions (commit
  `76a0d54`, CHANGELOG §5, 6 new files; loads cleanly but **not play-tested**, because
  screen control was declined): now 33 files differ (9 new). Every change is its own commit; see `docs/CHANGELOG.md`.
  Git tags: `final-2026-09-27` = the first package; `final-2026-09-27-v2` =
  the current package (adds the Slovak event and Nero/Werwolf).
- **Verified:** `python tools/verify_update.py` gives 48/48 PASS
  (docs/VERIFICATION.md). That covers integrity, only the intended files
  changed, the author's content byte-identical, and all fixes present. The
  game's own error.log went from 282 to 115 lines (base game alone: 1), and
  the game install is the official 1.19.3 (checksum 5632).
- **Not verified:** actual play (the Ichi-Go fix, the other crash reports),
  playing without some DLCs, and 3 heavily edited files not merged with
  1.19.3 (GER decisions, germany focus tree, artillery techs).
- **Package for the author:** `1944-Downfall-update-1.19.3.zip` on Oscar's
  desktop, containing the final mod folder, patches (one per commit), docs
  and tools. Start page: `docs/READ-ME-FIRST.md`.
- You can run the game's own error check yourself: start `hoi4.exe -debug`
  with the mod in `dlc_load.json`, wait for the main menu, and read
  `logs/error.log`. Back up `dlc_load.json` first and restore it afterwards.
  Writing `disabled_dlcs` there does **not** disable DLCs. The logs from
  2026-09-27 are in `docs/game-logs/`.
- A local test entry, "1944 - Downfall (local fixes)", points the game at this
  project's `mod\` folder (see CHANGELOG.md, "How to test in game").
- The five player reports have been investigated as far as reading the code
  allows. Results are in `docs/INVESTIGATION.md`.
- **Four reports have no cause found** (Bulgaria switch, Romania 12-day
  decision, Volkssturm focus, UK). They need a crash report from the game.
  One report ("D-Day seems broken") needs a proper description first.
- Added on Oscar's request: the Slovak uprising event, Nero Decree and
  Werwolf, and the Volkssturm redesign (CHANGELOG sections 4-6). They load
  cleanly; none has been play-tested yet.

## 3. Where everything is

| What | Path |
|---|---|
| Project (git repo) | `C:\Users\Ander\Desktop\Projects\1944-Downfall` |
| Mod working copy | `...\1944-Downfall\mod\` (baseline commit `253cea1` = Workshop version, byte-identical, checked on all 914 files) |
| Findings log | `...\1944-Downfall\docs\INVESTIGATION.md` |
| This file | `...\1944-Downfall\docs\HANDOVER.md` |
| Check scripts | `...\1944-Downfall\tools\` (Python 3.12, run as `python`) |
| Steam Workshop copy (**never edit**) | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3070639276` |
| Base game (vanilla files for comparison) | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` (version 1.19.3.0) |
| Game logs | `C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV\logs\` (`error.log`, `game.log`) |
| Crash reports | `...\Hearts of Iron IV\crashes\` (empty as of 2026-09-27) |
| A Downfall save | `...\Hearts of Iron IV\save games\GER_1944_04_07_09.hoi4` (Germany, April 1944) |
| Local test mod entry | `...\Hearts of Iron IV\mod\downfall_local_fixes.mod` (points at this project's `mod\`) |
| Applied changes | `...\1944-Downfall\docs\CHANGELOG.md` |

## 4. Rules for continuing

1. **Only edit files in this repo's `mod/`.** Never edit the Steam Workshop
   folder, because Steam overwrites it. The brother publishes to Steam himself.
2. **Ask Oscar before changing any mod file.** A plan being approved is not
   permission to start. Wait for an explicit "go ahead".
3. **One fix = one git commit.** The message says what changed, why, the
   evidence, and how it was tested. If it wasn't tested in game, say so.
4. **Check against vanilla before calling something a bug.** If the base game
   does the same thing, it's probably valid syntax. Log it as a false alarm.
5. **Don't call a crash "fixed"** until it has crashed without the fix and
   stopped crashing with it. Until then, say "suspected cause".
6. **Keep file bytes intact.** Keep each file's encoding (UTF-8, with BOM if
   it had one) and line endings (the mod mixes CRLF and LF files). After an
   edit, `git diff --stat` must show only the lines you meant to change. If a
   whole file shows as changed, the line endings were converted, so revert.
   Localisation `.yml` files must be UTF-8 **with** BOM.
7. **Document every step.** Findings go in `docs/INVESTIGATION.md`. Applied
   changes go in `docs/CHANGELOG.md` (create it with the first applied fix).
   Keep this file's "Status" section current.
8. **Keep usage low.** Search with grep and read only the part of a big file
   you need. `mod/common/national_focus/germany.txt` alone is 900 KB.

## 5. Git quirks (important)

- The repo is **local only**. There's no remote and no backup. Suggest
  pushing it to a private GitHub repo if Oscar wants a backup.
- The system git config has `core.autocrlf=true`. This repo sets
  `core.autocrlf=false` and has `.git/info/attributes` containing `* -text`.
  That's needed because `mod/.gitattributes` (shipped by the author) says
  `* text=auto`, which would rewrite line endings. **`.git/info/attributes`
  is not copied when cloning.** In any new clone, run:
  `printf '* -text\n' > .git/info/attributes`
- `C:\Users\Ander` is itself a git repo (Oscar's home-folder backup). This
  project is ignored there (`/Desktop/Projects/*`). **Never run `git add -A`
  in `C:\Users\Ander`.**
- Useful commands, run from the project folder:
  ```
  git log --oneline                 # history
  git diff 253cea1 -- mod/          # every mod change vs the Workshop version
  git show <commit>                 # one change and its reason
  ```

## 6. Findings in short

| # | Report | Status |
|---|---|---|
| A | "Crashes at a certain date" | Strong suspect: `mod/common/scripted_effects/japan_scripted_events_mod.txt` lines 221 and 328. **Fixed** in `e20698c` (untested in game) |
| B | Crash when Bulgaria switches sides | No cause found by reading |
| C | Crash in Romania's 12-day capitulation decision | No cause found by reading |
| D | Crash on completing the Volkssturm focus | No cause found by reading. The focus's unit creation was redesigned on Oscar's request (`e6c0034`, CHANGELOG section 6); the crash was never reproduced |
| E | "Playing UK crashes" | Author's comments show earlier UK crashes. May be the same as A. |
| F | "D-Day seems broken" | Needs a description of what's broken |
| G | (not reported) | States 870, 871, 873 were defined twice. **Fixed** in `ce4f33a` (stale copies deleted) |

Full evidence, confidence and the proposed fix are in `docs/INVESTIGATION.md`,
section 2A.

## 7. Next steps, in order

0. **Test with fewer DLCs** through the Paradox launcher (untick DLCs in
   the playset), then compare `logs/error.log` with the all-DLC result
   (115 lines).
1. **Test fixes A and G and the 1.19.3 update in game** (steps in
   `docs/CHANGELOG.md`, "How to test in game"). Use a playset with only "1944 - Downfall (local fixes)" and
   observe a game as any country except Japan or China past September 1944.
   Ideally also run the same save with the Workshop version (does it crash?)
   and with the local fixes (does it not?). Record the result in
   CHANGELOG.md and INVESTIGATION.md.
2. **Crash reports for B–E.** Launch HOI4 with `-debug` (Steam → HOI4 →
   Properties → Launch options), let the game reach the moment that crashes
   (observe mode is fine), then collect the newest folder in `crashes\` plus
   `logs\error.log` and `logs\game.log`. Read them before touching any code.
3. **Ask for details:** when does the UK game crash (on load, at a date, on an
   action)? What exactly is broken about D-Day (no landing, landing fails,
   wrong date)?
4. **Lower priority:** brace mismatches in `history/countries/RAJ - British Raj.txt`
   and `SER - Serbia.txt` (the AST one was fixed by the 1.19.3 rebuild) (INVESTIGATION.md §3). Check
   what each one actually does in game before changing it. Also for the author
   to decide: states 520, 523 and 872 (Australia) have manpower that differs
   from the current base game, probably left over from old syncs. That's a
   balance question; leave it unless he asks.
5. **Keeping up with game updates:** mod files with the same path as a vanilla
   file replace it completely. Many are copies of older base-game versions,
   some from before 1.19. After
   a HOI4 patch, diff the old and new vanilla versions of each overridden file
   and port the relevant changes.

## 8. HOI4 facts that matter here

- A mod file with the same relative path replaces the vanilla file. The
  descriptor has no `replace_path`.
- `#` starts a comment. `else` written *inside* an `if` block is valid (vanilla
  does it 182 times).
- The mod's daily logic runs from `on_daily` in
  `mod/common/on_actions/do_on_actions.txt`, which calls `MOD_daily_update`
  and `MOD_daily_update2` (`mod/common/scripted_effects/update_daily.txt`).
  Each effect there checks its own tag, date and flags.
- `<state id> = { add_province_modifier = { ... province = { id = N } } }`:
  N must be a province inside that state. Vanilla never breaks this rule
  (0 of 82 cases). The mod breaks it twice (finding A).
- The console opens with the key under Esc. Commands used above: `observe`,
  `tag <TAG>` (switch country), `event <event id> <TAG>`.

## 9. The tools

Run from the project folder:

```
python tools/check_province_modifiers.py   # finding A: provinces outside their state
python tools/check_structure.py            # brace balance, template slot clashes
python tools/check_references.py           # events/ideas/characters/tags used in play
python tools/verify_update.py              # re-checks every claim (46 checks)
```

`check_province_modifiers.py` also reports states defined by more than one
file (finding G). Expected output on the unpatched baseline: 154 references
checked, 3 duplicate states, 2 in the wrong state, 0 unknown modifiers, 2
removed-but-never-added. After fixes A and G: 152 checked, 0 duplicates, 0 in
the wrong state, 0 unknown, 1 removed-but-never-added (province 9982, which
was already there).

Tip: Git Bash's `grep` hides carriage returns in its output. To check line
endings, count bytes with Python (`data.count(b"\r\n")`), not `grep | cat -A`.

All are read-only, except that `verify_update.py` also rewrites
`docs/checksums/mod-files.sha256`. Paths default to Oscar's PC: set
`HOI4_PATH` (game folder) and `WORKSHOP_PATH` (Workshop copy) to override.
`tools/pdx.py` is a small, tolerant parser for Paradox
script. It is **not** a full HOI4 validator: it catches the specific problems
above, nothing more. The province check only covers fixed state scopes
(`123 = { ... }`), not dynamic ones like `every_state`.

## 10. If you can't read the files directly

Ask Oscar to upload `docs/HANDOVER.md`, `docs/INVESTIGATION.md`, and the
specific mod file you need. Give him exact commands to run (PowerShell or
Git Bash) and ask him to paste the output back.
