# File: training_pipeline/live_chat.py

"""
Live Chat CLI for Symbiont:
- Memory search (tag-based)
- Reflection trees
- What-if simulations
- Dynamic plugin loading
- Command aliases, shlex parsing, default depths
- Hot-reload core modules
- Ctrl-C guard
- Automatic learning prompt
"""

import sys
import pathlib
import json
import importlib
import importlib.util
import shlex
import random
import datetime
import traceback
import types

# -------------------------------------------------------------------
# Project root path
# -------------------------------------------------------------------
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# -------------------------------------------------------------------
# Optional readline for history
# -------------------------------------------------------------------
try:
    import readline  # Unix
except ImportError:
    try:
        import pyreadline3 as readline  # Windows
    except ImportError:
        readline = None

# -------------------------------------------------------------------
# Hot-reload helper
# -------------------------------------------------------------------
def hot_reload(module: types.ModuleType):
    try:
        importlib.reload(module)
    except Exception:
        traceback.print_exc()

# -------------------------------------------------------------------
# Import & reload core modules
# -------------------------------------------------------------------
import symbiont_core.memory_manager          as _mm;  hot_reload(_mm)
import symbiont_core.reflector               as _rf;  hot_reload(_rf)
import symbiont_core.reflector.reflection_tree_builder as _rtb; hot_reload(_rtb)
import symbiont_core.simulation_sandbox      as _ssb; hot_reload(_ssb)

MemoryManager         = _mm.MemoryManager
Reflector             = _rf.Reflector
ReflectionTreeBuilder = _rtb.ReflectionTreeBuilder
SimulationEngine      = _ssb.SimulationEngine

# -------------------------------------------------------------------
# Load config (handle BOM)
# -------------------------------------------------------------------
cfg = {
    "tree_default": 2,
    "sim_default": 3,
    "aliases": {
        "s":    "search", "se": "search",
        "t":    "tree",   "tr": "tree",
        "sim":  "simulate",
        "h":    "help",   "?":  "help",
        "q":    "exit",   "quit":"exit"
    }
}
config_path = PROJECT_ROOT / "config" / "settings.json"
if config_path.exists():
    try:
        with open(config_path, encoding="utf-8-sig") as f:
            cfg.update(json.load(f))
    except Exception:
        traceback.print_exc()

# -------------------------------------------------------------------
# Command registry
# -------------------------------------------------------------------
from typing import Callable, List, Dict
CommandFunc = Callable[[List[str]], None]
REGISTRY: Dict[str, CommandFunc] = {}

def register_command(name: str, func: CommandFunc, aliases: List[str] = []):
    REGISTRY[name] = func
    for a in aliases:
        cfg["aliases"][a] = name

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def split_cmd(line: str):
    return shlex.split(line)

def parse_depth_and_text(tokens: List[str], default_depth: int):
    if tokens and tokens[-1].isdigit():
        depth = int(tokens[-1])
        text = " ".join(tokens[:-1]).strip()
    else:
        depth = default_depth
        text = " ".join(tokens).strip()
    return text, depth

# -------------------------------------------------------------------
# Memory snapshot & refresh
# -------------------------------------------------------------------
def snapshot_memory():
    mem = MemoryManager()
    sums_raw = mem.load_all_summaries()
    refl_raw = mem.load_all_reflections()
    sums = {k: (v if isinstance(v, list) else v.get("points", [])) for k, v in sums_raw.items()}
    refl = {k: (v if isinstance(v, list) else v.get("questions", [])) for k, v in refl_raw.items()}
    trees = {}
    tdir = PROJECT_ROOT / "memory" / "trees"
    if tdir.exists():
        for fp in tdir.glob("*.json"):
            try:
                with open(fp, encoding="utf-8") as f:
                    trees[fp.stem] = json.load(f)
            except Exception:
                traceback.print_exc()
    return mem, sums, refl, trees

MEM, SUMS, REFL, TREES = snapshot_memory()

def refresh_memory():
    global MEM, SUMS, REFL, TREES
    MEM, SUMS, REFL, TREES = snapshot_memory()

# -------------------------------------------------------------------
# Learning helper
# -------------------------------------------------------------------
def save_chat(text: str):
    mem = MemoryManager()
    refl = Reflector()
    builder = ReflectionTreeBuilder()

    summary = [text]
    reflections = refl.reflect_on_summary(summary)
    tree = builder.grow_tree(reflections, layers=cfg["tree_default"])

    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name = f"chat{ts}"

    mem.save_summary(name, summary, tags=["chat"])
    mem.save_reflections(name, reflections, tags=["chat"])
    mem.save_tree(name, tree)

    print(f"\n✅ Learned & stored new chat memory: {name}\n")

# -------------------------------------------------------------------
# Built-in commands
# -------------------------------------------------------------------
def cmd_search(args):
    if not args:
        print("Usage: search [tag]")
        return
    tag = args[0].lower()
    res = MEM.search_memories(tag)
    if not res["summaries"] and not res["reflections"]:
        print(f"⚠️  No memories tagged '{tag}'.")
        return
    print(f"\n🔍 Memories tagged '{tag}':")
    for topic, data in res["summaries"].items():
        for i, p in enumerate(data["points"], 1):
            print(f"  [S] {topic} {i}. {p}")
    for topic, data in res["reflections"].items():
        for i, q in enumerate(data["questions"], 1):
            print(f"  [R] {topic} {i}. {q}")

def cmd_tree(args):
    if not args:
        print("Usage: tree [tag] [layers]")
        return
    tag, layers = parse_depth_and_text(args, cfg["tree_default"])
    hits = MEM.search_reflections_by_tag(tag)
    if not hits:
        print(f"⚠️  No reflections for tag '{tag}'.")
        return
    builder = ReflectionTreeBuilder()
    print(f"\n🌲 Reflection trees for '{tag}' ({layers} layers):")
    for topic, data in hits.items():
        print(f"\n⤷ Topic: {topic}")
        tree = builder.grow_tree(data["questions"], layers=layers)
        def walk(d, indent=1):
            for parent, children in d.items():
                print("  "*indent + f"- {parent}")
                if children:
                    walk({c: d.get(c, []) for c in children}, indent+1)
        walk(tree)

def cmd_simulate(args):
    if not args:
        print("Usage: simulate [text] [layers]")
        return
    text, depth = parse_depth_and_text(args, cfg["sim_default"])
    engine = SimulationEngine(MEM, Reflector(), ReflectionTreeBuilder())
    sim_tree = engine.simulate(text, depth=depth, tag_hint=text)
    print(f"\n🔮 Simulation from '{text}' ({depth} layers):")
    def walk(d, indent=0):
        for state, outs in d.items():
            print("  "*indent + f"> {state}")
            for o in outs:
                print("  "*(indent+1) + f"- {o}")
    walk(sim_tree)

def cmd_help(args):
    print("\nCommands:")
    for name in sorted(REGISTRY):
        aliases = [a for a, cmd in cfg["aliases"].items() if cmd == name and a != name]
        alias_str = f" ({', '.join(aliases)})" if aliases else ""
        print(f"  {name}{alias_str}")
    print()

def cmd_exit(args):
    print("🌱 Goodbye.")
    sys.exit(0)

# -------------------------------------------------------------------
# Register built-ins
# -------------------------------------------------------------------
register_command("search",   cmd_search,   aliases=["s","se"])
register_command("tree",     cmd_tree,     aliases=["t","tr"])
register_command("simulate", cmd_simulate, aliases=["sim"])
register_command("help",     cmd_help,     aliases=["h","?"])
register_command("exit",     cmd_exit,     aliases=["q","quit"])

# -------------------------------------------------------------------
# Plugin auto-loader
# -------------------------------------------------------------------
PLUGINS_DIR = PROJECT_ROOT / "symbiont_core" / "plugins"
if PLUGINS_DIR.exists():
    for f in PLUGINS_DIR.glob("*.plugin.py"):
        try:
            spec = importlib.util.spec_from_file_location(f.stem, str(f))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "register"):
                mod.register(register_command)
        except Exception:
            traceback.print_exc()

# -------------------------------------------------------------------
# Main loop
# -------------------------------------------------------------------
def main_loop():
    print("\n🌳 Symbiont Live Chat (type 'help')\n")
    while True:
        try:
            line = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n(use 'exit' to quit)")
            continue
        if not line:
            continue

        refresh_memory()

        tokens = split_cmd(line)
        key = tokens[0].lower()
        key = cfg["aliases"].get(key, key)
        func = REGISTRY.get(key)

        if func:
            try:
                func(tokens[1:])
            except Exception:
                traceback.print_exc()
        else:
            # fuzzy fallback
            q = line.lower()
            matches = []
            matches += [("summary", t, p)     for t, ps in SUMS.items()  for p in ps if q in p.lower()]
            matches += [("reflection", t, qn) for t, qs in REFL.items() for qn in qs if q in qn.lower()]
            for t, tr in TREES.items():
                for parent, kids in tr.items():
                    if q in parent.lower():
                        matches.append(("tree", t, parent))
                    matches += [("tree", t, c) for c in kids if q in c.lower()]

            if not matches:
                opt = random.choice([
                    f"If we probe deeper, consider: '{line}…'",
                    f"This might hint at: '{line}…'",
                    f"Imagine if: '{line}…'",
                    f"Under the surface, '{line}' reveals layers."
                ])
                print("\nSymbiont> " + opt + "\n")
            else:
                kind, topic, thought = random.choice(matches)
                print(f"\nSymbiont> Reflecting on '{topic}' ({kind}):\n  \"{thought}\"")
                print("Symbiont> " + random.choice([
                    f"Consider deeper: '{thought}…'",
                    f"Could imply: '{thought}…'",
                    f"Stretching: '{thought}…'",
                    f"Under the surface, '{thought}'…"
                ]) + "\n")

        # prompt to learn
        try:
            yn = input("🌱 Learn from this? (y/N): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            yn = ""
        if yn.startswith("y"):
            save_chat(line)

if __name__ == "__main__":
    main_loop()
