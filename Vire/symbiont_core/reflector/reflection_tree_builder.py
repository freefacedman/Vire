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
