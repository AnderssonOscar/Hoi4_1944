# 1944 - Downfall

A Hearts of Iron IV mod by **gastav3**: the Second World War from 1 January
1944. On the Steam Workshop:
[1944 - Downfall](https://steamcommunity.com/sharedfiles/filedetails/?id=3070639276).

This repository holds the mod and its **September 2026 update**: updated for
HOI4 1.19.3, bug fixes, and new 1944–45 content. Every change is its own
commit with its reason, and every claim can be checked again (see "Check it
yourself"). **None of the update has been play-tested yet.**

## What's here

| Folder | What it is |
|---|---|
| `mod/` | The mod itself. This is the folder the game loads and the one to upload to Steam. |
| `docs/` | The documentation. Start with [READ-ME-FIRST](docs/READ-ME-FIRST.md). |
| `tools/` | Python 3 scripts that re-check every claim, and a script that starts the game as one country. |

| Document | What it covers |
|---|---|
| [READ-ME-FIRST](docs/READ-ME-FIRST.md) | The update in short: every change in one table, and how to check and test it |
| [CHANGELOG](docs/CHANGELOG.md) | Every change: what, why, sources, how it was tested, in-game test steps |
| [VERIFICATION](docs/VERIFICATION.md) | How it was checked: 79 automated checks, the game's error logs, checksums |
| [INVESTIGATION](docs/INVESTIGATION.md) | The investigation of the reported crashes, including false alarms |
| [HANDOVER](docs/HANDOVER.md) | How to maintain and extend the project |
| [game-logs](docs/game-logs/README.md) | The game's error.log after each step |

## Latest changes (29 September 2026)

- **Complete:** Oscar's pictures, Wiking before Warsaw, the first bomb,
  Leningrad, the Crimea evacuation (with the fix from Oscar's play-test) and
  the invasion-beaten-back event.
- **Codex finished it** after Claude reached its usage limit
  ([CODEX-CONTINUATION](docs/CODEX-CONTINUATION.md)).
- **The author's D-Day mechanics are untouched:** Codex's change to the
  Overlord decisions was reverted at Oscar's request.
- **Checked again** in a running game ([CHANGELOG](docs/CHANGELOG.md)
  section 28).
- **Package tag:** `final-2026-09-29-v17`.

## The update in short

- **HOI4 1.19.3.** With the mod loaded, the game's error.log went from 282
  lines to 115 (the base game alone gives 1).
- **Fixes:**
  - starting as the United Kingdom crashed the game at once (also with the
    Steam version);
  - Ichi-Go province effects that ran in the wrong states (a suspected crash
    cause);
  - three state files defined twice;
  - "Königsberg in Ruins" removing forts in Africa;
  - the Stettin fort and the Antwerp sabotage running in the wrong states;
  - line endings kept byte-exact in every clone;
  - two equipment mistakes in the update's own 1945 operations and home
    front (lost rifles, wrong aircraft).
- **New content:**
  - the Slovak National Uprising (flavour event);
  - the Nero Decree and Werwolf (decisions);
  - the Volkssturm redesigned (levies by state population, historical 1945
    call-ups);
  - Festung Berlin (event chain);
  - the SS divisions "Wiking" and "Nordland" in the 1944 start;
  - four 1945 operations: Sonnenwende, Spring Awakening, the Courland
    evacuation, Sailors to the Front;
  - Germany's last reserves: six events and a Luftwaffe decision;
  - the home front, 1944–45: eight events, from women's labour service to
    the class of 1929;
  - five war measures: expanding the KONR, emergency railway repairs, the
    student companies to the front, and two decisions on civilian weapons;
  - six flavour events (the Indian Legion, the Handschar, the Eastern
    Legions, Wiking at Cherkassy and before Warsaw, Nordland);
  - the bridge at Remagen, with a real photograph;
  - flavour events for the first German atomic bomb, Leningrad taken and
    the invasion beaten back, with Oscar's pictures;
  - the Crimea: evacuate the 17th Army by sea, or hold Sevastopol.
- **Scope:** 112 files differ from the July 2026 Steam version (33 edited,
  3 deleted, 76 new).
- **On Steam:** the author published pull request #3's content on 29 Sep
  2026. The author's own content was kept byte-for-byte everywhere, and
  that is checked by script.

The full list is the table in [READ-ME-FIRST](docs/READ-ME-FIRST.md); the
reasons and sources are in the [CHANGELOG](docs/CHANGELOG.md).

## Play or test it

1. Clone or download this repository.
2. In `Documents\Paradox Interactive\Hearts of Iron IV\mod\`, create
   `downfall_test.mod` containing:
   ```
   version="1"
   name="1944 - Downfall (test)"
   supported_version="1.19.*"
   path="C:/full/path/to/Hoi4_1944/mod"
   ```
3. In the Paradox launcher, make a playset with only this mod. Never enable it
   together with the Workshop version: two copies of the same mod at once
   break the game.

## How it was checked

- **79 automated checks** (`python tools/verify_update.py`): integrity, a
  fresh clone is byte-exact, exactly the intended files changed, the author's
  content unchanged, every fix and feature in place. Every check written for
  new content was shown to fail on deliberately planted errors.
- **The game's own error.log** after every change: identical to the updated
  baseline (115 lines). The logs are in `docs/game-logs/`.
- **In-game runs** of the new effects during the game's setup, with no errors.
- **Rebuild test:** the July Steam version (commit `253cea1`) plus the 45
  patches reproduces `mod/` exactly (987 files).
- **Not tested:** actual play, and playing without some DLCs.

## Check it yourself

```
git log --oneline -- mod/        # every change to the mod
git show <commit>                # one change with its full reason
git diff 253cea1 -- mod/         # everything that differs from the Steam version
python tools/verify_update.py    # re-runs all 79 checks
cd mod && sha256sum -c ../docs/checksums/mod-files.sha256
```

`verify_update.py` needs git, HOI4 1.19.3 and the Steam Workshop copy of the
mod. Set `HOI4_PATH` and `WORKSHOP_PATH` if they aren't in Steam's default
folders.

## History of this repository

- **Commit `253cea1`:** the mod exactly as published on Steam in July 2026,
  placed in `mod/`. It already contains everything from the author's GitHub
  history; that was checked file by file.
- **After that:** one commit per change, each with its reason, and
  documentation commits that record the checks.
- **Tags** `final-2026-09-27` to `final-2026-09-29-v17` mark each package
  prepared for the author.
- **The author's repository** (github.com/gastav3/Hoi4_1944) receives the
  same changes in his layout: pull requests #2 and #3 (both merged by the
  author) and pull request #4 (open: Oscar's review round, the flavour
  events, the bridge at Remagen). The mod stays at the top level there, and the
  commit IDs differ; CHANGELOG section 13 pairs them.

## Status

- **Not play-tested yet.** Each new feature's CHANGELOG section lists console
  commands to try it.
- **The UK crash is fixed:** it was reproduced with the Steam version, and
  the cause is in [CHANGELOG section 15](docs/CHANGELOG.md).
- **Crash reports not yet explained:** Bulgaria switching sides, Romania's
  12-day decision and the Volkssturm focus (redesigned anyway).
  "The Allies sometimes skip D-Day" is not explained; the author's D-Day
  decisions are left as they are. See [INVESTIGATION](docs/INVESTIGATION.md).

## For the author: publishing to Steam

If you merge the pull requests in your repository, nothing changes in your
setup or your Steam upload: the mod stays where it was. If you use this
package instead, upload its `mod/` folder, not the repository root. That
also keeps the `.git` folder out of the Workshop upload (the July 2026 upload
included it, so subscribers could read the old history). `descriptor.mod`
already says `supported_version="1.19.3.0"`.

## Credits

*1944 - Downfall* is by gastav3. The September 2026 update was prepared by
Oscar Andersson with AI assistants (Claude, continued with Codex). Everything is documented so it
can be checked without trusting the AI.
