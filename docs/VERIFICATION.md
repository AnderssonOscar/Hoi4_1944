# Verification of the fixes and the 1.19.3 update (2026-09-27)

Everything below can be re-run: `python tools/verify_update.py` (46 checks,
prints PASS/FAIL) and `python tools/check_references.py`.

## Result: all 46 checks pass

| Area | What was checked | Result |
|---|---|---|
| Integrity | mod/ fully committed; all 911 mod files byte-identical to the commits | PASS |
| Integrity | Steam Workshop copy never touched (914/914 files = baseline) | PASS |
| Scope | exactly the 24 intended files changed, nothing else | PASS |
| Author's work | every line removed from his files is one of the documented fixes (checked line by line in 17 files) | PASS |
| Author's work | rebuilt files: his parts byte-identical (RKN edit, 17 cosmetic tags, AST 1944 block + 4 stockpiles, SIA 1944 block); all other content identical to 1.19.3 | PASS |
| Fixes | A (Ichi-Go), G (duplicate states), and every update item is present in the files | PASS |
| Game's error.log | each fixed error type is gone: duplicate states 3→0, special-forces techs 93→0, Netherlands focuses 39→0, decisions 2→0, event 1→0, renamed IDs 6→0 | PASS |

## Version and checksum

- **Game version:** the install is the official 1.19.3 build,
  `Operation Postern v1.19.3.0.c01a (5632)` (launcher-settings.json). Steam
  reports it fully updated (build 25205862, 2026-09-17), and no newer patch
  was found online.
- **Game checksum:** 5632 is the official 1.19.3 checksum. Unmodded saves on
  this PC from after the update (JAP_1942_02_23_20.hoi4, autosave.hoi4) record
  `c01a (5632)`, so the installed base-game files are genuine.
- **The mod's checksum** is different by nature: any mod that changes
  `common`, `events`, `history` or `map` changes it. The Workshop version's
  saves show `3ed9`. The updated version will have its own value, and all
  players need the same mod version for multiplayer. There is no "correct"
  value to check a mod's checksum against.
- **File checksums:** `docs/checksums/mod-files.sha256` lists SHA-256 for all
  911 mod files. Verified with `sha256sum -c` (all OK). After uploading to
  Steam, the Workshop folder can be checked the same way:
  `cd <workshop folder> && sha256sum -c <this file>`. Expect `descriptor.mod`
  and `thumbnail.png` to differ only if Steam rewrites them.

## Play-time references (check_references.py)

error.log at startup can't see events, national spirits, characters or
flag/name tags that are only used later in play. This check looks at all
123,758 such references in the game as loaded with the mod, and ignores the
base game's own issues:

| | Original Workshop version | After the update |
|---|---|---|
| Missing things caused by the mod | 11,853 | 4 |

- **11,848 of the original** were references to 84 flag/name (cosmetic) tags
  that the mod's old cosmetic.txt lacked. All are defined now.
- **The 4 left were already in the original**, inside the author's own 1944
  sections, which were deliberately not changed:
  - `history/countries/GER - Germany.txt`: `wilhelm_keitel`, `joseph_goebbels`
    as ideas (advisors are characters in current HOI4)
  - `history/countries/JAP - Japan.txt`: `JAP_mitsumasa_yonai`, the same kind
  - `history/countries/SIA - Siam.txt`: cosmetic tag `SIA_THAI_fascism` has no
    colour entry

  These are for the author to decide; none of them can crash the game (the
  line just does nothing).

## The package rebuilds exactly from the Steam version

Before packaging, a fresh copy of the Steam Workshop folder (914 files,
without `.git`) had the 13 patches applied with
`git -c core.autocrlf=false apply`. Result: all 911 files match
`docs/checksums/mod-files.sha256`, and the file list is identical (the 3
deleted files are gone, nothing extra). So `mod/` is exactly "Workshop
version + these patches", with nothing hidden.

A pitfall found while testing: the first attempt ran inside a folder that
sits within another git repository (Oscar's home folder). `git apply` then
silently skipped every path and still reported success. The checksum check
caught it (21 FAILED). Run it outside other repositories, or set
`GIT_CEILING_DIRECTORIES`.

## Not verified (so no guarantee here)

- **Actual play.** Only loading the game and its 1944 setup was tested. The
  Ichi-Go fix and the reported crashes (Bulgaria, Romania, Volkssturm, UK) can
  only be confirmed by playing.
- **Playing without some DLCs.** An attempt to switch DLCs off failed, so no
  claim is made. Test through the Paradox launcher.
- **Three heavily edited files not merged with 1.19.3:** decisions/GER.txt,
  national_focus/germany.txt, technologies/artillery.txt (see CHANGELOG §3).
