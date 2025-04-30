<#
  File:    grow-mainlauncher.ps1
  Purpose: Update Symbiont main.py to launch CLI interface cleanly.
           - Add launcher code
           - Log all changes
#>

param (
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$UpdatesFolder = "updates",
    [string]$Changelog = "logs\changes.log"
)

#--- helper: make directory if missing
function New-DirIfMissing {
    param ([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created folder: $Path"
        return "Created folder: $Path"
    }
    return $null
}

#--- helper: overwrite main.py
function Overwrite-MainLauncher {
    $path = Join-Path $ProjectRoot "main.py"
    $code = @"
from symbiont_core.symbiont import Symbiont
from symbiont_core.interfaces.cli_interface import launch_cli

if __name__ == '__main__':
    print("Booting Symbiont...")
    s = Symbiont()
    print(s.heartbeat())

    print("\\nLaunching CLI...")
    launch_cli()
"@
    Set-Content -Encoding UTF8 -Path $path -Value $code
    Write-Host "Overwritten: main.py (now launches CLI)"
    return "Updated main.py to launch CLI"
}

#--- helper: log growth
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Growing Symbiont Main Launcher..."

# 1. Make sure updates folder exists
$updatesPath = Join-Path $ProjectRoot $UpdatesFolder
$updatesChange = New-DirIfMissing -Path $updatesPath

# 2. Make sure logs folder exists
$logsPath = Join-Path $ProjectRoot "logs"
$logsChange = New-DirIfMissing -Path $logsPath

# 3. Update main.py
$changes = @()

if ($updatesChange) { $changes += $updatesChange }
if ($logsChange) { $changes += $logsChange }

$mainResult = Overwrite-MainLauncher
if ($mainResult) { $changes += $mainResult }

# 4. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Main launcher updated. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
