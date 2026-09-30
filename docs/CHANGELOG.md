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
| 11. SS-Division 'Nordland' | new "SS-Panzergrenadier-Division" | 11080, the author's Leningrad-front SS position: just south-west of Leningrad, directly behind the German line (the mod's state 208, whose file is named Pskov; German-held) | 1.0 (maximum) | 95% (manpower 100%) |

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
  - **Corrected in section 17:** this was wrong for rifles and guns. The
    game took the amount from every type in stock and gave it back as the
    newest type, so each use lost about 500 / 750 rifles. They are now
    taken and returned type by type, and that was measured in the game.
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

   **Fix, 28 September (commit `96f4a17`):** at first this step didn't work.
   The decision is unlocked by a flag that only the daily check set, so
   firing the popup from the console never showed the decision. The popup
   now sets the flag itself; in normal play nothing changes.
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

### 13. Files kept byte-exact in every clone; the update offered on the author's GitHub (commit `2a99f40`)

Oscar asked to publish the project to the author's GitHub repository
(github.com/gastav3/Hoi4_1944), with detailed documentation.

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

So building on the Steam version loses none of the author's work on GitHub.

**A first attempt, withdrawn (pull request #1).**
- It put this project on GitHub as it is here, joined to the author's history
  by a merge commit, with the mod moved into `mod/`.
- The author pointed out that moving every file breaks the history of his
  files and makes the commits unusable on his side. He was right: the pull
  request showed 980 changed files, where 119 really differ. It was closed.

**Pull request #2, in the author's layout:**
- **It starts from his `main`.** The mod stays at the top level and his
  line-ending setting (`* text=auto`) is kept. No file is moved.
- **First commit: the Steam version of July 2026** (`c56a5f1`). This is his
  own work that never reached GitHub, 62 files:
  - 33 changed files;
  - 28 new state files;
  - the stray `BLR.rar` removed;
  - the two placeholder lines gone.

  Nothing in it was written by Oscar or the AI.
- **Then every change of this package as its own commit** on his files, with
  the same message, author and date. These are 26 commits: all mod commits
  except `2a99f40`, because his repository keeps its own `.gitattributes`.
  A README describing the update comes last.
- **The commit IDs there differ** from the ones in these documents. The
  table below pairs them, and the README there has the same table.

**Checked (pull request #2):**
- **Identical files:** after every commit, the files are identical to this
  package at the same step, ignoring only CR at line ends (his repository
  stores text with LF). The sync commit is identical to the Steam copy.
- **Identical line changes:** each commit shows the same line changes as the
  original, except the Siam history rebuild (`c88694e`). That one counts one
  more changed line, the file's last line, because the old file had no
  newline at its end. The resulting file is identical.
- **Line endings:** text files are stored with LF, like the rest of his
  repository (0 files with CRLF, before and after).
- **In the game:** a fresh clone of the branch, with Git's default settings,
  loads with an identical error.log (115 = 115,
  `game-logs/14-pull-request-2-clone_error.log`).
- **Size:** the pull request shows 119 files, the 118 real differences plus
  the README.

| This package | Pull request #2 | Change |
|---|---|---|
| `e20698c` | `7ffb1d5` | Fix Ichi-Go province modifiers applied in the wrong state |
| `ce4f33a` | `9c0e8b3` | Remove stale duplicate definitions of states 870, 871, 873 |
| `6fa793c` | `c1dbe61` | Update supported game version to 1.19.3.0 |
| `2d80d87` | `0417681` | Netherlands focus tree: rebuild on 1.19.3, keep the RKN edit |
| `f646e4a` | `976e529` | cosmetic.txt: rebuild on 1.19.3, keep the mod's 17 own tags |
| `8041896` | `5fa14c9` | Fix a character and a focus ID renamed in 1.19 (Argentina, Australia) |
| `586de46` | `7d9606e` | Add base-game decisions the mod's older decision files lack |
| `0384e82` | `47bc46e` | Add news event bftb_news.11 missing from the mod's older copy |
| `c8dac21` | `d101815` | Special forces: replace pre-1.19 doctrine techs with 1.19 sub-doctrines |
| `4a17ff6` | `5a0f8ef` | Australia history: rebuild on 1.19.3, keep the author's 1944 content |
| `d5c3c69` | `c88694e` | Siam history: rebuild on 1.19.3, keep the author's 1944 content |
| `58a1a82` | `cdfb445` | Australia: re-apply the AST_domestic_industry fix (it is a 1.19.3 bug) |
| `d55cf37` | `18456dd` | JAP decisions: add the rest of the Tauran border-incident chain |
| `7de1ce8` | `7f5bfe4` | Add flavor event: Slovak National Uprising (29 August 1944) |
| `a5982fe` | `7c1b146` | Slovak uprising: Germany loses the 3,000 manpower, not Slovakia |
| `76a0d54` | `b41e8bc` | Add Nero Decree and Werwolf (Germany, last-stand decisions) |
| `e6c0034` | `059efbb` | Volkssturm: realistic levies, rifle mix and 1945 call-ups |
| `d9d7888` | `3021967` | Volkssturm bug check: raise units where Germany holds a state, not only where it holds all of it |
| `b88321a` | `847b39b` | Fix Konigsberg in Ruins: remove the ring fort, not forts in Africa |
| `e13d45d` | `fc01049` | Fix Oder-Neisse Defence: build the Stettin fort in Stettin's own state |
| `5fb4a0b` | `eddc310` | Fix "Destroy Antwerpen": hit Antwerp's port in Antwerp's own state |
| `1fa3c2c` | `3d6e75b` | Add Festung Berlin: a five-event chain for the defence of Berlin |
| `00807c5` | `10c5712` | Add 5. SS 'Wiking' and 11. SS 'Nordland' to the 1944 start |
| `97fad47` | `ad8ce09` | Add four 1945 operations for Germany |
| `9c950e1` | `79d97af` | 1945 operations: correct event texts against the sources |
| `70d287a` | `f2ba254` | Add Germany's last reserves: six events and a decision |

**Merged, 28 September.** The author merged pull request #2 himself
(merge commit `dd65ca7` on his `main`).
- **His own commit first:** before merging, he pushed his own commit `79fa453`
  "fix" and merged his `main` into the branch.
- **What it contained:** his July work, identical to the Steam version
  except `descriptor.mod` (`1.17.5.2` there).
- **The result is exactly what was tested:** his merged `main` equals the
  pull request's content file by file, ignoring only line endings, with
  `supported_version="1.19.3.0"`.

**Pull request #3** brings the two later changes (section 14 and the
Courland popup fix) the same way, on top of his merged `main`:

| This package | Pull request #3 | Change |
|---|---|---|
| `99c2aa4` | `90c19a8` | Add the home front, 1944–45: eight events for Germany |
| `96f4a17` | `bb7c0aa` | Courland: the popup itself unlocks the evacuation decision |

- **Identical files and changes:** after each commit, the files equal this
  package at the same step (ignoring CR at line ends), and the line changes
  match.
- **README:** `58b8bce` updates the README (the commit table, links to tag
  `final-2026-09-28-v11`).
- **In the game:** a fresh default clone of the branch loads with an
  identical error.log (`game-logs/16-pull-request-3-clone_error.log`).

**Pull request #3, extended (29 September 2026).** It wasn't merged yet, so
the next three changes were added to the same branch rather than opened as a
second pull request. The equipment fix (section 17) changes a file that pull
request #3 itself adds.

| This package | Pull request #3 | Change |
|---|---|---|
| `e578b10` | `08d8589` | Fix the crash when starting the 1944 game as the United Kingdom (section 15) |
| `ddda13e` | `45d728e` | Add five war measures for Germany (section 16) |
| `470916b` | `e126956` | Fix: 1945 operations lost rifles; Vlasov's air force got the wrong planes (section 17) |

- **Identical files and changes:** checked the same way as above, for all
  three.
- **Line endings:** stored with LF, as the repository's `* text=auto`
  setting does for every file (no CRLF files in the branch).
- **README:** `66adcd0` adds the three commits to the table, links to tag
  `final-2026-09-29-v12`, and notes that the UK crash is fixed.
- **In the game:** a fresh default clone of the branch (CRLF checkout) loads
  with an identical error.log
  (`game-logs/19-pull-request-3-extended-clone_error.log`).

**Pull request #3 merged.** The author merged pull request #3 on
29 September 2026 at 10:15 (merge commit `c267d4f`), at `66adcd0`. That
covers sections 14 to 17 and the Courland fix. His `main` now equals
`66adcd0` file by file.

**Published on Steam.** The author then uploaded the update to the Steam
Workshop himself: Steam records the update at 29 September 2026, 10:18
(`timeupdated` in `appworkshop_394360.acf`), three minutes after the merge.
- **What was published:** the Workshop copy now equals his GitHub `main`
  at `c267d4f` file by file, ignoring line endings (955 files). That is
  this package at `470916b` plus his README.md and his `.gitattributes`.
- **Not yet published:** Oscar's review round (section 18) and sections
  19–20.
- **The Workshop check** in verify_update.py now accepts either the July
  baseline or this published version.
- **The rebuild test** now starts from the baseline commit `253cea1`,
  which is identical to the July Workshop copy (914/914 files, checked
  on 27 Sep).

**Pull request #4: Oscar's review round.**
- **Why a new pull request:** the review commit was pushed to the same
  branch about 25 minutes after that merge, so it is not part of it. It is
  now pull request #4, on its own branch `update-2026-09-review`, which
  starts at `66adcd0`.
- **Correction:** tag `final-2026-09-29-v13` still said the commit was in
  pull request #3. It was pushed before the merge was noticed; this
  paragraph replaces that.

| This package | Pull request #4 | Change |
|---|---|---|
| `807249b` | `11aa2b9` | Oscar's review: Vlasov's airmen, railway 90 days, weapons with the Volksopfer, KONR later and poorly armed (section 18) |

- **Identical files and changes:** checked as above; stored with LF.
- **README:** `8ecc7ba` adds the commit, names pull request #4, and links to
  tag `final-2026-09-29-v14`. `3435bbb` is a README for pull request #3
  pushed after the merge. It is left unused on the old branch.
- **In the game:** a fresh default clone of `3435bbb` loads with an
  identical error.log (`game-logs/21-pull-request-3-review-clone_error.log`).
  Its mod files are identical to pull request #4's `8ecc7ba`; only the
  README differs.

**Pull request #4, extended (29 September 2026).** It wasn't merged yet, so
sections 19 and 20 were added to the same branch, as was done for pull
request #3.

| This package | Pull request #4 | Change |
|---|---|---|
| `04f75bb` | `12fa932` | Add five flavour events: the Indian Legion, the Handschar, the Eastern Legions, Wiking, Nordland (section 19) |
| `222caf2` | `d9785e3` | Add the bridge at Remagen: an event with a real photo, and the collapse (section 20) |

- **Identical files and changes:** checked as above; stored with LF. The
  photograph (`report_event_GER_remagen_bridge.dds`) is byte-identical,
  both in the branch and in a fresh clone.
- **README:** `d4e1359` adds the two commits, links to tag
  `final-2026-09-29-v15`, and credits the photograph.
- **In the game:** a fresh default clone of `d4e1359` (CRLF checkout) loads
  with an identical error.log
  (`game-logs/23-pull-request-4-extended-clone_error.log`), and setup.log
  shows the 5 + 2 new events loaded.

**Pull request #4 after the handover (29 September 2026, evening).**
- **Codex's update** pushed eleven more commits (`d4e1359` to `23b6824`): the
  seven of sections 21–25, and sections 26–27.
- **Checked here:**
  - each commit's files equal this package at the same step (ignoring CR),
    with the same line changes;
  - no text file stored with CRLF;
  - the branch only added to its history.
- **Then added:** the revert of the Overlord change and a new README.

| This package | Pull request #4 | Change |
|---|---|---|
| `a2790cb` | `7bd3cff` | Wiking before Warsaw (section 21) |
| `ef9dbce` | `c55a9a6` | The first German atomic bomb (section 22) |
| `a9a793d` | `d77c64b` | Leningrad, first version (section 23) |
| `204d7de` | `658638b` | The Crimea (section 24) |
| `b244eab` | `6ca6af2` | The Crimea fix after Oscar's play-test (sections 24–25) |
| `97a806f` | `c981f77` | Leningrad fires when the city is taken (sections 23, 25) |
| `df4cc07` | `5c7f468` | Oscar's pictures: the whole Wiking photo (section 21) |
| `c0f1767` | `4fd3bb4` | The invasion beaten back (section 26) |
| `1296bb8` | `4fc5eec` | Codex's Overlord change (section 27; reverted) |
| `46c665a` | `bc4018d` | The invasion event: western Allies only (sections 26–27) |
| `5ac05e9` | `010eac5` | The revert of the Overlord change (section 28) |

- **Identical files and changes:** checked as above; stored with LF. The
  author's `common/decisions/Allies_1944.txt` on the branch is again his
  own version (as at `d4e1359`).
- **README:** `30f5990` puts all fourteen commits of pull request #4 into
  its commit table and links to tag `final-2026-09-29-v17`. It replaces the
  README text Codex wrote (`23b6824`), which still said 74 checks.
- **In the game:** a fresh default clone of `30f5990` loads with an identical
  error.log (`game-logs/27-pull-request-4-v17-clone_error.log`).

**Pull request #4 with the SS names fix (30 September 2026).**

| This package | Pull request #4 | Change |
|---|---|---|
| `bb94b9e` | `44cb8d3` | SS division names in the 1944 start (section 29) |

- **Identical files:** checked as above; stored with LF; the branch only
  added to its history.
- **Fresh clone:** a default clone of the branch has the package's 988 mod
  files (ignoring CR), plus the README. The only file that differs is
  `.gitattributes`, which keeps the author's setting.
- **README:** `ae5135e` adds `44cb8d3` to its commit table and links to tag
  `final-2026-09-30-v18`.
- **In the game:** the fresh clone loads with an identical error.log
  (`game-logs/29-pull-request-4-v18-clone_error.log`).

**The line-ending fix (`mod/.gitattributes`, this package only; not part of
pull request #2):**
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

### 14. The home front, 1944–45: eight events (commits `99c2aa4`, `96f4a17`)

Asked for by Oscar: eight events from the last months of the war, with
suggested effects, the rest to be decided "creative and realistic".
- **When they fire:** each event fires once, on its historical date (or
  later while its window stays open), only while Germany is at war.
- **The regime must still stand:** the home-front measures also require it
  (`has_government = fascism`).
- **Files:** five new files; nothing of the author's was changed.

| Date | Event | Condition | Effect | Source |
|---|---|---|---|---|
| 15 Aug 1944 | Women's Labour Service Extended to 50 | until the end of 1944 | +10,000 manpower (men released from industry) | women's labour-service age raised from 45 to 50 [1] |
| 14 Oct 1944 | The Death of Field Marshal Rommel | until the end of 1944 | Rommel leaves German service. Story only if the author's 20 July event already retired him | [1]; Burgdorf and Maisel, the choice, cyanide, the official "heart failure", the state funeral in Ulm on 18 October, Rundstedt's eulogy [2] |
| 17 Nov 1944 | RAD Women at the Flak | | +7,500 manpower; lasting +1.5% State AA damage and hit chance | RAD women as Flak helpers, to release soldiers for the front [1] |
| 19 Dec 1944 | An Air Force for Vlasov | only if Vlasov was recruited (the mod's decision) | a choice: −25 PP for +5,000 manpower, 20 fighters and 10 ground-attack aircraft; or nothing | Göring's order of 19 December 1944; fighter, night-bomber, reconnaissance, liaison and transport squadrons; about 5,000 men and 87 aircraft [3] |
| 6 Jan 1945 | The Volksopfer | | a choice: −25 PP for 4,000 old rifles (the 1918 infantry equipment) and 1,000 support equipment; or nothing | the call for the "Volksopfer" to equip the Volkssturm [4] |
| 30 Jan 1945 | The Sinking of the Wilhelm Gustloff | at war with the Soviet Union, Gotenhafen (Gdynia) still ours | −1,500 manpower | 9,000 refugees dead [4]; the details [5] |
| 12 Feb 1945 | Women and Girls for the Volkssturm | | +5,000 manpower, −2% stability | [4]; girls as young as 14 trained with weapons [6] |
| 5 Mar 1945 | The Class of 1929 | | lasting: −25% training time, +0.25% recruitable population | all boys born in 1929 called up, sent to the front after a short basic training [4] |

**Design notes:**
- **Amounts.** Oscar's numbers are used where he gave them: the State AA
  +1.5%, the Volksopfer's and the air force's −25 PP, the class of 1929's
  −25% training time and +0.25% recruitable population, the Gustloff's
  −1,500. The rest are my choices within his ranges:
  - the Flak women: 7,500 (he said 5–10k);
  - the labour service: a one-time 10,000 rather than a lasting factor;
  - the Volkssturm women: 5,000 and −2% stability;
  - the Volksopfer: 4,000 + 1,000 (he said "perhaps 5k").

  The sources give no figures for these.
- **Vlasov's air force** only comes if Vlasov was recruited with the mod's
  decision: without him there is no Russian Liberation Army to give an air
  force to.
  - The −25 PP is the political cost Oscar asked for.
  - The 30 aircraft are the combat part of a formation that had 87 aircraft
    in all, many of them liaison and training planes.
  - They are Germany's current fighter and ground-attack designs, given the
    way the base game does it (`type = small_plane_airframe`).
  - **Corrected in section 17:** this was wrong. The game gave Ta 152
    fighters and pre-war ground-attack planes. The event now gives the
    types the KONR air force flew, Bf 109 G and Ju 87.
- **The Volksopfer** gives old kit (the 1918 rifles), because what was
  collected was old and mixed.
  - **Changed in section 18:** the sources name clothing and equipment,
    not weapons. The event now gives field equipment and warmer clothing;
    the rifles come from the call for weapons.
- **Rommel.** The author's own 20 July event can already retire Rommel (its
  option "Let the Gestapo sort this out").
  - This event then only tells the story; otherwise Rommel leaves service
    here.
  - Either way it fires on 14 October, while the regime stands.
- **The Gustloff.**
  - **The manpower:** the −1,500 stands for the naval personnel aboard (918
    U-boat trainees, 373 naval auxiliaries, 162 wounded soldiers and 173
    crew; almost none survived [5]).
  - **Oscar's request:** to portray it as a war crime and a horrible act.
  - **What the event does:** it describes the horror and the civilian death
    toll, and gives the judgement "nothing less than a crime" as the view of
    the survivors and the families of the dead.
  - **The historical assessment:** historians generally do not classify it
    as a war crime. The ship carried anti-aircraft guns and military
    personnel and was not a marked hospital ship; Günter Grass called it "a
    terrible result of war" [5]. The event does not state otherwise as fact.
- **Pictures:** base-game pictures, chosen by looking at them. The game has
  none of women, youths or Flak batteries.

**Changed in section 18 (Oscar's review):**
- **Vlasov's air force** gives +600 manpower instead of +5,000.
- **The Volksopfer** no longer gives rifles. It gives 1,000 support equipment
  and 90 days of −10% winter attrition. The rifles now come from the
  decision "Call on Citizens to Hand In Their Weapons", which runs
  alongside it.

**Also in this round, a Courland fix (commit `96f4a17`):** see the note at
the end of section 11.

**Checked:**
- **Check H** in verify_update.py. It covers every amount, both spirits,
  the date window and condition of each of the eight daily checks, each
  firing once, the 8 events and the 33 texts.
- **Check H was calibrated.** Four errors were planted one at a time, and
  each made it fail:
  - the Gustloff costs 1,000;
  - Rommel is retired even when he is already gone;
  - the class of 1929 could be called up in 1944;
  - the Courland popup no longer unlocks the decision.
- **Game features:**
  - `retire_character` "un-assigns a character from a nation", so
    `has_character` tells whether Rommel is still in German service. The
    game's own documentation uses Rommel as its example.
  - The four modifiers are in the game's modifier documentation.
  - Germany starts with the techs for the equipment given
    (`infantry_weapons`, `tech_support`).
- **Runtime test** (temporary test lines in Germany's history file, removed
  afterwards): all eight effects ran with no errors. Rommel was in service
  before and gone after, and both spirits were present.
- **Load test:** error.log identical (115 = 115,
  `game-logs/15-after-home-front_error.log`). setup.log shows the 8 events
  and 2 spirits loaded.

**Not play-tested yet.** Console: `event ger_homefront.1` to
`event ger_homefront.8`.

**Files:**
- `common/scripted_effects/GER_homefront_effects.txt` (all effects, also
  used by the runtime test)
- `common/ideas/GER_homefront_ideas.txt` (the two lasting spirits)
- `common/on_actions/GER_homefront_on_actions.txt` (the eight daily checks)
- `events/GER_homefront_events.txt` (8 events)
- `localisation/english/GER_homefront_l_english.yml` (33 texts)

Sources:
- [1] Deutsches Historisches Museum, LeMO, *Jahreschronik 1944*: 15 August
  (women's labour service to 50), 14 October (Rommel), 17 November (RAD
  women as Flak helpers).
- [2] de.wikipedia, *Erwin Rommel*:
  - 14 October 1944, Burgdorf and Maisel at Herrlingen;
  - the official cause, "Herzschlag, als Folge eines im Westen erlittenen
    Dienstunfalls";
  - the state funeral on 18 October 1944 in Ulm, with Rundstedt's eulogy
    ("Sein Herz gehörte dem Führer").
- [3] ru.wikipedia, *Военно-воздушные силы Комитета освобождения народов
  России*: Göring's order of 19 December 1944, the planned squadrons, under
  Vlasov from 4 February 1945, about 5,000 men and 87 aircraft.
- [4] Deutsches Historisches Museum, LeMO, *Jahreschronik 1945*: 6 January
  (Volksopfer), 30 January (Gustloff, 9,000 refugees dead), 12 February
  (women and girls for the Volkssturm), 5 March (the class of 1929).
- [5] en.wikipedia, *MV Wilhelm Gustloff*:
  - she left Gotenhafen on 30 January 1945;
  - S-13 (Marinesko): three torpedoes struck;
  - Heinz Schön's figures: 10,582 aboard, including 8,956 civilians; about
    9,343 dead;
  - "by far the largest loss of life in maritime history resulting from the
    sinking of a single vessel";
  - the war-crime question.
- [6] en.wikipedia, *Volkssturm*: women and girls from 12 February 1945,
  girls as young as 14 trained in using weapons.

### 15. Starting as the United Kingdom crashed the game (commit `e578b10`)

Reported by the author: choosing the UK crashes the game at once. He thought
it had to do with wars, because disabling some wars once helped.

**Reproduced.** The game's own start option `-start_tag=ENG` starts a new
1944 game directly as the UK. It crashed about a second after the game
launched, before the map appeared, every time. It crashed the same way with
the **unchanged Steam Workshop version**, so the crash is older than this
update. The USA, Canada, the Raj, the Soviet Union, Germany, Japan, France
and the Netherlands all started.

**Cause:**
- On 1 January 1944 four Allied countries control no land: Poland,
  Yugoslavia, the Philippines and British Burma. They are at war, because
  they are in the Allied faction or are colonies of its members. So the game
  makes them capitulate while it is still setting up the game, before the
  interface exists.
- A faction member that capitulates becomes a government in exile in the
  faction leader, the UK. The game then shows the host a popup: "We now host
  X as a Government in Exile".
- When the UK is the player, that popup is made before the interface exists,
  and the game crashes. With any other country as the player there is no
  popup, so nothing happens.
- This matches the author's observation: without the wars nobody
  capitulates.
- The author had hit this twice before:
  - `#add_to_faction = BEL #crashes` in the UK history;
  - `JAP = { transfer_state = 336 } # ... otherwise uk crashes` in
    `do_on_actions.txt`. State 336 is Singapore, the last land of British
    Malaya, which is in the faction.

**How it was found** (details in INVESTIGATION.md, section E):
1. **Bisection.** Mod folders were moved aside one group at a time, so the
   game used its own files instead. Only the country history files mattered.
   Among them, Germany's and Japan's files were each enough on their own:
   each puts the UK at war.
2. **The crash report.** `tools/crash_site.py` maps the report's stack to
   the game's own source-file names and texts. The crashing function is in
   `geography/country.cpp`. It uses the text "is trying to become an exile on
   capitulation" and the `NEW_EXILE_POPUP` texts, and it is called from the
   game setup (`CInGameIdler::InitData`).
3. **Who capitulates.** A temporary logger (`on_capitulation`) showed who
   capitulates during setup, in this order: Belgium, Poland, Yugoslavia, the
   Philippines, the Dutch East Indies, Burma. The UK game died right after
   Poland.
4. **One at a time.** Taking the countries out one by one moved the crash to
   the next one (Yugoslavia, then the Philippines, then Burma), until it was
   gone.

**Fix (4 files), the same way as the author's Belgium fix:**

| File | Change |
|---|---|
| `history/countries/ENG - Britain.txt` | Poland, Yugoslavia and the Philippines are no longer added to the Allied faction; Burma is no longer made a UK colony (lines turned into comments, with the reason) |
| `history/countries/USA - USA.txt` | the Philippines is no longer made a US colony |
| `history/countries/YUG - Yugoslavia.txt` | its `become_exiled_in` (UK, legitimacy 30) is turned into a comment... |
| `common/on_actions/do_on_actions.txt` | ...and moved here, into `on_startup`, which runs after the interface exists. It already made Poland and Burma exiles in the UK and the Philippines in the USA |

The Dutch East Indies also capitulate during setup while in the faction, but
they don't become an exile, cause no popup and were left as they were.

**Result.** The same logger recorded each country at game start and on
2 January 1944, before and after the fix. The USA was the player, since
the UK could not be played before the fix:

| Country | Before | After |
|---|---|---|
| Poland, Yugoslavia | exile in the UK, Allied faction | the same |
| Burma | exile in the UK, Allied faction, UK colony | exile in the UK, Allied faction, **not a colony** |
| Philippines | exile in the USA, Allied faction, US colony | exile in the USA, Allied faction, **not a colony** |
| Ethiopia, Iceland | exiles in the UK at game start | the same |
| Belgium, Dutch East Indies | capitulated, not exiles | the same |

**One difference, your call:** the Philippines and Burma are no longer
colonies.
- **Why not make them colonies again in `on_startup`?** That was tried. It
  pulls them back into the war, they capitulate again on 3 January, and the
  Philippines' exile moves from the USA to the UK.
- **Does anything depend on it?** Nothing in the mod checks whether they are
  Allied colonies. Only Japan's focuses check `has_subject` for Japan's own
  puppets.
- **Not tested:** what the difference means later, for example when they are
  liberated.

**Also seen, unchanged by the fix:** the Greek government ("Kingdom of
Greece", created by the author's scripts) holds no land either. It
capitulates on 3 January 1944 in every game, before and after the fix, during
normal play. In the UK game that popup caused no crash.

**Checked:**
- **The UK starts** and runs into 3 January 1944 (`-start_speed=5`). Germany,
  the Soviet Union, Japan, France, the Netherlands and the USA start too.
- **The Workshop version still crashes** the same way with the same test
  (the control).
- **Check E** in verify_update.py:
  - Poland, Yugoslavia, the Philippines and Belgium are not in the history
    faction list;
  - Burma and the Philippines are not colonies in history;
  - Yugoslavia is not an exile in history;
  - `on_startup` has all six exiles and the Singapore transfer.
- **Check E was calibrated.** Four errors were planted one at a time, and
  each made it fail:
  - Poland back in the faction;
  - Yugoslavia's history exile back;
  - Burma a colony again;
  - Yugoslavia missing from `on_startup`.
- **Load test:** error.log identical to log 15, except for one line number
  (`game-logs/17-after-uk-crash-fix_error.log`). The UK file is one comment
  line longer, so a warning that was already there moved from line 2051 to
  line 2052.

**Test it yourself:**
- In the launcher: start the 1944 game as the United Kingdom.
- Or from the project folder:
  `powershell -ExecutionPolicy Bypass -File tools\start_as_country.ps1 -Tag ENG`
  (it restores the launcher's playset afterwards). Add
  `-ModFile ugc_3070639276.mod` to run the Workshop version, which crashes.

**A rule for the future** (also in HANDOVER.md): a country that controls no
land at the game start must not be at war inside a faction, whether as a
member or as a member's colony. Make it an exile in `on_startup` instead.

### 16. Five war measures for Germany (commit `ddda13e`)

Asked for by Oscar, with the effects he gave; 50 political power each unless
stated, each once. Sources are listed at the end of the section.

| Decision (tab) | From | Cost | Effect |
|---|---|---|---|
| **Expand the KONR Armed Forces** (Collaborationist) | 23 Nov 1944, the order that began the first KONR division at Münsingen [1] | 50 PP | A popup with a choice: **two more KONR divisions** at low experience and half equipment (the 4th at once, the 5th after 60 days), each paying the equipment it arrives with, 805 infantry equipment, 15 support equipment and 6 artillery, from the stockpile; **or 12,000 manpower** |
| **Emergency Railway Repair Programme** (War Measures) | 1 Sep 1944 | 50 PP | 120 days: Railway Repair Speed +30%, Infrastructure Repair Speed +20%, Construction Speed −10% |
| **Send the Student Companies to the Front** (War Measures) | 1 Oct 1944, the winter semester 1944/45 [7] | 50 PP | +20,000 manpower; a lasting spirit, −5% research speed and −1% stability; a popup |
| **Call on Citizens to Hand In Their Weapons** (War Measures) | 18 Oct 1944, the Volkssturm's public launch [10] | 25 PP | +2,000 Basic Infantry Equipment; no stability cost |
| **Confiscate Civilian Firearms** (War Measures) | 1 Dec 1944, only after the call | 50 PP | +7,500 Basic Infantry Equipment, −1% stability |

**Changed in section 18 (Oscar's review):**
- **Expand the KONR** from 27 Feb 1945, at 30% equipment with old rifles
  rolled per division, paying 453 rifles, 9 support equipment and 4 guns.
- **The railway programme** lasts 90 days.
- **The call for weapons** opens on 7 Jan 1945, with the Volksopfer.
- **The confiscation** opens on 29 Jan 1945.

**The KONR decision and the author's own:**
- **What the author already has.** The "Collaborationist" tab has "Recruit
  Andrey Vlasov" (it creates the "Russische Befreiungsarmee" division
  template) and "Russian Liberation Army" (25 PP, human players only). The
  latter raises the 600th, 650th and 700th divisions, the KONR's historical
  1st, 2nd and 3rd.
- **So this decision adds a 4th and a 5th.** Himmler had won Hitler's
  permission for ten Russian divisions [3], but only three were formed, all
  incomplete. The new decision needs the author's template, so Vlasov must
  have been recruited first.
- **Your call:** with both decisions a player can have five KONR divisions,
  more than ever existed. The manpower option avoids that.
- **Why each division pays for its equipment.** In a running game Germany's
  army drew almost the whole rifle stockpile in the first five days of 1944
  (about 29,000 rifles). A division that started empty would therefore stay
  empty for a long time. So the divisions arrive half equipped, like the
  author's, and exactly that half is taken from the stockpile.
  - A full division of the author's template needs 1,610 rifles, 30 support
    equipment and 12 guns (16 infantry battalions, an engineer company and
    an artillery company).
    - **Corrected in section 18:** the template has 15 battalions (two share
      a slot), so a full division needs 1,510 rifles. That was measured in
      the game.
  - The payment is taken type by type, oldest rifles first (see section 17
    for why).
  - The option is only offered with that much in stock. The 5th division is
    raised after 60 days only if Germany is still at war with the Soviet
    Union and can still pay; otherwise it is not raised and nothing is paid.
- **Where they appear:** in Württemberg or Baden if held (Münsingen and
  Heuberg, where the KONR divisions formed [1]), otherwise in another German
  core state that Germany holds.
- **The manpower option (12,000)** is about the strength of the KONR's 2nd
  division in April 1945 (11,856 men [4]).
- **The popup says why many joined:** to get out of the prisoner-of-war
  camps, where millions of Soviet prisoners had died.

**The other four:**
- **Railway repair.** These are the game's own modifiers with exactly
  Oscar's names ("Railway Repair Speed" is `repair_speed_rail_way_factor`).
  The −10% applies to all construction, as the base game has no modifier
  for "building elsewhere". The text names who did the work:
  - Reichsbahn repair gangs, the Organisation Todt and forced labourers;
  - the SS railway construction brigades, formed in autumn 1944 from
    concentration camp prisoners, about 500 each, kept in freight wagons
    and moved from one bombed station to the next [5].
- **The student companies.** Oscar asked for better wording and research, a
  popup and a second small penalty.
  - **The history:** since 1941/42 most male students were
    "soldier-students", soldiers detached to study war-important subjects
    such as medicine, chemistry and engineering, under military discipline
    [7]. They went to the front in the vacations [9]. In the winter
    semester 1944/45 the student companies were sent to the front for good
    [8].
  - **The 20,000 men:** there were 19,123 male medical students in 1943
    alone [8]. Oscar gave a range of 10,000–30,000.
  - **The second penalty** is −1% stability. The obvious medical penalty,
    fewer wounded returning (`casualty_trickleback`), was rejected: the base
    game never uses it below zero, so what a negative value does is
    unknown.
- **The weapons.**
  - **The call:** by 18 November 1944 the Gauleiters had to report which
    weapons could be issued to the Volkssturm, private ones included, down
    to shotguns and small-bore rifles. One Party district in Upper Franconia
    counted 107 hunting weapons in private hands on 25 November [11].
  - **The confiscation:** in December 1944, households were to be checked
    for weapons still kept at home [11].
  - **"Infantry Equipment I (worst)":** in the game, "Infantry Equipment I"
    is the second rifle type; the worst is **Basic Infantry Equipment**
    (`infantry_equipment_0`). The decisions give the worst, as Oscar
    intended, and as the home front's Volksopfer does. Easy to change.
  - **The Volksopfer event (6 January 1945, section 14)** is the later
    collection of clothes and equipment. Both can happen.

**Checked:**
- **Check M** in verify_update.py covers:
  - costs, tabs and start dates;
  - the confiscation needing the call;
  - the 120-day modifier;
  - every amount, the spirit and the payment (needs and types);
  - both divisions (template, experience, equipment, place);
  - the stock the option and the 5th division require;
  - the events and the 21 texts;
  - that every equipment type the effects read is in the synchronized
    token list.
- **Check M was calibrated.** Five errors were planted one at a time, and
  each made it fail:
  - the call costs 50;
  - the confiscation without the call;
  - a division pays 800 rifles;
  - the railway programme lasts 60 days;
  - a type is missing from the token list.
- **Runtime test** (a temporary daily script in a running German game,
  started directly as Germany; removed afterwards). Each effect ran and was
  measured:
  - KONR option A: +1 division, and exactly 805 rifles, 15 support
    equipment and 6 guns left the stockpile. The same for the 5th
    division's path.
  - Option B: +12,000 manpower.
  - The students: +20,000 manpower, and the spirit is present.
  - The call: +2,000 Basic Infantry Equipment.
  - The confiscation: +7,500.
  - Stability read 100% before and after the confiscation: Germany's
    stability starts above the cap, so the −1% does not show.
- **Synchronized tokens:** reading an equipment stockpile in a script made
  the game warn 24 times that the types "can cause OOS" (multiplayer out of
  sync). The new file `common/synchronized_dynamic_tokens/GER_equipment_tokens.txt`
  lists them, as the base game's `tokens.txt` does for its own; the warnings
  are gone.
- **Load test:** error.log identical to log 17
  (`game-logs/18-after-war-measures_error.log`). setup.log shows 5
  decisions, 3 events and 1 spirit loaded.

**Not play-tested yet.** Console: `event ger_measures.1` (the KONR choice),
`event ger_measures.3` (the students' popup). For the KONR decision, first
take the author's "Recruit Andrey Vlasov".

**Files (all new):**
- `common/decisions/GER_measures_decisions.txt`
- `common/scripted_effects/GER_measures_effects.txt`
- `common/ideas/GER_measures_ideas.txt`
- `events/GER_measures_events.txt`
- `localisation/english/GER_measures_l_english.yml` (21 texts)
- `common/synchronized_dynamic_tokens/GER_equipment_tokens.txt`

Sources:
- [1] ru.wikipedia, *1-я пехотная дивизия (РОА)*: formation began under an
  order of 23 November 1944 at the Münsingen training area; 18,000 men.
  The source does not say who issued the order (Oscar's "OKH" could not be
  confirmed).
- [2] en.wikipedia, *600th Infantry Division*: established on 1 December
  1944; handed over to the KONR on 28 January 1945. *650th Infantry
  Division*: established on 10 January 1945, never at full strength, no
  real combat.
- [3] en.wikipedia, *Russian Liberation Army*: "Heinrich Himmler persuaded a
  very reluctant Hitler to permit the formation of 10 Russian Liberation
  Army divisions"; three incomplete divisions, about 50,000–60,000 men.
- [4] ru.wikipedia, *Комитет освобождения народов России*: strength on
  22 April 1945: 1st division about 20,000, 2nd 11,856, 3rd 10,000, reserve
  brigade 7,000, air force over 5,000.
- [5] KZ-Gedenkstätte Neuengamme, *Bad Sassendorf (11. SS-Eisenbahnbaubrigade)*:
  set up in autumn 1944 by the SS Economic and Administrative Main Office
  to repair destroyed tracks and stations; as a rule 500 prisoners each,
  living in railway wagons, "concentration camps on rails".
- [6] eisenbahn-stolberg.de, the Stolberg–Walheim line 1920–1949: the
  railway near Aachen was largely spared until mid-1944; strafing attacks
  on trains from 5 September 1944; passenger service stopped on
  10 September 1944 (a local example of the September 1944 turn).
- [7] Deutsches Historisches Museum, LeMO, *Universitäten und Studierende im
  Zweiten Weltkrieg*: from 1941/42 soldier-students dominated the lecture
  halls, under military rather than academic authority, detached "zum
  Studium kriegswichtiger Fächer wie Medizin, Chemie oder Technik".
- [8] Themenportal Europäische Geschichte (clio-online): a medical student's
  letter in the Frankfurter Rundschau, 1 February 1946 ("when the student
  companies were sent to the front in the winter semester 1944/1945"), with
  Karin Hausen's commentary: 13,821 male medical students in 1941, 19,123
  in 1943.
- [9] de.wikipedia, *Studentenkompanie*: students studied normally and were
  sent to the front in the vacations (the Munich medical company, 1942).
- [10] en.wikipedia, *Volkssturm*: established on 25 September 1944; the
  official launch on 18 October 1944, a date Himmler chose for the Battle
  of Leipzig in 1813.
- [11] weltkrieg2.de, *Volkssturm-Waffen*, citing Klaus Mammach, *Der
  Volkssturm: Das letzte Aufgebot 1944/45*: the report deadline of
  18 November 1944 (including private weapons, shotguns and small-bore
  rifles); the Lichtenfels-Staffelstein report of 25 November; the checks
  of households in December 1944.

### 17. Two equipment mistakes of mine, found while testing section 16 (commit `470916b`)

Found by reading the stockpile per equipment type in a running game (the
earlier tests ran during the game's setup, when every stockpile reads 0).

**How the game handles equipment by its general type** (measured with
Germany on 1 January 1944):
- **Removing by the general type takes the amount from every type in
  stock.** `add_equipment_to_stockpile = { type = infantry_equipment amount
  = -1600 }` took 1,600 Basic Infantry Equipment **and** 1,600 Infantry
  Equipment I: 3,200 in all.
  - For artillery, −50 took 50 from the one gun type that had at least 50,
    and left the other (6 guns) alone.
  - The game's documentation says that without a producer the effect "will
    be applied to all creators".
- **Adding by the general type gives the newest type:** +50
  `artillery_equipment` came back as the newest gun, and +500
  `infantry_equipment` as Infantry Equipment III.
- **Removing one specific type takes exactly that amount.**
- **Removing with `producer = GER` removed nothing.**

**Mistake 1: the 1945 operations (section 11) lost rifles.**
- **What went wrong.** Sonnenwende and Spring Awakening set aside 500 / 750
  rifles and 50 / 75 guns by the general type and gave them back the same
  way. With two rifle types in stock, each use cost Germany about 500 / 750
  rifles for good, and the guns came back as a newer model.
- **Section 11 was wrong.** Its note "exactly what was set aside comes back"
  and check O both looked at the numbers in the script, not at what the
  game does with them.
- **The fix.** Rifles and guns are now taken type by type, oldest first. The
  amount that actually left the stockpile is stored per type (for example
  `GER_1945_sonnenwende_infantry_equipment_0`), and exactly those types and
  amounts are handed back.
- **Measured:** after the set-aside and the return, every rifle and gun type
  and the fuel were back at their starting numbers, for both operations.
  The set-aside took 500 / 750 rifles and 50 / 75 guns, and fuel was already
  exact.

**Mistake 2: Vlasov's air force (section 14) got the wrong planes.**
- **What went wrong.** The home-front event gave 20 fighters and 10
  ground-attack planes by the general type. The game handed out Ta 152 A
  fighters (Germany's newest design) and ground-attack planes on the pre-war
  airframe (Do 17, Hs 123).
- **Section 14 was wrong.** It said "Germany's current designs".
- **The fix.** The event now names the types the KONR air force flew:
  **Bf 109 G** fighters and **Ju 87** dive bombers. Its fighter squadron had
  16 Bf 109s and its bomber squadron 12 Ju 87s [1]. This uses
  `variant_name`, as the base game does.
- **Measured:** +20 on the Bf 109 G airframe and +10 on the Ju 87 airframe.

**Checked:**
- **Check O** now parses the set-aside and the return: fuel, the amounts
  required, every rifle and gun type taken, what is stored and what is
  handed back.
- **Check H** now requires the two named designs, and that Germany's history
  creates them.
- **Both were calibrated.** Each failed with a planted error: a return by
  the general type, and the ground-attack planes by the general type.
- **Load test:** error.log identical
  (`game-logs/18-after-war-measures_error.log`).
- **Other stockpile changes checked:**
  - the reserves' deliveries (section 12) and the Sailors' convoys
    (section 11) already name a specific type;
  - the author's own content wasn't changed.

**Files:**
- `common/scripted_effects/GER_1945_operations_effects.txt` (set-aside and
  return)
- `common/scripted_effects/GER_homefront_effects.txt` (Vlasov's air force)

Source:
- [1] ru.wikipedia, *Военно-воздушные силы КОНР*: 5th fighter squadron with
  16 Bf 109, 8th bomber squadron with 12 Ju 87, a training squadron; 87
  aircraft in all.

### 18. Oscar's review of sections 14 and 16 (commit `807249b`)

Oscar asked for these changes after reading sections 14 and 16:

| What | Before | Now |
|---|---|---|
| Vlasov's air force (home-front event, 19 Dec 1944) | +5,000 manpower | **+600 manpower** |
| Emergency Railway Repair Programme | 120 days | **90 days** |
| Call on Citizens to Hand In Their Weapons | from 18 Oct 1944 | **from 7 Jan 1945**, alongside the Volksopfer collection |
| Confiscate Civilian Firearms (still only after the call) | from 1 Dec 1944 | **from 29 Jan 1945**, after the Volksopfer collection closed |
| The Volksopfer (home-front event, 6 Jan 1945) | −25 PP: 4,000 rifles and 1,000 support equipment | **−25 PP: 1,000 support equipment and 90 days of −10% winter attrition** (spirit "The Volksopfer") |
| Expand the KONR | from 23 Nov 1944; half equipment; German Infantry Equipment I | **from 27 Feb 1945**; **30% equipment**; old rifles rolled per division |
| The KONR payment per division | 805 rifles, 15 support equipment, 6 guns | **453 rifles, 9 support equipment, 4 guns** |

**Vlasov's air force: why 600.**
- **The real figure:** Oscar asked how many men it had. About 5,000 in all
  [1], but most of them served in its anti-aircraft regiment, parachute
  battalion, signals company and airfield units [1].
- **What the event creates:** only the flying part, 20 fighters and 10
  ground-attack planes.
- **So 600:** the game counts 20 men per small aircraft
  (`common/units/equipment/plane_airframes.txt`), so these 30 aircraft need
  600 men to deploy.

**The weapons and the Volksopfer.**
- **Timing:** Oscar asked for the call to come with the Volksopfer.
  Goebbels, Himmler and Funk called for it on 5 January 1945. From 7 to 28
  January (later extended to 11 February) the population handed in
  clothing and equipment at 60,000 Party collection points [2]. The
  posters read "Volksopfer! Gib alles für die Front!" [3].
- **The call now opens on 7 January.** Its text ties it to the collection
  and to the Party's registration of private weapons since November
  (section 16).
- **The sources name clothing and equipment for the Volksopfer, not
  weapons** [2], [4]. It brought in 80,000 tonnes of textiles.
  - My home-front event (section 14) had it give 4,000 rifles. With the
    call now running alongside it, that would count the same rifles twice.
  - So the event keeps its 1,000 support equipment (the equipment part)
    and now adds 90 days of −10% winter attrition for the donated coats,
    boots and blankets. The base game uses the same modifier in Finnish
    and Czechoslovak spirits.
  - **The rifles now come from the call.**
- **The confiscation** opens on 29 January, after the collection closed on
  28 January. Its text mentions the household checks the Party had ordered
  in December (section 16).

**Expand the KONR.**
- **27 February 1945 is Oscar's date** for the plans to expand the KONR. My
  sources don't name an event on that day. They do say that the 3rd KONR
  division began forming in the first half of February 1945 and never got
  weapons [5], so a 4th and 5th after that follows on.
- **It still needs the author's "Recruit Andrey Vlasov" first.**
- **Poorly armed, as Oscar asked.** The divisions arrive with 30% of their
  equipment and old rifles.
  - The game gives a division only one rifle model, so each division rolls
    it, as the author's Volkssturm does. The weights are Oscar's mix:
    German rifles from depot stocks 50, captured Soviet 40, captured
    Italian 5, captured French 5.
  - All are Basic Infantry Equipment of that maker. Italian and French
    rifles are only rolled while those countries exist.
- **The payment is 30% of a division's equipment:** 453 rifles, 9 support
  equipment and 4 guns.
  - The game makes 3.6 guns; 4 is rounded up.
  - **The rifle figure was wrong before.** The author's template lists 16
    infantry battalions, but two share the slot `x = 1, y = 2`, so the game
    builds 15. A full division therefore needs 1,510 rifles, not 1,610.
  - Measured in the game: 453 rifles, 9 support equipment and 3.6 guns per
    division.
  - The author's template was left as it is; his own three ROA divisions
    have 15 battalions too.
- **Still open, your call:** the new divisions take no manpower from the
  pool. Measured: manpower was the same before and after creating them.
  Oscar was offered a fix but hasn't chosen yet.

**Checked:**
- **Checks H and M** now cover all of this:
  - the dates, the 90 days and the 600 manpower;
  - the Volksopfer's new effect and spirit;
  - the rifle roll's weights, makers and guards;
  - the 453/9/4 payment and the stock the option requires.
- **Calibrated:** five planted errors each made the right check fail.
  - Check M: the KONR from 23 Nov 1944; the railway programme 120 days; the
    Soviet weight 50.
  - Check H: Vlasov's air force +5,000; the Volksopfer's 4,000 rifles.
- **Runtime test** (a temporary daily script in a running German game,
  removed afterwards):
  - the payment was exactly 453 / 9 / 4;
  - eight rolled KONR divisions were created without errors, each with 453
    rifles;
  - Vlasov's air force gave +600 manpower, 20 Bf 109 G and 10 Ju 87;
  - the Volksopfer gave +1,000 support equipment and its spirit, and no
    rifles.
- **Load test:** error.log identical to log 18
  (`game-logs/20-after-review-round-2_error.log`).

**Files:**
- `common/decisions/GER_measures_decisions.txt`
- `common/scripted_effects/GER_measures_effects.txt`
- `events/GER_measures_events.txt`
- `localisation/english/GER_measures_l_english.yml`
- `common/scripted_effects/GER_homefront_effects.txt`
- `common/ideas/GER_homefront_ideas.txt` (the new spirit)
- `localisation/english/GER_homefront_l_english.yml`

Sources:
- [1] ru.wikipedia, *Военно-воздушные силы КОНР*: strength 5,000; besides
  the aviation regiment, an anti-aircraft artillery regiment, a parachute
  battalion and a signals company.
- [2] de.wikipedia, *Volksopfer für Wehrmacht und Volkssturm*:
  - the call by Goebbels, Himmler and Funk on 5 January 1945;
  - clothing and equipment from 7 to 28 January, extended to 11 February;
  - 60,000 collection points and 80,000 tonnes of textiles;
  - no weapons are named.
- [3] Hoover Institution Library & Archives, poster "Volksopfer! Gib alles
  für die Front! Bis 28. Januar 1945. Annahmestellen in allen Ortsgruppen
  der NSDAP."
- [4] Deutsches Historisches Museum, LeMO, *Jahreschronik 1945*, 6 January:
  the call for the "Volksopfer" to collect for the equipment of the
  Volkssturm.
- [5] ru.wikipedia, *3-я пехотная дивизия (РОА)*: formation began in the
  first half of February 1945 at Münsingen; about 10,000 men by the end of
  the war, not armed.

### 19. Five flavour events: the Indian Legion, the Handschar, the Eastern Legions, Wiking, Nordland (commit `04f75bb`)

Asked for by Oscar. Each event fires once for Germany, on or after its
historical date, and only while its situation still holds.

| Event | From | Condition | Effect |
|---|---|---|---|
| The Indian Legion Comes Home | 15 Aug 1944 [1] | at war with the UK or the USA, and an enemy holds Paris (11506) | none |
| The Handschar Falls Apart | 5 Oct 1944, after the fighting at Janja on 3–4 October [2] | Croatia exists | −2,000 manpower |
| The Eastern Legions Pass to the SS | 30 Dec 1944 [4] | at war with the Soviet Union | +3,500 manpower |
| Wiking at Cherkassy | 17 Feb 1944, the night of the breakout [5] | at war with the Soviet Union | +10 army experience, +2% war support |
| The Blue Hills (Nordland) | 10 Aug 1944, the end of the battle for the Tannenberg Line | at war with the Soviet Union; Germany holds state 813 (with Narva, 4640) or 812 (Tallinn) | +10 army experience, +2% war support |

**Design notes:**
- **The Indian Legion (Legion Freies Indien, Infanterie-Regiment 950):**
  - Raised by Subhas Chandra Bose from Indian prisoners of war, up to
    4,500 men [1].
  - Transferred to the Waffen-SS on 8 August 1944 [1].
  - Left Lacanau for Germany on 15 August, fighting on the way; three
    officers were killed and 25 men went over to the Resistance [1].
  - Alleged crimes in the Médoc and around Ruffec [1].
  - It then trained at Camp Heuberg until March 1945 and never fought
    again as a unit [1], so the event has no effect.
  - The trigger (an enemy holds Paris) stands for the Allied advance that
    made the coast untenable.
- **The Handschar:**
  - Tito's amnesty came on 17 August 1944. Over 2,000 Bosnians deserted in
    the first three weeks of September, many with their weapons, and over
    700 joined the Partisans by early October [2].
  - After Janja (3–4 October), Army Group F judged the division's combat
    value "minimal" [2]. The remnant became Kampfgruppe Hanke.
  - Its crimes against Serb and Jewish civilians [2] are named in the text.
  - The division is not in the mod's 1944 order of battle; only its name
    is in the division-name list. So the loss is manpower (−2,000, the
    deserters), not a unit.
- **The Eastern Legions:**
  - The Army's legions had 53 field battalions, about 53,000 men [3].
  - On 20 October 1944 the East Muslim SS Regiment became the
    "Osttürkischer Waffen-Verband der SS" in Slovakia, 5,000 strong.
  - On 30 December its Azerbaijani group passed to the new "Kaukasischer
    Waffen-Verband der SS".
  - On Christmas Eve 450 men deserted and 300 came back [4].
  - The East Turkic unit grew to 8,500 by February 1945 [4]. The +3,500
    is that growth, as remnants were gathered in.
- **Wiking:**
  - About 60,000 men were trapped in the Korsun–Cherkassy pocket, and
    about half broke out on 16–17 February 1944. Wiking lost nearly all
    its heavy equipment [5].
  - In the mod's 1944 start Wiking stands at Cherkassy (province 11424,
    state 203; section 10). The event has two texts: the breakout if an
    enemy holds state 203, or holding the line if Germany still does.
- **Nordland:**
  - From 27 July 1944 it fought at the Tannenberg Line, in the Blue Hills
    (Sinimäed) west of Narva, alongside the Estonian 20th SS Division and
    elements of "Großdeutschland" [6].
  - Its commander, Fritz von Scholz, was killed on 28 July [6].
  - Its regiments were named "Norge" and "Danmark", although about 80% of
    its men were Germans [6].
- **"Positive, about how good they are" (Oscar):** the texts stay factual
  about the fighting and the losses; the effect is a small army-experience
  and war-support gain.
  - **The historical record:** both divisions belonged to the Waffen-SS,
    which the Nuremberg tribunal declared a criminal organisation.
  - **Wiking:** a former member described civilians burned in a church in
    Ukraine in autumn 1941 [5].
  - **Nordland:** its "Danmark" regiment took part in burning villages in
    the Banija region of Croatia in October 1943 [6].
  - The events do not glorify this.
- **Pictures:** base-game pictures, chosen by looking at them:
  - the Indian Legion: turbaned soldiers (`indian_parade`);
  - the Handschar: Yugoslav partisans;
  - the Eastern Legions: foreign volunteers in German uniform (the
    picture is of the Latvian Legion; the game has none of these legions);
  - Wiking: soldiers in the snow;
  - Nordland: German troops (the same picture as the student-companies
    event, section 16).

**Checked:**
- **Check L** in verify_update.py covers the five date windows and
  conditions, each event once, the effects, Wiking's two texts, that the
  pictures exist in the base game, the province-to-state facts (11424 in
  203, 4640 in 813, 3152 in 812) and the 17 texts.
- **Calibrated:** two planted errors each made it fail (the Handschar
  costs 3,000; Nordland fires without Estonia held).
- **Runtime test** (a temporary daily script in a running German game,
  removed afterwards):
  - the Handschar gave −2,000 manpower and the Eastern Legions +3,500;
  - Wiking and Nordland each gave +9 army experience, not 10: Germany's
    own experience modifiers apply;
  - there were no errors.
- **Load test:** error.log identical (log 22); setup.log shows the 5
  events loaded.

**Not play-tested yet.** Console: `event ger_legions.1` to
`event ger_legions.5`. For Wiking's other text: `setcontroller SOV 11424`,
then `event ger_legions.4`.

**Files (all new):**
- `common/scripted_effects/GER_legions_effects.txt`
- `common/on_actions/GER_legions_on_actions.txt`
- `events/GER_legions_events.txt`
- `localisation/english/GER_legions_l_english.yml` (17 texts)

Sources:
- [1] en.wikipedia, *Indian Legion*.
- [2] en.wikipedia, *13th Waffen Mountain Division of the SS Handschar (1st
  Croatian)*, section "August 1944 – May 1945".
- [3] de.wikipedia, *Ostlegionen*: 53 field battalions, 53,000 men.
- [4] en.wikipedia, *Azerbaijani SS volunteer formations*:
  - 20 October 1944, the move to Slovakia and the renaming;
  - 30 December 1944, the Azerbaijani group transferred;
  - the Christmas Eve desertions;
  - strengths (from a search summary of the same page: 5,000 from October
    1944 to January 1945, 8,500 from February 1945).
- [5] en.wikipedia, *5th SS Panzer Division Wiking*.
- [6] en.wikipedia, *11th SS Volunteer Panzergrenadier Division Nordland*.

### 20. The bridge at Remagen (commit `222caf2`)

Asked for by Oscar: an event when the Remagen bridgehead is taken, as
happened historically, with options, and a real photograph.

**When it fires:** once, on the first day a western enemy of Germany (at
war with it, not the Soviet Union) holds **province 529**, the east bank of
the Rhine opposite Remagen (Erpel), where the Ludendorff Bridge ended.
- **How 529 was found:**
  - The game map was fitted to the real coordinates of nine cities: the
    victory points of Köln, Bonn, Koblenz, Düsseldorf, Frankfurt,
    Wiesbaden, Mainz, Trier and Aachen, with residuals of 1–8 map pixels.
  - Remagen falls on the west bank south of Bonn, in 3547/11494. The
    game's own river layer (`map/rivers.bmp`) shows the Rhine between
    11494 (west, state 42) and 529 (east, state 51).
- **It links to the author's own Rhine events:** 529 is one of the
  east-bank provinces in his "Rhine crossing" effect (GER_rhine_crossing in
  `germany_scripted_events_mod.txt`). His "Defence of the Rhine" event
  orders the bridges blown; Remagen is the bridge that wasn't.
- **The text names the captor** ("American troops have crossed the
  Rhine..."). The captor is saved as the global event target
  `GER_remagen_captor`.
  - Tested: firing the event from inside the captor's scope did **not**
    make it `FROM` (FROM stayed Germany).
  - With the event target, a test event named the United States
    correctly.

**The options:**

| Option | Effect |
|---|---|
| Court-martial them, and destroy the bridge at any cost (what Hitler did) | −25 PP, −2,000 fuel, −2% stability; 10 days later the bridge collapses (event 2): the railway in province 529 is damaged by 2 |
| Contain the bridgehead; the Luftwaffe has better targets | nothing: no court-martial, and the bridge stands |

**History** [1], [2], [3]:
- **7 March 1945:** the US 9th Armored Division found the bridge standing.
  Its demolition charges, weak civilian explosive, damaged it but did not
  bring it down.
- **Troops across:** six divisions, about 125,000 men.
- **Hitler's reaction:** on 9 March he set up the Flying Court-Martial
  West under Generalleutnant Rudolf Hübner. On 13–14 March it sentenced
  five officers to death, and four were shot in the Westerwald; Hauptmann
  Bratge, already a prisoner, was sentenced in absentia. Rundstedt was
  replaced by Kesselring.
- **The attempts to destroy the bridge:**
  - 367 Luftwaffe aircraft attacked it in ten days, including Arado Ar 234
    jet bombers;
  - 11 V-2 rockets were fired at it, killing six Americans;
  - seven naval frogmen were sent;
  - the 600 mm Karl-Gerät mortar shelled it.
- **17 March 1945:** the bridge collapsed. 28 US engineers were killed
  according to the English source, 32 according to the German one; the
  text says "dozens".
- **Pontoon bridges** had already been built beside it.

**The −2% stability** stands for the terror of the court-martial. The
**rail damage** stands for the loss of the railway bridge; the Ludendorff
Bridge was a railway bridge.

**The photograph:**
- "U.S. First Army at Remagen Bridge before four hours before it collapsed
  into the Rhine", about 17 March 1945. U.S. National Archives, NAID
  195341, via Wikimedia Commons [4].
- **Public domain:** a work of the US Federal Government.
- **Downloaded with Oscar's permission** (3.2 MB, 3000 × 2426).
- **Cut to the game's format:** 210 × 176, a sepia tone, a paper border,
  tilted 2°, in the same uncompressed DDS format (and the identical file
  header) as the author's own event pictures in `gfx/events/`.
- **Sprite:** defined in a new file, `interface/GER_remagen.gfx`, so the
  author's `1944.gfx` is unchanged. The credit is in that file too.

**Checked:**
- **Check X** covers the trigger, the effects, both events, the picture
  (its size and a header identical to the author's DDS), the sprite, the
  province-to-state facts and the 10 texts.
- **Calibrated:** two planted errors each made it fail (watching 11494
  instead of 529; rail damage 5).
- **Runtime test:**
  - option A: −25 PP and −2,000 fuel, exact;
  - the collapse ran without errors;
  - the captor's name in a fired event: "United States / American".
- **Load test:** error.log identical (`game-logs/22-after-legions-and-remagen_error.log`);
  setup.log shows the 2 events loaded.

**Not play-tested yet.** Console: `setcontroller USA 529`, and the event
fires on the next day. Or `event ger_remagen.1`, but the captor's name is
then empty, because the console doesn't set it.

**Files (all new):**
- `events/GER_remagen_events.txt`
- `common/on_actions/GER_remagen_on_actions.txt`
- `common/scripted_effects/GER_remagen_effects.txt`
- `localisation/english/GER_remagen_l_english.yml` (10 texts)
- `interface/GER_remagen.gfx`
- `gfx/events/report_event_GER_remagen_bridge.dds`

Sources:
- [1] en.wikipedia, *Ludendorff Bridge*.
- [2] en.wikipedia, *Battle of Remagen*: 367 aircraft, Ar 234, 11 V-2s,
  seven frogmen, the Karl-Gerät.
- [3] de.wikipedia, *Ludendorff-Brücke*: the Flying Court-Martial West,
  the sentences and executions, Kesselring, the collapse (32 dead, 63
  injured).
- [4] Wikimedia Commons, *File:WWII, Europe, Germany, "U.S. First Army at
  Remagen Bridge before four hours before it collapsed into the Rhine" -
  NARA - 195341.jpg*.

**Recovery note (29 September 2026).** Sections 21–26 were recovered from
Claude's unfinished local draft. Their earlier runtime results are records
from that session, not newly repeated tests. The Codex checks and limitations
are recorded in section 27.

**About Oscar's pictures (sections 21, 22, 23 and 26).** Oscar chose four
pictures for these events; their sources are not recorded. Three events are
alternate history, and their pictures are illustrations of it:

| Event | Picture |
|---|---|
| Wiking before Warsaw | a wartime photograph: a Panzer III with Waffen-SS soldiers in camouflage smocks, in summer; date, place and unit unknown |
| The first German bomb | an illustration: German officers watching a nuclear explosion near a tower |
| Leningrad taken | an illustration: soldiers with "Nordland" cuff titles on the Nevsky Prospect, St Isaac's Cathedral behind |
| The invasion beaten back | German machine-gunners on a cliff above a beach full of landing craft, a plane falling in flames |

- Each is converted the same way as the Remagen photograph (section 20):
  cut to 210 × 176, a sepia tone, a paper border, a slight tilt, in the
  DDS format (and with the same file header) as the author's own pictures
  in `gfx/events/`. Each `.gfx` file says what its picture is.
- The Wiking photograph shows the whole tank, as Oscar asked (a first
  version left out its front plate; commit `df4cc07` restored it).

### 21. Wiking before Warsaw (commit `a2790cb`)

Oscar asked for his photograph of Wiking to be used for an SS Wiking event.
It shows a tank and its crew in summer, so it doesn't fit the Cherkassy
event (section 19: a February breakout in the snow, in which Wiking lost
its tanks). It gets its own event instead, a sixth in the legions file.

- **When:** once, from 4 August 1944 to the end of 1944, at war with the
  Soviet Union, while we hold Warsaw (province 3544, state 10) and an enemy
  holds Lublin (state 92), i.e. the front has come up from the east.
- **Effect:** the same as Wiking at Cherkassy (+10 army experience, +2% war
  support; the existing effect `GER_legions_wiking`).
- **History:**
  - The Battle of Radzymin, 1–4 August 1944: the 4th and 19th Panzer
    Divisions, the "Hermann Göring" Division and the 5th SS Panzer
    Division "Wiking" counterattacked the Soviet 2nd Tank Army north-east
    of Warsaw. The 3rd Tank Corps was pocketed and destroyed near Wołomin
    on 3 August [1].
  - From 1 to 10 August the 2nd Tank Army lost 284 tanks and
    self-propelled guns [1].
  - The German counterattacks halted the Soviet offensive, and the front
    stabilised for the rest of the year [2].
  - The Warsaw Uprising began on 1 August 1944 [3]; the text mentions it.
    Wiking fought east of the city; its source does not mention it in the
    suppression of the Uprising [2]. In 1943 elements of the division took
    part in suppressing the Warsaw Ghetto Uprising [2].
- **The picture:** Oscar's (see above). Wiking had Panzer IIIs in 1942–43
  (two of its three tank companies from June 1942 [2]); by 1944 it had
  Panthers and Panzer IVs [2], so the picture is probably older than the
  event.

**Checked:**
- **Check L** now covers six events: the new date window and conditions,
  the effect, Oscar's picture (sprite and DDS format) and 20 texts.
- **Calibrated:** two planted errors each made it fail (the event without
  the Lublin condition; a base-game picture instead of Oscar's).
- **Runtime:** at the start we hold Warsaw and Lublin, so it cannot fire
  then (logged). It was not run in August 1944.

**Console:** `event ger_legions.6`.

**Files:**
- changed: `GER_legions_on_actions.txt`, `GER_legions_events.txt`,
  `GER_legions_l_english.yml`
- new: `interface/GER_legions.gfx`, `gfx/events/report_event_GER_wiking_panzer.dds`

Sources:
- [1] en.wikipedia, *Battle of Radzymin (1944)*.
- [2] en.wikipedia, *5th SS Panzer Division Wiking*.
- [3] en.wikipedia, *Warsaw Uprising*.

### 22. The first German atomic bomb (commit `ef9dbce`)

Oscar asked for a flavour event, with his picture, when Germany first has an
atomic bomb in its stockpile.

- **When:** once, the first day `num_of_nukes > 0`. Germany can get bombs
  through the author's Uranverein focus and the nuclear special projects.
- **Effect:** none (flavour only, as asked).
- **The text** follows the real Uranverein up to 1942 [1] and then departs
  from history:
  - in 1939 physicists reported the military potential of uranium fission;
  - in 1942 it became clear that the project would not decide the war in
    the near term. A conference called by Speer on 4 June 1942 continued it
    only for energy production;
  - in reality it never came close to a bomb: the last reactor experiment,
    at Haigerloch in 1945, never reached criticality, and historians agree
    that Germany was never close to a nuclear weapon [1].
- **The picture:** Oscar's illustration (see above).

**Checked:**
- **Check Q:** the trigger, one event with no effect, the picture (and its
  note in the `.gfx`), 3 texts.
- **Calibrated:** two planted errors each made it fail (two bombs needed;
  the `.gfx` note removed).
- **Runtime:** no event at the start (0 bombs). A test script gave Germany one
  bomb (`add_nuclear_bombs = 1`), and the event fired the next day. No
  error in error.log for the picture.

**Console:** `event ger_bomb.1`, or `nuke` (adds bombs) and wait a day.

**Files (all new):** `GER_bomb_on_actions.txt`, `GER_bomb_events.txt`,
`GER_bomb_l_english.yml`, `interface/GER_bomb.gfx`,
`gfx/events/report_event_GER_first_bomb.dds`.

Sources:
- [1] en.wikipedia, *German nuclear program during World War II*.

### 23. Leningrad taken (commits `a9a793d`, `97a806f`)

Oscar asked for an event, with his picture, when German troops attack the
city of Leningrad, or, if that can't be done, when they take it.

- **The attack can't be detected:**
  - HOI4 has no trigger for where a battle is fought;
  - the combat on_actions (`on_army_leader_won_combat` and
    `on_army_leader_lost_combat`) give the general, not the place;
  - a general's position (`is_in_state`) is his headquarters, not the
    battle.
- **The first version** (`a9a793d`) fired when we held province 149 and
  6174, the city's neighbours inside state 195, with the city still Soviet.
  In the 1944 start we already hold 6174 and 79 (the siege line), so "our
  troops near Leningrad" alone would fire on day one. Oscar rejected this:
  only the city itself should count.
- **Now** (`97a806f`, Oscar's fallback): once, from 1944, the first day
  we hold the city itself (province 3151) at war with the Soviet Union.
- **The game's own news event** "The Fall of Leningrad" (news.103) also
  fires, for every country, when Germany controls the state.
- **Effect:** none (flavour only).
- **The text** says that in September 1941 Hitler ordered the city starved
  into ruin rather than taken, and that hundreds of thousands of its people
  died, most of them of hunger [1]. Historians class the siege as a
  genocide [1]. The event can only fire from 1944, so the text's "since
  September 1941" holds.
- **The picture:** Oscar's illustration (see above).

**Checked:**
- **Check D:** the trigger, province 3151 in state 195, the news event,
  the picture (and its note in the `.gfx`), 3 texts.
- **Calibrated:** before 1944, and holding 149 instead of the city: both
  made it fail. The first version was calibrated too (11068 instead of 149).
- **Runtime:**
  - first version: not fired at the start. When a test script gave us 149,
    the Soviet divisions there took it back before the next day's check
    (see the testing note below). With the province given just before the
    check, it fired;
  - now: not fired on day one; fired on the day a test script gave us the
    city.

**Console:** `event ger_leningrad.1`, or `setcontroller GER 3151` and wait a
day.

**Files (all new):** `GER_leningrad_on_actions.txt`, `GER_leningrad_events.txt`,
`GER_leningrad_l_english.yml`, `interface/GER_leningrad.gfx`,
`gfx/events/report_event_GER_leningrad.dds`.

Sources:
- [1] en.wikipedia, *Siege of Leningrad*: 8 September 1941 to 27 January
  1944; the directive of 29 September 1941; the death toll; the genocide
  classification.

### 24. The Crimea: evacuate the 17th Army, or hold Sevastopol (commits `204d7de`, `b244eab`)

Proposed on 28 September as the Crimean counterpart of the Courland
evacuation (section 11); Oscar agreed on 29 September. Built the same way.

**The situation in the 1944 start:**
- The Crimea is state 137: nine provinces, with Sevastopol (3686, victory
  points 20) and Kerch (9680, Soviet-held, as the real Kerch bridgehead).
- Its only land link is the Perekop isthmus: province 568, in Kherson
  (state 196), which the mod leaves to the Soviet Union.
- Three German divisions (two mountain, one infantry) and two Romanian
  divisions stand there.
- The author's AI strategy `ROM_hold_crimea_1944` has Romania keep units in
  the Crimea while Germany holds Sevastopol.

**The popup** (once): when we hold Sevastopol, have divisions in the Crimea
and an enemy holds Perekop. In the 1944 start that is day one: the Crimea
had been cut off since November 1943 [1].
- **Evacuate** (AI 25%): the decision "Evacuate the Crimea" starts at once
  (50 political power, 30 days).
- **Hold** (AI 75%; what Hitler did): Sevastopol becomes a fortress with the
  author's Festung values, the same as Fortress Courland: +20% defence, +75%
  maximum dig-in, −25% supply use. It is removed when Sevastopol falls or
  the Crimea is evacuated. The decision stays available.

**The decision** "Evacuate the Crimea":
- **Available:** we hold Sevastopol and have divisions in the Crimea.
- **Cost:** 50 political power.
- **Time:** 30 days; the real evacuation ran from 15 April to 14 May 1944
  [1]. If Sevastopol falls, it is cancelled.
- **At the end:** every German division in the Crimea is shipped:
  - to Constanta (state 971), the historical destination [1], if we or an
    ally hold it;
  - else to Odessa (192), then Mykolaiv (197);
  - else to the capital.
- **The Romanians:** if Romania is our ally, its divisions in the Crimea go
  too: to Constanta, or home to its capital.
- **The effect used:** `teleport_armies`, as for Courland.
- **The AI** takes it only by choosing "Evacuate" in the popup; after
  "Hold" it keeps holding.

**History** [1], [2]:
- **Advice:** Manstein, Kleist, Zeitzler and Antonescu repeatedly urged
  Hitler to evacuate; he refused. Dönitz argued that the Crimea shielded
  the Balkans "like a shield".
- **Strength:** five German and six Romanian divisions, about 200,000
  soldiers.
- **The offensive:** the Soviet attack began on 8 April 1944. Sevastopol
  was declared a fortress to be held at all costs, and fell on 9 May; the
  last pockets were destroyed on 12 May.
- **The evacuation:** over 113,000 men were evacuated by sea between
  Sevastopol and Constanta, 15 April to 14 May. The sinking of the Totila
  and Teja on 10 May alone caused up to 10,000 deaths.
- **Losses:** 60 ships; 31,700 Germans and 25,800 Romanians died.
- **Command:** on 1 May, Jaenecke was replaced by Allmendinger.

The event doesn't model losses at sea. The Courland evacuation doesn't
either, and an early evacuation is the orderly one the generals asked for.

**Oscar's play-test** found that the evacuation did not happen: see section
25. The fix is `b244eab`.

**Checked:**
- **Check C** covers:
  - the popup's trigger and the fortress clean-up;
  - the destination order, each destination's condition naming the same
    state it ships to (strengthened after calibration found a gap);
  - the Romanian part;
  - the fortress modifier, equal to the author's Festung values (as used
    for Courland);
  - the decision (cost, 30 days, cancel);
  - both options (the first starts the decision itself, without an extra
    charge) and the AI weights;
  - 14 texts.
- **Calibrated:** 7 planted errors. The first run missed one: a
  destination whose condition checked Odessa but shipped to Constanta.
  The check now pairs each condition with its destination, and that error
  makes it fail.
- **Runtime** (German games started with `-start_tag`):
  - the popup fired on 1 January 1944;
  - the evacuation, run directly: the German (more than two) and Romanian
    divisions left the Crimea and were in Northern Dobruja (Constanta) the
    same day. The fortress flag was set, then cleared;
  - the decision, with its 30 days shortened to 1 for the test: with
    Germany run by the AI (divisions in armies), it took the decision on
    day 2 under the old AI weight. On day 3 its divisions were in Northern
    Dobruja. A few days later the AI shipped divisions back into the
    Crimea, since Sevastopol was still its port. That is the AI's own
    choice;
  - the popup's first option (the same effects): the decision ran and the
    divisions were out the next day; 50 political power charged;
  - with only 20 political power, the decision still ran (political power
    went to −30).
- **Load test:** error.log identical (logs 24 and 25).

**Console:** `event ger_crimea.1`.

**Files (all new):** `GER_crimea_on_actions.txt`, `GER_crimea_decisions.txt`,
`GER_crimea_effects.txt`, `GER_crimea_events.txt`,
`common/modifiers/GER_crimea_modifiers.txt`, `GER_crimea_l_english.yml`.

Sources:
- [1] en.wikipedia, *Crimean offensive*: the cut-off in November 1943, 8
  April to 12 May 1944, the evacuation of over 113,000 (15 April to 14
  May, Sevastopol–Constanta), the Totila and Teja, the fall of Sevastopol
  on 9 May.
- [2] de.wikipedia, *Schlacht um die Krim*: the advice to evacuate and
  Hitler's refusal, Dönitz, the strength, Sevastopol as a fortress,
  Jaenecke and Allmendinger, the losses.

### 25. Oscar's play-test and answers (29 September 2026)

- **The Crimea evacuation did not happen.** Oscar held Sevastopol for more
  than 30 days, and the divisions stayed.
  - **The evacuation itself works:** it was tested directly, through the
    decision, and with AI Germany (section 24).
  - **The cause:** choosing "Evacuate" in the popup only unlocked the
    decision; nothing happened until it was clicked in the decisions tab.
    His game's logs weren't available to confirm this.
  - **The fix** (`b244eab`): the popup's "Evacuate" option now
    starts the decision itself with `activate_decision`, as the base game
    does for timed decisions.
    - Tested: this charges the decision's 50 political power. With an
      extra −50 in the option it charged 100, so that line was removed.
    - It runs even with too little political power (tested with 20).
  - **The AI weight** is now 0: before, AI Germany took the decision on day
    2 whatever it had chosen.
  - **The Courland evacuation** (section 11) has the same design: its
    popup also only unlocks a decision. Not changed here; the same fix
    would apply.
- **Leningrad** (`97a806f`): only the city itself should count; the
  event now fires when we take it (section 23).
- **The KONR divisions take no German manpower**, by Oscar's decision (they
  were raised from Soviet prisoners of war and volunteers). Nothing changed;
  see section 18.
- **New:** the event for a beaten-back invasion (section 26).

**Testing notes:**
- **Setting a province's controller doesn't hold** when the enemy has
  divisions there. `set_province_controller` on a province with Soviet
  divisions was undone before the next day's check.
- **The order of on_action files:** files in `common/on_actions` run in
  case-sensitive name order, so capital letters come first. A test file
  named `aa_...` ran after `GER_...`; one named `AA_...` ran before it.

### 26. The invasion beaten back (commit `c0f1767`)

Oscar asked for a flavour event, with his picture, one day after D-Day is
pushed back.

- **The author's own D-Day logic** (`common/scripted_effects/war.txt`,
  `ALL_DDAY_FAILED`) sets a global flag whenever, after 25 June 1944, the
  Axis fully holds northern and southern France. It does not check that
  a landing happened. His D-Day news event (`mod.news.1`) is never fired:
  the line that fired it is commented out. So this event keeps its own
  record.
- **The landing:** from 1 June 1944, at war with the UK or the USA, the
  first day a western Allied enemy holds any of the 37 provinces in Normandy (state 15), Brittany (14),
  Nord-Pas-de-Calais (29) or Flanders (6). These are the four states the
  author's news event watches, and all four are German in the 1944 start.
- **Beaten back:** after a landing, the first day we hold all four again.
  The event follows **one day later**, as Oscar asked. It fires only once;
  the author's Overlord decision can bring the Allied AI back every 80
  days.
- **Effect:** none (flavour only, as asked).
- **The picture:** Oscar's (see above).

**Checked:**
- **Check Y** covers:
  - both triggers and the one-day delay;
  - that the author's news event watches the same four states;
  - that all four are German at the start;
  - the event with no effect, the picture, 3 texts.
- **Calibrated:** see VERIFICATION.
- **Earlier-session runtime** (the initial detection logic, with the 1 June date lowered for the test only):
  - all four states were ours on day one;
  - a test script gave the UK a Normandy province: the landing was noted;
  - taking it back the next day: "beaten back" was noted and the event
    scheduled for the day after.

**Console:** `event ger_dday.1`.

**Files (all new):** `GER_dday_on_actions.txt`, `GER_dday_events.txt`,
`GER_dday_l_english.yml`, `interface/GER_dday.gfx`,
`gfx/events/report_event_GER_dday_repelled.dds`.

### 27. Finish the D-Day content and remove Overlord decision blockers

**Partly reverted (29 September, evening):** the Overlord change below (`1296bb8`)
was reverted in `5ac05e9` at Oscar's request; the author's D-Day decisions
are unchanged. The rest stands. See section 28.

Commits `c0f1767` (picture and event), `1296bb8` (decision gates), and
`46c665a` (western Allied landing detection), continued with Codex.

- Preparation was available until May 1945 and applied its -1000 invasion
  preparation-speed modifier for 28 days without a cancellation condition.
  A late selection could overlap or outlast the 18-day launch bonus. It is
  now selectable only on 2–28 May 1944 and cancels from 29 May, when the
  launch decision is active, or on peace with Germany.
- The launch required both Britain and the USA to have less than 1%
  surrender progress. A small territorial loss could therefore block the
  scripted operation. Both must now be uncapitulated. All other launch
  conditions and all of the author's effects are preserved.
- The recovered event's original test counted any loss of German coastal
  control as a landing, including friendly transfers. It now checks all 37
  provinces in the four coast states and requires a western Allied enemy.
- The selected picture was recovered from the earlier session's finished
  DDS; its source image was not recreated or edited.

**Evidence and checks:** see [CODEX-CONTINUATION](CODEX-CONTINUATION.md).
The main verification has 80 passing checks, incorporating 29 Overlord and
52 D-Day scenario/calibration checks. The unmodified game's installed
`documentation/triggers_documentation.md` documents `has_capitulated`,
`has_decision`, `any_enemy_country`, `controls_province`, and
`is_fully_controlled_by`. The change is 12 added and three removed lines in
`common/decisions/Allies_1944.txt`, with its original line endings retained.

A fresh HOI4 startup logs 115 lines, identical to log 22 after wall-clock
normalization. Short live runs activated preparation but did not advance
far enough to observe cancellation or a landing. A full AI invasion is
**not yet verified**; these fixes remove identified script barriers, while
naval plans, troops and sea control still determine execution. The old
D-Day news popup remains disabled.

The ten newer mod commits and README were pushed to PR #4 with the user's
approval (head `23b6824`), in the author's layout.
[PR4-COMMIT-MAPPING.tsv](PR4-COMMIT-MAPPING.tsv) pairs the mod commits. Earlier runtime claims in sections 21–26 are recovered records.

### 28. Checked again after the handover (29 September 2026, evening)

Claude reached its usage limit during section 26, and Oscar continued with
Codex (sections 26–27, `CODEX-CONTINUATION.md`). Oscar then asked for all of
it to be checked again, and for the author's D-Day mechanics to be left
alone.

**Codex's commits, reviewed one by one:**

| Commit | What | Result |
|---|---|---|
| `c0f1767` | the invasion event, with the picture and its sprite | kept: byte-identical to the files Claude had prepared, plus the sprite file |
| `1296bb8` | changes to the author's Overlord decisions | **reverted** in `5ac05e9` |
| `46c665a` | the invasion event counts only a western Allied enemy, in any of the 37 provinces of the four states | kept: the list is exactly those states' provinces; tested in the game |
| `782a805`, `5d8e704` | documentation, checks | kept, except the Overlord check and Codex's game runner (removed in `2f73be4`) |

**Why the Overlord change was reverted** (`5ac05e9`):
- Oscar's decision: the author's D-Day mechanics are not to be touched.
- It wasn't shown to fix anything.
  - It replaced "Britain and the USA below 1% surrender progress" with
    "neither has capitulated". Measured in a German game on 1 January
    1944, both were at 0.
  - It limited the preparation decision to 2–28 May 1944. No game was seen
    where a late preparation blocked the landing.
- `common/decisions/Allies_1944.txt` is again the author's file, byte for
  byte. The new check OL guards this; calibrated: an edited date line
  makes it fail.
- The report that the Allies sometimes skip D-Day remains unexplained.

**Re-checked in the game** (HOI4 1.19.3, `-start_tag`; temporary test files
removed afterwards):
- **Every event of the update, fired at once** for an AI Germany (Hungary
  played): the 50 events of sections 5–26. After 4 days, error.log was
  compared with a control run on the same setup without them.
  - The only new lines came from the KONR expansion (section 16). Its
    event was fired directly, without the author's "Recruit Andrey Vlasov"
    and its "Russische Befreiungsarmee" template. The decision that fires
    it in play requires that template.
  - Repeated with the author's template created first: the 4th KONR
    division was raised (302 → 303 divisions), with no errors.
- **Triggers in a running game** (the invasion event's 1 June date lowered
  for the test only):
  - a US-held east bank at Remagen fired the event and named the captor
    ("American");
  - holding the city fired the Leningrad event;
  - one bomb fired the bomb event;
  - the Crimea popup came on day one; the AI chose "Evacuate", and the
    decision was running the next day;
  - a British-held Normandy province noted the landing, and taking it back
    noted the invasion as beaten back the next day.
- **The pictures:** six events with our pictures were shown to a German
  player, with no picture or sprite errors.
- **The UK start** (section 15): still no crash.
- **Load test:** error.log identical (115 lines, `game-logs/26-after-overlord-revert_error.log`).
- **Checks:** 79, all pass (the Overlord check OL now guards the author's file).

### 29. SS divisions in the 1944 start had the wrong names (commit `bb94b9e`)

Oscar started a German game and, without moving anything, found
"11. SS-Division 'Nordland'" in Berlin and "5. SS-Division 'Wiking'" at
Seelow. Our Wiking and Nordland (section 10) should be at Cherkassy and on
the Leningrad front.

**The cause:**
- Germany's 1944 history (`history/countries/GER - Germany.txt`, the
  1943.12.30 block) completes two of the author's focuses, "Expand SS
  Recruitment" and "Strengthen the Waffen-SS".
- Their rewards create 11 SS divisions in Brandenburg: 6 "Waffen-SS
  Division", 3 "SS-Verfügungstruppe" and 2 "Waffen-SS Panzer Division".
  Their names come from the SS name list.
- The game loads the 1944 order of battle only after all the history has
  run. So those 11 took the numbers 1–11 first.
- The SS divisions of the order of battle ask for their own numbers
  (Leibstandarte 1, Das Reich 2 and so on). Those numbers were taken, so
  they got the next free numbers that have a name in the list.
- This comes from the author's setup, not from a recent change: the
  numbers 1, 2, 3, 11 and 12 were affected as well. Section 10 added the
  list entry "5 = Wiking", which is why the number-5 division at Seelow was
  called Wiking. The author's version itself was not run.

**Read from a save of a German game** (`game-logs/28-ss-division-names-before.txt`
and `-after.txt`):

| The order of battle's division | Where | Before (shown in the game) | Now |
|---|---|---|---|
| 1. Leibstandarte Adolf Hitler | Cherkassy | 12. 'Hitlerjugend' | 1. 'Leibstandarte Adolf Hitler' |
| 2. Das Reich | Limousin | 14. (ukrain. Nr. 1) | 2. 'Das Reich' |
| 3. Totenkopf | Kherson | 16. 'Reichsführer-SS' | 3. 'Totenkopf' |
| 5. Wiking (section 10) | Cherkassy | 18. 'Horst Wessel' | 5. 'Wiking' |
| 11. Nordland (section 10) | Leningrad front (Pskov) | 21. 'Skanderbeg' | 11. 'Nordland' |
| 12. Hitlerjugend | Antwerp | 13. 'Handschar' | 12. 'Hitlerjugend' |
| 17. Götz von Berlichingen | Champagne | 17. (correct) | 17. 'Götz von Berlichingen' |

**The fix** (`bb94b9e`):
- The two history lines are commented out, each with a note.
- The new file `common/on_actions/GER_ss_names_on_actions.txt` completes
  the same two focuses when the game starts (`on_startup`). That comes
  after the order of battle is loaded.
- Only for starts from 1943.12.30, the date of the history block they came
  from; games that start in 1936 or 1939 are not affected.
- In the same order, and only if not completed already.

**Tried first, did not work:** moving the two lines below `set_oob` in the
history file. A save showed exactly the same numbers: the order of battle
is loaded after the history, wherever the line is.

**What stays the same:**
- The 11 divisions are still created in Brandenburg, with the same
  templates. They now take the free numbers (9, 10, 13, 14, 16, 18, 21, 22,
  24, 25, 26), so they still get names from the list, for example
  "9. SS-Division 'Hohenstaufen'".
- The author's four SS-Regiments have no number of their own. They now get
  4, 6, 7 and 8 instead of 22, 24, 25 and 26.

**Checked:**
- **In the game** (HOI4 1.19.3, a German game via `-start_tag`):
  - plain-text saves of the version before (`e09019a`) and after,
    read with the new `tools/list_ss_divisions.py`;
  - to get a save quickly, the test copy's 1944 bookmark was moved to 31
    January 1944 (test copy only), so the monthly autosave came after one
    day. No history is dated between 1 and 31 January 1944, so the start
    is the same.
- **Result:**
  - all seven SS divisions of the order of battle have their own numbers
    and names (the table above);
  - still 22 SS divisions and 302 German divisions, in the same states,
    with the same templates;
  - the same 101 completed focuses and 17 ideas (Himmler as
    Reichsführer-SS), political power (1826.78), experience, stability and
    war support;
  - the same doctrine discounts: Strengthen the Waffen-SS, 50% for 2 uses.
- **error.log of the two runs:** the same lines. The only difference is
  how often the game's own "AI tried to post an invalid command:
  unlock_trait_command" line appears (605 and 621 times); it also appears
  in Oscar's own play logs.
- **Load test:** error.log identical to log 26 (115 lines,
  `game-logs/28-after-ss-names_error.log`).
- **Check Z** (new):
  - the two history lines are only commented, and the history file is
    otherwise byte-identical to `e09019a`;
  - the new file's structure and date;
  - nothing else completes the two focuses.
  - Calibrated: five planted errors, and each made it fail (a history line
    active again, another history line changed, the start date moved, the
    comparison flipped, the wrong focus).
- **Checks:** 80, all pass.

**To see it:** start a German game. Cherkassy has 1. 'Leibstandarte Adolf
Hitler' and 5. 'Wiking', the Leningrad front 11. 'Nordland'. Berlin and
Seelow have other SS numbers.

## How to test in game

A local copy of the fixed mod is registered as a separate mod,
**"1944 - Downfall (local fixes)"** (file
`Documents\Paradox Interactive\Hearts of Iron IV\mod\downfall_local_fixes.mod`).

- **It points at its own copy:** `Documents\...\Hearts of Iron IV\mod\1944-Downfall-local`,
  refreshed from this project's `mod\` folder.
- **That copy's `descriptor.mod` has its own name and no `remote_file_id`.**
  The Paradox launcher rewrites every `.mod` file from the `descriptor.mod`
  inside the mod's folder. A local copy that keeps the author's
  `remote_file_id="3070639276"` becomes a second "1944 - Downfall" with the
  Workshop item's ID, and the game then loads neither.
- **Found on 30 September 2026:** the Workshop version stopped loading on
  Oscar's PC ("Active Mod Count: 0" in `logs\system.log`) for exactly this
  reason. Steam players were not affected.

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

113 files differ from the July 2026 Steam version: 33 edited, 3 deleted, 77 new (full list:
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
