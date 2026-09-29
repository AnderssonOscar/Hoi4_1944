# 1944 - Downfall

A Hearts of Iron IV mod by **gastav3**: the Second World War from 1 January
1944. On the Steam Workshop:
[1944 - Downfall](https://steamcommunity.com/sharedfiles/filedetails/?id=3070639276).

## The September 2026 update

This updates the mod for HOI4 1.19.3, fixes bugs, and adds 1944–45 content.
**None of it has been play-tested yet.**

Nothing was moved: the mod stays at the top level of this repository, and
this repository's line-ending setting (`* text=auto`) is unchanged.

**How the commits are organised:**
1. **[`c56a5f1`](https://github.com/gastav3/Hoi4_1944/commit/c56a5f1) Sync with the Steam Workshop version of July
   2026.** This is the author's own work from the July upload that never
   reached GitHub (62 files, for example the new states in the Dutch East
   Indies, Malaya and Indochina). Nothing in it was written by Oscar or the
   AI assistant.
2. **One commit per change**, each with its full reason in the commit
   message: 26 in pull request #2, 5 more in pull request #3 (the home
   front 1944–45, a fix for the Courland popup, the fix for the crash when
   starting as the UK, five war measures for Germany, and a fix for two
   equipment mistakes in the update's own features), and 3 more in pull
   request #4 (Oscar's review of the new features, five flavour events, and
   the bridge at Remagen):

| Commit here | Change | CHANGELOG section | Update package |
|---|---|---|---|
| [`7ffb1d5`](https://github.com/gastav3/Hoi4_1944/commit/7ffb1d5) | Fix Ichi-Go province modifiers applied in the wrong state | 1 | [`e20698c`](https://github.com/AnderssonOscar/Hoi4_1944/commit/e20698c) |
| [`9c0e8b3`](https://github.com/gastav3/Hoi4_1944/commit/9c0e8b3) | Remove stale duplicate definitions of states 870, 871, 873 | 2 | [`ce4f33a`](https://github.com/AnderssonOscar/Hoi4_1944/commit/ce4f33a) |
| [`c1dbe61`](https://github.com/gastav3/Hoi4_1944/commit/c1dbe61) | Update supported game version to 1.19.3.0 | 3 | [`6fa793c`](https://github.com/AnderssonOscar/Hoi4_1944/commit/6fa793c) |
| [`0417681`](https://github.com/gastav3/Hoi4_1944/commit/0417681) | Netherlands focus tree: rebuild on 1.19.3, keep the RKN edit | 3 | [`2d80d87`](https://github.com/AnderssonOscar/Hoi4_1944/commit/2d80d87) |
| [`976e529`](https://github.com/gastav3/Hoi4_1944/commit/976e529) | cosmetic.txt: rebuild on 1.19.3, keep the mod's 17 own tags | 3 | [`f646e4a`](https://github.com/AnderssonOscar/Hoi4_1944/commit/f646e4a) |
| [`5fa14c9`](https://github.com/gastav3/Hoi4_1944/commit/5fa14c9) | Fix a character and a focus ID renamed in 1.19 (Argentina, Australia) | 3 | [`8041896`](https://github.com/AnderssonOscar/Hoi4_1944/commit/8041896) |
| [`7d9606e`](https://github.com/gastav3/Hoi4_1944/commit/7d9606e) | Add base-game decisions the mod's older decision files lack | 3 | [`586de46`](https://github.com/AnderssonOscar/Hoi4_1944/commit/586de46) |
| [`47bc46e`](https://github.com/gastav3/Hoi4_1944/commit/47bc46e) | Add news event bftb_news.11 missing from the mod's older copy | 3 | [`0384e82`](https://github.com/AnderssonOscar/Hoi4_1944/commit/0384e82) |
| [`d101815`](https://github.com/gastav3/Hoi4_1944/commit/d101815) | Special forces: replace pre-1.19 doctrine techs with 1.19 sub-doctrines | 3 | [`c8dac21`](https://github.com/AnderssonOscar/Hoi4_1944/commit/c8dac21) |
| [`5a0f8ef`](https://github.com/gastav3/Hoi4_1944/commit/5a0f8ef) | Australia history: rebuild on 1.19.3, keep the author's 1944 content | 3 | [`4a17ff6`](https://github.com/AnderssonOscar/Hoi4_1944/commit/4a17ff6) |
| [`c88694e`](https://github.com/gastav3/Hoi4_1944/commit/c88694e) | Siam history: rebuild on 1.19.3, keep the author's 1944 content | 3 | [`d5c3c69`](https://github.com/AnderssonOscar/Hoi4_1944/commit/d5c3c69) |
| [`cdfb445`](https://github.com/gastav3/Hoi4_1944/commit/cdfb445) | Australia: re-apply the AST_domestic_industry fix (it is a 1.19.3 bug) | 3 | [`58a1a82`](https://github.com/AnderssonOscar/Hoi4_1944/commit/58a1a82) |
| [`18456dd`](https://github.com/gastav3/Hoi4_1944/commit/18456dd) | JAP decisions: add the rest of the Tauran border-incident chain | 3 | [`d55cf37`](https://github.com/AnderssonOscar/Hoi4_1944/commit/d55cf37) |
| [`7f5bfe4`](https://github.com/gastav3/Hoi4_1944/commit/7f5bfe4) | Add flavor event: Slovak National Uprising (29 August 1944) | 4 | [`7de1ce8`](https://github.com/AnderssonOscar/Hoi4_1944/commit/7de1ce8) |
| [`7c1b146`](https://github.com/gastav3/Hoi4_1944/commit/7c1b146) | Slovak uprising: Germany loses the 3,000 manpower, not Slovakia | 4 | [`a5982fe`](https://github.com/AnderssonOscar/Hoi4_1944/commit/a5982fe) |
| [`b41e8bc`](https://github.com/gastav3/Hoi4_1944/commit/b41e8bc) | Add Nero Decree and Werwolf (Germany, last-stand decisions) | 5 | [`76a0d54`](https://github.com/AnderssonOscar/Hoi4_1944/commit/76a0d54) |
| [`059efbb`](https://github.com/gastav3/Hoi4_1944/commit/059efbb) | Volkssturm: realistic levies, rifle mix and 1945 call-ups | 6 | [`e6c0034`](https://github.com/AnderssonOscar/Hoi4_1944/commit/e6c0034) |
| [`3021967`](https://github.com/gastav3/Hoi4_1944/commit/3021967) | Volkssturm bug check: raise units where Germany holds a state, not only where it holds all of it | 6 | [`d9d7888`](https://github.com/AnderssonOscar/Hoi4_1944/commit/d9d7888) |
| [`847b39b`](https://github.com/gastav3/Hoi4_1944/commit/847b39b) | Fix Konigsberg in Ruins: remove the ring fort, not forts in Africa | 7 | [`b88321a`](https://github.com/AnderssonOscar/Hoi4_1944/commit/b88321a) |
| [`fc01049`](https://github.com/gastav3/Hoi4_1944/commit/fc01049) | Fix Oder-Neisse Defence: build the Stettin fort in Stettin's own state | 8 | [`e13d45d`](https://github.com/AnderssonOscar/Hoi4_1944/commit/e13d45d) |
| [`eddc310`](https://github.com/gastav3/Hoi4_1944/commit/eddc310) | Fix "Destroy Antwerpen": hit Antwerp's port in Antwerp's own state | 8 | [`5fb4a0b`](https://github.com/AnderssonOscar/Hoi4_1944/commit/5fb4a0b) |
| [`3d6e75b`](https://github.com/gastav3/Hoi4_1944/commit/3d6e75b) | Add Festung Berlin: a five-event chain for the defence of Berlin | 9 | [`1fa3c2c`](https://github.com/AnderssonOscar/Hoi4_1944/commit/1fa3c2c) |
| [`10c5712`](https://github.com/gastav3/Hoi4_1944/commit/10c5712) | Add 5. SS 'Wiking' and 11. SS 'Nordland' to the 1944 start | 10 | [`00807c5`](https://github.com/AnderssonOscar/Hoi4_1944/commit/00807c5) |
| [`ad8ce09`](https://github.com/gastav3/Hoi4_1944/commit/ad8ce09) | Add four 1945 operations for Germany | 11 | [`97fad47`](https://github.com/AnderssonOscar/Hoi4_1944/commit/97fad47) |
| [`79d97af`](https://github.com/gastav3/Hoi4_1944/commit/79d97af) | 1945 operations: correct event texts against the sources | 11 | [`9c950e1`](https://github.com/AnderssonOscar/Hoi4_1944/commit/9c950e1) |
| [`f2ba254`](https://github.com/gastav3/Hoi4_1944/commit/f2ba254) | Add Germany's last reserves: six events and a decision | 12 | [`70d287a`](https://github.com/AnderssonOscar/Hoi4_1944/commit/70d287a) |
| [`90c19a8`](https://github.com/gastav3/Hoi4_1944/commit/90c19a8) | Add the home front, 1944-45: eight events for Germany | 14 | [`99c2aa4`](https://github.com/AnderssonOscar/Hoi4_1944/commit/99c2aa4) |
| [`bb7c0aa`](https://github.com/gastav3/Hoi4_1944/commit/bb7c0aa) | Courland: the popup itself unlocks the evacuation decision | 11 | [`96f4a17`](https://github.com/AnderssonOscar/Hoi4_1944/commit/96f4a17) |
| [`08d8589`](https://github.com/gastav3/Hoi4_1944/commit/08d8589) | Fix the crash when starting the 1944 game as the United Kingdom | 15 | [`e578b10`](https://github.com/AnderssonOscar/Hoi4_1944/commit/e578b10) |
| [`45d728e`](https://github.com/gastav3/Hoi4_1944/commit/45d728e) | Add five war measures for Germany: KONR, railways, students, weapons | 16 | [`ddda13e`](https://github.com/AnderssonOscar/Hoi4_1944/commit/ddda13e) |
| [`e126956`](https://github.com/gastav3/Hoi4_1944/commit/e126956) | Fix: 1945 operations lost rifles; Vlasov's air force got the wrong planes | 17 | [`470916b`](https://github.com/AnderssonOscar/Hoi4_1944/commit/470916b) |
| [`11aa2b9`](https://github.com/gastav3/Hoi4_1944/commit/11aa2b9) | Oscar's review: Vlasov's airmen, railway 90 days, weapons with the Volksopfer, KONR later and poorly armed | 18 | [`807249b`](https://github.com/AnderssonOscar/Hoi4_1944/commit/807249b) |
| [`12fa932`](https://github.com/gastav3/Hoi4_1944/commit/12fa932) | Add five flavour events: the Indian Legion, the Handschar, the Eastern Legions, Wiking, Nordland | 19 | [`04f75bb`](https://github.com/AnderssonOscar/Hoi4_1944/commit/04f75bb) |
| [`d9785e3`](https://github.com/gastav3/Hoi4_1944/commit/d9785e3) | Add the bridge at Remagen: an event with a real photo, and the collapse | 20 | [`222caf2`](https://github.com/AnderssonOscar/Hoi4_1944/commit/222caf2) |

## September 29 continuation

The remaining Wiking, first German bomb, Leningrad and Crimea changes,
Oscar's four pictures, and the invasion-repelled event are now included.
Overlord preparation ends before the launch window and minor Allied
territorial losses no longer block the launch decision. The new event
recognizes a western Allied enemy's beachhead, excluding friendly transfers.

The package checks pass (80 checks, including 29 Overlord and 52 invasion
event scenarios/calibrations). HOI4 1.19.3 starts with the same 115-line
error log as the previous version. An actual AI landing still needs a
complete campaign test. The news popup remains as the author left it.

## Documentation

The update package holds the same changes plus the full documentation and
the check scripts, at tag `final-2026-09-29-v16-codex` of
[AnderssonOscar/Hoi4_1944](https://github.com/AnderssonOscar/Hoi4_1944/tree/final-2026-09-29-v16-codex). There the mod sits
in a `mod/` folder, and the commit IDs are the ones in the right-hand column
above; the documents refer to those.

| Document | What it covers |
|---|---|
| [READ-ME-FIRST](https://github.com/AnderssonOscar/Hoi4_1944/blob/final-2026-09-29-v16-codex/docs/READ-ME-FIRST.md) | The update in short: every change in one table |
| [CHANGELOG](https://github.com/AnderssonOscar/Hoi4_1944/blob/final-2026-09-29-v16-codex/docs/CHANGELOG.md) | Every change: what, why, sources, how it was tested, in-game test steps |
| [VERIFICATION](https://github.com/AnderssonOscar/Hoi4_1944/blob/final-2026-09-29-v16-codex/docs/VERIFICATION.md) | How it was checked: 74 automated checks, the game's error logs, checksums |
| [INVESTIGATION](https://github.com/AnderssonOscar/Hoi4_1944/blob/final-2026-09-29-v16-codex/docs/INVESTIGATION.md) | The investigation of the reported crashes, including false alarms |
| [HANDOVER](https://github.com/AnderssonOscar/Hoi4_1944/blob/final-2026-09-29-v16-codex/docs/HANDOVER.md) | How to maintain and extend the project |
| [game-logs](https://github.com/AnderssonOscar/Hoi4_1944/tree/final-2026-09-29-v16-codex/docs/game-logs) | The game's error.log after each step |
| [tools](https://github.com/AnderssonOscar/Hoi4_1944/tree/final-2026-09-29-v16-codex/tools) | The check scripts (Python 3) |

## How it was checked

- **In the update package:**
  - 74 automated checks;
  - the game's error.log after every change (115 lines, unchanged by every
    addition since the 1.19.3 update);
  - in-game runs of the new effects, during the game's setup and, since the
    war measures, in a running game with the stockpile measured;
  - a rebuild test: the Steam version plus the patches reproduces the mod
    exactly.
- **For this repository:** after every commit here, the files are identical
  to the tested package at the same step, ignoring only line endings (which
  this repository normalises).
  - Each commit shows the same line changes as the original, with one
    exception: the Siam history rebuild (`c88694e`) counts one more changed
    line. That's the file's last line, because the old file had no newline
    at its end.
  - The sync commit is identical to the Steam copy.
  - A fresh clone loads in the game with the same error.log as the tested
    version.
- **Not tested:** actual play, and playing without some DLCs.

## Status

- **Not play-tested yet.** Each feature's CHANGELOG section lists console
  commands to try it.
- **The UK crash is fixed:** starting as the United Kingdom crashed the game
  at once, also with the Steam version ([CHANGELOG](https://github.com/AnderssonOscar/Hoi4_1944/blob/final-2026-09-29-v16-codex/docs/CHANGELOG.md) section 15).
- **Crash reports not yet explained:** Bulgaria switching sides, Romania's
  12-day decision and the Volkssturm focus (redesigned anyway). "D-Day seems
  broken" needs a description.

## Credits

*1944 - Downfall* is by gastav3. The September 2026 update was prepared by
Oscar Andersson with an AI assistant (Claude). Everything is documented so it
can be checked without trusting the AI.

The Remagen event picture is made from the photograph "U.S. First Army at
Remagen Bridge" (about 17 March 1945), U.S. National Archives, NAID 195341,
via Wikimedia Commons; a work of the US Federal Government, in the public
domain.

## Continuation commit mapping

| This branch | Change | Package commit |
|---|---|---|
| `7bd3cff` | Add Wiking before Warsaw: a sixth flavour event, with Oscar's photo | `a2790cb` |
| `c55a9a6` | Add the first German atomic bomb: a flavour event, with Oscar's picture | `ef9dbce` |
| `d77c64b` | Add "Into Leningrad": a flavour event when the battle for the city begins | `a9a793d` |
| `658638b` | Add the Crimea: evacuate the 17th Army by sea, or hold Sevastopol | `204d7de` |
| `6ca6af2` | Fix the Crimea: choosing "Evacuate" now starts the evacuation | `b244eab` |
| `c981f77` | Leningrad: fire when we take the city itself, as Oscar asked | `97a806f` |
| `5c7f468` | Oscar's pictures: keep the whole Wiking photo; plain notes on the others | `df4cc07` |
| `4fd3bb4` | Complete the recovered D-Day repelled event with the prepared picture | `c0f1767` |
| `4fc5eec` | End Overlord preparation before launch and allow minor Allied territorial losses | `1296bb8` |
| `bc4018d` | Recognize D-Day only when a western Allied enemy holds a coast province | `46c665a` |
