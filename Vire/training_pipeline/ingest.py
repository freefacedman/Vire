import sys
import pathlib

# --- Setup Paths ---
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

# --- Imports ---
from symbiont_core.learner import Learner
from symbiont_core.reflector import Reflector
from symbiont_core.memory_manager import MemoryManager
from symbiont_core.reflector.reflection_tree_builder import ReflectionTreeBuilder

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def guess_tags(filename):
    """Generate default tags based on filename."""
    tags = []
    name = filename.lower()

    if 'chess' in name:
        tags.append('chess')
    if 'poetry' in name:
        tags.append('poetry')
    if 'science' in name:
        tags.append('science')
    if 'philosophy' in name:
        tags.append('philosophy')

    if not tags:
        tags.append('general')

    return tags

# =========================================================
# INGESTION PIPELINE
# =========================================================
class Ingestor:
    def __init__(self):
        self.learner = Learner()
        self.reflector = Reflector()
        self.memory = MemoryManager()
        self.tree_builder = ReflectionTreeBuilder()

    def load_inputs(self):
        """List available input files."""
        return self.learner.list_inputs()

    def process_file(self, file):
        """Process a single input file."""
        safe_name = file.name.replace('.txt', '')
        print(f"\nIngesting: {file.name}")

        text = self.learner.load_input(file.name)
        if not text:
            print(f"❌ Failed to load {file.name}")
            return

        summary = self.learner.summarize(text)
        if not summary:
            print(f"⚠️ No summary generated for {file.name}")
            return

        # Print summary
        print("\nSummary:")
        for idx, point in enumerate(summary, 1):
            print(f"{idx}. {point}")

        reflections = self.reflector.reflect_on_summary(summary)

        # Print reflections
        print("\nReflections:")
        for q in reflections:
            print(f"- {q}")

        tags = guess_tags(file.name)
        self.memory.save_summary(safe_name, summary, tags=tags)
        self.memory.save_reflections(safe_name, reflections, tags=tags)
        print(f"✅ Saved summary and reflections for {safe_name} with tags {tags}")

        tree = self.tree_builder.grow_tree(reflections, layers=2)
        self.memory.save_tree(safe_name, tree)
        print(f"🌳 Saved reflection tree for {safe_name}")

    def ingest_all(self):
        """Ingest all available inputs."""
        files = self.load_inputs()
        if not files:
            print("No files to ingest.")
            return

        for file in files:
            self.process_file(file)

# =========================================================
# MAIN EXECUTION
# =========================================================
if __name__ == '__main__':
    ingestor = Ingestor()
    ingestor.ingest_all()
