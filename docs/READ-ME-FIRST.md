# 1944 - Downfall: update for HOI4 1.19.3 + bug fixes

Prepared on 2026-09-27 by Oscar, with an AI assistant (Claude). You don't
have to trust the AI for any of it: every change is listed with its reason,
every change is a patch you can read, and everything can be checked
independently (see "Check it yourself").

## In short

- **Starting point:** the version currently on the Steam Workshop (id
  3070639276, July 2026), unchanged apart from what is listed here.
- **66 files differ** from that version: 31 edited, 3 deleted, 32 new. Your own
  content was kept byte-for-byte everywhere, and that was checked by script.
- **Updated for HOI4 1.19.3** (released 17 Sep 2026). With the mod loaded,
  the game's own `error.log` went from 282 lines to 115; the base game alone
  gives 1. The update itself adds no new errors (1 new line comes from
  Paradox's own Siam file and is harmless).
- **Fixes a suspected crash cause:** the Ichi-Go scripts still used provinces
  7167 and 4028 in the wrong state (you had already commented out their other
  uses at lines 165, 371 and 413 of `japan_scripted_events_mod.txt`).
- **Not play-tested.** It was tested by loading the game and its 1944 setup.
  The reported crashes for Bulgaria's switch, Romania's 12-day decision, the
  Volkssturm focus and the UK are **not** explained yet. (The Volkssturm
  focus was redesigned, see change 11, but its crash was never reproduced.)

## What's in this package

| Item | What it is |
|---|---|
| `mod/` | the complete updated mod, ready to test or upload |
| `patches/` | every change as a patch (27, in order), each with its reason |
| `docs/CHANGELOG.md` | what changed, why, and the gameplay effects |
| `docs/VERIFICATION.md` | how it was checked: 67 automated checks, game error logs, checksums |
| `docs/INVESTIGATION.md` | the full investigation log, including mistakes and false alarms |
| `docs/game-logs/` | the game's error.log: base game, Workshop version, updated version |
| `docs/checksums/mod-files.sha256` | SHA-256 of every file in `mod/` |
| `tools/` | the check scripts (Python 3) |
| `docs/HANDOVER.md` | notes for whoever continues the work |

## What changed

| # | Change | Files |
|---|---|---|
| 1 | Ichi-Go: 2 wrong-state province IDs commented out, the same way you did elsewhere | japan_scripted_events_mod.txt |
| 2 | 3 old Australian state files deleted: the base game renamed its files, so both loaded (the game logged "State ID conflict") | history/states/870, 871, 873 |
| 3 | `supported_version` 1.19.2.0 → 1.19.3.0 | descriptor.mod |
| 4 | Netherlands tree = 1.19.3 file + your RKN edit (restores the 15 Thunder at Our Gates focuses) | national_focus/netherlands.txt |
| 5 | cosmetic.txt = 1.19.3 file + your 17 tags (84 base-game tags were missing) | countries/cosmetic.txt |
| 6 | Special forces: the old doctrine techs no longer exist in 1.19; replaced with the 1.19 sub-doctrines (mapping in patch 0009) | 11 files in history/countries |
| 7 | Australia and Siam history = 1.19.3 file + your 1943.12.30 block (+ your 4 AST stockpiles) | AST, SIA |
| 8 | Missing base-game decisions and a news event added; 3 renamed IDs fixed | JAP.txt, SOV.txt, BFTB_NewsEvents.txt, ARG, AST |
| 10 | New: **Nero Decree** and **Werwolf** decisions for Germany's last stand (CHANGELOG section 5). **Not play-tested yet** | 6 new files `GER_last_stand_*` |
| 9 | New flavor event: the Slovak National Uprising (29 Aug 1944). Germany loses 3,000 manpower crushing it; Slovakia and Germany see it | 3 new files: events, on_actions, localisation |
| 11 | **Volkssturm redesigned** (CHANGELOG section 6). The focus now raises divisions in every German state by population (42 if all are held), and 4 decisions add more from the historical dates in 1945 (east, Oder/Pomerania, west, Berlin): 89 divisions / 445 battalions in all, about the 700+ real battalions that fought. Rifles follow the Gau Bayreuth list of Jan 1945 (mostly Italian Carcanos), 40–75% equipped, no training. Your template, availability and AI weights are unchanged. **Not play-tested yet** | germany.txt focus block, focus tooltip, 3 new files `GER_volkssturm_*` |
| 12 | Fix: "Königsberg in Ruins" removed forts from three provinces in Africa (wrong IDs) instead of Königsberg's ring fort; now it removes them from the ring fort your Festung focus builds (11265). | mod_news.txt |
| 13 | Fix: your Oder–Neisse Defence decision built the Stettin fort in the wrong state (Vorpommern instead of Hinterpommern), and "Destroy Antwerpen" targeted Antwerp's port in Flanders instead of Antwerp's own state. One line each (CHANGELOG section 8) | GER_mod.txt, mod_events.txt |
| 14 | New: **Festung Berlin**, a five-event chain for the defence of Berlin (Defence Area, Seelow Heights, Clausewitz, Weidling, encirclement): forts built over six weeks, only topped up to at most level 5 so your Festung Cities and Oder–Neisse forts are respected; 3 weak emergency divisions; a Brandenburg bonus; your human-only Berlin bonus rule kept (CHANGELOG section 9). **Not play-tested yet** | 6 new files `GER_festung_berlin_*` |
| 15 | New in the 1944 start: **5. SS 'Wiking'** (your SS Panzer-Division template, at your Cherkassy position) and **11. SS 'Nordland'** (your Panzergrenadier template with SS names, at your Leningrad-front SS position), maximum experience, your elite equipment lines; "5 = Wiking" added to the SS name list; the SS recruitment event no longer makes a second Wiking in 1944 games (CHANGELOG section 10). Only additions, nothing of yours changed | GER_1944.txt, GER_1944_nsb.txt, GER_names_divisions.txt, ss_recruitment_event.txt |
| 16 | New: **four 1945 operations** for Germany (CHANGELOG section 11). **Operation Sonnenwende** and **Operation Spring Awakening**: a popup when the front makes them relevant; the decision (50 PP) sets fuel, rifles and artillery aside during the preparation (7 / 10 days) and returns exactly that at the launch, then +15% attack on German soil for 12 days / +10% against the Soviet Union for 14 days. **Courland**: a popup when the pocket is cut off, then a decision (50 PP, 30 days, Libau or Windau held) that ships every German division in Kurzeme to the first Baltic port still held; or hold it, with your Festung values on the two ports. **Sailors to the Front** (50 PP, from Feb 1945): +1,000 manpower, 10 convoys laid up, three naval infantry divisions on the historical dates (ordinary infantry, so not counted as special forces; 50% equipped, no experience). **Not play-tested yet** | 8 new files `GER_1945_operations_*` |
| 17 | New: **Germany's last reserves** (CHANGELOG section 12), each event once and only in its historical window: **Estonian Mobilisation** (Feb 1944, +38,000); **Collaborators Flee East** (once Paris is lost, +3,000, with the neutral volunteers); **Hungarian SS Divisions** (30 days after your Arrow Cross coup, up to 7,500 moved from Hungary to Germany); **Luftwaffe Men to the Front** (decision, 50 PP, from Sept 1944: +75,000, then −10% air missions for 90 days); **The Last Swedish Deliveries** (late Sept 1944: 3 trains, 137 trucks, 1,800 support equipment, 250 fuel, 35 days of aircraft 13% cheaper); **Eastern Workers and Prisoners Volunteer** (Feb 1945, a choice: +15,000 and −1% factory output for 180 days); **Round-ups Behind the Front** (1945, manpower below 200,000 or the enemy at Berlin: +15,000). **Not play-tested yet** | 6 new files `GER_reserves_*` |
| 18 | `mod/.gitattributes`: `* text=auto` becomes `* -text`, so every clone gets the files byte-for-byte (the old setting converted the line endings of 45 files on Windows). The game doesn't read this file. The project is also on GitHub now, with the mod in `mod/` (CHANGELOG section 13) | .gitattributes |

**Your call** (decisions made for you, easy to change):

- the special-forces mapping (for example GER → paratroopers_1 + _2), with no
  mastery added;
- the Australian states 870/871/873 now use the base game's manpower (you
  can restore the old files under the new names);
- the Burma oil decisions were not added;
- your GER decisions, germany focus tree and artillery techs were **not**
  merged with 1.19.3 and are unchanged (apart from the Volkssturm focus's
  unit block, change 11);
- Volkssturm (all set in `GER_volkssturm_effects.txt` and
  `GER_volkssturm_decisions.txt`): the rifle shares (Oscar widened the
  Bayreuth mix; the 4% Danish share has no source), Czech rifles counted as
  German (Czechoslovakia doesn't exist in 1944), 25 political power per
  decision, and the per-state numbers.

## Check it yourself

1. **Read the patches.** Each one is one change with the full explanation
   and the exact diff.
2. **Rebuild it from your Steam version.** Copy the Workshop folder
   (without its `.git`) somewhere that is *not* inside another git
   repository, then:
   ```
   git -c core.autocrlf=false apply --whitespace=nowarn <package>/patches/*.patch
   sha256sum -c <package>/docs/checksums/mod-files.sha256
   ```
   All 943 files should say OK, which shows `mod/` is exactly your Steam
   version plus these patches. (If `git apply` succeeds but files don't
   change, the folder is inside another git repository and git silently
   skips the paths. Move it, or set `GIT_CEILING_DIRECTORIES`.) This exact
   test was run before packaging and passed.
3. **Run the game** with `-debug` and compare `logs/error.log` with
   `docs/game-logs/`.
4. **Optional:** run `python tools/check_province_modifiers.py`,
   `check_structure.py` or `check_references.py` next to `mod/`. Set
   `HOI4_PATH` if your game isn't in the default Steam folder.

## Test it in game

Create `Documents\Paradox Interactive\Hearts of Iron IV\mod\downfall_test.mod`
containing:

```
version="1"
name="1944 - Downfall (test)"
supported_version="1.19.*"
path="C:/full/path/to/this/package/mod"
```

In the launcher, make a playset with **only** this mod; don't enable it
together with the Workshop version. Play or observe (`observe` in the
console) past September 1944 as any country except Japan or China. If it
crashes, the newest folder in `Documents\Paradox Interactive\Hearts of Iron
IV\crashes\` shows why.

## Publish

Bring your copy in line with `mod/`: copy the changed files and delete the
three state files, or apply the patches. If your copy has changes that
aren't on Steam yet, use the patches. Then upload as usual.

The whole project is also on GitHub (github.com/gastav3/Hoi4_1944), with
the mod in `mod/`: upload that folder, not the repository root.

Note: the July upload included your old `.git` folder (history to 2024,
remote github.com/gastav3/Hoi4_1944), so subscribers can read that history.
You may want to leave it out next time.

## Known limits

- Not play-tested. Playing without some DLCs is not tested either.
- Nero Decree and Werwolf load cleanly but have not been tested in play yet.
- The Volkssturm focus and decisions load cleanly and their script ran
  without errors, but it hasn't been confirmed in play that the divisions
  appear (CHANGELOG section 6 has the test steps).
- Festung Berlin loads cleanly and its fort steps were run inside the game
  (right levels, no errors), but the chain hasn't been played through yet
  (CHANGELOG section 9 has console test steps).
- The four 1945 operations load cleanly and their effects ran inside the game
  without errors, but they haven't been played through yet (CHANGELOG
  section 11 has console test steps).
- Germany's last reserves (six events and a decision) load cleanly and their
  effects ran inside the game without errors, but they haven't been played
  through yet (CHANGELOG section 12 has console test steps).
- `tools/check_berlin_map.py` needs Pillow and numpy (`pip install pillow numpy`).
- 4 small issues that were already in your 1944 blocks were left alone:
  GER `wilhelm_keitel` and `joseph_goebbels`, and JAP `JAP_mitsumasa_yonai`,
  used as ideas although they're characters in 1.19; SIA tag
  `SIA_THAI_fascism` has no colour entry. None of these can crash the game.
- The 115 remaining error.log lines were all there before; they're listed
  in INVESTIGATION.md §8.
