<#
  File:    grow-cli.ps1
  Purpose: Grow Symbiont by adding first CLI (Command Line Interface).
           - Add CLI interface code
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

#--- write cli interface module
function Write-CLIInterfaceModule {
    $path = Join-Path $ProjectRoot "symbiont_core\interfaces\cli_interface.py"
    $code = @"
from symbiont_core.learner import Learner
from symbiont_core.reflector import Reflector

def launch_cli():
    learner = Learner()
    reflector = Reflector()

    print("\\nWelcome to the Symbiont CLI. Type 'help' for options.\\n")

    loaded_text = None
    summarized_points = None

    while True:
        command = input("Symbiont> ").strip().lower()

        if command == 'help':
            print("Commands:")
            print("  list        - list available inputs")
            print("  load [file] - load a document")
            print("  summarize   - summarize loaded document")
            print("  reflect     - reflect on summarized points")
            print("  exit        - quit CLI")

        elif command == 'list':
            files = learner.list_inputs()
            if not files:
                print("No input files found.")
            else:
                print("Available files:")
                for f in files:
                    print(f"- {f.name}")

        elif command.startswith('load '):
            parts = command.split(' ', 1)
            if len(parts) == 2:
                filename = parts[1]
                loaded_text = learner.load_input(filename)
                if loaded_text:
                    print(f"Loaded file: {filename}")
                else:
                    print("Failed to load file.")
            else:
                print("Usage: load [filename]")

        elif command == 'summarize':
            if loaded_text:
                summarized_points = learner.summarize(loaded_text)
                print("Summary:")
                for idx, point in enumerate(summarized_points, 1):
                    print(f"{idx}. {point}")
            else:
                print("No document loaded.")

        elif command == 'reflect':
            if summarized_points:
                questions = reflector.reflect_on_summary(summarized_points)
                print("Reflection Questions:")
                for q in questions:
                    print(f"- {q}")
            else:
                print("No summary available to reflect on.")

        elif command == 'exit':
            print("Goodbye.")
            break

        else:
            print("Unknown command. Type 'help' for a list.")
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
Write-Host "`n🌱 Growing Symbiont CLI Interface..."

# 1. Make sure updates folder exists
$updatesPath = Join-Path $ProjectRoot $UpdatesFolder
$updatesChange = New-DirIfMissing -Path $updatesPath

# 2. Make sure logs folder exists
$logsPath = Join-Path $ProjectRoot "logs"
$logsChange = New-DirIfMissing -Path $logsPath

# 3. Add CLI interface
$changes = @()

if ($updatesChange) { $changes += $updatesChange }
if ($logsChange) { $changes += $logsChange }

$cliResult = Write-CLIInterfaceModule
if ($cliResult) { $changes += $cliResult }

# 4. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ CLI interface grown. Changes logged."
}
else {
    Write-Host "`nNo new changes needed. Project already contained CLI."
}
