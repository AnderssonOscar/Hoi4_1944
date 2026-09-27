# 1944 - Downfall: update for HOI4 1.19.3 + bug fixes

Prepared on 2026-09-27 by Oscar, with an AI assistant (Claude). You don't
have to trust the AI for any of it: every change is listed with its reason,
every change is a patch you can read, and everything can be checked
independently (see "Check it yourself").

## In short

- **Starting point:** the version currently on the Steam Workshop (id
  3070639276, July 2026), unchanged apart from what is listed here.
- **27 files differ** from that version: 21 edited, 3 deleted, 3 new. Your own
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
  Volkssturm focus and the UK are **not** explained yet.

## What's in this package

| Item | What it is |
|---|---|
| `mod/` | the complete updated mod, ready to test or upload |
| `patches/` | every change as a patch (14, in order), each with its reason |
| `docs/CHANGELOG.md` | what changed, why, and the gameplay effects |
| `docs/VERIFICATION.md` | how it was checked: 47 automated checks, game error logs, checksums |
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
| 9 | New flavor event: the Slovak National Uprising (29 Aug 1944). Germany loses 3,000 manpower crushing it; Slovakia and Germany see it | 3 new files: events, on_actions, localisation |

**Your call** (decisions made for you, easy to change):

- the special-forces mapping (for example GER → paratroopers_1 + _2), with no
  mastery added;
- the Australian states 870/871/873 now use the base game's manpower (you
  can restore the old files under the new names);
- the Burma oil decisions were not added;
- your GER decisions, germany focus tree and artillery techs were **not**
  merged with 1.19.3 and are unchanged.

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
   All 914 files should say OK, which shows `mod/` is exactly your Steam
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

Note: the July upload included your old `.git` folder (history to 2024,
remote github.com/gastav3/Hoi4_1944), so subscribers can read that history.
You may want to leave it out next time.

## Known limits

- Not play-tested. Playing without some DLCs is not tested either.
- 4 small issues that were already in your 1944 blocks were left alone:
  GER `wilhelm_keitel` and `joseph_goebbels`, and JAP `JAP_mitsumasa_yonai`,
  used as ideas although they're characters in 1.19; SIA tag
  `SIA_THAI_fascism` has no colour entry. None of these can crash the game.
- The 115 remaining error.log lines were all there before; they're listed
  in INVESTIGATION.md §8.
