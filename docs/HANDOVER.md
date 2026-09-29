# Maintaining this project

For anyone continuing the work on this update, a person or an AI assistant.
Read this first, then `docs/INVESTIGATION.md`.

## 1. What this project is

*1944 - Downfall* is gastav3's Hearts of Iron IV mod (Steam Workshop id
3070639276). This project updates it for HOI4 1.19.3, fixes reported bugs and
adds content, at Oscar's request. The author has little time to maintain the
mod, so every change must be easy for him to check himself.

## 2. Principles

- **Evidence for every claim:** file, line number and reason, and a source
  for anything historical.
- **Small, separate changes:** one change per commit. The message says what
  changed, why, the evidence, and how it was tested; if it wasn't tested in
  game, it says so.
- **Honest uncertainty:** "suspected" is not "fixed". Record false alarms
  instead of hiding them (`docs/INVESTIGATION.md` section 3 does this).
- **Check against the base game** before calling something a bug. If the base
  game does the same, it's probably valid.
- **Agree changes before making them.** A plan that was discussed is not a
  go-ahead; wait for an explicit yes.

## 3. Status (29 September 2026, Codex continuation)

- **113 files differ** from the July 2026 Steam version (34 edited, 3 deleted,
  76 new). The author published pull request #3's content on Steam on
  29 Sep 2026. Every change is in `docs/CHANGELOG.md` (sections 1–27) and summarised in
  `docs/READ-ME-FIRST.md`.
- **`python tools/verify_update.py`:** 80 checks, all pass.
- **The game's error.log** with the mod: 115 lines, unchanged by every
  addition since the 1.19.3 update (`docs/game-logs/`).
- **Packages:** the tags `final-2026-09-27` to `final-2026-09-29-v15`. Each
  package is `mod/`, the patches (one per commit), `docs/` and `tools/`, in
  a zip.
- **GitHub:** the same changes go to the author's repository in his layout
  (the mod at the top level, his line-ending setting): pull requests #2 and
  #3 (both merged by the author; #3 covers sections 14 to 17 and the
  Courland fix) and pull request #4 (open: sections 18–27, updated to 23b6824). The commit IDs there differ; CHANGELOG section 13 pairs
  them.
- **Not verified:**
  - actual play: none of the new content has been played through;
  - playing without some DLCs;
  - three heavily edited files not merged with 1.19.3 (GER decisions, the
    germany focus tree, artillery techs).
- **Open reports:** the crashes for Bulgaria's switch, Romania's 12-day
  decision and the Volkssturm focus need crash reports from the game. The
  UK crash is fixed (CHANGELOG section 15).
  D-Day decision blockers are corrected (section 27); the full AI landing remains unverified.

## 4. Where everything is

| What | Where |
|---|---|
| The mod | `mod/` (commit `253cea1` = the Steam version, byte-for-byte) |
| Findings | `docs/INVESTIGATION.md` |
| Applied changes | `docs/CHANGELOG.md` |
| How it was checked | `docs/VERIFICATION.md` |
| Check scripts | `tools/` (Python 3) |
| Game logs from the tests | `docs/game-logs/` |
| Steam Workshop copy (**never edit**) | `<Steam>\steamapps\workshop\content\394360\3070639276` |
| Base game (for comparison) | `<Steam>\steamapps\common\Hearts of Iron IV` (1.19.3) |
| The game's own logs | `<Documents>\Paradox Interactive\Hearts of Iron IV\logs\` (`error.log`, `game.log`, `setup.log`) |
| Crash reports | `<Documents>\Paradox Interactive\Hearts of Iron IV\crashes\` |

## 5. Rules for changing the mod

1. **Only edit files in `mod/`.** Never edit the Steam Workshop folder:
   Steam overwrites it. The author publishes to Steam himself.
2. **One change = one commit**, with its reason. Documentation and checks can
   follow in a separate commit.
3. **Keep file bytes intact:** each file's encoding (UTF-8, with a BOM where
   it had one) and its line endings (the mod mixes CRLF and LF files). After
   an edit, `git diff --stat` must show only the lines you meant to change; if
   a whole file shows as changed, the line endings were converted, so revert.
   Localisation `.yml` files must be UTF-8 **with** a BOM.
4. **New content in new files** where possible, so the author's files stay
   unchanged. `verify_update.py` checks every line removed from his files.
5. **Every new feature gets a check** in `verify_update.py`, and the check
   must be shown to fail on a deliberately planted error.
6. **Document every step:** findings in `INVESTIGATION.md`, applied changes
   in `CHANGELOG.md`, and keep this file's status current.

## 6. How to test

- **Load test:** add the mod to `dlc_load.json` (back it up first and restore
  it afterwards), start `hoi4.exe -debug`, wait for "Executing History" in
  `game.log`, then compare `error.log` with the latest file in
  `docs/game-logs/`. Writing `disabled_dlcs` in `dlc_load.json` does **not**
  disable DLCs.
- **Measuring an effect in a running game:** add a temporary
  `on_daily_GER` script (in its own file in `common/on_actions/`) that runs
  the effect once and logs values such as `[?ROOT.manpower_k]`,
  `[?ROOT.num_divisions]` or `[?ROOT.num_equipment@infantry_equipment_1]`,
  then start `tools/start_as_country.ps1 -Tag GER -Speed 5`. Unlike the
  history-file trick below, stockpiles and units are real here. Dates in
  triggers take no hour (`date > 1944.1.2`, not `1944.1.2.18`). Delete the
  file afterwards.
- **Running an effect in the game:** temporarily append a dated block with
  the effect and a `log = "..."` line to `mod/history/countries/GER -
  Germany.txt`, run the load test, read `game.log`, then restore the file
  with `git checkout`. Building levels and national spirits can be read at
  that moment; unit counts, stockpiles and manpower can't.
- **Starting as one country:** `tools/start_as_country.ps1 -Tag ENG` starts
  a new 1944 game directly as that country (the game's `-start_tag` option)
  and reports whether it crashed. With `-ModFile ugc_3070639276.mod` it runs
  the Workshop version instead. `tools/crash_site.py <crash folder>` shows
  which part of the game a crash report points to.
- **The 1944 order of battle** isn't read by the load test. To test it, load
  it in a temporary block with `load_oob = "GER_1944_nsb"`.
- **In play:** the console (the key under Esc): `event <id>`,
  `setcontroller <TAG> <province>`, `observe`, `tag <TAG>`. Each CHANGELOG
  section lists the commands for its feature.

## 7. Git notes

- **Line endings:** `.gitattributes` (at the repository root and in `mod/`)
  says `* -text`, so git never converts line endings and every clone is
  byte-exact. `verify_update.py` checks this with a fresh clone.
- **Useful commands:**
  ```
  git log --oneline -- mod/          # every change to the mod
  git diff 253cea1 -- mod/           # everything changed vs. the Steam version
  git show <commit>                  # one change and its reason
  ```
- **Patches for a package:** `git format-patch --relative=mod 253cea1..HEAD
  -- mod`. Apply them with `git -c core.autocrlf=false apply` in a folder
  that is not inside another git repository; otherwise git silently skips the
  paths (or set `GIT_CEILING_DIRECTORIES`).

## 8. Findings in short

| # | Report | Status |
|---|---|---|
| A | "Crashes at a certain date" | Strong suspect: `mod/common/scripted_effects/japan_scripted_events_mod.txt` lines 221 and 328. **Fixed** in `e20698c` (untested in game) |
| B | Crash when Bulgaria switches sides | No cause found by reading |
| C | Crash in Romania's 12-day capitulation decision | No cause found by reading |
| D | Crash on completing the Volkssturm focus | No cause found by reading. The focus's unit creation was redesigned (`e6c0034`, bug-check fix `d9d7888`, CHANGELOG section 6); the crash was never reproduced |
| E | "Playing UK crashes" | **Fixed** in `e578b10`: Allied countries with no land capitulated during the game setup, and the UK's "government in exile" popup crashed (CHANGELOG section 15) |
| F | Sometimes no Allied D-Day | Decision blockers corrected; full AI landing unverified (CHANGELOG 27) |
| G | (not reported) | States 870, 871, 873 were defined twice. **Fixed** in `ce4f33a` (stale copies deleted) |

Full evidence, confidence and the proposed fixes are in
`docs/INVESTIGATION.md`, section 2A.

## 9. Next steps, in order

1. **Play-test the new content** (each CHANGELOG section says how to test
   it), and fixes A and G: observe a game as any country except Japan or
   China past September 1944. Ideally run the same save with the Workshop
   version (does it crash?) and with this version (does it not?). Record the
   results in CHANGELOG.md and INVESTIGATION.md.
2. **Test with fewer DLCs** through the Paradox launcher (untick DLCs in the
   playset), and compare `error.log` with the all-DLC result (115 lines).
3. **Crash reports for B–D.** Launch HOI4 with `-debug`, let the game reach
   the moment that crashes (observe mode is fine), and collect the newest
   folder in `crashes\` plus `logs\error.log` and `logs\game.log`. Read them
   before touching any code.
4. **D-Day campaign test:** compare the same save before and after the section 27
   fixes. Observe an AI landing; retain the save and logs if none occurs.
5. **Lower priority:** the brace mismatches in `history/countries/RAJ -
   British Raj.txt` and `SER - Serbia.txt` (INVESTIGATION.md section 3); check
   what each does in game before changing it. States 520, 523 and 872
   (Australia) have manpower that differs from the current base game; that's a
   balance question for the author.
6. **Keeping up with game updates:** a mod file with the same path as a
   base-game file replaces it completely, and many are copies of older
   base-game versions. After a HOI4 patch, compare the old and new base-game
   versions of each overridden file and port the relevant changes.

## 10. HOI4 facts that matter here

- A mod file with the same relative path replaces the base-game file. The
  descriptor has no `replace_path`.
- The game ships its own script documentation in `<HOI4>\documentation\`
  (effects, triggers, modifiers, console commands). Use it before guessing.
- `#` starts a comment. `else` written *inside* an `if` block is valid (the
  base game does it 182 times).
- The mod's daily logic runs from `on_daily` in
  `mod/common/on_actions/do_on_actions.txt`, which calls `MOD_daily_update`
  and `MOD_daily_update2` (`mod/common/scripted_effects/update_daily.txt`).
  The new features use their own `on_daily_GER` blocks in their own files.
- `<state id> = { add_province_modifier = { ... province = { id = N } } }`:
  N must be a province inside that state. The base game never breaks this
  rule; the mod broke it in finding A. The same kind of mistake with
  buildings (a province outside the state) was fixed in CHANGELOG sections 7
  and 8.
- A country that controls no land but is at war capitulates while the game
  is still being set up. If it is in a faction (as a member, or as a
  member's colony), it becomes an exile in the faction leader, and when
  the leader is the player the game crashes on the exile popup. So such a
  country must not be in a faction at the start: make it an exile in
  `on_startup` instead (CHANGELOG section 15, check E).
- Equipment by its general type (`add_equipment_to_stockpile = { type =
  infantry_equipment ... }`): a negative amount is taken from **every** type
  in stock, and a positive amount arrives as the **newest** type. Name a
  specific type (and `variant_name` for a particular design). Measured in
  CHANGELOG section 17.
- In a division template, two sub-units at the same `x`/`y` count as one. The
  author's "Russische Befreiungsarmee" lists 16 infantry battalions but
  builds 15 (measured, CHANGELOG section 18).
- Reading a stockpile in script (`num_equipment@<type>`) needs the type in
  `common/synchronized_dynamic_tokens/`, or the game warns about
  multiplayer desyncs (OOS).
- An event fired from inside another country's scope
  (`random_country = { ROOT = { country_event = ... } }`) does **not** get
  that country as `FROM`: tested, FROM stayed Germany. To name another
  country in an event, save it first with `save_global_event_target_as`
  (CHANGELOG section 20).
- Event pictures are 210 × 176 uncompressed 32-bit DDS files with the
  tilted-photo frame drawn into the picture. The author keeps his in
  `gfx/events/`.
- `activate_decision` starts a timed decision from script and charges its
  cost; it runs even when the country can't afford it (tested: 20 political
  power became −30). Used by the Crimea popup (CHANGELOG section 25).
- `teleport_armies` moves the divisions in a state, whether or not they
  are in armies (tested with the player's and the AI's divisions).
- The game can't tell where a battle is fought: there is no such trigger,
  and the combat on_actions give the general, not the place.
- In tests, `set_province_controller` on a province with enemy divisions
  is undone before the next day. Files in `common/on_actions` run in
  case-sensitive name order (capitals first).
- A decision that is cancelled runs only its `cancel_effect`, not its
  `remove_effect`. This isn't documented, but 309 base-game decisions rely on
  it.
- In 1.19 the CAS, naval bomber, heavy fighter and jet planes are separate
  "duplicate archetypes" (`x_plane_airframes.txt`). A bonus for "all
  aircraft" must list each of them.

## 11. The tools

Run from the project folder:

```
python tools/check_province_modifiers.py   # provinces outside their state, unknown modifiers
python tools/check_structure.py            # brace balance, template slot clashes
python tools/check_references.py           # events/ideas/characters/tags used in play
python tools/check_berlin_map.py           # Festung Berlin's map facts (needs Pillow and numpy)
python tools/verify_update.py              # re-checks every claim (80 checks)
python tools/crash_site.py "<crash folder>" # which part of the game a crash report points to
```

`check_province_modifiers.py` also reports states defined by more than one
file (finding G). Current output: 544 province references checked; the 22
remaining "not in the state" hits are lines copied unchanged from the base
game (CHANGELOG section 8).

All are read-only, except that `verify_update.py` also rewrites
`docs/checksums/mod-files.sha256`. Paths default to Steam's standard
folders; set `HOI4_PATH` (game folder) and `WORKSHOP_PATH` (Workshop copy) to
override. `tools/pdx.py` is a small, tolerant parser for Paradox script. It
is **not** a full HOI4 validator: it catches the specific problems above,
nothing more.

Tip: Git Bash's `grep` hides carriage returns in its output. To check line
endings, count bytes with Python (`data.count(b"\r\n")`).
