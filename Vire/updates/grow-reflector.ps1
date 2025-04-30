<#
  File:    grow-reflector.ps1
  Purpose: Grow Symbiont by adding first Reflector module.
           - Ensure updates/ folder exists
           - Add real reflector code
           - Log changes in logs/changes.log
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

#--- write reflector module
function Write-ReflectorModule {
    $path = Join-Path $ProjectRoot "symbiont_core\reflector.py"
    $code = @"
class Reflector:
    \"\"\"Symbiont's reflection module: generates self-questions based on learnings.\"\"\"
    def __init__(self):
        pass

    def reflect_on_summary(self, summary):
        \"\"\"Given a summary list, create reflection questions.\"\"\"
        questions = []
        for point in summary:
            questions.append(f'Why is "{point}" important?')
            questions.append(f'What assumptions are hidden inside "{point}"?')
        return questions
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
Write-Host "`n🌱 Growing Symbiont Reflector module..."

# 1. Make sure updates folder exists
$updatesPath = Join-Path $ProjectRoot $UpdatesFolder
$updatesChange = New-DirIfMissing -Path $updatesPath

# 2. Make sure logs folder exists
$logsPath = Join-Path $ProjectRoot "logs"
$logsChange = New-DirIfMissing -Path $logsPath

# 3. Add reflector code
$changes = @()

if ($updatesChange) { $changes += $updatesChange }
if ($logsChange) { $changes += $logsChange }

$reflectorResult = Write-ReflectorModule
if ($reflectorResult) { $changes += $reflectorResult }

# 4. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Reflector module grown. Changes logged."
}
else {
    Write-Host "`nNo new changes needed. Project already contained reflector."
}
