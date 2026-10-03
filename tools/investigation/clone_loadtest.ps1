param([string]$Clone, [string]$Out)
# Load test of a fresh clone of the pull-request branch: mirror it into the local test copy (keeping the copy's own
# descriptor, without .git), run loadtest_mod.ps1, then mirror the package's mod/ back into the copy.
$S = $PSScriptRoot
$L = "C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV\mod\1944-Downfall-local"
$P = "C:\Users\Ander\Desktop\Projects\1944-Downfall\mod"
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { "HOI4 is running - not starting"; exit 1 }
$desc = [IO.File]::ReadAllText("$L\descriptor.mod")
try {
  robocopy $Clone $L /MIR /XD .git /NFL /NDL /NJH /NJS /NP | Out-Null
  [IO.File]::WriteAllText("$L\descriptor.mod", $desc, (New-Object Text.UTF8Encoding $false))
  "copy = clone: " + ((Get-ChildItem $L -Recurse -File).Count) + " files"
  & powershell -ExecutionPolicy Bypass -File "$S\loadtest_mod.ps1" -Out $Out
} finally {
  robocopy $P $L /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
  [IO.File]::WriteAllText("$L\descriptor.mod", $desc, (New-Object Text.UTF8Encoding $false))
  "copy restored from the package: " + ((Get-ChildItem $L -Recurse -File).Count) + " files; descriptor name: " + ((Select-String -Path "$L\descriptor.mod" -Pattern '^name=').Line)
}
