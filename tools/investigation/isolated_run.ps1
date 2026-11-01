param([string]$Name, [string]$Tag = "SWI", [int]$MaxMinutes = 45,
      [string]$Source = "C:\Users\Ander\Desktop\Projects\1944-Downfall\mod",
      [string[]]$TestFiles = @(), [string]$Bookmark = "", [switch]$DebugMode, [switch]$StopAtAutosave, [switch]$NoMod)
# One observed game that neither reads nor writes Documents\Paradox Interactive (not the playset, the settings or the saves).
# The game takes its user folder from gameDataPath in launcher-settings.json, in the folder of the exe. So it is run from a game
# root of its own, tools\investigation\out\gameroot: a copy of the exe and the small files next to it, a launcher-settings.json
# with gameDataPath = tools\investigation\out\userdir, and junctions to the real game's folders (nothing in Program Files changes).
# NEVER delete out\gameroot with a recursive delete: the junctions point at the real game. Use: cmd /c rmdir <each junction>.
# Copies $Source to the user folder's test mod (its own descriptor), drops temporary on_actions files in, plays as $Tag at speed 5,
# and saves game.log, error.log, system.log and any new crash folder under out\run_$Name.
$doc = "C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV"
$game = "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
$Root = "$PSScriptRoot\out\gameroot"
$U = "$PSScriptRoot\out\userdir"
$L = "$U\mod\1944-Downfall-test"
$out = "$PSScriptRoot\out\run_$Name"
$noBom = New-Object Text.UTF8Encoding $false
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { "HOI4 is running - not starting"; exit 1 }
New-Item -ItemType Directory -Force $Root, "$U\mod", "$U\save games", "$U\crashes", $out | Out-Null

# the game root: refreshed every run, so it follows game updates
foreach ($d in Get-ChildItem $game -Directory) {
  if (-not (Test-Path "$Root\$($d.Name)")) { cmd /c mklink /J "$Root\$($d.Name)" "$($d.FullName)" | Out-Null }
}
foreach ($f in Get-ChildItem $game -File) {
  if ($f.Name -in "libcef.so", "launcher-installer-windows_2024.14.exe", "dowser.exe") { continue }
  if (-not (Test-Path "$Root\$($f.Name)") -or (Get-Item "$Root\$($f.Name)").LastWriteTime -ne $f.LastWriteTime -or (Get-Item "$Root\$($f.Name)").Length -ne $f.Length) { Copy-Item $f.FullName "$Root\$($f.Name)" -Force }
}
$ls = [IO.File]::ReadAllText("$game\launcher-settings.json")
$anchor = '"gameDataPath": "%USER_DOCUMENTS%/Paradox Interactive/Hearts of Iron IV"'
if (-not $ls.Contains($anchor)) { "gameDataPath anchor not found in launcher-settings.json"; exit 1 }
[IO.File]::WriteAllText("$Root\launcher-settings.json", $ls.Replace($anchor, '"gameDataPath": "' + $U.Replace("\", "/") + '"'), $noBom)

# the user folder
robocopy $Source $L /MIR /XD .git /R:2 /W:2 /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { "robocopy failed with exit code ${LASTEXITCODE}, not starting"; exit 1 }
$desc = "version=`"1`"`r`nname=`"1944 - Downfall (test)`"`r`npicture=`"thumbnail.png`"`r`nsupported_version=`"1.19.*`"`r`n"
[IO.File]::WriteAllText("$L\descriptor.mod", $desc, $noBom)
[IO.File]::WriteAllText("$U\mod\downfall_test.mod", $desc + "path=`"" + $L.Replace("\", "/") + "`"`r`n", $noBom)
$modList = if ($NoMod) { '[]' } else { '["mod/downfall_test.mod"]' }   # -NoMod: the base game alone, for comparison
[IO.File]::WriteAllText("$U\dlc_load.json", '{"enabled_mods":' + $modList + ',"disabled_dlcs":[]}', $noBom)
$cfg = [IO.File]::ReadAllText("$doc\settings.txt")   # read only: the display settings of the real game
$cfg = $cfg.Replace("save_as_binary=yes", "save_as_binary=no")
$cfg = [regex]::Replace($cfg, 'autosave="[A-Z]+"', 'autosave="MONTHLY"')
[IO.File]::WriteAllText("$U\settings.txt", $cfg, $noBom)
foreach ($tf in $TestFiles) { Copy-Item $tf "$L\common\on_actions\$(Split-Path $tf -Leaf)" -Force }
if ($Bookmark) {
  $bmPath = "$L\common\bookmarks\1944.txt"
  $bmText = [IO.File]::ReadAllText($bmPath)
  if (-not $bmText.Contains("date = 1944.1.1.12")) { "bookmark anchor not found"; exit 1 }
  [IO.File]::WriteAllText($bmPath, $bmText.Replace("date = 1944.1.1.12", "date = $Bookmark"), $noBom)
}
$crashesBefore = @(Get-ChildItem "$U\crashes" -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Name })
$t0 = Get-Date
$argList = @("-nofilewatcher", "-start_tag=$Tag", "-start_speed=5"); if ($DebugMode) { $argList = @("-debug") + $argList }
$proc = Start-Process -FilePath "$Root\hoi4.exe" -ArgumentList $argList -WorkingDirectory $Root -PassThru
$outcome = "stopped after $MaxMinutes minutes, still running"
try {
  while (((Get-Date) - $t0).TotalMinutes -lt $MaxMinutes) {
    Start-Sleep -Seconds 10
    if ($proc.HasExited) { $outcome = "the game exited by itself after $([int]((Get-Date)-$t0).TotalSeconds) s, exit code $($proc.ExitCode)"; break }
    if ($StopAtAutosave) {
      $new = Get-ChildItem "$U\save games" -File -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $t0 -and $_.Name -notlike "*_temp*" } | Select-Object -First 1
      if ($new) { Start-Sleep -Seconds 20; Copy-Item $new.FullName "$out\save.hoi4" -Force; $outcome = "stopped at the first autosave: $($new.Name)"; break }
    }
  }
} finally {
  if ($proc -and -not $proc.HasExited) { Stop-Process -Id $proc.Id -Force }
  for ($j = 0; $j -lt 30 -and (Get-Process -Name hoi4 -ErrorAction SilentlyContinue); $j++) { Start-Sleep -Seconds 1 }
  Start-Sleep -Seconds 2
  foreach ($lg in "error.log", "game.log", "system.log") { if (Test-Path "$U\logs\$lg") { Copy-Item "$U\logs\$lg" "$out\$lg" -Force } }
  $newCrash = @(Get-ChildItem "$U\crashes" -Directory -ErrorAction SilentlyContinue | Where-Object { $crashesBefore -notcontains $_.Name })
  foreach ($c in $newCrash) { Copy-Item $c.FullName "$out\$($c.Name)" -Recurse -Force }
  "outcome: $outcome"
  "user folder used: " + (Test-Path "$U\logs\game.log") + "; source: $Source"
  "new crash folders: " + (($newCrash | ForEach-Object { $_.Name }) -join ", ")
  $lastSave = Get-ChildItem "$U\save games" -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -notlike "*_temp*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($lastSave -and -not (Test-Path "$out\save.hoi4")) { Copy-Item $lastSave.FullName "$out\save.hoi4" -Force }
  Remove-Item "$U\save games\*" -Force -ErrorAction SilentlyContinue
}
