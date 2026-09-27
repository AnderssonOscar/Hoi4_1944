# 1944 - Downfall: bug-fix workspace

Working copy of the Steam Workshop mod *1944 - Downfall* (id 3070639276) for
investigating and fixing reported bugs.

| Folder | What it is |
|---|---|
| `mod/` | The mod. Commit `253cea1` is the Workshop version byte-for-byte. |
| `docs/INVESTIGATION.md` | What was looked at, what was found, how sure, what's proposed. |
| `tools/` | Read-only check scripts used for the findings. |

## Reviewing changes

Every change to the mod is a separate git commit that explains why.

```
git log --oneline -- mod/          # list of mod changes
git show <commit>                   # one change with its reason
git diff 253cea1 -- mod/            # everything changed vs. the Workshop version
```

No mod files have been changed yet.
