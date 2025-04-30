<#
  File:    grow-inputexamples.ps1
  Purpose: Create proper example .txt files in memory/inputs/ for Symbiont
           - Write real visible contents
           - No errors, no broken -Path issues
#>

param (
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$InputsFolder = "memory\inputs",
    [string]$Changelog = "logs\changes.log"
)

#--- helper: create directory if missing
function New-DirIfMissing {
    param ([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created folder: $Path"
        return "Created folder: $Path"
    }
    return $null
}

#--- helper: actually create example .txt files
function Create-ExampleInputs {
    param ([string]$FolderPath)

    $examples = @{
        "philosophy.txt" = @"
Reality is often stranger than fiction.
The human condition is defined by its ceaseless search for meaning.
In a universe indifferent to our struggles, we find purpose through connection.
"@

        "science.txt" = @"
Gravity is the curvature of spacetime caused by mass.
All observable matter follows the principles outlined in the Standard Model of physics.
New fields such as quantum mechanics suggest deep, nonlocal entanglement between particles.
"@

        "poetry.txt" = @"
The river runs silent but not still, carrying forgotten dreams.
Beneath the ancient oak, whispers gather in mossy twilight.
Every ending is a beginning wearing a mask of sorrow.
"@
    }

    $created = @()
    foreach ($entry in $examples.GetEnumerator()) {
        $path = Join-Path $FolderPath $entry.Key
        if (-not (Test-Path $path)) {
            [System.IO.File]::WriteAllText($path, $entry.Value.Trim(), [System.Text.Encoding]::UTF8)
            Write-Host "Created example file: $path"
            $created += "Created example input: $path"
        }
    }
    return $created
}

#--- helper: log changes
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Growing Symbiont Input Examples (Fixed)..."

# 1. Ensure memory/inputs/ exists
$inputsPath = Join-Path $ProjectRoot $InputsFolder
New-DirIfMissing -Path $inputsPath | Out-Null

# 2. Create example input files
$changes = @()

$createdExamples = Create-ExampleInputs -FolderPath $inputsPath
if ($createdExamples) {
    $changes += $createdExamples
}

# 3. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Example input files created and populated. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
