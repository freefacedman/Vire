<#
  File:    grow-learner.ps1
  Purpose: Grow Symbiont by adding first Learner module.
           - Ensure updates/ folder exists
           - Add real learner code
           - Track changes in logs/changes.log
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
        $Content | Out-File -FilePath $Path -Encoding UTF8
        Write-Host "Created file: $Path"
        return "Created file: $Path"
    }
    return $null
}

#--- write learner module
function Write-LearnerModule {
    $path = Join-Path $ProjectRoot "symbiont_core\learner.py"
    $code = @"
import pathlib

class Learner:
    \"\"\"Symbiont's learning module: loads and digests inputs.\"\"\"
    def __init__(self, inputs_path=None):
        self.inputs_path = pathlib.Path(inputs_path) if inputs_path else pathlib.Path(__file__).parents[2] / 'memory' / 'inputs'

    def list_inputs(self):
        \"\"\"List all available learning files.\"\"\"
        return list(self.inputs_path.glob('*.txt'))

    def load_input(self, filename):
        \"\"\"Load a specific input file as text.\"\"\"
        file_path = self.inputs_path / filename
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        else:
            return None

    def summarize(self, text):
        \"\"\"Basic digest: summarize the input to main ideas.\"\"\"
        lines = text.splitlines()
        keypoints = [line.strip() for line in lines if len(line.strip()) > 30]
        return keypoints[:5]
"@
    $result = New-FileIfMissing -Path $path -Content $code
    return $result
}

#--- helper: log growth
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Growing Symbiont Learner module..."

# 1. Make sure updates folder exists
$updatesPath = Join-Path $ProjectRoot $UpdatesFolder
$updatesChange = New-DirIfMissing -Path $updatesPath

# 2. Make sure logs folder exists
$logsPath = Join-Path $ProjectRoot "logs"
$logsChange = New-DirIfMissing -Path $logsPath

# 3. Add learner code
$changes = @()

if ($updatesChange) { $changes += $updatesChange }
if ($logsChange) { $changes += $logsChange }

$learnerResult = Write-LearnerModule
if ($learnerResult) { $changes += $learnerResult }

# 4. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Learner module grown. Changes logged."
}
else {
    Write-Host "`nNo new changes needed. Project already contained learner."
}
