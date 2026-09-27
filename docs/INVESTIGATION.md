# 1944 - Downfall: bug investigation log

Started 2026-09-27. Written so the mod author can check every claim himself.

**Status: investigation only. No file in `mod/` has been changed.**
`git diff 253cea1 -- mod/` is empty. Every proposed fix below is a proposal
until it has been tested in-game and approved.

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

These scripts run from `on_daily` (`common/scripted_effects/update_daily.txt`,
`MOD_daily_update2`), for any game where Japan and China are both AI. That covers
every game where the player is *not* Japan or China, including UK games.

- Phase 2 (`province 7167`): AI Japan can take the decision after **1944-05-11**
  (`JAP_mod.txt:165`). The script runs the next day.
- Phase 3 (`province 4028`): after **1944-08-01** (`JAP_mod.txt:330`).

So the game would die at a similar date in each playthrough, whatever the
player is doing. That's exactly how the reports describe it. It would also
explain why a crash seems to "happen during" some other event on screen, like
Romania's or Bulgaria's switch in summer 1944. That link is a possibility, not
something I've shown.

**Not proven yet:** I haven't reproduced the crash. The link between
"wrong-state province modifier" and "crash" rests on the author's own `#fix`
edits, not on a crash log.

**Proposed fix (not applied)**

- Line 221: comment out `id = 7167`. Phase 1 never adds a modifier to 7167
  (line 165 is already commented out), so there's nothing to remove. This is
  the same change the author made at line 371.
- Line 328: move `id = 4028` into a `594 = { ... }` block so the phase-3 bonus
  still applies where it was meant to. Then re-enable the matching removal in
  `JAP_ichi_go_failed_modifiers` under state 594 instead of 599. The
  alternative, simply commenting it out like line 413, is safer but drops that
  province's bonus.

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

---

## 3. Checks that turned out to be false alarms

Kept here on purpose. These are things that *looked* like bugs but aren't.

| Check | Result in mod | Result in vanilla | Verdict |
|---|---|---|---|
| `else` written inside its `if` block | 272 cases | 182 cases | Valid HOI4 syntax. **Not a bug.** |
| Two units in one template slot | 14 cases | 19 cases | Sloppy but harmless. Low priority. |
| Unbalanced braces | 20 (17 in unused `FIN_1944_old.txt`) | 21 cases | Worth tidying. Not a crash suspect. |

The brace problems are still worth a later look. `history/countries/RAJ - British Raj.txt:662`
opens a block that is never closed, so anything after it may be ignored.

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
