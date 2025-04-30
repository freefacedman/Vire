# symbiont_core/plugins/metrics.plugin.py

from symbiont_core.memory_manager import MemoryManager
import json

def metrics_cmd(args):
    """
    Show counts of summaries, reflections, trees, and tag frequencies.
    """

    mem = MemoryManager()

    # Locate files
    sum_files  = list(mem.embeddings_path.glob("*_summary.json"))
    refl_files = list(mem.reflections_path.glob("*_reflections.json"))
    tree_files = list(mem.trees_path.glob("*_tree.json"))

    # Counters
    total_points = 0
    total_questions = 0
    tag_counts = {}

    # Summaries
    for f in sum_files:
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
        if isinstance(data, list):
            pts = data
            tags = []
        else:
            pts = data.get("points", [])
            tags = data.get("tags", [])
        total_points += len(pts)
        for t in tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    # Reflections
    for f in refl_files:
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
        if isinstance(data, list):
            qs = data
            tags = []
        else:
            qs = data.get("questions", [])
            tags = data.get("tags", [])
        total_questions += len(qs)
        for t in tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    # Display
    print("\n📊 Symbiont Memory Metrics")
    print(f"  Summaries  : {len(sum_files)} files, {total_points} points total")
    print(f"  Reflections: {len(refl_files)} files, {total_questions} questions total")
    print(f"  Trees      : {len(tree_files)} files")
    if tag_counts:
        print("  Tag frequencies:")
        for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
            print(f"    • {tag}: {count}")
    print()

def register(register_command):
    register_command("metrics", metrics_cmd, aliases=["stats","m"])
