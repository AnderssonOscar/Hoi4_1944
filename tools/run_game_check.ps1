param(
    [Parameter(Mandatory=$true)][string]$ModPath,
    [Parameter(Mandatory=$true)][string]$OutputPath,
    [string]$Tag = '',
    [int]$RunSeconds = 30
)
$ErrorActionPreference = 'Stop'
$doc = 'C:\Users\Ander\Documents\Paradox Interactive\Hearts of Iron IV'
$game = 'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV'
if (Get-Process -Name hoi4 -ErrorAction SilentlyContinue) { throw 'HOI4 is already running; close it before testing.' }
$modRoot = (Resolve-Path -LiteralPath $ModPath).Path
$outputRoot = [IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
$priorLogs = Join-Path $outputRoot 'prior-logs'
New-Item -ItemType Directory -Path $priorLogs -Force | Out-Null
Get-ChildItem -LiteralPath (Join-Path $doc 'logs') -File | Copy-Item -Destination $priorLogs
$loadPath = Join-Path $doc 'dlc_load.json'
$descriptorPath = Join-Path $doc 'mod\downfall_codex_verification.mod'
$savedLoad = [IO.File]::ReadAllBytes($loadPath)
$savedDescriptor = if (Test-Path -LiteralPath $descriptorPath) { [IO.File]::ReadAllBytes($descriptorPath) } else { $null }
[IO.File]::WriteAllBytes((Join-Path $outputRoot 'original-dlc_load.json'), $savedLoad)
$process = $null
$markerFound = $false
try {
    $descriptor = 'name="1944 - Downfall (Codex verification)"' + "`n" + 'supported_version="1.19.*"' + "`n" + 'path="' + $modRoot.Replace('\','/') + '"' + "`n"
    [IO.File]::WriteAllText($descriptorPath, $descriptor, [Text.UTF8Encoding]::new($false))
    $load = [Text.Encoding]::UTF8.GetString($savedLoad) | ConvertFrom-Json
    $load.enabled_mods = @('mod/downfall_codex_verification.mod')
    [IO.File]::WriteAllText($loadPath, ($load | ConvertTo-Json -Compress), [Text.UTF8Encoding]::new($false))
    $arguments = @('-debug', '-nofilewatcher')
    if ($Tag) { $arguments += @("-start_tag=$Tag", '-start_speed=5') }
    $started = Get-Date
    $process = Start-Process -FilePath (Join-Path $game 'hoi4.exe') -ArgumentList $arguments -WorkingDirectory $game -WindowStyle Hidden -PassThru
    $readyAt = $null
    while (((Get-Date) - $started).TotalSeconds -lt 180) {
        Start-Sleep -Seconds 2
        if ($process.HasExited) { throw "Test game exited unexpectedly: $($process.ExitCode)" }
        $logFile = Join-Path $doc 'logs\game.log'
        if (Test-Path -LiteralPath $logFile) {
            $fresh = (Get-Item -LiteralPath $logFile).LastWriteTime -ge $started
            $pattern = if ($Tag) { 'Launching SINGLEPLAYER' } else { 'Executing History from 2.1.1.1' }
            if (-not $readyAt -and $fresh -and (Select-String -LiteralPath $logFile -Pattern $pattern -SimpleMatch -Quiet)) {
                $readyAt = Get-Date
                $markerFound = $true
            }
            if ($readyAt -and ((Get-Date) - $readyAt).TotalSeconds -ge $RunSeconds) { break }
        }
    }
    if (-not $markerFound) { throw 'The expected game startup marker was not observed.' }
    foreach ($name in @('error.log', 'game.log', 'setup.log', 'system.log')) {
        $log = Join-Path $doc ('logs\' + $name)
        if (Test-Path -LiteralPath $log) { Copy-Item -LiteralPath $log -Destination (Join-Path $outputRoot $name) }
    }
    "Game startup verified. Error-log lines: $((Get-Content -LiteralPath (Join-Path $outputRoot 'error.log')).Count)"
} finally {
    if ($process -and -not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
        $process.WaitForExit(10000) | Out-Null
    }
    [IO.File]::WriteAllBytes($loadPath, $savedLoad)
    if ($null -ne $savedDescriptor) { [IO.File]::WriteAllBytes($descriptorPath, $savedDescriptor) }
    else { Remove-Item -LiteralPath $descriptorPath -ErrorAction SilentlyContinue }
    if (-not [Linq.Enumerable]::SequenceEqual([byte[]]$savedLoad, [byte[]][IO.File]::ReadAllBytes($loadPath))) {
        throw 'The launcher playset did not restore exactly.'
    }
    'Launcher playset restored byte for byte. Prior logs preserved in the test output folder.'
}
