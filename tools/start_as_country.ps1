param([string]$Tag = "ENG", [string]$ModFile = "downfall_local_fixes.mod", [string]$Speed = "", [int]$After = 25)
# Starts a new 1944 game directly as one country and reports whether the game crashed.
# Uses the game's own command-line options: -start_tag=TAG starts a single-player game as TAG,
# -start_speed=N unpauses at speed N, -nofilewatcher stops debug mode reloading files that change.
#
#   powershell -ExecutionPolicy Bypass -File tools\start_as_country.ps1 -Tag ENG
#   ... -Tag ENG -ModFile ugc_3070639276.mod   (the Steam Workshop version instead of the local copy)
#
# dlc_load.json (the launcher's playset) is backed up first and always restored.
# The game is closed $After seconds after the game has launched. Never runs while HOI4 is open.
$doc = "$env:USERPROFILE\Documents\Paradox Interactive\Hearts of Iron IV"
$game = "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { "HOI4 is running - not starting a test"; exit 0 }
$saved = Get-Content "$doc\dlc_load.json" -Raw
$crashesBefore = @(Get-ChildItem "$doc\crashes" -Directory -ErrorAction SilentlyContinue).Count
$p = $null
try {
  Set-Content -Path "$doc\dlc_load.json" -Value ('{"enabled_mods":["mod/' + $ModFile + '"],"disabled_dlcs":[]}') -Encoding ascii -NoNewline
  $arguments = @("-debug", "-nofilewatcher", "-start_tag=$Tag")
  if ($Speed) { $arguments += "-start_speed=$Speed" }
  $p = Start-Process -FilePath "$game\hoi4.exe" -ArgumentList $arguments -WorkingDirectory $game -PassThru
  $log = "$doc\logs\game.log"
  $launched = $null
  for ($i = 0; $i -lt 150; $i++) {
    Start-Sleep -Seconds 2
    if ($p.HasExited) { break }
    if (-not $launched -and (Test-Path $log) -and (Select-String -Path $log -Pattern "Launching SINGLEPLAYER" -Quiet)) { $launched = Get-Date }
    if ($launched -and ((Get-Date) - $launched).TotalSeconds -gt $After) { break }
  }
  $crashesAfter = @(Get-ChildItem "$doc\crashes" -Directory -ErrorAction SilentlyContinue).Count
  if (-not $launched) { "$Tag : the game never launched" }
  elseif ($p.HasExited) { "$Tag : CRASHED (new crash folders: $($crashesAfter - $crashesBefore)); last lines of game.log:"; Get-Content $log -Tail 3 }
  else { "$Tag : running $After s after launch, no crash" }
} finally {
  if ($p -and -not $p.HasExited) { Stop-Process -Id $p.Id -Force }
  for ($j = 0; $j -lt 30 -and (Get-Process -Name hoi4 -ErrorAction SilentlyContinue); $j++) { Start-Sleep -Seconds 1 }
  Set-Content -Path "$doc\dlc_load.json" -Value $saved -Encoding ascii -NoNewline
}
