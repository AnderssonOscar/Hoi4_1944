param([string]$Out, [string]$ModFile = "downfall_local_fixes.mod")
# Starts HOI4 -debug with the local test mod, waits for the main menu (history executed), copies error.log to $Out.
$doc = "C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV"
$game = "C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { "HOI4 is running - not starting a test"; exit 0 }
$cur = Get-Content "$doc\dlc_load.json" -Raw
$p = $null
try {
  Set-Content -Path "$doc\dlc_load.json" -Value ('{"enabled_mods":["mod/' + $ModFile + '"],"disabled_dlcs":[]}') -Encoding ascii -NoNewline
  $t0 = Get-Date
  $p = Start-Process -FilePath "$game\hoi4.exe" -ArgumentList @("-debug", "-nofilewatcher") -WorkingDirectory $game -PassThru
  $found = $false
  for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 2
    if ($p.HasExited) { break }
    foreach ($f in @("game.log", "system.log", "setup.log")) {
      if ((Test-Path "$doc\logs\$f") -and (Select-String -Path "$doc\logs\$f" -Pattern "Executing History from 2.1.1.1" -SimpleMatch -Quiet)) { $found = $true }
    }
    if ($found) { break }
  }
  Start-Sleep -Seconds 15
  "marker found: $found after ~$([int]((Get-Date) - $t0).TotalSeconds)s; exited=$($p.HasExited)"
  Copy-Item "$doc\logs\error.log" $Out -Force
  "error.log lines: " + (Get-Content $Out).Count
} finally {
  if ($p -and -not $p.HasExited) { Stop-Process -Id $p.Id -Force }
  for ($j = 0; $j -lt 30 -and (Get-Process -Name hoi4 -ErrorAction SilentlyContinue); $j++) { Start-Sleep -Seconds 1 }
  Set-Content -Path "$doc\dlc_load.json" -Value $cur -Encoding ascii -NoNewline
  "dlc_load.json restored: " + (Get-Content "$doc\dlc_load.json")
}
