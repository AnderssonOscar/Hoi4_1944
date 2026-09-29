# Continuation from the interrupted Claude session

**Update, 29 September 2026 (evening):** checked again by Claude at Oscar's
request (CHANGELOG section 28). The Overlord change below was reverted
(`5ac05e9`), and `tools/check_overlord.py` and `tools/run_game_check.ps1`
were removed (`2f73be4`). Everything else here stands.

Recovered on 29 September 2026 from the Desktop project and the matching
local Claude session. The original checkout was left intact. This working
copy includes its seven newer mod commits and its uncommitted D-Day files.

## Completed here

- Installed the already prepared D-Day picture and its missing sprite.
- Finished the D-Day repelled event. It records a landing only when a
  western Allied enemy holds a province in Normandy, Brittany, Pas-de-Calais
  or Flanders. A friendly transfer or Soviet occupation cannot count.
- Restricted Overlord preparation to 2–28 May 1944. It cancels from 29 May,
  when Overlord is already active, or when the country is no longer at war
  with Germany. The previous preparation decision could be selected until
  May 1945 and could overlap the 18-day launch bonus.
- Replaced the launch decision's less-than-1% surrender-progress tests for
  Britain and the USA with checks that neither has capitulated. The existing
  AI-only rule, war requirements, Normandy/Paris control, launch window,
  rest-day gate, costs, bonuses and repeat interval remain as written.
- Recovered the draft documentation for Wiking, the first German bomb,
  Leningrad, the Crimea and the invasion event.

The author's original D-Day news popup remains disabled. The Allied naval
AI remains responsible for executing invasions; this update does not create
a guaranteed landing or guarantee victory.

## Verification

- `python tools/verify_update.py`: 80 checks, including byte-exact cloning,
  file scope, original-content preservation, pictures, localisation and
  all the earlier features.
- `python tools/check_overlord.py`: 25 gate scenarios plus four planted
  defects, all passing. Restoring either old surrender-progress gate,
  allowing late preparation or delaying cancellation makes the checks fail.
- `python tools/check_dday.py`: 49 event scenarios plus three planted
  defects, all passing. Includes each of the 37 coastal provinces, friendly
  transfers, Soviet occupation, a non-enemy USA, the one-day delay and
  once-only behavior.
- HOI4 1.19.3 startup: 115 error-log lines, identical to the previous saved
  baseline after stripping wall-clock timestamps. The final log is saved
  as `docs/game-logs/25-after-dday-and-play-test-fixes_error.log`.
- A shortened test campaign starting on 27 May activated preparation, but
  the timed run only reached the first day. It did **not** establish live
  cancellation or an AI landing. A complete campaign comparison is still
  needed. Older runtime results in sections 21–26 of the changelog were
  recovered from Claude's draft and are identified as earlier work.

The game tests used a temporary mod descriptor. The launcher playset was
restored byte for byte and the previous logs were backed up.

## GitHub handoff

PR #4 was updated from `d4e1359` to `23b6824` with the user's approval.
It contains the ten newer mod commits and the revised README in the author's
repository layout. `docs/PR4-COMMIT-MAPPING.tsv` pairs the mod commits.
The package tag is `final-2026-09-29-v16-codex`. The author decides when to merge.
The author's Steam Workshop files have not been changed.

## Repeat the relevant game test

With this mod alone enabled, observe an AI Britain and USA through late
May and June 1944. Check that `operation_overlord_prep` has ended by the
launch window and that `operation_overlord` can run after small Allied
territorial losses. Watch the actual naval plans and sea control if no
invasion occurs. Compare the same starting save with the previous version.

For the flavour event, after 1 June give a coastal province such as 6449
to a western Allied enemy, wait for the daily check, return all four coast
states to Germany, then wait through the following day. Occupation changes
made by the console can be undone by divisions already in that province.
