# File: updates/setup-plugins.ps1
# Usage: 
#   PS C:\Users\Riley\OneDrive\Desktop\Vire> . .\updates\setup-plugins.ps1

# Resolve project root (parent of this script)
$projectRoot = Split-Path -Parent $PSScriptRoot

# Plugins folder
$pluginsDir = Join-Path $projectRoot "symbiont_core\plugins"

# Create plugins directory if missing
if (-not (Test-Path $pluginsDir)) {
    New-Item -ItemType Directory -Path $pluginsDir -Force | Out-Null
    Write-Host "Created directory: symbiont_core\plugins"
}

# __init__.py for plugin loader
$initFile = Join-Path $pluginsDir "__init__.py"
if (-not (Test-Path $initFile)) {
    @"
import importlib
from pathlib import Path

def load_all(register_command):
    \"\"\"
    Auto-load every *.plugin.py in this folder and
    call its register(register_command) if present.
    \"\"\"
    plug_dir = Path(__file__).parent
    for f in plug_dir.glob("*.plugin.py"):
        mod = importlib.import_module(f"symbiont_core.plugins.{f.stem}")
        if hasattr(mod, "register"):
            mod.register(register_command)
"@ | Out-File -FilePath $initFile -Encoding UTF8
    Write-Host "Created file: symbiont_core\plugins\__init__.py"
}

# Sample wiki plugin
$wikiFile = Join-Path $pluginsDir "wiki.plugin.py"
if (-not (Test-Path $wikiFile)) {
    @"
from symbiont_core.memory_manager import MemoryManager

def wiki_cmd(args):
    if not args:
        print(\"Usage: wiki [topic]\")
        return
    topic = \" \".join(args)
    # Placeholder – replace with real API call.
    print(f\"\n🌐 Wikipedia summary for '{topic}':\")
    print(\"  [This is a stub. Hook up the real API in wiki.plugin.py]\\n\")

def register(register_command):
    register_command(\"wiki\", wiki_cmd, aliases=[\"w\",\"define\"])
"@ | Out-File -FilePath $wikiFile -Encoding UTF8
    Write-Host "Created file: symbiont_core\plugins\wiki.plugin.py"
}

Write-Host "`n✅ Plugin scaffold complete. You can now drop additional *.plugin.py files into symbiont_core\plugins.`n"
