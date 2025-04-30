<#
  File:    grow-trainingpipeline.ps1
  Purpose: Create Symbiont Training Pipeline
           - Adds training_pipeline/ folder
           - Adds ingest.py and fine_tune.py
           - Log changes
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

#--- helper: create file if missing
function New-FileIfMissing {
    param ([string]$Path, [string]$Content = "")
    if (-not (Test-Path $Path)) {
        $Content | Out-File -Path $Path -Encoding UTF8
        Write-Host "Created file: $Path"
        return "Created file: $Path"
    }
    return $null
}

#--- build ingest.py
function Write-Ingest {
    $path = Join-Path $ProjectRoot "training_pipeline\ingest.py"
    $content = @"
from symbiont_core.learner import Learner

def ingest_all_inputs():
    learner = Learner()
    files = learner.list_inputs()
    if not files:
        print("No files to ingest.")
        return
    for f in files:
        print(f"Ingesting: {f.name}")
        text = learner.load_input(f.name)
        summary = learner.summarize(text)
        for idx, point in enumerate(summary, 1):
            print(f"{idx}. {point}")

if __name__ == '__main__':
    ingest_all_inputs()
"@
    $result = New-FileIfMissing -Path $path -Content $content
    return $result
}

#--- build fine_tune.py (placeholder)
function Write-FineTune {
    $path = Join-Path $ProjectRoot "training_pipeline\fine_tune.py"
    $content = @"
def fine_tune_model():
    print("Fine-tuning model... (future feature)")

if __name__ == '__main__':
    fine_tune_model()
"@
    $result = New-FileIfMissing -Path $path -Content $content
    return $result
}

#--- log changes
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Growing Symbiont Training Pipeline..."

# 1. Ensure updates/ and logs/ folders
New-DirIfMissing -Path (Join-Path $ProjectRoot $UpdatesFolder) | Out-Null
New-DirIfMissing -Path (Join-Path $ProjectRoot "logs") | Out-Null

# 2. Create training_pipeline/ folder
$trainingPath = Join-Path $ProjectRoot "training_pipeline"
$changes = @()

$dirChange = New-DirIfMissing -Path $trainingPath
if ($dirChange) { $changes += $dirChange }

# 3. Add ingest.py and fine_tune.py
$ingestChange = Write-Ingest
if ($ingestChange) { $changes += $ingestChange }

$fineTuneChange = Write-FineTune
if ($fineTuneChange) { $changes += $fineTuneChange }

# 4. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Training Pipeline created. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
