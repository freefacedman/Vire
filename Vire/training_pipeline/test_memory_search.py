import sys
import pathlib

# --- Setup paths (same as ingest.py)
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from symbiont_core.memory_manager import MemoryManager

def test_memory_search():
    memory = MemoryManager()

    print("\n🔍 Searching memories for tag: 'chess'")
    results = memory.search_memories('chess')

    print("\nSummaries found:")
    for topic, data in results['summaries'].items():
        print(f"  - {topic}: {len(data['points'])} points")

    print("\nReflections found:")
    for topic, data in results['reflections'].items():
        print(f"  - {topic}: {len(data['questions'])} questions")

    print("\n✅ Search test complete.\n")

if __name__ == '__main__':
    test_memory_search()
