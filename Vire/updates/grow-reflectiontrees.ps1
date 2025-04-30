<#
  File:    grow-reflectiontrees.ps1
  Purpose: Fully rebuild Reflection Tree Builder
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

#--- write reflection_tree_builder.py
function Write-ReflectionTreeBuilder {
    # Ensure reflector folder exists first
    $reflectorFolder = Join-Path $ProjectRoot "symbiont_core\reflector"
    New-DirIfMissing -Path $reflectorFolder | Out-Null

    $path = Join-Path $reflectorFolder "reflection_tree_builder.py"
    $content = @"
import pathlib
import json

class ReflectionTreeBuilder:
    def __init__(self):
        self.trees_path = pathlib.Path(__file__).resolve().parents[2] / 'memory' / 'trees'
        self.trees_path.mkdir(parents=True, exist_ok=True)

    def grow_tree(self, reflections, layers=2):
        tree = {}
        current_layer = reflections
        for depth in range(layers):
            next_layer = []
            for reflection in current_layer:
                sub_questions = [
                    f'Why is \"{reflection}\" significant?',
                    f'What could challenge \"{reflection}\"?'
                ]
                tree[reflection] = sub_questions
                next_layer.extend(sub_questions)
            current_layer = next_layer
        return tree

    def save_tree(self, filename, tree):
        file_path = self.trees_path / f"{filename}_tree.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(tree, f, indent=2)
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
Write-Host "`n🌱 Rebuilding Reflection Tree Builder..."

# 1. Ensure updates/, logs/, reflector/, trees/ folders
New-DirIfMissing -Path (Join-Path $ProjectRoot $UpdatesFolder) | Out-Null
New-DirIfMissing -Path (Join-Path $ProjectRoot "logs") | Out-Null
New-DirIfMissing -Path (Join-Path $ProjectRoot "symbiont_core\reflector") | Out-Null
New-DirIfMissing -Path (Join-Path $ProjectRoot "memory\trees") | Out-Null

# 2. Add reflection_tree_builder.py
$changes = @()

$treeBuilderChange = Write-ReflectionTreeBuilder
if ($treeBuilderChange) { $changes += $treeBuilderChange }

# 3. Log changes
if ($changes.Count -gt 0) {
    Log-Changes -Changes $changes
    Write-Host "`n✅ Reflection Tree Builder rebuilt cleanly. Changes logged."
}
else {
    Write-Host "`nNo new changes needed."
}
