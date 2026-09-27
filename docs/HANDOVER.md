# Handover: 1944 - Downfall bug-fix project

For the next assistant (ChatGPT or another AI) continuing this work.
Written by Claude on 2026-09-27. Read this first, then `docs/INVESTIGATION.md`.

---

## 1. The situation

Oscar's brother made the Hearts of Iron IV mod **1944 - Downfall** (Steam
Workshop id 3070639276; his Steam/GitHub name is "gastav3"). He has no time
to maintain it, and players report crashes. Oscar is trying to fix it with
AI help.

**The brother distrusts AI and expects it to fail.** The work only helps if:

- every claim has evidence he can check himself (file, line number, reason),
- every change is small, separate, and easy to review,
- uncertainty is stated honestly. "Suspected" is not "fixed".

Overclaiming is the quickest way to lose his trust. Record false alarms
instead of hiding them. Section 3 of INVESTIGATION.md does this on purpose.

## 2. Status

- **No mod file has been changed.** `git diff 253cea1 -- mod/` is empty.
- The five player reports have been investigated as far as reading the code
  allows. Results are in `docs/INVESTIGATION.md`.
- **One strong finding (A):** the Japan "Ichi-Go" scripts put province
  modifiers on provinces outside the state they run in. This is probably
  behind "the game crashes at a certain date". A fix is proposed but **not
  applied or tested in game**.
- **Four reports have no cause found** (Bulgaria switch, Romania 12-day
  decision, Volkssturm focus, UK). They need a crash report from the game.
  One report ("D-Day seems broken") needs a proper description first.

## 3. Where everything is

| What | Path |
|---|---|
| Project (git repo) | `C:\Users\Ander\Desktop\Projects\1944-Downfall` |
| Mod working copy | `...\1944-Downfall\mod\` (baseline commit `253cea1` = Workshop version, byte-identical, checked on all 914 files) |
| Findings log | `...\1944-Downfall\docs\INVESTIGATION.md` |
| This file | `...\1944-Downfall\docs\HANDOVER.md` |
| Check scripts | `...\1944-Downfall\tools\` (Python 3.12, run as `python`) |
| Steam Workshop copy (**never edit**) | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3070639276` |
| Base game (vanilla files for comparison) | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` (version 1.19.3.0) |
| Game logs | `C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV\logs\` (`error.log`, `game.log`) |
| Crash reports | `...\Hearts of Iron IV\crashes\` (empty as of 2026-09-27) |
| A Downfall save | `...\Hearts of Iron IV\save games\GER_1944_04_07_09.hoi4` (Germany, April 1944) |

## 4. Rules for continuing

1. **Only edit files in this repo's `mod/`.** Never edit the Steam Workshop
   folder, because Steam overwrites it. The brother publishes to Steam himself.
2. **Ask Oscar before changing any mod file.** A plan being approved is not
   permission to start. Wait for an explicit "go ahead".
3. **One fix = one git commit.** The message says what changed, why, the
   evidence, and how it was tested. If it wasn't tested in game, say so.
4. **Check against vanilla before calling something a bug.** If the base game
   does the same thing, it's probably valid syntax. Log it as a false alarm.
5. **Don't call a crash "fixed"** until it has crashed without the fix and
   stopped crashing with it. Until then, say "suspected cause".
6. **Keep file bytes intact.** Keep each file's encoding (UTF-8, with BOM if
   it had one) and line endings (the mod mixes CRLF and LF files). After an
   edit, `git diff --stat` must show only the lines you meant to change. If a
   whole file shows as changed, the line endings were converted, so revert.
   Localisation `.yml` files must be UTF-8 **with** BOM.
7. **Document every step.** Findings go in `docs/INVESTIGATION.md`. Applied
   changes go in `docs/CHANGELOG.md` (create it with the first applied fix).
   Keep this file's "Status" section current.
8. **Keep usage low.** Search with grep and read only the part of a big file
   you need. `mod/common/national_focus/germany.txt` alone is 900 KB.

## 5. Git quirks (important)

- The repo is **local only**. There's no remote and no backup. Suggest
  pushing it to a private GitHub repo if Oscar wants a backup.
- The system git config has `core.autocrlf=true`. This repo sets
  `core.autocrlf=false` and has `.git/info/attributes` containing `* -text`.
  That's needed because `mod/.gitattributes` (shipped by the author) says
  `* text=auto`, which would rewrite line endings. **`.git/info/attributes`
  is not copied when cloning.** In any new clone, run:
  `printf '* -text\n' > .git/info/attributes`
- `C:\Users\Ander` is itself a git repo (Oscar's home-folder backup). This
  project is ignored there (`/Desktop/Projects/*`). **Never run `git add -A`
  in `C:\Users\Ander`.**
- Useful commands, run from the project folder:
  ```
  git log --oneline                 # history
  git diff 253cea1 -- mod/          # every mod change vs the Workshop version
  git show <commit>                 # one change and its reason
  ```

## 6. Findings in short

| # | Report | Status |
|---|---|---|
| A | "Crashes at a certain date" | Strong suspect: `mod/common/scripted_effects/japan_scripted_events_mod.txt` lines 221 and 328 |
| B | Crash when Bulgaria switches sides | No cause found by reading |
| C | Crash in Romania's 12-day capitulation decision | No cause found by reading |
| D | Crash on completing the Volkssturm focus | No cause found by reading |
| E | "Playing UK crashes" | Author's comments show earlier UK crashes. May be the same as A. |
| F | "D-Day seems broken" | Needs a description of what's broken |

Full evidence, confidence and the proposed fix are in `docs/INVESTIGATION.md`,
section 2A.

## 7. Next steps, in order

1. **Ichi-Go fix (A).** Show Oscar the proposed change. Apply it only after he
   says yes (one commit). Then test it:
   play or observe (console command `observe`) a game as any country except
   Japan or China, past September 1944. Ideally run the same save once
   without the fix (does it crash?) and once with it (does it not?).
2. **Crash reports for B–E.** Launch HOI4 with `-debug` (Steam → HOI4 →
   Properties → Launch options), let the game reach the moment that crashes
   (observe mode is fine), then collect the newest folder in `crashes\` plus
   `logs\error.log` and `logs\game.log`. Read them before touching any code.
3. **Ask for details:** when does the UK game crash (on load, at a date, on an
   action)? What exactly is broken about D-Day (no landing, landing fails,
   wrong date)?
4. **Lower priority:** brace mismatches in `history/countries/RAJ - British Raj.txt`,
   `AST - Australia.txt` and `SER - Serbia.txt` (INVESTIGATION.md §3). Check
   what each one actually does in game before changing it.
5. **Keeping up with game updates:** mod files with the same path as a vanilla
   file replace it completely. Many are copies of 1.19.2 vanilla files. After
   a HOI4 patch, diff the old and new vanilla versions of each overridden file
   and port the relevant changes.

## 8. HOI4 facts that matter here

- A mod file with the same relative path replaces the vanilla file. The
  descriptor has no `replace_path`.
- `#` starts a comment. `else` written *inside* an `if` block is valid (vanilla
  does it 182 times).
- The mod's daily logic runs from `on_daily` in
  `mod/common/on_actions/do_on_actions.txt`, which calls `MOD_daily_update`
  and `MOD_daily_update2` (`mod/common/scripted_effects/update_daily.txt`).
  Each effect there checks its own tag, date and flags.
- `<state id> = { add_province_modifier = { ... province = { id = N } } }`:
  N must be a province inside that state. Vanilla never breaks this rule
  (0 of 82 cases). The mod breaks it twice (finding A).
- The console opens with the key under Esc. Commands used above: `observe`,
  `tag <TAG>` (switch country), `event <event id> <TAG>`.

## 9. The tools

Run from the project folder:

```
python tools/check_province_modifiers.py   # finding A: provinces outside their state
python tools/check_structure.py            # brace balance, template slot clashes
```

Both are read-only. `tools/pdx.py` is a small, tolerant parser for Paradox
script. It is **not** a full HOI4 validator: it catches the specific problems
above, nothing more. The province check only covers fixed state scopes
(`123 = { ... }`), not dynamic ones like `every_state`.

## 10. If you can't read the files directly

Ask Oscar to upload `docs/HANDOVER.md`, `docs/INVESTIGATION.md`, and the
specific mod file you need. Give him exact commands to run (PowerShell or
Git Bash) and ask him to paste the output back.
