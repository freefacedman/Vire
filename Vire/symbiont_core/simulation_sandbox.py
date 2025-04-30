from symbiont_core.memory_manager import MemoryManager
from symbiont_core.reflector import Reflector
from symbiont_core.reflector.reflection_tree_builder import ReflectionTreeBuilder

class SimulationEngine:
    """
    Builds a “what-if” tree of possible next states from
    a starting scenario, using either tagged memories
    or fresh reflections.
    """
    def __init__(self, memory_manager=None, reflector=None, tree_builder=None):
        self.mem          = memory_manager or MemoryManager()
        self.reflector    = reflector        or Reflector()
        self.tree_builder = tree_builder     or ReflectionTreeBuilder()

    def simulate(self, scenario, depth=3, tag_hint=None):
        """
        scenario : str          – textual “starting state”
        depth    : int          – number of projection layers
        tag_hint : str or None  – if set, biases pulling reflections by this tag

        returns: nested dict { state: [possible_next_state, …], … }
        """
        tree    = { scenario: [] }
        current = [scenario]

        for level in range(depth):
            next_round = []
            for state in current:
                # choose reflections by tag or fresh
                if tag_hint:
                    hits = self.mem.search_reflections_by_tag(tag_hint) \
                                   .get(tag_hint, {}) \
                                   .get("questions", [])
                else:
                    hits = self.reflector.reflect_on_summary([state])
                tree[state] = hits
                next_round.extend(hits)
            current = next_round

        return tree
