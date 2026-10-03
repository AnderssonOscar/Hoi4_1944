param([string]$Name = "before", [string]$Tag = "GER", [int]$MaxMinutes = 12, [string]$Source = "C:\Users\Ander\Desktop\Projects\1944-Downfall\mod")
# Fast plain-text save of the game's start position, for reading division names.
# 1. Refreshes the LOCAL COPY from the package (robocopy /MIR, keeps the copy's own descriptor).
# 2. In the copy only, moves the 1944 bookmark to 31 Jan 1944 (no history is dated between 1 and 31 Jan 1944,
#    so the start position is the same), so the first MONTHLY autosave (1 Feb) comes after one game day.
# 3. Starts the game as $Tag at speed 5 with plain-text monthly autosaves, copies the first autosave, closes the game.
# Always restores: dlc_load.json, settings.txt, Oscar's autosave.hoi4, the copy's bookmark; removes save files it made.
$doc = "C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV"
$game = "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
$S = "$PSScriptRoot\out"; New-Item -ItemType Directory -Force $S | Out-Null
$ModSrc = $Source
$L = "$doc\mod\1944-Downfall-local"
$bk = "$S\savetest-backup"
$sg = "$doc\save games"
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { "HOI4 is running - not starting"; exit 1 }
New-Item -ItemType Directory -Force $bk | Out-Null
Copy-Item "$doc\dlc_load.json" "$bk\dlc_load.json" -Force
Copy-Item "$doc\settings.txt" "$bk\settings.txt" -Force
$before = @(Get-ChildItem $sg -File | ForEach-Object { $_.Name })
$hadAutosave = Test-Path "$sg\autosave.hoi4"
if ($hadAutosave) { Copy-Item "$sg\autosave.hoi4" "$bk\autosave.hoi4" -Force }
$desc = [IO.File]::ReadAllText("$L\descriptor.mod")
robocopy $ModSrc $L /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
[IO.File]::WriteAllText("$L\descriptor.mod", $desc, (New-Object Text.UTF8Encoding $false))
$bmPath = "$L\common\bookmarks\1944.txt"
$bm = [IO.File]::ReadAllBytes($bmPath)
$bmText = [Text.Encoding]::UTF8.GetString($bm)
if (-not $bmText.Contains("date = 1944.1.1.12")) { "bookmark anchor not found"; exit 1 }
[IO.File]::WriteAllText($bmPath, $bmText.Replace("date = 1944.1.1.12", "date = 1944.1.31.12"), (New-Object Text.UTF8Encoding $false))
$p = $null
try {
  Set-Content -Path "$doc\dlc_load.json" -Value '{"enabled_mods":["mod/downfall_local_fixes.mod"],"disabled_dlcs":[]}' -Encoding ascii -NoNewline
  $cfg = [IO.File]::ReadAllText("$doc\settings.txt")
  $cfg = $cfg.Replace("save_as_binary=yes", "save_as_binary=no")
  $cfg = [regex]::Replace($cfg, 'autosave="[A-Z]+"', 'autosave="MONTHLY"')
  [IO.File]::WriteAllText("$doc\settings.txt", $cfg, (New-Object Text.UTF8Encoding $false))
  $t0 = Get-Date
  $p = Start-Process -FilePath "$game\hoi4.exe" -ArgumentList @("-nofilewatcher", "-start_tag=$Tag", "-start_speed=5") -WorkingDirectory $game -PassThru
  $found = $null
  while (((Get-Date) - $t0).TotalMinutes -lt $MaxMinutes) {
    Start-Sleep -Seconds 5
    $new = Get-ChildItem $sg -File -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -gt $t0 -and $_.Name -notlike "*_temp*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($new) {
      $len = -1
      for ($k = 0; $k -lt 30; $k++) { Start-Sleep -Seconds 3; $n2 = (Get-Item $new.FullName).Length; if ($n2 -eq $len) { break }; $len = $n2 }
      $found = $new; break
    }
    if ($p.HasExited) { "game exited before any autosave"; break }
  }
  if ($found) {
    Copy-Item $found.FullName "$S\save_$Name.hoi4" -Force
    "autosave after $([int]((Get-Date)-$t0).TotalSeconds) s: $($found.Name) -> save_$Name.hoi4 ($((Get-Item "$S\save_$Name.hoi4").Length) bytes), header: " + [Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes("$S\save_$Name.hoi4")[0..9])
  } else { "no autosave within $MaxMinutes minutes" }
  New-Item -ItemType Directory -Force "$S\run_$Name" | Out-Null
  foreach ($lg in "error.log", "game.log") { Copy-Item "$doc\logs\$lg" "$S\run_$Name\$lg" -Force }
  "logs copied to run_$Name (error.log " + (Get-Content "$S\run_$Name\error.log").Count + " lines), source: $ModSrc"
} finally {
  if ($p -and -not $p.HasExited) { Stop-Process -Id $p.Id -Force }
  for ($j = 0; $j -lt 30 -and (Get-Process -Name hoi4 -ErrorAction SilentlyContinue); $j++) { Start-Sleep -Seconds 1 }
  Copy-Item "$bk\dlc_load.json" "$doc\dlc_load.json" -Force
  Copy-Item "$bk\settings.txt" "$doc\settings.txt" -Force
  if ($hadAutosave) { Copy-Item "$bk\autosave.hoi4" "$sg\autosave.hoi4" -Force }
  foreach ($f in Get-ChildItem $sg -File) { if ($before -notcontains $f.Name) { "removing test save: $($f.Name)"; Remove-Item -LiteralPath $f.FullName } }
  [IO.File]::WriteAllBytes($bmPath, $bm)
  "restored: dlc_load.json = " + (Get-Content "$doc\dlc_load.json" -Raw)
  "restored: settings " + ((Select-String -Path "$doc\settings.txt" -Pattern 'save_as_binary=\w+|autosave="\w+"').Matches.Value -join ", ")
  "restored: autosave.hoi4 " + (Get-Item "$sg\autosave.hoi4").LastWriteTime + " " + (Get-Item "$sg\autosave.hoi4").Length
  "restored: bookmark " + ((Select-String -Path $bmPath -Pattern "date = [\d.]+").Matches[0].Value)
}
