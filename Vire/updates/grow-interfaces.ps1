<#
  File:    grow-interfaces.ps1
  Purpose: Rebuild missing symbiont_core/interfaces/ folder structure
           - Create interfaces/
           - Add __init__.py
           - Add cli_interface.py with real code
           - Log everything
#>

param (
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$UpdatesFolder = "updates",
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
        $Content | Set-Content -Path $Path -Encoding UTF8
        Write-Host "Created file: $Path"
        return "Created file: $Path"
    }
    return $null
}

#--- actual CLI interface code
function Write-CliInterfaceFile {
    $path = Join-Path $ProjectRoot "symbiont_core\interfaces\cli_interface.py"
    $content = @"
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
    $result = New-FileIfMissing -Path $path -Content $content
    return $result
}

#--- log growth
function Log-Changes {
    param ([string[]]$Changes)
    $timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    $entry = "`n[$timestamp]`n" + ($Changes -join "`n") + "`n"
    Add-Content -Path (Join-Path $ProjectRoot $Changelog) -Value $entry
}

#--- MAIN EXECUTION ---------------------------------------------------------
Write-Host "`n🌱 Growing Symbiont Interfaces folder and CLI..."

# 1. Ensure updates/ and logs/ folders
New-DirIfMissing -Path (Join-Path $ProjectRoot $UpdatesFolder) | Out-Null
New-DirIfMissing -Path (Join-Path $ProjectRoot "logs") | Out-Null

# 2. Create interfaces/ folder
$interfacesPath = Join-Path $ProjectRoot "symbiont_core\interfaces"
$changes = @()

$dirChange = New-DirIfMissing -Path $interfacesPath
if ($dirChange) { $changes += $dirChange }

# 3. Add __init__.py and cli_interface.py
$initChange = New-FileIfMissing -Path (Join-Path $interfacesPath "__init__.py")
if ($initChange) { $changes += $initChange }

$cliChange = Write-CliInterfaceFile
if ($cliChange) { $changes += $cliChange }

# 4. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Interfaces folder and CLI created. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
