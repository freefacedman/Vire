import pathlib
import json

class MemoryManager:
    def __init__(self):
        # --- Initialization ---
        self.embeddings_path = pathlib.Path(__file__).resolve().parents[2] / "memory" / "embeddings"
        self.reflections_path = pathlib.Path(__file__).resolve().parents[2] / "memory" / "reflections"
        self.trees_path = pathlib.Path(__file__).resolve().parents[2] / "memory" / "trees"
        self.embeddings_path.mkdir(parents=True, exist_ok=True)
        self.reflections_path.mkdir(parents=True, exist_ok=True)
        self.trees_path.mkdir(parents=True, exist_ok=True)

    # =========================================================
    # SUMMARY MANAGEMENT
    # =========================================================
    def save_summary(self, filename, summary, tags=None):
        """Save a single summary with optional tags to the embeddings folder."""
        data = {
            "tags": tags or [],
            "points": summary
        }
        file_path = self.embeddings_path / f"{filename}_summary.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_summary(self, filename):
        """Load a specific summary from the embeddings folder."""
        file_path = self.embeddings_path / f"{filename}_summary.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def load_all_summaries(self):
        """Load all summaries from the embeddings folder."""
        summary_files = self.embeddings_path.glob("*_summary.json")
        summaries = {}
        for file in summary_files:
            topic = file.stem.replace("_summary", "")
            with open(file, "r", encoding="utf-8") as f:
                summaries[topic] = json.load(f)
        return summaries

    # =========================================================
    # REFLECTIONS MANAGEMENT
    # =========================================================
    def save_reflections(self, filename, reflections, tags=None):
        """Save reflections with optional tags to the reflections folder."""
        data = {
            "tags": tags or [],
            "questions": reflections
        }
        file_path = self.reflections_path / f"{filename}_reflections.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_reflections(self, filename):
        """Load specific reflections from the reflections folder."""
        file_path = self.reflections_path / f"{filename}_reflections.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def load_all_reflections(self):
        """Load all reflections from the reflections folder."""
        reflection_files = self.reflections_path.glob("*_reflections.json")
        reflections = {}
        for file in reflection_files:
            topic = file.stem.replace("_reflections", "")
            with open(file, "r", encoding="utf-8") as f:
                reflections[topic] = json.load(f)
        return reflections

    # =========================================================
    # REFLECTION TREE MANAGEMENT
    # =========================================================
    def save_tree(self, filename, tree):
        """Save a reflection tree to the trees folder."""
        file_path = self.trees_path / f"{filename}_tree.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tree, f, indent=2, ensure_ascii=False)

    def load_tree(self, filename):
        """Load a specific reflection tree from the trees folder."""
        file_path = self.trees_path / f"{filename}_tree.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    # =========================================================
    # SMART MEMORY SEARCH (with LEGACY PATCH)
    # =========================================================
    def search_summaries_by_tag(self, search_tag):
        """Search summaries by tag."""
        matches = {}
        for file in self.embeddings_path.glob("*_summary.json"):
            topic = file.stem.replace("_summary", "")
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # --- Legacy patch ---
                if isinstance(data, list):
                    data = {"tags": ["legacy"], "points": data}
                tags = data.get("tags", [])
                if search_tag in tags:
                    matches[topic] = data
        return matches

    def search_reflections_by_tag(self, search_tag):
        """Search reflections by tag."""
        matches = {}
        for file in self.reflections_path.glob("*_reflections.json"):
            topic = file.stem.replace("_reflections", "")
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # --- Legacy patch ---
                if isinstance(data, list):
                    data = {"tags": ["legacy"], "questions": data}
                tags = data.get("tags", [])
                if search_tag in tags:
                    matches[topic] = data
        return matches

    def search_memories(self, search_tag):
        """Search summaries and reflections by tag."""
        summary_matches = self.search_summaries_by_tag(search_tag)
        reflection_matches = self.search_reflections_by_tag(search_tag)
        return {
            "summaries": summary_matches,
            "reflections": reflection_matches
        }
