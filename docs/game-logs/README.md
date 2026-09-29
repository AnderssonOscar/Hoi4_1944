# Game error logs (HOI4 1.19.3, all 28 DLCs on, 2026-09-27)

Each is `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` from
starting `hoi4.exe -debug` and waiting until the main menu (the mod's 1944
history runs at startup). Compare them with any diff tool.

| File | What was loaded | Lines |
|---|---|---|
| 1-base-game-no-mods_error.log | no mods | 1 |
| 2-workshop-version_error.log | Steam Workshop version (unchanged) | 282 |
| 3-after-fixes-A-G_error.log | this repo after commits e20698c + ce4f33a | 279 |
| 4-after-1.19.3-update_error.log | this repo after the 1.19.3 update (d55cf37) | 115 |
| 5-after-slovak-uprising_error.log | after adding the Slovak uprising event (7de1ce8); identical to 4 | 115 |
| 6-after-volkssturm_error.log | after the Volkssturm redesign (e6c0034; Nero Decree and Werwolf also included); identical to 5 | 115 |
| 7-after-volkssturm-bug-check_error.log | after the Volkssturm bug-check fix (d9d7888); identical to 5 | 115 |
| 8-after-konigsberg-fix_error.log | after the Königsberg in Ruins fix (b88321a); identical to 5 | 115 |
| 9-after-stettin-antwerp-fixes_error.log | after the Stettin and Antwerp fixes (e13d45d, 5fb4a0b); identical to 5 | 115 |
| 10-after-festung-berlin_error.log | after Festung Berlin (1fa3c2c); identical to 5 | 115 |
| 11-after-wiking-nordland_error.log | after adding Wiking and Nordland (00807c5); identical to 5 (this stage does not read the 1944 order of battle; see CHANGELOG section 10 for the load_oob test) | 115 |
| 12-after-1945-operations_error.log | after the four 1945 operations (97fad47, texts corrected in 9c950e1); identical to 5 | 115 |
| 13-after-last-reserves_error.log | after Germany's last reserves (70d287a); identical to 5 | 115 |
| 14-pull-request-2-clone_error.log | a fresh clone of pull request #2's branch (the author's layout, commit 80d1d1c) with Git's default settings (CRLF checkout); identical to 13 | 115 |
| 16-pull-request-3-clone_error.log | a fresh clone of pull request #3's branch (the author's layout, commit 58b8bce) with Git's default settings; identical to 15. A first run logged 15 extra lines, all from a debug-mode database reload ("Reloading Database: common/decisions", then the base game's CHL.txt): the freshly created files were still being touched. The rerun on the same clone had no reload and is identical; this file is the rerun | 115 |
| 22-after-legions-and-remagen_error.log | after the five flavour events (04f75bb) and the bridge at Remagen (222caf2); identical to 20 | 115 |
| 21-pull-request-3-review-clone_error.log | a fresh clone of the branch after Oscar's review round (the author's layout, commit 3435bbb, pushed after pull request #3 was merged; the same mod files as pull request #4's 8ecc7ba) with Git's default settings; identical to 20 | 115 |
| 20-after-review-round-2_error.log | after Oscar's review round (807249b); identical to 18 | 115 |
| 19-pull-request-3-extended-clone_error.log | a fresh clone of pull request #3's branch after it was extended (the author's layout, commit 66adcd0) with Git's default settings; identical to 18 | 115 |
| 18-after-war-measures_error.log | after the five war measures (ddda13e) and the equipment fixes (470916b); identical to 17. Also identical with only ddda13e applied | 115 |
| 17-after-uk-crash-fix_error.log | after the UK start fix (e578b10); identical to 15 except one line number: the UK history file is one comment line longer, so the old Swordfish icon warning moved from line 2051 to 2052 | 115 |
| 15-after-home-front_error.log | after the home front, 1944–45 (99c2aa4) and the Courland popup fix (96f4a17); identical to 13 | 115 |
