<#
  File:    fix-reflector-init.ps1
  Purpose: Create __init__.py in symbiont_core/reflector to make it a proper Python package
#>

param (
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$ReflectorFolder = "symbiont_core\reflector",
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

#--- helper: create file if missing
function New-FileIfMissing {
    param ([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType File -Path $Path | Out-Null
        Write-Host "Created file: $Path"
        return "Created file: $Path"
    }
    return $null
}

#--- log changes
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Fixing Reflector Folder..."

# 1. Ensure reflector folder exists
$reflectorPath = Join-Path $ProjectRoot $ReflectorFolder
New-DirIfMissing -Path $reflectorPath | Out-Null

# 2. Ensure __init__.py exists
$initFilePath = Join-Path $reflectorPath "__init__.py"
$changes = @()

$initChange = New-FileIfMissing -Path $initFilePath
if ($initChange) { $changes += $initChange }

# 3. Log if anything changed
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Reflector folder fixed. __init__.py created. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
