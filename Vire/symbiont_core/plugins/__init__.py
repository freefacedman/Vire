import importlib
from pathlib import Path

def load_all(register_command):
    """
    Auto-load every *.plugin.py in this folder and
    call its register(register_command) if present.
    """
    plug_dir = Path(__file__).parent
    for f in plug_dir.glob("*.plugin.py"):
        mod = importlib.import_module(f"symbiont_core.plugins.{f.stem}")
        if hasattr(mod, "register"):
            mod.register(register_command)
