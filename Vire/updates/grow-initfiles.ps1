<#
  File:    grow-initfiles.ps1
  Purpose: Make sure Symbiont project has correct __init__.py files
           - symbiont_core/
           - symbiont_core/interfaces/
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

#--- helper: create __init__.py if missing
function Ensure-InitFile {
    param ([string]$FolderPath)
    $initPath = Join-Path $FolderPath "__init__.py"
    if (-not (Test-Path $initPath)) {
        "" | Out-File -Encoding utf8 -FilePath $initPath
        Write-Host "Created __init__.py in $FolderPath"
        return "Created __init__.py in $FolderPath"
    }
    return $null
}

#--- helper: log changes
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Growing Symbiont Init Files..."

# 1. Make sure updates/ and logs/ exist
$updatesPath = Join-Path $ProjectRoot $UpdatesFolder
New-DirIfMissing -Path $updatesPath | Out-Null

$logsPath = Join-Path $ProjectRoot "logs"
New-DirIfMissing -Path $logsPath | Out-Null

# 2. Add __init__.py files
$changes = @()

$symbiontCorePath = Join-Path $ProjectRoot "symbiont_core"
$interfacesPath   = Join-Path $symbiontCorePath "interfaces"

$change = Ensure-InitFile -FolderPath $symbiontCorePath
if ($change) { $changes += $change }

$change = Ensure-InitFile -FolderPath $interfacesPath
if ($change) { $changes += $change }

# 3. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Init files created. Changes logged."
}
else {
    Write-Host "`nNo new init files needed. Everything is ready."
}
