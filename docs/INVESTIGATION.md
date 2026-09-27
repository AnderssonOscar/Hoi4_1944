# 1944 - Downfall: bug investigation log

Started 2026-09-27. Written so the mod author can check every claim himself.

**Status: investigation only. No file in `mod/` has been changed.**
`git diff 253cea1 -- mod/` is empty. Every proposed fix below is a proposal
until it has been tested in-game and approved.

The one ready fix is a tested patch in `docs/proposed-fixes/`. Apply it only
after approval, with
`git apply docs/proposed-fixes/0001-ichi-go-wrong-state-provinces.patch`.
Section 6 records the self-review of everything in this file.

---

## 0. What I worked from

| Item | Value |
|---|---|
| Source | Steam Workshop item 3070639276, local download dated 2026-07-04 |
| Game version on this PC | 1.19.3.0 (mod declares 1.19.2.0) |
| Baseline commit | `253cea1`, the Workshop files copied unmodified |
| Excluded | the `.git` folder shipped inside the Workshop upload (see below) |

**Baseline integrity.** Every one of the 914 mod files in the baseline commit
was hashed (`git hash-object --no-filters`) and compared against the same file
in the Steam Workshop folder: 914/914 identical. Line endings are stored as-is.
The mod's own `.gitattributes` (`* text=auto`) would have converted them, so this
repo overrides it in `.git/info/attributes`. The mod's copy is left untouched.

**About the `.git` folder in the Workshop upload.** The upload contains a `.git`
directory whose remote is `https://github.com/gastav3/Hoi4_1944.git`. Its last
commit is `6df4cfb "random fixes"` from 2024-07-11 by gastav3. That repo now
returns 404 (private or deleted). The Workshop files are newer than that commit:
about 860 files differ, including map files. So the Workshop version is the
source of truth, and the old `.git` was not used for anything.

---

## 1. Summary

| # | Reported bug | Status | Confidence |
|---|---|---|---|
| A | "Crashes at a certain date" | **Strong suspect found**: Ichi-Go scripts (Japan vs China) | High that it's a bug, medium that it's *this* crash |
| B | Crash when Bulgaria switches sides | Code read, no definite cause found | Not yet identified |
| C | Crash in Romania's 12-day capitulation decision | Code read, no definite cause found | Not yet identified |
| D | Crash on completing the Volkssturm focus | Code read, one weak lead (ruled mostly out) | Not yet identified |
| E | "Playing UK crashes the game" | Clues found in author's own comments, may be the same as A | Not yet identified |
| F | "D-Day seems broken" | Report too vague, needs a description | Not started |
| G | *(not reported; found in self-review)* | Three Australian states are defined twice | Certain it's a defect; no known crash link |

The honest summary: reading the scripts produced **one** well-supported bug.
The other crashes need an in-game reproduction with the crash report HOI4
writes (see section 4), because the code has no obvious defect.

---

## 2. Findings

### A. Ichi-Go scripts put province modifiers on provinces outside the state

**Where**

- `mod/common/scripted_effects/japan_scripted_events_mod.txt:221`. In
  `JAP_ichi_go_2_start_script`, `620 = { remove_province_modifier = { ... id = 7167 } }`.
  Province 7167 is in **state 1036**, not 620.
- `mod/common/scripted_effects/japan_scripted_events_mod.txt:328`. In
  `JAP_ichi_go_3_start_script`, `599 = { add_province_modifier = { ... id = 4028 } }`.
  Province 4028 is in **state 594**, not 599.

**Evidence**

1. The mod author already treated exactly these two provinces as a problem.
   Elsewhere in the same file they are commented out with notes:
   - line 165: `#id = 7167` (the phase-1 *add*)
   - line 371: `#id = 7167 fix`
   - line 413: `#id = 4028 #fix`

   The two lines above are the remaining uses of those provinces that were
   *not* commented out.
2. `tools/check_province_modifiers.py` checks every `add/remove_province_modifier`
   in the mod against the province lists in `history/states` (mod files
   overriding vanilla, the same way the game loads them). Out of all province
   references in fixed state scopes, **only these two** are in the wrong state.
3. Calibration against the base game: the same check over vanilla 1.19.3 finds
   **0 of 82** references in the wrong state. Paradox never does this, so it's
   not an accepted pattern.

**Why it matches "crashes at a certain date"**

These scripts run every day from `on_daily` (`common/on_actions/do_on_actions.txt:356`
→ `MOD_daily_update2` in `common/scripted_effects/update_daily.txt`), once for
each country. That they run per country is verified, not assumed: the flag
`GER_operation_margarethe`, which a daily script sets only when the country
running it is Germany, is present in the Downfall save `GER_1944_04_07_09.hoi4`.

When the bad lines actually run:

- The script requires **China to be AI** (`CHI = { is_ai = yes }`). Japan can
  be AI or the player.
- Phase 2 (`province 7167`) runs the day after Japan takes stage 2 of Ichi-Go.
  AI Japan can do that after **1944-05-11** (`JAP_mod.txt:165`), but only if it
  first **won stage 1**, taking the Beijing–Wuhan railway within 60 days.
- Phase 3 (`province 4028`) needs stage 2 won as well, and for AI Japan a date
  after **1944-08-01** (`JAP_mod.txt:330`).

So in games where Japan's offensive goes well, the game would hit this at a
similar date each time, whatever the player is doing. That fits the "certain
date" report. But it isn't guaranteed in every game: if Japan's stage 1 fails,
these lines never run. It could also explain crashes that seem to "happen
during" another event on screen, like Romania's or Bulgaria's switch in summer
1944. That link is a possibility, not something I've shown.

**Not proven yet:** I haven't reproduced the crash. The link between
"wrong-state province modifier" and "crash" rests on the author's own `#fix`
edits, not on a crash log.

**Proposed fix (not applied):** `docs/proposed-fixes/0001-ichi-go-wrong-state-provinces.patch`

Two lines change, both commented out the same way the author did it himself:

```
line 221:  id = 7167   →   #id = 7167 # fix: province 7167 is in state 1036, not 620
line 328:  id = 4028   →   #id = 4028 # fix: province 4028 is in state 594, not 599
```

- Line 221: nothing ever adds this modifier to 7167 (the phase-1 add at line
  165 is already commented out), so there's nothing to remove. This is the same
  change the author made at line 371.
- Line 328: after this change, phase 3's add (state 599: 1023, 7095, 1597)
  matches its removal at line 406 exactly. What the modifier does
  (`mod/common/modifiers/mod_static_modifiers.txt`): `army_defence_factor = -0.75`,
  `army_speed_factor = 0.2`. So it's a defence penalty for whoever defends that
  province. Today its removal is disabled (line 413), so if the wrong-state add
  works at all, province 4028 keeps a permanent −75 % defence penalty after
  Ichi-Go ends. The fix removes that too. What's lost: during phase 3, province
  4028 doesn't get the penalty. The state-wide `JAP_offensive_modifier` the
  phase-3 decision puts on state 594 still applies.

*Changed from my first proposal.* I first suggested moving 4028 into a
`594 = { ... }` block and re-enabling its removal. I dropped that, because the
cleanup script also runs when Ichi-Go fails *before* phase 3. That would add
another removal of a modifier that was never added, and whether that's safe in
this engine is unknown. Commenting the line out adds no new behaviour.

**Tested so far (without the game):** applied to a scratch copy and ran both
checkers before and after. Wrong-state references went from 2 to 0, 7167 dropped
out of "removed but never added", nothing new appeared, and the structure check
output was byte-identical. `git diff --stat` shows 1 file, 2 lines. Line endings
are preserved (CRLF: 422 before, 422 after), and the patch applies cleanly to
the baseline. **Not tested in game.**

**How to verify:** play as any country except Japan or China and run past
August 1944. Or, faster, with the console on the April 1944 save: set
Japan's flags and let the day tick (steps in section 4).

### B. Bulgaria switches sides: `common/decisions/BUL_mod.txt`

Read the whole decision (`BUL_surrender_soviet`) and the event it fires
(`bulgaria.switch.side.1`, `events/mod_events.txt:617`).

- All referenced objects exist: cosmetic tag `BUL_communism`, idea
  `mod_switched_side`, event ids.
- The sequence (white peace → leave Axis → become Soviet puppet → join Soviet
  faction → join war vs Germany → white peace with Finland) is the usual
  side-switch approach. None of these calls is obviously invalid.
- Only happens when Bulgaria is **AI** (`visible = { is_ai = yes }`), after 1944-07-10.

**No definite cause found by reading.** Needs a crash report (section 4).

### C. Romania's 12-day capitulation: `common/decisions/ROM_mod.txt`

The "quick one with the 12-day timer" is `ROM_surrender_soviet`
(`days_remove = 12`). When Romania takes it, Germany gets `romania.switch.side.2`
("Our offensive will sort this out" / "Launch Operation Margarethe II"). If
Germany doesn't retake the lost ground, the `remove_effect` runs after 12 days
and switches Romania to the Soviet side. The player's report ("crashes...
forcing me to manually trigger Operation Margarethe") fits a crash in that
`remove_effect`, which choosing Margarethe avoids.

Things I noticed in `remove_effect`, none proven to crash:

- It spawns 8 divisions in state 46 (Bucharest) without checking that Romania
  still controls it (`ROM_mod.txt:260`).
- The template `"Sov Divizia Infanterie"` puts two regiments in each of four
  slots (`ROM_mod.txt:244-251`). This is sloppy, but vanilla has 19 similar
  cases and runs fine, so I'm **not** counting it as a crash cause.

**No definite cause found by reading.** Needs a crash report.

### D. Volkssturm focus: `common/national_focus/germany.txt:39306`

`GER_form_volksturm` creates a template and 32 divisions. Some divisions force
rifles made by POL, DEN, HOL, FRA or SOV (`force_equipment_variants`).

- Vanilla uses foreign-made equipment the same way (`events/Mexico.txt`), so
  the syntax is valid.
- My first theory was that some of those countries might no longer exist. But
  in this mod POL, DEN and HOL all own states at the 1944 start, so that's weak.
  It could still matter if one of them has been annexed by the time the focus
  completes (after 1944-11-01 or at 10% surrender).

**No definite cause found by reading.** Needs a crash report.

### E. Playing as the UK

Clues left by the author:

- `common/on_actions/do_on_actions.txt:50`: `JAP = { transfer_state = 336 } # this has to be done here otherwise uk crashes when choosen as nation`
- `history/countries/ENG - Britain.txt:630`: `#add_to_faction = BEL #crashes`

So UK-specific crashes have happened before and were worked around. The report
doesn't say *when* the UK game crashes. If it's mid-1944, finding A applies to
UK games too. **Need to ask:** crash on load, at a date, or on a specific action?

### F. D-Day

D-Day is scripted through AI-only decisions (`common/decisions/Allies_1944.txt`:
`operation_overlord_prep`, `operation_overlord`, `operation_overlord_breakout`,
`operation_dragoon`) plus daily scripts (`allied_scripted_events_mod.txt`). The
airborne template it spawns (`"Airborne Division"`) exists in the USA OOB. Without
knowing what "broken" means (no invasion? invasion fails? wrong date?), there's
nothing specific to check yet.

### G. Three Australian states are defined twice (found in self-review)

A mod file only replaces a base-game file with **exactly the same name**. The
mod ships these state files, but the base game (files dated 2026-06-11) uses
different names for the same states, so the game now loads **both**:

| State | Base game file | Mod file | Only difference in content |
|---|---|---|---|
| 870 | `870-Pilbara-Kimberley.txt` | `870-North West Australia.txt` | manpower 25000 → 1000, category pastoral → wasteland |
| 871 | `871-Esperence-Goldfields.txt` | `871-South West Australia.txt` | manpower 105000 → 50000 |
| 873 | `873-Channel Country.txt` | `873-South West Queensland.txt` | manpower 60000 → 10000 |

(Compared after stripping comments and whitespace. Everything else, including
the province lists, is identical.)

Most likely the base game renamed these files in a patch, and the mod's
versions stopped overriding them. Result: two definitions per state, and the
mod's lower Australian manpower may not apply. I don't know of a crash caused
by this.

**Proposed fix (not applied, needs approval):** rename the three mod files to
the base game's names, so they override again as intended. There's no content
change. `tools/check_province_modifiers.py` now reports this under "State ids
defined by more than one file".

---

## 3. Checks that turned out to be false alarms

Kept here on purpose. These are things that *looked* like bugs but aren't.

| Check | Result in mod | Result in vanilla | Verdict |
|---|---|---|---|
| `else` written inside its `if` block | 272 cases | 182 cases | Valid HOI4 syntax. **Not a bug.** |
| Two units in one template slot | 14 cases | 19 cases | Sloppy but harmless. Low priority. |
| Unbalanced braces | 20 (17 in unused `FIN_1944_old.txt`) | 21 cases | Worth tidying. Not a crash suspect. |

The brace problems in files that are actually used (the base game's copies of
these files have none, so the mod introduced them):

- `history/countries/RAJ - British Raj.txt:662`: `1943.12.30 = {` is never
  closed. It's the last block and runs to the end of the file (line 981), so
  the fix is a missing `}` at the end. Probably harmless if the game closes it
  at end of file, but unverified.
- `history/countries/AST - Australia.txt:1277` and `SER - Serbia.txt:409`: one
  extra `}` on the last line of the file. Probably harmless.
- The other 17 are in `history/units/FIN_1944_old.txt`, which nothing in the mod
  or base game references (checked), so the game never loads it.

---

## 4. How to confirm the crashes (next step)

HOI4 writes a crash report to
`Documents\Paradox Interactive\Hearts of Iron IV\crashes\` when it crashes.
That folder is currently empty on this PC, so no crash report exists yet.

Plan:

1. Launch HOI4 with the mod and `-debug` in the launch options, so errors are
   logged and the console is available.
2. Load `GER_1944_04_07_09.hoi4` (a Downfall save on this PC) or start a new game.
3. Let it run to late 1944 as a non-Japan, non-China country. If it crashes, the
   crash folder plus `logs/error.log` and `logs/game.log` show where.
4. For B, C and D, trigger each one directly with the console and read the
   crash report.

Each crash report goes into this file, next to the finding it confirms or
disproves.

---

## 5. Tools used (in `tools/`)

All read-only; they never modify `mod/`.

- `pdx.py`: a small parser for Paradox script files.
- `check_province_modifiers.py`: finding A.
- `check_structure.py`: the checks in section 3.

Run from the project folder: `python tools/check_province_modifiers.py`

---

## 6. Self-review (2026-09-27)

Everything above was re-checked before handover. What was checked and what
changed as a result:

| Check | Result |
|---|---|
| Every file:line cited in this document | All correct |
| "`FIN_1944_old.txt` is unused" | Correct: no reference in mod or base game |
| Does `on_daily` run per country? (finding A depends on it) | Yes. Evidence in the save (see A) |
| Calibration re-run, each tree against its own map | Mod: 154 references, 2 wrong. Base game: 82 references, 0 wrong |
| Parser bug: a `#` between escaped quotes (`\"`) in a string was treated as a comment | Fixed in `tools/pdx.py`. All results unchanged |
| Duplicate definitions of the same state | **New finding G** |
| Finding A's trigger conditions | **Corrected**: needs China AI and Japan winning stage 1. Not "every game" |
| Proposed fix for line 328 | **Changed**: comment out instead of moving (see A) |
| Proposed fix, dry run on a scratch copy | Only the intended 2 lines change, line endings kept, nothing new flagged, applies cleanly |

Still **not** verified: anything in the running game. In particular, that a
province modifier in the wrong state actually crashes HOI4. That rests on the
author's own `#fix` edits, and only an in-game test settles it.
