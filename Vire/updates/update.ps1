<#
  File:    update.ps1
  Purpose: Evolve Symbiont project without overwriting work.
           - Fix bugs (like utf-8 encoding)
           - Add new folders or stubs
           - Log updates cleanly
#>

param (
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$Changelog = "logs\changes.log"
)

#--- helper: create folder if missing
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
    param ([string]$Path, [string]$Content = "")
    if (-not (Test-Path $Path)) {
        $Content | Out-File -FilePath $Path -Encoding UTF8
        Write-Host "Created file: $Path"
        return "Created file: $Path"
    }
    return $null
}

#--- fix symbiont encoding (utf-8-sig)
function Fix-SymbiontEncoding {
    $target = Join-Path $ProjectRoot "symbiont_core\symbiont.py"
    if (Test-Path $target) {
        (Get-Content $target -Raw) -replace "encoding='utf-8'", "encoding='utf-8-sig'" | Set-Content -Encoding UTF8 -Path $target
        Write-Host "Fixed encoding in symbiont.py (utf-8-sig)."
        return "Fixed encoding in symbiont.py"
    }
    else {
        Write-Host "symbiont.py not found. Skipping encoding fix."
        return "symbiont.py not found, no encoding fix applied"
    }
}

#--- add new folders if missing
function Add-NewFolders {
    $newFolders = @(
        "memory\embeddings",
        "memory\reflections",
        "symbiont_core\growth",
        "symbiont_core\interfaces"
    )
    $results = @()
    foreach ($folder in $newFolders) {
        $fullpath = Join-Path $ProjectRoot $folder
        $result = New-DirIfMissing $fullpath
        if ($result) { $results += $result }
    }
    return $results
}

#--- add new stub files if missing
function Add-NewStubFiles {
    $stubs = @{
        "symbiont_core\growth\mutator.py" = "class Mutator:\n    pass"
        "symbiont_core\growth\optimizer.py" = "class Optimizer:\n    pass"
        "symbiont_core\interfaces\cli_interface.py" = "def launch_cli():\n    print('CLI interface launching...')"
    }
    $results = @()
    foreach ($stub in $stubs.GetEnumerator()) {
        $path = Join-Path $ProjectRoot $stub.Key
        if (-not (Test-Path $path)) {
            $stub.Value | Set-Content -Path $path -Encoding UTF8
            Write-Host "Created stub: $path"
            $results += "Created stub: $path"
        }
    }
    return $results
}

#--- log changes to changelog
function Log-Changes {
    param (
        [string[]]$Changes
    )
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`nRunning Symbiont Project Update in $ProjectRoot"

# ensure changelog folder exists
New-DirIfMissing (Join-Path $ProjectRoot "logs")

$changes = @()

$change = Fix-SymbiontEncoding
if ($change) { $changes += $change }

$changes += Add-NewFolders
$changes += Add-NewStubFiles

if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`nUpdate complete. Changes logged to $Changelog."
}
else {
    Write-Host "`nNothing new needed. Project already up to date."
}
