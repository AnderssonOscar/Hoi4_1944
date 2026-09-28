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

### 7. "Königsberg in Ruins" removed forts in Africa (commit `b88321a`)

Found on 2026-09-28 by extending `tools/check_province_modifiers.py` to
building effects. Oscar asked for it to be fixed.

- **The bug:** news event `mod.news.5` ("Königsberg in Ruins") fires when the
  Soviets take Königsberg. Inside the Königsberg state (763) it removed 5 fort
  levels from the city (6332, correct) and from provinces 13372, 13371 and
  13370. In the current map those are in **Zambezi, Angola and Congo** (states
  891, 540 and 295), so the fortress's ring fort was never removed. The
  game's documentation doesn't say what a province outside the scope state
  does; at best nothing, at worst it acts on the African province.
- **The fix:** the author's `GER_festung_cities` focus builds exactly one ring
  fort next to Königsberg: province 11265, level 6. The map confirms it
  borders the city. The event now removes the author's 5 levels there. The
  three old blocks are kept, commented out, in the author's style.
- **Checked:** check K (only 6332 and 11265, both in state 763); every line
  removed is one of the three old blocks; the game loads with error.log
  identical (115 = 115, `game-logs/8-after-konigsberg-fix_error.log`).
- **Two more of the same kind** in the author's own code were fixed next, on
  Oscar's request (section 8):
  - `common/decisions/GER_mod.txt:280` builds a level-5 fort in Stettin
    (6282) inside Vorpommern (62), but Stettin belongs to Hinterpommern (63).
  - `events/mod_events.txt:400` and `:406` ("Destroy Antwerpen") remove
    and damage Antwerp's naval base (6598) inside state 6, but Antwerp is
    in state 977 in the current map.
  The other 22 findings are lines copied unchanged from the base game
  (Japan and Netherlands focus trees, GER.txt, SOV.txt), which does the same
  thing itself, so they are not the mod's bugs (INVESTIGATION.md §9).

### 8. Stettin fort and Antwerp sabotage ran in the wrong state (commits `e13d45d`, `5fb4a0b`)

Same kind of bug as sections 1 and 7, found by the same check. Oscar asked
for them to be fixed only if certain; both were double-checked against the
mod's and the base game's state files:

- **Stettin** (`common/decisions/GER_mod.txt`, decision "Oder–Neisse
  Defence"): the level-5 fort for Stettin (province 6282) was built inside
  state 62 (Vorpommern). Stettin belongs to state 63 (Hinterpommern);
  state 62's provinces are 349, 3207, 3258, 3312, 3340, 9388 and 13257.
  The block now runs in state 63. The decision's other forts (3207, Seelow
  9496, 3572, 9535) were already in the right states.
- **Antwerp** (`events/mod_events.txt`, event `german.sabotage.ports.8`,
  "Destroy Antwerpen"): removing 3 naval-base levels and damaging Antwerp's
  port (province 6598) ran inside state 6, which is Flanders (its only port
  is province 6560). Antwerp is state 977, with its level-8 naval base on
  6598. The game's documentation says `damage_building` finds province
  buildings through the state it runs in, so the sabotage couldn't find
  Antwerp's port. The block now runs in state 977. The other six port
  sabotage events were already correct.
- **Change:** one line each (the state number), plus a comment.
- **Checked:** check S/A fails if any province effect in the three fixed
  files points outside its state. Run on the original files, it finds all
  6 old wrong references; on the fixed files, none. The game loads with
  error.log identical (115 = 115, `game-logs/9-after-stettin-antwerp-fixes_error.log`).
  The province checker now reports only the 22 base-game lines.

### 9. Festung Berlin: an event chain for the defence of Berlin (commit `1fa3c2c`)

Asked for by Oscar: when the enemy approaches Berlin, stronger defences in and
around the city, a few weak emergency units, noticeably harder to take but
balanced and realistic, with events for immersion. The plan was agreed and
reviewed for realism before building. Six **new** files, no existing file
changed.

**Oscar's decisions:**
- Keep the author's rule that Berlin's Festung bonus is for a human-led
  Germany only.
- No "open city" option.
- Weidling gets a combat bonus (a game bonus, not history).
- Enemies 10% slower in Brandenburg.
- Three emergency divisions.

**The chain** (checked once a day for Germany; each event fires once):

| # | Event | Fires when | Effect |
|---|---|---|---|
| 1 | The Berlin Defence Area | an enemy holds part of any state bordering Brandenburg: Hannover, Thüringen, Mecklenburg, Vorpommern, Sachsen, Ostmark | forts built over six weeks: Berlin to level 2, 4, then 5 (every three weeks); the five provinces around Berlin to 1, then 2 |
| 2 | The Seelow Heights | the enemy holds one of Seelow's neighbours beyond Brandenburg (Küstrin 3473, 537, 3572, 3207) | Seelow to fort level 2, then 4 three weeks later; +10% defence and +50% maximum dig-in there while Germany holds it |
| 3 | Clausewitz | Seelow falls, or the enemy holds one of the five provinces around Berlin | 3 weak emergency divisions in Berlin (Berlin police, Hitler Youth, other emergency units; untrained, 50–75% equipped); Brandenburg bonus (below); for a human-led Germany without the author's Festung Cities focus, his Festung bonus in Berlin (+20% defence, +75% maximum dig-in, −25% supply use); world news |
| 4 | Weidling Takes Command | 3 days after Clausewitz, if Berlin still holds | Weidling (in the mod as a corps commander) gains the base game's "urban assault specialist" trait (+10% attack and defence in cities) |
| 5 | Berlin Is Encircled | the enemy holds all five provinces around Berlin (at the earliest 3 days after Clausewitz) | story only |

- **"Clausewitz"** was the code word Hitler gave on 20 April 1945, the day
  after the Seelow front broke. It made Berlin a front-line city: Wehrmacht
  and SS offices were evacuated and files destroyed. In the chain it marks the
  moment the city itself becomes the battlefield.
- **The Brandenburg bonus:** in the game "Brandenburg" is one state (64) of 16
  provinces, including Berlin, Potsdam, Magdeburg and Seelow. While Germany
  both owns and controls that state, enemy units there move 10% slower and
  forts there work 10% better. It uses the same kind of state modifier as the
  base game's `RAJ_fortified_position` (−30% enemy speed),
  `DEN_home_guard_state_modifier` (−10%) and `FIN_motti_tactics_modifier`
  (−15%). Requiring both owner and controller guarantees "enemy" can only mean
  Germany's enemies.
- **Where it all is, from the game's own map** (`tools/check_berlin_map.py`
  re-derives it):
  - Berlin (6521) is ringed by exactly five provinces: 375, Potsdam (3499),
    9428, 11444 and 11505, all in Brandenburg.
  - Seelow (9496) borders Küstrin and three more provinces outside
    Brandenburg.
  - The states bordering Brandenburg are exactly the six above.

**How it respects the author's work:**
- **Forts are only topped up**, never added on top. Each province checks its
  current fort level once and adds exactly the difference. So nothing stacks
  on the forts from the author's Festung Cities focus (Berlin 5) or his
  Oder–Neisse Defence decision (Seelow 4).
- **Nothing goes above level 5.** The game's defines make AI armies in
  "careful" mode refuse to attack provinces with fort level 5 or more.
- **No doubled Berlin bonus.** The chain adds its own copy of the author's
  Festung bonus only if his focus hasn't. If the focus adds his later, the
  chain's copy is removed.
- **Province bonuses end with the ground.** The Seelow and Berlin bonuses are
  removed when the province is lost, as the author does for Königsberg.
- **Separate units.** The emergency divisions don't overlap with the Berlin
  Volkssturm decision (section 6) or the author's "Emergency Reserves"
  decision (Ersatz divisions).
- **The author's own Berlin plans:** his Festung Cities focus contains
  commented-out forts "around Berlin" and at "Küstrin" (IDs 13377–13380).
  Those IDs are in Asia in the current map, so they were never active. The
  chain uses the correct provinces.

**Realism review:**
- **Forts are built over weeks, not instantly.** Reymann, who took over the
  Berlin Defence Area in March 1945, "had inherited almost nothing". If the
  enemy comes fast, the defences are unfinished.
- **Clausewitz timing.** It fires on Seelow falling or the enemy next to
  Berlin (historically 19–20 April). It doesn't fire when the enemy merely
  enters Brandenburg: Soviet bridgeheads were there from February.
- **What matches history:** the three emergency groups (police and Hitler
  Youth are in the sources); the flak towers; Berlin's AA already at the
  maximum since 1939; the ring closing (25 April); Wenck's failed relief.
- **Weidling's trait is a deliberate game bonus** (Oscar's choice).
  Historically his appointment did not strengthen the defence.

**Checked:**
- **Check B** in verify_update.py:
  - simulates every fort top-up for start levels 0–10: it always ends
    exactly at the target or the old level, whichever is higher, and never
    above 5;
  - confirms all provinces are in Brandenburg and the triggers use the right
    states and provinces;
  - confirms the owner-and-controller condition, the 3 units, the
    human-only rule and the Weidling guard;
  - confirms 9 events, all called, and 25 texts.
- **`tools/check_berlin_map.py`:** ring, Seelow front and bordering states
  match the map.
- **Runtime test** (a temporary test line in Germany's history file, removed
  afterwards). The real fort steps ran inside the game, with step 3 twice.
  The game then reported Berlin at exactly 5, Potsdam at exactly 2 and
  Seelow at exactly 4. The emergency units, both bonuses and the Weidling
  step raised no errors.
- **Load test:** error.log identical (115 = 115,
  `game-logs/10-after-festung-berlin_error.log`). setup.log lists both new
  province bonuses by name.

**Not play-tested yet.** Quick test as Germany with the console (key under
Esc), province numbers from the table above:
1. `setcontroller SOV 3473` (Küstrin): events 1 and 2 on the next days.
2. `setcontroller SOV 9496` (Seelow): Clausewitz, then Weidling 3 days later.
3. `setcontroller SOV 375`, `3499`, `9428`, `11444`, `11505`: encirclement.

The fort steps follow 21 and 42 days after events 1 and 2.

**Files:**
- `common/scripted_effects/GER_festung_berlin_effects.txt` (forts, units)
- `common/modifiers/GER_festung_berlin_modifiers.txt` (Seelow and Berlin
  bonuses)
- `common/dynamic_modifiers/GER_festung_berlin_dynamic_modifiers.txt`
  (Brandenburg bonus)
- `common/on_actions/GER_festung_berlin_on_actions.txt` (triggers,
  clean-up)
- `events/GER_festung_berlin_events.txt`
- `localisation/english/GER_festung_berlin_l_english.yml`

Sources:
- de.wikipedia, *Schlacht um Berlin*: the 9 March order "bis zum letzten
  Mann und zur letzten Patrone"; Clausewitz on 20 April; outer and inner
  rings and the Zitadelle; encirclement on 25 April; surrender on 2 May.
- en.wikipedia, *Battle in Berlin*: Clausewitz; about 45,000 soldiers plus
  police, Hitler Youth and 40,000 Volkssturm; Weidling, an artillery general,
  commander of the Berlin Defence Area on 23 April (de.wikipedia: 24 April);
  eight sectors A–H, most commanders without combat experience; Wenck's
  relief halted south-west of Potsdam.
- en.wikipedia, *Battle of the Seelow Heights*: 16–19 April; a light screen
  on the river, three lines behind the heights, the floodplain flooded from a
  reservoir.
- en.wikipedia, *Hellmuth Reymann* ("inherited almost nothing").
- en.wikipedia, *Flak tower*: the three Berlin towers, used as strongpoints.

### 10. SS divisions "Wiking" and "Nordland" in the 1944 start (commit `00807c5`)

Oscar's request: both existed on the start date, so add them "with equipment
realistic for these elite units and with max experience".

**History:**
- **Wiking** was formally reorganised as a panzer division in October 1943,
  and moved to the Cherkassy area in December 1943. The Korsun–Cherkassy
  pocket battle began on 24 January 1944 [1][2].
- **Nordland** was formed in 1943: SS panzergrenadier regiments "Norge" and
  "Danmark", SS Panzer Battalion 11 "Hermann von Salza" and Artillery
  Regiment 11, about 15,000 men [3]. It fought partisans in Croatia in autumn
  1943 and moved north to the Leningrad front in the winter of 1943/44 [3][4].

**Before:** neither was in the 1944 order of battle.
- Wiking could only appear later, through the base game's SS recruitment
  decisions (Denmark and Norway, "historical" option).
- Nordland existed only as a name in the SS name list.

**Now**, in both of the author's order-of-battle files (with and without the
No Step Back DLC):

| Division | Template | Position | Experience | Equipment |
|---|---|---|---|---|
| 5. SS-Division 'Wiking' | the author's "SS Panzer-Division" | 11424, the author's Cherkassy position (German-held on 1 Jan 1944), next to his Leibstandarte | 1.0 (maximum) | 90% (manpower 95%) |
| 11. SS-Division 'Nordland' | new "SS-Panzergrenadier-Division" | 11080, the author's Leningrad-front SS position (the Luga state, German-held) | 1.0 (maximum) | 95% (manpower 100%) |

**The Nordland template:** the author's own Panzergrenadier template (4
motorised and 5 mechanised battalions, artillery, a StuG brigade; he uses it
for 12 divisions), with the SS name list and SS priority. Nothing else is
different.

**Equipment**, using the lines the author gives his own SS divisions:
- **Wiking:** infantry, artillery and AA level 3, StuG III, Wespe, Panzer IV
  Ausf. H, mechanised level 2.
- **Nordland:** infantry level 3, artillery level 2, StuG III (for its panzer
  battalion), mechanised level 2.
- **Tank designs** (StuG III, Wespe, Panzer IV) appear only in the No Step
  Back file, as the author does.
- **Fill level:** Wiking's 90% sits between the author's Totenkopf (81%) and
  Leibstandarte (98%), for a veteran division in the line. Nordland's 95%
  fits a fresh division at full strength.
- **Maximum experience is Oscar's choice.** Historically Nordland was a new
  division with a veteran cadre.

**Other changes:**
- **Name list:** the SS list had no number 5; "5. SS-Division 'Wiking'" was
  added (11 = Nordland was already there). Side effect: the author's four
  unnamed SS regiments are named by the game from this list. If one of them
  used to be called "5. SS-Division", it now gets another number.
- **No second Wiking:** the base game's SS recruitment in Denmark and Norway
  (`events/ss_recruitment_event.txt`) would otherwise create another Wiking
  in a 1944 game. It now creates Wiking only if the game started before 1944
  (`has_start_date`, which the base game uses over 300 times). In a 1944
  game, the second recruitment gives +5,000 manpower instead, the author's
  own amount for the first one.
- **All four files only gain lines.** Nothing of the author's was changed or
  removed.

**Checked:**
- **Check W** in verify_update.py: both divisions in both files with the
  right template, position, experience and equipment; both positions
  German-held on the start date according to the mod's own state files;
  no SS number used twice; the new template identical to the author's
  Panzergrenadier template; the name list; the event guard. A "0 removed
  lines" check for each of the four files.
- **The order of battle loads in the game.** The normal load test does *not*
  read the 1944 order of battle: a deliberately broken template name gave no
  error there. So a temporary test line loaded it with the game's own
  `load_oob` during history setup:
  - With a deliberately broken Wiking template, the game reported
    "Invalid division at line 632 in history/units/GER_1944_nsb.txt", so
    the test catches such errors.
  - With the real files, both versions loaded with no error about any German
    division. The only new lines were 12 "Country SOV/GRE does not have any
    equipment variant" messages. They appear identically in every run: the
    author's order of battle includes units with captured Soviet and Greek
    weapons, and at that early moment the Soviet and Greek histories haven't
    run yet. That's an artifact of the test timing, not a real start.
  - The temporary line was removed afterwards.
- **Load test** of the committed version: error.log identical (115 = 115,
  `game-logs/11-after-wiking-nordland_error.log`).
- **Not yet seen in a started game.** Start as Germany and look near
  Cherkassy (Ukraine) and south-west of Leningrad.

Sources:
- [1] de.wikipedia, *5. SS-Panzer-Division "Wiking"*: panzer division
  October 1943; Cherkassy area December 1943; pocket from 24 January 1944;
  1943 organisation.
- [2] en.wikipedia, *5th SS Panzer Division Wiking*: trapped in the
  Korsun–Cherkassy pocket along the Dnieper, January 1944.
- [3] de.wikipedia, *11. SS-Freiwilligen-Panzergrenadier-Division
  "Nordland"*: formed 1943; Croatia in autumn 1943; north in winter
  1943/44; organisation; 15,000 men.
- [4] en.wikipedia, *11th SS Volunteer Panzergrenadier Division Nordland*:
  on the Eastern Front from autumn 1943; action near Leningrad; Berlin 1945.

### 11. Four 1945 operations: Sonnenwende, Spring Awakening, Courland, Sailors to the Front (commits `97fad47`, `9c950e1`)

Asked for by Oscar:
- **Operation Sonnenwende** and **Operation Spring Awakening**, offered by a
  popup when the front makes them relevant. Fuel and equipment are set aside
  while the attack is prepared and handed back the moment it starts ("not a
  huge amount").
- **Courland:** an automatic evacuation, because moving the trapped
  divisions by hand is tedious. The texts must explain what is required.
- **Sailors to the Front:** poorly equipped naval infantry with no
  experience that does not count towards the special forces limit, a few
  transport ships lost, and about 1,000 manpower.
- **50 political power each** (Oscar's decision).

Eight **new** files; nothing of the author's was changed.

**How the two operations work** (Oscar's design):
1. A popup appears once, when the front makes the operation relevant.
   Accepting only makes a decision available; declining costs nothing.
2. Taking the decision costs 50 PP and takes the supplies out of the
   stockpile for the preparation time.
3. When the preparation ends, everything set aside comes back at once and
   the bonus starts. If the key place falls first, the operation is called
   off: everything comes back, and there is no bonus.

This models something real: before Sonnenwende "only three days' ammunition
and fuel were immediately available" [1]. Supplies committed to an attack
can't be used elsewhere until it starts.

| | Operation Sonnenwende | Operation Spring Awakening |
|---|---|---|
| Popup when | from 1945, at war; the enemy holds part of Ostmark (state 68) while Germany holds Stettin | from 1945, at war with the Soviet Union; the enemy holds part of Northern Hungary (43, Budapest) while Germany or an ally holds North Transdanubia (155) and South Transdanubia (974, the Hungarian oil) |
| Decision needs | Stettin (6282) held; the enemy in Ostmark; the supplies in stock | both Transdanubia states held by Germany or an ally; the supplies in stock |
| Set aside (50 PP) | 5,000 fuel, 500 infantry equipment, 50 artillery | 7,500 fuel, 750 infantry equipment, 75 artillery |
| Preparation | 7 days | 10 days |
| Called off if | Stettin falls | South Transdanubia falls |
| Bonus | 12 days: +15% attack for German troops fighting on German soil in Hinterpommern, Ostmark and Brandenburg | 14 days: +10% attack against the Soviet Union, for Germany and for Hungary if it is still an ally |
| Events | "Begins" at the launch; "Halted" 12 days later | "Begins" at the launch; "Ends" 14 days later, with a text for oil held and one for oil lost |
| History | 15–18 February 1945, from Stargard in Pomerania; Nordland relieved the garrison of Arnswalde; the attack stalled, but the Soviets cleared Pomerania before attacking Berlin [1] | 6–15 March 1945, the last major German offensive; the 6th Panzer Army from the Ardennes; three prongs; the spring thaw and over 700 anti-tank mines per km of front; aims: the Nagykanizsa oil fields and the Danube [2] |

**Design notes:**
- **Exactly what was set aside comes back.** The decision can only be taken
  when the stockpile holds at least the amounts, so the full amount is
  removed. The return adds the same numbers. Which versions of a rifle or
  gun are taken and given back is up to the game. If the fuel tank is full
  when the fuel comes back, the excess is lost, as with any fuel gain.
- **The Sonnenwende bonus only helps Germans.** It is a state bonus with
  `army_core_attack_factor`, which only counts for troops fighting on their
  own country's core territory. Soviet troops in the same states never get
  it. It also switches off if a state stops being German. This is the same
  kind of state bonus as the base game's `DEN_home_guard_state_modifier`.
- **The Spring Awakening bonus** is a national spirit for 14 days with the
  base game's own "attack bonus against" a country. For example,
  `ideas/afghanistan.txt` line 514 gives +15% against the Soviet Union the
  same way.
- **The AI** accepts each popup 80% of the time.

**Courland:**
- **Popup when** Germany holds Libau (Liepāja, 9262) or Windau (Ventspils,
  3296) and has divisions in Kurzeme (190), while the enemy holds both of
  Kurzeme's land neighbours, Žemaitija (189) and Zemgale (809). That means the
  pocket is cut off by land. Historically the Red Army reached the coast
  near Memel on 9 October 1944 [3].
- **The choice:**
  - "Bring them home by sea" (Guderian's view).
  - "Courland will be held" (Hitler's view). Libau and Windau become
    fortresses while held, with the author's own Festung values
    (`GER_festung_static_modifier`: +20% defence, +75% maximum dig-in,
    −25% supply use). A port loses the bonus when it falls.
  - Either way, the evacuation decision stays available.
- **The decision** (50 PP, 30 days):
  - It moves every German division in Kurzeme to the first Baltic port
    state Germany still holds: Gotenhafen/Gdynia (807), Danzig (85),
    Hinterpommern with Stettin (63), Vorpommern (62), Holstein with Kiel
    (58). If Germany holds none of them, the divisions go to the capital.
  - Libau or Windau must be held the whole time; if both fall, the
    evacuation fails.
  - It uses the base game's `teleport_armies`, the same effect as its
    `ICE.txt` decisions. The game's own documentation says that without a
    destination, units go to their capital.
  - Only armies owned by Germany move (`original_tag = GER`), so allied
    units are not moved.
- **The AI** holds Courland 75% of the time, as Hitler did. If it chose to
  evacuate, it takes the decision much more readily.
- **History:** part of the army group was evacuated by sea from the middle
  of January 1945 (among others the 4th Panzer Division, the 31st, 32nd and
  93rd Infantry Divisions and Nordland). The rest surrendered: about 135,000
  men on 9 May 1945 [3]. The decision lets the player do what Guderian
  wanted: bring them all home.

**Sailors to the Front** (a decision from 1 February 1945, while at war,
50 PP):
- **+1,000 manpower** (specialists moved to the replacement pool) and
  **10 convoys** laid up. Oscar asked for "a small amount".
- **Three naval infantry divisions**, on the historical schedule:

| Division | In the game | History |
|---|---|---|
| 1. Marine-Infanterie-Division | at once, at Stettin | formed at the start of February 1945 at Angermünde from the Marine-Schützen-Brigade Nord; fought on the Oder and, in March, at the Stettin bridgehead (Greifenhagen–Altdamm) [4] |
| 2. Marine-Infanterie-Division | 30 days later, at Kiel (Holstein) | formed in March 1945 at Glückstadt and Itzehoe, both in Holstein, mostly from naval personnel; fought the British on the Weser–Aller line in April [5] |
| 3. Marine-Infanterie-Division | 60 days later, in Vorpommern | formed on 1 April 1945 from the survivors of the 163rd Infantry Division who escaped from Stargard; fought in Pomerania, around Swinemünde [6] |

- **If Germany no longer holds the state,** the division forms at the
  capital instead.
- **The template** is "Marine-Infanterie-Division": 6 ordinary infantry
  battalions and engineers, locked, lowest priority. It is **not** the
  marine battalion type, so it doesn't count towards the special forces
  limit (Oscar's condition).
- **Equipment:** 50% of it, with the 1939 rifle (Infantry Equipment I), and
  no experience.

**Checked:**
- **Check O** in verify_update.py parses the files; it doesn't just search
  the text. It confirms:
  - for each operation separately: set aside = returned = required;
    returned both at the launch and when called off; a called-off operation
    never launches;
  - 12 and 14 days of bonus, 7, 10 and 30 days of waiting, 50 PP each;
  - the evacuation only moves German armies, and lists the five port
    states in order;
  - Stettin, Kiel, Libau and Windau are in the states the scripts use,
    according to the mod's own state files;
  - 6 unit creations, all owned by Germany, 50% equipment, 0 experience;
    the template has only infantry battalions and no marines;
  - +1,000 manpower and −10 convoys;
  - 10 events, each one both defined and called; 60 texts with BOM, and
    every text used exists.
- **Check O was calibrated.** Three errors were planted one at a time, and
  each made it fail:
  - the return gives 6,000 fuel instead of 5,000;
  - a called-off operation still launches;
  - one battalion is a marine battalion.
- **What a called-off decision does.** The game's documentation doesn't say
  whether a cancelled decision also runs its `remove_effect`. If it did, the
  supplies would come back twice and the operation would launch anyway.
  Paradox's own decisions rely on it not doing so: 309 have both effects.
  For example, `AFG_claim_state` gives its reward in `remove_effect` and
  only clears a flag in `cancel_effect`. The operations follow the same
  pattern.
- **Documented game features only:** `teleport_armies` (including the
  capital fallback), `divisions_in_state`, `is_fully_controlled_by`,
  `has_fuel` and `has_template` are all described in the game's own
  `documentation/` folder. `divisions_in_state` counts only the country's
  own divisions, so Soviet units in Courland don't count.
- **Runtime test.** Temporary test lines in Germany's history file (removed
  afterwards) ran these inside the game during its 1944 setup: set-aside and
  return, both launches, the fortress on and off, all three divisions. There
  were no errors.
  - The stockpile itself could not be observed. At that early moment the
    game reads fuel and every equipment stockpile as 0, even right after
    2,000 rifles were added directly.
  - So this test proves the effects run without errors, not the amounts
    (the same limit as the division count in section 6). The amounts rest
    on check O.
- **Load test:** error.log identical (115 = 115,
  `game-logs/12-after-1945-operations_error.log`), and no line mentions the
  new files. setup.log lists the new "Fortress Courland" bonus by name.
- **Event texts checked against the sources.** The first version had four
  claims the sources don't support. They were corrected in `9c950e1`,
  before packaging:
  - Nordland at Arnswalde "on the first day";
  - the Hungarian fields as the Axis's "last oil fields" (the Vienna oil
    region still existed);
  - Hitler holding Courland "to tie down Soviet armies" (the source gives
    the U-boat bases and a bridgehead for a new offensive);
  - where the 2nd and 3rd naval infantry divisions were formed.

**Not play-tested yet.** Quick tests as Germany, with the console (the key
under Esc):
1. **Sonnenwende:**
   - `event ger_1945.1`, then choose "Prepare the counterattack".
   - `setcontroller SOV 3473` puts Küstrin, in Ostmark, in Soviet hands.
   - Take the decision in War Measures. The fuel and equipment go down now,
     and come back with the "Sonnenwende Begins" event 7 days later.
2. **Spring Awakening:** `event ger_1945.4`, then take the decision. The
   offensive begins 10 days later.
3. **Courland:**
   - `event ger_1945.8`.
   - Move a division into Kurzeme (Latvia), then take the decision. After
     30 days, the division should be at Gdynia.
4. **Sailors to the Front:** the decision appears from 1 February 1945.
   - `event ger_1945.11` creates the 2nd division at Kiel directly.
   - `event ger_1945.12` creates the 3rd in Vorpommern.

The popups themselves only come when the front conditions above are met in
1945.

**Files:**
- `common/decisions/GER_1945_operations_decisions.txt` (4 decisions, in
  War Measures)
- `common/scripted_effects/GER_1945_operations_effects.txt` (set aside and
  return, launches, evacuation, fortress, divisions)
- `common/dynamic_modifiers/GER_1945_operations_dynamic_modifiers.txt`
  (Sonnenwende state bonus)
- `common/ideas/GER_1945_operations_ideas.txt` (Spring Awakening spirit)
- `common/modifiers/GER_1945_operations_modifiers.txt` (Fortress Courland)
- `common/on_actions/GER_1945_operations_on_actions.txt` (popups, fortress
  clean-up)
- `events/GER_1945_operations_events.txt` (10 events)
- `localisation/english/GER_1945_operations_l_english.yml` (60 texts)

Sources:
- [1] en.wikipedia, *Operation Solstice*: 15–18 February 1945, launched from
  Stargard; the Eleventh SS Panzer Army being assembled in Pomerania;
  Nordland attacked towards Arnswalde and relieved its garrison; "only three
  days' ammunition and fuel were immediately available"; the Soviets
  postponed the attack on Berlin to clear Pomerania.
- [2] en.wikipedia, *Operation Spring Awakening*: 6–15 March 1945, "the last
  major German offensive"; the 6th Panzer Army withdrawn from the Ardennes;
  three prongs (Balaton–Velence–Danube, south of Lake Balaton, south of the
  Drava); the Nagykanizsa oil fields; the spring thaw; over 700 anti-tank
  mines per km of front; the Vienna offensive from 16 March.
- [3] en.wikipedia, *Courland Pocket*: the coast reached near Memel on
  9 October 1944; Libau; evacuation at Windau (photo, 19 October 1944);
  Guderian urged an evacuation and Hitler refused (U-boat bases, a
  bridgehead for a new offensive); divisions evacuated by sea from the
  middle of January 1945; about 135,000 surrendered on 9 May.
- [4] de.wikipedia, *1. Marine-Infanterie-Division (Wehrmacht)*;
  en.wikipedia, *1st Marine Division (Wehrmacht)*: "excess naval personnel
  who no longer had ships or submarines to man".
- [5] de.wikipedia, *2. Marine-Infanterie-Division (Wehrmacht)*;
  en.wikipedia, *2nd Marine Division (Wehrmacht)*.
- [6] de.wikipedia, *3. Marine-Infanterie-Division (Wehrmacht)*;
  en.wikipedia, *3rd Marine Division (Wehrmacht)*.

### 12. Germany's last reserves: six events and a decision (commit `70d287a`)

Asked for by Oscar: events adding manpower for these groups:
- the foreign volunteers of 1944;
- the Baltic "selective conscription" (he suggested exactly 38,000);
- the 1945 semi-volunteers, as a choice with a very small factory
  penalty;
- round-ups once manpower runs low or Berlin is threatened;
- a Luftwaffe transfer (about 75,000 men, a slight temporary air
  penalty).

He also asked for a flavour event for the last Swedish deliveries, with
his exact rewards.

The plan was agreed first. Oscar's decisions:
- Hungary's men are taken from Hungary and given to Germany.
- The Luftwaffe transfer is a decision followed by a story event.
- The fuel stays at 250.
- The neutral volunteers are folded into the Western event.

Six **new** files; nothing of the author's was changed.

**What happens.** Each event fires once, from a daily check for Germany,
and only inside its historical window:

| # | Event | When | Effect | History |
|---|---|---|---|---|
| 1 | The Estonian Mobilisation | 7 Feb to 31 Dec 1944, at war with the Soviet Union, while Germany holds Tallinn | +38,000 manpower | Jüri Uluots' radio appeal (7 Feb 1944) to men born 1904–1923: 38,000 reported, forming seven border guard regiments and the 20th Estonian division [1][2] |
| 2 | Collaborators Flee East | from 6 June 1944, once an enemy holds Paris | +3,000 | about 2,500 members of the French Milice went into the SS unit "Charlemagne" [3]; Dutch collaborators fled to Germany in September 1944 [4]; Spaniards stayed on after the Blue Legion was recalled [5]; Oscar's 500 neutral volunteers are included |
| 3 | Hungarian SS Divisions | 30 days after the author's Arrow Cross coup (his event `hungary.operation.panzerfaust.1`, or his Hungarian decision), with Hungary still allied or subject | up to 7,500 moved from Hungary to Germany | "Hunyadi", formed in November 1944 from the Hungarian 13th Division and a ski battalion; trained at Neuhammer; short of weapons [6] |
| 4 | Luftwaffe Men to the Front | a decision (War Measures, 50 PP) from 1 September 1944, then a story event | +75,000; −10% air mission efficiency for 90 days | the Luftwaffe field divisions went to the army at the end of 1943 [7]; the 1st Parachute Army was formed in September 1944, 30,000 men [8]. 75,000 is Oscar's figure; no source found gives a total |
| 5 | The Last Swedish Deliveries | 28 Sep to 31 Dec 1944, if Sweden is neither at war with Germany nor its ally, and Germany holds Stettin or Kiel | 3 trains, 137 trucks, 1,800 support equipment, 250 fuel; for 35 days every aircraft type 13% cheaper | the transit of German soldiers on leave ended in 1943, and Sweden kept selling steel and machine parts [9]; Sweden's decision to close its Baltic ports to German shipping was reported on 28 September 1944 [10]. The amounts are Oscar's |
| 6 | Eastern Workers and Prisoners Volunteer | from 1 Feb 1945, at war with the Soviet Union | a choice: +15,000 and −1% factory output for 180 days, or nothing (AI: 75% / 25%) | Vlasov's committee (KONR) from November 1944; Soviet prisoners volunteered to escape camps where they were starving; the 2nd division nearly doubled with eastern workers [11] |
| 7 | Round-ups Behind the Front | from 1945, once manpower falls below 200,000 or an enemy takes one of the five provinces around Berlin (the same five as Festung Berlin) | +15,000 | the Feldjägerkorps (from January 1944) hunted stragglers and deserters with flying courts-martial, which executed an estimated 7,000–8,000 in the last four months of the war [12]; the Volkssturm took in foreigners in some cases [13] |

**Design notes:**
- **Date windows.** Every event is tied to its historical period, so none
  can fire at an absurd time. For example, the Western event can only come
  after June 1944.
- **Hungary.** Germany gains exactly what Hungary loses:
  - 7,500 if Hungary has at least that much;
  - otherwise 5,000 or 2,500;
  - nothing if Hungary has less than 2,500.

  The author's coup event requires an AI-run Hungary, so no human player
  loses men to this.
- **The aircraft bonus.** The game has no "aircraft production output"
  modifier. Instead, the spirit makes every aircraft type 13% cheaper to
  build for 35 days, so the same factories make about 15% more
  (1 / 0.87 = 1.149).
  - `instant = yes` makes it apply to production lines already running,
    as in the base game's Austrian air production spirit
    (`common/ideas/austria.txt`).
  - The CAS, naval bomber, heavy fighter and jet types are separate
    "duplicate archetypes" in 1.19 (`x_plane_airframes.txt`). So all 20
    aircraft types are listed one by one, as Paradox does in 24 of its own
    bonus blocks. Check R compares the list with the game's equipment
    files.
- **Pictures.** All are base-game pictures, chosen by looking at them. Two
  names that looked right were unusable: `GER_goring` is an empty
  silhouette, and `desertion_poster` is an American "A.W.O.L." poster.
- **Already in the game:**
  - The base game's SS recruitment decisions (25 PP,
    `common/decisions/SS.txt`) still create the historical Baltic and
    Western SS divisions or give 1,000–2,000 manpower. These events are
    separate from them.
  - The mod's "Recruit Andrey Vlasov" decision creates Vlasov's units;
    event 6 only adds the manpower.
  - "Sailors to the Front" (section 11) covers the navy.

**What was not taken from the pasted history.** The plan said so in
advance, and the texts only say what the sources support:
- **"Aktion Göring" and "Marine-Hilfe":** no source uses these names.
- **The Swedish "stranded property"** (locomotives at Storlien, bonded
  warehouses, Köping machinery, a negotiated release): not found in any
  source. The event uses the documented facts and Oscar's rewards.
- **"Hunyadi"** was built mainly from a Hungarian army division, not from
  volunteers [6].
- **Press-gangs by "SS-Jagdkommandos"**, and "any foreign worker handed a
  rifle, refusal meant execution": not supported by the sources. The event
  describes the documented Feldjäger round-ups instead.
- **Belgian collaborators fleeing:** not found in the source checked, so
  the text names only the French and the Dutch.

**Checked:**
- **Check R** in verify_update.py parses the files and confirms:
  - every amount;
  - Hungary's transfer: Germany gains exactly what Hungary loses, never
    more than Hungary has;
  - the three spirits and their durations;
  - all 20 aircraft types, each −13% with `instant = yes`, compared with
    the game's own equipment files;
  - the decision: 50 PP, once, from September 1944, then the story event;
  - the exact conditions of each of the six daily checks, and that each
    fires once;
  - Tallinn, Paris, Stettin, Kiel and the five Berlin provinces are in the
    states the scripts assume;
  - the author's Arrow Cross flag exists;
  - 7 events, all called; 32 texts, all used.
- **Check R was calibrated.** Four errors were planted one at a time, and
  each made it fail:
  - Estonia gives 39,000;
  - Germany gains 8,000 while Hungary loses 7,500;
  - the Me 262 type is left out of the aircraft bonus;
  - the Western event is allowed from 1940.
- **Game features.** Each one is described in the game's own
  `documentation/` folder or used by the base game:
  - `any_enemy_country`, `has_global_flag` with `days`, `has_manpower`,
    `add_manpower`, `add_timed_idea`;
  - `equipment_bonus` with `build_cost_ic` in a spirit (44 base-game idea
    files);
  - the trains, trucks and support equipment: Germany starts with the
    techs for them (`basic_train`, `motorised_infantry`, `tech_support`).
- **Runtime test.** Temporary test lines in Germany's history file (removed
  afterwards) ran all seven effects inside the game, with no errors.
  - The game then reported all three spirits as present (`has_idea`),
    including the aircraft one.
  - As in section 11, stockpile and manpower amounts can't be read at that
    early moment; the amounts rest on check R.
- **Load test:** error.log identical (115 = 115,
  `game-logs/13-after-last-reserves_error.log`). setup.log shows that the
  game loaded 1 decision, 7 events and 3 spirits from the new files.
- **Project checkers:**
  - province references: 544 checked, the same 22 base-game hits,
    0 unknown modifiers;
  - structure: no problem in the new files;
  - references: the same 4 old issues, nothing new.

**Not play-tested yet.** Quick tests as Germany, with the console (the key
under Esc):
1. `event ger_reserves.1` through `event ger_reserves.7` each show their
   text and apply their effect. Event 4 is only the story part of the
   decision: its effects come from the decision itself.
2. The decision "Luftwaffe Men to the Front" appears in War Measures from
   1 September 1944.
3. The automatic triggers need the dates and conditions in the table.

**Files:**
- `common/scripted_effects/GER_reserves_effects.txt` (all effects, shared
  by the events, the decision and the runtime test)
- `common/ideas/GER_reserves_ideas.txt` (the three timed spirits)
- `common/decisions/GER_reserves_decisions.txt` (Luftwaffe decision, in
  War Measures)
- `common/on_actions/GER_reserves_on_actions.txt` (the six daily checks)
- `events/GER_reserves_events.txt` (7 events)
- `localisation/english/GER_reserves_l_english.yml` (32 texts)

Sources:
- [1] en.wikipedia, *Battle of Narva (1944)*: Uluots' radio speech of
  7 February 1944; 38,000 men; seven border guard regiments and the 20th
  Estonian division.
- [2] en.wikipedia, *Jüri Uluots*: prime minister 12 October 1939 to
  20 June 1940; a radio address urging men born 1904–1923 to report;
  38,000 draftees. This article places the address in January 1944.
- [3] en.wikipedia, *33rd Waffen Grenadier Division of the SS
  Charlemagne*: formed in September 1944, including French collaborators
  fleeing the Allied advance; 2,500 from the Milice.
- [4] en.wikipedia, *Dolle Dinsdag*: "many Germans and Dutch collaborators
  fled to Germany, fearing reprisals".
- [5] en.wikipedia, *Blue Legion*: Spaniards who refused to return; the
  101st SS Spanish Volunteer Company (140 men).
- [6] en.wikipedia, *25th Waffen Grenadier Division of the SS Hunyadi (1st
  Hungarian)*: November 1944; the 13th Honvéd Division and a ski
  battalion; Neuhammer; 20,000 men; few weapons.
- [7] en.wikipedia, *Luftwaffe Field Divisions*: handed over to the army
  late in 1943.
- [8] en.wikipedia, *1st Parachute Army*: formed in September 1944,
  30,000 men.
- [9] en.wikipedia, *Sweden during World War II*: the permittenttrafik
  until 1943; steel and machine parts sold at inflated rates.
- [10] FRUS 1944 vol. IV, telegram of 28 September 1944
  (history.state.gov): "the decision of the Swedish Government to close
  the Baltic ports to German shipping"; Malmö and Göteborg still open.
- [11] en.wikipedia, *Russian Liberation Army*: KONR from 14 November 1944;
  prisoners volunteering to escape starvation; the 2nd division nearly
  doubled with eastern workers; 50,000–60,000 men by February 1945.
- [12] en.wikipedia, *Feldjägerkorps*: created in January 1944; hunted
  deserters and stragglers; flying courts-martial; an estimated
  7,000–8,000 executed in the last four months.
- [13] en.wikipedia, *Volkssturm*: foreigners inducted in some cases, if
  deemed ideologically acceptable.

### 13. Files kept byte-exact in every clone; the project on GitHub (commit `2a99f40`)

Oscar asked to publish the project to the author's GitHub repository
(github.com/gastav3/Hoi4_1944), replacing its old content, with detailed
documentation.

**What was on GitHub:** the author's own history up to 29 June 2026 (branch
`main`, plus an older branch `states_update`). It was compared file by file,
ignoring line endings, with the Steam version this project starts from
(`253cea1`, July 2026):
- the Steam version already contains everything from GitHub `main`,
  including the author's last two commits of 29 June 2026 ("STATES",
  "STATE FIXES");
- the 28 state files that exist only in the Steam version are new states the
  author created after June;
- only two things on GitHub are not in the Steam version: a stray
  `common/characters/BLR.rar`, and two placeholder lines ("ADD THE REST
  1944", "ADD LATER 1944") in states 523 and 669, which the author removed
  himself before his July upload.

So replacing GitHub's content with this project loses none of the author's
work.

**How it was published:**
- **No force-push.** One merge commit joins GitHub's history with this
  project's, so the author's earlier commits stay. The `states_update` branch
  is untouched.
- **The layout is this project's:** `mod/` (the mod), `docs/` and `tools/`,
  with a README as the front page. On GitHub the mod files used to be at the
  top level, so a game setup or Steam upload that pointed at the repository
  root must now point at `mod/`. That also keeps `.git` out of the Steam
  upload.

**The line-ending fix (`mod/.gitattributes`):**
- The author's `mod/.gitattributes` was the GitHub Desktop template
  (`* text=auto`, "perform LF normalization").
- A test clone showed the problem. On Windows, with Git's default
  `core.autocrlf=true`, it converts the line endings of the mod's 45 LF-only
  files on checkout (38 state files, `cosmetic.txt`, `descriptor.mod` and
  others). They then differ from the tested and checksummed files, and
  `sha256sum -c` fails in a clone.
- Because the file sits inside `mod/`, it overrides the repository's own
  `* -text`.
- Now `mod/.gitattributes` says `* -text`, so git never converts and every
  clone is byte-exact. The game doesn't read this file.

**Checked:**
- **A new integrity check** in verify_update.py clones the repository into a
  temporary folder and compares all 943 mod files with the committed bytes.
- **Calibrated:** with the old `* text=auto` put back on a temporary branch,
  the check failed.
- **The removed lines** of `.gitattributes` are allowed only as exactly the
  two template lines.

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

66 files differ from the version on Steam: 31 edited, 3 deleted, 32 new (full list:
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
