<#
  File:    grow-memoryupgrade.ps1
  Purpose: Add Symbiont Memory Manager to save learning into memory folders
           - Save summaries into memory/embeddings/
           - Save reflections into memory/reflections/
           - Log all actions
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

#--- write memory_manager.py
function Write-MemoryManager {
    $path = Join-Path $ProjectRoot "symbiont_core\memory_manager.py"
    $content = @"
import pathlib
import json

class MemoryManager:
    def __init__(self):
        self.embeddings_path = pathlib.Path(__file__).resolve().parents[1] / 'memory' / 'embeddings'
        self.reflections_path = pathlib.Path(__file__).resolve().parents[1] / 'memory' / 'reflections'
        self.embeddings_path.mkdir(parents=True, exist_ok=True)
        self.reflections_path.mkdir(parents=True, exist_ok=True)

    def save_summary(self, filename, summary):
        file_path = self.embeddings_path / f"{filename}_summary.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

    def save_reflections(self, filename, reflections):
        file_path = self.reflections_path / f"{filename}_reflections.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(reflections, f, indent=2)
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
Write-Host "`n🌱 Growing Symbiont Memory Manager..."

# 1. Ensure updates/ and logs/ folders
New-DirIfMissing -Path (Join-Path $ProjectRoot $UpdatesFolder) | Out-Null
New-DirIfMissing -Path (Join-Path $ProjectRoot "logs") | Out-Null

# 2. Add memory_manager.py
$changes = @()

$memoryManagerChange = Write-MemoryManager
if ($memoryManagerChange) { $changes += $memoryManagerChange }

# 3. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Memory Manager created. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
