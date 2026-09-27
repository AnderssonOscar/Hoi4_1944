# 1944 - Downfall: bug-fix workspace

Working copy of the Steam Workshop mod *1944 - Downfall* (id 3070639276) for
investigating and fixing reported bugs.

| Folder | What it is |
|---|---|
| `mod/` | The mod. Commit `253cea1` is the Workshop version byte-for-byte. |
| `docs/HANDOVER.md` | Start here if you're continuing the work (any assistant). |
| `docs/INVESTIGATION.md` | What was looked at, what was found, how sure, what's proposed. |
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

Two fixes have been applied so far, not yet tested in game. See `docs/CHANGELOG.md`.
