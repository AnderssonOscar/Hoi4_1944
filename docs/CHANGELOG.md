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

## For the author (publishing)

The changes are one edited file and three deleted files, listed above. Review
them with `git show e20698c` and `git show ce4f33a`. To publish, make the same
changes in your own copy and upload as usual. The three files must be
**deleted**, not just left out of an edit.
