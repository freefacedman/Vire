# File: updates/setup-structure.ps1
# Usage: 
#   PS C:\Users\Riley\OneDrive\Desktop\Vire> . .\updates\setup-structure.ps1

# Resolve project root (parent of this script)
$projectRoot = Split-Path -Parent $PSScriptRoot

# Directories to ensure exist
$dirs = @(
  "symbiont_core\utils",
  "training_pipeline"
)

foreach ($rel in $dirs) {
    $full = Join-Path $projectRoot $rel
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        Write-Host "Created directory: $rel"
    }
}

# Placeholder files to touch
$files = @(
    "symbiont_core\utils\simulation_sandbox.py",
    "training_pipeline\simulation_sandbox_test.py"
)

foreach ($rel in $files) {
    $full = Join-Path $projectRoot $rel
    if (-not (Test-Path $full)) {
        New-Item -ItemType File -Path $full -Force | Out-Null
        Write-Host "Created placeholder file: $rel"
    }
}

Write-Host "`n✅ Project structure is ready. You can now populate these files."  
