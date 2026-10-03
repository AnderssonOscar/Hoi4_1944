param([string]$Name, [string]$Tag = "SWI", [int]$MaxMinutes = 45,
      [string]$Source = "C:\Users\Ander\Desktop\Projects\1944-Downfall\mod",
      [string[]]$TestFiles = @(), [string]$Bookmark = "", [switch]$DebugMode)
# One observed game from the real 1944 start (or -Bookmark date) until the first MONTHLY plain-text autosave.
# Mirrors $Source into the LOCAL TEST COPY (own descriptor kept), drops temporary on_actions files into the copy,
# plays as $Tag at speed 5, then saves game.log / error.log / the autosave under run_$Name.
# Always restores: dlc_load.json, settings.txt, Oscar's autosave.hoi4, and the copy (mirrored back from the package).
$doc = "C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV"
$game = "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
$Scr = "$PSScriptRoot\out"
$Pkg = "C:\Users\Ander\Desktop\Projects\1944-Downfall\mod"
$L = "$doc\mod\1944-Downfall-local"
$bk = "$Scr\politics-backup"
$sg = "$doc\save games"
$out = "$Scr\run_$Name"
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { "HOI4 is running - not starting"; exit 1 }
New-Item -ItemType Directory -Force $bk | Out-Null
New-Item -ItemType Directory -Force $out | Out-Null
Copy-Item "$doc\dlc_load.json" "$bk\dlc_load.json" -Force
Copy-Item "$doc\settings.txt" "$bk\settings.txt" -Force
$before = @(Get-ChildItem $sg -File | ForEach-Object { $_.Name })
$hadAutosave = Test-Path "$sg\autosave.hoi4"
if ($hadAutosave) { Copy-Item "$sg\autosave.hoi4" "$bk\autosave.hoi4" -Force }
$desc = [IO.File]::ReadAllText("$L\descriptor.mod")
$proc = $null
try {
  robocopy $Source $L /MIR /XD .git /NFL /NDL /NJH /NJS /NP | Out-Null
  [IO.File]::WriteAllText("$L\descriptor.mod", $desc, (New-Object Text.UTF8Encoding $false))
  foreach ($tf in $TestFiles) { Copy-Item $tf "$L\common\on_actions\$(Split-Path $tf -Leaf)" -Force }
  if ($Bookmark) {
    $bmPath = "$L\common\bookmarks\1944.txt"
    $bmText = [IO.File]::ReadAllText($bmPath)
    if (-not $bmText.Contains("date = 1944.1.1.12")) { throw "bookmark anchor not found" }
    [IO.File]::WriteAllText($bmPath, $bmText.Replace("date = 1944.1.1.12", "date = $Bookmark"), (New-Object Text.UTF8Encoding $false))
  }
  Set-Content -Path "$doc\dlc_load.json" -Value '{"enabled_mods":["mod/downfall_local_fixes.mod"],"disabled_dlcs":[]}' -Encoding ascii -NoNewline
  $cfg = [IO.File]::ReadAllText("$doc\settings.txt")
  $cfg = $cfg.Replace("save_as_binary=yes", "save_as_binary=no")
  $cfg = [regex]::Replace($cfg, 'autosave="[A-Z]+"', 'autosave="MONTHLY"')
  [IO.File]::WriteAllText("$doc\settings.txt", $cfg, (New-Object Text.UTF8Encoding $false))
  $t0 = Get-Date
  $argList = @("-nofilewatcher", "-start_tag=$Tag", "-start_speed=5"); if ($DebugMode) { $argList = @("-debug") + $argList }
  $proc = Start-Process -FilePath "$game\hoi4.exe" -ArgumentList $argList -WorkingDirectory $game -PassThru
  $found = $null
  while (((Get-Date) - $t0).TotalMinutes -lt $MaxMinutes) {
    Start-Sleep -Seconds 10
    $new = Get-ChildItem $sg -File -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $t0 -and $_.Name -notlike "*_temp*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($new) {
      $len = -1
      for ($k = 0; $k -lt 30; $k++) { Start-Sleep -Seconds 3; $n2 = (Get-Item $new.FullName).Length; if ($n2 -eq $len) { break }; $len = $n2 }
      $found = $new; break
    }
    if ($proc.HasExited) { "game exited before any autosave (crash?)"; break }
  }
  if ($found) {
    Copy-Item $found.FullName "$out\save.hoi4" -Force
    "autosave after $([int]((Get-Date)-$t0).TotalMinutes) min: $($found.Name) -> run_$Name\save.hoi4 ($((Get-Item "$out\save.hoi4").Length) bytes)"
  } else { "no autosave within $MaxMinutes minutes" }
  foreach ($lg in "error.log", "game.log") { Copy-Item "$doc\logs\$lg" "$out\$lg" -Force }
  "logs copied to run_$Name; PL lines in game.log: " + @(Select-String -Path "$out\game.log" -Pattern "PL ").Count + "; source: $Source"
} finally {
  if ($proc -and -not $proc.HasExited) { Stop-Process -Id $proc.Id -Force }
  for ($j = 0; $j -lt 30 -and (Get-Process -Name hoi4 -ErrorAction SilentlyContinue); $j++) { Start-Sleep -Seconds 1 }
  Copy-Item "$bk\dlc_load.json" "$doc\dlc_load.json" -Force
  Copy-Item "$bk\settings.txt" "$doc\settings.txt" -Force
  if ($hadAutosave) { Copy-Item "$bk\autosave.hoi4" "$sg\autosave.hoi4" -Force }
  foreach ($f in Get-ChildItem $sg -File) { if ($before -notcontains $f.Name) { "removing test save: $($f.Name)"; Remove-Item -LiteralPath $f.FullName } }
  robocopy $Pkg $L /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
  [IO.File]::WriteAllText("$L\descriptor.mod", $desc, (New-Object Text.UTF8Encoding $false))
  "restored: playset " + (Get-Content "$doc\dlc_load.json" -Raw)
  "restored: settings " + ((Select-String -Path "$doc\settings.txt" -Pattern 'save_as_binary=\w+|autosave="\w+"').Matches.Value -join ", ")
  "restored: autosave.hoi4 " + (Get-Item "$sg\autosave.hoi4").LastWriteTime + " " + (Get-Item "$sg\autosave.hoi4").Length
  "restored: test copy mirrored from the package; test files left in it: " + @(Get-ChildItem "$L\common\on_actions" -Filter "*TEMP*").Count
}
