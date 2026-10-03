# Handover to Codex, 3 October 2026

Written by Claude for whoever continues (Codex). Claude was running out of
usage in the middle of an investigation. Read this first, then
`docs/HANDOVER.md` (the general project notes) and `docs/CHANGELOG.md`
(sections 1–29, every change with its reason and evidence).

**The open problem in one line:** after the mod update was published on
Steam, players report that Germany "becomes democratic" and that a "Soviet
civil war" starts after a few days. The cause is **not found yet**. The
investigation log and the next steps are below.

---

## 1. Where everything is

| Thing | Location |
|---|---|
| Package repository (this one) | `C:\Users\Ander\Desktop\Projects\1944-Downfall`, branch `main`, pushed to `github.com/AnderssonOscar/Hoi4_1944` branch `update-package` |
| The mod inside it | `mod/` (988 files). Baseline = commit `253cea1` = the July 2026 Steam version |
| The author's repository (the brother, "gastav3") | `github.com/gastav3/Hoi4_1944`, mod at the top level, his line-ending setting. Never restructure it, never force-push |
| Pull requests | #2, #3, #4 all **merged** by the author. #4 merged 30 Sep 2026 20:41 UTC (merge `afa6dc8`, head `ae5135e`) |
| On Steam now | Workshop item 3070639276 = the author's main after PR #4 (= this package's `mod/` at `bb94b9e`, plus his README). Updated 30 Sep, minutes after the merge |
| Latest package tag | `final-2026-09-30-v18` (commit `8dcbbdb`); zip on Oscar's Desktop: `1944-Downfall-update-1.19.3.zip` |
| Local test copy the game loads | `Documents\Paradox Interactive\Hearts of Iron IV\mod\1944-Downfall-local` via `downfall_local_fixes.mod` (own descriptor, no Workshop ID). Refresh it from `mod/` before testing |
| Investigation tools from this session | `tools/investigation/` (see section 7) |
| Game | HOI4 1.19.3, all DLCs, `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` |

## 2. Oscar's standing rules (do not break these)

- The brother **distrusts AI**: every change small, sourced, documented,
  with evidence. One commit per change with its reason.
- **Never edit the Steam Workshop folder.** Never restructure or force-push
  the brother's repository. Check a pull request's state
  (`gh pr view N --repo gastav3/Hoi4_1944 --json state`) before pushing to
  its branch.
- **The author's D-Day mechanics (`common/decisions/Allies_1944.txt`) are
  not to be touched.**
- Never crop or censor historical photos; describe alt-history
  illustrations neutrally.
- Never `git add -A` in `C:\Users\Ander` (the home folder is itself a git
  repository). Never `git reset --hard` with uncommitted work.
- Testing on Oscar's PC: never start or kill HOI4 while he is using it;
  always back up and restore `dlc_load.json` (his playset),
  `settings.txt` and `save games\autosave.hoi4`. The scripts in
  `tools/investigation/` do this.
- A plan being approved is not permission to build; an explicit request is.
- Oscar denied computer-use (screen control). Don't ask again.
- Commit messages end with a `Co-Authored-By:` line for the assistant.

## 3. What Oscar asked in this session (in order)

1. "nordland is in berlin at start, should it be there?" then "you can run
   it and fix it". **Done**: CHANGELOG section 29, commit `bb94b9e`,
   package v18, in PR #4, on Steam.
2. "make sure it all works, then look if any other SS divisions that
   historically exist 1944 are missing, and also where grossdeutchland is".
   **Answered, nothing built**: see section 8 below. Oscar has not yet
   chosen whether to add the missing SS divisions.
3. (3 October) "after the new update we did we got many complaints … seems
   many have the same issue, why". **In progress**: sections 4–6.
4. "You are running out of usage, first and foremost, write proper
   documentation, and handover doc for chatgpt codex to take over".
   **This file.**

## 4. The complaints (Steam Workshop comments, verbatim)

Page: `https://steamcommunity.com/sharedfiles/filedetails/comments/3070639276`
(times as Steam showed them to Claude, probably US Pacific time).

| When | Who | Text |
|---|---|---|
| 28 Sep 10:34am | the author | "Updated" (the first upload of the update: PR #2 content; PR #3 content followed on 29 Sep, PR #4 on 30 Sep) |
| 29 Sep 5:08pm | ALİ | "I dont know why but when ım playing with germany the german reich demands me be his puppet and it triggers the country to go democratic." |
| 30 Sep 1:12am | Kenan Evren (= Oscar) | asks ALİ who he played, what date, which DLCs. No answer yet |
| 1 Oct 10:17am | Señor Dirlewanger | "Why I became democratic? xD" (no country named) |
| 2 Oct 4:31am | bog | "the soviet civil war popped off after a few days" |
| ~2 Oct | the author | "What dlcs are you playing with?" No answer yet |

Before 28 September the comments are about crashes only. So the reports
started with the update. Two readings are possible and **neither is
proven**:

- the update changed something that causes this; or
- before the update the mod crashed for most players on HOI4 1.19, and now
  that it runs they reach older problems (the author's files plus HOI4
  1.19.3's own files).

ALİ's report came **before** PR #4 was published, so if all three reports
have one cause, it is in the PR #2/#3 content (commits up to `470916b`),
not in the SS names fix of v18. That is not certain either: the reports may
have different causes.

An earlier answer of Claude's (30 September) said ALİ's report was "not
reproduced, not our update". That conclusion was too quick. Treat it as
unproven.

## 5. Investigation log (3 October)

### 5.1 Checked and ruled out

- **The base-game Soviet decision added in `586de46`**
  (`common/decisions/SOV.txt`): it is only
  `SOV_cancel_the_japanese_resource_rights_to_sakhalin_decision`. Not
  related.
- **The generic low-stability crisis** (base game
  `events/stability_events.txt`, `stability.33`: a fascist or communist
  country gets a democratic civil war). It needs draft dodging and a failed
  crackdown, which takes months. Does not fit "after a few days".
- **`common/on_actions/16_taog_on_actions.txt`** (new 1.19 file with a
  civil-war effect): Australia only.
- **Soviet civil war scripts** (base game `events/NSB_Soviet.txt`,
  `NSB_soviet_communist_civil_war.*`, `NSB_Soviet_fascist_civil_war.001`):
  fired only by the opposition focuses and their decisions in the Soviet
  tree. No automatic trigger found. A player (or a non-historical AI) who
  takes the opposition path gets a civil war by design.

### 5.2 Mechanisms found that can change Germany's government (not shown to be the cause)

1. **The SS / Wehrmacht "anger" chain.**
   - Base game `common/decisions/SS.txt` (the mod does not override it):
     eight "SS recruitment" decisions (Denmark, Norway, Netherlands,
     Belgium, France, Estonia, Latvia, Lithuania), 25 PP each, visible
     once `GER_expand_ss_recruitment` is completed. Each fires
     `ss_recruitment_event.1`–`.8`.
   - **Correction of an earlier statement:** Claude told Oscar that nothing
     fires the author's SS recruitment events. That was wrong: these
     base-game decisions do (they use `country_event = ss_recruitment_event.N`).
   - The mod's `events/ss_recruitment_event.txt` is an **older copy** of
     the base-game file. In the current base game the anger system is
     commented out; in the mod's copy `SS_resolve_effects_ss = yes` is
     **active** in the third option of every recruitment event
     ("small group of specialists": `SS_anger` +10), and
     `add_to_variable wehrmacht_anger` is active in the first two.
     (`SS_resolve_effects_wehrmacht` is commented out in both.)
   - Base game `common/scripted_effects/SS_scripted_effects.txt`,
     `SS_resolve_effects_ss`: from `SS_anger` 30, "Himmler plots"; from 40,
     a 10–15% chance of an assassination attempt
     (`ss_recruitment_event.24`); then `.26` "power struggle", whose
     options start civil wars (`neutrality`, or
     `ruling_party = neutrality` with fascist rebels).
   - So a **player who picks the third option four or more times** can end
     in a German civil war within days. The result is non-aligned, not
     democratic, and there is no "puppet" text, so it does not match ALİ's
     words well. A player comment of 21 Aug ("Idk if this would trigger
     civil war") shows players use these decisions.
   - In the observed AI game (5.3) `SS_anger` and `wehrmacht_anger` stayed
     0 for the first 8 days.
2. **The Götterdämmerung "influence" spirits.**
   - Base game `common/ideas/GER.txt` (not overridden by the mod):
     `GER_democratic_influence`, `GER_fascism_influence`,
     `GER_neutrality_influence`, `GER_communist_influence`. Each is
     cancelled when that ideology passes 45% (communism 40%), and its
     `on_remove` fires `wuw_GER_realpolitik.27/.28/.29` or
     `wuw_GER_diplomacy.75` in the country that held it.
   - Those events (mod `events/WUW_Germany.txt`, lines about 4268 and
     17687–17860) do exactly what players describe:
     `start_civil_war = { ideology = ROOT ruling_party = democratic … }`,
     i.e. the country's government becomes democratic and the old regime
     becomes the rebel side. `.75` does the same with communism, which
     would look like a "Soviet civil war" if the Soviet Union held
     `GER_communist_influence`.
   - The spirits are handed out by Germany's influence decisions and
     focuses (mod `common/decisions/GER.txt` about lines 14900–15650 and
     21400–21700, `common/national_focus/germany.txt` about 8700,
     `events/WUW_Germany.txt` `wuw_GER_diplomacy.10`, `.72`, `.73`).
   - **Not found:** any way Germany itself or the Soviet Union gets one of
     these spirits in a 1944 game. No history file adds them. This needs a
     save from an affected game, or a search of a save for
     `GER_*_influence`.
3. **"Demands we become their Client State"** is a real event title
   (`wuw_GER_realpolitik.7` and `.13`), which matches "demands me be his
   puppet", but those are sent by German focuses to Lithuania and similar
   targets, not to Germany.

### 5.3 The observed game (published version, all majors AI)

Run with `tools/investigation/politics_run.ps1` as Switzerland (`SWI`), so
Germany and the Soviet Union are AI, with a temporary logger
(`tools/investigation/zz_TEMP_politics_log.txt`, test copy only) that
writes every government change, capitulation, peace conference, puppeting,
annexation and civil war to `game.log`.

**At setup (1 January 1944, 12:00–13:00), on the published version:**

- `on_capitulation`: Belgium → Japan; **Poland → Germany; Yugoslavia →
  Germany; the Philippines → Japan**; Dutch East Indies → UK; **Burma →
  Japan**.
- Greek civil war set up by the mod (D04 "Kingdom of Greece" against GRE
  "Hellenic State"); D04 capitulates to Germany on 2 January and goes into
  exile in the UK.
- **Peace conferences with loser HOL "German Netherlands"**: winners the
  Soviet Union, Mongolia, Tannu Tuva, and then the UK with every Allied
  country. Afterwards HOL is "Netherlands", democratic, and **leaves
  Germany's faction**; the Dutch East Indies leaves it too.
  - HOL is a German integrated puppet because of the author's own line in
    `history/countries/GER - Germany.txt` (about line 514,
    `set_autonomy = { target = HOL autonomous_state = autonomy_integrated_puppet }`),
    unchanged by the update. HOL's own history says `ruling_party = democratic`.
- Japan annexes British Malaya.
- 13:00: **the Italian civil war ends**: ITA "Repubblica Sociale Italiana"
  annexes D05 "Kingdom of Italy".
- Afterwards, up to 8 January: AI Germany stays fascist ("German Reich"),
  AI Soviet Union stays communist, no civil war in either;
  `SS_anger` and `wehrmacht_anger` 0.

**Not yet known: which of these setup events are new.** The same run on
the July baseline (`253cea1`) had not been done when this was written. See
5.5 for results added later, if any.

### 5.4 Main suspect: the UK start fix (`e578b10`, CHANGELOG section 15, in PR #3)

To stop the crash when starting as the UK, that commit:

- removed `add_to_faction = PHI`, `POL`, `YUG` from
  `history/countries/ENG - Britain.txt`;
- removed the colony status of Burma (UK history) and the Philippines (USA
  history);
- moved Yugoslavia's exile to `on_startup`
  (`common/on_actions/do_on_actions.txt`, which already exiled Poland,
  Burma and the Philippines there).

Consequence to check: Germany's history declares war on Poland and
Yugoslavia separately (`GER - Germany.txt` lines 1150–1151,
`declare_war_on = { target = POL/YUG type = annex_everything }`). With
Poland and Yugoslavia **no longer in the Allied faction**, those may be
separate wars in which the only enemy has no land, capitulates at setup and
may be peace-conferenced or annexed before `on_startup` can exile it. The
same for the Philippines and Burma against Japan. That changes who exists,
who is in which faction and which peace conferences happen on day one, and
a **human** Germany may get peace-conference screens that the AI resolves
silently. This is a hypothesis; the baseline comparison decides it.

Second suspect, lower: the v18 change (`bb94b9e`) completes two German
focuses in `on_startup` instead of in history. It was tested (same
focuses, ideas, political power, divisions) and ALİ's report predates its
publication, but the later two reports do not.

### 5.5 Results added after the first draft of this file

(Claude appends here if more runs finish. Start with section 6, step 1
unless a result below says otherwise.)

**3 October, about 15:25 local time:**

- The first observed game (published version, player Switzerland) reached
  15 January 1944: AI Germany still fascist "German Reich", AI Soviet Union
  still communist, no civil war in either, `SS_anger` and
  `wehrmacht_anger` 0, Germany's subjects unchanged (Albania, Croatia,
  Greece, Italy/RSI, RKG, RKN, Serbia, Slovakia). So with AI majors the
  problem does **not** appear in the first two weeks. It is probably tied
  to something a **human** player does or sees (decisions, event choices,
  a peace-conference screen), or to DLC or game-rule settings.
- **A plain-text save lists every fired event**: top-level block
  `fired_event_names={ … }`. It also has `faction={ … members={ … } }`
  blocks and `pending_events`. Use this on a save from an affected game,
  or on test saves, to see exactly which events ran.
- From the save of 30 September (German player, one game day, v18 mod;
  Claude's scratch file `save_fix2.hoi4`):
  - fired at start: `mod.start.1`, `mod.start.options.1`,
    `wuw_GER_reichskommissariats.3` ("The Leadership of Norwegen", from the
    author's `on_startup` line `activate_decision = GER_reichskommissariat_norwegen`),
    `ger_crimea.1` (our Crimea popup);
  - the Allied faction's members include `ICE POL BRM YUG PHI D04 COG`
    and **`HOL`**. So after our UK fix Poland, Yugoslavia, Burma and the
    Philippines still end up in the Allies as exiles (they are not
    annexed), and the Netherlands (HOL) ends up in the Allies after the
    setup peace conference;
  - the Axis faction: `GER SLO ALB HUN ROM BUL FIN SER ITA CRO GRE RKN RKG`.
- `wuw_GER_reichskommissariats.*` events only ask Germany who leads a
  Reichskommissariat. Not related.
- Claude tried to stop the test game early to save time; the harness
  refused to kill the process, so the run was left to finish. If a
  `hoi4.exe` is still running when you start, it may be that test game:
  check `tools/investigation` backups before anything else, and do not
  kill a game Oscar may be playing.
- **Still not done: the baseline run (section 6, step 1).** It is the next
  thing to do.

**3 October, about 15:45: the published-version run finished (31 game days).**
Files: Claude's scratch folder `smoke\run_pol_published\` (game.log,
error.log, save.hoi4; not in the repository, 84 MB).

- AI Germany on 31 January: still fascist, stability unchanged, political
  power 1974 → 358, **`SS_anger` 20, `wehrmacht_anger` −10**.
- The save shows Germany's flags `SS_recruitment_denmark`, `_norway`,
  `_netherlands`, `_belgium` and SS templates created. So **the AI takes
  the SS recruitment decisions within the first month**, and the SS anger
  chain of section 5.2 item 1 is running in every game. At `SS_anger` 30
  "Himmler plots" starts; at 40 and above assassination attempts become
  possible (10–15% each time the check runs). A human who takes all eight
  decisions in the first days and picks the third option reaches 40 after
  four of them.
- This chain is in the author's July files too (the event file is his
  older copy; the focus was already completed in his history), so it is
  **not new with the update**. It may still be what players hit now that
  the game no longer crashes early. Its outcomes are non-aligned or
  fascist civil wars, not "democratic", so it does not explain the wording
  of the reports by itself.
- AI Soviet Union on 31 January: communist, no civil war, political power
  1884 → 126.
- No `GER_*_influence` spirit anywhere in the save.
- `fired_event_names` in a save holds only some events (42 here; probably
  the fire-only-once ones), so it is a partial record.
- Only civil war in the whole month: the mod's own Greek one.
- The baseline run (July version, about ten game days) was started right
  after this; its result follows below if Claude got that far.

**3 October, about 15:50: the baseline (July version, `253cea1`) at setup.**
Read from the live game.log of the run `pol_baseline` (same logger, player
Switzerland).

- **The setup is almost the same as in the published version.** Present in
  both: the capitulations of Belgium, Poland, Yugoslavia, the Philippines,
  the Dutch East Indies and Burma; the Greek civil war; **the peace
  conference with loser HOL "German Netherlands" and 36 winners**, HOL and
  the Dutch East Indies leaving Germany's faction; Japan annexing Malaya;
  the Italian civil war ending at 13:00 with the RSI annexing the Kingdom
  of Italy.
- **The only differences:** in the baseline Poland, the Philippines and
  Burma go into exile in the UK during setup (`on_government_exiled`, the
  cause of the UK crash); in the published version they do so in
  `on_startup`. Burma capitulates "to Germany" in the baseline and "to
  Japan" in the published version.
- **Conclusion: the strange day-one events are the author's own setup, not
  something the update introduced.** This largely clears the UK start fix
  (section 5.4) as the cause. Section 6 step 2 (bisecting the UK fix) is
  therefore low priority.

**Also checked and ruled out on 3 October:**

- **The author's start popup** (`mod.start.options.1`): Normal Mode, Easy
  Mode, Disable Soviet Offensives. Nothing political.
- **Operation Panzerfaust** (`GER_operation_panzerfaust_events.01/.02`,
  "[Hitler] Demands Horthy's Resignation", Hungary becomes a German
  puppet): this would match "the German Reich demands me be his puppet" for
  someone playing **Hungary**, but in the mod's `events/WUW_Germany.txt`
  the author added `date < 1944.1.1` to its trigger, so it cannot fire in
  a 1944 game.
- **The author's Operation Margarethe** (`GER_operation_margarethe` in
  `common/scripted_effects/germany_scripted_events_mod.txt`, event
  `operation.margarethe.1`): after 18 March 1944, **only if Hungary is
  AI**; makes Hungary a German satellite with a non-aligned government.
  Not democratic, and not for a human Hungary.
- **`wuw_GER_diplomacy.76` "Demands We Subjugate"**: only on the communist
  Germany path.

**Where this leaves the question (Claude's view):**

1. The update did not change the day-one politics. With AI majors nothing
   goes wrong in the first month.
2. The only mechanism seen moving in a real game is the SS anger chain
   (section 5.2 item 1), which is older than the update. It can kill
   Hitler and start a civil war, but its results are non-aligned or
   fascist, not democratic.
3. "Playing with Germany" (ALİ) may mean playing an Axis minor, and the
   1 October report names no country. The reports may be about the
   author's side-switch scripts for Romania, Bulgaria, Finland or Italy
   (those do change governments), which were not examined in this
   session. **Next: read the author's Romania/Bulgaria/Finland/Hungary
   scripts in `events/mod_events.txt`, `common/scripted_effects/*_mod.txt`
   and `common/scripted_effects/update_daily.txt`, and run
   `politics_run.ps1 -Tag ROM`, `-Tag BUL`, `-Tag HUN`, `-Tag FIN` with the
   logger** (popups stay unanswered for the played country, but scripted
   government changes are logged).
4. The players' answers (country, date, DLCs, what they clicked) would
   decide it faster than anything else.

**More ruled out (3 October, about 15:55):**

- **Germany's alt-history branch.** `GER_oppose_hitler` (which starts the
  German civil war and leads to "The Return of Democracy",
  `wuw_GER_german_politics.01`) is mutually exclusive with
  `GER_remilitarize_the_rhineland`, and the 1944 history unlocks that focus
  (`unlock_national_focus`, history line about 570; the run's save lists
  it as completed). So neither a player nor a non-historical AI can take
  the branch. Germany's current focus in the AI run was
  `GER_hand_out_panzerfausts`.
- `wuw_GER_military_events.2` and `wuw_GER_releasable.2` (self-firing
  events that mention a democratic ideology): the first is a flavour event
  limited to before 1944; neither sets Germany's government.

**Not checked yet, worth doing:**

- **The Soviet tree with historical focuses off.** Is an opposition focus
  (left, right, exiles) open for the Soviet Union at the 1944 start, as
  `GER_oppose_hitler` would have been for Germany? Look in the mod's
  `common/national_focus/soviet.txt` for the focuses that fire
  `NSB_soviet_communist_civil_war.001/.004/.005/.007` and
  `NSB_Soviet_fascist_civil_war.001`, their `mutually_exclusive` and
  `available` blocks, and whether the 1944 history completes or unlocks the
  focus that excludes them. If the branch is open, an AI Soviet Union with
  historical focuses off (a lobby setting many players use) can start its
  civil war early, which would explain "the soviet civil war popped off
  after a few days" without any change of ours. The fix would be one
  `unlock_national_focus` line in the Soviet 1944 history, as the author
  did for Germany.
- **The same question for the Axis minors' trees** (Hungary, Romania,
  Bulgaria, Italy, Finland): a democratic branch open at the 1944 start
  would explain "Why I became democratic?".
- The test games here ran with the default lobby settings (historical AI
  focuses on). There is no known command-line switch for the other
  setting; a human has to start that game.

**State of the machine when Claude stopped:** the baseline run
(`pol_baseline`) was in its last minutes. Its script restores the playset,
settings, autosave and the test copy by itself. If in doubt, check:
`dlc_load.json` should enable only `mod/ugc_3070639276.mod`; `settings.txt`
should say `save_as_binary=yes` and `autosave="HALFYEAR"`;
`save games\autosave.hoi4` should be Oscar's (29 Sep 2026 15:55,
63,423,717 bytes); backups are in Claude's scratch folder
`smoke\politics-backup\`.

## 6. Next steps, in order

1. **Baseline comparison (most important).**
   ```powershell
   # export the July version next to the tools (not inside another git repo's working tree problem: this is only read by robocopy)
   git -C C:\Users\Ander\Desktop\Projects\1944-Downfall archive 253cea1 mod | tar -x -C <some folder>\export_253cea1
   powershell -ExecutionPolicy Bypass -File tools\investigation\politics_run.ps1 -Name pol_baseline -Tag SWI -MaxMinutes 45 `
     -Source <some folder>\export_253cea1\mod -TestFiles tools\investigation\zz_TEMP_politics_log.txt
   powershell -ExecutionPolicy Bypass -File tools\investigation\politics_run.ps1 -Name pol_published -Tag SWI -MaxMinutes 45 `
     -TestFiles tools\investigation\zz_TEMP_politics_log.txt
   python tools\investigation\politics_summary.py pol_baseline pol_published
   ```
   One game day takes 25–40 s; a run to the 1 February autosave takes
   about 15–20 minutes and shows the game window. `politics_summary.py`
   prints the setup events of each run and what is only in one of them.
2. **If the setup differs** (Poland/Yugoslavia/Philippines/Burma
   capitulating, the HOL conference, Italy's civil war ending): bisect with
   exports of `e578b10^` and `e578b10` (the UK fix), the same way.
   - If the UK fix is the cause, the repair must keep the UK start from
     crashing (CHANGELOG section 15, check E in `tools/verify_update.py`,
     test with `tools/start_as_country.ps1 -Tag ENG`). One idea: keep the
     three in the faction but make the capitulation harmless, or put them
     back into the faction in `on_startup` right after exiling them. Test
     before choosing.
3. **Play-side check as Germany.** Run `politics_run.ps1 -Tag GER`. Event
   popups for the player stay unanswered, but peace conferences and
   government changes are logged. Look for
   `on_peaceconference_started` lines with Germany, and for Germany's
   `ruling` changing in the daily lines.
4. **Look in a save for the influence spirits.** In the plain-text save
   of a run (`run_<name>\save.hoi4`), search for `GER_democratic_influence`,
   `GER_fascism_influence`, `GER_neutrality_influence`,
   `GER_communist_influence`. If Germany or the Soviet Union holds one,
   trace who added it (section 5.2, item 2).
5. **Ask the players** (through Oscar): which country, which date, which
   DLCs, and whether they clicked the "SS recruitment" decisions or chose
   non-historical AI focuses. A save or screenshot would settle it.
6. **Soviet civil war:** check whether AI Soviet Union takes an opposition
   focus in the 1944 tree (`common/national_focus/soviet.txt` in the mod),
   with historical focuses on and off. If the opposition branch is open in
   1944, that may simply be the cause.
7. Whatever the cause: fix in one small commit, add a check to
   `tools/verify_update.py` and calibrate it with planted errors, add a
   CHANGELOG section 30, run the load test (error.log must stay at 115
   lines, identical to `docs/game-logs/28-after-ss-names_error.log`), then
   a **new pull request** to the author's repository (PR #4 is merged; do
   not push to its branch), built the same way as before (CHANGELOG
   section 13 and `docs/PR4-COMMIT-MAPPING.tsv` show the method: replay the
   package commit in his layout, files stored with LF).

## 7. Tools from this session (`tools/investigation/`)

All of them back up and restore Oscar's playset, settings and autosave, and
mirror `mod/` back into the local test copy when they finish. They refuse
to start while HOI4 is running.

| File | What it does |
|---|---|
| `politics_run.ps1` | One observed game from the 1944 start until the first monthly plain-text autosave. `-Source` = which mod folder to test, `-Tag` = the country "played", `-TestFiles` = temporary on_actions files to drop into the test copy, `-Bookmark 1944.1.31.12` = start later to get a save after one day. Output in `tools/investigation/out/run_<Name>/` (game.log, error.log, save.hoi4) |
| `zz_TEMP_politics_log.txt` | The logger (lines start with `PL`). Test copy only; never commit it into `mod/` |
| `politics_summary.py` | Summarises one run or compares two |
| `save_test.ps1` | The fast-save trick: moves the test copy's 1944 bookmark to 31 January so the monthly autosave comes after one game day |
| `list_ss_divisions.py` (in `tools/`) | Reads division names from a plain-text save |
| `provinfo.py` | Province lookup: state, map position, 1944 owner; `near <province> <radius>` |
| `loadtest_mod.ps1`, `clone_loadtest.ps1` | The standard load test (error.log at the main menu) for the test copy or a fresh clone |

PowerShell pitfalls met in this session: variable names are
case-insensitive (`$s` overwrote `$S`, `$p` overwrote `$P`); the game writes
`autosave_temp.hoi4` before renaming it; `verify_update.py` rewrites
`docs/checksums/mod-files.sha256` on every run, so run it once more on
clean files after calibrating a check.

Engine facts learned (also in CHANGELOG): `set_oob` in a country's history
is applied only after all history has run; `on_startup` runs after that;
a taken division number falls to the lowest free number that has an entry
in the name list; saves store division names as numbers.

## 8. Other open items

- **Missing SS divisions (Oscar's question, answered, nothing built).** The
  1944 start has LSSAH, Das Reich, Totenkopf, Wiking, Nordland,
  Hitlerjugend, Götz von Berlichingen and four unnamed "SS-Regiment"
  units (Finland, Leningrad, Brussels, Munich). Existing on 1 Jan 1944 but
  absent: 4 Polizei (Greece), 6 Nord (Finland), 7 Prinz Eugen (Bosnia),
  8 Florian Geyer (Hungary/Croatia), 9 Hohenstaufen and 10 Frundsberg
  (France; to Tarnopol end of March 1944), 13 Handschar (training), 14
  Galizien (training), 15 Latvian No. 1 (Eastern Front), 16
  Reichsführer-SS. Formed in January 1944: 18, 19, 20. Oscar was offered
  three options (add the ten; also the January ones by event; or only name
  the four regiments) and **has not answered**. Do not build before he
  chooses.
- **Großdeutschland** is in the start (province 3452, Cherkasy state, on
  the front about 35 km north of Kirovograd). Historically right.
- The four author's "SS-Regiment" units and the 11 focus-created SS
  divisions still take arbitrary names from the SS list (CHANGELOG
  section 29). Offered to give them plain names; not answered.
- Crash reports still unexplained: Bulgaria switching sides, Romania's
  12-day decision, "crashes when Germany loses" (`docs/INVESTIGATION.md`).
- "The Allies sometimes skip D-Day": unexplained; the author's D-Day file
  is not to be touched.
- Courland popup: only unlocks the decision (the Crimea popup was changed
  to start the evacuation at once after Oscar's play-test). Offered the
  same change; not answered.

## 9. How to verify the package before any delivery

```powershell
cd C:\Users\Ander\Desktop\Projects\1944-Downfall
python tools\verify_update.py        # 80 checks, must all pass; mod/ must be fully committed
```
Then the load test (error.log 115 lines), the rebuild test (July version +
`git format-patch --relative=mod 253cea1..HEAD -- mod` reproduces `mod/`,
checked with `docs/checksums/mod-files.sha256`), and for a pull request a
fresh clone compared file by file with `mod/` (ignoring CR). CHANGELOG
sections 13, 28 and 29 show each step with its evidence.
