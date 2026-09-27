# Changelog: changes to the mod

Compared with the Steam Workshop version (id 3070639276), stored unmodified in
baseline commit `253cea1`. See every change at once with
`git diff 253cea1 -- mod/`.

## Not yet released (not on Steam, **not yet tested in game**)

### 1. Ichi-Go province modifiers applied in the wrong state (commit `e20698c`)

- **File:** `mod/common/scripted_effects/japan_scripted_events_mod.txt`, 2 lines
- **Change:** commented out `id = 7167` (line 221) and `id = 4028` (line 328),
  each with a note saying which state the province really belongs to.
- **Why:** these were the only 2 of 154 province references in the mod that
  point at a province outside the state they run in. The base game never does
  this (0 of 82). The author had already commented out the other uses of these
  two provinces (lines 165, 371, 413). Suspected cause of the "crashes at a
  certain date" report. Details: INVESTIGATION.md §2A.
- **Gameplay effect:** Ichi-Go stage 3 no longer puts its defence penalty on
  province 4028. It still applies to provinces 1023, 7095 and 1597, and the
  state-wide bonus on state 594 still applies. It also no longer leaves that
  penalty on 4028 for the rest of the game, which the old code did because
  its removal was disabled. The stage 2 line had no gameplay effect: it
  removed something that was never added.
- **Checked:** only these 2 lines differ; line endings unchanged; checkers
  show 0 wrong-state references; every Ichi-Go modifier that is added is
  removed again at the end; no other script uses this modifier.

### 2. States 870, 871, 873 were defined twice (commit `ce4f33a`)

- **Files deleted:** `mod/history/states/870-North West Australia.txt`,
  `871-South West Australia.txt`, `873-South West Queensland.txt`
- **Why:** the base game renamed its files for these states
  (`870-Pilbara-Kimberley.txt`, `871-Esperence-Goldfields.txt`,
  `873-Channel Country.txt`). A mod file only replaces a base-game file with the
  exact same name, so the game was loading two definitions of each state. The
  mod's copies came from a bulk sync in the author's commit `4ce7056`
  (2023-02-19) and were never edited. Apart from manpower and category, they
  match the base game's current files. Details: INVESTIGATION.md §2G.
- **Gameplay effect:** these three outback states now use the base game's
  values: 870 pastoral with 25,000 manpower (the old copy: wasteland, 1,000),
  871 105,000 (old copy: 50,000), 873 60,000 (old copy: 10,000). It's unknown
  which definition the game used before. At most, Australia gets about 129,000
  more manpower, which is small next to the 2,650,000 in its main state.
- **If the lower values were intended:** restore the old files under the base
  game's names, e.g.
  `git show 253cea1:"mod/history/states/870-North West Australia.txt" > "mod/history/states/870-Pilbara-Kimberley.txt"`
- **Checked:** each state now has exactly one definition; the province-to-state
  map is unchanged (10,272 provinces); nothing refers to the deleted file names.

### 3. Update to Hearts of Iron IV 1.19.3 (commits `6fa793c` … `d55cf37`)

The current game is 1.19.3 (released 2026-09-17). The mod said 1.19.2, but
many files it replaces were older copies from before 1.19 (Thunder at Our
Gates), so new base-game content broke. **Rule followed throughout: the
author's own content is kept byte-for-byte; only old base-game text is
updated, and missing base-game pieces are added.** How each file was
checked is in INVESTIGATION.md §8.

| Commit | Change |
|---|---|
| `6fa793c` | descriptor.mod: supported_version 1.19.2.0 → 1.19.3.0 |
| `2d80d87` | Netherlands focus tree = 1.19.3 file + the author's only edit (`RKN` may use the Dutch tree). Restores the 15 Thunder at Our Gates focuses (~60 errors) |
| `f646e4a` | cosmetic.txt = 1.19.3 file + the mod's 17 own tags (84 base-game tags were missing) |
| `8041896` | Argentina: character ID renamed in 1.19; a duplicate recruit removed. (Its Australia part was undone by `4a17ff6` and redone in `58a1a82`.) |
| `586de46`, `d55cf37` | JAP/SOV decision files: added base-game decisions they lacked (Tauran border-incident chain; Sakhalin decision) |
| `0384e82` | Added news event bftb_news.11, which the mod's Bulgaria tree fires |
| `c8dac21` | Special forces: dead pre-1.19 doctrine techs in 11 countries' 1944 setups → 1.19 sub-doctrines (mapping table in the commit message). Nobody was getting these doctrines before |
| `4a17ff6` | Australia history = 1.19.3 file + the author's 1944 block + his 4 stockpiles |
| `d5c3c69` | Siam history = 1.19.3 file + the author's 1944 block |
| `58a1a82` | Australia: fixes a Paradox bug in the 1.19.3 file (`AST_domestic_industries` → `AST_domestic_industry`) |
| `368cee9` | tools/rebase_helpers.py, used for the above |

**Gameplay changes to be aware of:** the 11 countries now actually get
special-forces doctrines (with Arms Against Tyranny, as before). Australia
and Siam start with the 1.19.3 setup plus the author's 1944 changes.

**Checked in the game** (error.log, all 28 DLCs on): Workshop version 282
errors → 115 after the update. Only 1 error is new: Paradox's own 1.19.3
Siam file retires a politician it only hires *without* Thunder at Our
Gates. It's harmless and left as Paradox wrote it. The mod's own checkers
are also clean (0 wrong-state modifiers, 0 duplicate states).

**Not done / not verified:**
- **Playing without some DLCs is not tested.** My attempt to switch DLCs
  off when starting the game didn't work, so that result was thrown away.
  Test it through the Paradox launcher.
- Three heavily edited files that 1.19.3 also changed were **not** merged:
  `decisions/GER.txt`, `national_focus/germany.txt` and
  `technologies/artillery.txt`. The relevant 1.19.3 changes (Reichskommissariat
  Australasien states, Second Treaty of Berlin conditions) are 1936–41
  content with little effect on a 1944 start, and merging safely needs the
  author. His versions are unchanged.
- Base-game Burma oil-field decisions (`BRM_blow_up_the_oil_fields`,
  `BRM_repair_the_oil_fields`) are missing from the mod's JAP.txt. Not
  added, because they'd add new 1944 gameplay; the author's call.
- The remaining 115 errors were already there before the update and are
  mostly harmless. INVESTIGATION.md §8 has the list.

### 4. Flavor event: Slovak National Uprising (commits `7de1ce8`, `a5982fe`)

Added on Oscar's request: a simple event, about 3,000 manpower lost.

- **New files only** (nothing existing changed; delete these three to remove it):
  `events/slovak_uprising.txt`, `common/on_actions/slovak_uprising_on_actions.txt`,
  `localisation/english/slovak_uprising_l_english.yml`.
- **When:** once, from 29 August 1944, if Slovakia is in Germany's faction, at
  war with the Soviet Union and not capitulated (checked daily for Slovakia
  only, via `on_daily_SLO`).
- **Effect:** **Germany** loses 3,000 manpower (the troops sent in to crush the
  uprising), applied once by the trigger. Slovakia loses nothing. The event is
  shown to Slovakia **and Germany**; its single option only shows the loss as
  a tooltip, so nothing is applied twice. (The first version, `7de1ce8`, took the
  manpower from Slovakia; `a5982fe` moved it to Germany, as Oscar intended.)
- **Picture:** `GFX_report_event_czech_soldiers_02` (base game: Czechoslovak
  soldiers at a machine gun), chosen after viewing six candidates.
- **Checked:** both script files parse; the text file is UTF-8 with BOM and
  every value is on one line; the game loads it, and error.log is identical
  before and after (115 = 115, 0 new); text.log has nothing about it.
- **See it quickly in game:** console `event slovak.uprising.1 GER` shows the
  pop-up (the console does not apply the manpower loss; the real trigger does).

## How to test in game

A local copy of the fixed mod is registered as a separate mod,
**"1944 - Downfall (local fixes)"** (file
`Documents\Paradox Interactive\Hearts of Iron IV\mod\downfall_local_fixes.mod`,
pointing at this project's `mod\` folder).

1. In the Paradox launcher, create a new playset with **only** "1944 - Downfall
   (local fixes)". Never enable it together with the Workshop "1944 - Downfall";
   two copies of the same mod at once will break the game.
2. Optional: Steam → HOI4 → Properties → Launch options: `-debug`, for more
   detailed logs.
3. Start the 1944 game as any country except Japan or China and let it run past
   September 1944. Observe mode (console command `observe`) is fine.
4. If it crashes, note the in-game date and what was on screen. Then keep the
   newest folder in `Documents\Paradox Interactive\Hearts of Iron IV\crashes\`
   and `logs\error.log`.
5. Afterwards, switch back to your usual playset. To remove the test entry,
   delete `downfall_local_fixes.mod`.

On another PC, register the `mod/` folder the same way (a `.mod` file with its
`path`); docs/READ-ME-FIRST.md shows how.

## For the author (publishing)

27 files differ from the version on Steam: 21 edited, 3 deleted, 3 new (full list:
`git diff --name-status 253cea1 -- mod/`, or docs/READ-ME-FIRST.md). Each
change is also a patch in the package's `patches/` folder (one per commit,
with its reason), or can be viewed with `git show <commit>`.

To publish, bring your copy in line with the final `mod/` folder. Either copy
the changed files over your copy and delete the three state files, or apply
the patches. If your copy has changes that aren't on Steam yet, use the
patches so none of your work is overwritten. The three files must be
**deleted**, not just left out. Then upload as usual: `descriptor.mod`
already says `supported_version="1.19.3.0"`.

Note: the July 2026 upload contained your old `.git` folder (history up to
2024, remote github.com/gastav3/Hoi4_1944), so anyone subscribed can read
that commit history. You may want to leave it out of future uploads.
