# Changelog: changes to the mod

Compared with the Steam Workshop version (id 3070639276), stored unmodified in
baseline commit `253cea1`. See every change at once with
`git diff 253cea1 -- mod/`.

## Not yet released (not on Steam, **not yet tested in game**)

### 1. Ichi-Go province modifiers applied in the wrong state (commit `e20698c`)

- **File:** `mod/common/scripted_effects/japan_scripted_events_mod.txt`, 2 lines
- **Change:** commented out `id = 7167` (line 221) and `id = 4028` (line 328),
  each with a note saying which state the province really belongs to.
- **Why:** these were the only 2 of 154 province references in the mod that
  point at a province outside the state they run in. The base game never does
  this (0 of 82). The author had already commented out the other uses of these
  two provinces (lines 165, 371, 413). Suspected cause of the "crashes at a
  certain date" report. Details: INVESTIGATION.md §2A.
- **Gameplay effect:** Ichi-Go stage 3 no longer puts its defence penalty on
  province 4028. It still applies to provinces 1023, 7095 and 1597, and the
  state-wide bonus on state 594 still applies. It also no longer leaves that
  penalty on 4028 for the rest of the game, which the old code did because
  its removal was disabled. The stage 2 line had no gameplay effect: it
  removed something that was never added.
- **Checked:** only these 2 lines differ; line endings unchanged; checkers
  show 0 wrong-state references; every Ichi-Go modifier that is added is
  removed again at the end; no other script uses this modifier.

### 2. States 870, 871, 873 were defined twice (commit `ce4f33a`)

- **Files deleted:** `mod/history/states/870-North West Australia.txt`,
  `871-South West Australia.txt`, `873-South West Queensland.txt`
- **Why:** the base game renamed its files for these states
  (`870-Pilbara-Kimberley.txt`, `871-Esperence-Goldfields.txt`,
  `873-Channel Country.txt`). A mod file only replaces a base-game file with the
  exact same name, so the game was loading two definitions of each state. The
  mod's copies came from a bulk sync in the author's commit `4ce7056`
  (2023-02-19) and were never edited. Apart from manpower and category, they
  match the base game's current files. Details: INVESTIGATION.md §2G.
- **Gameplay effect:** these three outback states now use the base game's
  values: 870 pastoral with 25,000 manpower (the old copy: wasteland, 1,000),
  871 105,000 (old copy: 50,000), 873 60,000 (old copy: 10,000). It's unknown
  which definition the game used before. At most, Australia gets about 129,000
  more manpower, which is small next to the 2,650,000 in its main state.
- **If the lower values were intended:** restore the old files under the base
  game's names, e.g.
  `git show 253cea1:"mod/history/states/870-North West Australia.txt" > "mod/history/states/870-Pilbara-Kimberley.txt"`
- **Checked:** each state now has exactly one definition; the province-to-state
  map is unchanged (10,272 provinces); nothing refers to the deleted file names.

### 3. Update to Hearts of Iron IV 1.19.3 (commits `6fa793c` … `d55cf37`)

The current game is 1.19.3 (released 2026-09-17). The mod said 1.19.2, but
many files it replaces were older copies from before 1.19 (Thunder at Our
Gates), so new base-game content broke. **Rule followed throughout: the
author's own content is kept byte-for-byte; only old base-game text is
updated, and missing base-game pieces are added.** How each file was
checked is in INVESTIGATION.md §8.

| Commit | Change |
|---|---|
| `6fa793c` | descriptor.mod: supported_version 1.19.2.0 → 1.19.3.0 |
| `2d80d87` | Netherlands focus tree = 1.19.3 file + the author's only edit (`RKN` may use the Dutch tree). Restores the 15 Thunder at Our Gates focuses (~60 errors) |
| `f646e4a` | cosmetic.txt = 1.19.3 file + the mod's 17 own tags (84 base-game tags were missing) |
| `8041896` | Argentina: character ID renamed in 1.19; a duplicate recruit removed. (Its Australia part was undone by `4a17ff6` and redone in `58a1a82`.) |
| `586de46`, `d55cf37` | JAP/SOV decision files: added base-game decisions they lacked (Tauran border-incident chain; Sakhalin decision) |
| `0384e82` | Added news event bftb_news.11, which the mod's Bulgaria tree fires |
| `c8dac21` | Special forces: dead pre-1.19 doctrine techs in 11 countries' 1944 setups → 1.19 sub-doctrines (mapping table in the commit message). Nobody was getting these doctrines before |
| `4a17ff6` | Australia history = 1.19.3 file + the author's 1944 block + his 4 stockpiles |
| `d5c3c69` | Siam history = 1.19.3 file + the author's 1944 block |
| `58a1a82` | Australia: fixes a Paradox bug in the 1.19.3 file (`AST_domestic_industries` → `AST_domestic_industry`) |
| `368cee9` | tools/rebase_helpers.py, used for the above |

**Gameplay changes to be aware of:** the 11 countries now actually get
special-forces doctrines (with Arms Against Tyranny, as before). Australia
and Siam start with the 1.19.3 setup plus the author's 1944 changes.

**Checked in the game** (error.log, all 28 DLCs on): Workshop version 282
errors → 115 after the update. Only 1 error is new: Paradox's own 1.19.3
Siam file retires a politician it only hires *without* Thunder at Our
Gates. It's harmless and left as Paradox wrote it. The mod's own checkers
are also clean (0 wrong-state modifiers, 0 duplicate states).

**Not done / not verified:**
- **Playing without some DLCs is not tested.** My attempt to switch DLCs
  off when starting the game didn't work, so that result was thrown away.
  Test it through the Paradox launcher.
- Three heavily edited files that 1.19.3 also changed were **not** merged:
  `decisions/GER.txt`, `national_focus/germany.txt` and
  `technologies/artillery.txt`. The relevant 1.19.3 changes (Reichskommissariat
  Australasien states, Second Treaty of Berlin conditions) are 1936–41
  content with little effect on a 1944 start, and merging safely needs the
  author. His versions are unchanged.
- Base-game Burma oil-field decisions (`BRM_blow_up_the_oil_fields`,
  `BRM_repair_the_oil_fields`) are missing from the mod's JAP.txt. Not
  added, because they'd add new 1944 gameplay; the author's call.
- The remaining 115 errors were already there before the update and are
  mostly harmless. INVESTIGATION.md §8 has the list.

### 4. Flavor event: Slovak National Uprising (commits `7de1ce8`, `a5982fe`)

Added on Oscar's request: a simple event, about 3,000 manpower lost.

- **New files only** (nothing existing changed; delete these three to remove it):
  `events/slovak_uprising.txt`, `common/on_actions/slovak_uprising_on_actions.txt`,
  `localisation/english/slovak_uprising_l_english.yml`.
- **When:** once, from 29 August 1944, if Slovakia is in Germany's faction, at
  war with the Soviet Union and not capitulated (checked daily for Slovakia
  only, via `on_daily_SLO`).
- **Effect:** **Germany** loses 3,000 manpower (the troops sent in to crush the
  uprising), applied once by the trigger. Slovakia loses nothing. The event is
  shown to Slovakia **and Germany**; its single option only shows the loss as
  a tooltip, so nothing is applied twice. (The first version, `7de1ce8`, took the
  manpower from Slovakia; `a5982fe` moved it to Germany, as Oscar intended.)
- **Picture:** `GFX_report_event_czech_soldiers_02` (base game: Czechoslovak
  soldiers at a machine gun), chosen after viewing six candidates.
- **Checked:** both script files parse; the text file is UTF-8 with BOM and
  every value is on one line; the game loads it, and error.log is identical
  before and after (115 = 115, 0 new); text.log has nothing about it.
- **See it quickly in game:** console `event slovak.uprising.1 GER` shows the
  pop-up (the console does not apply the manpower loss; the real trigger does).

### 5. Nero Decree and Werwolf (commit `76a0d54`)

Designed with Oscar; the plan was agreed before building, and every mechanic
was checked against the 1.19.3 game files first. Six **new** files, no existing
file changed: `common/decisions/`, `common/dynamic_modifiers/`, `common/ideas/`,
`common/on_actions/`, `events/` and `localisation/english/`, each named
`GER_last_stand_*`.

- **Both decisions:** Germany only, 50 political power each, appear once an
  enemy holds a German core state. The AI takes them then.
- **Where the effects work:** only in German core states held by an enemy
  of Germany. Each effect switches off automatically if Germany takes the
  state back, so German troops are never affected.
- **Nero Decree:** the occupier moves 10% slower and captures 50% less
  equipment there. When an enemy takes a German core state from Germany, the
  state is wrecked once, using the base game's own scorched-earth amounts:
  factories -2 each, infrastructure -3, rail -1.
- **Speer event (7 days later):** the AI follows history and usually lets
  Speer spare the factories. That halves the decree (-5% speed, -25% capture);
  new captures then lose only infrastructure (-1.5) and rail (-0.5), and the
  factories are spared.
- **Werwolf:** a national spirit gives +10% resistance growth, ceiling and
  garrison damage in occupied German land (the base game's standard values),
  and the occupier moves 5% slower in German core states.
- **Rail sabotage:** every month, where resistance is above 25%, the rails
  are cut for 35 days, so the occupier can't strategically redeploy there,
  and one rail level is damaged when a campaign starts. It is "repaired"
  once the occupier gets resistance down to 25% or lower.
- **Radio Werwolf news:** 14 days after the Werwolf decision, shown to
  Germany and its enemies.
- **Checked:** every file parses; no name clashes with the base game or the
  mod; all pictures and icons exist; the game loads with error.log identical
  (115 = 115); check N/W in verify_update.py (it also fails if a test
  threshold is ever left in).
- **Not tested in play yet.** Screen control was declined, so the capture
  hook, the Speer event and the rail sabotage haven't run in a game. The
  equipment-capture modifier is one the base game never uses; if play shows
  the game doesn't recognise it, it gets dropped (Oscar's decision).

### 6. Volkssturm: realistic levies, rifles and 1945 call-ups (commits `e6c0034`, `d9d7888`)

Oscar's request: realistic numbers, a realistic mix of rifles, only 40–75%
armed, and more call-ups in 1945 at the historical times, up to the real
maximum. The author's template, focus position, cost, availability, AI
weights and training-level change are **unchanged**. Only the focus's
unit-creation block (193 lines) was replaced and its tooltip rewritten.

**Before:** 32 divisions (160 militia battalions) in three stacks of 12, 8
and 12, each in one random German state. They were 65–100% equipped, 6 of them
with Germany's 1942-level weapons, and had no Italian rifles.

**Now, the focus (first levy, available from 1 Nov 1944 as before):**
- Every German core state that Germany still holds (controls) raises
  Volkssturm divisions by population, about one per 1.9 million people: under 0.95M
  none, 0.95–2.85M 1, 2.85–4.75M 2, 4.75–6.65M 3, above that 4.
- With all 38 German core states held, that's 42 divisions (210
  battalions). States already lost raise none.

**Four decisions** (war measures, 25 political power, once each):
- Each appears on the date its historical offensive began.
- Each can be taken once the front has reached its region, i.e. an enemy
  holds part of one of its states, or a neighbouring state.
- Divisions only appear in states Germany still holds (controls), and
  never on an enemy-held province (the game's default for `create_unit`).

| Decision | From | That day | Divisions (5 battalions each) | Total |
|---|---|---|---|---|
| The Eastern Gaue | 12 Jan 1945 | Soviet winter offensive from the Vistula | Königsberg 5, Ermland-Masuren 3, Danzig 1, Gdynia 1, Posen 5, Lower Silesia 7, Upper Silesia 3, Sudeten Silesia 1 | 26 |
| The Oder and Pomerania | 31 Jan 1945 | Red Army reaches the Oder north of Küstrin | Hinterpommern 4, Vorpommern 3, Brandenburg 3 | 10 |
| The Western Gaue | 8 Feb 1945 | Allied Rhineland offensive (Veritable) | Rhineland 2, Westphalia 2, Moselland 1, Weser-Ems 1 | 6 |
| The Battle of Berlin | 16 Apr 1945 | Soviet attack from the Oder on Berlin | Brandenburg (Berlin) 5 | 5 |

**Total:** 89 divisions = 445 battalions of 1,000 men. How it was sized:
- **The real maximum:** Hans Kissel, chief of the Volkssturm's command
  staff, estimated that over 700 Volkssturm battalions saw combat [1].
  - A battalion had 642 men on paper [2], or 576–649 depending on the
    levy [3]. That's about 450,000 men.
  - In HOI4 a militia battalion is 1,000 men.
  - The mod's Germany starts with 286 divisions, about real size, so the
    scale is roughly 1:1.
- **Why the larger share comes in 1945, and mostly in the east:**
  - In the east the Volkssturm fought mainly from mid-January to
    mid-April 1945: Breslau, Posen, the Oder line, Pomerania, Berlin [1].
  - Most battalions that saw combat came from the eastern border
    districts [3].
  - In the west, Volkssturm battalions gave up very quickly [1], so the
    western call-up is small.
- **Per state:** the numbers are split by population. Two places can be
  compared with sources:
  - **Lower Silesia** ends up with 9 divisions (45,000 men). That includes
    Breslau, defended by about 15,000 Volkssturm [1] (25,000 in 38
    battalions according to [3]).
  - **Brandenburg** ends up with 12 divisions (60,000 men), matching "about
    60,000 in the Berlin area, in 92 battalions" [2]. [4] gives 40,000 for
    the city itself.

**Rifles** (one source per division, drawn at random):

| Share | Rifles | Game equipment (maker, level) | Gau Bayreuth, 15 Jan 1945 [5] |
|---|---|---|---|
| 65% | Italian Carcano | Italy, 1918 | 17,562 (77%) |
| 13% | Gewehr 88 / Gewehr 98 | Germany, 1918 | 2,413 (10.5%) |
| 5% | Kar98k | Germany, 1936 | 543 (2.4%), plus 5 Gewehr 43 |
| 8% | French (Lebel, Berthier) | France, 1918 | 1,974 (8.6%) |
| 4% | Danish Krag-Jørgensen | Denmark, 1918 | none |
| 2% | Belgian Mauser | Belgium, 1918 | 129 |
| 1% | Czech vz. 24 | Germany (see below), 1918 | 134 |
| 1% | Dutch Mannlicher M95 | Netherlands, 1918 | 34 |
| 1% | Soviet Mosin-Nagant | Soviet Union, 1918 | 64 |

- **The Bayreuth list** (22,908 rifles) is the only complete inventory
  found. It covers one Gau in the south. Oscar decided the whole Reich gets
  fewer Carcanos and more Danish, Kar98k, Gewehr 88/98, Belgian, Czech and
  Dutch rifles.
- **Danish rifles are an assumption.** No source was found that the
  Volkssturm received Danish rifles; the Germans did seize and catalogue them.
- **Equipment levels:** "1918" is `infantry_equipment_0`. These were
  1880s–1890s designs, and Bayreuth had only 8 machine guns for 22,908
  rifles. The Kar98k is `infantry_equipment_1`.
- **Czech rifles count as German.** Czechoslovakia doesn't exist in 1944 in
  this mod, and no base-game example creates units with equipment from a
  country that doesn't exist. The Germans had taken these rifles over as
  Gewehr 24(t).
- **No rifles from countries that don't exist:** a foreign rifle source is
  only drawn while that country exists. Otherwise its share goes to the
  others.

**Equipment and training:**
- Each division starts 40, 50, 60 or 75% equipped (equal chance), with no
  training.
- Later they only get equipment from Germany's stockpile, and they're last
  in line (the author's template already has the lowest reinforcement
  priority).

**Technical note:** by default `random_list` uses the scope's seed. Several
divisions raised in one state on the same day would then all roll the same
rifles and equipment. Every list therefore uses `seed = random`, as the game's
effects documentation describes and as the base game does in loops.

**Files:**
- Changed: `common/national_focus/germany.txt` (focus) and
  `localisation/english/custom_mod_l_english.yml` (focus tooltip).
- New: `common/scripted_effects/GER_volkssturm_effects.txt` (template,
  population rule, rifle tables), `common/decisions/GER_volkssturm_decisions.txt`
  and `localisation/english/GER_volkssturm_l_english.yml` (20 texts).

**Checked:**
- **Check V** in verify_update.py covers: the population rule gives 42 with
  the 38 German cores; the decisions give 26/10/6/5 on the four dates; every
  rifle table sums to 100; the foreign-country guard; `seed = random`; the texts.
- A second check confirms, line by line, that everything removed from
  germany.txt was the old unit block.
- **Load test:** error.log is identical, 115 = 115 with 0 new lines
  (`game-logs/6-after-volkssturm_error.log`), and setup.log shows the 4
  decisions loaded.
- **Runtime test:** the unit-raising script was also run once while the game
  set up its history (a temporary line, removed afterwards). It gave no
  errors.
- **Inconclusive:** a second attempt to count the divisions it created
  failed. Germany's division count read 0 before and after, even for its
  regular army, during history setup.
- **Not confirmed yet:** that divisions actually appear. That needs a real
  game (see below).

**Bug check (commit `d9d7888`):** a review of `e6c0034` found one real
design bug and two smaller issues. All three are fixed:
- **Bug:** every spawn and the decisions' "held" test required Germany to
  control *every* province of the state. The Brandenburg state contains
  Berlin and Seelow, where the Soviet Oder bridgehead was before 16 April
  1945. So in a historical game the Berlin decision would have been locked
  exactly when it was needed, and the same goes for partly occupied East
  Prussia, Silesia or the Rhineland, where the Volkssturm actually fought.
  Now the state only has to be controlled by Germany.
- **Front test:** the "front has arrived" test missed an enemy holding only
  part of a region state. It now counts that too.
- **Unit owner:** units were created for the tag `GER`; now it's `ROOT`, the
  country that took the focus or decision (920 uses of that form in the
  base game). This way units can't go to another or non-existent country
  if Germany's tag ever changes.
- **Retested after the fix:** error.log 115 = 115 (`game-logs/7-after-volkssturm-bug-check_error.log`);
  the runtime test ran again with 0 errors; verify_update.py now also
  checks that every changed spot in germany.txt is inside the Volkssturm
  focus (52 checks, all pass).
- **Also checked, no problem found:** every trigger is valid in the scope
  where it's used (game documentation); every rifle maker has the needed
  rifle technology in its 1944 history (`infantry_weapons`, and
  `infantry_weapons1` for Germany's Kar98k); no other template in the mod
  is named "Volkssturm".

**Still open:** the reported crash "when completing the focus for the 32
Volkssturm divisions" was never reproduced or explained. The old
unit-creation code is gone, but that doesn't prove the crash is.

Sources:
- [1] de.wikipedia, *Deutscher Volkssturm* (Kissel's estimate, where and
  when it fought, Breslau, the west).
- [2] en.wikipedia, *Volkssturm* (642-man battalion; Berlin area: 60,000 in
  92 battalions).
- [3] warhistory.org, "Volkssturm I" (levy sizes, battalion strengths,
  eastern border districts, Breslau).
- [4] en.wikipedia, *Battle in Berlin* (40,000 elderly Volkssturm men, some
  First World War veterans; Hitler Youth).
- [5] ww2-weapons.com, "German Volkssturm Weapons" (Gau Bayreuth
  inventory, from Klaus Mammach, *Der Volkssturm*).
- Dates: Britannica, "The Soviet advance to the Oder" (12 Jan; the Oder
  north of Küstrin on 31 Jan); en.wikipedia, *Operation Veritable* (8 Feb)
  and *Battle of Berlin* (16 Apr).

**Test it in game:**
1. Play Germany. Open the console (the key under Esc) and enter
   `Focus.NoChecks`, `Focus.IgnorePrerequisites` and `Focus.AutoComplete`.
2. Click the Volkssturm focus. Divisions named "Volkssturm" should appear
   across Germany.
3. Open one and look at its equipment: mostly Italian flags, 40–75% strength.
4. The decisions appear under war measures from 12 Jan 1945 (and so on).
   `Decision.NoChecks` may let you take them early; it isn't known whether
   it also shows them before their date.

## How to test in game

A local copy of the fixed mod is registered as a separate mod,
**"1944 - Downfall (local fixes)"** (file
`Documents\Paradox Interactive\Hearts of Iron IV\mod\downfall_local_fixes.mod`,
pointing at this project's `mod\` folder).

1. In the Paradox launcher, create a new playset with **only** "1944 - Downfall
   (local fixes)". Never enable it together with the Workshop "1944 - Downfall";
   two copies of the same mod at once will break the game.
2. Optional: Steam → HOI4 → Properties → Launch options: `-debug`, for more
   detailed logs.
3. Start the 1944 game as any country except Japan or China and let it run past
   September 1944. Observe mode (console command `observe`) is fine.
4. If it crashes, note the in-game date and what was on screen. Then keep the
   newest folder in `Documents\Paradox Interactive\Hearts of Iron IV\crashes\`
   and `logs\error.log`.
5. Afterwards, switch back to your usual playset. To remove the test entry,
   delete `downfall_local_fixes.mod`.

On another PC, register the `mod/` folder the same way (a `.mod` file with its
`path`); docs/READ-ME-FIRST.md shows how.

## For the author (publishing)

38 files differ from the version on Steam: 23 edited, 3 deleted, 12 new (full list:
`git diff --name-status 253cea1 -- mod/`, or docs/READ-ME-FIRST.md). Each
change is also a patch in the package's `patches/` folder (one per commit,
with its reason), or can be viewed with `git show <commit>`.

To publish, bring your copy in line with the final `mod/` folder. Either copy
the changed files over your copy and delete the three state files, or apply
the patches. If your copy has changes that aren't on Steam yet, use the
patches so none of your work is overwritten. The three files must be
**deleted**, not just left out. Then upload as usual: `descriptor.mod`
already says `supported_version="1.19.3.0"`.

Note: the July 2026 upload contained your old `.git` folder (history up to
2024, remote github.com/gastav3/Hoi4_1944), so anyone subscribed can read
that commit history. You may want to leave it out of future uploads.
