# 1944 - Downfall: bug-fix workspace

Working copy of the Steam Workshop mod *1944 - Downfall* (id 3070639276) for
investigating and fixing reported bugs.

| Folder | What it is |
|---|---|
| `mod/` | The mod. Commit `253cea1` is the Workshop version byte-for-byte. |
| `docs/READ-ME-FIRST.md` | Start page for the mod author (also at the top of the zip). |
| `docs/HANDOVER.md` | Start here if you're continuing the work (any assistant). |
| `docs/INVESTIGATION.md` | What was looked at, what was found, how sure, what's proposed. |
| `docs/VERIFICATION.md` | Proof that the fixes and the 1.19.3 update are correct (46 checks). |
| `docs/CHANGELOG.md` | Every change made to the mod, and how to test it in game. |
| `docs/proposed-fixes/` | Patch files for proposed fixes. `0001` has been applied (commit `e20698c`). |
| `tools/` | Read-only check scripts used for the findings. |

## Reviewing changes

Every change to the mod is a separate git commit that explains why.

```
git log --oneline -- mod/          # list of mod changes
git show <commit>                   # one change with its reason
git diff 253cea1 -- mod/            # everything changed vs. the Workshop version
```

Final state (2026-09-27): two bug fixes, the update to HOI4 1.19.3 and one
flavor event (Slovak National Uprising), verified by 47 checks (`docs/VERIFICATION.md`), not yet play-tested. What was
sent to the author is described in `docs/READ-ME-FIRST.md`.
