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
